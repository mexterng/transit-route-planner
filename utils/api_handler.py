import requests
import time
import datetime
from typing import Dict, List

def query_connection(api_key: str, origin: str, destinations: list, arrival_time_str: str) -> dict:
    url = 'https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix'
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': api_key,
        'X-Goog-FieldMask': '*'}

    arrival_time_rfc3339 = datetime.datetime.strptime(arrival_time_str, '%Y-%m-%dT%H:%M:%S').isoformat() + 'Z'
    destination_list = [{'waypoint': {'address': school['address']}} for school in destinations]
    body = {
        'origins': [{'waypoint': {'address': origin}}],
        'destinations': destination_list,
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
        return {'response_time': response_time, 'response': response.json()}
    except requests.RequestException as e:
        print(f"Fehler bei API-Anfrage: {e}")
        return {'response_time': -1, 'response': {"status": "REQUEST_FAILED"}}

def parse_response(data: Dict) -> Dict[str, int]:
    response = data['response']
    if response.get('status') != 'OK' or not response.get('routes'):
        return {'address': '', 'departure_time': -1, 'arrival_time': -1, 'duration': -1, 'transfers': -1}

    try:
        leg = response['routes'][0]['legs'][0]
        address = leg['end_address']
        departure_time = leg['departure_time']['text']
        arrival_time = leg['arrival_time']['text']
        duration = leg['duration']['value'] // 60  # seconds to minutes
        transfers = sum(1 for step in leg['steps'] if step.get('travel_mode') == 'TRANSIT') - 1
        return {'address': address, 'departure_time': departure_time, 'arrival_time': arrival_time, 'duration': duration, 'transfers': transfers}
    except (KeyError, IndexError, TypeError):
        return {'address': '', 'departure_time': -1, 'arrival_time': -1, 'duration': -1, 'transfers': -1}