#!/usr/bin/env python

import rospy
from my_rb1_ros.srv import Rotate, RotateResponse
from rotate import RotateRobot

def callback(request):
    roateangle = request.degrees
    rotaterobot = RotateRobot()
    rotateresult = rotaterobot.rotate(roateangle)
    response = RotateResponse()
    if(rotateresult):
        rospy.loginfo("Success")
    else:
        rospy.loginfo("Failure")
    #rospy.loginfo(response.result)

rospy.init_node('rotate_service_robot')
rospy.loginfo("Service Ready.")
rotaterobotservice = rospy.Service('/rotate_robot',Rotate,callback)
rospy.spin()