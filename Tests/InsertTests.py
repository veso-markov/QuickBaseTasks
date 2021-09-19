import json

import pytest

from BaseApiRequests.ApiRecords import ApiRecords as Records
from BaseApiRequests.General import General


class ImportTests(Records, General):
    @pytest.mark.Insert
    def test_create_record(self):
        response = self.Insert(table="brfnk4id5", id=[], values=[], fields_to_return="")
        self.assertEqual(response.status_code, 200)

    @pytest.mark.Insert
    def test_create_record_without_header(self):
        self.headers = {}
        response = self.Insert(table="brfnk4id5", id=[], values=[], fields_to_return="")
        self.assertEqual(response.status_code, 400)

    @pytest.mark.Insert
    def test_create_record_to_wrong_realm(self):
        self.headers = {
            'QB-Realm-Hostname': 'wrong.quickbase.com',
            'Authorization': 'QB-USER-TOKEN b6dvxg_uyp_0_cc9sq7rb6fgcfesh3ificzrjm84'
        }
        response = self.Insert(table="brfnk4id5", id=[], values=[], fields_to_return="")
        self.assertEqual(response.status_code, 502)
        self.assertEqual(json.loads(response.text)["message"], "Unknown Hostname")

    @pytest.mark.Insert
    def test_create_record_with_wrong_token(self):
        self.headers = {
            'QB-Realm-Hostname': 'team.quickbase.com',
            'Authorization': 'QB-USER-TOKEN wrong-token'
        }
        response = self.Insert(table="brfnk4id5", id=[], values=[], fields_to_return="")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.text)["message"], "Access denied")

    @pytest.mark.Insert
    def test_create_record_with_invalid_table(self):
        response = self.Insert(table="wrong_table", id=[], values=[], fields_to_return="")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.text)["message"], "Invalid request")

    @pytest.mark.Insert
    def test_create_record_with_wrong_table(self):
        response = self.Insert(table="brfnk4id6", id=[], values=[], fields_to_return="")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.text)["message"], "Access denied")

    @pytest.mark.Insert
    def test_create_incrementing_id(self):
        first_response = self.Insert(table="brfnk4id5", id=[], values=[], fields_to_return="")
        self.assertEqual(first_response.status_code, 200)
        second_response = self.Insert(table="brfnk4id5", id=[], values=[], fields_to_return="")
        self.assertEqual(second_response.status_code, 200)
        self.assertLess(json.loads(first_response.text)["metadata"]["createdRecordIds"],
                        json.loads(second_response.text)["metadata"]["createdRecordIds"])

    @pytest.mark.Insert
    def test_number_field(self):
        response = self.Insert(table="brfnk4id5", id=['7'], values=['text'], fields_to_return="")
        self.assertEqual(response.status_code, 207)
        self.assertIn("Incompatible value", json.loads(response.text)["metadata"]["lineErrors"]["1"][0])

    @pytest.mark.Insert
    def test_percentage_field(self):
        response = self.Insert(table="brfnk4id5", id=['8'], values=['text'], fields_to_return="")
        self.assertEqual(response.status_code, 207)
        self.assertIn("Incompatible value", json.loads(response.text)["metadata"]["lineErrors"]["1"][0])

    @pytest.mark.Insert
    def test_time_field(self):
        response = self.Insert(table="brfnk4id5", id=['9'], values=['text'], fields_to_return="")
        self.assertEqual(response.status_code, 207)
        self.assertIn("The value for Time Of Day ", json.loads(response.text)["metadata"]["lineErrors"]["1"][0])

    @pytest.mark.Insert
    def test_all_fields_correct_data(self):
        response = self.Insert(table="brfnk4id5", id=['6', '7', '8', '9', '10', '11'],
                               values=['Text', 2, 0.2, self.generate_now_time(), "some@mail.com",
                                       "https://quickbase.com"], fields_to_return="")
        self.assertEqual(response.status_code, 200)

    @pytest.mark.Insert
    def test_response_time(self):
        avg_time = 0
        for i in range(10):
            response = self.Insert(table="brfnk4id5", id=['6', '7', '8', '9', '10', '11'],
                                   values=['Text', 2, 0.2, self.generate_now_time(), "some@mail.com",
                                           "https://quickbase.com"], fields_to_return="")
            avg_time = avg_time + response.elapsed.total_seconds()
        self.assertLess(avg_time, 10)
        self.assertEqual(response.status_code, 200)

    @pytest.mark.Insert
    def test_text_field_accept_chars(self):
        response = self.Insert(table="brfnk4id5", id=['6'], values=['textабвö™®'], fields_to_return="")
        self.assertEqual(response.status_code, 200)

    @pytest.mark.Insert
    def test_insert_prepopulated_timedate_fields(self):
        response = self.Insert(table="brfnk4id5", id=['6'], values=['test'], fields_to_return="")
        query = self.Query(table="brfnk4id5", where="{6.CT.'test'}", select=[1, 2, 3, 4, 5])
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.validate_string_is_in_qb_format(json.loads(query.text)["data"][0]["1"]["value"]))
        self.assertTrue(self.validate_string_is_in_qb_format(json.loads(query.text)["data"][0]["2"]["value"]))

    @pytest.mark.Insert
    def test_insert_prepopulated_email_fields(self):
        response = self.Insert(table="brfnk4id5", id=['6'], values=['test'], fields_to_return="")
        query = self.Query(table="brfnk4id5", where="{6.CT.'test'}", select=[1, 2, 3, 4, 5])
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.validate_email_format(json.loads(query.text)["data"][0]["4"]["value"]["email"]))
        self.assertTrue(self.validate_email_format(json.loads(query.text)["data"][0]["5"]["value"]["email"]))
