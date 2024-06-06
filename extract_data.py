import json
import csv
import os
from datetime import datetime

def process_json_file(file_path):
    # Abre y carga el archivo JSON
    with open(file_path) as f:
        data = json.load(f)
        data_sleep = data.get('sleep_health',{}).get('sleep_summaries',{}) 
        data_activity = data.get('physical_health',{}).get('physical_summaries') 
        data_activity_event = data.get('physical_health',{}).get('activity_events') 

    # Define el nombre del archivo CSV
    csv_file_sleep = 'data_sleep.csv'
    csv_file_activity = 'data_activity.csv'
    csv_file_activity_event = 'data_activity_event.csv'

    # Verifica si los archivos CSV ya existen
    file_exists_sleep = os.path.isfile(csv_file_sleep)
    file_exists_activity = os.path.isfile(csv_file_activity)
    file_exists_activity_event = os.path.isfile(csv_file_activity_event)
    
    # ----- SLEEP DATA ---------------------------------------------------------------------------

    # Abre los archivos CSV en modo append ('a')
    with open(csv_file_sleep, 'a', newline='') as f:
        writer = csv.writer(f)

        # Si el archivo no existe, escribe los encabezados de las columnas
        if not file_exists_sleep:
            writer.writerow(['user_id', 'date', 'sleep_duration', 'time_in_bed', 'light', 'rem', 'deep', 'time_to_fall_asleep', 'awake', 'source'])

        # Itera sobre los elementos en los datos
        for item in data_sleep:
            user_id = item.get("user_id")
            sleep_summary = item.get('sleep_health',{}).get('summary',{}).get('sleep_summary',{}).get('duration')

            datetime_str = sleep_summary.get('sleep_start_datetime_string')
            # Ajustar formato de fecha
            dt = datetime.fromisoformat(datetime_str)
            dt = dt.replace(tzinfo=None)
            date = dt.isoformat()

            # Datos relevantes
            sleep_duration = sleep_summary.get('sleep_duration_seconds_int')
            time_in_bed = sleep_summary.get('time_in_bed_seconds_int')
            light = sleep_summary.get('light_sleep_duration_seconds_int')
            rem = sleep_summary.get('rem_sleep_duration_seconds_int')
            deep = sleep_summary.get('deep_sleep_duration_seconds_int')
            time_to_fall_asleep = sleep_summary.get('time_to_fall_asleep_seconds_int')
            awake = sleep_summary.get('time_awake_during_sleep_seconds_int')

            # Source
            source = item.get('sleep_health',{}).get('summary',{}).get('sleep_summary',{}).get('metadata',{}).get('sources_of_data_array')

            # Escribe los datos en el archivo CSV
            writer.writerow([user_id, date, sleep_duration, time_in_bed, light, rem, deep, time_to_fall_asleep, awake, source])

    # ----- ACTIVITY DATA ---------------------------------------------------------------------------
        
    # Abre los archivos CSV en modo append ('a')
    with open(csv_file_activity, 'a', newline='') as f:
        writer = csv.writer(f)

        # Si el archivo no existe, escribe los encabezados de las columnas
        if not file_exists_activity:
            writer.writerow(['user_id', 'datetime', 'heart_rate', 'sources'])
        
        # Itera sobre los elementos en los datos
        for item in data_activity:
            user_id = item.get('user_id')

            # Source
            source = item.get('physical_health',{}).get('summary',{}).get('physical_summary',{}).get('metadata',{}).get('sources_of_data_array')

            # Datos relevantes
            granular_data = item.get('physical_health',{}).get('summary',{}).get('physical_summary',{}).get('heart_rate',{}).get('hr_granular_data_array')
            for item in granular_data:
                heart_rate = item.get('hr_bpm_int')
                datetime_str = item.get('datetime_string')

                # Ajustar formato de fecha
                dt = datetime.fromisoformat(datetime_str)
                dt = dt.replace(tzinfo=None)
                date = dt.isoformat()

                # Escritura en CSV
                writer.writerow([user_id, date, heart_rate, source])

    # ----- ACTIVITY SUMMARIES ---------------------------------------------------------------------------

    # Extracción de data de activity (eventos)
    # Abre los archivos CSV en modo append ('a')
    with open(csv_file_activity_event, 'a', newline='') as f:
        writer = csv.writer(f)

        # Si el archivo no existe, escribe los encabezados de las columnas
        if not file_exists_activity_event:
            writer.writerow(['user_id', 'datetime', 'activity', 'duration', 'low_intensity', 'moderate_intensity', 'vigorous_intensity', 'heart_rate_max', 'heart_rate_min', 'heart_rate_avg', 'source'])

        # Itera sobre los elementos en los datos
        for item in data_activity_event:
            user_id = item.get('user_id')

            # Datos relevantes
            events = item.get('physical_health',{}).get('events',{}).get('activity_event')
            for item in events:
                activity = item.get('activity',{}).get('activity_type_name_string')
                duration = item.get('activity',{}).get('activity_duration_seconds_int')
    
                low_intensity = item.get('activity',{}).get('low_intensity_seconds_int')
                moderate_intensity = item.get('activity',{}).get('moderate_intensity_seconds_int')
                vigorous_intensity = item.get('activity',{}).get('vigorous_intensity_seconds_int')

                heart_rate_max = item.get('heart_rate',{}).get('hr_maximum_bpm_int')
                heart_rate_min = item.get('heart_rate',{}).get('hr_minimum_bpm_int')
                heart_rate_avg = item.get('heart_rate',{}).get('hr_avg_bpm_int')

                datetime_str = item.get('metadata',{}).get('datetime_string')

                # Ajustar formato de fecha
                dt = datetime.fromisoformat(datetime_str)
                dt = dt.replace(tzinfo=None)
                date = dt.isoformat()

                # Source
                source = item.get('metadata',{}).get('sources_of_data_array')

                # Escritura en CSV
                writer.writerow([user_id, date, activity, duration, low_intensity, moderate_intensity, vigorous_intensity, heart_rate_max, heart_rate_min, heart_rate_avg, source])


# Llamada de la función
process_json_file('ROOK Datasets/ROOKConnect-Garmin-dataset-v2.json')
process_json_file('ROOK Datasets/ROOKConnect-Oura-dataset-v2.json')
process_json_file('ROOK Datasets/ROOKConnect-Whoop-dataset-v2.json')
process_json_file('ROOK Datasets/ROOKConnect-Polar-dataset-v2.json')

# Updated
process_json_file('ROOK Datasets/Updated 2024-04-26/ROOKConnect-Apple Health-dataset-v2.json')
process_json_file('ROOK Datasets/Updated 2024-04-26/ROOKConnect-Fitbit-dataset-v2 (1).json')
process_json_file('ROOK Datasets/Updated 2024-04-26/ROOKConnect-Garmin-dataset-v2.json')
process_json_file('ROOK Datasets/Updated 2024-04-26/ROOKConnect-Health Connect-dataset-v2.json')
process_json_file('ROOK Datasets/Updated 2024-04-26/ROOKConnect-Oura-dataset-v2.json')
process_json_file('ROOK Datasets/Updated 2024-04-26/ROOKConnect-Polar-dataset-v2.json')
process_json_file('ROOK Datasets/Updated 2024-04-26/ROOKConnect-Whoop-dataset-v2.json')
process_json_file('ROOK Datasets/Updated 2024-04-26/ROOKConnect-Withings-dataset-v2.json')