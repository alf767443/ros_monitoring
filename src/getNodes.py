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

        # Creates the publisher of the messages
        try:
            self.message_pub = rospy.Publisher("nodesStatus", NodesInformation, queue_size=10)
        except Exception as e:
            rospy.logerr("Failure to create publisher")
            rospy.logerr("An exception occurred:", type(e).__name__,e.args)


        data = []
        master = rosgraph.Master('/rosnode')
        print('---------------------')
        print(master)
        while not rospy.is_shutdown():  
            try:
                node_list = rosnode.get_node_names()
                print('---------------------')
                print(node_list)
                for node in node_list:
                    print('---------------------')
                    print(node)
                    node_api = rosnode.get_api_uri(master, node)
                    print('---------------------')
                    print(node_api)
                    node_info_msg = self.parsecNodeInfo(msg=rosnode.get_node_info_description(node))
                print(data)
            except Exception as e:
                print(e)
            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            rospy.sleep(1)

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
            # Set node message values
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
