#Title-Change_Camera_with_File.py
#Author-NE
#Description-Changes the camera view to the saved view in the text file. Used with Capture_Camera_with_File.py
import adsk.core, adsk.fusion, traceback

commandId = 'CameraHome'
workspaceToUse = 'FusionSolidEnvironment'
panelToUse = 'SolidScriptsAddinsPanel'

# global set of event handlers to keep them referenced for the duration of the command
handlers = []

def cameraFront():
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        camera = app.activeViewport.camera
        camera.eye = adsk.core.Point3D.create(13.468716356034628,-15.772487302489822,17.61395623273426)
        camera.target = adsk.core.Point3D.create(2.4999999274732545,0.1962289810180664,1.6452399492263794)
        camera.upVector = adsk.core.Vector3D.create(0.0,0.0,1.0)

        app.activeViewport.camera = camera
        app.activeViewport.fit()

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def commandDefinitionById(id):
    app = adsk.core.Application.get()
    ui = app.userInterface
    if not id:
        ui.messageBox('commandDefinition id is not specified')
        return None
    commandDefinitions_ = ui.commandDefinitions
    commandDefinition_ = commandDefinitions_.itemById(id)
    return commandDefinition_

def commandControlByIdForPanel(id):
    app = adsk.core.Application.get()
    ui = app.userInterface
    if not id:
        ui.messageBox('commandControl id is not specified')
        return None
    workspaces_ = ui.workspaces
    modelingWorkspace_ = workspaces_.itemById(workspaceToUse)
    toolbarPanels_ = modelingWorkspace_.toolbarPanels
    toolbarPanel_ = toolbarPanels_.itemById(panelToUse)
    toolbarControls_ = toolbarPanel_.controls
    toolbarControl_ = toolbarControls_.itemById(id)
    return toolbarControl_

def destroyObject(uiObj, tobeDeleteObj):
    if uiObj and tobeDeleteObj:
        if tobeDeleteObj.isValid:
            tobeDeleteObj.deleteMe()
        else:
            uiObj.messageBox('tobeDeleteObj is not a valid object')
def run(context):
    ui = None
    try:
        commandName = 'cameraHome'
        commandDescription = 'cameraHome'
        commandResources = './resources/'

        app = adsk.core.Application.get()
        ui = app.userInterface

        class CommandExecuteHandler(adsk.core.CommandEventHandler):
            def __init__(self):
                super().__init__()
            def notify(self, args):
                try:
                  cameraFront()
                except:
                    if ui:
                        ui.messageBox('command executed failed:\n{}'.format(traceback.format_exc()))

        class CommandCreatedEventHandlerPanel(adsk.core.CommandCreatedEventHandler):
            def __init__(self):
                super().__init__() 
            def notify(self, args):
                try:
                    cmd = args.command
                    onExecute = CommandExecuteHandler()
                    cmd.execute.add(onExecute)
                    # keep the handler referenced beyond this function
                    handlers.append(onExecute)

                except:
                    if ui:
                        ui.messageBox('Panel command created failed:\n{}'.format(traceback.format_exc()))

        class CommandCreatedEventHandlerQAT(adsk.core.CommandCreatedEventHandler):
            def __init__(self):
                super().__init__()
            def notify(self, args):
                try:
                    command = args.command
                    onExecute = CommandExecuteHandler()
                    command.execute.add(onExecute)
                    # keep the handler referenced beyond this function
                    handlers.append(onExecute)

                except:
                    ui.messageBox('QAT command created failed:\n{}'.format(traceback.format_exc()))

        commandDefinitions_ = ui.commandDefinitions

		# check if we have the command definition
        commandDefinition_ = commandDefinitions_.itemById(commandId)
        if not commandDefinition_:
            commandDefinition_ = commandDefinitions_.addButtonDefinition(commandId, commandName, commandDescription, commandResources)		 

        onCommandCreated = CommandCreatedEventHandlerPanel()
        commandDefinition_.commandCreated.add(onCommandCreated)
        # keep the handler referenced beyond this function
        handlers.append(onCommandCreated)
        
        # add a command on create panel in modeling workspace
        workspaces_ = ui.workspaces
        modelingWorkspace_ = workspaces_.itemById(workspaceToUse)
        toolbarPanels_ = modelingWorkspace_.toolbarPanels
        toolbarPanel_ = toolbarPanels_.itemById(panelToUse) 
        toolbarControlsPanel_ = toolbarPanel_.controls
        toolbarControlPanel_ = toolbarControlsPanel_.itemById(commandId)
        if not toolbarControlPanel_:
            toolbarControlPanel_ = toolbarControlsPanel_.addCommand(commandDefinition_, '')
            toolbarControlPanel_.isVisible = True
            #ui.messageBox('A CSV command is successfully added to the create panel in modeling workspace')

    except:
        if ui:
            ui.messageBox('AddIn Start Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        objArray = []

        commandControlPanel_ = commandControlByIdForPanel(commandId)
        if commandControlPanel_:
            objArray.append(commandControlPanel_)
            
        commandDefinition_ = commandDefinitionById(commandId)
        if commandDefinition_:
            objArray.append(commandDefinition_)

        for obj in objArray:
            destroyObject(ui, obj)

    except:
        if ui:
            ui.messageBox('AddIn Stop Failed:\n{}'.format(traceback.format_exc()))

