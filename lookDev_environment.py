import maya.cmds as mc
import maya.mel as mel
import math

'''
This tool allows the user to create a basic look development set-up.
It allows the user to specifiy whether they want to include three-point lighting,
as well as whether they want to include image based lighting, a new render camera, and a backdrop.
Once lighting options are chosen, the user can then adjust basic parameters using the GUI.

'''

# Create the GUI.
def lookDevWindow():
    # Check for existing window and delete if it exists.
    if mc.window("lookDev_win", ex=True):
        mc.deleteUI("lookDev_win", window=True)
    
    # Creates the main window.
    mc.window("lookDev_win", title="Look Development Environment Creator", w=100, s=False)
    # Establishes a column layout for the window.
    mc.columnLayout("c_layout", adj=True)
    # Creates a heading using the separator command along with text.
    mc.separator()
    mc.text("SELECT YOUR BASIC SETTINGS")
    mc.separator()
    # Creates the options for the environment.  Allows the user to choose what objects to include in the environment.
    mc.checkBox("threeLight", label="Create Three-Point Lighting")
    mc.checkBox("hdrLight", label="Create Image Based Lighting")
    mc.checkBox("camCreate", label="Create New Render Camera")
    mc.checkBox("bdCreate", label="Create Backdrop")
    # Allows the user to browse to their desired location to import an HDR file to use with the IBL.
    mc.textFieldButtonGrp("getFile", label='HDRI file',text="", buttonLabel='Browse', buttonCommand="browseBtnCmd()")
    # Compartmentalizes the create button using a separator.  Mostly just for keeping the UI organized.
    mc.separator(style="in")
    # The create button that creates the LookDev environment using the createLookDev() function.
    mc.button(label="Create LookDev Environment", command="createLookDev()", p="c_layout")
    mc.separator(style="in")
    # Another heading using separators with text.
    mc.separator()
    mc.text("ADJUST ENVIRONMENT")
    mc.separator()
    # A section of the UI where the user can adjust the environment with the lights in it.  This is interactive.
    mc.floatSliderGrp("sceneScale", label="Scene Scale", field=True, minValue=0, value = 1, dc="adjustEnvironmentScale()")
    mc.floatSliderGrp("lightAngle", label="Light Angle", field=True, minValue=-10, maxValue=10, value = 0, dc="adjustEnvironmentAngle()")
    mc.floatSliderGrp("position", label="Light Position", field=True, minValue=-360, maxValue=360, value = 0, dc="adjustEnvironmentPosition()")
    # Heading number 3.
    mc.separator()
    mc.text("ADJUST LIGHT SETTINGS")
    mc.separator()
    # Attribute adjustments for the main three-point lighting.  Requires the user to have selected this to be included in the scene.
    # Adjustments for the Key Light.
    mc.text("Key Light")
    mc.floatSliderGrp("keyOne", label="Intensity", min=0, field=True, dc="adjustLookDevLightsIntensity()", cw3=(98, 75, 1))
    mc.checkBox("keyShad", label="Turn On Shadows", onc="adjustLookDevLightsKeyShadows()", ofc="adjustLookDevLightsKeyShadows()")
    mc.checkBox("keyDiff", label="Emit Diffuse", onc="adjustLookDevLightsKeyDiffuse()", ofc="adjustLookDevLightsKeyDiffuse()")
    mc.checkBox("keySpec", label="Emit Specular", onc="adjustLookDevLightsKeySpec()", ofc="adjustLookDevLightsKeySpec()")
    # Adjustments for the Rim Light.
    mc.text("Rim Light")
    mc.floatSliderGrp("rimOne", label="Intensity", min=0, field=True, dc="adjustLookDevLightsIntensity()", cw3=(98, 75, 1))
    mc.checkBox("rimShad", label="Turn On Shadows", onc="adjustLookDevLightsRimShadows()", ofc="adjustLookDevLightsRimShadows()")
    mc.checkBox("rimDiff", label="Emit Diffuse", onc="adjustLookDevLightsRimDiffuse()", ofc="adjustLookDevLightsRimDiffuse()")
    mc.checkBox("rimSpec", label="Emit Specular", onc="adjustLookDevLightsRimSpec()", ofc="adjustLookDevLightsRimSpec()")
    # Adjustments for the Fill Light.
    mc.text("Fill Light")
    mc.floatSliderGrp("fillOne", label="Intensity", min=0, field=True, dc="adjustLookDevLightsIntensity()", cw3=(98, 75, 1))
    mc.checkBox("fillShad", label="Turn On Shadows", onc="adjustLookDevLightsFillShadows()", ofc="adjustLookDevLightsFillShadows()")
    mc.checkBox("fillDiff", label="Emit Diffuse", onc="adjustLookDevLightsFillDiffuse()", ofc="adjustLookDevLightsFillDiffuse()")
    mc.checkBox("fillSpec", label="Emit Specular", onc="adjustLookDevLightsFillSpec()", ofc="adjustLookDevLightsFillSpec()")
    
    # Header for the tool help section.
    mc.separator()
    mc.text("TOOL HELP")
    mc.separator()
    # Frame layout that collapses to show or hide the tool help.
    mc.frameLayout(label="Help", collapsable=True)
    mc.scrollField(wordWrap=True,text="To use this tool:\n" + 
                                "1. Make sure Mental Ray is loaded via the Plug-In manager.\n" + 
                                "2. Select which types of lights you want created.\n" +
                                "3. If creating IBL, browse to your desired HDR image.\n" +
                                "4. Click create button to create set-up.\n" +
                                "5. Once environment has been created, use additional options to adjust set-up to suit your needs.\n\n\n" +
                                "Additional Notes: \n\n" +
                                "- If Reset UI button after Look-Dev scene has been created, tool will not function properly.\n" +
                                "- Only reset the UI if Look-Dev scene has not yet been created.\n" +
                                "- All lights will have initial intensities set to 0 with exception of IBL.\n" +
                                "- Make sure there are no groups with the name ThreePointLighting in the scene prior to creating 3-point lighting 				with the tool.\n" +
                                "- Once Look-Dev environment is created, lighting and rendering options can be adjusted like normal.\n" +
                                "- Render globals will still need to be set as per usual.",
                                edit = False, ed= False, width = 400, height = 200)
    # Separates the close button from the rest of the GUI.
    mc.separator()
    # Button for reseting the GUI.
    mc.button(label="Reset Tool", command="resetUI()", p="c_layout")
    # Closes the GUI.
    mc.button(label="Close Tool", command="closeUI()", p="c_layout")

    # Shows the GUI.
    mc.showWindow()
