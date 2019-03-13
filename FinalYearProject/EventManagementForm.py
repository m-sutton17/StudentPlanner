import clr
from System import Array
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

from System.Drawing import *
from System.Windows.Forms import *
#from ScheduleGenerationForm import *
from Scheduler import Event

class EventManagementForm(Form):
    #initialisation
    def __init__(self, events):
        self.Text = 'Event Management'
        self.Name = 'frmEventManagement'

        self.callerForm = None
        self.events = events
        self.inputMode = 'add'
        self.editingIndex = -1
        
        self.initialiseControls()

        self.displayEvents()

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
        self.lblEventTitle = Label()
        self.lblEventTitle.Text = "Events"
        self.lblEventTitle.Location = Point(700, 45)
        self.lblEventTitle.Size = Size(600, 20)

        # activities list box
        self.lbxEvents = ListBox()
        self.lbxEvents.Location = Point(700, 75)
        self.lbxEvents.Size = Size(300, 570)

        # new event button
        self.btnNew = Button()
        self.btnNew.Text = 'Add New Event'
        self.btnNew.Location = Point(1100, 200)
        self.btnNew.Click += self.btnNewPress

        # edit button
        self.btnEdit = Button()
        self.btnEdit.Text = 'Edit Event'
        self.btnEdit.Location = Point(1100, 300)
        self.btnEdit.Click += self.btnEditPress
        
        # remove button
        self.btnRemove = Button()
        self.btnRemove.Text = 'Remove Event'
        self.btnRemove.Location = Point(1100, 400)

        # back button
        self.btnBack = Button()
        self.btnBack.Text = 'Back'
        self.btnBack.Location = Point(550, 675)
        self.btnBack.Click += self.btnExitPress

        # add controls to panel
        self.mainPanel.Controls.Add(self.lblTitle)
        self.mainPanel.Controls.Add(self.lblEventTitle)
        self.mainPanel.Controls.Add(self.lbxEvents)
        self.mainPanel.Controls.Add(self.btnNew)
        self.mainPanel.Controls.Add(self.btnEdit)
        self.mainPanel.Controls.Add(self.btnRemove)
        self.mainPanel.Controls.Add(self.btnBack)

        ## sub panel for input controls
        self.inputPanel = Panel()
        self.inputPanel.ForeColor = Color.Blue
        self.inputPanel.BackColor = Color.Gray
        self.inputPanel.Location = Point(15, 45)
        self.inputPanel.Size = Size(600, 600)

        # editing mode label
        self.lblEditingMode = Label()
        self.lblEditingMode.Text = "Adding new event"
        self.lblEditingMode.Location = Point(10, 20)
        self.lblEditingMode.Size = Size(100, 20)

        # event name label
        self.lblEventName = Label()
        self.lblEventName.Text = "Name"
        self.lblEventName.Location = Point(10, 50)
        self.lblEventName.Size = Size(100, 20)
        
        # event name textbox
        self.tbxEventName = TextBox()
        self.tbxEventName.Location = Point(210, 50)
        self.tbxEventName.Size = Size(150, 20);

        # event days label
        self.lblEventDays = Label()
        self.lblEventDays.Text = "Days"
        self.lblEventDays.Location = Point(10, 200)
        self.lblEventDays.Size = Size(100, 20)

        ## event days checkbox panel
        self.daysPanel = Panel()
        self.daysPanel.ForeColor = Color.Blue
        self.daysPanel.BackColor = Color.LightGray
        self.daysPanel.Location = Point(220, 150)
        self.daysPanel.Size = Size(300, 175)
        # event days checkboxes
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

        # event time label
        self.lblEventTime = Label()
        self.lblEventTime.Text = "Time"
        self.lblEventTime.Location = Point(10, 370)
        self.lblEventTime.Size = Size(100, 20)

        # event time combobox
        self.cbxEventTime = ComboBox()
        self.cbxEventTime.DropDownStyle = ComboBoxStyle.DropDownList;
        self.cbxEventTime.Location = Point(220, 370)
        self.cbxEventTime.Size = Size(280, 20);
        self.cbxEventTime.Items.Add('Any')
        self.cbxEventTime.Items.Add('Morning')
        self.cbxEventTime.Items.Add('Afternoon')

        # event add button
        self.btnAddEvent = Button()
        self.btnAddEvent.Text = 'Add Event'
        self.btnAddEvent.Location = Point(50, 450)
        self.btnAddEvent.Click += self.btnAddPress
        
        # event clear button
        self.btnClearEvent = Button()
        self.btnClearEvent.Text = 'Clear'
        self.btnClearEvent.Location = Point(250, 450)
        self.btnClearEvent.Click += self.btnClearPress

        # add contros to panel
        self.inputPanel.Controls.Add(self.lblEventName)
        self.inputPanel.Controls.Add(self.tbxEventName)
        self.inputPanel.Controls.Add(self.lblEventDays)
        self.inputPanel.Controls.Add(self.daysPanel)
        self.inputPanel.Controls.Add(self.lblEventTime)
        self.inputPanel.Controls.Add(self.cbxEventTime)
        self.inputPanel.Controls.Add(self.btnAddEvent)
        self.inputPanel.Controls.Add(self.btnClearEvent)

        # add subpanel
        self.mainPanel.Controls.Add(self.inputPanel)

        # add panels
        self.Controls.Add(self.mainPanel)

