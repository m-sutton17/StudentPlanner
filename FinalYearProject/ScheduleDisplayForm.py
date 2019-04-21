import clr


clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')
clr.AddReference("IronPython.SQLite")

import sqlite3

from System.Drawing import *
from System.Windows.Forms import *
from TimetableInputForm import *
from EventManagementForm import *
from Scheduler import TimeSlot, EventSlot, TimetableSlot
from System import *

class ScheduleDisplayForm(Form):
    #initialisation
    def __init__(self):
        # Create child controls and initialize form
        self.Text = 'Schedule Display'
        self.Name = 'frmScheduleDisplay'

        self.initialiseControls()

        self.callerForm = None
        
        self.conn = sqlite3.connect("schedulerDatabase.db")
        self.cursor = self.conn.cursor()

        self.columns = 8
        self.rows = 5

        self.schedule = Array.CreateInstance(str, self.rows, self.columns)

        self.allSchedules = []
        self.fillScheduleList()
        self.events = []
        self.classes = []

        # set up grid
        self.setUpGrid()
        #self.grdSchedule.Columns.Clear()
        #for i in range(self.columns):
        #     self.grdSchedule.Columns.Add("" ,"%s - %s" % (i+9, i+10))

    def initialiseControls(self):
        
        self.ClientSize = Size(1280, 720);
        self.FormBorderStyle = FormBorderStyle.FixedDialog

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
        self.lblTitle.Text = "Schedule Display"
        self.lblTitle.Location = Point(10, 10)
        self.lblTitle.Size = Size(900, 35);
        self.lblTitle.Font = titleFont
        
        # schedule grid data view
        self.grdSchedule = DataGridView();
        self.grdSchedule.Location = Point(320, 50);
        self.grdSchedule.Name = "grdSchedule";
        self.grdSchedule.Size = Size(900, 650);
        self.grdSchedule.RowsDefaultCellStyle.WrapMode = DataGridViewTriState.True
        self.grdSchedule.AutoSizeRowsMode = DataGridViewAutoSizeRowsMode.AllCells

        # saved schedules combobox
        self.cbxSchedules = ComboBox()
        self.cbxSchedules.DropDownStyle = ComboBoxStyle.DropDownList;
        self.cbxSchedules.Location = Point(15, 80)
        self.cbxSchedules.Size = Size(275, 100);
        self.cbxSchedules.Font = textFont
        self.cbxSchedules.BackColor = Color.White
        self.cbxSchedules.SelectedIndexChanged += self.scheduleSelectionChanged

        # save button
        self.btnSave = Button()
        self.btnSave.Text = 'Save Changes'
        self.btnSave.Location = Point(40, 200)
        self.btnSave.Size = Size(225, 60)
        self.btnSave.Font = buttonFont
        self.btnSave.BackColor = Color.FromArgb(0, 99, 160)
        #self.btnSave.Click += self.buttonPressed

        # export button
        self.btnExport = Button()
        self.btnExport.Text = 'Export Schedule'
        self.btnExport.Location = Point(40, 350)
        self.btnExport.Size = Size(225, 60)
        self.btnExport.Font = buttonFont
        self.btnExport.BackColor = Color.FromArgb(0, 99, 160)
        self.btnExport.Click += self.btnExportPress

        # back button
        self.btnBack = Button()
        self.btnBack.Text = 'Back to Menu'
        self.btnBack.Location = Point(40, 500)
        self.btnBack.Size = Size(225, 60)
        self.btnBack.Font = buttonFont
        self.btnBack.BackColor = Color.FromArgb(0, 99, 160)
        self.btnBack.Click += self.btnExitPress

        # add controls to panel
        self.mainPanel.Controls.Add(self.lblTitle)
        self.mainPanel.Controls.Add(self.cbxSchedules)
        self.mainPanel.Controls.Add(self.btnSave)
        self.mainPanel.Controls.Add(self.btnExport)
        self.mainPanel.Controls.Add(self.btnBack)
        self.mainPanel.Controls.Add(self.grdSchedule)

        # add panels
        self.Controls.Add(self.mainPanel)

    def setUpGrid(self):

        self.grdSchedule.Columns.Clear()
        for i in range(self.columns):
             self.grdSchedule.Columns.Add("" ,"%s - %s" % (i+9, i+10))   # (i+9) + " - " + (i+10)

        row = Array.CreateInstance(str, self.columns)
        rowNames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        for x in range(self.rows):
            for y in range(self.columns):
                row[y] = ''

            self.grdSchedule.Rows.Add(row)
            self.grdSchedule.Rows[x].HeaderCell.Value = rowNames[x]
        
        self.grdSchedule.Font = Font("Open Sans", 8)
        self.grdSchedule.RowHeadersWidth = 95
        self.grdSchedule.ColumnHeadersHeight = 75
        self.grdSchedule.RowTemplate.MinimumHeight = 100
        self.grdSchedule.RowTemplate.Height = 100
        style = DataGridViewCellStyle()
        style.Font = Font("Open Sans", 15)
        self.grdSchedule.ColumnHeadersDefaultCellStyle = style

        self.updateGrid(self.schedule)

    def updateGrid(self, data):
        self.grdSchedule.Rows.Clear()
        
        rowNames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        for x in range(self.rows):
            row = Array.CreateInstance(str, self.columns)
            for y in range(self.columns):
                if (data[x,y]):
                    if ('tt' in data[x,y]):
                        timeSlot = self.retrieveClassSlot(data[x,y])
                        if (timeSlot):
                            row[y] = timeSlot.printSlot()
                    elif ('et' in data[x,y]):
                        timeSlot = self.retrieveEventSlot(data[x,y])
                        if (timeSlot):
                            row[y] = timeSlot.printSlot()
                    else:
                        row[y] = ''
                else:
                    row[y] = ''

            self.grdSchedule.Rows.Add(row)
            self.grdSchedule.Rows[x].HeaderCell.Value = rowNames[x]
            style = DataGridViewCellStyle()
            style.Font = Font("Open Sans", 10)
            self.grdSchedule.Rows[x].DefaultCellStyle = style

    def retrieveClassSlot(self, code):
        for timetableClass in self.classes:
            if (timetableClass.code == code):
                return timetableClass

    def retrieveEventSlot(self, code):
        for event in self.events:
            if (event.code == code):
                return event

    def displaySavedSchedule(self, index):
        self.classes.Clear()
        self.events.Clear()
        schedule = self.allSchedules[index]
        
        # retrieve schedule
        sql = "SELECT * FROM FullSchedules WHERE code = '" + schedule + "'"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()

        offset = 2
        i = 0
        for x in range(self.rows):
            for y in range(self.columns):
                index = i + offset
                
                if (result[index] != ""):
                    if ('tt' in result[index]):
                        if self.checkForClass(result[index]):
                            pass
                        else:
                            self.classes.Add(self.getClassFromDB(result[index]))
                    elif ('et' in result[index]):                       
                       self.events.Add(self.getEventFromDB(result[index]))
                        
                    self.schedule[x,y] = result[index]
                else:
                    self.schedule[x,y] = None
                
                i = i + 1

        self.updateGrid(self.schedule)

    def getClassFromDB(self, code):
        sql = "SELECT * FROM ScheduleClasses WHERE code = '" + code + "'"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()

        return TimetableSlot(result[1], result[0], result[2], result[3])

    def checkForClass(self, code):
        
        for timetableClass in self.classes:
            if (timetableClass == code):
                return True

    def getEventFromDB(self, code):
        sql = "SELECT * FROM ScheduleEvents WHERE code = '" + code + "'"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()

        return EventSlot(result[1], result[0], result[2], result[3])

    def fillScheduleList(self):
        sql = "SELECT code, name FROM FullSchedules"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        self.cbxSchedules.Items.Clear()
        for row in results:
            self.allSchedules.Add(row[0])
            self.cbxSchedules.Items.Add(row[1])

# UI events
    def btnExitPress(self, sender, args):
        self.conn.close()
        self.callerForm.Show()
        self.Close()

    def btnExportPress(self, sender, args):
        bm = Bitmap(self.grdSchedule.Bounds.Width, self.grdSchedule.Bounds.Height)
        self.grdSchedule.DrawToBitmap(bm, Rectangle(1,1,self.grdSchedule.Width, self.grdSchedule.Height))
        
        dialog = SaveFileDialog()
        dialog.Title = 'Save Schedule as Image'
        dialog.Filter = 'Image Files(*.JPG)|*.JPG'

        if dialog.ShowDialog() == DialogResult.OK:
            try:
                bm.Save(dialog.FileName, Drawing.Imaging.ImageFormat.Jpeg)
            except IOError, e:
                print 'An error occured: ', e


    def scheduleSelectionChanged(self, sender, args):
        self.displaySavedSchedule(self.cbxSchedules.SelectedIndex)

#Application.EnableVisualStyles()
#Application.SetCompatibleTextRenderingDefault(False)

#form = ScheduleDisplayForm()
#Application.Run(form)