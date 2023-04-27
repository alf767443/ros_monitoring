#!/usr/bin/env python3

from tcppinglib import async_tcpping, models
from ros_monitoring.msg import SignalInformation, Info_ping

import rospy, asyncio

from pingList import IP2PING

class getSignal:
    def __init__(self) -> None:
        rospy.init_node('getConnectionStatus', anonymous=False)
        self.pub = rospy.Publisher("connectionStatus", SignalInformation, queue_size=10)
        self.loop = asyncio.get_event_loop()
        self.ip_list = IP2PING.copy()  # Armazena a lista de IPs a serem pingados
        self.msg_list = [{}]


        for i in range(0,len(self.ip_list)):
            self.ip_list[i].update({'_id': i})
            self.msg_list.append({'_id': i})
            print(self.ip_list[i])

        self.ping_tasks = {}  # Dicionário que mapeia os IPs para as tarefas de ping

        print(1)
        
        asyncio.run(self.ping_ips(self.ip_list))  # Inicia a tarefa assíncrona para pingar os IPs
        asyncio.run(self.publish())
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
            self.msg_list[ip_dict['_id']].update({'msg': self.ping2msg(ping=aping, publisher=self.pub)})
            print(55)
            await asyncio.sleep(delay=ip_dict['interval'])
            print(555)
            self.ip_list.append(ip_dict)
        except Exception as e:
            print(e)
        finally:
            del self.ping_tasks[ip_dict['_id']]  # Remove a tarefa do dicionário de tarefas de ping

    def ping2msg(self, ping: models.TCPHost, publisher: rospy.Publisher):
        try:
            print(6)
            _msg = Info_ping()
            _msg.is_alive = int(ping.is_alive)
            _msg.packets_sent = int(ping.packets_sent)
            _msg.packets_loss = int(ping.packet_loss)
            _msg.packets_received = int(ping.packets_received)
            _msg.port = ping.port
            _msg.rtt_max = ping.max_rtt
            _msg.rtt_min = ping.min_rtt
            _msg.rtt_avg = ping.avg_rtt
            _msg.ip_target = ping.ip_address
            print(7)
            return _msg
        except Exception as e:
            print(e)

    async def publish(self):
        while not rospy.is_shutdown():  # Exec
            print(12)
            _msg = SignalInformation()
            print(120)
            _msg.ping
            print(1200)
            msg = []
            print(12000)
            for i in self.msg_list:
                print(121)
                msg.append(i['msg'])
                print(i)
            print(12021)
            _msg.ping = msg
            print(120210)
            self.pub.publish(_msg)
            print(120212)
            asyncio.sleep(1)


    async def ping_ips(self, ip_list):
        while not rospy.is_shutdown():  # Executa enquanto o roscore estiver ativo
            for ip in self.ip_list:
                print(ip)
                if ip['_id'] not in self.ping_tasks:
                    print(8)
                    self.ping_tasks[ip['_id']] = asyncio.ensure_future(self.ping(ip_dict=ip))
                    self.ip_list.remove(ip)
                    print(9)
                print(99)
            await asyncio.sleep(0.1)
        
    def __del__(self):
        self.loop.stop()

if __name__ == '__main__':
    try:
        getSignal()
    except rospy.ROSInterruptException:
        pass
