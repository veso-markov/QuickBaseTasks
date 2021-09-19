import requests

class ApiRecords:

    def Query(self, table,where,select):
        body = {"from": table,"where":where,"select":select}
        r = requests.post(
            self.url + "/query",
            headers=self.headers,
            json=body
        )
        print(body)
        print(r.text)
        return r

    def Insert(self, table,id,values,fields_to_return):
        id_value_pair = {}
        value_pair = {}
        if len(id)<1:
            pass
        elif len(id)>=1:
            for i in range(len(id)):
                value_pair["value"] = values[i]
                id_value_pair[id[i]] = {}
                id_value_pair[id[i]].update(value_pair)
        body = {"to": table, "data": [id_value_pair],
                "fieldsToReturn": [fields_to_return]}
        r = requests.post(
            self.url,
            headers=self.headers,
            json=body
        )
        print(body)
        return r




