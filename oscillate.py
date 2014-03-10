import maya.cmds as mc
import math

# This script allows the user to create a polygon primitive and then specify how the object will oscillate.



# Creates the custom window class called EN_BaseUIWindow.
class EN_BaseUIWindow(object):
    @classmethod
    def showUI(cls):
        win=cls()
        win.create()
        return win
    # Initializes the handle, title, and size attributes for the window class.  
    def __init__(self):
        self.window = "en_baseuiwindow"
        self.title = "Base GUI Window"
        self.size = (600, 400)
        self.supportsToolAction = False
        self.actionName = "Create and Close"
    # Function to draw the window
    def create(self):
        # Checks to see if this window has already been created.  If it has, it deletes the window.
        if mc.window(self.window, exists=True):
            mc.deleteUI(self.window, window=True)
        # Creates the window using the already initialized attributes as well as the menuBar attribute from below.
        self.window = mc.window(self.window, title=self.title, wh=self.size, menuBar = True)
        # Establishes themain layout of the GUI.
        self.mainForm = mc.formLayout(numberOfDivisions=100)
        # Calls the cmmonMenu function created below.  
        self.commonMenu()
        # Calls the button creation function that is created below.
        self.commonButtons()
        # Creates a central pane in the display.
        self.optionsBorder = mc.tabLayout(scrollable=True, tabsVisible = False, height = 1)
        # Nests the pane within the main form layout.
        mc.formLayout(self.mainForm, e=True, attachForm = (
            # Pins the top edge to the top of the UI with a padding of 0 pixels.
            [self.optionsBorder, 'top', 0], 
            # Pins the left edge of pane to the left of the UI with a padding of 2 pixels.
            [self.optionsBorder, 'left', 2],
            # Pins the right edge of the pane to the right of the UI with a padding of 2 pixels.
            [self.optionsBorder, 'right', 2]),
            # Pins the bottom edge of the pane to the top edge of the buttons.
            attachControl = ([self.optionsBorder, 'bottom', 5, self.createBtn]))
        # Allows the panel to scale with the main UI.
        self.optionsForm = mc.formLayout(numberOfDivisions=100)
        # Calls the display option function from below.  
        self.displayOptions()
        # Shows (displays) the window.
        mc.showWindow()
    
    # Adds menu items to the window.
    def commonMenu(self):
        # Creates a drop down menu labeled "Edit".
        self.editMenu = mc.menu(label="Edit")
        # Creates the option to either save settings or reset the settings.  This is in the drop down menu "Edit".
        self.editMenuSave = mc.menuItem(label = "Save Settings")
        self.editMenuReset = mc.menuItem(label = "Reset Settings")
        # Creates another drop down menu for the user to get help.  Labels it "Help".
        self.helpMenu = mc.menu(label = "Help")
        # Creates an option to get help on the menu/script.  
        self.helpMenuItem = mc.menuItem(label = "Help on %s" %self.title)

    # Function for the creation of the command buttons.
    def commonButtons(self):
        # Creates a button size parameter with a padding of 18 pixels.  The width is the size of the UI width minus the padding
        # divided by three.  The height is 26 pixels.  
        self.commonBtnSize = ((self.size[0]-18)/3, 26)
        # Establishes the layout of the buttons.  Sets them into a row, with three buttons in the row.  Also establishes their size.
        
        # Creates the "create and close" button.
        self.actionBtn = mc.button(label = self.actionName, height = self.commonBtnSize[1], command = self.actionBtnCmd)
        # Creates the "create" button.
        self.createBtn = mc.button(label = "Create", height = self.commonBtnSize[1], command = self.createBtnCmd)
        # Creates the "close" button.
        self.closeBtn = mc.button(label = "Close", height = self.commonBtnSize[1], command = self.closeBtnCmd)
        # Dictates how the buttons scale when the user scales the UI.  
            # First sets the main form to edit mode.
        mc.formLayout(self.mainForm, e=True, attachForm=(
            # Then takes each button, specifies the edge to adjust, and then specifies the value to adjust by.
            # Pins the action button to the left of the UI with a padding of 5 pixels.
            [self.actionBtn, 'left', 5],
            # Pins the action button to the bottom of the UI with a padding of 5 pixels.
            [self.actionBtn, 'bottom', 5],
            # Pins the create button to the bottom of the UI with a padding of 5 pixels.
            [self.createBtn, 'bottom', 5],
            # Pins the close botton to the bottom of the UI with a padding of 5 pixels.
            [self.closeBtn, 'bottom', 5],
            # Pins the close button to the right of the UI with a padding of 5 pixels. 
            [self.closeBtn, 'right', 5]),
            # Pins buttons relative to the coordinates specified in the create(self) function according to the
            # numberOfDivisions flag in the mainForm command.
            attachPosition = ([self.actionBtn, 'right', 1, 33], [self.closeBtn, 'left', 0, 67]),
            # Pins the middle button to the outer two buttons.  Allows it to scale along with the other two buttons.
            attachControl = ([self.createBtn, 'left', 4, self.actionBtn], [self.createBtn, 'right', 4, self.closeBtn]),
            # Makes sure that the the top edges of the buttons scale according to the above parameters.  
            attachNone = ([self.actionBtn, 'top'], [self.createBtn, 'top'], [self.closeBtn, 'top']))
        
    # Function for the help menu goes here.  This will load a help text file explaining the options of the GUI.  
    
    # Place holder commands for the menu items
    def editMenuSaveCmd(self, *args): 
        pass
    def editMenuResetCmd(self, *args): 
        pass

    # Creates function for the create and close button.  When user clicks button, action happens and UI closes.
    def actionBtnCmd(self, *args):
        self.createBtnCmd()
        self.closeBtnCmd()
    # Creates a function for the create button.  When user clicks button, UI creates something.
    def createBtnCmd(self, *args):
        pass
    # Creates a function for the close button.  When user clicks button, UI closes.
    def closeBtnCmd(self, *args):
        mc.deleteUI(self.window, window=True)
    # Creates a display options function.  This is a placeholder
    def displayOptions(self):
        pass
    


