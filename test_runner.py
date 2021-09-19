from unittest import TestCase

from Tests.DeleteTests import DeleteTests
from Tests.InsertTests import ImportTests


class Testrunner(ImportTests, DeleteTests, TestCase):
    def setUp(self):
        self.headers = {
            'QB-Realm-Hostname': 'team.quickbase.com',
            'Authorization': 'QB-USER-TOKEN b6dvxg_uyp_0_cc9sq7rb6fgcfesh3ificzrjm84'
        }
        self.url = 'https://api.quickbase.com/v1/records'

    def tearDown(self):
        if self.headers != {}:
            DeleteTests.delete(self, table="brfnk4id5", where="{CT.''}")
