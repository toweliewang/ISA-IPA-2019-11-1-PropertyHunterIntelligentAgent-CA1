from __future__ import print_function
from datetime import datetime, timedelta
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pandas import DataFrame

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def makeAppointment(email, name, projectName, address, recommendedOfferPrice):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    calendarSlot = {}
    email_A = []
    name_A = []
    timeslot_A = []
    project_A = []
    address_A = []
    price_A = []

    for i in range (336):
        now = datetime.utcnow() + timedelta(hours=(8+i))
        date = now.strftime('%m-%dT%H')
        calendarSlot.update({date:'F'})

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    #print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:

        start = event['start'].get('dateTime', event['start'].get('date'))
        start = start[5:13]
        if len(start) == 5:
            start = start + 'T00'

        end = event['end'].get('dateTime', event['end'].get('date'))
        end = end[5:13]
        if len(end) == 5:
            end = end + 'T23'

        calendarSlot[start] = 'S'
        calendarSlot[end] = 'E'
        busy = False

        for i in range (336):
            now = datetime.utcnow() + timedelta(hours=(8+i))
            date = now.strftime('%m-%dT%H')
            if busy:
                if calendarSlot[date] == 'F':
                    calendarSlot[date] = 'B'
                elif calendarSlot[date] == 'E':
                    busy = False        
            if calendarSlot[date] == 'S':
                busy = True
    
    #loop through the calendarSlot and find the earliest appointments
    for i in range (331):
        now = datetime.utcnow() + timedelta(hours=(11+i))
        nowP1 = datetime.utcnow() + timedelta(hours=(12+i))
        nowP2 = datetime.utcnow() + timedelta(hours=(13+i))
        date = now.strftime('%m-%dT%H')
        dateP1 = nowP1.strftime('%m-%dT%H')
        dateP2 = nowP2.strftime('%m-%dT%H')
                
        if int(now.strftime('%H')) > 12 and int(now.strftime('%H')) < 20 and calendarSlot[date] == 'F' and calendarSlot[dateP1] == 'F' and calendarSlot[dateP2] == 'F':
            hour = int(nowP1.strftime('%I'))
            day = nowP1.strftime('%d %b')
            timeslot = f'{day}, {hour}PM'
            email_A.append(email)
            name_A.append(name)
            timeslot_A.append(timeslot)
            project_A.append(projectName)
            address_A.append(address)
            price_A.append(recommendedOfferPrice)

    Appointment_Detail = {'Email':email_A, 'Client Name':name_A, 'Appointment': timeslot_A, 'Project Name': project_A,'Address': address_A, 'Predicted Price': price_A}
    df = DataFrame(Appointment_Detail, columns=['Email','Client Name','Appointment','Project Name','Address','Predicted Price'])
    export_csv = df.to_csv('user_appointment_detail.csv', index = None)