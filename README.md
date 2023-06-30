
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
This package is intended to get the running nodes and connections between them. Publishing a message of type *NodesInformation* from *ros_monitoring*, in the publisher */nodesStatus* 

## Published information (*/nodesStatus*)

The information published by this node is as follows:

    {
	    nodes: 	[{
		    node: -- node name.................as string
		    publications: [{
			    topic:    -- topic name....as string
			    msg_type: -- message type..as string
		    }, ...],
		    subscriptions: [{
			    topic:    -- topic name....as string
			    msg_type: -- message type..as string
		    }, ...],
		    services: [ -- node name...........as string, ...]
	    }, ...]
    }

# Get the connection with an IP and port (*getSignal.py*)

This topic should get the connection status between the computer running ROS, with other IPs pings periodically. The information is published in a message of type *SignalInformation* from *ros_monitoring* in the publisher */connectionStatus*.

## pinglist (*pingList.py*)

To configure which IPs the node will ping, you must edit the file *pingList.py*, which is a dictionary in the following format:

    {	
	    'ip': 	    -- IP to ping......as string
	    'port': 	    -- Port to ping....as integer
		'interval': -- Ping interval...as integer
		'timeout':  -- Timeout ping....as integer
		'count':    -- Number of trys..as integer
	}

## Published information (*/connectionStatus*)

The information published by this node is as follows:

    {
	    Info_ping: [{
		    is_alive: 	  	  -- The status of connection...as integer
			packets_sent: 	  -- Number of sent packets.....as integer
			packets_loss: 	  -- Number of loss packets.....as integer
			packets_received: -- Number of received packets.as integer
			port:	          -- Port it was sent to........as integer
			rtt_max:	  -- Maximum connection RTT.....as float
			rtt_min:	  -- Minimum connection RTT.....as float
			rtt_avg:	  -- Average connection RTT.....as float
			ip_target:	  -- IP it was ping.............as string
			}, ...]
	 }

# More information

This package was developed as part of the thesis for a Master in Industrial Engineering with a specialization in Electrical Engineering at the Polytechnic Institute of Bragança (_IPB_), the work was developed at the Research Centre in Digitalization and Intelligent Robotics (_CeDRI_).
The project consists of three repositories with the links below:
	
>https://github.com/alf767443/node_monitoring

>https://github.com/alf767443/ros_monitoring

>https://github.com/alf767443/UGV-dashboard

>https://github.com/alf767443/UGV-backend
