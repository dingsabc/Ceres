from getPasses import get_site_passes
from getpie import getPIE
import pandas as pd
from datetime import timedelta
import numpy as np


def checkTLE(SCC, TLEfile):  # gets new TLE file if more than 7 days old
    pie = getPIE(SCC, TLEfile)
    if np.datetime64('now') - pie[4] > timedelta(days=7):
        print(SCC, "TLE is over a week old, getting new TLEs")  # User warning
        import sys
        sys.path.append('/Users/traxtar3/Dropbox/Coding/Python/Projects/getTLEfile')
        from pw import username, password
        from tleRetrive import useapi
        import os
        # useapi((username, password), TLE)  # Updates TLE File

    if pie[0] > 225:  # check to see if period is too large, SGP4 is hard coded to hate 255+ min period
        print("Period too large")  # will need to set up later for sdt.out for web
        # exit()


def passToTables(SCC, places, CALC_HRS, TLEfile, fileout=None):  # one ESV for multiple sites
    appended_data = []
    checkTLE(SCC, TLEfile)
    if getPIE(SCC, TLEfile)[0] < 225:
        for i in places:
            run = get_site_passes(SCC, i, CALC_HRS, TLEfile)
            appended_data.append(run)
    else:
        print(SCC, "period too large")
        exit()
    final_data = pd.concat(appended_data)
    final_data = final_data.round({'EnterAz': 3})
    final_data = final_data.sort_values(by=['PassStart'])
    final_data = final_data[['SCC', 'Site', 'PassStart', 'EnterAz', 'Length']]
    final_data.to_csv(fileout, index=False)
    return final_data


def PosNegPassToTable(ESVs, site, CALC_HRS, TLEfile, fileout=None):  # multiple ESVs for one site
    appended_data = []
    esvlist1 = []
    esvlist2 = []
    for i in esvs:
        try:
            esvlist1.append(getTLE(i, TLEfile)[2])
        except Exception:
            pass
    for w in esvlist1:
        if getPIE(w, TLEfile)[0] < 225:
            esvlist2.append(w)
        else:
            print(w, "has a period < 225, skipping")
    for esv in esvlist2:
        checkTLE(esv, TLEfile)
        run = get_site_passes(esv, site, CALC_HRS, TLEfile)
        appended_data.append(run)
    final_data = pd.concat(appended_data)
    final_data = final_data.round({'EnterAz': 3})
    final_data = final_data.sort_values(by=['PassStart'])
    final_data = final_data[['SCC', 'PassStart', 'EnterAz', 'Length', 'Site']]
    final_data.to_csv(fileout, index=False)
    return final_data


def combined(ESVs, places, CALC_HRS, TLEfile, fileout=None):
    appended_data = []
    esvlist1 = []
    esvlist2 = []
    for i in esvs:
        try:
            esvlist1.append(getTLE(i, TLEfile)[2])
        except Exception:
            pass
    for w in esvlist1:
        if getPIE(w, TLEfile)[0] < 225:
            esvlist2.append(w)
        else:
            print(w, "has a period < 225, skipping")
    for x in esvlist2:
        # for x in ESVs:
        checkTLE(x, TLEfile)
        for i in places:
            run = get_site_passes(x, i, CALC_HRS, TLEfile)
            appended_data.append(run)
    final_data = pd.concat(appended_data)
    final_data = final_data.round({'EnterAz': 3})
    final_data = final_data.sort_values(by=['PassStart'])
    final_data = final_data[['SCC', 'Site', 'PassStart', 'EnterAz', 'Length']]
    final_data.to_csv(fileout, index=False)
    return final_data
