# tests web_reader.py
# CB: Michael Kukar
# Copyright Michael Kukar 2020.

import unittest
import sys, os, shutil

sys.path.append('..')
from web_reader import *

class WebTestCases(unittest.TestCase):

    def test_isNewDataAvailableReturnsFalseIfWebTimestampOlderThanLatestDbTimestamp(self):
        self.assertTrue(False)
    
    def test_isNewDataAvailableReturnsTrueIfWebTimestampNewerThanLatestDbTimestamp(self):
        self.assertTrue(False)
    
    def test_isNewDataAvailableReturnsFalseIfCannotReadWebsite(self):
        self.assertTrue(False)
    
    def test_isNewDataAvailableReturnsFalseIfWebTimestampMatchesDbTimestamp(self):
        self.assertTrue(False)
    
    def test_readLatestEntryFromWebReturnsValidDatasetOnValidWebsite(self):
        self.assertTrue(False)
    
    def test_readLatestEntryFromWebReturnsNoneIfInvalidWebsiteData(self):
        self.assertTrue(False)
    
    def test_readLatestEntryFromWebReturnsNoneIfWebsiteInaccessible(self):
        self.assertTrue(False)


class DatabaseTestCases(unittest.TestCase):

    EMPTY_DB_FILE = "empty_test_database.db"

    VALID_DB_ENTRY = {
        'date' : '01022020',
        'total_cases' : 1,
        'new_cases' : 1,
        'new_tests' : 1,
        'hospitalizations' : 0,
        'intensive_care' : 5,
        'deaths' : 0
    }

    INCOMPLETE_DB_ENTRY = {
        'date' : '01022020',
        'total_cases' : 1,
        'new_cases' : 1
    }

    BAD_RANGES_DB_ENTRY = {
        'date' : '01022020',
        'total_cases' : -1,
        'new_cases' : -1,
        'new_tests' : -1,
        'hospitalizations' : 0,
        'intensive_care' : -5,
        'deaths' : 0
    }

    def setUp(self):
        # copies dummy database that is empty
        shutil.copyfile(self.EMPTY_DB_FILE, "temp_" + self.EMPTY_DB_FILE)

        self.wr = WebReader("temp_" + self.EMPTY_DB_FILE)

    def tearDown(self):
        # deletes our dummy database file
        os.remove("temp_" + self.EMPTY_DB_FILE)

    def test_addEntryToDatabaseSucceedsWhenDatasetIsValid(self):
        self.assertTrue(self.wr.addEntryToDatabase(self.VALID_DB_ENTRY))
        conn = sqlite3.connect("temp_" + self.EMPTY_DB_FILE)
        dataset = conn.execute("select * from DATA")
        self.assertEqual(1, len(dataset.fetchall()))
        conn.close()
    
    def test_addEntryToDatabaseFailsWhenDatasetIsCorrupted(self):
        self.assertFalse(self.wr.addEntryToDatabase(None))
    
    def test_addEntryToDatabaseFailsWhenDatasetIsIncomplete(self):
        self.assertFalse(self.wr.addEntryToDatabase(self.INCOMPLETE_DB_ENTRY))
    
    def test_addEntryToDatabaseFailsWhenDatasetIsOutOfValidRanges(self):
        self.assertFalse(self.wr.addEntryToDatabase(self.BAD_RANGES_DB_ENTRY))

    def test_addEntryToDatabaseFailsWhenDatasetTimestampAlreadyExists(self):
        self.assertTrue(self.wr.addEntryToDatabase(self.VALID_DB_ENTRY))
        self.assertFalse(self.wr.addEntryToDatabase(self.VALID_DB_ENTRY))
        conn = sqlite3.connect("temp_" + self.EMPTY_DB_FILE)
        dataset = conn.execute("select * from DATA")
        self.assertEqual(1, len(dataset.fetchall()))
        conn.close()

    def test_readLatestEntryFromDatabaseReturnsMostRecentTimestampFromDatabase(self):
        self.assertTrue(False)
    
    def test_readLatestEntryFromDatabaseReturnsNoneIfNoDataPresent(self):
        self.assertTrue(False)

if __name__ == "__main__":
    unittest.main()