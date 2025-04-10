import requests
import time
import datetime
from typing import Dict

def query_connection(api_key: str, origin: str, destination: str, arrival_time_str: str) -> Dict:
    url = 'https://maps.googleapis.com/maps/api/directions/json'
    arrival_time_unix = int(datetime.datetime.strptime(arrival_time_str, '%Y-%m-%dT%H:%M:%S').timestamp())
    params = {
        'origin': origin,
        'destination': destination,
        'mode': 'transit',
        'arrival_time': arrival_time_unix,
        'key': api_key,
        'transit_routing_preference': 'fewer_transfers',
        'language': 'de'
    }
    try:
        response_time = time.time()
        response = requests.get(url, params=params, timeout=10)
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