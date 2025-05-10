import requests
import json

# Replace with your WhatsApp API credentials and endpoint
api_url = 'https://graph.facebook.com/v15.0/588725624332260/messages'
access_token = 'EAAQ4t0ZBbUEUBO0yipWDjTddnAB8bYbw7nanICkdPSjs37tEg4IesRxh0UXotjPBUvKmrAxE3zzCvsJysyhf6r2pmpP1yJz9icAnLrtdHdD6aDDSwr4aBp4ZB9kzTnnZBoKMIIeA7OZC9IIyIzib9KyxW8pKidjDGH3ZAwnEwDm4lELZC79y5AXMEDcfAXeZC3ByZBGkp3bWOZBXrJGKKkuKch1ziDckZD'
data = {
    "messaging_product": "whatsapp",
    "to": "+917000454350",  # Replace with the recipient's phone number
    "text": {"body": "Test message from WhatsApp API!"}
}

# Headers for authentication
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {access_token}'
}

# Send the request
response = requests.post(api_url, headers=headers, data=json.dumps(data))

# Check the response
if response.status_code == 200:
    print("WhatsApp message sent successfully!")
else:
    print(f"Failed to send message: {response.status_code}")
    print(response.text)
