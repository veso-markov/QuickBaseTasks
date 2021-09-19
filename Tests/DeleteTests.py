import json

import pytest

from BaseApiRequests.api_delete import api_delete as delete
from BaseApiRequests.api_records import api_records as records


class DeleteTests(delete, records):
    @pytest.mark.delete
    def test_delete_to_wrong_realm(self):
        self.headers = {
            'QB-Realm-Hostname': 'wrong.quickbase.com',
            'Authorization': 'QB-USER-TOKEN b6dvxg_uyp_0_cc9sq7rb6fgcfesh3ificzrjm84'
        }
        response = self.delete(table="brfnk4id5", where="{CT.''}")
        self.assertEqual(response.status_code, 502)
        self.assertEqual(json.loads(response.text)["message"], "Unknown Hostname")

    @pytest.mark.delete
    def test_delete_without_header(self):
        self.headers = {}
        response = self.delete(table="brfnk4id5", where="{CT.''}")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.text)["message"], "Bad request")

    @pytest.mark.delete
    def test_delete_with_wrong_token(self):
        self.headers = {
            'QB-Realm-Hostname': 'team.quickbase.com',
            'Authorization': 'QB-USER-TOKEN wrong-token'
        }
        response = self.delete(table="brfnk4id5", where="{CT.''}")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.text)["message"], "Access denied")

    @pytest.mark.delete
    def test_delete_with_invalid_table(self):
        response = self.delete(table="invalid_table", where="{CT.''}")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.text)["message"], "Invalid request")

    @pytest.mark.delete
    def test_delete_with_wrong_table(self):
        response = self.delete(table="brfnk4id6", where="{CT.''}")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.text)["message"], "Access denied")

    @pytest.mark.delete
    def test_delete_more_than_one(self):
        first_record = self.insert(table="brfnk4id5", id=['6'], values=['test'], fields_to_return="")
        second_record = self.insert(table="brfnk4id5", id=['6'], values=['test1'], fields_to_return="")
        response = self.delete(table="brfnk4id5", where="{CT.''}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.text)["numberDeleted"], 2)

    @pytest.mark.delete
    def test_delete_none(self):
        response = self.delete(table="brfnk4id5", where="{CT.''}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.text)["numberDeleted"], 0)
