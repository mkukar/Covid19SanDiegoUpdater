# reads data from web on coronavirus
# tailored for San Diego, may be adaptable to other govmt websites
# CB: Michael Kukar
# Copyright Michael Kukar 2020.

import sqlite3
from collections import Mapping

class WebReader:

    dbFilename = "covid19.db"

    REQUIRED_ENTRY_FIELDS = ['date', 'total_cases', 'new_cases', 'new_tests', 'hospitalizations', 'intensive_care', 'deaths']

    ADD_ENTRY_COMMAND = ("INSERT INTO DATA (DATE, TOTAL_CASES, NEW_CASES, NEW_TESTS, HOSPITALIZATIONS, INTENSIVE_CARE, DEATHS) VALUES ("
        ":date, :total_cases, :new_cases, :new_tests, :hospitalizations, :intensive_care, :deaths);"
    )

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

    def isNewDataAvailable(self):
        pass

    def readLatestEntryFromDatabase(self):
        pass

    def readLatestEntryFromWeb(self):
        pass

