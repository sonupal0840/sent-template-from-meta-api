# yourapp/tasks.py
import requests
from .utils import send_template_message_to_numbers

def fetch_contacts_and_send_messages():
    print("Running scheduled WhatsApp sender...")

    # Step 1: Call your external API
    
    response = requests.get('https://callapi.sherlockslife.com/api/Values/contacts/')
    if response.status_code != 200:
        print("Failed to fetch contacts")
        return

    contacts = response.json()
    # contacts = [{'phone':8989512905,'name':'sonu'}]

    # Step 2: Loop and send template messages
    for contact in contacts:
        phone = contact.get('phone')
        name = contact.get('name', 'User')
        if phone:
            # Prepare variables dict for template parameters
            variables = {"1": name}
            try:
                send_template_message_to_numbers(
                    template_name='status_updated',  # or your template name
                    numbers=[str(phone)],
                    variables=variables,
                    language="en_US"
                )
                print(f"Message sent to {phone}")
            except Exception as e:
                print(f"Failed to send message to {phone}: {e}")
