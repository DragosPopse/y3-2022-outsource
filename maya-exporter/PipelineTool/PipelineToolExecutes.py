import maya.cmds as cmds
import os



### - EXPORT FILE TO LOCATION (AND ENGINE IF SELECTED)
def ExportNow(ENGINEDIRREF,SUFFIXREF,CheckboxRoute,ENGINE,*args):
    
    # get maya file location
    LOCALDIR = cmds.file(q=1,sn=1)
    FILENAME = None
    SUFFIX = cmds.textFieldGrp(SUFFIXREF,q=1,tx=1)
    ENGINEDIR = cmds.text(ENGINEDIRREF,q=1,l=1)
    FILE = None

    #get checkbox value
    PIVOT = cmds.checkBox(CheckboxRoute,q=1,v=1)

    # get selected objects
    selectedBase = cmds.ls(sl=1)
    selected = cmds.duplicate(selectedBase)
    for object in selected:
        cmds.makeIdentity(object,a=1,t=1)

    # get starting positions and set objects to origin
    if PIVOT:
        for object in selected:
            oldPosWhole = cmds.xform(object,q=1,piv=1,ws=1)
            oldPos = [-oldPosWhole[0], -oldPosWhole[1], -oldPosWhole[2]]
            cmds.xform(object,t=oldPos)
            cmds.makeIdentity(object,a=1,t=1)

    # LOCAL EXPORT
    # check if anything is selected
    if len(selected) > 0:

        selectedFirst = selected[0]
    
        # check if the current directory of the maya file exists
        if LOCALDIR != None or LOCALDIR != "":

            # create export directory in maya directory
            FILENAMEBASE = os.path.basename(LOCALDIR)
            FILENAME, ext = os.path.splitext(FILENAMEBASE)
            EXPORTDIR = LOCALDIR.replace(FILENAMEBASE,"") + FILENAME + "_Exports"
            FILE = "/" + FILENAME + "_" + selectedFirst + SUFFIX
            EXPORTFILE = EXPORTDIR + FILE
            
            # check if export folder exists, if it doesnt, create it
            if os.path.exists(EXPORTDIR) == False:
                os.mkdir(EXPORTDIR)
            
            # export the file
            cmds.file(EXPORTFILE,es=1,typ="FBX export")

        # if the local directory doesnt exist, give warning
        else:
            cmds.warning("Maya file has no directory, please save the file before exporting.")
    
    # if no object is selected, give warning
    else:
        cmds.warning("No objects selected.")


    # ENGINE EXPORT
    # check if this will be an engine export
    if ENGINE == True:
        
        # if anything is selected
        if len(selected) > 0:

            # check if engine directory contains anything at all
            if ENGINEDIR != "" or ENGINEDIR != None:

                # check if engine directory input exists
                if os.path.exists(ENGINEDIR) == True:
                    
                    # create engine file ref and export
                    ENGINEFILE = ENGINEDIR + FILE
                    cmds.file(ENGINEFILE,es=1,typ="FBX export")
                
                # give warning if engine directory doesnt exist
                else:
                    cmds.warning("Engine path either does not exist, or is wrongly put in. Please check and try again.")
            
            # give warning if engine directory is not given
            else:
                cmds.warning("No engine directory given")

        # if no object is selected, give warning
        else:
            cmds.warning("No objects selected.")

    # reset positions
    cmds.delete(selected)




### - CREATE UV MATERIAL AT GIVEN RESOLUTION
def UVMat(SIZEREF,*args):

    # get selection
    selection = cmds.ls(sl=1)

    # only do this if something is selected
    if len(selection) != 0:

        # get uv selected size
        SIZE = cmds.optionMenu(SIZEREF,q=1,v=1)

        # get this python module path
        PATH = __file__
        PYFILE = os.path.basename(__file__)
        MODULEPATH = PATH.replace(PYFILE,"")

        # get uv file and material that are needed
        UVFILE = MODULEPATH + "UV" + str(SIZE) + ".tga"
        MATERIAL = "M_PipelineToolUV_" + str(SIZE)

        # check if needed material exists, if not, create it
        allMaterials = cmds.ls(materials=1)
        if allMaterials.count(MATERIAL) == 0:
            MATERIAL = cmds.shadingNode("lambert", name=MATERIAL, asShader=True)
            
            # apply texture
            fileNode = cmds.shadingNode('file',asTexture=1)
            cmds.setAttr(fileNode + '.fileTextureName',UVFILE,type='string')
            cmds.connectAttr(fileNode + ".outColor",MATERIAL + ".color")

        # apply materials
        for selected in selection:
            cmds.select(selected)
            cmds.hyperShade(assign=MATERIAL)
    
    # give warning if nothing is selected
    else:
        cmds.warning("No objects are selected")
    
    cmds.select(selection)



