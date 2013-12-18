#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray

distFromRobotTorso = 0.5
clearanceFromPipe = 0.05
pipeDiam = 0.1
handleHeight = 37.7*0.0254


def pipe_factory(marker, markerid, yLoc):
    marker.header.frame_id = "leftFoot"
    marker.header.stamp = rospy.get_rostime()
    marker.id = markerid
    marker.type = 3
    marker.action = 0
    marker.pose.position.x = distFromRobotTorso
    marker.pose.position.y = yLoc
    marker.pose.position.z = 2.23*0.5

    marker.scale.x = pipeDiam
    marker.scale.y = pipeDiam
    marker.scale.z = 2.35

    marker.color.a = 1.0
    marker.color.r = 0.0
    marker.color.g = 0.0
    marker.color.b = 1.0

    return marker

def handle_factory(marker, markerid, diam, yLoc, Type):
    marker.header.frame_id = "leftFoot"
    marker.header.stamp = rospy.get_rostime()
    marker.id = markerid
    marker.type = 3 
    marker.action = 0
    marker.pose.position.x = distFromRobotTorso - clearanceFromPipe - pipeDiam*0.5
    marker.pose.position.y = yLoc
    marker.pose.position.z = handleHeight

    if(Type == "round"):
        marker.pose.orientation.x = 0.0
        marker.pose.orientation.y = 0.707
        marker.pose.orientation.z = 0.0
        marker.pose.orientation.w = 0.707
    
        marker.scale.x = diam
        marker.scale.y = diam
        marker.scale.z = 0.05

    elif(Type == "lever"):
        length = diam
        marker.pose.position.z = handleHeight+length*0.5
        marker.scale.x = 0.05
        marker.scale.y = 0.05
        marker.scale.z = length
        
    marker.color.a = 1.0
    marker.color.r = 1.0
    marker.color.g = 1.0
    marker.color.b = 1.0

    return marker

def marker_publisher():
    pub1 = rospy.Publisher('pipe_setup', MarkerArray)
    pub2 = rospy.Publisher('handle_setup', MarkerArray)
    rospy.init_node('valve_setup_publisher')

    pipes = MarkerArray()
    leftPipe = pipe_factory(Marker(), 0, -0.7066)
    pipes.markers.append(leftPipe)

    midPipe = pipe_factory(Marker(), 1, 0.0)
    pipes.markers.append(midPipe)

    rightPipe = pipe_factory(Marker(), 2, 0.9652)
    pipes.markers.append(rightPipe)
    

    handles = MarkerArray()
    leftHandle = handle_factory(Marker(), 3, 0.3302, -0.7066, "lever")
    handles.markers.append(leftHandle)

    midHandle = handle_factory(Marker(), 4, 0.4572, 0.0, "round")
    handles.markers.append(midHandle)

    rightHandle = handle_factory(Marker(), 5, 0.2286, 0.9652, "round")
    handles.markers.append(rightHandle)
    
    while not rospy.is_shutdown():
        pub1.publish(pipes)
        pub2.publish(handles)

if __name__ == "__main__":
    try:
        marker_publisher()
    except rospy.ROSInterruptException:
        pass
