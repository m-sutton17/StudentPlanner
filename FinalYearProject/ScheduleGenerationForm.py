import clr
from TimetableInputForm import *
from EventManagementForm import *
from Scheduler import *
from System import *
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

from System.Drawing import *
from System.Windows.Forms import *

class ScheduleGenerationForm(Form):
   #initialisation
    def __init__(self):
        # Create child controls and initialize form
        self.Text = 'Schedule Generation'
        self.Name = 'frmScheduleGeneration'

        self.initialiseControls()

        columns = 8
        rows = 5
        
        # set up array with hard coded timetable
        timetable = Array.CreateInstance(str, rows, columns)
        # timetable cells
        # 1,0 1,1 1,2 1,5 1,6 1,7
        # 3,0 3,1 3,4 3,6
        # 4,4 4,5 4,6 4,7
        timetable[1,0] = "tt1"
        timetable[1,1] = "tt1"
        timetable[1,2] = "tt1"
        timetable[1,5] = "tt2"
        timetable[1,6] = "tt2"
        timetable[1,7] = "tt5"
        timetable[3,0] = "tt3"
        timetable[3,1] = "tt3"
        timetable[3,4] = "tt4"
        timetable[3,6] = "tt3"
        timetable[4,4] = "tt5"
        timetable[4,5] = "tt5"
        timetable[4,6] = "tt6"
        timetable[4,7] = "tt6"

        # set up hardcoded events
        events = [Event('gym', 'et1')]

        # set up grid
        self.grdSchedule.Columns.Clear()
        for i in range(columns):
             self.grdSchedule.Columns.Add("" ,"%s - %s" % (i+9, i+10))   # (i+9) + " - " + (i+10)

        self.Scheduler = Scheduler()
        self.Scheduler.setTimetable(timetable)
        self.Scheduler.setEvents(events)

        # add array to grid
        row = Array.CreateInstance(str, columns)
        for x in range(rows):
            for y in range(columns):
                row[y] = timetable[x,y]

            self.grdSchedule.Rows.Add(row)
        

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
        self.grdSchedule.Name = "grdGame";
        self.grdSchedule.Size = Size(900, 650);

        # save button
        self.btnSave = Button()
        self.btnSave.Text = 'Save Changes'
        self.btnSave.Location = Point(1000, 600)
        #self.btnSave.Click += self.buttonPressed

        # back button
        self.btnBack = Button()
        self.btnBack.Text = 'Back To Menu'
        self.btnBack.Location = Point(1150, 600)
        #self.btnBack.Click += self.buttonPressed

        # add controls to panel
        self.mainPanel.Controls.Add(self.lblTitle)
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
        

# button events
    def btnSchedulePress(self, sender, args):
        self.grdSchedule.Rows.Clear()

        self.schedule = self.Scheduler.GenerateSchedule()
        
        row = Array.CreateInstance(str, self.schedule.GetLength(1))
        for x in range(self.schedule.GetLength(0)):
            for y in range(self.schedule.GetLength(1)):
                row[y] = self.schedule[x,y]

            self.grdSchedule.Rows.Add(row)
        pass

    def btnTimetablePress(self, sender, args):
        timetableForm = TimetableInputForm()
        timetableForm.Show()
        self.Hide()

    def btnEventsPress(self, sender, args):
        activitiesForm = ActivityManagementForm()
        activitiesForm.Show()
        self.Hide()
        
Application.EnableVisualStyles()
Application.SetCompatibleTextRenderingDefault(False)

form = ScheduleGenerationForm()
Application.Run(form)
