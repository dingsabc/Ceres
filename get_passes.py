from pyorbital.orbital import Orbital, get_observer_look
from datetime import datetime, timedelta, date
import time
from numpy import fabs
import re
from sites import BLE, CAV, CLR, COD, EGL, FYL, THL
from getTLE import getTLE


# TODO : Remove prints

# SITE = [lat(N), long(E), alt(km), horizon(deg), begin coverage (closest to zero), end coverage, begin coverage, end coverage(closest to 360)]

def get_site_passes(satno, site, duration, filename):  # Duration in hours from current time,  # filename = file with TLEs in it

    now = datetime.utcnow()  # set time to current time
    sat = Orbital(satellite='None', line1=getTLE(satno, filename)[0], line2=getTLE(satno, filename)[1])
    x = Orbital.get_next_passes(sat, now, duration, site[1], site[0], site[2], tol=0.001, horizon=site[3])  # builds list of all passes that break 3 degrees
    passes = []  # begins empty list for passes
    for i in x:
        print(" ")  # prints empty line (used for dev)

        en = Orbital.get_observer_look(sat, i[0], site[1], site[0], site[2])  # Gets entry Az & El
        ex = Orbital.get_observer_look(sat, i[1], site[1], site[0], site[2])  # Gets exitAz & El
        hi = Orbital.get_observer_look(sat, i[2], site[1], site[0], site[2])  # Gets exitAz & El

        print("Pass Start:", i[0], "Enter Az", en[0], "Pass Term:", i[1], "Exit Az:", ex[0], "MaxEl:", hi[1])  # prints passes (used for dev)

        if site[4] < en[0] < site[5] or site[6] < en[0] < site[7]:  # if satellite enters FOV on face
            print("Check Pass | Az:", en[0])  # prints pass info (used for dev)
            passes.append(i[0])  # appedns check passes to passes list
            print(i[0])  # prints pass info (used for dev)

        elif not site[4] < en[0] < site[5]:  # if enters FOV not on face1
            print("Fence Pass | Az:", ex[0])  # prints pass info (used for dev)
            p1 = Orbital.get_observer_look(sat, i[0], site[1], site[0], site[2])[0]  # az when time enters 3 degree bubble FOV
            p2 = Orbital.get_observer_look(sat, i[0] + timedelta(seconds=5), site[1], site[0], site[2])[0]  # p1 5 seconds later
            start = i[0]  # sets beginning time to pass start time

            if (p1 - p2) < 0:  # if the azimuth is growing after 5 seconds
                rx = i[0]  # Sets variables so it doesn't mess up other operations
                ptmp1 = p1  # Sets variables so it doesn't mess up other operations
                while ptmp1 < site[6]:  # looks for when azimuth breaches sides of coverage
                    ptmp1 = Orbital.get_observer_look(sat, rx, site[1], site[0], site[2])[0]  # gets new azimuth
                    rx = rx + timedelta(seconds=10)  # sets time for 10s later to retrieve azimuth at that time
                print("Fence Time:", rx, "Angle:", p1)  # prints pass info (used for dev)
                passes.append(rx)

            if (p1 - p2) > 0:  # if the azimuth is shrinking after 5 seconds
                rx = i[0]  # Sets variables so it doesn't mess up other operations
                ptmp2 = p1  # Sets variables so it doesn't mess up other operations
                while ptmp2 < site[6]:  # looks for when azimuth breaches sides of coverage
                    ptmp2 = Orbital.get_observer_look(sat, rx, site[1], site[0], site[2])[0]  # gets new azimuth
                    rx = rx + timedelta(seconds=10)
                print("Fence Time:", rx, "Angle:", p1)  # prints passe info (used for dev)
                passes.append(rx)  # appedns check passes to passes list

        elif not site[6] < en[0] < site[7]:  # if enters FOV not on face2
            print("Fence Pass | Az:", ex[0])  # prints pass info (used for dev)
            p1 = Orbital.get_observer_look(sat, i[0], site[1], site[0], site[2])[0]  # az when time enters 3 degree bubble FOV
            p2 = Orbital.get_observer_look(sat, i[0] + timedelta(seconds=5), site[1], site[0], site[2])[0]  # p1 5 seconds later
            start = i[0]

            if (p1 - p2) < 0:  # if the azimuth is growing after 5 seconds
                rx = i[0]  # Sets variables so it doesn't mess up other operations
                ptmp3 = p1  # Sets variables so it doesn't mess up other operations
                while ptmp4 < site[6]:  # looks for when azimuth breaches sides of coverage
                    ptmp4 = Orbital.get_observer_look(sat, rx, site[1], site[0], site[2])[0]  # gets new azimuth
                    rx = rx + timedelta(seconds=10)  # sets time for 10s later to retrieve azimuth at that time
                print("Fence Time:", rx, "Angle:", p1)  # prints pass info (used for dev)
                passes.append(rx)  # appedns check passes to passes list

            if (p1 - p2) > 0:  # if the azimuth is shrinking after 5 seconds
                rx = i[0]  # Sets variables so it doesn't mess up other operations
                ptmp4 = p1  # Sets variables so it doesn't mess up other operations
                while ptmp4 > site[6]:  # looks for when azimuth breaches sides of coverage
                    ptmp4 = Orbital.get_observer_look(sat, rx, site[1], site[0], site[2])[0]  # gets new azimuth
                    rx = rx + timedelta(seconds=10)  # sets time for 10s later to retrieve azimuth at that time
                print("Fence Time:", rx, "Angle:", p1)  # prints pass info (used for dev)
                passes.append(rx)  # appedns check passes to passes list
    print("")
    return passes
