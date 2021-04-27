import sys, ibm_db, sqlparse
import MainForm, MainFormLogic, idaa_logic, SettingsForm, IdaaForm
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog, QMenu
from PyQt5.QtGui import QBrush, QColor, QFont, QCursor
from PyQt5 import QtCore, QtWidgets
from IDAA_Settings import prd_DATABASE, prd_HOSTNAME, prd_PORT, prd_PROTOCOL, prd_UID, prd_PWD, std_aud_col_lst, dev_db_conn_dict


global LegacySchema
global LegacyView
global PDASchema
global PDAView

LegacySchema = ""
LegacyView = ""
PDASchema = ""
PDAView = ""

#cDATABASE = prd_DATABASE
#cHOSTNAME = prd_HOSTNAME
#cPORT = prd_PORT
#cPROTOCOL = prd_PROTOCOL
#cUID = prd_UID
#cPWD = prd_PWD
cDATABASE, cHOSTNAME, cPORT, cPROTOCOL, cUID, cPWD = dev_db_conn_dict.values()
standard_audit_col_list = std_aud_col_lst

conn = ibm_db.connect(
    f"DATABASE={cDATABASE};HOSTNAME={cHOSTNAME};PORT={cPORT};PROTOCOL={cPROTOCOL};UID={cUID};PWD={cPWD};", "", "")




def comboBox1_changed():
    myUI.comboBox2.clear()
    PDASchema = myUI.comboBox1.currentText().upper()
    myUI.comboBox2.addItems(MainFormLogic.get_pda_view_list(PDASchema))


def pushButton_Clicked(self):
    myUI.comboBox1.setEnabled(True)
    myUI.comboBox1.addItems(MainFormLogic.get_pda_schema_list())
    myUI.comboBox2.setEnabled(True)


def pushButton3_Clicked(self):
    PDASchema = myUI.comboBox1.currentText().upper()
    PDAView = myUI.comboBox2.currentText().upper()
    LegacySchema, LegacyView = MainFormLogic.get_legacy_view_name(PDASchema, PDAView)
    myUI.Text_DB2_Schema.setText(LegacySchema)
    myUI.Text_DB2_View.setText(LegacyView)

def pushButton4_Clicked(self):
    return 0

def pushButton2_Clicked(self):
    nz_schema = myUI.comboBox1.currentText().upper()
    nz_view = myUI.comboBox2.currentText().upper()
    db2_schema, db2_view = MainFormLogic.get_legacy_view_name(nz_schema, nz_view)
    view_map_data = MainFormLogic.get_view_mapping(nz_schema, nz_view, db2_schema, db2_view)

    numrows = len(view_map_data)
    numcols = len(view_map_data[0])
    myUI.statusbar.showMessage(f"Rows: {numrows} ;  Cols: {numcols}")
    myUI.tableWidget.setColumnCount(numcols)
    myUI.tableWidget.setRowCount(numrows)
    TableHeader = ["DB2 SCHEMA", "DB2 VIEWNAME", "DB2 COLNAME", "DB2 COLNO", "PDA SCHEMA", "PDA VIEWNAME", "PDA COLNAME", "PDA COLNO"]
    myUI.tableWidget.setHorizontalHeaderLabels(TableHeader)

    row = 0
    for tuple_row in view_map_data:
        col = 0
        for item in tuple_row:
            cell_value = tuple_row[col]
            myUI.tableWidget.setItem(row,col,QTableWidgetItem(str(cell_value)))

            if col in (3,7):
                # Example how to color an item
                myitem = myUI.tableWidget.item(row, col)
                #myitem.setFont(QFont("Times", 9, QFont.Bold))
                #myitem.setForeground(QBrush(QColor(102, 0, 255)))

            col += 1
        row += 1
    #myUI.tableWidget.removeRow(myUI.tableWidget.rowCount()-1)
    myUI.tableWidget.resizeColumnsToContents()
    myUI.tableWidget.resizeRowsToContents()

    myUI.tableWidget.horizontalHeader().setStyleSheet("QHeaderView::section { background-color:lightgrey }")

    # If need to resize tableWidget to remove Horizontal Scrollbar
    #width = myUI.tableWidget.verticalHeader().width()
    #width += myUI.tableWidget.horizontalHeader().width()
    #if myUI.tableWidget.verticalScrollBar().isVisible():
    #    width += myUI.tableWidget.verticalScrollBar().width() * 2
    #width += myUI.tableWidget.frameWidth() * 2
    #myUI.tableWidget.setMinimumWidth(width)

def delete_selected_rows():
    rows = set()
    for index in myUI.tableWidget.selectedIndexes():
        rows.add(index.row())
    for row in sorted(rows, reverse=True):
        myUI.tableWidget.removeRow(row)

def comboBox2_changed():
    PDASchema = myUI.comboBox1.currentText().upper()
    PDAView = myUI.comboBox2.currentText().upper()

