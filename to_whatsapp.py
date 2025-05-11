import requests
import json

# WhatsApp API endpoint and token
api_url = 'https://graph.facebook.com/v15.0/588725624332260/messages'
access_token = 'EAAQ4t0ZBbUEUBOzN7bcQyIXOQ0ZBg4W9n3ZAXADx47YvbCvCKxG93JIZB9EUP6oDYZArH3WYBaeaFRZAa8ZBOcOV3fVdqXNuvU5LrV3ZBx4D7QT1ZCkdsVEqBKSYQz0aTiZCHIngKcxnn4zSUTbuseARyMkZCv6oTnmWPZAJHDk5PaA55Nz23iYz4AbZAZCAOyDZAQYTBR253Caz0OhDz0EbA9w1vTLPzohec4ZD'

# Recipient info
mobile_number = '+917000454350'  # Replace with recipient
name = 'Sonu'  # This will fill the {{1}} placeholder in the template

# Payload for template message
data = {
    "messaging_product": "whatsapp",
    "to": mobile_number,
    "type": "template",
    "template": {
        "name": "account_creation",  # Replace with your approved template name
        "language": {
            "code": "en_US"  # Use "hi" if your template is in Hindi
        },
        "components": [
            {
                "type": "body",
                "parameters": [
                    {
                        "type": "text",
                        "text": name
                    }
                ]
            }
        ]
    }
}

# Headers
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {access_token}'
}

# Send request
response = requests.post(api_url, headers=headers, data=json.dumps(data))

# Check response
if response.status_code == 200:
    print("✅ WhatsApp template message sent successfully!")
else:
    print(f"❌ Failed to send message: {response.status_code}")
    print(response.text)
