import re


def getTLE(satno, filename):
    ln1 = str("1 " + str(satno))  # Sets up search query for TLE finder
    ln2 = str("2 " + str(satno))
    ln1 = re.sub(' +', ' ', ln1)

    searchfile = open(filename, "r")  # Opens TLE file for TLE that matches satno
    for line in searchfile:
        if ln1 in line:
            L1 = line

        if ln2 in line:
            L2 = line
    searchfile.close()
    return L1, L2