# This function allows the user to browse to their desired file location to load an HDR image.  It then displays the file path in the text field of the GUI.
def browseBtnCmd():
    # The code in this function has been adapted from "Maya Python for Games and Film" by Adam Mechtley and Ryan Trowbridge.
    # The original code can be found on page 230.
    # Creates an empty variable named filePath
    filePath = ""
    # Tells Maya to fill the filePath variable with the file information from the user.
    try: 
    # Creates the file browser dialog.
        filePath = mc.fileDialog2(ff=self.fileFilter, fileMode=1)
    except: 
    # Creates an alternate browser dialog for older versions of Maya.
        filePath = mc.fileDialog(dm="*.hdr", mode=0)
    #display file path
    try: mc.textFieldButtonGrp("getFile", edit=True, text=(filePath))
    except: pass
# Creates the environment.  Once created, allows the user to adjust settings and attributes.  This is the main chunk of the script.
def createLookDev():
    # Create variables for the checkboxes to pull data from user input.
    threePoint = mc.checkBox("threeLight", query=True, value=True)
    ibl = mc.checkBox("hdrLight", query=True, value=True)
    cam = mc.checkBox("camCreate", query=True, value=True)
    backDrop = mc.checkBox("bdCreate", query=True, value=True)

    # The code for checking for the loading of mentalRay was adapted from "Creating Maya GUI for asset lighting" by Alex Khan on Creative Crash.
    # http://www.creativecrash.com/maya/tutorials/development-api/c/creating-maya-gui-for-asset-lighting
    # Check for mentalRay being loaded.
    if mc.pluginInfo("Mayatomr", query=True, loaded=True) != 1 :
        mc.loadPlugin( "Mayatomr" )
    if not mc.objExists('mentalrayGlobals'):
        mc.mel.eval("miCreateDefaultNodes")
        
    # Use those variables to create the look dev scene.
    # Create three point lighting set up.
    # Checks to see whether or not the user has selected the Three-point lighting option in the GUI.
    if threePoint == True:
        # Create Key Light.  Set basic attributes to zero.
        mc.directionalLight(name="KeyLight")
        mc.setAttr("KeyLight.intensity",0)
        mc.setAttr("KeyLightShape.useRayTraceShadows", 0)
        mc.setAttr("KeyLightShape.emitDiffuse", 0)
        mc.setAttr("KeyLightShape.emitSpecular", 0)
        # Position Key Light
        mc.move(10, 10, 12)
        mc.rotate(-32.641, 39.888, 0)
        # Place Key Light center of illumination at the origin.
        mc.setAttr("KeyLight.centerOfIllumination", 18.57)
        # Center rotation and scale points at the origin.
        mc.select("KeyLight.rotatePivot")
        mc.move(0,0,0)
        mc.select("KeyLight.scalePivot")
        mc.move(0,0,0)
        # Create Rim Light.  Set basic attributes to zero.
        mc.directionalLight(name="RimLight")
        mc.setAttr("RimLight.intensity",0)
        mc.setAttr("RimLightShape.useRayTraceShadows", 0)
        mc.setAttr("RimLightShape.emitDiffuse", 0)
        mc.setAttr("RimLightShape.emitSpecular", 0)
        # Position Rim Light
        mc.move(10, 9, -9)
        mc.rotate(146.219, 48.013, -180)
        # Place Rim Light illumination center at the origin.
        mc.setAttr("RimLight.centerOfIllumination", 16.186)
        # Center rotation and scale points at the origin.
        mc.select("RimLight.rotatePivot")
        mc.move(0,0,0)
        mc.select("RimLight.scalePivot")
        mc.move(0,0,0)
        # Create Fill Light.  Set basic attributes to zero.
        mc.directionalLight(name="FillLight")
        mc.setAttr("FillLight.intensity",0)
        mc.setAttr("FillLightShape.useRayTraceShadows", 0)
        mc.setAttr("FillLightShape.emitDiffuse", 0)
        mc.setAttr("FillLightShape.emitSpecular", 0)
        # Position Fill Light.
        mc.move(-12, 4, 5)
        mc.rotate(-17.103, -67.38, 0)
        # Place Fill Light illumination center at the origin.
        mc.setAttr("FillLight.centerOfIllumination", 13.601)
        # Center rotation and scale points at the origin.
        mc.select("FillLight.rotatePivot")
        mc.move(0,0,0)
        mc.select("FillLight.scalePivot")
        mc.move(0,0,0)
    # If option for creation of three-point lighting is not selected, print statement.
    else:
        print "Three-point lighting not selected"
    # Clear all selections in the scene.
    mc.select(cl=True)
    
    # Create IBL.
    # IBL creation code was adapted from "Creating Maya GUI for asset lighting" by Alex Khan on Creative Crash.
    # Alterations to the original code were made to fix errors and to fit this tool.
    # Original code can be found here: http://www.creativecrash.com/maya/tutorials/development-api/c/creating-maya-gui-for-asset-lighting
    # Checks to see if IBL option was selected.
    if ibl == True:
        # Creates an IBL node.
        mc.createNode("mentalrayIblShape", name="IblEnvironment")
        # Connects the IBL node to the Mental Ray render globals.
        mc.connectAttr("IblEnvironment.message",'mentalrayGlobals.imageBasedLighting',force=True)
        # Sets the IBL to be visible in Final Gather
        mc.setAttr("IblEnvironment.visibleInFinalGather", True)
        # Creates a file node for the HDR image.
        mc.createNode('file', name= 'HdrFile')
        # Connects the file node to a place 2d node.
        mc.createNode('place2dTexture', name='Place2dTxt')
        # Connects the file node to the place2d node.
        mc.connectAttr("HdrFile.uvCoord", "Place2dTxt.coverage")
        # Creates a variable that calls the results of the user input.
        filePath = mc.textFieldButtonGrp("getFile", q=True, text=True)
        # Sets the file nodes texture/image input to the file path from the user.
        mc.setAttr("HdrFile.fileTextureName", filePath, type= "string")
        # Sets the IBL texture/image input to the file node's image attribute.
        mc.setAttr("IblEnvironment.texture", mc.getAttr('HdrFile.fileTextureName'), type="string")
    # If IBL option was not selected, prints statement.
    else:
        print "No IBL selected"
    # Create Render Cam.
    # Checks to see if render camera options was created.
    if cam == True:
        # Creates camera.
        mc.camera(name="Render_Cam", displayResolution=True, dgm=True, horizontalFilmAperture=1.0, verticalFilmAperture=1.0, ff="fill")
        # Positions camera.
        mc.move(0, 5, 20)
    # If render camera option was not selected, prints statement.
    else:
        print "New camera not selected"
    # Create Back Drop.
    # Checks to see if backdrop option was selected.
    if backDrop == True:
        # Creates the backdrop and positions it.
        mc.nurbsPlane(name="BackDrop", v=5, w=15, lr=0.5)
        mc.setAttr("BackDrop.rotateX", 90)
        mc.setAttr("BackDrop.rotateZ", 90)
        mc.setAttr("BackDrop.scaleY", 20)
        mc.setAttr("BackDrop.scaleZ", 5)
        mc.setAttr("BackDrop.translateZ", -10)
        mc.select("BackDrop.cv[0:3][0]")
        mc.xform(relative=True, translation=(45,0,0))
        mc.select("BackDrop.cv[0:3][1]")
        mc.xform(relative=True, translation=(9,-0.25,0))
        mc.select("BackDrop")
        # Freezes backdrop transformations.
        mc.makeIdentity(apply=True)
        # Clears cv selections.
        mc.select(cl=True)
    # If backdrop option was not selected,  prints statement.
    else:
        print "Backdrop Not Selected"
    # Groups the lights if three-point lighting was selected.
    if threePoint == True:
        mc.select("KeyLight", "RimLight", "FillLight")
        mc.group(name="ThreePointLighting")
    # If three-point lighting option was not selected, prints statement.  
    else:
        print "Three-point lighting not selected."
