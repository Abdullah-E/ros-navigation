#!/usr/bin/env python3

import time
import robomaster
from robomaster import robot

import rospy
from nav_msgs.msg import Odometry

import numpy as np

def euler_to_quaternion(yaw, pitch, roll):

        qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
        qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
        qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
        qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

        return [qx, qy, qz, qw]

class OdomPublisher:
	def __init__(self):
		ep_robot = robot.Robot()
		ep_robot.initialize(conn_type="rndis")
		ep_chassis = ep_robot.chassis
		ep_chassis.sub_attitude(freq=5, callback=self.sub_att_cb)
		
		rospy.init_node('odom_publisher', anonymous=True)
		self.odom_pub = rospy.Publisher('odom', Odometry, queue_size=10)
	
		self.rate = rospy.Rate(10)
		self.quarts = [0,0,0,0]
	def sub_att_cb(self, att_info):
		yaw, pitch, roll = att_info
		self.quarts = euler_to_quaternion(yaw, pitch, roll)	
	def publish(self):
		odom = Odometry()
		odom.pose.pose.orientation.x = self.quarts[0]
		odom.pose.pose.orientation.y = self.quarts[1]
		odom.pose.pose.orientation.y = self.quarts[2]
		odom.pose.pose.orientation.y = self.quarts[3]
		
		self.odom_pub.publish(odom)
		self.rate.sleep()
	def spin(self):
		while not rospy.is_shutdown():
			self.publish()

if __name__ == '__main__':
	try:
		odom_node = OdomPublisher()
		odom_node.spin()
	except rospy.ROSInterruptException:
		pass
