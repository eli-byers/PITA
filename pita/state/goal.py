# Contains the Goal class and its methods for managing goals
import json
import os
from datetime import datetime
from paths import ROOT_DIR
from utils.config import GOAL_HISTORY_LOG_PATH

from state.task import Task
from communication.sms_handler import delete_sms

abs_goal_history_log_path = f"{ROOT_DIR}/{GOAL_HISTORY_LOG_PATH}"

class Goal:
    def __init__(self, command, tasks: [Task], completion_handler):
        self.command = command
        self.tasks = tasks
        self.creation_time = datetime.now()
        self.completion_time = None
        self.completion_handler = completion_handler

    @staticmethod
    def parse_command(sms=None, terminal=None):
        # TODO: add command parsing with LLM
        if sms:
            task = Task(
                task_type="sms",
                description="Respond to sms",
                parameters={"message": "Response to: {}".format(sms.get("body"))}
            )
            return Goal("Respond to sms", [task], lambda: delete_sms(sms.get("sid")))

    def all_tasks_completed(self):
        return len(self.tasks) == 0

    def save_to_history_log(self):
        delta = self.completion_time - self.creation_time
        log = "[{}][{}][Δ{}] {}\n".format(self.creation_time, self.completion_time, delta, self.command)
        os.makedirs(os.path.dirname(abs_goal_history_log_path), exist_ok=True)
        with open(abs_goal_history_log_path, "a") as f:
            f.write(log)

    def process_and_execute_tasks(self, pita):
        current_time = datetime.now()
        for task in self.tasks:
            if task.is_due(current_time):
                task.execute(pita)
                if task.is_recurring():
                    task.update_next_execution_time()
                else:
                    self.tasks.remove(task)
        if self.all_tasks_completed():
            self.completion_time = datetime.now()
            self.completion_handler()
            self.save_to_history_log()

    def to_dict(self):
        return {
            "command": self.command,
            "creation_time": self.creation_time.isoformat(),
            "completion_time": self.creation_time.isoformat(),
        }