# Creates a function for adjusting the environment scale.   
def adjustEnvironmentScale():
    # Create variables for the user input options.
    threePointScl = mc.checkBox("threeLight", query=True, value=True)
    camAdj = mc.checkBox("camCreate", query=True, value=True)
    backDropAdj = mc.checkBox("bdCreate", query=True, value=True)
    scaleEnv = mc.floatSliderGrp("sceneScale", query=True, value=True)
    
    # Scale the lights.
    # Checks to see if user selected the creation of three-point lighting.
    if threePointScl == True:
        # If selected, creates selects the lights and scales them using the user input.
        mc.select("KeyLight")
        mc.scale(scaleEnv, scaleEnv, scaleEnv)
        mc.select("FillLight")
        mc.scale(scaleEnv, scaleEnv, scaleEnv)
        mc.select("RimLight")
        mc.scale(scaleEnv, scaleEnv, scaleEnv)
    # If not selected, prints statement.
    else:
        print "Three-point lighting was not selected"
    # Clear selections.
    mc.select(cl=True)
    # Scale the backdrop. 
    # Checks to see if user selected the backdrop to be created.
    if backDropAdj == True:
        # If backdrop creation was selected, selects the backdrop and scales it using the user input. 
        mc.select("BackDrop")
        mc.scale(scaleEnv, scaleEnv, scaleEnv)
    # If backdrop creation was not selected, prints statement.
    else:
        print "Backdrop Not Selected"
    # Clear selections.
    mc.select(cl=True)
    # Scale the camera.
    # Checks to see if user selected the creation of a new render camera.
    if camAdj == True:
        # If new render camera was created, selects the camera and scales it using user input.
        mc.select("Render_Cam1")
        mc.scale(scaleEnv, scaleEnv, scaleEnv)
    # If render camera was not selected to be created, prints statement.
    else: 
        print "Render camera was not created"
    # Clear selections.
    mc.select(cl=True)
