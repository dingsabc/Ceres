from getPasses import get_site_passes
from getpie import getPIE
import pandas as pd
from datetime import timedelta
import numpy as np


def checkTLE(SCC):
    pie = getPIE(SCC, 'tle.txt')

    if np.datetime64('now') - pie[4] > timedelta(days=7):
        print(SCC, "TLE is over a week old")  # User warning

    if pie[0] > 225:  # check to see if period is too large, SGP4 is hard coded to hate 255+ min period
        print("Period too large")  # will need to set up later for sdt.out for web
        exit()


def SitePassesToTables(SCC, places, CALC_HRS, TLEfile, fileout=None):
    appended_data = []
    for i in places:
        checkTLE(esv)
        run = get_site_passes(SCC, i, CALC_HRS, TLEfile)
        appended_data.append(run)
    final_data = pd.concat(appended_data)
    final_data = final_data.round({'EnterAz': 3})
    final_data = final_data.sort_values(by=['PassStart'])
    print(final_data.to_csv(index=False))
    final_data.to_csv(fileout, index=False)
    return final_data


def PosNegPassToTable(ESVs, site, CALC_HRS, TLEfile, fileout=None):
    appended_data = []
    for esv in esvs:
        checkTLE(esv)
        run = get_site_passes(esv, site, CALC_HRS, TLEfile)
        appended_data.append(run)
    final_data = pd.concat(appended_data)
    final_data = final_data.round({'EnterAz': 3})
    final_data = final_data.sort_values(by=['PassStart'])
    final_data = final_data[['SCC', 'PassStart', 'EnterAz', 'Length', 'Site']]
    print(final_data.to_csv(index=False))
    final_data.to_csv(fileout, index=False)
    return final_data
