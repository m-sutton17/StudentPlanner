import clr
from System import Array
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

from System.Drawing import *
from System.Windows.Forms import *

class MainMenuForm(Form):
    #initialisation
    def __init__(self):
        self.Text = 'Main Menu'
        self.Name = 'frmMainMenu'
        
        self.initialiseControls()


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
        self.btnSchedule.Location = Point(150, 200)

        # timetable form button
        self.btnTimetable = Button()
        self.btnTimetable.Text = 'Timetable Input'
        self.btnTimetable.Location = Point(150, 350)

        # view schedule form button
        self.btnViewSchedule = Button()
        self.btnViewSchedule.Text = 'View Schedule'
        self.btnViewSchedule.Location = Point(150, 500)

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

        pass


Application.EnableVisualStyles()
Application.SetCompatibleTextRenderingDefault(False)

form = MainMenuForm()
Application.Run(form)
