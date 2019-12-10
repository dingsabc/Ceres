from pyorbital.orbital import Orbital, get_observer_look
from datetime import datetime, timedelta, date
import time
from numpy import fabs
import re
from getTLE import getTLE

# SITE = [lat(N), long(E), alt(km), horizon(deg), begin coverage (closest to zero), end coverage, begin coverage, end coverage(closest to 360)]


def get_site_passes(satno, site, duration, filename):  # Duration in hours from current time,  # filename = file with TLEs in it

    now = datetime.utcnow()  # set time to current time
    sat = Orbital(satellite='None', line1=getTLE(satno, filename)[0], line2=getTLE(satno, filename)[1])
    x = Orbital.get_next_passes(sat, now, duration, site[1], site[0], site[2], tol=0.001, horizon=site[3])  # builds list of all passes that break 3 degrees
    passes = []  # begins empty list for passes
    for i in x:
        en = Orbital.get_observer_look(sat, i[0], site[1], site[0], site[2])  # Gets entry Az & El
        ex = Orbital.get_observer_look(sat, i[1], site[1], site[0], site[2])  # Gets exitAz & El
        hi = Orbital.get_observer_look(sat, i[2], site[1], site[0], site[2])  # Gets exitAz & El
        p1 = Orbital.get_observer_look(sat, i[0], site[1], site[0], site[2])[0]  # az at 3 degree entry
        p2 = Orbital.get_observer_look(sat, i[0] + timedelta(seconds=1), site[1], site[0], site[2])[0]  # p1 1 seconds later
        p3 = Orbital.get_observer_look(sat, i[1], site[1], site[0], site[2])[0]  # az at 3 degree exit

        print(site[8], "Pass Start:", i[0], "Enter Az", en[0], "Pass Term:", i[1], "Exit Az:", ex[0], "MaxEl:", hi[1])  # prints passes (used for dev)

        if site[4] < en[0] < site[5] or site[6] < en[0] < site[7]:  # if satellite enters FOV on face *checkpass*
            len = int((i[1] - i[0]).total_seconds())  # length of pass in seconds
            passes.append(i[0])  # appedns check passes to passes list            print("Check Pass | Az:", en[0])  # prints pass info (used for dev)

        elif not site[4] < en[0] < site[5]:  # if enters FOV not on face1
            print("Fence Pass | Az:", ex[0])  # prints pass info (used for dev)

            if (p1 - p2) < 0:  # if the azimuth is growing after 5 seconds
                rx = i[0]  # Sets variables so it doesn't mess up other operations
                while p1 <= site[6]:  # looks for when azimuth breaches sides of coverage
                    p1 = Orbital.get_observer_look(sat, rx, site[1], site[0], site[2])[0]  # gets new azimuth
                    rx = rx + timedelta(seconds=10)  # sets time for 10s later to retrieve azimuth at that time
                print("Fence Time:", rx, "Angle:", p1)  # prints pass info (used for dev)
                len = int((i[1] - rx).total_seconds())
                passes.append(rx)

            if (p1 - p2) > 0:  # if the azimuth is shrinking after 5 seconds
                rx = i[0]  # Sets variables so it doesn't mess up other operations
                while p1 >= site[6]:  # looks for when azimuth breaches sides of coverage
                    p1 = Orbital.get_observer_look(sat, rx, site[1], site[0], site[2])[0]  # gets new azimuth
                    rx = rx + timedelta(seconds=10)
                print("Fence Time:", rx, "Angle:", p1)  # prints passe info (used for dev)
                len = int((i[1] - rx).total_seconds())
                passes.append(rx)  # appedns check passes to passes list

        elif not site[6] < en[0] < site[7]:  # if enters FOV not on face2
            print("Fence Pass | Az:", ex[0])  # prints pass info (used for dev)

            if (p1 - p2) < 0:  # if the azimuth is growing after 5 seconds
                rx = i[0]  # Sets variables so it doesn't mess up other operations
                while p1 <= site[6]:  # looks for when azimuth breaches sides of coverage
                    p1 = Orbital.get_observer_look(sat, rx, site[1], site[0], site[2])[0]  # gets new azimuth
                    rx = rx + timedelta(seconds=10)  # sets time for 10s later to retrieve azimuth at that time
                print("Fence Time:", rx, "Angle:", p1)  # prints pass info (used for dev)
                len = int((i[1] - rx).total_seconds())

                passes.append(rx)  # appedns check passes to passes list

            if (p1 - p2) > 0:  # if the azimuth is shrinking after 5 seconds
                rx = i[0]  # Sets variables so it doesn't mess up other operations
                while p1 >= site[6]:  # looks for when azimuth breaches sides of coverage
                    p1 = Orbital.get_observer_look(sat, rx, site[1], site[0], site[2])[0]  # gets new azimuth
                    rx = rx + timedelta(seconds=10)  # sets time for 10s later to retrieve azimuth at that time
                print("Fence Time:", rx, "Angle:", p1)  # prints pass info (used for dev)
                len = int((i[1] - rx).total_seconds())

                passes.append(rx)  # appedns check passes to passes list

        if len < 0:
            print("Not a Pass")
        elif len < 180:
            print("Pass Length: ", len, "sec (short)")
        else:
            print("Pass Length: ", len, "sec")
    return passes  # Returns datetime objects for all passes
