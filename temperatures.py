#!/usr/bin/python
import os
import glob
import time
import pymysql

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

while True:
        for name in glob.glob(base_dir + '28*'):
            device_file = name + '/w1_slave'
            temp_c = read_temp()
            sensorid = name[-12:]
            conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='temps')
            cur = conn.cursor()
            sql = "INSERT into temperatures (sensor, time, temperature) values (%s, now(), %s) "
            cur.execute(sql, (sensorid,  str(round(temp_c,2))))
            conn.commit()
            conn.close
        time.sleep(10)
            