def Program_preference_open():
    myDlg = QDialog()
    dlg = SettingsForm.Ui_Dialog()
    dlg.setupUi(myDlg)
    myDlg.exec_()



def show_menu():

    menu = QMenu()
    act_delete = menu.addAction("Delete selected row(s)..")

def pushButton6_Clicked ():
    PDASchema = myUI.comboBox1.currentText().upper()
    PDAView = myUI.comboBox2.currentText().upper()
    idaaDlg = QDialog()
    dlgIDAA = IdaaForm.Ui_Dialog_IDAA()
    dlgIDAA.setupUi(idaaDlg)



    bmsiw_schema, bmsiw_view = MainFormLogic.get_legacy_view_name(PDASchema, PDAView)

    ############## This section is ... ################
    dlgIDAA.plainTextEdit.appendPlainText("-- " + "#" * 80)
    dlgIDAA.plainTextEdit.appendPlainText(f"-- # PDA view: {PDASchema:>23}.{PDAView}")
    dlgIDAA.plainTextEdit.appendPlainText(f"-- # Legacy view: {bmsiw_schema:>20}.{bmsiw_view}")
    dlgIDAA.plainTextEdit.appendPlainText("-- #")
    dlgIDAA.plainTextEdit.appendPlainText(f"-- # Legacy view column count = {idaa_logic.get_view_row_count('DB2', bmsiw_schema, bmsiw_view):>5}")
    dlgIDAA.plainTextEdit.appendPlainText(f"-- # PDA view column count = {idaa_logic.get_view_row_count('PDA', PDASchema, PDAView):>8}")
    dlgIDAA.plainTextEdit.appendPlainText("-- " + "#" * 80)
    dlgIDAA.plainTextEdit.appendPlainText("")
    ###########################################################################
    level_audit_cols = 0
    level_audit_cols = idaa_logic.get_view_row_count('PDA', PDASchema, PDAView) - idaa_logic.get_view_row_count('DB2',bmsiw_schema,bmsiw_view)
    print(level_audit_cols)

    #new_col_list - is a col list from myUI.tableWidget, PDA columns
    new_col_list = []
    #new_col_list =
    num_rows = myUI.tableWidget.rowCount()
    col_rows = myUI.tableWidget.columnCount()
    #print (num_rows, col_rows)

    for i in range (num_rows):
        #print (myUI.tableWidget.item(i,2).text())
        new_col_list.append(myUI.tableWidget.item(i,2).text())

    #print (new_col_list)
    ##################################################################

    idaa_view_header = idaa_logic.print_idaa_view_header(PDASchema, PDAView, level_audit_cols, new_col_list)
    idaa_view_statement = idaa_logic.get_bmsiw_view_body(bmsiw_schema, bmsiw_view)
    cur_sqlid = "SIWASDBA"
    idaa_label = "\nLABEL ON TABLE " + PDASchema.upper() + "." + PDAView.upper() + " IS 'IDAA " + PDASchema.upper() + "';\n"

    dlgIDAA.plainTextEdit.appendPlainText("\nSET CURRENT SQLID = '" + cur_sqlid + "';\n")
    s = sqlparse.format(idaa_view_header, reindent=True, wrap_after=True, truncate_strings=80)
    dlgIDAA.plainTextEdit.appendPlainText(s)
    dlgIDAA.plainTextEdit.appendPlainText(sqlparse.format(idaa_view_statement, reindent=True, wrap_after=True, truncate_strings=80) + "\n")
    dlgIDAA.plainTextEdit.appendPlainText(idaa_label)
    dlgIDAA.plainTextEdit.appendPlainText("\n")

    idaaDlg.exec_()

def pushButton8_Clicked ():
    PDASchema = myUI.comboBox1.currentText().upper()
    PDAView = myUI.comboBox2.currentText().upper()
    bmsiw_schema, bmsiw_view = MainFormLogic.get_legacy_view_name(PDASchema, PDAView)
    idaa_view_statement = idaa_logic.get_bmsiw_view_body(bmsiw_schema, bmsiw_view)


if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    myWin = QMainWindow()
    myUI = MainForm.Ui_MainWindow()
    myUI.setupUi(myWin)
    myUI.pushButton.clicked.connect(pushButton_Clicked)
    myUI.pushButton_2.clicked.connect(pushButton2_Clicked)
    myUI.pushButton_3.clicked.connect(pushButton3_Clicked)
    myUI.pushButton_6.clicked.connect(pushButton6_Clicked)
    myUI.comboBox1.currentTextChanged.connect(comboBox1_changed)
    myUI.comboBox2.currentTextChanged.connect(comboBox2_changed)
    myUI.pushButton_7.clicked.connect(delete_selected_rows)
    myUI.pushButton_4.clicked.connect(pushButton4_Clicked)
    myUI.pushButton_8.clicked.connect(pushButton8_Clicked)
    myUI.actionProgram_preference.triggered.connect(Program_preference_open)
    myUI.actionDeleteRow.triggered.connect(show_menu)
    myWin.show()
    sys.exit(myapp.exec_())


