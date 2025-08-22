#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
import math

class RotateRobot:
    def __init__(self):
        self.cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        rospy.Subscriber('/odom', Odometry, self.odom_callback)
        self.rate = rospy.Rate(10)

        self.current_yaw = None
        self.start_yaw = None
        self.target_yaw = None
        self.rotation_done = False
        #self.degrees_to_rotate = 270  # Change this to your desired angle
    
    def shutdownhook(self):
        # works better than the rospy.is_shutdown()
        self.ctrl_c = True

    def odom_callback(self, msg):
        orientation_q = msg.pose.pose.orientation
        (_, _, yaw) = euler_from_quaternion([
            orientation_q.x,
            orientation_q.y,
            orientation_q.z,
            orientation_q.w
        ])
        self.current_yaw = yaw

    def normalize_angle(self, angle):
        return math.atan2(math.sin(angle), math.cos(angle))

    def rotate(self,rotateangle):
        rospy.loginfo("Service Requested.")
        while not rospy.is_shutdown():
            if self.current_yaw is None or self.rotation_done:
                self.rate.sleep()
                continue

            if self.start_yaw is None:
                self.start_yaw = self.current_yaw
                self.target_yaw = self.normalize_angle(self.start_yaw + math.radians(rotateangle))
                rospy.loginfo("Starting rotation from %.2f° to %.2f°",
                              math.degrees(self.start_yaw), math.degrees(self.target_yaw))

            angle_diff = self.normalize_angle(self.target_yaw - self.current_yaw)
            twist = Twist()

            if abs(angle_diff) > math.radians(2):  # 2° tolerance
                if (rotateangle>0):
                    twist.angular.z = 0.5  # rad/s
                    self.cmd_pub.publish(twist)
                else:
                    twist.angular.z = -0.5  # rad/s
                    self.cmd_pub.publish(twist)
            else:
                self.cmd_pub.publish(Twist())  # Stop rotation
                self.rotation_done = True
                rospy.loginfo("Rotation complete.")
                rospy.loginfo("Service completed.")
                #self.shutdownhook()
                break
                #rospy.signal_shutdown("Task completed successfully.")
            self.rate.sleep()
        
        #rospy.signal_shutdown("Rotation done")

        
            
            


if __name__ == '__main__':
    rospy.init_node('rotateangle_robot', anonymous=True)
    robot = RotateRobot()
    try:
        robot.rotate(90)
        rospy.signal_shutdown("Task completed successfully.")
    except rospy.ROSInterruptException:
        pass
    
