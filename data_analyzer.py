# analyzes the latest data for trends and patterns
# Copyright Michael Kukar 2020. MIT License.

import sqlite3
import statistics

class DataAnalyzer:

    LATEST_ENTRY_QUERY = "SELECT DATE, TOTAL_CASES, NEW_CASES, NEW_TESTS, HOSPITALIZATIONS, INTENSIVE_CARE, DEATHS from DATA ORDER BY strftime('%Y-%m-%d', DATE) DESC"
    MAX_NEW_CASES_ENTRY_QUERY = "SELECT DATE, TOTAL_CASES, MAX(NEW_CASES), NEW_TESTS, HOSPITALIZATIONS, INTENSIVE_CARE, DEATHS from DATA"


    def __init__(self, dbFilename):
        self.dbFilename = dbFilename


    # checks if latest entry has the maximum new cases of entire db
    # return : true if latest is max, false otherwise
    def checkIfLatestIsMaxNewCases(self):
        # connects to database
        conn = sqlite3.connect(self.dbFilename)
        c = conn.cursor()
        c.execute(self.LATEST_ENTRY_QUERY)
        latestEntryData = c.fetchone()
        c.execute(self.MAX_NEW_CASES_ENTRY_QUERY)
        maxEntryData = c.fetchone()
        conn.close()

        # first index is DATE, if dates equal then max == latestentry
        if latestEntryData[0] == maxEntryData[0]:
            return True
        else:
            return False
    

    # trends the new cases difference between X number of latest days in the database
    # NOTE - If one of the days new_cases entry is None, will ignore it but not load another day
    # days   : (optional) number of days to trend
    # return : float of trend between days
    def getNewCasesTrend(self, days=3):
        # with only 1 or less entries, cannot get trend (difference)
        if days < 2:
            return 0
        # essentially a linear interpolation
        newCasesEachDay = []
        # connects to database
        conn = sqlite3.connect(self.dbFilename)
        c = conn.cursor()
        c.execute(self.LATEST_ENTRY_QUERY)
        latestEntries = c.fetchmany(days)
        for entry in latestEntries:
            # NEW_CASES is in location 2, skips any None entries
            if entry[2] is not None:
                newCasesEachDay.append(int(entry[2]))
        conn.close()
        # gets difference between each day, and then averages them
        diffBetweenEachDay = []
        # too many None cases, so we don't have enough data
        if len(newCasesEachDay) < 2:
            return 0
        for i in range(len(newCasesEachDay)-1):
            diffBetweenEachDay.append(newCasesEachDay[i]-newCasesEachDay[i+1])
        trend = statistics.mean(diffBetweenEachDay)

        return trend


    # averages the X latest new_cases days
    # NOTE - If one of the days new_cases entry is None, will ignore it but not load another day
    # days   : (optional) number of days to average
    # return : float of average of new_cases across the days
    def getLatestNewCasesAverage(self, days=7):
        # cannot have zero or negative days
        if days < 1:
            return 0.0
        
        # connects to databse
        conn = sqlite3.connect(self.dbFilename)
        newCasesEachDay = []
        # connects to database
        conn = sqlite3.connect(self.dbFilename)
        c = conn.cursor()
        c.execute(self.LATEST_ENTRY_QUERY)
        latestEntries = c.fetchmany(days)
        for entry in latestEntries:
            # NEW_CASES is in location 2, skips any None entries
            if entry[2] is not None:
                newCasesEachDay.append(int(entry[2]))
        conn.close()
        # gets average of the new cases across the most recent X days
        return statistics.mean(newCasesEachDay)