# Function for adjusting the angle of the lights.   
def adjustEnvironmentAngle():
    # Variables for pulling the user input data.
    threePointAng = mc.checkBox("threeLight", query=True, value=True)
    angle = mc.floatSliderGrp("lightAngle", query=True, value=True)
    # To adjust the angle of the lights.
    # Checks to see if create three-point lighting was selected.
    if threePointAng == True:
        # If selected, rotates the lights using user input.
        mc.select("KeyLight")
        mc.rotate(-angle, 0, 0, os=True, r=True)
        mc.select("FillLight")
        mc.rotate(-angle, 0, 0, os=True, r=True)
        mc.select("RimLight")
        mc.rotate(-angle, 0, 0, os=True, r=True)
    # If not selected, prints statement.
    else:
        print "Three-point lighting was not selected"
    # Clear the selections.
    mc.select(cl=True)
# Function for adjusting the rotation of the lights around the center axis.
def adjustEnvironmentPosition():
    # Variables for pulling user data from above.
    threePointPos = mc.checkBox("threeLight", query=True, value=True)
    rotation = mc.floatSliderGrp("position", query=True, value=True)
    # To adjust the  rotation of the lights around the axis.
    # Checks to see if create three-point lighting was selected.
    if threePointPos == True:
        # IF selected, rotates the whole light group around the scene origin.
        mc.select("ThreePointLighting")
        mc.rotate(0, rotation, 0)
    # If not selected, prints statement.
    else:
        print "Three-point lighting was not selected"
    # Clears selections.  
    mc.select(cl=True)
    
