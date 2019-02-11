import clr
from TimetableInputForm import TimetableInputForm
from ActivityManagementForm import ActivityManagementForm
from System import Array
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
        schedule = Array.CreateInstance(str, rows, columns)
        # timetable cells
        # 1,0 1,1 1,2 1,5 1,6 1,7
        # 3,0 3,1 3,4 3,6
        # 4,4 4,5 4,6 4,7
        schedule[1,0] = "O"
        schedule[1,1] = "O"
        schedule[1,2] = "O"
        schedule[1,5] = "O"
        schedule[1,6] = "O"
        schedule[1,7] = "O"
        schedule[3,0] = "O"
        schedule[3,1] = "O"
        schedule[3,4] = "O"
        schedule[3,6] = "O"
        schedule[4,4] = "O"
        schedule[4,5] = "O"
        schedule[4,6] = "O"
        schedule[4,7] = "O"

        # set up grid
        self.grdSchedule.Columns.Clear()
        for i in range(columns):
             self.grdSchedule.Columns.Add("" ,"%s - %s" % (i+9, i+10))   # (i+9) + " - " + (i+10)

        # add array to grid
        row = Array.CreateInstance(str, columns)
        for x in range(rows):
            for y in range(columns):
                row[y] = schedule[x,y]

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
        #self.btnGenerate.Click += self.buttonPressed
        
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
        self.btnActivities.Text = 'Manage Activities'
        self.btnActivities.Location = Point(10, 450)
        self.btnActivities.Click += self.btnActivitiesPress

        # add controls to panel
        self.gridControlPanel.Controls.Add(self.btnGenerate)
        self.gridControlPanel.Controls.Add(self.cbxTimetables)
        self.gridControlPanel.Controls.Add(self.btnTimetable)
        self.gridControlPanel.Controls.Add(self.btnActivities)

        # add panels
        self.mainPanel.Controls.Add(self.gridControlPanel)
        self.Controls.Add(self.mainPanel)
        

# button events
    def btnTimetablePress(self, sender, args):
        #print 'The label *used to say* : %s' % self.label.Text
        #print 'Button Pressed'
        #self.lblTitle.Text = "You clicked the button."
        timetableForm = TimetableInputForm()
        timetableForm.Show()
        self.Hide()

    def btnActivitiesPress(self, sender, args):
        #print 'The label *used to say* : %s' % self.label.Text
        #print 'Button Pressed'
        #self.lblTitle.Text = "You clicked the button."
        activitiesForm = ActivityManagementForm()
        activitiesForm.Show()
        self.Hide()
        
#Application.EnableVisualStyles()
#Application.SetCompatibleTextRenderingDefault(False)

#form = ScheduleGenerationForm()
#Application.Run(form)
