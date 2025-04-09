import json
import os

def append_output_csv(results: list, csv_path: str):
    # Ergebnisse in die CSV-Datei anhängen
    with open(csv_path, 'a', encoding='utf-8') as f:
        f.write(";".join(map(str, results)) + "\n")

def append_output_json(student_id: int, results: dict, json_path: str):
    # Anhängen der Ergebnisse an die JSON-Datei
    if not os.path.exists(json_path):
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({student_id: results}, f, ensure_ascii=False, indent=2)
    else:
        with open(json_path, 'r+', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
            data[student_id] = results
            f.seek(0)
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.truncate()

def append_response_json(response, response_json_path, student_id, school_id, response_time):
    # Anhängen der API-Antwort an response.json
    if os.path.exists(response_json_path):
        with open(response_json_path, 'r') as file:
            response_dict = json.load(file)
    else:
        response_dict = {}
    
    # Falls student_id noch nicht vorhanden, initialisieren
    if student_id not in response_dict:
        response_dict[student_id] = {}

    # Die Antwort und Response-Zeit für den bestimmten school_id speichern
    response_dict[student_id][school_id] = {
        "response_time": response_time,
        "response": response
    }

    # Die Daten zurück in die JSON-Datei speichern
    with open(response_json_path, 'w') as file:
        json.dump(response_dict, file, indent=4)