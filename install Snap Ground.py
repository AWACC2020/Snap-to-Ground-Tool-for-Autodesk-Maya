import os
import shutil

try:
    import maya.mel
    import maya.cmds as cmds
    isMaya = True
except ImportError:
    isMaya = False

def onMayaDroppedPythonFile(*args, **kwargs):
    pass

def MayaDropinstall():
    """Drag and drop this file into the scene executes the file."""

    ContainPath = os.path.join(os.path.dirname(__file__), 'Snap_to_Ground')
    ContainPath = os.path.normpath(ContainPath)

    print ContainPath

    if not os.path.exists(ContainPath):
        raise IOError('Cannot find ' + ContainPath)

    User_script_dir =  cmds.internalVar(usd=1)
    AWA_script_dir = os.path.join( User_script_dir , 'AWACS')

    try:
        os.makedirs( AWA_script_dir )
    except:
        # AWA_script_dir Already exist
        pass

    result_path = os.path.join( AWA_script_dir , 'Snap_to_Ground')
    # print result_path
    # result_path = os.path.normpath(result_path)
    # print result_path

    if os.path.isdir( result_path ):
        print ( str( result_path ) + " is Already Exist " + " -------------reinstalling")
        shutil.rmtree( result_path )
    else :
        pass

    shutil.copytree( ContainPath , result_path )

    print ('//install success')

    iconPath = os.path.join(result_path, 'icon.jpg')
    iconPath = os.path.normpath(iconPath)

    command = '''
import sys
sys.path.append( "{path}" )
import Snap_Ground
reload (Snap_Ground)
'''.format(path=result_path)

    shelf = maya.mel.eval('$gShelfTopLevel=$gShelfTopLevel')
    parent = cmds.tabLayout(shelf, query=True, selectTab=True)
    cmds.shelfButton(
        command=command,
        annotation='Snap to Ground',
        sourceType='Python',
        image=iconPath,
        image1=iconPath,
        parent=parent
    )

    print("// Snap_Ground has been added to current shelf")


if isMaya:
    MayaDropinstall()
