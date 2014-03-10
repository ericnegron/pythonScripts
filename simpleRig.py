import maya.cmds as mc
import math

#This script creates a GUI that allows the user to create a basic bipedal skeleton and then scale it uniformly.
#It also allows the user to scale individual parts of the skeleton.  



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
    


# This portion of the script allows the user to create a basic bipedal skeleton using the base window class from above.

#  Establishes the new window class based on the base GUI window class.
class EN_ModuleElevenWindow(EN_BaseUIWindow):
    # Initializes the new window values
    def __init__(self):
        EN_BaseUIWindow.__init__(self)
        # Overrides the base window class window name
        self.title = "Module Eleven Window"
        # Overrides the base window class window size
        self.size = (300, 350)
        # Initializes the action buttons to make sure that the "Create and Close" button closes after executing the command.
        self.actionName = "Create and Close"
    #  Creates the layout within the base gui.
    def displayOptions(self):
        # Creates a column layout within the established base GUI.
        mc.columnLayout()
        # Creates the neck length slider group.
        self.neck = mc.floatSliderGrp(label= "Neck Length", field = True, minValue = 1, value = 1)
        # Creates the torso length slider group.
        self.torso = mc.floatSliderGrp(label = "Torso Length", field = True, minValue = 1, value = 1)
        # Creates the shoulder width slider group.
        self.shoulder = mc.floatSliderGrp(label = "Shoulder Width", field = True, minValue = 1, value = 1)
        # Creates the arm length slider group.
        self.arms = mc.floatSliderGrp(label = "Upper Arm Length", field = True, minValue = 1, value = 1)
        # Creates the forearm length slider group.
        self.armFor = mc.floatSliderGrp(label = "Forearm Length", field = True, minValue = 1, value = 1)
        # Creates the hip width slider group.
        self.hips = mc.floatSliderGrp(label = "Hip Width", field = True, minValue = 1, value = 1)
        # Creates the thigh length slider group.
        self.legs = mc.floatSliderGrp(label = "Leg Length", field = True, minValue = 1, value = 1)
        # Creates the shin length slider group.
        self.legShin = mc.floatSliderGrp(label = "Shin Length", field = True, minValue = 1, value = 1)
        # Creates a foot slider group.
        self.foot = mc.floatSliderGrp(label = "Foot Size", field = True, minValue = 1, value = 1)
        # Creates the overall scale slider group.
        self.scale = mc.floatSliderGrp(label = "Overall Sekeleton Size", field = True, minValue = 1, value = 1)
        
    # This is the function that the create button will execute when clicked.  
    def createBtnCmd(self, *args):
        # Creates a neckLength variable that pulls the user input from the neck length slider group.
        neckLength = mc.floatSliderGrp(self.neck, q = True, value = True)
        # Creates a torsoLength variable that pulls the user input from the torso slider.
        torsoLength = mc.floatSliderGrp(self.torso, q = True, value = True)
        # Creats a variable for the shoulder width that pulls the user input from the shoulder slider.
        shoulderWidth = mc.floatSliderGrp(self.shoulder, q = True, value = True)
        # Creates a variable for the hip width using user input from hip slider.
        hipWidth = mc.floatSliderGrp(self.hips, q = True, value = True)
        # Creats a varaible for the  arm length using user input from the arms slider.
        armLength = mc.floatSliderGrp(self.arms, q = True, value = True)
        # Creats a varaible for the  forearm length using user input from the arms slider.
        foreArmLength = mc.floatSliderGrp(self.armFor, q = True, value = True)
        # Creates a variable for the leg length using user input from the leg slider.
        legLength = mc.floatSliderGrp(self.legs, q = True, value = True)
        # Creates a variable for the shin length using user input from the leg slider.
        shinLength = mc.floatSliderGrp(self.legShin, q = True, value = True)
        # Creates a variable for the foot length.
        footSize = mc.floatSliderGrp(self.foot, q = True, value = True)
        # Creates a variable for the overall scale of the sekeleton using the scale slider.
        overallSize = mc.floatSliderGrp(self.scale, q = True, value = True)
        
        
        # This part creates the skeleton.
        # Creates the center hip joint
        hip = mc.joint()
        # Creates the chest joint and positions it using the torsoLength input.
        chest = mc.joint(position = (0,torsoLength,0))
        # Creates the neck joint using the neckLength input to position it.
        mc.joint(position = (0,(neckLength+torsoLength),0))
        # Creates the head joint two units above the neck joint.
        mc.joint(position = (0,(neckLength+2)+torsoLength,0))
        # Selects the chest joint.
        mc.select(chest)
        # Creates the right shoulder using the inverse of the shoulder width input.  Sets it equal to the chest height minus 1.
        mc.joint(position=(-shoulderWidth, torsoLength-1, 0))
        # Creates the right upper arm
        mc.joint(position = (-shoulderWidth - 1, -armLength, 0))
        # Creates the right forearm via the wrist as a viarable.
        mc.joint(position = (-shoulderWidth -1, (-armLength +-foreArmLength), 0))
        # Creates the right hand.
        mc.joint(relative=True, position = (0,-2,0))
        # Selects the chest joint.
        mc.select(chest)
        # Creates the left shoulder joint.
        mc.joint(position=(shoulderWidth, torsoLength-1, 0))
        # Creates the left upper arm.
        mc.joint(position = (shoulderWidth + 1, -armLength, 0))
        # Creates the left forearm.
        mc.joint(position = (shoulderWidth + 1, (-armLength +-foreArmLength), 0))
        # Creates the left hand.
        mc.joint(relative=True, position = (0,-2,0))
        # Creates the right hip joint.
        mc.select(hip)
        mc.joint(position = (-hipWidth, -2, 0))
        # Creates the right thigh.
        mc.joint(position = (-hipWidth, -legLength, 0))
        # Creates the right shin.
        mc.joint(position = (-hipWidth, (-legLength +- shinLength), 0))
        # Creates the right heel.
        mc.joint(relative=True, position=(0, -2, 0))
        # Creates the right foot.
        mc.joint(relative=True, position=(-footSize, -1, 0))
        # Creates the left hip joint.
        mc.select(hip)
        mc.joint(position = (hipWidth, -2, 0))
        # Creates the left thigh.
        mc.joint(position = (hipWidth, -legLength, 0))
        # Creates the left shin.
        mc.joint(position = (hipWidth, (-legLength +- shinLength), 0))
        # Creates the left heel.
        mc.joint(relative=True, position=(0, -2, 0))
        # Creates the left foot.
        mc.joint(relative=True, position=(footSize, -1, 0))
        
        # Scales the overall size of the skeleton based on user input.
        # Selects all of the joints.
        mc.select(all=True)
        # Groups the joints into one group
        mc.group(absolute=True)
        # Scales the group based on user input.
        mc.scale(overallSize, overallSize, overallSize)
        
       
        
        
#  Calls the GUI.
EN_ModuleElevenWindow.showUI()
