import time
import math
import bluepy
from bluepy.bluepy import sensortag

MAGNETIC_DECLINATION = 2.0 # Zürich CH

print "=== init"
tag = sensortag.SensorTag('XX:XX:XX:XX:XX:XX')

time.sleep(1.0)
tag.magnetometer.enable()

max_x = -5000
max_y = -5000
min_x = 5000
min_y = 5000

for i in range(15):
    tag.waitForNotifications(0.1)
    x,y,z = tag.magnetometer.read()
    if x != 0.0 and y != 0.0 and z != 0.0:
        break

print "=== calibrate"
for i in range(90):
    tag.waitForNotifications(0.1)
    x,y,z = tag.magnetometer.read()
    if x > max_x:
        max_x = x
    if x < min_x:
        min_x = x
    if y > max_y:
        max_y = y
    if y < min_y:
        min_y = y
    print (max_x,min_x,max_y,min_y)

ax = (max_x + min_x)/2.0
ay = (max_y + min_y)/2.0

print "=== run"
for i in range(150):
    tag.waitForNotifications(1.0)
    x,y,z = tag.magnetometer.read()
    if(MAGNETIC_DECLINATION > 0):
        azimuth = 180 * math.atan2(x-ax,y-ay)/math.pi + MAGNETIC_DECLINATION
    else:
        azimuth = 180 * math.atan2(x-ax,y-ay)/math.pi - MAGNETIC_DECLINATION
    if azimuth < 0:
        azimuth += 360
    print azimuth
tag.disconnect()
del tag
