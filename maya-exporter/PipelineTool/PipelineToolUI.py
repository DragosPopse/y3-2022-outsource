import maya.cmds as cmds
import PipelineTool.PipelineToolExecutes as PTE
from functools import partial

# window settings
WinWidth = 400
WinHeight = 600
ModuleHeight = 35
BackgroundColorMaya = [16/255, 110/255, 140/255]
BackgroundColorExport = [23/255, 101/255, 16/255]
BackgroundColorTools = [100/255, 0/255, 0/255]

### - CREATE WINDOW
def PipelineToolUIFunc():
    PipelineWindow = cmds.window("Pipeline Tools v1.0",w=WinWidth,h=WinHeight,s=0)
    cmds.columnLayout(rowSpacing=0)
    EngineDirectory = None
    
    # new maya file section
    cmds.frameLayout("New Maya File",cll=1,w=WinWidth,bgc=BackgroundColorMaya,ebg=1)
    cmds.rowLayout(nc=2,w=WinWidth)
    FileName = cmds.textFieldGrp(tx="File_Name",w=WinWidth/2,h=ModuleHeight)
    FileType = cmds.optionMenu(w=WinWidth/2,h=ModuleHeight)
    cmds.menuItem(l=".ma")
    cmds.menuItem(l=".mb")
    cmds.setParent("..")
    cmds.button(l="Choose Directory and Create",c=partial(PTE.CreateMayaFiles,FileType,FileName),w=WinWidth,h=ModuleHeight)

    # create seperator in between
    cmds.setParent("..")
    cmds.separator(h=10,style="singleDash",w=WinWidth)
    
    # export section
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.frameLayout("Export",cll=1,w=WinWidth,bgc=BackgroundColorExport,ebg=1)
    ExportSuffix = cmds.textFieldGrp(label="Suffix",w=WinWidth,h=ModuleHeight)
    cmds.rowLayout(nc=2,w=WinWidth)
    EngineDirectory = cmds.text(l="Please pick a directory",w=WinWidth/2)
    cmds.button(l="Set Engine Directory",c=partial(PTE.PickEngineDirectory,EngineDirectory),w=WinWidth/2,h=ModuleHeight)
    cmds.setParent("..")
    cmds.rowLayout(nc=2,w=WinWidth)
    CheckBox = cmds.checkBox(label="Export with\npivot in origin",w=WinWidth/2, v=0)
    cmds.button(l="Open Export Folder",c=PTE.OpenExportFolder,w=WinWidth/2,h=ModuleHeight)
    cmds.setParent("..")
    cmds.rowLayout(nc=2,w=WinWidth)
    cmds.button(l="Export",c=partial(PTE.ExportNow,EngineDirectory,ExportSuffix, CheckBox,False),w=WinWidth/2,h=ModuleHeight)
    cmds.button(l="Export to Engine",c=partial(PTE.ExportNow,EngineDirectory,ExportSuffix, CheckBox,True),w=WinWidth/2,h=ModuleHeight)
    cmds.setParent("..")
    
    # create seperator in between
    cmds.setParent("..")
    cmds.separator(h=10,style="singleDash",w=WinWidth)
    
    # tools sections
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.frameLayout("Tools",cll=1,w=WinWidth,bgc=BackgroundColorTools,ebg=1)
    cmds.rowLayout(nc=2,w=WinWidth)
    UVSIZE = cmds.optionMenu(label="Select UV size",w=WinWidth/2,h=ModuleHeight)
    cmds.menuItem(l="512")
    cmds.menuItem(l="1024")
    cmds.menuItem(l="2048")
    cmds.button(l="Create UV Texture",c=partial(PTE.UVMat, UVSIZE),w=WinWidth/2,h=ModuleHeight)
    cmds.setParent("..")
    cmds.separator(h=5,style="singleDash",w=WinWidth)
    cmds.button(l="Import Character",c=PTE.CharImport,w=WinWidth,h=ModuleHeight)
    cmds.separator(h=5,style="singleDash",w=WinWidth)
    cmds.rowLayout(nc=2,w=WinWidth)
    MATSUFFIX = cmds.textFieldGrp(label="Suffix",w=WinWidth/2,h=ModuleHeight)
    cmds.button(l="Create Material",c=partial(PTE.MakeMat, MATSUFFIX),w=WinWidth/2,h=ModuleHeight)
    
    # show the window after constructing
    cmds.showWindow(PipelineWindow)