# reads data from web on coronavirus
# tailored for San Diego, may be adaptable to other govmt websites
# CB: Michael Kukar
# Copyright Michael Kukar 2020.

import sqlite3
from collections import Mapping
from bs4 import BeautifulSoup
import urllib
import requests
from datetime import datetime

class WebReader:

    dbFilename = "covid19.db"

    SD_COVID19_URL = "https://www.sandiegocounty.gov/content/sdc/hhsa/programs/phs/community_epidemiology/dc/2019-nCoV/status.html"

    REQUIRED_ENTRY_FIELDS = ['date', 'total_cases', 'new_cases', 'new_tests', 'hospitalizations', 'intensive_care', 'deaths']

    ADD_ENTRY_COMMAND = ("INSERT INTO DATA (DATE, TOTAL_CASES, NEW_CASES, NEW_TESTS, HOSPITALIZATIONS, INTENSIVE_CARE, DEATHS) VALUES ("
        ":date, :total_cases, :new_cases, :new_tests, :hospitalizations, :intensive_care, :deaths);"
    )
    LATEST_ENTRY_QUERY = "SELECT DATE, TOTAL_CASES, NEW_CASES, NEW_TESTS, HOSPITALIZATIONS, INTENSIVE_CARE, DEATHS from DATA ORDER BY strftime('%m%d%Y', DATE) ASC"

    def __init__(self, dbFilename):
        # stores filename of database
        self.dbFilename = dbFilename

    def addEntryToDatabase(self, entry):
        # makes sure entry is a dictionary
        if entry is None or not isinstance(entry, Mapping):
            return False
        # makes sure entry contains all required fields (they can be None, but must exist)
        for field in self.REQUIRED_ENTRY_FIELDS:
            if field not in entry.keys():
                return False
        # checks that fields are within bounds (not negative, etc.)
        # all fields except DATE must be greater than 0
        for field in self.REQUIRED_ENTRY_FIELDS:
            if field == 'date': continue
            # makes sure entry is able to be cast to an int type
            try:
                int(entry[field])
            except:
                return False
            if int(entry[field]) < 0:
                return False
        # adds entry to database
        try:
            conn = sqlite3.connect(self.dbFilename)
            res = conn.execute(self.ADD_ENTRY_COMMAND, entry)
            conn.commit()
            conn.close()
        except Exception as e:
            return False
        return True

    def readLatestEntryFromDatabase(self):
        res = None
        try:
            conn = sqlite3.connect(self.dbFilename)
            c = conn.cursor()
            c.execute(self.LATEST_ENTRY_QUERY)
            res = c.fetchone()
            conn.close()
        except Exception as e:
            return None
        if res is None:
            return None
        # now maps res to a dict
        resDict = {}
        for idx, field in enumerate(self.REQUIRED_ENTRY_FIELDS):
            resDict[field] = res[idx]
        return resDict

    def isNewDataAvailable(self, url=None):
        if url is None:
            url = self.SD_COVID19_URL
        # gets latest db entry and extracts date
        try:
            dbDate = self.readLatestEntryFromDatabase()
            if dbDate is None:
                # no database entry, so we return True (anything is newer)
                return True
            dbDate = datetime.strptime(dbDate['date'], '%m%d%Y')
        except:
            return False

        webDate = None
        # reads latest update field from the website and extracts date
        try:
            source = urllib.request.urlopen(url).read()
            bs = BeautifulSoup(source, "lxml")
            # location of date is in a string located at
            # table -> tr -> td -> "table updated X, with date through Y"
            table = bs.find("table")
            # gets first td in the first tr
            table_rows = table.tbody.find_all("tr")
            td = table_rows[0].find_all("td")[0]
            # extract the date after "with data through"
            rawDateStr = str(td).split("with data through ")[1]
            rawDateStr = rawDateStr.split(".</i>")[0]
            webDate = datetime.strptime(rawDateStr, '%B %d, %Y')
        except:
            return False

        # if date is newer, return True, else false
        if webDate > dbDate:
            return True
        else:
            return False

    def readLatestEntryFromWeb(self, url=None):
        if url is None:
            url = self.SD_COVID19_URL
        # opens website
        # reads the date and converts to our format MMDDYYYY
        # reads the table data
        # returns as a dictionary
        return None

