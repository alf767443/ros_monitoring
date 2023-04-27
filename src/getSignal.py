#!/usr/bin/env python3

from tcppinglib import async_tcpping, models
from ros_monitoring.msg import SignalInformation, Info_ping

import rospy, asyncio

from pingList import IP2PING

class getSignal:
    def __init__(self) -> None:
        # Start the node
        rospy.init_node('getConnectionStatus', anonymous=False)

        # Creates the publisher of the messages
        try:
            self.message_pub = rospy.Publisher("connectionStatus", SignalInformation, queue_size=10)
        except Exception as e:
            rospy.logerr("Failure to create publisher")
            rospy.logerr("An exception occurred:", type(e).__name__,e.args)

        # Set the asynchronous loop
        try:
            self.loop = asyncio.get_event_loop()
        except:
            rospy.logerr("Failure to asynchronous loop")
            rospy.logerr("An exception occurred:", type(e).__name__,e.args)
        
        # Create the global lists
        try: 
            # Copy the list of ips and settings defined in the pingList file
            self.ip_list = IP2PING.copy()
            # Creates an empty list to store the messages
            self.msg_list = []
            # Create an empty list for asynchronous tasks
            self.ping_tasks = {}
            # Add verification keys to the lists of ips and messages
            for i in range(0,len(self.ip_list)):
                # Add an ID key in the list of ips and configurations
                self.ip_list[i].update({'_id': i})
                # Links the same key to the list of messages
                self.msg_list.append({'_id': i})
                rospy.loginfo("Ping to: " + self.ip_list[i]['ip'] + ':' + str(self.ip_list[i]['port']))
        except:
            rospy.logerr("Failure to create the global lists")
            rospy.logerr("An exception occurred:", type(e).__name__,e.args)
        
        # Launches the ping_ips task asynchronously
        try:
            asyncio.run(self.ping_ips(self.ip_list))
        except:
            rospy.logerr("Error on launch task asynchronously")
            rospy.logerr("An exception occurred:", type(e).__name__,e.args)

        # Keeps the no alive
        rospy.spin()

# Function to ping against defined ips
    async def ping(self, ip_dict: dict):
        try:
            # Ping against ip_dict settings asynchronously
            aping = await async_tcpping(
                address=ip_dict['ip'], 
                port=ip_dict['port'],
                timeout=ip_dict['timeout'],
                count=ip_dict['count'],
                interval=ip_dict['interval'])
            # Adds the ROS Info_ping message to the message list for the ip
            self.msg_list[ip_dict['_id']].update({'msg': self.ping2msg(ping=aping)})
            # Publishes the updated message to the ROS publisher
            await self.publish()
        except Exception as e:
            rospy.logerr("Error on ping to " + ip_dict['ip'] + ':' + str(ip_dict['port']))
            rospy.logerr("An exception occurred:", type(e).__name__,e.args)
        finally:
            # Wait one more interval cycle to release finish the function
            await asyncio.sleep(delay=ip_dict['interval'])
            # Add to ip_list the dictionary that was removed
            self.ip_list.append(ip_dict)
            # Deletes the task from the task list
            del self.ping_tasks[ip_dict['_id']]

# Converts the ping values to the ROS message Info_ping
    def ping2msg(self, ping: models.TCPHost):
        try:
            # Starts the message
            _msg = Info_ping()
            # Fill in the message
            _msg.is_alive = int(ping.is_alive)
            _msg.packets_sent = int(ping.packets_sent)
            _msg.packets_loss = int(ping.packet_loss)
            _msg.packets_received = int(ping.packets_received)
            _msg.port = ping.port
            _msg.rtt_max = ping.max_rtt
            _msg.rtt_min = ping.min_rtt
            _msg.rtt_avg = ping.avg_rtt
            _msg.ip_target = ping.ip_address
            # Returns the converted message
            return _msg
        except Exception as e:
            rospy.logerr("Error on convert ping to message: " + ping.ip_address + ':' + ping.port)
            rospy.logerr("An exception occurred:", type(e).__name__,e.args)

# Publishes the ROS SignalInfomation message to the defined topic via the publisher
    async def publish(self):
        try:
            # Initiates the SignalInformation message 
            _msg = SignalInformation()
            # Start an empty list of Info_ping messages
            msg = [message['msg'] for message in self.msg_list]
            # Fills the msg list with the messages in the list self.msg_list
            # for item in self.msg_list:
                # Adds the message to the _msg list
                # msg.append(item['msg'])
            # Adds the message list to the ping field in the ROS message
            _msg.list = msg
        except Exception as e:
            rospy.logerr("Error on convert ROS message")
            rospy.logerr("An exception occurred:", type(e).__name__,e.args)
        
        # Publishes the message to the publisher
        try:    
            self.message_pub.publish(_msg)
        except Exception as e:
            rospy.logerr("Error on publish the message")
            rospy.logerr("An exception occurred:", type(e).__name__,e.args)
        

# Performs a read of the listed ips
    async def ping_ips(self, ip_list):
        # Keeps the loop going as long as ROS core is running
        while not rospy.is_shutdown():
            # For all items of ip_list
            for item in self.ip_list:
                try:
                    # If no ping task exists for the _id of item create a task
                    if item['_id'] not in self.ping_tasks:
                        # Create a ping job for the item
                        self.ping_tasks[item['_id']] = asyncio.ensure_future(self.ping(ip_dict=item))
                        # Remove item from ip_list to decrease operations
                        self.ip_list.remove(item)
                except Exception as e:
                    rospy.logerr("Error create the ping task to " + item['ip'] + ':' + str(item['port']))
                    rospy.logerr("An exception occurred:", type(e).__name__,e.args)
                
            # Wait 0.1 s to start a new round of forcing so as not to overload processing
            await asyncio.sleep(0.1)

# On program interruption terminates asynchronous tasks
    def __del__(self):
        self.loop.stop()
        rospy.rospy.loginfo("Interrupted asynchronous tasks")
        

if __name__ == '__main__':
    try:
        getSignal()
    except rospy.ROSInterruptException:
        pass
