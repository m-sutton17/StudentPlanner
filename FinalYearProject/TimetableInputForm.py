import clr

from System import Array
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')
clr.AddReference("IronPython.SQLite")

import sqlite3

from System.Drawing import *
from System.Windows.Forms import *
from ScheduleGenerationForm import *

from Scheduler import TimetableSlot


class TimetableInputForm(Form):
    def __init__(self):
        self.Text = 'Timetable Input'
        self.Name = 'frmTimetableInput'

        self.columns = 8
        self.rows = 5
        self.timetableArray = Array.CreateInstance(str, self.rows, self.columns)
        self.classes = []
        self.timetables = []

        self.callerForm = None

        self.initialiseControls()

        self.setUpGrid()

        self.conn = sqlite3.connect("schedulerDatabase.db")
        self.cursor = self.conn.cursor()

        self.fillTimetableList()

    def initialiseControls(self):
        
        self.ClientSize = Size(1280, 720);
        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.MaximizeBox = False

        buttonFont = Font("Open Sans", 14)
        buttonSmallFont = Font("Open Sans", 10)
        titleFont = Font("Open Sans", 18)
        textFont = Font("Open Sans", 9)

        ## main controls
        self.mainPanel = Panel()
        self.mainPanel.ForeColor = Color.Black
        self.mainPanel.BackColor = Color.FromArgb(161, 162, 163)
        self.mainPanel.Location = Point(0, 0)
        self.mainPanel.Size = Size(1280, 720)

        # title label
        self.lblTitle = Label()
        self.lblTitle.Text = "Timetable Input"
        self.lblTitle.Location = Point(10, 5)
        self.lblTitle.Size = Size(1280, 40)
        self.lblTitle.Font = titleFont

        # timetable data grid
        self.grdTimetable = DataGridView();
        self.grdTimetable.Location = Point(10, 45);
        self.grdTimetable.Name = "grdTimetable";
        self.grdTimetable.Size = Size(900, 600);
        self.grdTimetable.MultiSelect = True;
        self.grdTimetable.ReadOnly = True;
        self.grdTimetable.RowsDefaultCellStyle.WrapMode = DataGridViewTriState.True
        self.grdTimetable.AutoSizeRowsMode = DataGridViewAutoSizeRowsMode.AllCells

        # timetable combo box
        self.cbxTimetables = ComboBox()
        self.cbxTimetables.DropDownStyle = ComboBoxStyle.DropDownList;
        self.cbxTimetables.Location = Point(950, 50)
        self.cbxTimetables.Size = Size(280, 50);
        self.cbxTimetables.Font = textFont
        self.cbxTimetables.BackColor = Color.White
        self.cbxTimetables.SelectedIndexChanged += self.timetableSelectionChanged

        # timetable name label
        self.lblTTName = Label()
        self.lblTTName.Text = "Name"
        self.lblTTName.Location = Point(950, 125)
        self.lblTTName.Size = Size(100, 20)
        self.lblTTName.Font = textFont

        # timetable name text box
        self.tbxTTName = TextBox()
        self.tbxTTName.Location = Point(1050, 125)
        self.tbxTTName.Size = Size(200, 20)
        self.tbxTTName.Font = textFont

        # add timetable button
        self.btnAddTimetable = Button()
        self.btnAddTimetable.Text = 'Add TimeTable'
        self.btnAddTimetable.Location = Point(1000, 200)
        self.btnAddTimetable.Size = Size(200, 50)
        self.btnAddTimetable.Font = buttonFont
        self.btnAddTimetable.BackColor = Color.FromArgb(0, 99, 160)
        self.btnAddTimetable.Click += self.saveTimetablePressed

        # back button
        self.btnBack = Button()
        self.btnBack.Text = 'Return'
        self.btnBack.Location = Point(500, 660)
        self.btnBack.Size = Size(400, 50)
        self.btnBack.Font = buttonFont
        self.btnBack.BackColor = Color.FromArgb(0, 99, 160)
        self.btnBack.Click += self.exitButtonPressed

        # add controls
        self.mainPanel.Controls.Add(self.lblTitle)
        self.mainPanel.Controls.Add(self.grdTimetable)
        self.mainPanel.Controls.Add(self.cbxTimetables)
        self.mainPanel.Controls.Add(self.lblTTName)
        self.mainPanel.Controls.Add(self.tbxTTName)
        self.mainPanel.Controls.Add(self.btnAddTimetable)
        self.mainPanel.Controls.Add(self.btnBack)

        ## input controls
        self.inputPanel = Panel()
        self.inputPanel.ForeColor = Color.Black
        self.inputPanel.BackColor = Color.FromArgb(226, 226, 226)
        self.inputPanel.Location = Point(930, 327)
        self.inputPanel.Size = Size(325, 300)

        # class name label
        self.lblClassName = Label()
        self.lblClassName.Text = "Name"
        self.lblClassName.Location = Point(10, 10)
        self.lblClassName.Size = Size(100, 20)
        self.lblClassName.Font = textFont

        # class name textbox
        self.tbxClassName = TextBox()
        self.tbxClassName.Location = Point(150, 10)
        self.tbxClassName.Size = Size(150, 20);
        self.tbxClassName.Font = textFont

        # class room label
        self.lblClassRoom = Label()
        self.lblClassRoom.Text = "Room"
        self.lblClassRoom.Location = Point(10, 85)
        self.lblClassRoom.Size = Size(100, 20)
        self.lblClassRoom.Font = textFont
        
        # class room textbox
        self.tbxClassRoom = TextBox()
        self.tbxClassRoom.Location = Point(150, 85)
        self.tbxClassRoom.Size = Size(150, 20);
        self.tbxClassRoom.Font = textFont

        # class teacher label
        self.lblClassTeacher = Label()
        self.lblClassTeacher.Text = "Teacher/Lecturer"
        self.lblClassTeacher.Location = Point(10, 160)
        self.lblClassTeacher.Size = Size(100, 20)
        self.lblClassTeacher.Font = textFont
        
        # class teacher textbox
        self.tbxClassTeacher = TextBox()
        self.tbxClassTeacher.Location = Point(150, 160)
        self.tbxClassTeacher.Size = Size(150, 20);
        self.tbxClassTeacher.Font = textFont

        # add lessons button
        self.btnAddLessons = Button()
        self.btnAddLessons.Text = "Add classes to selected slots"
        self.btnAddLessons.Location = Point(55, 210)
        self.btnAddLessons.Size = Size(200, 60)
        self.btnAddLessons.Font = buttonFont
        self.btnAddLessons.BackColor = Color.FromArgb(0, 99, 160)
        self.btnAddLessons.Click += self.addLessonsPressed

        # add controls
        self.inputPanel.Controls.Add(self.lblClassName)
        self.inputPanel.Controls.Add(self.tbxClassName)
        self.inputPanel.Controls.Add(self.lblClassRoom)
        self.inputPanel.Controls.Add(self.tbxClassRoom)
        self.inputPanel.Controls.Add(self.lblClassTeacher)
        self.inputPanel.Controls.Add(self.tbxClassTeacher)
        self.inputPanel.Controls.Add(self.btnAddLessons)

        self.mainPanel.Controls.Add(self.inputPanel)

        self.Controls.Add(self.mainPanel)

    def setUpGrid(self):

        self.grdTimetable.Columns.Clear()
        for i in range(self.columns):
             self.grdTimetable.Columns.Add("" ,"%s - %s" % (i+9, i+10))   # (i+9) + " - " + (i+10)

        row = Array.CreateInstance(str, self.columns)
        rowNames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        for x in range(self.rows):
            for y in range(self.columns):
                row[y] = ''

            self.grdTimetable.Rows.Add(row)
            self.grdTimetable.Rows[x].HeaderCell.Value = rowNames[x]
        
        self.grdTimetable.Font = Font("Open Sans", 8)
        self.grdTimetable.RowHeadersWidth = 95
        self.grdTimetable.ColumnHeadersHeight = 75
        self.grdTimetable.RowTemplate.MinimumHeight = 100
        self.grdTimetable.RowTemplate.Height = 100
        style = DataGridViewCellStyle()
        style.Font = Font("Open Sans", 15)
        self.grdTimetable.ColumnHeadersDefaultCellStyle = style

        self.updateGrid()

    def updateGrid(self):
        self.grdTimetable.Rows.Clear()
        
        rowNames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        for x in range(self.rows):
            row = Array.CreateInstance(str, self.columns)
            for y in range(self.columns):
                classSlot = self.retrieveClassSlot(self.timetableArray[x,y])
                if (classSlot):
                    row[y] = classSlot.printSlot()

            self.grdTimetable.Rows.Add(row)
            self.grdTimetable.Rows[x].HeaderCell.Value = rowNames[x]
            style = DataGridViewCellStyle()
            style.Font = Font("Open Sans", 10)
            self.grdTimetable.Rows[x].DefaultCellStyle = style

    def displaySavedTimetable(self, index):
        self.classes.Clear()
        timetable = self.timetables[index]
        
        # retrieve timetable
        sql = "SELECT * FROM TimetableSchedules WHERE code = '" + timetable + "'"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()

        offset = 2
        i = 0
        for x in range(self.rows):
            for y in range(self.columns):
                index = i + offset
                
                if (result[index] != ""):
                    if self.checkForClass(result[index]):
                        pass
                    else:
                        self.classes.Add(self.getClassFromDB(result[index]))
                        self.timetableArray[x,y] = result[index]
                else:
                    self.timetableArray[x,y] = ""
                
                i = i + 1

        self.updateGrid()

    def generateClassCode(self):
        index = 1
        prefix = 'tt'

        sql = "SELECT code FROM ScheduleClasses"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()

        free = False
        while free == False:
            found = False
            for row in results:
                if (prefix + str(index) == row[0]):
                    found = True

            if (found == False):
                free = True
            else:
                index = index + 1

        return prefix + str(index)

    def generateTimetableCode(self):
        index = 1
        prefix = 'tts'

        sql = "SELECT code FROM TimetableSchedules"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()

        free = False
        while free == False:
            found = False
            for row in results:
                if (prefix + str(index) == row[0]):
                    found = True


            if (found == False):
                free = True
            else:
                index = index + 1

        return prefix + str(index)

    def retrieveClassSlot(self, code):
        for timetableClass in self.classes:
            if (timetableClass.code == code):
                return timetableClass

    def checkForClass(self, code):
        
        for timetableClass in self.classes:
            if (timetableClass == code):
                return True

        return False

    def convertSlotsToSQL(self):
        sql = ''
        for x in range(self.rows):
            for y in range(self.columns):
                if (self.timetableArray[x,y]):
                    sql = sql + "'" + self.timetableArray[x,y] + "',"
                else:
                    sql = sql + "'',"

        return sql[:-1]
       
    def saveClassToDB(self, timetableClass):
        sql = """
                INSERT INTO ScheduleClasses
                VALUES ('""" + str(timetableClass.code) + "','" + str(timetableClass.name) + "','" + str(timetableClass.room) + "','" + str(timetableClass.teacher) + "')"
              
        self.cursor.execute(sql)
        self.conn.commit()

    def getClassFromDB(self, code):
        sql = "SELECT * FROM ScheduleClasses WHERE code = '" + code + "'"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()

        return TimetableSlot(result[1], result[0], result[2], result[3])
        
    def fillTimetableList(self):
        sql = "SELECT code, name FROM TimetableSchedules"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        self.cbxTimetables.Items.Clear()
        for row in results:
            self.timetables.Add(row[0])
            self.cbxTimetables.Items.Add(row[1])
        

