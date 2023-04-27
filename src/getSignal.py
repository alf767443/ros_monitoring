#!/usr/bin/env python3

from tcppinglib import async_tcpping, models
from ros_monitoring.msg import SignalInformation

import rospy, asyncio

from pingList import IP2PING

class getSignal:
    def __init__(self) -> None:
        rospy.init_node('getConnectionStatus', anonymous=False)
        self.pub = rospy.Publisher("connectionStatus", SignalInformation, queue_size=10)
        self.loop = asyncio.get_event_loop()
        print(1)
        # Inicia a tarefa assíncrona
        self.loop.create_task(self.ping_ips(IP2PING))
        print(2)
        rospy.spin()

    async def ping(self, ip_dict: dict):
        try:
            print(3)
            aping = await async_tcpping(
                address=ip_dict['ip'], 
                port=ip_dict['port'],
                timeout=ip_dict['timeout'],
                count=ip_dict['count'],
                interval=ip_dict['interval'])
            print(4)
            self.ping2msg(ping=aping, publisher=self.pub)
            print(44)
        except Exception as e:
            print(e)

    def ping2msg(self, ping: models.TCPHost, publisher: rospy.Publisher):
        try:
            print(5)
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
            print(6)
            publisher.publish(_msg)
            print(7)
        except Exception as e:
            print(e)

    async def ping_ips(self, ip_list):
        for ip in ip_list:
            print(0)
            await self.ping(ip_dict=ip)
            print(101)
            await asyncio.sleep(0.1)
        print(111)

if __name__ == '__main__':
    try:
        getSignal()
    except rospy.ROSInterruptException:
        pass
