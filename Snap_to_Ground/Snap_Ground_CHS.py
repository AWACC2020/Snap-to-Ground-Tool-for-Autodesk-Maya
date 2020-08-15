# -!- coding: utf-8 -!-
# Author  : AWACS
# Time    : 2020/08/15
# version : 0.85 beta

import maya.cmds as cmds
import os
import math

def Get_Center_Pos_from_list( input_pos_list ):
    Xsum , Ysum , Zsum = [0,0,0]
    #get center pos
    for indFindedPos in input_pos_list :
        Xsum += indFindedPos[0]
        Ysum += indFindedPos[1]
        Zsum += indFindedPos[2]
        # print (indFindedPos)
    Findednum = float( len(input_pos_list) )
    Result = [ Xsum / Findednum , Ysum / Findednum , Zsum / Findednum ]
    return Result

def GetObjectAxisPos( Object ):
    # Result =  cmds.xform( Object , query = 1, worldSpace = 1, translation = 1)
    Result =  cmds.xform( Object , query = 1, worldSpace = 1 ,rotatePivot  = 1)
    return Result

def GetObjectBBOX_transpos( Object , Axis = "Y" , PositiveAxis = True ,boundingBoxInvisible = False):
    if boundingBoxInvisible:
        BB = cmds.xform( Object , query = 1, worldSpace = 1, boundingBoxInvisible = 1)
    else:
        BB = cmds.xform( Object , query = 1, worldSpace = 1, bb = 1)

    Result = []
    if Axis == "Y":
        Result.append( (BB [0] + BB [3]) / 2.0 )
        if PositiveAxis :
            Result.append( BB [1] )
        else :
            Result.append( BB [4] )
        Result.append( (BB [2] + BB [5]) / 2.0 )
    elif Axis == "X":
        if PositiveAxis :
            Result.append( BB [0] )
        else :
            Result.append( BB [3] )
        Result.append( (BB [1] + BB [4]) / 2.0 )
        Result.append( (BB [2] + BB [5]) / 2.0 )
    elif Axis == "Z":
        Result.append( (BB [0] + BB [3]) / 2.0 )
        Result.append( (BB [1] + BB [4]) / 2.0 )
        if PositiveAxis :
            Result.append( BB [2] )
        else :
            Result.append( BB [5] )
    # print Result
    return Result

def Find_Loweset_Pos( Object  , Threshold_Val = 0.02 , Threshold_On = True , Axis = "Y" , PositiveAxis = True):
    Object_elem = ".vtx["
    try:
        elemnum = cmds.polyEvaluate( Object )['vertex']
    except:
        #bypass,is not a polygon
        try:
            cmds.select( cl = 1 )
            cmds.select ( Object +'.cv[:]' )
            cv_list = cmds.ls(selection = True ,flatten = True )
            elemnum = len(cv_list)
            Object_elem = ".cv["
        except:
            #bypass,neither a Curve
            Result = GetObjectBBOX_transpos( Object , Axis , PositiveAxis)
            return Result

    Axis_index = 1
    if Axis == "X":
        Axis_index = 0
    elif Axis == "Z":
        Axis_index = 2

    Value_list = []
    if Threshold_On == True:
        Pos_All = []
        for indelemId in range( elemnum ):
            Pos_All.append( cmds.xform( Object + Object_elem + str(indelemId) + ']', query = 1, worldSpace = 1, translation = 1) )
        for indPos in Pos_All:
            Value_list.append( indPos[ Axis_index ] )
        FindedPos = []
        if PositiveAxis :
            Search_Threshold = min(Value_list) + Threshold_Val
            for indPos in Pos_All:
                if indPos[ Axis_index ] <= Search_Threshold:
                    FindedPos.append(indPos)
        else:
            Search_Threshold = max(Value_list) - Threshold_Val
            for indPos in Pos_All:
                if indPos[ Axis_index ] >= Search_Threshold:
                    FindedPos.append(indPos)

        Result = Get_Center_Pos_from_list( FindedPos )

    else:
        for indelemId in range( elemnum ):
            Value_list.append( cmds.xform( Object + Object_elem + str(indelemId) + ']', query = 1, worldSpace = 1, translation = 1)[ Axis_index ] )
        # temporarily , sorry , No optimize yet
        # preciser = cmds.checkBox('Faster_Result', query=1, value= 1)

        # # not so precise?
        # if PositiveAxis :
        #     ResultIndex = Value_list.index( min(Value_list) )
        # else:
        #     ResultIndex = Value_list.index( max(Value_list) )
        # Result =  cmds.xform( Object + Object_elem + str(ResultIndex) + ']', query = 1, worldSpace = 1, translation = 1)

        # #---------------------
        # preciser Result?
        initval = Value_list[0]
        ResultIndex = []
        #DIFFERENCE ONLY :"<" ">"
        if PositiveAxis :
            for indValue_index in range(len(Value_list)):
                if Value_list[ indValue_index ] < initval :
                    initval = Value_list[ indValue_index ]
                    ResultIndex = []
                if Value_list[ indValue_index ] == initval :
                    ResultIndex.append( indValue_index )
        else :
            for indValue_index in range(len(Value_list)):
                if Value_list[ indValue_index ] > initval :
                    initval = Value_list[ indValue_index ]
                    ResultIndex = []
                if Value_list[ indValue_index ] == initval :
                    ResultIndex.append( indValue_index )

        FindedPos = []
        for indResult in ResultIndex:
            FindedPos.append( cmds.xform( Object + Object_elem + str(indResult) + ']', query = 1, worldSpace = 1, translation = 1) )

        Result =  Get_Center_Pos_from_list( FindedPos )
        # print (Result)
        #---------------------
    # print("Find_Loweset_Pos ----------- Success")
    return Result

