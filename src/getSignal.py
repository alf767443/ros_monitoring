#!/usr/bin/env python3

from GlobalSets.Mongo import DataSource as Source, Clients, DataBases as db, Collections as col
from GlobalSets.localSave import createFile
from tcppinglib import tcpping

import rospy, bson
import datetime

dataPath = {
    'dataSource': Source.CeDRI_UGV, 
    'dataBase'  : db.dataLake,
    'collection': col.Connection
}

class getSignal:
    def __init__(self) -> None:
        rospy.init_node('getSignal', anonymous=False)
        rate = rospy.Rate(1)
        while not rospy.is_shutdown():
            try:
                (isAlive , RTT) = self.getInfo(ip=Clients.ip, port=Clients.port)
                data = {
                    'dateTime': datetime.datetime.now(),
                    'Connect': isAlive,
                    'RTT': RTT
                }
                
                createFile(dataPath=dataPath, content=data) 
            except Exception as e:
                print(e)
            rate.sleep()

    def getInfo(self, ip: str, port: int):
        try:
            ping = tcpping(address=ip, port=port, interval=1, timeout=2, count=5)
        except Exception as e:
            print(e)
        return(ping.is_alive, ping.avg_rtt)

if __name__ == '__main__':
    try:
        getSignal()
    except rospy.ROSInterruptException:
        pass
