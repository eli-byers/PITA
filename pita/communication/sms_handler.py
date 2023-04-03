# Handles the retrieval and parsing of SMS messages. Contains the functions for parsing goals and recurrence from
# messages.

from twilio.rest import Client

from utils.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, YOUR_PHONE_NUMBER

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def send_sms(body):
    message = client.messages.create(
        body=body,
        from_=TWILIO_PHONE_NUMBER,
        to=YOUR_PHONE_NUMBER
    )


def check_sms():
    messages = client.messages.list(from_=YOUR_PHONE_NUMBER, to=TWILIO_PHONE_NUMBER)
    new_messages = []

    for message in messages:
        if message.direction == 'inbound':
            new_messages.append({
                "body": message.body,
                "sid": message.sid
            })

    return new_messages


def delete_sms(message_sid):
    client.messages(message_sid).delete()

# Example usage
# send_sms(YOUR_PHONE_NUMBER, "Test message")
