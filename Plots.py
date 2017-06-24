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

for names in sensors:
    x_val = [] ;
    y_val = [] ;
    sensor = str(names[1])
    sensorname = str(names[0])
    sql = "SELECT time , temperature from temperatures where sensor=%s order by time desc limit 40"
    cur.execute(sql, sensor)
    data = cur.fetchall()
    for linez in data:
        the_date = str(linez[0])
        x_val.append(time.mktime(datetime.datetime.strptime(the_date, "%Y-%m-%d %H:%M:%S").timetuple()));
        y_val.append(float(linez[-1]));
        print (the_date, x_val[-1], y_val[-1])
     
    plt.plot(x_val,y_val, label=sensorname)
    print "done plotting %s!",sensorname

conn.close

plt.xlabel('Time')
plt.ylabel('Temperature')
plt.legend()
plt.savefig('foo.png')
