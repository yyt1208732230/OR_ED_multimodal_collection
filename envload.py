import os
import ast
import numpy as np
import logging
from dotenv import load_dotenv

# Initial
load_dotenv()

PROJECT_NAME = os.getenv('PROJECT_NAME')
RGB_PATH = os.getenv('RGB_PATH')