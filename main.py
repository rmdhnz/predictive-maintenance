#!/usr/bin/env python3
import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from app import app

if __name__ == "__main__":
    app()