def Projection_Curve( Center_Pos_in , Geometry , Align_to_Surface , Expand = 0.1 , Axis = "Y" , PositiveAxis = True):
    # if Align_to_Surface:
    if True:
        Curve_init_list = []
        # print ( Center_Pos_in )
        Center_Pos = Center_Pos_in
        if Axis == "Y":
            Axis_1 = 0
            Axis_2 = 2
        elif Axis == "X":
            Axis_1 = 1
            Axis_2 = 2
        elif Axis == "Z":
            Axis_1 = 0
            Axis_2 = 1
        Poslist_Start = [ Center_Pos[:] , Center_Pos[:] , Center_Pos[:] , Center_Pos[:] , Center_Pos[:] ]

        Poslist_Start[ 1 ][ Axis_1 ] = Poslist_Start[ 1 ][ Axis_1 ] + Expand
        Poslist_Start[ 2 ][ Axis_1 ] = Poslist_Start[ 2 ][ Axis_1 ] - Expand
        Poslist_Start[ 3 ][ Axis_2 ] = Poslist_Start[ 3 ][ Axis_2 ] + Expand
        Poslist_Start[ 4 ][ Axis_2 ] = Poslist_Start[ 4 ][ Axis_2 ] - Expand

        offset_endpos = 30.0
        Poslist_End = []
        for indpos in Poslist_Start:
            Poslist_End.append( [ indpos[0]+ offset_endpos , indpos[1]+ offset_endpos , indpos[2]+ offset_endpos ] )

        for indpos_index in range(0,5):
            Curve_init_list.append(cmds.curve( p=[ Poslist_Start[indpos_index] , Poslist_End[indpos_index] ], k=[0, 1], d=1) )

        # print (Poslist_Start)
        # print (Poslist_End)
        ProjectResultGRP_list = []
        # ProjectResult_list = []
        # print ( "=================--------------=============")

        # if PositiveAxis :
        #     Pointing = -1.0
        # else:
        #     Pointing = 1.0
        Pointing = 1.0
        direction = (0.0, Pointing , 0.0)
        if Axis == "X":
            direction = (Pointing, 0.0 , 0.0)
        elif Axis == "Z":
            direction = (0.0, 0.0 , Pointing)
        #---------------------------------------------

        try:
            Result_Pos_list = []
            for indCurve in Curve_init_list:
                ProjectResultGRP = cmds.polyProjectCurve( indCurve , Geometry , direction= direction , ch=0, automatic=1, curveSamples=50, tolerance=0.001, pointsOnEdges=0)[0]
                ProjectResultGRP_list.append ( ProjectResultGRP )
                ProjectResult_list = cmds.listRelatives(ProjectResultGRP,c=1)
                if len(ProjectResult_list) == 1:
                    ProjectResult = ProjectResult_list[0]
                else:
                    # try find the shortest curve from multiple Result
                    ProjectResult = ProjectResult_list[0]
                    for indProjectResult_index in range(len(ProjectResult_list)):
                        indbb = cmds.xform( ProjectResult_list[indProjectResult_index] , query = 1, worldSpace = 1, bb = 1)
                        indCP = [ 
                                ( indbb[3]-indbb[0] )/2.0 + indbb[0] ,
                                ( indbb[4]-indbb[1] )/2.0 + indbb[1] ,
                                ( indbb[5]-indbb[2] )/2.0 + indbb[2] ]
                        disX = Center_Pos [0] - indCP [0]
                        disY = Center_Pos [1] - indCP [1]
                        disZ = Center_Pos [2] - indCP [2]
                        distance = pow ( ( disX * disX + disY * disY + disZ * disZ ) , 1.0/3.0 )
                        # print  ProjectResult_list[indProjectResult_index] 
                        # print distance

                        if indProjectResult_index == 0:
                            initdist = distance
                        else:
                            if distance < initdist :
                                initdist = distance
                                ProjectResult = ProjectResult_list[indProjectResult_index]
                    # addable: try to get the curve base on Axis?

                # print ( ProjectResult )
                # print ( "AAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
                cmds.select( cl = 1 )
                # cmds.duplicate(ProjectResultGRP)
                cmds.select( ProjectResult + ".cv[:]" ,add = 1)
                cv = cmds.ls( selection = True ,flatten = True )
                # print ( cv )
                cvpos = [ ]

                for indcv in cv :
                    cvpos.append( cmds.xform( indcv , query = 1, worldSpace = 1, translation = 1 ) )

                initpos = cvpos[0]
                found_orginal = ""
                for indcvnum in range( len ( cvpos ) ):
                    if Axis == "X":
                        if cvpos[ indcvnum ][ 1 ] <= initpos[ 1 ] or cvpos[ indcvnum ][ 2 ] <= initpos[ 2 ]:
                            initpos[ 1 ] = cvpos[ indcvnum ][ 1 ]
                            initpos[ 2 ] = cvpos[ indcvnum ][ 2 ]
                            found_orginal = cv [ indcvnum ]
                    if Axis == "Y":
                        if cvpos[ indcvnum ][ 0 ] <= initpos[ 0 ] or cvpos[ indcvnum ][ 2 ] <= initpos[ 2 ]:
                            initpos[ 0 ] = cvpos[ indcvnum ][ 0 ]
                            initpos[ 2 ] = cvpos[ indcvnum ][ 2 ]
                            found_orginal = cv [ indcvnum ]
                    if Axis == "Z":
                        if cvpos[ indcvnum ][ 0 ] <= initpos[ 0 ] or cvpos[ indcvnum ][ 1 ] <= initpos[ 1 ]:
                            initpos[ 0 ] = cvpos[ indcvnum ][ 0 ]
                            initpos[ 1 ] = cvpos[ indcvnum ][ 1 ]
                            found_orginal = cv [ indcvnum ]
                Result_Pos = cmds.xform( found_orginal , query = 1, worldSpace = 1, translation = 1 )
                Result_Pos_list.append(Result_Pos)
                # print (indCurve)
                # print (found_orginal)
                # print (Result_Pos)
            cmds.delete( ProjectResultGRP_list )
            cmds.delete( Curve_init_list )

            # print ( "Projection_Curve ------------- Success" )
            # print (Result_Pos_list)
            # print ( "result  ====================" )
            return Result_Pos_list

        except :
            pass
            cmds.delete( Curve_init_list )
            try:
                cmds.delete( ProjectResultGRP_list )
                return False
            except :
                pass
                return False

    # else:
    #     Curve = cmds.curve(p=[ Center_Pos , Center_Pos ], k=[0, 1], d=1)

