#!/usr/bin/env python3

from GlobalSets.Mongo import DataSource as Source, Clients, DataBases as db, Collections as col
from GlobalSets.localSave import createFile
from tcppinglib import tcpping

import rospy, bson, rosnode, rosgraph
from datetime import datetime
import re

dataPath = {
    'dataSource': Source.CeDRI_UGV, 
    'dataBase'  : db.dataLake,
    'collection': col.Nodes
}

class getNodes:
    def __init__(self) -> None:
        data = []
        master = rosgraph.Master('/rosnode') 
        _createFile = False
        rospy.init_node('getNodes', anonymous=False)
        rate = rospy.Rate(1)
        while not rospy.is_shutdown():  
            try:
                node_list = rosnode.get_node_names()
                for node in node_list:
                    _node = list(filter(lambda x: x['node'] == node, data))
                    if _node == []:
                        _createFile =True
                        node_api = rosnode.get_api_uri(master, node)
                        (node_name, publications, subscriptions, services) = self.parsecInfo(msg=rosnode.get_node_info_description(node))
                        connection = self.parsecConnection(rosnode.get_node_connection_info_description(node_api, master))
                        bnode = {
                            'node' : node_name,
                            'pubs' : publications,
                            'subs' : subscriptions,
                            'serv' : services, 
                            'conn' : connection
                        }
                        data.append(bnode)
                    else:
                        _createFile =False
                    
                _data = {
                    'nodes': data, 
                    'dateTime': datetime.now()
                    }
                if _createFile: 
                    createFile(dataPath=dataPath, content=_data) 
                    print('create file')
            except Exception as e:
                print(e)
            rate.sleep()
            
        
    
    def parsecConnection(self, msg):
        parsed_data = {}

        pid_match = re.search(r'Pid:\s*(\d+)', msg)
        if pid_match:
            parsed_data['Pid'] = int(pid_match.group(1))

        # Extrai as conexões da msg e armazena no dicionário
        connections_match = re.findall(r'\* topic:\s*(.*?)\n\s+\* to:\s*(.*?)\n\s+\* direction:\s*(.*?)\((\d+)\s-\s(.*?)\)\s\[(\d+)\]\n\s+\* transport:\s*(.*?)\n', msg, re.DOTALL)
        parsed_data['Connections'] = []
        for connection in connections_match:
            parsed_data['Connections'].append({
                'topic': connection[0],
                'to': connection[1],
                'direction': connection[2],
                'port': int(connection[3]),
                'address': connection[4],
                'bytes': int(connection[5]),
                'transport': connection[6]
            })
        return parsed_data

    def parsecInfo(self, msg):
        #Extrai o nome do nó
        node_name = re.search(r"Node \[(.*)\]", msg).group(1)
        # print(msg)
        # Extrai as publicações
        pubs = re.findall(r"\* (.*) \[(.*)\]", re.search(r"Publications:(.*)Subscriptions", msg, re.DOTALL).group(1))
        publications = [{"topic": topic, "type": msg_type} for topic, msg_type in pubs]

        # Extrai as subscrições
        subs = re.findall(r"\* (.*) \[(.*)\]", re.search(r"Subscriptions:(.*)Services", msg, re.DOTALL).group(1))
        subscriptions = [{"topic": topic, "type": msg_type} for topic, msg_type in subs]

        # Extrai os serviços
        services = re.findall(r"\* (.*)", re.search(r"Services:(.*)", msg, re.DOTALL).group(1))
        return (node_name, publications, subscriptions, services)


if __name__ == '__main__':
    try:
        getNodes()
    except rospy.ROSInterruptException:
        pass
