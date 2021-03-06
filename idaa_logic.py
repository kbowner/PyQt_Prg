import ibm_db, sqlparse, logging, os, os.path

cDATABASE = "SAMPLE"
cHOSTNAME = "192.168.253.128"
cPORT = "50000"
cPROTOCOL = "TCPIP"
cUID = "db2inst1"
cPWD = "db2inst1"
standard_audit_col_list = ['ROW_STAT_CD', 'INSRT_TMS', 'UPDT_TMS']

conn = ibm_db.connect(f"DATABASE={cDATABASE};HOSTNAME={cHOSTNAME};PORT={cPORT};PROTOCOL={cPROTOCOL};UID={cUID};PWD={cPWD};", "", "")

# Output directory for IDAA views ddl files, logs, etc
#f_pda_list = "C:\PERSONAL\PYTHON_PRG\pda_view_list.txt"
output_directory = "d:\Work\PyQt_Prg\DDL"
fLog = "IDAA_session.out"

# Dictionary to check and compare audit columns in both views PDA and DB2
audit_col_status_code = {
    1: 'Audit columns: YES (PDA and DB2); Last 3 columns and order are the same.',
    2: 'Audit columns: YES (PDA and DB2); Last 3 columns are the same, but the order is different.',
    3: 'Audit columns: NO (PDA and DB2); Both views have the same num of column.',
    4: 'Audit columns: NO (PDA and DB2); Both views column count is different!',
    5: 'Audit columns: YES (DB2) and NO (PDA); Both views column count is different!',
    6: 'Audit columns: NO (DB2) and YES (PDA); Both views column count is different!',
    7: 'Audit columns: YES (DB2) and NO (PDA); But views column count is the same!',
    8: 'Audit columns: NO (DB2) and YES (PDA); But views column count is the same!',
    9: 'Check columns and fix header/body of the view!',
    10: 'Audit columns: NO (DB2) and YES (PDA); Both views column count is different! Will remove 3 last audit columns.'}
# in case of it.6 and if a difference are audit columns list, then need to remove last 3 columns from the view header

def IDAA_view_to_file (pda_schema, pda_view, bmsiw_schema, bmsiw_view):

    fname = pda_schema.upper() + "." + pda_view.upper()

    # fname_abs - is a full file name for the view DDL
    fname_abs = output_directory + "\\" + fname + ".DDL"
    if os.path.exists(fname_abs):
        os.remove(fname_abs)
    f = open(fname_abs, "a")
    f.write("-- " + "#" * 80+"\n")
    f.write(f"-- # PDA view: {nz_schema:>23}.{nz_view}\n")
    f.write(f"-- # Legacy view: {bmsiw_schema:>20}.{bmsiw_view}\n")
    f.write("-- " + "#" * 80+"\n")
    f.write("\n")

    level_audit_cols = 0
    level_audit_cols = get_view_row_count('PDA', nz_schema, nz_view) - get_view_row_count('DB2', bmsiw_schema,
                                                                                          bmsiw_view)
    idaa_view_header = print_idaa_view_header(nz_schema, nz_view, level_audit_cols)
    idaa_view_statement = get_bmsiw_view_body(bmsiw_schema, bmsiw_view)
    cur_sqlid = "SIWASDBA"
    idaa_label = "\nLABEL ON TABLE " + pda_schema.upper() + "." + pda_view.upper() + " IS 'IDAA " + pda_schema.upper() + "';\n"
    f.write("\nSET CURRENT SQLID = '" + cur_sqlid + "';\n")
    f.write(sqlparse.format(idaa_view_header, reindent=True, wrap_after=True, truncate_strings=80))
    f.write(sqlparse.format(idaa_view_statement, reindent=True, wrap_after=True, truncate_strings=80)+"\n")
    f.write(idaa_label)
    f.write("\n")
    f.close()


def log_print(msg):
    logging.basicConfig(format='%(message)s', level=logging.INFO, filename=flog_abs)
    logging.info(msg)


def get_legacy_view_name(pda_schema, pda_view):
    sql = f"SELECT OLD_SCHEMA, OLD_VIEW_NAME FROM IDAA.PDA_VIEW_MAP WHERE NEW_SCHEMA = '{pda_schema}' AND NEW_VIEW_NAME = '{pda_view}' FETCH FIRST 1 ROW ONLY;"
    stmt = ibm_db.exec_immediate(conn, sql)
    tuple = ibm_db.fetch_tuple(stmt)
    while tuple:
        return tuple[0], tuple[1]
        tuple = ibm_db.fetch_tuple(stmt)

