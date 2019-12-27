import math

# mm = Mean Motion in Rev/Day
# dista = Distance in Meters
# toez = Time off Element Set in seconds


def toes(mm, dista):
    mu = 398600441800000
    sma = (pow(mu, (1 / 3))) / (pow((2 * mm * math.pi / 86400), 2 / 3)) / 100
    circum = sma * 2 * math.pi
    period_min = (1 / mm) * 24 * 60
    period_sec = (1 / mm) * 24 * 60 * 60
    spd_min = circum / period_min  # speed in km/min
    spd_sec = circum / period_sec  # speed in km/sec
    toe = dista / spd_sec  # time off elset in sec
    return toe


def dist(mm, toez):
    mu = 398600441800000
    sma = (pow(mu, (1 / 3))) / (pow((2 * mm * math.pi / 86400), 2 / 3)) / 100
    circum = sma * 2 * math.pi
    period_min = (1 / mm) * 24 * 60
    period_sec = (1 / mm) * 24 * 60 * 60
    spd_min = circum / period_min  # speed in km/min
    spd_sec = circum / period_sec  # speed in km/sec
    dista = spd_sec * toez
    return dista
