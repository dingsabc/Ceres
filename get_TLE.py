import re


def getTLE(satno, filename):
    ln1 = str("1 " + str(satno))  # Sets up search query for TLE finder
    while len(ln1) < 7:
        ln1 = re.sub(' ', '  ', ln1, 1)
    ln2 = str("2 " + str(satno))
    while len(ln2) < 7:
        ln2 = re.sub(' ', '  ', ln2, 1)
    ln1 = re.sub(' +', ' ', ln1)
    L1, L2 = '', ''
    searchfile = open(filename, "r")  # Opens TLE file for TLE that matches satno
    for line in searchfile:
        if ln1 in line:
            L1 = line

        if ln2 in line:
            L2 = line
    searchfile.close()
    if L1:
        return L1, L2, satno
    else:
        print(satno, "TLE not found, skipping")
        # exit()
