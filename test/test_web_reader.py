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

    def setUp(self):
        # copies dummy database that is empty
        shutil.copyfile(self.EMPTY_DB_FILE, "temp_" + self.EMPTY_DB_FILE)

    def tearDown(self):
        # deletes our dummy database file
        os.remove("temp_" + self.EMPTY_DB_FILE)

    def test_addEntryToDatabaseSucceedsWhenDatasetIsValid(self):
        self.assertTrue(False)
    
    def test_addEntryToDatabaseFailsWhenDatasetIsCorrupted(self):
        self.assertTrue(False)
    
    def test_addEntryToDatabaseFailsWhenDatasetIsIncomplete(self):
        self.assertTrue(False)
    
    def test_addEntryToDatabaseFailsWhenDatasetIsOutOfValidRanges(self):
        self.assertTrue(False)

    def test_addEntryToDatabaseFailsWhenDatasetTimestampAlreadyExists(self):
        self.assertTrue(False)

    def test_readLatestEntryFromDatabaseReturnsMostRecentTimestampFromDatabase(self):
        self.assertTrue(False)
    
    def test_readLatestEntryFromDatabaseReturnsNoneIfNoDataPresent(self):
        self.assertTrue(False)

if __name__ == "__main__":
    unittest.main()