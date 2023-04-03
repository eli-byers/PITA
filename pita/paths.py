import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(
    __file__))  # This is your Project Root

# Add the parent directory of the current file to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))