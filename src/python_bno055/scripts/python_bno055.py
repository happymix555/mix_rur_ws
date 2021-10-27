#!/usr/bin/env python3

from bno055_usb_stick_py import BnoUsbStick
from sensor_msgs.msg import Imu
import rospy

def pub_bno055_imu():

    #set param
    frequency = 20
    frame_id = 'imu_link'
    imu_data_seq_counter = 0 #always set to 0

    rospy.init_node('imu_bno055_node', anonymous=False)

    bno_usb_stick = BnoUsbStick()
    bno_usb_stick.activate_streaming()
    rate = rospy.Rate(frequency)

    imu_publisher = rospy.Publisher('imu/data', Imu, queue_size=1)

    while not rospy.is_shutdown():
        packet = bno_usb_stick.recv_streaming_packet()
        quaternion = packet.quaternion
        linear_acceleration = packet.lin_a
        gyroscope = packet.g
        imu_data = Imu()  

        imu_data.header.stamp = rospy.Time.now()
        imu_data.header.frame_id = frame_id
        imu_data.header.seq = imu_data_seq_counter

        imu_data.orientation.w = quaternion[0]
        imu_data.orientation.x = quaternion[1]
        imu_data.orientation.y = quaternion[2]
        imu_data.orientation.z = quaternion[3]

        imu_data.linear_acceleration.x = linear_acceleration[0]
        imu_data.linear_acceleration.y = linear_acceleration[1]
        imu_data.linear_acceleration.z = linear_acceleration[2]

        imu_data.angular_velocity.x = gyroscope[0]
        imu_data.angular_velocity.y = gyroscope[1]
        imu_data.angular_velocity.z = gyroscope[2]

        imu_data.orientation_covariance[0] = -1
        imu_data.linear_acceleration_covariance[0] = -1
        imu_data.angular_velocity_covariance[0] = -1

        imu_data_seq_counter=+1

        imu_publisher.publish(imu_data)

        rate.sleep()

if __name__ == '__main__':
    pub_bno055_imu()
    # try:
    #     pub_bno055_imu()
    # except:
    #     rospy.logerr('Something wrong with bno055 node')
        