# UI events
    def addLessonsPressed(self, sender, args):
        valid = True
        if (self.tbxClassName.Text):
            name = self.tbxClassName.Text
        else:
            # not valid
            valid = False
        if (self.tbxClassRoom.Text):
            room = self.tbxClassRoom.Text
        else:
            # not valid
            valid = False
        if (self.tbxClassTeacher.Text):
            teacher = self.tbxClassTeacher.Text
        else:
            # not valid
            valid = False

        
        if (valid):
            timetableClass = TimetableSlot(name, self.generateClassCode(), room, teacher)
            self.classes.Add(timetableClass)
            self.saveClassToDB(timetableClass)

            for cell in self.grdTimetable.SelectedCells:
                print('x: ' + str(cell.RowIndex) + ' y: ' + str(cell.ColumnIndex))
                self.timetableArray[cell.RowIndex, cell.ColumnIndex] = timetableClass.code

            self.updateGrid()

            MessageBox.Show("Class added", "Success", MessageBoxButtons.OK)
        else:
            print('invalid')
            MessageBox.Show("Class information missing. Enter a name, room and teacher for the class", "Invalid", MessageBoxButtons.OK)

    def saveTimetablePressed(self, sender, args):
        if (self.tbxTTName.Text):
            code = self.generateTimetableCode()
            name = self.tbxTTName.Text
            sql = """
                    INSERT INTO TimetableSchedules
                    VALUES ('""" + str(code) + "','" + str(name) + "'," + self.convertSlotsToSQL() + ")"
              
            self.cursor.execute(sql)
            self.conn.commit()
            self.fillTimetableList()

            MessageBox.Show("Timetable added", "Success", MessageBoxButtons.OK)
        else:
            MessageBox.Show("Enter a name for the timetable", "Invalid", MessageBoxButtons.OK)

    def timetableSelectionChanged(self, sender, args):
        self.displaySavedTimetable(self.cbxTimetables.SelectedIndex)

    def exitButtonPressed(self, sender, args):
        #self.callerForm.scheduler.setTimetable(self.timetableArray)
        self.conn.close()
        try:
            self.callerForm.fillTimetableList()
        except:
            print("Not the correct form")
        self.callerForm.Show()
        self.Close()


#class DGVMultiSelect (DataGridView):
#     def __init__(self):
#         pass


#     def OnCellMouseDown(self, DataGridViewCellMouseEventArgs e):


#Application.EnableVisualStyles()
#Application.SetCompatibleTextRenderingDefault(False)

#form = TimetableInputForm()
#Application.Run(form)