def Move_To_Ground( PivotPos , Projection_Result , Object , Axis  ):
    cmds.select(cl = 1 )
    cmds.select( Object )
    if Axis == "Y":
        Axis_index = 1
        cmds.move(0, -(PivotPos[1] - Projection_Result [0][1]) , 0, r=1)
    elif Axis == "X":
        Axis_index = 0
        cmds.move(-(PivotPos[0] - Projection_Result [0][0]), 0 , 0, r=1)
    elif Axis == "Z":
        Axis_index = 2
        cmds.move(0, 0 , -(PivotPos[2] - Projection_Result [0][2]), r=1)
    cmds.select(cl = 1 )

def Rotate_Align_to_Surface( Proj_Result , Object, Axis, Expand = 0.1 ):

    # print "RRRRRRRRRRRRRRRRRRRRRRRRRRRRRR"
    # print math.atan( Proj_Result[2][Axis_index] - Proj_Result[1][Axis_index] ) / ( Expand * 2)
    cmds.select(cl = 1 )
    cmds.select( Object )

    Axis_index = 1
    if Axis == "X":
        Axis_index = 0
    elif Axis == "Z":
        Axis_index = 2

    Axis_Rotate_1 = math.degrees( math.atan( abs(Proj_Result[2][ Axis_index ] - Proj_Result[1][ Axis_index ] ) / ( Expand * 2) ) )
    Axis_Rotate_2 = math.degrees( math.atan( abs(Proj_Result[4][ Axis_index ] - Proj_Result[3][ Axis_index ] ) / ( Expand * 2) ) )
    if Proj_Result[2][ Axis_index ] - Proj_Result[1][ Axis_index ] < 0 :
        Axis_Rotate_1 = -Axis_Rotate_1
    if Proj_Result[4][ Axis_index ] - Proj_Result[3][ Axis_index ] > 0 :
        Axis_Rotate_2 = -Axis_Rotate_2

    if Axis == "Y":
        cmds.rotate( - Axis_Rotate_2, 0, 0, r=1, p = Proj_Result[0] , fo=1 , eu = 1)
        cmds.rotate( 0, 0, - Axis_Rotate_1, r=1, p = Proj_Result[0] , fo=1 , eu = 1)
    elif Axis == "X":
        cmds.rotate( 0, Axis_Rotate_2, 0, r=1, p = Proj_Result[0] , fo=1 , eu = 1)
        cmds.rotate( 0, 0, Axis_Rotate_1, r=1, p = Proj_Result[0] , fo=1 , eu = 1)
    elif Axis == "Z":
        cmds.rotate( Axis_Rotate_2, 0, 0, r=1, p = Proj_Result[0] , fo=1 , eu = 1)
        cmds.rotate( 0, Axis_Rotate_1, 0, r=1, p = Proj_Result[0] , fo=1 , eu = 1)

    # print (Axis_Rotate_1)
    # print (Axis_Rotate_2)

    cmds.select(cl = 1 )

