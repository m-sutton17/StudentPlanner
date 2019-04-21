import clr

from System import Array
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')
clr.AddReference("IronPython.SQLite")

import sqlite3

from System.Drawing import *
from System.Windows.Forms import *
#from ScheduleGenerationForm import *
from Scheduler import EventSlot

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

        self.conn = sqlite3.connect("schedulerDatabase.db")
        self.cursor = self.conn.cursor()

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
        self.lblTitle.Text = "Event Management"
        self.lblTitle.Location = Point(10, 5)
        self.lblTitle.Size = Size(1280, 40)
        self.lblTitle.Font = titleFont

        # activities title label
        self.lblEventTitle = Label()
        self.lblEventTitle.Text = "Events"
        self.lblEventTitle.Location = Point(700, 45)
        self.lblEventTitle.Size = Size(600, 20)
        self.lblEventTitle.Font = textFont

        # activities list box
        self.lbxEvents = ListBox()
        self.lbxEvents.Location = Point(700, 75)
        self.lbxEvents.Size = Size(300, 570)
        self.lbxEvents.Font = textFont

        # new event button
        self.btnNew = Button()
        self.btnNew.Text = 'Add New Event'
        self.btnNew.Location = Point(1050, 150)
        self.btnNew.Size = Size(175, 50)
        self.btnNew.Font = buttonFont
        self.btnNew.BackColor = Color.FromArgb(0, 99, 160)
        self.btnNew.Click += self.btnNewPress

        # edit button
        self.btnEdit = Button()
        self.btnEdit.Text = 'Edit Event'
        self.btnEdit.Location = Point(1050, 300)
        self.btnEdit.Size = Size(175, 50)
        self.btnEdit.Font = buttonFont
        self.btnEdit.BackColor = Color.FromArgb(0, 99, 160)
        self.btnEdit.Click += self.btnEditPress
        
        # remove button
        self.btnRemove = Button()
        self.btnRemove.Text = 'Remove Event'
        self.btnRemove.Location = Point(1050, 450)
        self.btnRemove.Size = Size(175, 50)
        self.btnRemove.Font = buttonFont
        self.btnRemove.BackColor = Color.FromArgb(0, 99, 160)

        # back button
        self.btnBack = Button()
        self.btnBack.Text = 'Back'
        self.btnBack.Location = Point(480, 660)
        self.btnBack.Size = Size(400, 50)
        self.btnBack.Font = buttonFont
        self.btnBack.BackColor = Color.FromArgb(0, 99, 160)
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
        self.inputPanel.ForeColor = Color.Black
        self.inputPanel.BackColor = Color.FromArgb(226, 226, 226)
        self.inputPanel.Location = Point(25, 45)
        self.inputPanel.Size = Size(600, 600)

        # editing mode label
        self.lblEditingMode = Label()
        self.lblEditingMode.Text = "Adding new event"
        self.lblEditingMode.Location = Point(475, 5)
        self.lblEditingMode.Size = Size(150, 20)
        self.lblEditingMode.Font = textFont

        # event name label
        self.lblEventName = Label()
        self.lblEventName.Text = "Name"
        self.lblEventName.Location = Point(25, 50)
        self.lblEventName.Size = Size(100, 20)
        self.lblEventName.Font = textFont
        
        # event name textbox
        self.tbxEventName = TextBox()
        self.tbxEventName.Location = Point(210, 50)
        self.tbxEventName.Size = Size(150, 20);
        self.tbxEventName.Font = textFont

        # event days label
        self.lblEventDays = Label()
        self.lblEventDays.Text = "Days"
        self.lblEventDays.Location = Point(25, 200)
        self.lblEventDays.Size = Size(100, 20)
        self.lblEventDays.Font = textFont

        ## event days checkbox panel
        self.daysPanel = Panel()
        self.daysPanel.ForeColor = Color.Black
        self.daysPanel.BackColor = Color.FromArgb(125, 169, 196)
        self.daysPanel.Location = Point(220, 150)
        self.daysPanel.Size = Size(300, 175)
        # event days checkboxes
        self.cbMonday = CheckBox()      #mon
        self.cbMonday.Text = "Monday"
        self.cbMonday.Location = Point(20, 15)
        self.cbMonday.Size = Size(350, 20)
        self.cbMonday.Font = textFont
        self.cbTuesday = CheckBox()     #tue
        self.cbTuesday.Text = "Tuesday"
        self.cbTuesday.Location = Point(20, 45)
        self.cbTuesday.Size = Size(350, 20)
        self.cbTuesday.Font = textFont
        self.cbWednesday = CheckBox()     #wed
        self.cbWednesday.Text = "Wednesday"
        self.cbWednesday.Location = Point(20, 75)
        self.cbWednesday.Size = Size(350, 20)
        self.cbWednesday.Font = textFont
        self.cbThursday = CheckBox()     #thur
        self.cbThursday.Text = "Thursday"
        self.cbThursday.Location = Point(20, 105)
        self.cbThursday.Size = Size(350, 20)
        self.cbThursday.Font = textFont
        self.cbFriday = CheckBox()     #fri
        self.cbFriday.Text = "Friday"
        self.cbFriday.Location = Point(20, 135)
        self.cbFriday.Size = Size(350, 20)
        self.cbFriday.Font = textFont

        self.daysPanel.Controls.Add(self.cbMonday)
        self.daysPanel.Controls.Add(self.cbTuesday)
        self.daysPanel.Controls.Add(self.cbWednesday)
        self.daysPanel.Controls.Add(self.cbThursday)
        self.daysPanel.Controls.Add(self.cbFriday)

        # event time label
        self.lblEventTime = Label()
        self.lblEventTime.Text = "Time"
        self.lblEventTime.Location = Point(25, 390)
        self.lblEventTime.Size = Size(100, 20)
        self.lblEventTime.Font = textFont

        # event time combobox
        self.cbxEventTime = ComboBox()
        self.cbxEventTime.DropDownStyle = ComboBoxStyle.DropDownList;
        self.cbxEventTime.Location = Point(220, 390)
        self.cbxEventTime.Size = Size(280, 20);
        self.cbxEventTime.Font = textFont
        self.cbxEventTime.BackColor = Color.White
        self.cbxEventTime.Items.Add('Any')
        self.cbxEventTime.Items.Add('Morning')
        self.cbxEventTime.Items.Add('Afternoon')

        # event add button
        self.btnAddEvent = Button()
        self.btnAddEvent.Text = 'Add Event'
        self.btnAddEvent.Location = Point(75, 475)
        self.btnAddEvent.Size = Size(200, 60)
        self.btnAddEvent.Font = buttonFont
        self.btnAddEvent.BackColor = Color.FromArgb(0, 99, 160)
        self.btnAddEvent.Click += self.btnAddPress
        
        # event clear button
        self.btnClearEvent = Button()
        self.btnClearEvent.Text = 'Clear'
        self.btnClearEvent.Location = Point(325, 475)
        self.btnClearEvent.Size = Size(200, 60)
        self.btnClearEvent.Font = buttonFont
        self.btnClearEvent.BackColor = Color.FromArgb(0, 99, 160)
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
        self.inputPanel.Controls.Add(self.lblEditingMode)

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
        self.lblEditingMode.Text = 'Adding new event'
        self.inputMode = 'add'
        self.editingIndex = -1
        self.clearInputControls()
        
    def btnEditPress(self, sender, args):
        if (self.lbxEvents.SelectedIndex != -1):
            self.btnAddEvent.Text = 'Update Event'
            self.lblEditingMode.Text = 'Editing existing event'
            self.inputMode = 'edit'
            self.editingIndex = self.lbxEvents.SelectedIndex
            self.displaySelectedEvent(self.lbxEvents.SelectedIndex)
        else:
            print('nothing selected')

    def btnExitPress(self, sender, args):
        self.conn.close()
        self.callerForm.scheduler.setEvents(self.events)
        self.callerForm.Show()
        self.Close()

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
            newEventRecord = EventSlot(name, self.generateEventCode(), days, time)
            if (self.inputMode == 'add'):
                #newEvent = Event(name, self.generateEventCode(), days, time)
                self.events.append(newEventRecord)
                #self.addEventToDB(newEvent)
            elif (self.inputMode == 'edit' and self.editingIndex != -1):
                #editEvent = Event(name, self.generateEventCode(), days, time)
                self.events[self.editingIndex] = newEventRecord
                #self.editEventDBEntry(editEvent)
            
            self.addEventToDB(newEventRecord)
            self.displayEvents()
        else:
            print(invalidReason)

    def generateEventCode(self):
        index = 1
        prefix = 'et'

        sql = "SELECT code FROM ScheduleEvents"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()

        free = False
        while free == False:
            found = False
            #for event in self.events:
            #    if (prefix + str(index) == event.code):
            #        found = True
            for row in results:
                if (prefix + str(index) == row[0]):
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

    def addEventToDB(self, newEvent):
        sql = """
                INSERT INTO ScheduleEvents
                VALUES ('""" + str(newEvent.code) + "','" + str(newEvent.name) + "','" + str(newEvent.printDays()) + "','" + str(newEvent.time) + "')"
              
        self.cursor.execute(sql)
        self.conn.commit()


#Application.EnableVisualStyles()
#Application.SetCompatibleTextRenderingDefault(False)

#form = EventManagementForm()
#Application.Run(form)