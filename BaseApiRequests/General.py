from datetime import datetime
import re

class General:
    def generate_now_time(self):
        return datetime.now().strftime("%H:%M:%S")

    def validate_string_is_in_qb_format(self,string):
        try:
            datetime.strptime(string,'%Y-%m-%dT%H:%M:%SZ')
            return True
        except ValueError:
            return False
    def validate_email_format(self,string):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if(re.fullmatch(regex,string)):
            return True
        else:
            return False