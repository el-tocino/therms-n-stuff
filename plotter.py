import sys
import time
import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pylab
import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd= 'root', db='temps')
cur = conn.cursor()
sensorsql = "select name, sensor from sensors"
cur.execute(sensorsql)
sensors = cur.fetchall()

tempcount = int(sys.argv[1])
pngfile = sys.argv[2]

for names in sensors:
    x_val = [] ;
    y_val = [] ;
    sensor = str(names[1])
    sensorname = str(names[0])
    sql = "SELECT time , temperature from temperatures where sensor=%s order by time desc limit %s"
    cur.execute(sql, (sensor,tempcount))
    data = cur.fetchall()
    for linez in data:
        the_date = str(linez[0])
        x_val.append(time.mktime(datetime.datetime.strptime(the_date, "%Y-%m-%d %H:%M:%S").timetuple()));
        y_val.append(float(linez[-1]));
        #print (the_date, x_val[-1], y_val[-1])
     
    plt.plot(x_val,y_val, label=sensorname)
    #print "done plotting %s!",sensorname

conn.close

x_label=time.ctime()

plt.xticks([])
plt.xlabel(x_label)
plt.ylabel('Temperature')
plt.legend()
plt.savefig(pngfile)
