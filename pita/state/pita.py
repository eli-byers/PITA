# Contains the InternalState class and its methods for managing user information, AI information, goals, tasks,
# and memories.
import json
import os
from datetime import datetime, timedelta

from .goal import Goal
from paths import ROOT_DIR
from utils.config import STATE_FILE_PATH, STATE_SAVE_PERIOD_SECONDS

abs_state_file_path = f"{ROOT_DIR}/{STATE_FILE_PATH}"


class Pita:
    def __init__(self):
        self.updated_at = datetime.now()
        self.user_information = {}
        self.ai_information = {}
        self.goals = []
        self.memories = []

    def update_user_information(self, key, value):
        self.user_information[key] = value

    def update_ai_information(self, key, value):
        self.ai_information[key] = value

    def add_goal(self, goal):
        self.goals.append(goal)

    def add_goals(self, goals):
        self.goals.extend(goals)

    def add_memory(self, memory):
        self.memories.append(memory)

    def get_context(self):
        # Combine user information, AI information, goals, and memories to generate context
        context = {
            'user_information': self.user_information,
            'ai_information': self.ai_information,
            'goals': self.goals,
            'memories': self.memories
        }
        return context

    def load_from_file(self):
        with open(abs_state_file_path, "r") as f:
            data = json.load(f)

        self.updated_at = datetime.fromisoformat(
            data.get("updated_at") or datetime.now().isoformat())
        self.user_information = data.get("user_information", {})
        self.ai_information = data.get("ai_information", {})
        self.goals = [Goal.from_dict(g) for g in data.get("goals", [])]
        self.memories = data.get("memories", [])

    def lazy_save_state(self):
        state_save_period = datetime.now() - timedelta(seconds=STATE_SAVE_PERIOD_SECONDS)
        if self.updated_at <= state_save_period:
            self.save_to_file()

    def save_to_file(self):
        self.updated_at = datetime.now()
        data = {
            "updated_at": self.updated_at.isoformat(),
            "user_information": self.user_information,
            "ai_information": self.ai_information,
            "goals": [g.to_dict() for g in self.goals],
            "memories": self.memories,
        }
        with open(abs_state_file_path, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def init():
        pita = Pita()
        if os.path.exists(abs_state_file_path):
            print(
                f"Initializing PITA with state from: {abs_state_file_path}")
            pita.load_from_file()
        else:
            print(
                f"No PITA state found, creating a new state at: {abs_state_file_path}")
            pita.save_to_file()
        return pita

    def process_and_execute_goals(self):
        completed_goals = []
        for goal in self.goals:
            goal.process_and_execute_tasks(self)
            if goal.all_tasks_completed():
                completed_goals.append(goal)
                self.memories.append(goal.to_dict())

        # Remove completed goals from the list of goals
        for completed_goal in completed_goals:
            self.goals.remove(completed_goal)
