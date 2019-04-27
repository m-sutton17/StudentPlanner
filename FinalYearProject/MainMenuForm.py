import clr


clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')
clr.AddReference("IronPython.SQLite")

import sqlite3

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
        self.MaximizeBox = False

        buttonFont = Font("Open Sans", 18)
        titleFont = Font("Open Sans", 18)
        textFont = Font("Open Sans", 9)

        ## main controls
        self.mainPanel = Panel()
        self.mainPanel.ForeColor = Color.Black
        self.mainPanel.BackColor = Color.FromArgb(161, 162, 163)
        self.mainPanel.Location = Point(0, 0)
        self.mainPanel.Size = Size(600, 720)      #(self.ClientSize.Height, self.ClientSize.Width)

        # form title label
        self.lblTitle = Label()
        self.lblTitle.Text = "Main Menu"
        self.lblTitle.Location = Point(240, 10)
        self.lblTitle.Size = Size(600, 40)
        self.lblTitle.Font = titleFont

        ## info subpanel
        self.infoPanel = Panel()
        self.infoPanel.ForeColor = Color.Black
        self.infoPanel.BackColor = Color.FromArgb(226, 226, 226)
        self.infoPanel.Location = Point(100, 50)
        self.infoPanel.Size = Size(400, 200)
        # info label
        self.lblInfo = Label()
        self.lblInfo.Text = 'Welcome.\nThis schedule generator will help organise your educational and free time effectively. Enter your timetable in the Timetable Input section and select it when generating a schedule. '   \
            + 'Before generating, input your desired extra activities in the Event Management section. Then click generate and your customised schedule will be created. You can then save this schedule and export it in the View Schedule section'
        self.lblInfo.Location = Point(10, 10)
        self.lblInfo.Size = Size(380, 180)
        self.lblInfo.Font = textFont
        self.lblInfo.TextAlign = ContentAlignment.MiddleCenter
        # add controls to panel
        self.infoPanel.Controls.Add(self.lblInfo)

        # schedule form button
        self.btnSchedule = Button()
        self.btnSchedule.Text = 'Schedule Generation'
        self.btnSchedule.Location = Point(150, 275)
        self.btnSchedule.Size = Size(325, 60)
        self.btnSchedule.Font = buttonFont
        self.btnSchedule.BackColor = Color.FromArgb(0, 99, 160)
        self.btnSchedule.Click += self.btnSchedulePress

        # timetable form button
        self.btnTimetable = Button()
        self.btnTimetable.Text = 'Timetable Input'
        self.btnTimetable.Location = Point(150, 375)
        self.btnTimetable.Size = Size(325, 60)
        self.btnTimetable.Font = buttonFont
        self.btnTimetable.BackColor = Color.FromArgb(0, 99, 160)
        self.btnTimetable.Click += self.btnTimetablePress

        # view schedule form button
        self.btnViewSchedule = Button()
        self.btnViewSchedule.Text = 'View Schedule'
        self.btnViewSchedule.Location = Point(150, 475)
        self.btnViewSchedule.Size = Size(325, 60)
        self.btnViewSchedule.Font = buttonFont
        self.btnViewSchedule.BackColor = Color.FromArgb(0, 99, 160)
        self.btnViewSchedule.Click += self.btnDisplayPress

        # exit button
        self.btnExit = Button()
        self.btnExit.Text = 'Exit'
        self.btnExit.Location = Point(150, 575)
        self.btnExit.Size = Size(325, 60)
        self.btnExit.BackColor = Color.FromArgb(0, 99, 160)
        self.btnExit.Font = buttonFont
        self.btnExit.Click += self.btnExitPress

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

    def btnExitPress(self, sender, args):
        self.Close()

Application.EnableVisualStyles()
Application.SetCompatibleTextRenderingDefault(False)

form = MainMenuForm()
Application.Run(form)