def get_idaa_view_header(pda_schema, pda_view,level_audit_cols):
    sql = f"SELECT COLNAME||',' FROM IDAA.PDA_REL_COLUMNS WHERE CREATOR = '{pda_schema}' AND NAME = '{pda_view}' ORDER BY COLNO;"
    stmt = ibm_db.exec_immediate(conn, sql)
    s2 = ibm_db.fetch_tuple(stmt)
    cols = []
    while s2:
        cols.append (s2[0])
        s2 = ibm_db.fetch_tuple(stmt)
    s1 = "CREATE VIEW " + pda_schema + "." + pda_view + " ("
    col_list_len = len(cols)

    #remove 3 last audit columns in header
    if level_audit_cols == 3:
      col_list_len = col_list_len - 3
    i=0
    col_list = []
    for i in range (0,col_list_len-1):
        if (i<col_list_len-1):
            col_list.append(cols[i])
    last_col = cols[i + 1]
    col_list.append(last_col[:-1])
    s3 = ")"
    return s1, col_list, s3

def print_idaa_view_header(schema, view, level_audit_cols, edit_col_list):
    #col_list = []
    header_begin, col_list, header_end = get_idaa_view_header(schema, view, level_audit_cols)
    s = ""
    for items in edit_col_list:
        s = s + ", " + items
    s = s[1:]
    idaa_header = header_begin+ " " + s + " " + header_end
    return idaa_header

def get_bmsiw_view_body(schema, view):
    sql = f"SELECT STMT, LENGTH(STMT) AS LENS FROM IDAA.BMSIW_VIEWS WHERE SCHEMA = '{schema}' AND VIEWNAME = '{view}';"
    stmt = ibm_db.exec_immediate(conn, sql)
    stmt_len = 0
    stmt_txt = ""
    res = ibm_db.fetch_tuple(stmt)
    while res:
        stmt_len = res[1]
        stmt_txt = res[0]
        res = ibm_db.fetch_tuple(stmt)
    view_body = stmt_txt[stmt_txt.find(' AS '):]+';'
    return view_body

def get_view_row_count(src_db, schema, view):
    #src_db - either PDA or DB2
    if src_db == 'DB2':
        sql = f"SELECT COUNT(*) AS CNT FROM IDAA.BMSIW_COLUMNS WHERE SCHEMA = '{schema}' AND VIEWNAME = '{view}';"
    elif src_db == 'PDA':
        sql = f"SELECT COUNT(*) AS CNT FROM IDAA.PDA_REL_COLUMNS WHERE CREATOR = '{schema}' AND NAME = '{view}';"
    else:
        print('ERROR: Data not found!')
    stmt = ibm_db.exec_immediate(conn, sql)
    res = ibm_db.fetch_tuple(stmt)
    while res:
        return res[0]
        res = ibm_db.fetch_tuple(stmt)

def check_audit_col (src_db, schema, view):
    # check if there are audit columns in PDA and BMSIW views
    # src_db - either PDA or DB2
    aud_col_list = []

    if src_db == 'DB2':
        sql = f"SELECT COLNAME, COLNO FROM IDAA.BMSIW_COLUMNS WHERE SCHEMA = '{schema}' AND "\
                f"VIEWNAME = '{view}' ORDER BY COLNO DESC FETCH FIRST 3 ROWS ONLY;"
    elif src_db == 'PDA':
        sql = f"SELECT COLNAME, COLNO FROM IDAA.PDA_REL_COLUMNS WHERE CREATOR = '{schema}' AND "\
                f"NAME = '{view}' ORDER BY COLNO DESC FETCH FIRST 3 ROWS ONLY;"

    else:
        #print('ERROR: Data not found!')
        return aud_col_list

    stmt = ibm_db.exec_immediate(conn, sql)
    res = ibm_db.fetch_tuple(stmt)

    while res:
        aud_col_list.append(res[0])
        res = ibm_db.fetch_tuple(stmt)
    aud_col_list.reverse()

    return aud_col_list


def compare_audit_col2(db2_list, pda_list):
    res = 0
    print("Here!")
    # Now check the order of the audit columns
    if (all(x in db2_list for x in pda_list)) and (db2_list == standard_audit_col_list) and (db2_list == pda_list):
        res = 1
    elif (all(x in db2_list for x in pda_list)) and (db2_list == standard_audit_col_list) and (db2_list != pda_list):
        res = 2
    elif (db2_list != standard_audit_col_list) and (pda_list != standard_audit_col_list) \
            and (get_view_row_count('DB2', bmsiw_schema, bmsiw_view) == get_view_row_count('PDA', nz_schema, nz_view)):
        res = 3
    elif (db2_list != standard_audit_col_list) and (pda_list != standard_audit_col_list) \
            and (get_view_row_count('DB2', bmsiw_schema, bmsiw_view) != get_view_row_count('PDA', nz_schema, nz_view)):
        res = 4
    elif (db2_list == standard_audit_col_list) and (pda_list != standard_audit_col_list) \
            and (get_view_row_count('DB2', bmsiw_schema, bmsiw_view) != get_view_row_count('PDA', nz_schema, nz_view)):
        res = 5
    elif (db2_list != standard_audit_col_list) and (pda_list == standard_audit_col_list) \
            and (get_view_row_count('DB2', bmsiw_schema, bmsiw_view) != get_view_row_count('PDA', nz_schema, nz_view)):
        res = 6
        # if a difference are audit columns list, then need to remove last 3 columns from the view header
        if (get_view_row_count('PDA', nz_schema, nz_view) - get_view_row_count('DB2', bmsiw_schema, bmsiw_view)) == 3:
            res = 10
    elif (db2_list == standard_audit_col_list) and (pda_list != standard_audit_col_list) \
            and (get_view_row_count('DB2', bmsiw_schema, bmsiw_view) == get_view_row_count('PDA', nz_schema, nz_view)):
        res = 7
    elif (db2_list != standard_audit_col_list) and (pda_list == standard_audit_col_list) \
            and (get_view_row_count('DB2', bmsiw_schema, bmsiw_view) == get_view_row_count('PDA', nz_schema, nz_view)):
        res = 8
    else:
        res = 9
    print ("Here!")
    return res