### - CREATE MATERIAL WITH OBJECT NAME
def MakeMat(SUFFIXREF,*args):

    # get the suffix for the material
    SUFFIX = cmds.textFieldGrp(SUFFIXREF,q=1,tx=1)
    
    # get selection
    selection = cmds.ls(sl=1)

    # create the material names
    for selected in selection:
        if "SM_" in selected:
            MATERIAL = selected.replace("SM_","M_") + SUFFIX
        else:
            MATERIAL = "M_" + selected + SUFFIX
        
        # create the materials
        MATERIAL = cmds.shadingNode("lambert", name=MATERIAL, asShader=True)
        cmds.select(selected)
        cmds.hyperShade(assign=MATERIAL)
    
    cmds.select(selection)



### - IMPORT CHARACTER FOR SIZE COMPARISON
def CharImport(*args):
    cmds.file("C:/Users/oli4d/Documents/maya/2023/scripts/PipelineTool/UnrealCharacter.fbx",
        i=1,
        type="FBX",
        ignoreVersion=1,
        ra=1,
        mergeNamespacesOnClash=0,
        namespace="UnrealCharacter",
        options="fbx",
        pr=1,
        importFrameRate=1,
        importTimeRange="override")



### - CUSTOM FILE LOCATION AND SAVE
def CreateMayaFiles(FiletypeRoute,FilenameRoute,*args):

    # get initial file type and name
    Filetype = cmds.optionMenu(FiletypeRoute,q=1,v=1)
    Filename = cmds.textFieldGrp(FilenameRoute,q=1,tx=1)
    Filename = Filename.replace(" ","_")
    
    # open file browser
    unicodeLocation = cmds.fileDialog2(caption="Set Maya File Location",okCaption="Create",dialogStyle=1,fileMode=3,ff="Maya Ascii (.ma).mb")

    # check if path exists
    if unicodeLocation != None and unicodeLocation != "":
        cleanpath = str(unicodeLocation[0])
    
        # clean path
        if cleanpath[-1] != "/" or cleanpath[-1] != "\\":
            cleanpath = cleanpath + "/"
        cleanpath.replace("\\","/")

        # get full path
        newdir = cleanpath + Filename + "/"
        fullpath = newdir + Filename + Filetype

        # check if directory exists, if not, make it
        if os.path.exists(newdir) == False:
            os.mkdir(newdir)
        
        # create and save new file
        cmds.file(new=1)
        cmds.file(rename=fullpath)
        if os.path.exists(fullpath) == False:
            if Filetype == ".ma":
                cmds.file(save=1,type="mayaAscii")
            elif Filetype == ".mb":
                cmds.file(save=1,type="mayaBinary")



### - OPEN LOCAL EXPORT FOLDER
def OpenExportFolder(*args):

    # get file location
    LOCALDIR = cmds.file(q=1,sn=1)

    # get export directory, if local directory exists
    if LOCALDIR != None or LOCALDIR != "":
        FILENAMEBASE = os.path.basename(LOCALDIR)
        FILENAME, ext = os.path.splitext(FILENAMEBASE)
        EXPORTDIR = LOCALDIR.replace(FILENAMEBASE,"") + FILENAME + "_Exports"

        # if the export folder exists, open it. otherwise give a warning
        if os.path.exists(EXPORTDIR) == True:
            os.startfile(EXPORTDIR)
        else:
            cmds.warning("No export folder found, please first export a file.")
    
    # if the local directory doesnt exist, give a warning
    else:
        cmds.warning("Maya file not saved, please first save the Maya file.")



### - PICK ENGINE DIRECTORY BUTTON
def PickEngineDirectory(ENGINEDIR,*args):

    # get path from file dialog
    unicodeLocation = cmds.fileDialog2(caption="Set Engine Directory",fileMode=3,okCaption="Select")

    # check if path exists
    if unicodeLocation != None and unicodeLocation != "":
        cleanpath = str(unicodeLocation[0])
    
        # clean path
        if cleanpath[-1] != "/" or cleanpath[-1] != "\\":
            cleanpath = cleanpath + "/"
        cleanpath.replace("\\","/")
        
        # store path on ui text
        cmds.text(ENGINEDIR,e=1,l=cleanpath)