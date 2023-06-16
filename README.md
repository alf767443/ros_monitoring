# ros_monitoring

This ROS package is intended to collect data from topics, transform, store, manage and send them to a MongoDB server. Being designed to maintain the collection even in connection drops with the server.



# Install

To install this ROS package:

	cd ~/catkin_ws/src
	git clone https://github.com/alf767443/ros_monitoring.git
	sudo chmod +x src/get*
	cd ..
	catkin_make

Installation of **node_monitoring** is recommended. Check the link:
>https://github.com/alf767443/node_monitoring.git


# Get the ROS running nodes (*getNodes.py*)

# Get the connection with a IP and port (*getSignal.py*)

## pinglist (*pingList.py*)

# More information

This package was developed as part of the thesis for Master in Industrial Engineering with specialization in Electrical Engineering at Polytechnic Institute of Bragança (_IPB_), the work was developed at the Research Centre in Digitalization and Intelligent Robotics (_CeDRI_).
The project consists of three repositories with the links below:
	
>https://github.com/alf767443/node_monitoring

>https://github.com/alf767443/ros_monitoring

>https://github.com/alf767443/UGV-dashboard
