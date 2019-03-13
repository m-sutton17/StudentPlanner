import clr
from System import Array
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

from System.Drawing import *
from System.Windows.Forms import *


class TimetableInputForm(Form):
    def __init__(self):
        self.Text = 'Timetable Input'
        self.Name = 'frmTimetableInput'

        self.columns = 8
        self.rows = 5
        self.timetableArray = Array.CreateInstance(str, self.rows, self.columns)

        self.initialiseControls()

        self.setUpGrid()


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
        self.lblTitle.Text = "Timetable Input"
        self.lblTitle.Location = Point(10, 15)
        self.lblTitle.Size = Size(1280, 20)

        # timetable data grid
        self.grdTimetable = DataGridView();
        self.grdTimetable.Location = Point(10, 45);
        self.grdTimetable.Name = "grdTimetable";
        self.grdTimetable.Size = Size(900, 600);
        self.grdTimetable.MultiSelect = True;
        self.grdTimetable.ReadOnly = True;

        # timetable combo box
        self.cbxTimetables = ComboBox()
        self.cbxTimetables.DropDownStyle = ComboBoxStyle.DropDownList;
        self.cbxTimetables.Location = Point(950, 50)
        self.cbxTimetables.Size = Size(280, 50);

        # timetable name label
        self.lblTTName = Label()
        self.lblTTName.Text = "Name"
        self.lblTTName.Location = Point(950, 85)
        self.lblTTName.Size = Size(100, 20)

        # timetable name text box
        self.tbxTTName = TextBox()
        self.tbxTTName.Location = Point(1050, 85)
        self.tbxTTName.Size = Size(200, 20)

        # add timetable button
        self.btnAddTimetable = Button()
        self.btnAddTimetable.Text = 'Add TimeTable'
        self.btnAddTimetable.Location = Point(1000, 120)

        # back button
        self.btnBack = Button()
        self.btnBack.Text = 'Return'
        self.btnBack.Location = Point(550, 660)
        self.btnBack.Click += self.exitButtonPressed

        # add controls
        self.mainPanel.Controls.Add(self.lblTitle)
        self.mainPanel.Controls.Add(self.grdTimetable)
        self.mainPanel.Controls.Add(self.cbxTimetables)
        self.mainPanel.Controls.Add(self.lblTTName)
        self.mainPanel.Controls.Add(self.tbxTTName)
        self.mainPanel.Controls.Add(self.btnAddTimetable)
        self.mainPanel.Controls.Add(self.btnBack)

        ## input controls
        self.inputPanel = Panel()
        self.inputPanel.ForeColor = Color.Blue
        self.inputPanel.BackColor = Color.Gray
        self.inputPanel.Location = Point(930, 327)
        self.inputPanel.Size = Size(300, 300)

        # class name label
        self.lblClassName = Label()
        self.lblClassName.Text = "Name"
        self.lblClassName.Location = Point(10, 10)
        self.lblClassName.Size = Size(100, 20)

        # class name textbox
        self.tbxClassName = TextBox()
        self.tbxClassName.Location = Point(50, 10)
        self.tbxClassName.Size = Size(150, 20);

        # class room label
        self.lblClassRoom = Label()
        self.lblClassRoom.Text = "Room"
        self.lblClassRoom.Location = Point(10, 50)
        self.lblClassRoom.Size = Size(100, 20)
        
        # class room textbox
        self.tbxClassRoom = TextBox()
        self.tbxClassRoom.Location = Point(50, 50)
        self.tbxClassRoom.Size = Size(150, 20);

        # class teacher label
        self.lblClassTeacher = Label()
        self.lblClassTeacher.Text = "Teacher/Lecturer"
        self.lblClassTeacher.Location = Point(10, 90)
        self.lblClassTeacher.Size = Size(100, 20)
        
        # class teacher textbox
        self.tbxClassTeacher = TextBox()
        self.tbxClassTeacher.Location = Point(50, 90)
        self.tbxClassTeacher.Size = Size(150, 20);

        # add lessons button
        self.btnAddLessons = Button()
        self.btnAddLessons.Text = "Add classes to selected slots"
        self.btnAddLessons.Location = Point(25, 130)
        self.btnAddLessons.Size = Size(200, 20)
        self.btnAddLessons.Click += self.addLessonsPressed

        # add controls
        self.inputPanel.Controls.Add(self.lblClassName)
        self.inputPanel.Controls.Add(self.tbxClassName)
        self.inputPanel.Controls.Add(self.lblClassRoom)
        self.inputPanel.Controls.Add(self.tbxClassRoom)
        self.inputPanel.Controls.Add(self.lblClassTeacher)
        self.inputPanel.Controls.Add(self.tbxClassTeacher)
        self.inputPanel.Controls.Add(self.btnAddLessons)

        self.mainPanel.Controls.Add(self.inputPanel)

        self.Controls.Add(self.mainPanel)

    def setUpGrid(self):

        self.grdTimetable.Columns.Clear()
        for i in range(self.columns):
             self.grdTimetable.Columns.Add("" ,"%s - %s" % (i+9, i+10))   # (i+9) + " - " + (i+10)

        row = Array.CreateInstance(str, self.columns)
        rowNames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        for x in range(self.rows):
            for y in range(self.columns):
                row[y] = ''

            self.grdTimetable.Rows.Add(row)
            self.grdTimetable.Rows[x].HeaderCell.Value = rowNames[x]

        

    def updateGrid(self):
        self.grdTimetable.Rows.Clear()

        row = Array.CreateInstance(str, self.columns)
        rowNames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        for x in range(self.rows):
            for y in range(self.columns):
                row[y] = self.timetableArray[x,y]

            self.grdTimetable.Rows.Add(row)
            self.grdTimetable.Rows[x].HeaderCell.Value = rowNames[x]
        pass

    def displaySavedTimetable(self):
        pass

# button events
    def addLessonsPressed(self, sender, args):
        for cell in self.grdTimetable.SelectedCells:
            print('x: ' + str(cell.RowIndex) + ' y: ' + str(cell.ColumnIndex))
            #cell.value = tbxClassName.Text
            self.timetableArray[cell.RowIndex, cell.ColumnIndex] = self.tbxClassName.Text

        self.updateGrid()

    def exitButtonPressed(self, sender, args):
        form.Show()
        self.Close()


#class DGVMultiSelect (DataGridView):
#     def __init__(self):
#         pass


#     def OnCellMouseDown(self, DataGridViewCellMouseEventArgs e):


Application.EnableVisualStyles()
Application.SetCompatibleTextRenderingDefault(False)

form = TimetableInputForm()
Application.Run(form)