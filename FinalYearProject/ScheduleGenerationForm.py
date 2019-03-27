import clr
import sqlite3

clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

from System.Drawing import *
from System.Windows.Forms import *
from TimetableInputForm import *
from EventManagementForm import *
from Scheduler import *
from System import *

class ScheduleGenerationForm(Form):
   #initialisation
    def __init__(self):
        # Create child controls and initialize form
        self.Text = 'Schedule Generation'
        self.Name = 'frmScheduleGeneration'

        self.initialiseControls()

        self.callerForm = None
        
        self.conn = sqlite3.connect("schedulerDatabase.db")
        self.cursor = self.conn.cursor()

        self.columns = 8
        self.rows = 5

        self.timetables = []
        self.fillTimetableList()
        self.events = []
        self.classes = []

        # set up array with hard coded timetable
        self.timetable = Array.CreateInstance(str, self.rows, self.columns)
        # timetable cells
        #timetable[0,0] = "tt1"
        #timetable[0,1] = "tt1"
        #timetable[1,5] = "tt2"
        #timetable[1,6] = "tt2"
        #timetable[1,7] = "tt5"
        #timetable[3,0] = "tt3"
        #timetable[3,1] = "tt3"
        #timetable[3,4] = "tt4"
        #timetable[3,6] = "tt3"
        #timetable[4,4] = "tt5"
        #timetable[4,5] = "tt5"
        #timetable[4,6] = "tt6"
        #timetable[4,7] = "tt6"

        # set up hardcoded events/classes
        #self.events = [EventSlot('gym', 'et1', ['monday'], 'morning'), EventSlot('washing', 'et2', ['tuesday'], 'any')]
        #self.classes = [TimetableSlot('abc', 'tt1', 's1', 'dave'),TimetableSlot('def', 'tt2', 's2', 'chris'),TimetableSlot('ghi', 'tt3', 's3', 'hayley'),
        #                TimetableSlot('jkl', 'tt4', 's4', 'annie'),TimetableSlot('mno', 'tt5', 's5', 'jake'),TimetableSlot('pqr', 'tt6', 's6', 'anthony')]

        # set up grid
        self.grdSchedule.Columns.Clear()
        for i in range(self.columns):
             self.grdSchedule.Columns.Add("" ,"%s - %s" % (i+9, i+10))   

        self.scheduler = Scheduler()
        #self.scheduler.setTimetable()
        #self.scheduler.setEvents()

        # add array to grid
        # self.updateGrid(timetable)
        #row = Array.CreateInstance(str, columns)
        #for x in range(rows):
        #    for y in range(columns):
        #        row[y] = timetable[x,y]

        #    self.grdSchedule.Rows.Add(row)
        

    def initialiseControls(self):
        
        self.ClientSize = Size(1280, 720);
        self.FormBorderStyle = FormBorderStyle.FixedDialog

        ## main controls
        self.mainPanel = Panel()
        self.mainPanel.ForeColor = Color.Blue
        self.mainPanel.BackColor = Color.LightSlateGray
        self.mainPanel.Location = Point(0, 0)
        self.mainPanel.Size = Size(1280, 720)

        # title label
        self.lblTitle = Label()
        self.lblTitle.Text = "Schedule Generation"
        self.lblTitle.Location = Point(10, 10)
        self.lblTitle.Size = Size(900, 35);
        
        # schedule grid data view
        self.grdSchedule = DataGridView();
        self.grdSchedule.Location = Point(10, 50);
        self.grdSchedule.Name = "grdSchedule";
        self.grdSchedule.Size = Size(900, 650);
        self.grdSchedule.RowsDefaultCellStyle.WrapMode = DataGridViewTriState.True
        self.grdSchedule.AutoSizeRowsMode = DataGridViewAutoSizeRowsMode.AllCells

        # schedule name label
        self.lblScheduleName = Label()
        self.lblScheduleName.Text = "Schedule Name"
        self.lblScheduleName.Location = Point(970, 580)
        self.lblScheduleName.Size = Size(100, 20)
        
        # schedule name textbox
        self.tbxScheduleName = TextBox()
        self.tbxScheduleName.Location = Point(1070, 580)
        self.tbxScheduleName.Size = Size(150, 20);

        # save button
        self.btnSave = Button()
        self.btnSave.Text = 'Save Changes'
        self.btnSave.Location = Point(1000, 650)
        self.btnSave.Click += self.saveSchedulePressed

        # back button
        self.btnBack = Button()
        self.btnBack.Text = 'Back To Menu'
        self.btnBack.Location = Point(1150, 650)
        self.btnBack.Click += self.btnExitPress

        # add controls to panel
        self.mainPanel.Controls.Add(self.lblTitle)
        self.mainPanel.Controls.Add(self.lblScheduleName)
        self.mainPanel.Controls.Add(self.tbxScheduleName)
        self.mainPanel.Controls.Add(self.btnSave)
        self.mainPanel.Controls.Add(self.btnBack)
        self.mainPanel.Controls.Add(self.grdSchedule)

        
        ## sub panel containing grid controls
        # panel title label above panel
        self.lblGridControlTitle = Label()
        self.lblGridControlTitle.Text = "Schedule Management"
        self.lblGridControlTitle.Location = Point(960, 15)
        self.lblGridControlTitle.Size = Size(290, 20)
        self.mainPanel.Controls.Add(self.lblGridControlTitle)

        self.gridControlPanel = Panel()
        self.gridControlPanel.ForeColor = Color.Blue
        self.gridControlPanel.BackColor = Color.Gray
        self.gridControlPanel.Location = Point(950, 35)
        self.gridControlPanel.Size = Size(300, 500);
        
        # generate schedule button
        self.btnGenerate = Button()
        self.btnGenerate.Text = 'Generate Schedules'
        self.btnGenerate.Location = Point(10, 50)
        self.btnGenerate.Click += self.btnSchedulePress
        
        # timetables combobox
        self.cbxTimetables = ComboBox()
        self.cbxTimetables.DropDownStyle = ComboBoxStyle.DropDownList;
        self.cbxTimetables.Location = Point(10, 250)
        self.cbxTimetables.SelectedIndexChanged += self.timetableSelectionChanged

        # open manage timetables form button
        self.btnTimetable = Button()
        self.btnTimetable.Text = 'Manage Timetables'
        self.btnTimetable.Location = Point(200, 250)
        self.btnTimetable.Click += self.btnTimetablePress
        
        # open manage activities form button
        self.btnActivities = Button()
        self.btnActivities.Text = 'Manage Events'
        self.btnActivities.Location = Point(10, 450)
        self.btnActivities.Click += self.btnEventsPress

        # add controls to panel
        self.gridControlPanel.Controls.Add(self.btnGenerate)
        self.gridControlPanel.Controls.Add(self.cbxTimetables)
        self.gridControlPanel.Controls.Add(self.btnTimetable)
        self.gridControlPanel.Controls.Add(self.btnActivities)

        # add panels
        self.mainPanel.Controls.Add(self.gridControlPanel)
        self.Controls.Add(self.mainPanel)
        

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


    def retrieveClassSlot(self, code):
        for timetableClass in self.classes:
            if (timetableClass.code == code):
                return timetableClass

    def retrieveEventSlot(self, code):
        for event in self.events:
            if (event.code == code):
                return event

    def fillTimetableList(self):
        sql = "SELECT code, name FROM TimetableSchedules"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        self.cbxTimetables.Items.Clear()
        for row in results:
            self.timetables.Add(row[0])
            self.cbxTimetables.Items.Add(row[1])
    
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
                        self.timetable[x,y] = result[index]
                else:
                    self.timetable[x,y] = None
                
                i = i + 1

        self.updateGrid(self.timetable)

    def checkForClass(self, code):
        
        for timetableClass in self.classes:
            if (timetableClass == code):
                return True

        return False

    def getClassFromDB(self, code):
        sql = "SELECT * FROM ScheduleClasses WHERE code = '" + code + "'"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()

        return TimetableSlot(result[1], result[0], result[2], result[3])

    def generateScheduleCode(self):
        index = 1
        prefix = 'fs'

        sql = "SELECT code FROM FullSchedules"
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


    def convertSlotsToSQL(self):
        sql = ''
        for x in range(self.rows):
            for y in range(self.columns):
                if (self.schedule[x,y]):
                    sql = sql + "'" + self.schedule[x,y] + "',"
                else:
                    sql = sql + "'',"

        return sql[:-1]