def IDAA_proceed_single_view (nz_schema, nz_view,  bmsiw_schema, bmsiw_view):

    # Next section is commented out - for console output
    # ----------------
    # print("--", "#" * 80)
    # print(f"-- # PDA view: {nz_schema:>23}.{nz_view}")
    # print(f"-- # Legacy view: {bmsiw_schema:>20}.{bmsiw_view}")
    # print("--", "#")
    # print("--", f"# Legacy view column count = {get_view_row_count('DB2', bmsiw_schema, bmsiw_view):>5}")
    # print("--", f"# PDA view column count = {get_view_row_count('PDA', nz_schema, nz_view):>8}")
    # print("--","#"*80)
    # idaa_view_header = print_idaa_view_header(nz_schema, nz_view)
    # idaa_view_statement = get_bmsiw_view_body(bmsiw_schema, bmsiw_view)
    # print(sqlparse.format(idaa_view_header, reindent=True, wrap_after=True, truncate_strings=80))
    # print(sqlparse.format(idaa_view_statement, reindent=True, wrap_after=True, truncate_strings=80))
    # ----------------

############## This section is commented out for Win-app ################
#    log_print("-- " + "#" * 80)
#    print("Here!2")
#    log_print(f"-- # PDA view: {nz_schema:>23}.{nz_view}")
#    log_print(f"-- # Legacy view: {bmsiw_schema:>20}.{bmsiw_view}")
#    log_print("-- #")
#    log_print(f"-- # Legacy view column count = {get_view_row_count('DB2', bmsiw_schema, bmsiw_view):>5}")
#    log_print(f"-- # PDA view column count = {get_view_row_count('PDA', nz_schema, nz_view):>8}")
#    log_print("-- #")
#    log_print("-- # " + audit_col_status_code [compare_audit_col2(check_audit_col('DB2', bmsiw_schema, bmsiw_view), check_audit_col('PDA', nz_schema, nz_view))])
#    log_print("")
###########################################################################

    # First check if there are records for PDA view
    if get_view_row_count('PDA', nz_schema, nz_view) > 0:
        IDAA_view_to_file (nz_schema, nz_view, bmsiw_schema, bmsiw_view)
    else:
        c=1
###        log_print("ERROR: No rows for PDA view found!")
###    log_print("-- " + "#" * 80)
###    log_print("")

def IDAA_create_view_ddl(nz_schema, nz_view):
    # prepare log
    flog_abs = output_directory + "\\" + fLog
    if os.path.exists(flog_abs):
        os.remove(flog_abs)
    bmsiw_schema, bmsiw_view = get_legacy_view_name(nz_schema, nz_view)
    #IDAA_proceed_single_view(nz_schema, nz_view, bmsiw_schema, bmsiw_view)

    txt = bmsiw_schema+"."+bmsiw_view
    return txt



if __name__ == '__main__':

    # prepare log
    flog_abs = output_directory + "\\" + fLog
    if os.path.exists(flog_abs):
        os.remove(flog_abs)

    # Provide a choice: either to proceed with a single view or all views in mappinng table
    #how_to_proceed = input("Please may your choice whether to proceed with a single view or all views in mapping table:")
    #if

    # -- example - how to proceed with a single view -----------------------
    #nz_schema = 'CMNREF'
    #nz_view = 'LOCAL_COLUMN_AUDIT_V'
    #bmsiw_schema, bmsiw_view = get_legacy_view_name(nz_schema, nz_view)
    #IDAA_proceed_single_view (nz_schema, nz_view, bmsiw_schema, bmsiw_view)
    # ----------------------------------------------------------------------

    sql = f"SELECT NEW_SCHEMA, NEW_VIEW_NAME FROM IDAA.PDA_VIEW_MAP WHERE NEW_SCHEMA = 'WORKER';"
    stmt = ibm_db.exec_immediate(conn, sql)
    tuple = ibm_db.fetch_tuple(stmt)
    while tuple:
        nz_schema = tuple[0]
        nz_view = tuple[1]
        tuple = ibm_db.fetch_tuple(stmt)
        bmsiw_schema, bmsiw_view = get_legacy_view_name(nz_schema, nz_view)
        IDAA_proceed_single_view(nz_schema, nz_view, bmsiw_schema, bmsiw_view)



