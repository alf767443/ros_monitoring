#!/usr/bin/env python3

from tcppinglib import async_tcpping, models
from ros_monitoring.msg import SignalInformation

import rospy, asyncio

from pingList import IP2PING

class getSignal:
    def __init__(self) -> None:
        rospy.init_node('getConnectionStatus', anonymous=False)
        pub = rospy.Publisher("connectionStatus", SignalInformation, queue_size=10)
        rate = rospy.Rate(1)
        
        for ip in IP2PING:
            asyncio.ensure_future(self.ping(ip_dict=ip))

        rospy.spin()
            

    async def ping(self, ip_dict: dict):
        try:
            aping = await async_tcpping(
                address=ip_dict['ip'], 
                port=ip_dict['port'],
                timeout=ip_dict['timeout'],
                count=ip_dict['count'],
                interval=ip_dict['interval'])
            self.ping2msg(ping=aping)
            self.ping(ip_dict=ip_dict)
        except Exception as e:
            print(e)

    def ping2msg(self, ping: models.TCPHost,publisher: rospy.Publisher):
        try:
            _msg = SignalInformation()
            _msg.is_alive = ping.is_alive
            _msg.packets_sent = ping.packets_sent
            _msg.packet_loss = ping.packet_loss
            _msg.packets_received = ping.packets_received
            _msg.port = ping.port
            _msg.max_rtt = ping.max_rtt
            _msg.min_rtt = ping.min_rtt
            _msg.avg_rtt = ping.avg_rtt
            _msg.ip_address = ping.ip_address
            
            publisher.publish(_msg)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    try:
        getSignal()
    except rospy.ROSInterruptException:
        pass
