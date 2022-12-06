import maya.cmds as cmds


# There is no way to edit a runtime command so we need to check if it
# exists and then remove it if it does.
my_command_name = 'export'
if cmds.runTimeCommand(my_command_name, q=True, exists=True):
    cmds.runTimeCommand(my_command_name, e=True, delete=True)

cmds.runTimeCommand(
    my_command_name, 
    ann='My Command', 
    category='User', 
    command='import PipelineTool.PipelineToolUI as PTUI; PTUI.PipelineToolUIFunc()', 
    commandLanguage='python'
    )
# cmds.nameCommand('export', ann='Export UI', command=my_command_name)
cmds.hotkey(k='k', altModifier=True, shiftModifier=True, ctrlModifier=True, name='')
cmds.hotkey(k='k', altModifier=True, shiftModifier=True, ctrlModifier=True, name='export')
