from __future__ import print_function
import httplib2
import os
import json
import urllib2
# from urllib2 import HTTPError
from apiclient import discovery
from apiclient import errors
import oauth2client
from oauth2client import client
from oauth2client import tools
from quickstart import get_credentials
import base64
from email.mime.text import MIMEText

def CreateMessage(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string())}

def CreateDraft(service, user_id, message_body):
  """Create and insert a draft email. Print the returned draft's message and id.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message_body: The body of the email message, including headers.

  Returns:
    Draft object, including draft id and message meta data.
  """
  try:
    message = {'message': message_body}
    draft = service.users().drafts().create(userId=user_id, body=message).execute()
    send = (service.users.drafts().send(userId=user_id,draft=draft).execute())
    print('sent id: %s\n'%(send['id']))
    print('Draft id: %s\nDraft message: %s' % (draft['id'], draft['message']))

    # return json.dumps(draft,ensure_ascii=False)
  except errors.HttpError as error:
    print("Hello %s",error)
    # return None

def sendMessage(service, user_id, message):
  try:
    message = (service.users().messages().send(userId=user_id, body=message).execute())
    print('Message Id: %s' % message['id'])
    return message
  except errors.HttpError, error:
    print('An error occurred: %s' % error)

def main():
  credentials = get_credentials()
  http = credentials.authorize(httplib2.Http())
  service = discovery.build('gmail', 'v1', http=http)
  message_body = CreateMessage('dnjha240@gmail.com','sjha1519@gmail.com','Test again','I am testing again')
  CreateDraft(service,'me',message_body)


if __name__ == '__main__':
    main()