def indProjection( Object , Ground , Axis_index , Axis_Method , PointCheckThreshold , Threshold_On , Align_to_Surface ):
    Axis = "X"
    PositiveAxis = True
    if Axis_index == 1 or Axis_index == 4 :
        Axis = "Y"
    if Axis_index == 2 or Axis_index == 5 :
        Axis = "Z"
    if Axis_index >= 3 :
        PositiveAxis = False
    # print ( 'PositiveAxis ' + str(PositiveAxis) )
    Curve_Axis_Expanding = 0.2
    if Ground != Object:
        try:

            if Axis_Method == 1 :
                PivotPos = GetObjectBBOX_transpos( Object , Axis , PositiveAxis )
            elif Axis_Method == 2 :
                PivotPos = GetObjectAxisPos ( Object )
            else :
                PivotPos = Find_Loweset_Pos( Object , PointCheckThreshold, Threshold_On , Axis , PositiveAxis)

            # print Axis_Method 
            Projection_Result = Projection_Curve( PivotPos , Ground ,Align_to_Surface , Curve_Axis_Expanding , Axis , PositiveAxis)

            Move_To_Ground( PivotPos , Projection_Result , Object , Axis  )
            # print ("======================================================================================")
            if Align_to_Surface :
                Rotate_Align_to_Surface( Projection_Result , Object , Axis , Curve_Axis_Expanding )

            return True
        except:
            # print ("=======Drop Failed")
            return False
    else :
        return False

