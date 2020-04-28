# tests covid19_updater.py
# NOTE - As this is the main class, these test cases are system-level
# CB: Michael Kukar
# Copyright Michael Kukar 2020.

import unittest
import sys, os, shutil

sys.path.append('..')
from covid19_updater import *

class TestCases(unittest.TestCase):

    ACTUAL_CONFIG = "../config.json"

    VALID_CONFIG = "valid_configuration_file.json"
    INVALID_CONFIG = "invalid_configuration_file.json"
    CORRUPTED_CONFIG = "corrupted_configuration_file.json"

    EMPTY_DB_FILE = "empty_test_database.db"

    def setUp(self):
        # copies dummy database that is empty
        shutil.copyfile(self.EMPTY_DB_FILE, "temp_" + self.EMPTY_DB_FILE)

    def tearDown(self):
        # deletes our dummy database file
        os.remove("temp_" + self.EMPTY_DB_FILE)

    def test_parseConfigReturnsTrueWithValidConfigFile(self):
        # parseConfig is called on construction, so ensure we don't throw
        try:
            Covid19Updater(self.VALID_CONFIG, "temp_" + self.EMPTY_DB_FILE)
        except:
            self.fail()
    
    def test_parseConfigReturnsFalseWithInvalidConfigFile(self):
        self.assertRaises(Exception, Covid19Updater, self.INVALID_CONFIG, "temp_" + self.EMPTY_DB_FILE)
    
    def test_parseConfigReturnsFalseWithCorruptConfigFile(self):
        self.assertRaises(Exception, Covid19Updater, self.CORRUPTED_CONFIG, "temp_" + self.EMPTY_DB_FILE)

    def test_checkForUpdateAndSend(self):
        try:
            cu = Covid19Updater(self.ACTUAL_CONFIG, "temp_" + self.EMPTY_DB_FILE)
            cu.checkForUpdateAndSend(forceSend=True)
        except:
            self.fail()



if __name__ == "__main__":
    unittest.main()