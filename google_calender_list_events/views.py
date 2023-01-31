import requests
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
import json
# Replace with your own client ID and secret
# Client ID and Client secrets are dummy ones. They are not working anymore. 
CLIENT_ID = '599189350231-9tdurvjgltfbes14ophjpfpm4t4ja8a6.apps.googleusercontent.com'
CLIENT_SECRET = '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'

def google_calendar_init(request):
    # Step 1: Generate the authorization URL
    authorization_base_url = 'https://accounts.google.com/o/oauth2/auth'
    redirect_uri = 'http://127.0.0.1:8000/rest/v1/calendar/redirect/'
    scope = 'https://www.googleapis.com/auth/calendar.readonly'

    authorization_url = f'{authorization_base_url}?client_id={CLIENT_ID}&redirect_uri={redirect_uri}&scope={scope}&response_type=code'

    # Step 2: Redirect the user to the authorization URL
    return redirect(authorization_url)

def google_calendar_redirect(request):
    # Step 3: Handle the redirect and obtain the authorization code
    authorization_code = request.GET.get('code')

    # Step 4: Request the access token
    token_request_url = 'https://oauth2.googleapis.com/token'
    token_request_data = {
        'code': authorization_code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': 'http://127.0.0.1:8000/rest/v1/calendar/redirect/',
        'grant_type': 'authorization_code',
    }

    response = requests.post(token_request_url, data=token_request_data)
    response_data = response.json()
    access_token = response_data.get('access_token')

    # Step 5: Get the events from the user's calendar
    events_url = 'https://www.googleapis.com/calendar/v3/calendars/primary/events'
    events_request_headers = {
        'Authorization': f'Bearer {access_token}',
    }

    events_response = requests.get(events_url, headers=events_request_headers)
    events_data = events_response.json()

    # Step 6: Return the events as a JSON response
    return render(request, 'list.html', context={'data':events_data})
