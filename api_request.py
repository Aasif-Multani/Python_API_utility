import requests
import csv
import datetime
import configparser


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


# Function to write itineraries to CSV file
def write_to_csv(itineraries):
    # Validate JSON response
    if not isinstance(itineraries, list):
        raise ValueError('Itineraries is not a list')
    for itinerary in itineraries:
        if not isinstance(itinerary, dict):
            raise ValueError('Itinerary is not a dictionary')
        required_keys = ['guid', 'createdAt', 'name', 'itineraryId', 'updatedAt']
        missing_keys = [key for key in required_keys if key not in itinerary]
        if missing_keys:
            for key in missing_keys:
                itinerary[key] = None

    # Write to CSV file
    today = datetime.date.today()
    file_name = str(today) + '_output.csv'
    with open(file_name, 'w', newline='') as csvfile:
        fieldnames = ['guid', 'createdAt', 'name', 'itineraryId', 'updatedAt']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for itinerary in itineraries:
            writer.writerow(itinerary)


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
    write_to_csv(itineraries)

if __name__ == '__main__':
    main()
