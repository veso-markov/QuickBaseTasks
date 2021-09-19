import requests
class ApiDelete:
    def delete(self, table, where):
        body = {"from": table, "where":where}
        r = requests.delete(
            self.url,
            headers=self.headers,
            json=body
        )
        print(body)
        print(r.text)
        return r
