import clr
import sqlite3

clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

from System.Drawing import *
from System.Windows.Forms import *
from System import Array
from ScheduleGenerationForm import *
from TimetableInputForm import *
from ScheduleDisplayForm import *

class MainMenuForm(Form):
    #initialisation
    def __init__(self):
        self.Text = 'Main Menu'
        self.Name = 'frmMainMenu'
        
        self.initialiseControls()

        self.initialiseDB()


    def initialiseControls(self):
        self.ClientSize = Size(600, 720);
        self.FormBorderStyle = FormBorderStyle.FixedDialog

        ## main controls
        self.mainPanel = Panel()
        self.mainPanel.ForeColor = Color.Blue
        self.mainPanel.BackColor = Color.LightSlateGray
        self.mainPanel.Location = Point(0, 0)
        self.mainPanel.Size = Size(600, 720)      #(self.ClientSize.Height, self.ClientSize.Width)

        # form title label
        self.lblTitle = Label()
        self.lblTitle.Text = "Main Menu"
        self.lblTitle.Location = Point(0, 15)
        self.lblTitle.Size = Size(600, 20)

        ## info subpanel
        self.infoPanel = Panel()
        self.infoPanel.ForeColor = Color.Blue
        self.infoPanel.BackColor = Color.DarkGray
        self.infoPanel.Location = Point(100, 50)
        self.infoPanel.Size = Size(400, 200)
        # info label
        self.lblInfo = Label()
        self.lblInfo.Text = "info"
        self.lblInfo.Location = Point(10, 10)
        self.lblInfo.Size = Size(380, 180)
        # add controls to panel
        self.infoPanel.Controls.Add(self.lblInfo)

        # schedule form button
        self.btnSchedule = Button()
        self.btnSchedule.Text = 'Schedule Generation'
        self.btnSchedule.Location = Point(150, 250)
        self.btnSchedule.Click += self.btnSchedulePress

        # timetable form button
        self.btnTimetable = Button()
        self.btnTimetable.Text = 'Timetable Input'
        self.btnTimetable.Location = Point(150, 350)
        self.btnTimetable.Click += self.btnTimetablePress

        # view schedule form button
        self.btnViewSchedule = Button()
        self.btnViewSchedule.Text = 'View Schedule'
        self.btnViewSchedule.Location = Point(150, 500)
        self.btnViewSchedule.Click += self.btnDisplayPress

        # exit button
        self.btnExit = Button()
        self.btnExit.Text = 'Exit'
        self.btnExit.Location = Point(150, 650)

        # add controls to panel
        self.mainPanel.Controls.Add(self.lblTitle)
        self.mainPanel.Controls.Add(self.infoPanel)
        self.mainPanel.Controls.Add(self.btnSchedule)
        self.mainPanel.Controls.Add(self.btnTimetable)
        self.mainPanel.Controls.Add(self.btnViewSchedule)
        self.mainPanel.Controls.Add(self.btnExit)

        self.Controls.Add(self.mainPanel)

    def initialiseDB(self):
        # connect to db
        conn = sqlite3.connect("schedulerDatabase.db")
        cursor = conn.cursor()
        
        # create tables if they dont exist
        sql = """
                CREATE TABLE IF NOT EXISTS FullSchedules 
                (code text PRIMARY KEY,name text,""" + self.insertTableLength() + ")"
        cursor.execute(sql)

        sql = """
                CREATE TABLE IF NOT EXISTS TimetableSchedules 
                (code text PRIMARY KEY,name text,""" + self.insertTableLength() + ")"
        cursor.execute(sql)
        
        sql= """
                CREATE TABLE IF NOT EXISTS ScheduleClasses 
                (code text PRIMARY KEY,name text,room text,teacher text);
             """
        cursor.execute(sql)
        
        sql= """
                CREATE TABLE IF NOT EXISTS ScheduleEvents 
                (code text PRIMARY KEY,name text,days text,time text);
             """
        cursor.execute(sql)
        
        conn.commit()
        # close connection to db
        conn.close()

    def insertTableLength(self):
        rows = 5
        columns = 8
        sql = ""
        for i in range(rows * columns):
            if (i == (rows * columns) - 1):
                sql = sql + "slot" + str(i) + " text"
            else:
                sql = sql + "slot" + str(i) + " text,"

        return sql

# button events
    def btnSchedulePress(self, sender, args):
        scheduleForm = ScheduleGenerationForm()
        scheduleForm.callerForm = self
        scheduleForm.Show()
        self.Hide()

    def btnTimetablePress(self, sender, args):
        timetableForm = TimetableInputForm()
        timetableForm.callerForm = self
        timetableForm.Show()
        self.Hide()

    def btnDisplayPress(self, sender, args):
        displayForm = ScheduleDisplayForm()
        displayForm.callerForm = self
        displayForm.Show()
        self.Hide()

Application.EnableVisualStyles()
Application.SetCompatibleTextRenderingDefault(False)

form = MainMenuForm()
Application.Run(form)
