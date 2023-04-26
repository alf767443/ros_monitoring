#!/usr/bin/env python3

# from GlobalSets.Mongo import DataSource as Source, DataBases as db, Collections as col
#
import rospy, bson, rosnode, rosgraph
import psutil, os, json
from datetime import datetime
from ros_monitoring import _process

class getNodes:
    def __init__(self) -> None:
        rospy.init_node('robot_HTOP', anonymous=False)
        pub = rospy.Publisher('pub_HTOP', _process, queue_size = 5)

        rate = rospy.Rate(1)
        while not rospy.is_shutdown():  
            try:           
                process = _process()
                process.cpu_percent = 0.1
                pub.publish(process)
                # data = []
                # process = psutil.process_iter(attrs=['status', 'cpu_num', 'pid', 'memory_full_info', 'cpu_percent', 'username', 'name', 'num_threads', 'memory_percent'])
                # for proc in process:
                #     try:
                #         temp = proc.info
                #     except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                #         pass
                #     else:
                #         data.append(temp)
                # _data = {
                #     'process': data, 
                #     'computer': {                    
                #         'cpu_perc': psutil.cpu_percent(percpu=True),
                #         'memory': psutil.virtual_memory(),
                #         'memory_swap': psutil.swap_memory()
                #     },
                #     'dateTime': datetime.now()
                #     }
                # _data = json.
            except Exception as e:
                print(e)
            for i in range(0,60): rate.sleep()

if __name__ == '__main__':
    try:
        getNodes()
    except rospy.ROSInterruptException:
        pass



