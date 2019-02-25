import clr
from System import Array
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

from System.Drawing import *
from System.Windows.Forms import *

class EventManagementForm(Form):
    #initialisation
    def __init__(self):
        self.Text = 'Event Management'
        self.Name = 'frmEventManagement'
        
        self.initialiseControls()


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
        self.lblTitle.Text = "Event Management"
        self.lblTitle.Location = Point(0, 15)
        self.lblTitle.Size = Size(1280, 20)

        # activities title label
        self.lblActivitiesTitle = Label()
        self.lblActivitiesTitle.Text = "Events"
        self.lblActivitiesTitle.Location = Point(700, 45)
        self.lblActivitiesTitle.Size = Size(600, 20)

        # activities list box
        self.lbxActivities = ListBox()
        self.lbxActivities.Location = Point(700, 75)
        self.lbxActivities.Size = Size(300, 570)

        # edit button
        self.btnEdit = Button()
        self.btnEdit.Text = 'Edit Event'
        self.btnEdit.Location = Point(1100, 200)
        
        # remove button
        self.btnRemove = Button()
        self.btnRemove.Text = 'Remove Event'
        self.btnRemove.Location = Point(1100, 400)

        # back button
        self.btnBack = Button()
        self.btnBack.Text = 'Back'
        self.btnBack.Location = Point(550, 675)

        # add controls to panel
        self.mainPanel.Controls.Add(self.lblTitle)
        self.mainPanel.Controls.Add(self.lblActivitiesTitle)
        self.mainPanel.Controls.Add(self.lbxActivities)
        self.mainPanel.Controls.Add(self.btnEdit)
        self.mainPanel.Controls.Add(self.btnRemove)
        self.mainPanel.Controls.Add(self.btnBack)

        ## sub panel for input controls
        self.inputPanel = Panel()
        self.inputPanel.ForeColor = Color.Blue
        self.inputPanel.BackColor = Color.Gray
        self.inputPanel.Location = Point(15, 45)
        self.inputPanel.Size = Size(600, 600)

        # activity name label
        self.lblActivityName = Label()
        self.lblActivityName.Text = "Name"
        self.lblActivityName.Location = Point(10, 20)
        self.lblActivityName.Size = Size(100, 20)
        
        # activity name textbox
        self.tbxActivityName = TextBox()
        self.tbxActivityName.Location = Point(210, 20)
        self.tbxActivityName.Size = Size(150, 20);

        # activity days label
        self.lblActivityDays = Label()
        self.lblActivityDays.Text = "Days"
        self.lblActivityDays.Location = Point(10, 200)
        self.lblActivityDays.Size = Size(100, 20)

        ## activity days checkbox panel
        self.daysPanel = Panel()
        self.daysPanel.ForeColor = Color.Blue
        self.daysPanel.BackColor = Color.LightGray
        self.daysPanel.Location = Point(220, 150)
        self.daysPanel.Size = Size(300, 175)
        # activity days checkboxes
        self.cbMonday = CheckBox()      #mon
        self.cbMonday.Text = "Monday"
        self.cbMonday.Location = Point(5, 5)
        self.cbMonday.Size = Size(350, 20)
        self.cbTuesday = CheckBox()     #tue
        self.cbTuesday.Text = "Tuesday"
        self.cbTuesday.Location = Point(5, 30)
        self.cbTuesday.Size = Size(350, 20)
        self.cbWednesday = CheckBox()     #wed
        self.cbWednesday.Text = "Wednesday"
        self.cbWednesday.Location = Point(5, 55)
        self.cbWednesday.Size = Size(350, 20)
        self.cbThursday = CheckBox()     #thur
        self.cbThursday.Text = "Thursday"
        self.cbThursday.Location = Point(5, 80)
        self.cbThursday.Size = Size(350, 20)
        self.cbFriday = CheckBox()     #fri
        self.cbFriday.Text = "Friday"
        self.cbFriday.Location = Point(5, 105)
        self.cbFriday.Size = Size(350, 20)

        self.daysPanel.Controls.Add(self.cbMonday)
        self.daysPanel.Controls.Add(self.cbTuesday)
        self.daysPanel.Controls.Add(self.cbWednesday)
        self.daysPanel.Controls.Add(self.cbThursday)
        self.daysPanel.Controls.Add(self.cbFriday)

        # activity time label
        self.lblActivityTime = Label()
        self.lblActivityTime.Text = "Time"
        self.lblActivityTime.Location = Point(10, 370)
        self.lblActivityTime.Size = Size(100, 20)

        # activity time combobox
        self.cbxActivityTime = ComboBox()
        self.cbxActivityTime.DropDownStyle = ComboBoxStyle.DropDownList;
        self.cbxActivityTime.Location = Point(220, 370)
        self.cbxActivityTime.Size = Size(280, 20);

        # activity add button
        self.btnAddActivity = Button()
        self.btnAddActivity.Text = 'Add Event'
        self.btnAddActivity.Location = Point(50, 450)
        
        # activity clear button
        self.btnClearActivity = Button()
        self.btnClearActivity.Text = 'Clear'
        self.btnClearActivity.Location = Point(250, 450)

        # add contros to panel
        self.inputPanel.Controls.Add(self.lblActivityName)
        self.inputPanel.Controls.Add(self.tbxActivityName)
        self.inputPanel.Controls.Add(self.lblActivityDays)
        self.inputPanel.Controls.Add(self.daysPanel)
        self.inputPanel.Controls.Add(self.lblActivityTime)
        self.inputPanel.Controls.Add(self.cbxActivityTime)
        self.inputPanel.Controls.Add(self.btnAddActivity)
        self.inputPanel.Controls.Add(self.btnClearActivity)

        # add subpanel
        self.mainPanel.Controls.Add(self.inputPanel)

        # add panels
        self.Controls.Add(self.mainPanel)

        pass


