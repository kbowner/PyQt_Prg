import ibm_db, hashlib

cDATABASE = "SAMPLE"
cHOSTNAME = "192.168.253.128"
cPORT = "50000"
cPROTOCOL = "TCPIP"
cUID = "db2inst1"
cPWD = "db2inst1"
standard_audit_col_list = ['ROW_STAT_CD', 'INSRT_TMS', 'UPDT_TMS']

conn = ibm_db.connect(
    f"DATABASE={cDATABASE};HOSTNAME={cHOSTNAME};PORT={cPORT};PROTOCOL={cPROTOCOL};UID={cUID};PWD={cPWD};", "", "")


def get_pda_schema_list():
    sql = f"SELECT DISTINCT TRIM(NEW_SCHEMA) AS PDA_SCHEMA FROM IDAA.PDA_VIEW_MAP ORDER BY 1"
    stmt = ibm_db.exec_immediate(conn, sql)
    tuple = ibm_db.fetch_tuple(stmt)
    pda_schemas = []
    while tuple:
        pda_schemas.append(tuple[0])
        tuple = ibm_db.fetch_tuple(stmt)
    return pda_schemas


def get_pda_view_list(schema):
    sql = f"SELECT DISTINCT TRIM(NEW_VIEW_NAME) AS PDA_VIEW FROM IDAA.PDA_VIEW_MAP WHERE NEW_SCHEMA = '{schema}'ORDER BY 1"
    stmt = ibm_db.exec_immediate(conn, sql)
    tuple = ibm_db.fetch_tuple(stmt)
    pda_views = []
    while tuple:
        pda_views.append(tuple[0])
        tuple = ibm_db.fetch_tuple(stmt)
    return pda_views


def get_legacy_view_name(pda_schema, pda_view):
    sql = f"SELECT OLD_SCHEMA, OLD_VIEW_NAME FROM IDAA.PDA_VIEW_MAP WHERE NEW_SCHEMA = '{pda_schema}' AND NEW_VIEW_NAME = '{pda_view}' FETCH FIRST 1 ROW ONLY;"
    stmt = ibm_db.exec_immediate(conn, sql)
    tuple = ibm_db.fetch_tuple(stmt)
    while tuple:
        return tuple[0], tuple[1]
        tuple = ibm_db.fetch_tuple(stmt)


def get_view_mapping(nz_schema, nz_view, db2_schema, db2_view):
    mapping_sql = f"WITH V_DB2 (SCHEMA,VIEWNAME,COLNAME,COLTYPE,COLNO) AS " \
                  f"(SELECT SCHEMA,VIEWNAME,COLNAME,COLTYPE,COLNO " \
                  f"FROM IDAA.BMSIW_COLUMNS WHERE SCHEMA = '{db2_schema}' AND VIEWNAME = '{db2_view}')," \
                  f"V_PDA (SCHEMA,VIEWNAME,COLNAME,COLTYPE,COLNO) AS " \
                  f"(SELECT CREATOR,NAME,COLNAME,COLTYPE,COLNO FROM IDAA.PDA_REL_COLUMNS " \
                  f"WHERE CREATOR = '{nz_schema}' AND NAME = '{nz_view}' AND OBJECT_TYPE = 'VIEW') " \
                  f"SELECT NVL(V_DB2.SCHEMA,'') AS DB2_SCHEMA, NVL(V_DB2.VIEWNAME,'') AS DB2_VIEWNAME, " \
                  f"NVL(V_DB2.COLNAME,'') AS DB2_COLNAME, NVL(TO_CHAR(V_DB2.COLNO),'') AS DB2_COLNO, " \
                  f"NVL(V_PDA.SCHEMA,'') AS PDA_SCHEMA, NVL(V_PDA.VIEWNAME,'') AS PDA_VIEWNAME, " \
                  f"NVL(V_PDA.COLNAME,'') AS PDA_COLNAME, NVL(TO_CHAR(V_PDA.COLNO),'') AS PDA_COLNO " \
                  f"FROM V_DB2 FULL OUTER JOIN V_PDA ON V_DB2.COLNO = V_PDA.COLNO ORDER BY V_DB2.COLNO;"
    stmt = ibm_db.exec_immediate(conn, mapping_sql)
    map_tuple = []
    tuple = ibm_db.fetch_tuple(stmt)
    while tuple != False:
        map_tuple.append(tuple)
        tuple = ibm_db.fetch_tuple(stmt)
    return map_tuple

def save_param (encrypted = True, param_name = "New_Parameter", param_value = "Empty_Value"):
    res = hashlib.sha256(str.encode())
    print(f"The hexadecimal equivalent of SHA256 is : {res.hexdigest()}")