# UI events
    def btnSchedulePress(self, sender, args):
        self.grdSchedule.Rows.Clear()

        self.schedule = self.scheduler.GenerateSchedule()
        
        self.updateGrid(self.schedule)
        #row = Array.CreateInstance(str, self.schedule.GetLength(1))
        #for x in range(self.schedule.GetLength(0)):
        #    for y in range(self.schedule.GetLength(1)):
        #        row[y] = self.schedule[x,y]

        #    self.grdSchedule.Rows.Add(row)

    def saveSchedulePressed(self, sender, args):
        code = self.generateScheduleCode()
        name = self.tbxScheduleName.Text
        sql = """
                INSERT INTO FullSchedules
                VALUES ('""" + str(code) + "','" + str(name) + "'," + self.convertSlotsToSQL() + ")"
              
        self.cursor.execute(sql)
        self.conn.commit()
        self.fillTimetableList()

    def timetableSelectionChanged(self, sender, args):
        self.displaySavedTimetable(self.cbxTimetables.SelectedIndex)
        self.scheduler.setTimetable(self.timetable)

    def btnTimetablePress(self, sender, args):
        timetableForm = TimetableInputForm()
        timetableForm.callerForm = self
        timetableForm.Show()
        self.Hide()

    def btnEventsPress(self, sender, args):
        eventsForm = EventManagementForm(self.events)
        eventsForm.callerForm = self
        eventsForm.Show()
        self.Hide()

    def btnExitPress(self, sender, args):
        self.conn.close()
        self.callerForm.Show()
        self.Close()
        
#Application.EnableVisualStyles()
#Application.SetCompatibleTextRenderingDefault(False)

#form = ScheduleGenerationForm()
#Application.Run(form)