# Function for adjusting the individual attributes of the lights.
def adjustLookDevLightsIntensity():
    # Create variables for the user input options.
    threePointAdj = mc.checkBox("threeLight", query=True, value=True)
    # Variable for the key light.
    keyIntense = mc.floatSliderGrp("keyOne", q=True, value=True)
    # Variable for the rim light.
    rimIntense = mc.floatSliderGrp("rimOne", q=True, value=True)
    # Variable for the fill light.
    fillIntense = mc.floatSliderGrp("fillOne", q=True, value=True)
    # Checks to see if create three-point lighting was selected.
    if threePointAdj == True:
        # If selected, adjusts the light intensities based on user input.
        mc.setAttr("KeyLight.intensity", keyIntense)
        mc.setAttr("RimLight.intensity", rimIntense)
        mc.setAttr("FillLight.intensity", fillIntense)
    # If not selected, prints statement.
    else:
        print "Three-point lighting was not selected"
# Function for adjusting the ray trace shadow attribute of the key light.
def adjustLookDevLightsKeyShadows():
    # Variables for pulling user input.
    threePointShad = mc.checkBox("threeLight", query =True, value = True)
    keyOpts1 = mc.checkBox("keyShad", q=True, value=True)
    # Checks to see if create three-point lighting was selected.
    if threePointShad == True:
        # If selected, checks to see if the show ray trace shadows option was selected.  
        if keyOpts1 == True:
            # If selected, turns on ray trace shadows for the key light.
            mc.setAttr("KeyLightShape.useRayTraceShadows", 1)
        # If not selected, turns off ray trace shadows for the key light.
        else:
            mc.setAttr("KeyLightShape.useRayTraceShadows", 0)
    # IF three point lighting not selected, prints statement.  
    else:
        print "Three-point lighting was not selected"
# Function for adjusting the emit diffuse attribute of the key light.   
def adjustLookDevLightsKeyDiffuse():
    # Creates variables for pulling user data.
    threePointDif = mc.checkBox("threeLight", query=True, value=True)
    keyOpts2 = mc.checkBox("keyDiff", q=True, value=True)
    # Checks to see if create three-point lighting was selected.
    if threePointDif == True:
        # If selected, checks to see if the emit diffuse option was selected.  
        if keyOpts2 == True:
            # If selected, turns on emit diffuse for the key light.
            mc.setAttr("KeyLightShape.emitDiffuse", 1)
        # If not selected, turns off emit diffuse for the key light.
        else:
            mc.setAttr("KeyLightShape.emitDiffuse", 0)
    # IF three point lighting not selected, prints statement. 
    else:
        print "Three-point lighting was not selected"
# Function for adjusting the emit specular attribute of the key light. 
def adjustLookDevLightsKeySpec():
    # Creates variables for pulling user data.
    threePointSpec = mc.checkBox("threeLight", query =True, value = True)
    keyOpts3 = mc.checkBox("keySpec", q=True, value=True)
    # Checks to see if create three-point lighting was selected.
    if threePointSpec == True:
        # If selected, checks to see if the emit specular option was selected
        if keyOpts3 == True:
            # If selected, turns on emit specular for the key light.
            mc.setAttr("KeyLightShape.emitSpecular", 1)
        # If not selected, turns off emit specular for the key light.
        else:
            mc.setAttr("KeyLightShape.emitSpecular", 0)
    # IF three point lighting not selected, prints statement.
    else:
        print "Three-point lighting was not selected"
# Function for adjusting the ray trace shadow attribute of the rim light.    
def adjustLookDevLightsRimShadows():
    # Creates variables for pulling user data.
    threePointShad2 = mc.checkBox("threeLight", query =True, value = True)
    rimOpts1 = mc.checkBox("rimShad", q=True, value=True)
    # Checks to see if create three-point lighting was selected.
    if threePointShad2 == True:
        # If selected, checks to see if the show ray trace shadows option was selected.
        if rimOpts1 == True:
            # If selected, turns on ray trace shadows for the rim light.
            mc.setAttr("RimLightShape.useRayTraceShadows", 1)
        # If not selected, turns off ray trace shadows for the rim light.
        else:
            mc.setAttr("RimLightShape.useRayTraceShadows", 0)
    # IF three point lighting not selected, prints statement.
    else:
        print "Three-point lighting was not selected"
