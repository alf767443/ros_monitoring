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
        self.ip_list = IP2PING.copy()  # Armazena a lista de IPs a serem pingados
        # self.ping_tasks = {}  # Dicionário que mapeia os IPs para as tarefas de ping

        print(1)
        
        asyncio.run(self.ping_ips(self.ip_list))  # Inicia a tarefa assíncrona para pingar os IPs
        
        
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
            await self.ping(ip_dict=ip_dict)
            print(5)
            self.ping2msg(ping=aping, publisher=self.pub)
            print(55)
            await asyncio.sleep(delay=ip_dict['interval'])
            print(555)
            self.ip_list.append(ip_dict)
        except Exception as e:
            print(e)

    def ping2msg(self, ping: models.TCPHost, publisher: rospy.Publisher):
        try:
            print(6)
            _msg = SignalInformation()
            _msg.is_alive = int(ping.is_alive)
            _msg.packets_sent = ping.packets_sent
            _msg.packets_loss = int(ping.packet_loss)
            _msg.packets_received = ping.packets_received
            _msg.port = ping.port
            _msg.rtt_max = ping.max_rtt
            _msg.rtt_min = ping.min_rtt
            _msg.rtt_avg = ping.avg_rtt
            _msg.ip_target = ping.ip_address
            print(7)
            publisher.publish(_msg)
        except Exception as e:
            print(e)

    async def ping_ips(self, ip_list):
         while not rospy.is_shutdown():  # Executa enquanto o roscore estiver ativo
            for ip in self.ip_list:
                await self.ping(ip_dict=ip)
                self.ip_list.remove(ip)
            await asyncio.sleep(0.1)
        
    def __del__(self):
        self.loop.stop()

if __name__ == '__main__':
    try:
        getSignal()
    except rospy.ROSInterruptException:
        pass