def Snap_To_Ground_Main( ):
    # Axis , Ground_Geometry_list , Object_list , Axis_Method , PointCheckThreshold , Threshold_On , Align_to_Surface
    Axis_RadioButton_List = [ 'POSX' , 'POSY' , 'POSZ' , 'NEGX' , 'NEGY' , 'NEGZ']
    Axis_index = 0
    for indRB in Axis_RadioButton_List:
        if cmds.radioButton( indRB , q = 1 , sl = 1):
            # print ('Axis ' + indRB)
            break
        else:
            Axis_index += 1

    Object_list = cmds.ls(selection = True)


    # Axis_Method 0 : bbox 1 : ObjectAxis 2: Lowest/extreme Position

    # Axis_Method = cmds.radioButton( 'Object_Axis' , q = 1 , sl = 1)

    # Axis_Method = cmds.optionMenu( "Transfrom_Method" , q = 1 , v = 1)
    Axis_Method = cmds.optionMenu( "Transfrom_Method" , q = 1 , sl = 1)

    Check_Other_Point = cmds.checkBox('Check_Other_Point', query=1, value= 1)
    threshold = cmds.floatField('PointCheckThreshold', query=1, value=1)
    Align_to_Surface = cmds.checkBox('Align_to_Surface', query=1, value= 1)
    Refresh_Viewport_each_Move = cmds.checkBox('Refresh_Viewport_each_Move', query=1, value= 1)

    # print (Ground_Geometry_list)
    # print (" Axis_Method " + str(Axis_Method))
    # print ( 'Check_Other_Point' + str ( Check_Other_Point ) )
    # print (threshold)
    # print ("-----------------------------Snap_To_Ground_Main")
    cmds.select( cl = 1 )
    for indObject in Object_list:
        for indGround in Ground_Geometry_list:
            # print ( ('indProjection ')+str((indObject , indGround )) )
            Action_Success = indProjection( indObject , indGround , Axis_index , Axis_Method , threshold , Check_Other_Point , Align_to_Surface )
            # print ( "Action_Success " +  str(Action_Success) )
            if Action_Success:
                print ( "Success : Move < " + indObject + " > to < " + indGround)
                if Refresh_Viewport_each_Move :
                    cmds.refresh()
                break
            else :
                print ( "Operation Failed Try next Ground" )
            
    cmds.select( Object_list ) 

def SetInputGround( ):
    Selection = cmds.ls(selection = True)
    for indsel in Selection:
        try:
            cmds.polyEvaluate( indsel )['vertex']
        except:
            print ("// Warning : Ground Object Must be a polygon mesh ,if your selection included Non-polygon Object,it will be automatically excluded")
            Selection.remove( indsel )

    global Ground_Geometry_list 
    Ground_Geometry_list = Selection
    displaystr =""
    for indsel in Selection:
        displaystr = displaystr + " " +indsel
    cmds.textField('InputGround', e = 1, tx = displaystr )
    print ("// InputGround Seted : " + displaystr )

def Question_Button( COMMAND = None , blank_space = 1 ,  btn_label = " ? " ):
    cmds.text( l= " " ,w = blank_space )
    cmds.button( c=lambda *args: eval( COMMAND ) , l= btn_label , w=20 )

def Question_Window( imageNum = 0 , Window_name = 'Question_Window' , w = 540 , h = 540):
    if cmds.window( Window_name , q=1, ex=1 ):
        cmds.deleteUI( Window_name )
    cmds.window( Window_name )
    #cmds.dockControl( area='left', content=myWindow, allowedArea=allowedAreas )
    imagelist = ["Question_Snap_To_Ground_1.jpg" ,
                 "Question_Snap_To_Ground_2.jpg" ,
                 "Question_Snap_To_Ground_3.jpg" ,
                 "Question_Snap_To_Ground_4.jpg" ,
                 "Question_Snap_To_Ground_5.jpg" ,
                 ]
    print ( Question_Window_image_path +  "/" + imagelist[ imageNum ] )
    cmds.paneLayout()
    cmds.image( image= Question_Window_image_path +  "/" + imagelist[ imageNum ] )

    cmds.showWindow( Window_name )

def UIserial( counter , width = 20):
    cmds.text(l= " " + str(counter) + " : " , w = 20 , al = "left" )
    counter +=1
    return counter

# def ToggleUI_Point_Threshold():
#     Enable = cmds.checkBox('Check_Other_Point', q=1, ed = 1 )
#     if Enable:
#         cmds.checkBox('Check_Other_Point', e=1, ed = 0 )
#     else:
#         cmds.checkBox('Check_Other_Point', e=1, ed = 1 )