# Function for adjusting the emit diffuse attribute of the rim light.        
def adjustLookDevLightsRimDiffuse():
    # Creates variables for pulling user data.
    threePointDif2 = mc.checkBox("threeLight", query=True, value=True)
    rimOpts2 = mc.checkBox("rimDiff", q=True, value=True)
    # Checks to see if create three-point lighting was selected.
    if threePointDif2 == True:
        # If selected, checks to see if the emit diffuse option was selected.
        if rimOpts2 == True:
            # If selected, turns on emit diffuse for the rim light.
            mc.setAttr("RimLightShape.emitDiffuse", 1)
        # If not selected, turns off emit diffuse for the key light.
        else:
            mc.setAttr("RimLightShape.emitDiffuse", 0)
    # IF three point lighting not selected, prints statement.
    else:
        print "Three-point lighting was not selected"
# Function for adjusting the emit specular attribute of the rim light.         
def adjustLookDevLightsRimSpec():
    # Creates variables for pulling user data.
    threePointSpec2 = mc.checkBox("threeLight", query =True, value = True)
    rimOpts3 = mc.checkBox("rimSpec", q=True, value=True)
    # Checks to see if create three-point lighting was selected.
    if threePointSpec2 == True:
        # If selected, checks to see if the emit specular option was selected
        if rimOpts3 == True:
            # If selected, turns on emit specular for the rim light.
            mc.setAttr("RimLightShape.emitSpecular", 1)
        # If not selected, turns off emit specular for the key light.
        else:
            mc.setAttr("RimLightShape.emitSpecular", 0)
    # IF three point lighting not selected, prints statement.
    else:
        print "Three-point lighting was not selected"
# Function for adjusting the ray trace shadow attribute of the fill light.       
def adjustLookDevLightsFillShadows():
    # Creates variables for pulling user data.
    threePointShad3 = mc.checkBox("threeLight", query =True, value = True)
    fillOpts1 = mc.checkBox("fillShad", q=True, value=True)
    # Checks to see if create three-point lighting was selected.
    if threePointShad3 == True:
        # If selected, checks to see if the show ray trace shadows option was selected.
        if fillOpts1 == True:
            # If selected, turns on ray trace shadows for the fill light.
            mc.setAttr("FillLightShape.useRayTraceShadows", 1)
        # If not selected, turns off ray trace shadows for the rim light.
        else:
            mc.setAttr("FillLightShape.useRayTraceShadows", 0)
    # IF three point lighting not selected, prints statement.
    else:
        print "Three-point lighting was not selected"
# Function for adjusting the emit diffuse attribute of the fill light.         
def adjustLookDevLightsFillDiffuse():
    # Creates variables for pulling user data
    threePointDif3 = mc.checkBox("threeLight", query=True, value=True)
    fillOpts2 = mc.checkBox("fillDiff", q=True, value=True)
    # Checks to see if create three-point lighting was selected.
    if threePointDif3 == True:
        # If selected, checks to see if the emit diffuse option was selected.
        if fillOpts2 == True:
            # If selected, turns on emit diffuse for the rim light.
            mc.setAttr("FillLightShape.emitDiffuse", 1)
        # If not selected, turns off emit diffuse for the key light.
        else:
            mc.setAttr("FillLightShape.emitDiffuse", 0)
    # IF three point lighting not selected, prints statement.
    else:
        print "Three-point lighting was not selected"
# Function for adjusting the emit specular attribute of the fill light.    
def adjustLookDevLightsFillSpec():
    # Creates variables for pulling user data
    threePointSpec3 = mc.checkBox("threeLight", query =True, value = True)
    fillOpts3 = mc.checkBox("fillSpec", q=True, value=True)
    # Checks to see if create three-point lighting was selected.
    if threePointSpec3 == True:
        # If selected, checks to see if the emit specular option was selected
        if fillOpts3 == True:
            # If selected, turns on emit specular for the fill light.
            mc.setAttr("FillLightShape.emitSpecular", 1)
        # If not selected, turns off emit specular for the fill light.
        else:
            mc.setAttr("FillLightShape.emitSpecular", 0)
    # IF three point lighting not selected, prints statement.
    else:
        print "Three-point lighting was not selected"
# Function to reset the GUI.  Does not clear scene.
def resetUI():
    lookDevWindow()
# Function to close the GUI.
def closeUI():
    mc.deleteUI("lookDev_win")    

# Calls the showWindow function.
lookDevWindow()