# This portion of the script allows the user to create a geometric primitive and then specify how it wants it to move.
# It follows the module example expression but adds the ability to choose your object.  It also changes the sin function to a cos function.

#  Establishes the new window class based on the base GUI window class.
class EN_ModuleThirteenWindow(EN_BaseUIWindow):
    # Initializes the new window values
    def __init__(self):
        EN_BaseUIWindow.__init__(self)
        # Overrides the base window class window name
        self.title = "Module Thirteen Window"
        # Overrides the base window class window size
        self.size = (300, 350)
        # Initializes the action buttons to make sure that the "Create and Close" button closes after executing the command.
        self.actionName = "Create and Close"
    #  Creates the layout within the base gui.
    def displayOptions(self):
        # Creates a column layout within the established base GUI.
        mc.columnLayout()
        # Creates a label for the radio button group.
        self.labelZero=mc.text(label="Select the Object to Create")
        # Creates the radio button group.
        self.objType=mc.radioButtonGrp(labelArray4=['Cube', 'Cone', 'Cylinder', 'Sphere'], numberOfRadioButtons=4, select=1)
        # Creates a label for the text field.
        self.labelOne=mc.text(label="Name of Attribute to Effect")
        # Creates the attribute field.
        self.attribute = mc.textField(width=150)
        # Creates a label for the Max value field.
        self.labelTwo=mc.text(label="Maximum Value")
        # Creates the maximum value field.
        self.max = mc.floatField(minValue = 0)
        # Creates a label for the min value field.
        self.labelThree=mc.text(label="Minimum Value")
        # Creates the minimum value field.
        self.min = mc.floatField(minValue = 0)
        # Creates a label for the time field.
        self.labelFour=mc.text(label="Number of seconds per cycle")
        # Creates the time field.
        self.time = mc.floatField(minValue = 0.001, value = 1)
        # Creates a label for the type of oscillation.
        self.labelFive=mc.text(label="Type of Oscillation")
        # Creates a radio button group that allows the user to specify the type of oscillation the object will do.
        self.oscillate=mc.radioButtonGrp(labelArray2=['sin', 'cos'], numberOfRadioButtons=2, select=1)
        # Creates a new column layout for the notes.  Makes it collapsable and gives it a label of "Notes".
        self.xformGrp = mc.frameLayout(label="Notes", collapsable=True)
        # Creates the notes text field.
        self.notes=mc.scrollField(wordWrap=True,text="To use this tool:\n" + 
                                "First select the type of object you wish to create.\n" + 
                                "Next, enter the attribute you wish to be effected.\n" +
                                "Third, enter the values for the maximum and minimum values you wish to effect as well as the number of seconds per oscillation.\n" +
                                "Finally, select whether you want the object to oscillate using a sin or cos function.",
                                edit = False, ed= False, width = 400, height = 200)
                               
       
        
        
    # This is the function that the create button will execute when clicked.  
    def createBtnCmd(self, *args):
        # Creates a function for the radio button group.
        self.objIndAsCmd = {1:mc.polyCube, 2:mc.polyCone, 3:mc.polyCylinder, 4:mc.polySphere}
        # Creates the object variable for the create function.
        objIndex = mc.radioButtonGrp(self.objType, query = True, select = True)
        # Creates a variable for the new object to be created based on the above array and objIndex variable.
        newObject = self.objIndAsCmd[objIndex]()
       
        # Following section creates necessary variables for the expression.
        # Creates a variable to select the previously created object.
        sel = mc.ls(sl=True)
        # Creates the attribute variable using the user input from the GUI.
        att = mc.textField(self.attribute, query = True, text = True)
        # Creates the minimum value variable using the user input from the GUI.
        minimum = mc.floatField(self.min, query = True, value = True)
        # Creates the maximum value variable using the user input from the GUI.
        maximum = mc.floatField(self.max, query = True, value = True)
        # Creates the time period variable using the user input from the GUI.
        period = mc.floatField(self.time, query = True, value = True)
        # Creates the variable for the type of oscillation radio group.
        oscType = mc.radioButtonGrp(self.oscillate, query = True, select = True)
        # Creates the speed variable for which the created object will travel at.
        speed = 6.28/period
        # Creates the random variable.  It is created as 'ran' because random is a pre-defined function in python.
        ran = (maximum - minimum)/2.0
        # Creates the start variable.
        start = minimum + ran
        
       
        # Creates the expression that will drive the script.
        # objectName.attributeName = sin(time*speed) * range + start.
        # Creates the expression for the cos oscillation.
        expressionTextCos = (sel[0] + "." + str(att)
                          + " = cos(time * " + str(speed)
                          + " ) * " + str(ran) + " + "
                          + str(start) + ";")
        
        # Creates the expression for sin
        expressionTextSin = (sel[0] + "." + str(att)
                          + " = sin(time * " + str(speed)
                          + " ) * " + str(ran) + " + "
                          + str(start) + ";")
        # Calls the expression.
        if oscType == 1:
            mc.expression(string=expressionTextSin)
            print "ExpressionSin has sucessfully run."
        elif oscType == 2:
            mc.expression(string=expressionTextCos)
            print "ExpressionCos has successfully run."
        else:
            print "Expression didn't properly execute."

        
        
#  Calls the GUI.
EN_ModuleThirteenWindow.showUI()
