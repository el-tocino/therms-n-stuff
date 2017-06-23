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
    sensor = str(names[1])
    sensorname = str(names[0])
    sql = "SELECT time , temperature from temperatures where sensor=%s order by time desc limit 10"
    cur.execute(sql, sensor)
    data = cur.fetchall()
    for linez in data:
        print (str(linez[0]),float(linez[1]))

    x_val = [str(x[0]) for x in linez]
    y_val = [float(y[1]) for y in linez]
    plt.plot(x_val,y_val, label='sensorname')
    print "done plotting!"

conn.close

plt.xlabel('Time')
plt.ylabel('Temperature')
plt.savefig('foo.png')
#plt.savefig('foo.png', bbox_inches='tight')