def Snap_To_Ground_GUI():
    RowCounter = 1
    if cmds.window('Snap_To_Ground_By_AWACS' , q=1, ex=1 ):
        cmds.deleteUI('Snap_To_Ground_By_AWACS')

    TOOL_T = cmds.window('Snap_To_Ground_By_AWACS' )
    #cmds.dockControl( area='left', content=myWindow, allowedArea=allowedAreas )
    cmds.showWindow('Snap_To_Ground_By_AWACS')
    cmds.columnLayout()
            #global proc AWA_IK_FK_Switch  ()
    #MAYA API part ------------------------------
    cmds.rowLayout(nc=6 , h = 30 ,w = 400 )
    RowCounter = UIserial( RowCounter )
    cmds.text(l=u"选择地面网格 :  " , al = "left", w = 120)
    cmds.textField('InputGround', text = "" , w = 160, bgc = (0.1,0.1,0.1) , ed = False )
    cmds.button(c=lambda *args:  SetInputGround(), l=u"确认", w = 60 )
    Question_Button( "Question_Window( 0 )" , 10)
    cmds.setParent('..')
    
    cmds.rowLayout(nc=6 , h = 30 ,w = 400 )
    RowCounter = UIserial( RowCounter )
    cmds.text(l = u"对齐至表面 (测试中功能) : " , w = 140 , al = "left")
    cmds.checkBox( 'Align_to_Surface' , l = '',  value = True )
    Question_Button( 'Question_Window( 1 )' ,198)
    cmds.setParent('..')

    cmds.rowLayout(nc=12 , h = 30)
    RowCounter = UIserial( RowCounter )
    cmds.text(l = u"向上轴向是 : " , w = 80 , al = "left")
    cmds.radioCollection( "Axis_Collection" )
    cmds.radioButton( "POSX" , label='+X' )
    cmds.radioButton( "POSY" , label='+Y' , sl = 1)
    cmds.radioButton( "POSZ" , label='+Z' )
    cmds.radioButton( "NEGX" , label='-X' )
    cmds.radioButton( "NEGY" , label='-Y' )
    cmds.radioButton( "NEGZ" , label='-Z' )
    cmds.radioCollection( "Axis_Collection", edit=True, select="POSY" ) #set default
    Question_Button( 'Question_Window( 2 )' , 53)
    cmds.setParent('..')
    cmds.setParent('..')

    cmds.rowLayout(nc=6 , h = 30)
    RowCounter = UIserial( RowCounter )
    cmds.text(l = u"移动参照的位置是 : ")

    cmds.optionMenu( "Transfrom_Method" )
    cmds.menuItem( 'Bounding Box' , label=u'边界框 (默认)' )
    cmds.menuItem( 'Object Axis' ,label=u'物体坐标轴' )
    cmds.menuItem( 'Lowest Position' ,label=u'物体最低点' )

    # cmds.radioCollection( "Axis_Type" )
    # cmds.radioButton( "LowestPosition" , label='Lowest Position' , sl = 1 )
    # cmds.radioButton( "Object_Axis" , label='Object Axis' )
    # cmds.radioCollection( "Axis_Type", edit=True, select="LowestPosition" ) #set default
    Question_Button( 'Question_Window( 3 )' , 145)
    cmds.setParent('..')

    cmds.rowLayout(nc=8 , h = 30)
    RowCounter = UIserial( RowCounter )
    cmds.text(l = u"查找其他顶点  ")
    cmds.checkBox( 'Check_Other_Point' , l = '',  value = True )
    cmds.text(l="   ")
    cmds.text(l = u"顶点查找范围 : ")
    cmds.floatField("PointCheckThreshold" , min=0.0 , value = 1.000 )
    Question_Button( 'Question_Window( 4 )' , 116)
    cmds.setParent('..')

    cmds.rowLayout(nc=6 , h = 30)
    RowCounter = UIserial( RowCounter )
    cmds.text(l = u"每一个物体位移后刷新一次视窗 (只是给点视觉效果玩玩): ")
    cmds.checkBox( 'Refresh_Viewport_each_Move' , l = '',  value = False )
    cmds.setParent('..')

    #temporarily---------<
    # cmds.rowLayout(nc=6 , h = 30)
    # RowCounter = UIserial( RowCounter )
    # cmds.text(l = "Faster Result (temporarily because I didn't optimize some code): ")
    # cmds.checkBox( 'Faster_Result' , l = '',  value = False )
    # cmds.setParent('..')
    #temporarily--------->

    cmds.rowLayout(nc=6 , h = 30)
    RowCounter = UIserial( RowCounter )
    cmds.button(c=lambda *args: Snap_To_Ground_Main() , l=u"执行", w=150)
    cmds.setParent('..')

global Question_Window_image_path 
Question_Window_image_path = os.path.join(os.path.dirname(__file__), 'Question_Snap_To_Ground')
Snap_To_Ground_GUI()