#!/usr/bin/env python3
from tcppinglib import tcpping
from ros_monitoring.msg import NodesInformation, Info_node, TopicInfo

import rospy, bson, rosnode, rosgraph
from datetime import datetime
import re

class getNodes:
    def __init__(self) -> None:
        # Start the node
        rospy.init_node('getROSNodes', anonymous=False)
        rate = rospy.Rate(1)
        # Creates the publisher of the messages
        try:
            self.message_pub = rospy.Publisher("nodesStatus", NodesInformation, queue_size=10)
        except Exception as e:
            rospy.logerr("Failure to create publisher")
            rospy.logerr("An exception occurred:", type(e).__name__,e.args)

        while not rospy.is_shutdown():
            # Get ROS nodes
            try:
                node_list = rosnode.get_node_names()
            except Exception as e:
                rospy.logerr("Error on get ROS nodes")
                rospy.logerr("An exception occurred:", type(e).__name__,e.args)
            # Parsec the ROS nodes
            nodes = []
            for node in node_list:
                try:
                    nodes.append(self.parsecNodeInfo(msg=rosnode.get_node_info_description(node)))
                except Exception as e:
                    rospy.logerr("Error in the node parsec info:" + str(node))
                    rospy.logerr("An exception occurred:", type(e).__name__,e.args)
                    
            # Create the topic message
            try:
                # Starts the message
                msg = NodesInformation()
                # Fill in the message
                msg.nodes = nodes
            except Exception as e:
                rospy.logerr("Error on create the message")
                rospy.logerr("An exception occurred:", type(e).__name__,e.args)
            # Publish ROS message
            self.message_pub.publish(msg)
            rate.sleep()
        # Keeps the node alive
        rospy.spin()




# Function to parsec the node informarion
    def parsecNodeInfo(self, msg):
        # Parsec node infomation
        try:
            # Get node name
            node_name = re.search(r"Node \[(.*)\]", msg).group(1)
            # Get publications
            pubs = re.findall(r"\* (.*) \[(.*)\]", re.search(r"Publications:(.*)Subscriptions", msg, re.DOTALL).group(1))
            # publications = [{"topic": topic, "type": msg_type} for topic, msg_type in pubs]
            publications = [self.topic2msg({"topic": topic, "type": msg_type}) for topic, msg_type in pubs]
            # Get subscriptions
            subs = re.findall(r"\* (.*) \[(.*)\]", re.search(r"Subscriptions:(.*)Services", msg, re.DOTALL).group(1))
            # subscriptions = [{"topic": topic, "type": msg_type} for topic, msg_type in subs]
            subscriptions = [self.topic2msg({"topic": topic, "type": msg_type}) for topic, msg_type in subs]
            # Get services
            services = re.findall(r"\* (.*)", re.search(r"Services:(.*)", msg, re.DOTALL).group(1))
        except Exception as e:
            rospy.logerr("Error on node parsec: " + str(msg))
            rospy.logerr("An exception occurred:", type(e).__name__,e.args)
        # Convert to Info_node ROS message
        try:
            # Starts the message
            _msg = Info_node()
            # Fill in the message
            _msg.node = str(node_name)
            _msg.publications = publications
            _msg.subscriptions = subscriptions
            _msg.services = services
            return _msg
            # Fill in the message
        except Exception as e:
            rospy.logerr("Error on convert node to message: " + str(msg))
            rospy.logerr("An exception occurred:", type(e).__name__,e.args)

# Converts the topic information to ROS message TopicInfo
    def topic2msg(self, msg):
        try:
            # Starts the message
            _msg = TopicInfo()
            # Fill in the message
            _msg.topic = str(msg['topic'])
            _msg.msg_type = str(msg['type'])
            # Returns the converted message
            return _msg
        except Exception as e:
            rospy.logerr("Error on convert topic to message: " + str(msg))
            rospy.logerr("An exception occurred:", type(e).__name__,e.args)
        

if __name__ == '__main__':
    try:
        getNodes()
    except rospy.ROSInterruptException:
        pass