# button events
    def btnAddPress(self, sender, args):
        self.addEvent()

    def btnClearPress(self, sender, args):
        self.clearInputControls()

    def btnNewPress(self, sender, args):
        self.btnAddEvent.Text = 'Add Event'
        self.inputMode = 'add'
        self.editingIndex = -1
        self.clearInputControls()
        
    def btnEditPress(self, sender, args):
        if (self.lbxEvents.SelectedIndex != -1):
            self.btnAddEvent.Text = 'Update Event'
            self.inputMode = 'edit'
            self.editingIndex = self.lbxEvents.SelectedIndex
            self.displaySelectedEvent(self.lbxEvents.SelectedIndex)
        else:
            print('nothing selected')

    def btnExitPress(self, sender, args):
        self.callerForm.scheduler.setEvents(self.events)
        self.callerForm.Show()
        self.Close()
        pass

# methods
    def addEvent(self):
        invalidReason = 'none'

        # name
        if (self.tbxEventName.Text != ''):
            name = self.tbxEventName.Text
        else:
            invalidReason = 'No name entered'

        # days
        daySelected = False
        days = []
        if (self.cbMonday.Checked):
            days.append('monday')
            daySelected = True
        if (self.cbTuesday.Checked):
            days.append('tuesday')
            daySelected = True
        if (self.cbWednesday.Checked):
            days.append('wednesday')
            daySelected = True
        if (self.cbThursday.Checked):
            days.append('thursday')
            daySelected = True
        if (self.cbFriday.Checked):
            days.append('friday')
            daySelected = True

        if (daySelected == False):
            invalidReason = 'No day selected'

        # time
        if (self.cbxEventTime.Text != ''):
            time = self.cbxEventTime.Text
        else:
            invalidReason = 'No time selected'

        if (invalidReason == 'none'):
            if (self.inputMode == 'add'):
                self.events.append(Event(name, self.generateEventCode(), days, time))
            elif (self.inputMode == 'edit' and self.editingIndex != -1):
                self.events[self.editingIndex] = Event(name, self.generateEventCode(), days, time)
            self.displayEvents()
        else:
            print(invalidReason)

    def generateEventCode(self):
        index = 1
        prefix = 'et'

        free = False
        while free == False:
            found = False
            for event in self.events:
                if (prefix + str(index) == event.code):
                    found = True

            if (found == False):
                free = True
            else:
                index = index + 1

        return prefix + str(index)

    def displayEvents(self):
        self.lbxEvents.Items.Clear()
        for event in self.events:
            self.lbxEvents.Items.Add(event.name)
        pass

    def displaySelectedEvent(self, index):
        self.clearInputControls()
        # get selected event
        event = self.events[index]

        self.tbxEventName.Text = event.name
        for day in event.days:
            if (day == 'monday'):
                self.cbMonday.Checked = True
            if (day == 'tuesday'):
                self.cbTuesday.Checked = True
            if (day == 'wednesday'):
                self.cbWednesday.Checked = True
            if (day == 'thursday'):
                self.cbThursday.Checked = True
            if (day == 'friday'):
                self.cbFriday.Checked = True
        self.cbxEventTime.SelectedIndex = self.cbxEventTime.FindString(event.time)

    def clearInputControls(self):
        self.tbxEventName.Text = ''
        self.cbMonday.Checked = False
        self.cbTuesday.Checked = False
        self.cbWednesday.Checked = False
        self.cbThursday.Checked = False
        self.cbFriday.Checked = False
        self.cbxEventTime.SelectedIndex = -1

#Application.EnableVisualStyles()
#Application.SetCompatibleTextRenderingDefault(False)

#form = EventManagementForm()
#Application.Run(form)