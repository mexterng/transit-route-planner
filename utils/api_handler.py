import requests
import time
import datetime
from typing import Dict

def query_connection(api_key: str, origin: str, destination: str, arrival_time_str: str) -> dict:
    url = 'https://routes.googleapis.com/directions/v2:computeRoutes'
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': api_key,
        'X-Goog-FieldMask': 'routes.legs.stepsOverview.multiModalSegments.travelMode,routes.legs.duration'
    }

    arrival_time_rfc3339 = datetime.datetime.strptime(arrival_time_str, '%Y-%m-%dT%H:%M:%S').isoformat() + 'Z'
    body = {
        'origin': {'address': origin},
        'destination': {'address': destination},
        'travelMode': 'TRANSIT',
        'arrivalTime': arrival_time_rfc3339,
        'languageCode': 'de',
        'transitPreferences': {
            'routingPreference': 'FEWER_TRANSFERS',
        }
    }
    try:
        response_time = time.time()
        response = requests.post(url, headers=headers, json=body, timeout=10)
        response_time = time.time() - response_time
        response.raise_for_status()
        response = response.json()
        response['routes'][0]['legs'][0]['end_address'] = destination
        response['status'] = "OK"
        return {'response_time': response_time, 'response': response}
    except requests.RequestException as e:
        print(f"Fehler bei API-Anfrage: {e}")
        print(response.content)
        response = response.json()
        return {'response_time': -1, 'response': {'status': response['error']['status']}}
    except KeyError as e:
        print(response)
        return {'response_time': -1, 'response': {'status': "EMPTY_RESPONSE"}}

def parse_response(data: Dict) -> Dict[str, int]:
    response = data['response']
    if response.get('status') != 'OK' or not response.get('routes'):
        return {'address': '', 'departure_time': -1, 'arrival_time': -1, 'duration': -1, 'transfers': -1}

    try:
        leg = response['routes'][0]['legs'][0]
        address = leg['end_address']
        duration = int(int(leg['duration'].rstrip('s')) // 60)  # seconds to minutes
        transfers = sum(1 for step in leg['stepsOverview']['multiModalSegments'] if step.get('travelMode') == 'TRANSIT') - 1
        return {'address': address, 'duration': duration, 'transfers': transfers}
    except (KeyError, IndexError, TypeError):
        return {'address': '', 'departure_time': -1, 'arrival_time': -1, 'duration': -1, 'transfers': -1}