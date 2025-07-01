# tasks.py

import threading
import time
from .utils import send_whatsapp

def schedule_followup_messages(phone, name):
    def task():
        # First delay - 15 minutes
        time.sleep(900)
        send_whatsapp(phone, name_param=name)

        # Second delay - 1 hour (after the 15 minutes already waited)
        time.sleep(2700)
        send_whatsapp(phone, name_param=name)

    thread = threading.Thread(target=task)
    thread.start()
