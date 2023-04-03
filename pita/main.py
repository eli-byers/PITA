# Main script to run the PITA system. Includes main loop, SMS checking, and scheduled tasks handling.

import time

from communication.sms_handler import check_sms, send_sms
from state.pita import Pita
from state.goal import Goal


def main():
    pita = Pita.init()
    # send_sms("PITA is up and running")

    while True:
        # now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # print(f"[{now}] Looping")

        # get new commands
        received_sms = check_sms()

        # parse commands from sms
        goals = list(map(lambda sms: Goal.parse_command(sms), received_sms))
        if len(goals):
            pita.add_goals(goals)

        # handle current goals
        pita.process_and_execute_goals()

        # pita.lazy_save_state()
        time.sleep(5)


if __name__ == "__main__":
    main()
