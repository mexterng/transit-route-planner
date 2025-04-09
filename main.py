from utils.config_loader import load_config_ini
from utils.api_handler import query_connection, parse_response
from utils.file_handler import append_output_json, append_output_csv, append_response_json

import pandas as pd
import os
from time import sleep
import json

def main():
    # Konfiguration laden
    config = load_config_ini('config.ini')
    
    # Schüler und Schulen aus CSV-Datei einlesen (ID, Adresse)
    students_df = pd.read_csv(config.students_csv, delimiter=";", dtype=str)
    students_dict = students_df.to_dict(orient="records")
    schools_df = pd.read_csv(config.schools_csv, delimiter=";", dtype=str)
    schools_dict = schools_df.to_dict(orient="records")

    # Output-Ordner erstellen, falls nicht vorhanden
    os.makedirs(config.output_path, exist_ok=True)

    # Ergebnisdateien
    output_json_path = os.path.join(config.output_path, "output.json")
    response_json_path = os.path.join(config.output_path, "response.json")
    output_csv_path = os.path.join(config.output_path, "output.csv")

    # CSV-Überschriften in output.csv erstellen
    header = ['student_id', 'address']
    for school in schools_dict:
        header.append(f"{school['school_id']}_duration")
        header.append(f"{school['school_id']}_transfers")
    append_output_csv(header, output_csv_path)
    
    # API-Abfragen durchführen
    for student in students_dict:
        student_api_fails = 0
        student_id = student['student_id']
        student_address = student['address']
        results_csv = [student_id, student_address]
        results_json = {'address': student_address, 'schools': {}}
        for school in schools_dict:
            school_id = school['school_id']
            school_address = school['address']
            response = query_connection(config.api_key, student_address, school_address, config.datetime)
            
            if response['response']['status'] != 'OK':
                student_api_fails += 1            
            if student_api_fails > 5:
                break

            # Speichern der API Response in response.json
            append_response_json(response['response'], response_json_path, student_id, school_id, response['response_time'])

            parsed = parse_response(response)
            results_csv.append(parsed["duration"])
            results_csv.append(parsed["transfers"])

            # Ergebnisse für JSON
            results_json["schools"][str(school_id)] = {
                "duration": parsed["duration"],
                "transfers": parsed["transfers"]
            }
            sleep(1)  # Rate limit einhalten

        # Ergebnisse in CSV und JSON speichern
        append_output_csv(results_csv, output_csv_path)
        append_output_json(student_id, results_json, output_json_path)

def reset_output_files():
    # Konfiguration laden
    config = load_config_ini('config.ini')
    
    # Output-Ordner erstellen, falls nicht vorhanden
    os.makedirs(config.output_path, exist_ok=True)

    # Dateipfade
    output_json_path = os.path.join(config.output_path, "output.json")
    response_json_path = os.path.join(config.output_path, "response.json")
    output_csv_path = os.path.join(config.output_path, "output.csv")

    # Leere Dateien erstellen, falls sie existieren
    with open(output_json_path, 'w') as output_json_file:
        output_json_file.truncate(0)  # Datei leeren (wenn sie existiert)
        json.dump({}, output_json_file)
        
    with open(response_json_path, 'w') as response_json_file:
        response_json_file.truncate(0)  # Datei leeren (wenn sie existiert)
        json.dump({}, response_json_file)
    
    with open(output_csv_path, 'w', newline='') as output_csv_file:
        output_csv_file.truncate(0)  # Datei leeren (wenn sie existiert)
    

if __name__ == '__main__':
    reset_output_files()
    main()