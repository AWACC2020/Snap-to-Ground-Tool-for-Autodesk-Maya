# Author  : AWACS
# Time    : 2020/09/03

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

def MayaDropRemove():
    """Drag and drop this file into the scene executes the file."""

    User_script_dir =  cmds.internalVar(usd=1)
    Customized_script_dir = os.path.join( User_script_dir , 'AWACS')

    result_path = os.path.join( Customized_script_dir , 'Snap_to_Ground')

    if os.path.isdir( result_path ):
        shutil.rmtree( result_path )
    else :
        print ( "No such path , Nothing good to remove" )

    # print (os.listdir ( Customized_script_dir ) )

    if len( os.listdir ( Customized_script_dir ) ) < 1:
        shutil.rmtree( Customized_script_dir )

    print("// Snap_Ground has been Removed From your software, you can remove the command from shelf now")


if isMaya:
    MayaDropRemove()
