from pyorbital.orbital import Orbital, get_observer_look
from datetime import datetime, timedelta, date
import time
from numpy import fabs
import re
from sites import BLE, CAV, CLR, COD, EGL, FYL, THL
from getTLE import getTLE
import pandas as pd

# SITE = [lat(N), long(E), alt(km), horizon(deg), begin coverage (closest to zero), end coverage, begin coverage, end coverage(closest to 360), site name]


def get_site_passes(satno, site, duration, filename):  # Duration in hours from current time,  # filename = file with TLEs in it
    now = datetime.utcnow()  # set time to current time
    sat = Orbital(satellite='None', line1=getTLE(satno, filename)[0], line2=getTLE(satno, filename)[1])
    x = Orbital.get_next_passes(sat, now, duration, site[1], site[0], site[2], tol=0.001, horizon=site[3])  # builds list of all passes that break 3 degrees
    passes = []  # begins empty list for passes
    s = pd.DataFrame(columns=['Site', 'PassStart', 'EnterAz', 'Length'])  # initial dataframe build

    for i in x:
        en = Orbital.get_observer_look(sat, i[0], site[1], site[0], site[2])  # Gets entry Az & El at 3 degree entry
        ex = Orbital.get_observer_look(sat, i[1], site[1], site[0], site[2])  # Gets exitAz & El at 3 degree exit
        hi = Orbital.get_observer_look(sat, i[2], site[1], site[0], site[2])  # Gets exitAz & El for entire pases *even outside fences*
        p1 = Orbital.get_observer_look(sat, i[0], site[1], site[0], site[2])[0]  # az at 3 degree entry
        p2 = Orbital.get_observer_look(sat, i[0] + timedelta(seconds=1), site[1], site[0], site[2])[0]  # p1 1 seconds later
        p3 = Orbital.get_observer_look(sat, i[1], site[1], site[0], site[2])[0]  # az at 3 degree exit

        if site[4] < en[0] < site[5] or site[6] < en[0] < site[7]:  # if satellite enters FOV on face *checkpass*
            len = int((i[1] - i[0]).total_seconds())  # length of pass in seconds
            s = s.append({'Site': site[8], 'PassStart': i[0], 'EnterAz': en[0], 'Length': len}, ignore_index=True)  # adds pass to dataframe

        elif not site[4] < en[0] < site[5]:  # if enters FOV not on face1

            if (p1 - p2) < 0:  # if the azimuth is growing after 5 seconds
                rx = i[0]  # req'd  since i[0] can't be added to later

                while p1 <= site[6]:  # looks for when azimuth breaches sides of coverage
                    p1 = Orbital.get_observer_look(sat, rx, site[1], site[0], site[2])[0]  # gets new azimuth after rx added seconds
                    rx = rx + timedelta(seconds=10)  # sets time for 10s later to retrieve azimuth at that time
                len = int((i[1] - i[0]).total_seconds())
                s = s.append({'Site': site[8], 'PassStart': rx, 'EnterAz': p1, 'Length': len}, ignore_index=True)  # adds pass to dataframe

            if (p1 - p2) > 0:  # if the azimuth is shrinking after 5 seconds
                rx = i[0]  # req'd  since i[0] can't be added to later

                while p1 >= site[6]:  # looks for when azimuth breaches sides of coverage
                    p1 = Orbital.get_observer_look(sat, rx, site[1], site[0], site[2])[0]  # gets new azimuth
                    rx = rx + timedelta(seconds=10)
                len = int((i[1] - rx).total_seconds())  # length of pass in seconds
                s = s.append({'Site': site[8], 'PassStart': rx, 'EnterAz': p1, 'Length': len}, ignore_index=True)  # adds pass to dataframe

        elif not site[6] < en[0] < site[7]:  # if enters FOV not on face2

            if (p1 - p2) < 0:  # if the azimuth is growing after 5 seconds
                rx = i[0]  # req'd  since i[0] can't be added to later

                while p1 <= site[6]:  # looks for when azimuth breaches sides of coverage
                    p1 = Orbital.get_observer_look(sat, rx, site[1], site[0], site[2])[0]  # gets new azimuth
                    rx = rx + timedelta(seconds=10)  # sets time for 10s later to retrieve azimuth at that time
                len = int((i[1] - rx).total_seconds())  # length of pass in seconds
                s = s.append({'Site': site[8], 'PassStart': rx, 'EnterAz': p1, 'Length': len}, ignore_index=True)  # adds pass to dataframe

            if (p1 - p2) > 0:  # if the azimuth is shrinking after 5 seconds
                rx = i[0]  # req'd  since i[0] can't be added to later

                while p1 >= site[6]:  # looks for when azimuth breaches sides of coverage
                    p1 = Orbital.get_observer_look(sat, rx, site[1], site[0], site[2])[0]  # gets new azimuth
                    rx = rx + timedelta(seconds=10)  # sets time for 10s later to retrieve azimuth at that time
                len = int((i[1] - rx).total_seconds())  # length of pass in seconds
                s = s.append({'Site': site[8], 'PassStart': rx, 'EnterAz': p1, 'Length': len}, ignore_index=True)

    s = s.drop(s[s.Length < 0].index)
    return s
