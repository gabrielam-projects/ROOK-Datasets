import json
import csv
from datetime import datetime, timezone

# Abre y carga el archivo JSON
with open('ROOKConnect-Oura-dataset-v2.json') as f:
    data = json.load(f)
    data_sleep = data.get('sleep_health',{}).get('sleep_summaries',{}) # Array with sleep data for different users
    data_activity = data.get('physical_health',{}).get('physical_summaries') # (Array) Summary
    data_activity_event = data.get('physical_health',{}).get('activity_events')
    

# Abre el archivo data_sleep.csv en modo de escritura
with open('data_sleep.csv', 'w', newline='') as f:
    writer = csv.writer(f)

    # Escribe los encabezados de las columnas
    writer.writerow(['user_id', 'sleep_duration', 'time_in_bed', 'light', 'rem', 'deep', 'time_to_fall_asleep', 'awake', 'source'])

    # Itera sobre los elementos en los datos
    for item in data_sleep:
        user_id = item.get("user_id")
        sleep_summary = item.get('sleep_health',{}).get('summary',{}).get('sleep_summary',{}).get('duration')

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
        writer.writerow([user_id, sleep_duration, time_in_bed, light, rem, deep, time_to_fall_asleep, awake, source])


# Extracción de data de activity (summaries)
# Abre el archivo data_activity_event.csv en modo de escritura
with open('data_activity.csv', 'w', newline='') as f:
    writer = csv.writer(f)

    # Escribe los encabezados de las columnas
    writer.writerow(['user_id', 'datetime', 'heart_rate'])

    # Itera sobre los elementos en los datos
    for item in data_activity:
        user_id = item.get('user_id')

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
            writer.writerow([user_id, date, heart_rate])


# Extracción de data de activity (eventos)
# Abre el archivo data_activity.csv en modo de escritura
with open('data_activity_event.csv', 'w', newline='') as f:
    writer = csv.writer(f)

    # Escribe los encabezados de las columnas
    writer.writerow(['user_id', 'activity', 'duration', 'heart_rate_max', 'heart_rate_min', 'heart_rate_avg'])

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

            # Escritura en CSV
            writer.writerow([user_id, activity, duration, low_intensity, moderate_intensity, vigorous_intensity, heart_rate_max, heart_rate_min, heart_rate_avg])