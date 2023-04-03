# Contains the Task class and its methods for managing tasks, sub-tasks, actions, parameters, schedules, motivations,
# and recurrences.

from datetime import datetime, timedelta
from communication.sms_handler import send_sms


class Task:


    def __init__(self, task_type, description, parameters, due_time=datetime.now(), recurring=False,
                 recurring_interval=None):
        self.task_type = task_type
        self.description = description
        self.parameters = parameters
        self.due_time = due_time
        self.recurring = recurring
        self.recurring_interval = recurring_interval

    @classmethod
    def from_dict(cls, task_data):
        task_type = task_data.get("action") or "unknown"
        description = task_data.get("description") or "error"
        parameters = task_data.get("parameters") or {}
        due_time = datetime.fromisoformat(task_data.get("due_time") or datetime.now().isoformat())
        recurring = task_data.get("recurring") or False
        recurring_interval = task_data.get("recurring_interval") or 0

        return cls(task_type, description, parameters, due_time, recurring, recurring_interval)

    def send_sms_task(self):
        body = self.parameters.get("message")
        if not body:
            print("[ERROR] send_sms_task: invalid task, missing 'parameters.message'")
            return
        send_sms(body)

    # def to_dict(self):
    #     return {
    #         "task_type": self.task_type,
    #         "due_time": self.due_time.isoformat(),
    #         "recurring": self.recurring,
    #         "recurring_interval": self.recurring_interval
    #     }

    def is_due(self, current_time):
        return current_time >= self.due_time

    def execute(self, pita):
        task_action_map = {
            "search": lambda arguments: print("search"),
            "summarize": lambda arguments: print("summarize"),
            "email": lambda arguments: print("email"),
            "sms": lambda task: task.send_sms_task(),
            "send_email": lambda arguments: print("send_email"),
        }

        if self.task_type not in task_action_map:
            print(f"missing implementation for: {self.task_type}")
            return
        task_action_map[self.task_type](self)

    def is_recurring(self):
        return self.recurring

    def update_next_execution_time(self):
        if self.is_recurring():
            self.due_time += timedelta(seconds=self.recurring_interval)
