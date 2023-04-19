import requests
import csv
import configparser

import json
import os
from datetime import datetime


# Function to call /pull/token API endpoint and return token
def get_token(client_id, auth_basic):
    url = 'https://axustravelapp.com/api/v1/pull/token'
    headers = {'Authorization': auth_basic, 'clientId': client_id}

    response = requests.get(url, headers=headers)
    response_json = response.json()

    if response.status_code == 200:
        token = response_json.get('token')
        if token:
            return token
        else:
            raise ValueError('Token not found in response JSON')
    else:
        errors = response_json.get('errors', [])
        error_msg = ', '.join(errors)
        raise ValueError(f'Error getting token: {error_msg}')


# Function to call /pull/itineraries API endpoint and return itineraries
def get_itineraries(token, client_id, auth_basic):
    url = f'https://axustravelapp.com/api/v1/pull/itineraries?token={token}'
    headers = {'Authorization': auth_basic, 'clientId': client_id}

    response = requests.get(url, headers=headers)
    response_json = response.json()

    if response.status_code == 200:
        itineraries = response_json.get('itineraries', [])
        return itineraries
    else:
        errors = response_json.get('errors', [])
        error_msg = ', '.join(errors)
        raise ValueError(f'Error getting itineraries: {error_msg}')


# Function to write itineraries to CSV, JSON, and plain text file
def write_to_file(output_file_path, data):
    """
    Write the given data to a CSV, JSON, and plain text file.

    :param output_file_path: Path to the output file directory.
    :param data: List of dictionaries containing itinerary data.
    """

    # Create the output directory if it doesn't exist.
    os.makedirs(output_file_path, exist_ok=True)

    # Define the filenames for the CSV, JSON, and text files.
    today = datetime.now().strftime('%Y-%m-%d')
#    csv_file_name = f'{today}_output.csv'
    json_file_name = f'{today}_output.json'
#    text_file_name = f'{today}_output.txt'

    # Define the paths to the CSV, JSON, and text files.
#    csv_file_path = os.path.join(output_file_path, csv_file_name)
    json_file_path = os.path.join(output_file_path, json_file_name)
#    text_file_path = os.path.join(output_file_path, text_file_name)

    # Write to the CSV file.
#    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
#        writer = csv.writer(csv_file)
#        writer.writerow(['guid', 'created', 'name', 'itinerary', 'updated'])
#        for row in data:
#            writer.writerow([row.get('guid', ''),
#                             row.get('created', ''),
#                             row.get('name', ''),
#                             row.get('itinerary', ''),
#                             row.get('updated', '')])

    # Write to the JSON file.
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    # Write to the plain text file.
 #   with open(text_file_path, 'w', encoding='utf-8') as text_file:
 #       for row in data:
 #           text_file.write(f"{row.get('guid', '')}\t"
 #                           f"{row.get('created', '')}\t"
 #                           f"{row.get('name', '')}\t"
 #                           f"{row.get('itinerary', '')}\t"
 #                           f"{row.get('updated', '')}\n")


# Function to validate the client_id and auth_basic parameters
def validate_input(client_id, auth_basic):
    if not client_id:
        raise ValueError('client_id parameter is required')
    if not auth_basic:
        raise ValueError('auth_basic parameter is required')


# Main function to call other functions in sequence
def main():
    # Read the client_id and auth_basic from config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    client_id = config['api']['client_id']
    auth_basic = config['api']['auth_basic']

    validate_input(client_id, auth_basic)
    token = get_token(client_id, auth_basic)
    itineraries = get_itineraries(token, client_id, auth_basic)
    write_to_file(itineraries)


if __name__ == '__main__':
    main()
