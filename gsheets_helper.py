from __future__ import print_function
import httplib2
import os
from gsheets_enums import *

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'TotRC Pythoc'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    credentials_filename = "sheets.googleapis.com-python-test.json"

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, credentials_filename)

    store = Storage(credential_path)
    credentials = store.get()
    # print(helpers.print_dict(credentials.__dict__))
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to', credential_path)
    return credentials


def read_cells(spreadsheet_id, cell_range) -> list or None:
    discovery_url = 'https://sheets.googleapis.com/$discovery/rest?version=v4'

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discovery_url)

    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=cell_range).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')

    return values


def update_cells(spreadsheet_id, cell_range, values,
                 value_input_option=ValueInputOption.INPUT_VALUE_OPTION_UNSPECIFIED,
                 major_dimension=Dimension.DIMENSION_UNSPECIFIED):
    discovery_url = 'https://sheets.googleapis.com/$discovery/rest?version=v4'

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discovery_url)

    value_range_body = {
        "range": cell_range,
        "majorDimension": major_dimension,
        "values": values
    }

    request = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=cell_range,
                                                     valueInputOption=value_input_option, body=value_range_body)
    response = request.execute()

    print(response)


def main():
    spreadsheetId = '15GA8fKb70gAdEV5O32ow8sjwBZBkGXoI94CYzZntSCg'
    rangeName = 'A1:E5'

    values = read_cells(spreadsheetId, rangeName)

    if values:
        print(*values, sep="\n")

    update_cells(spreadsheetId, rangeName, [["{}{}".format(i, x) for i in "ABCDE"] for x in range(1, 6)])


if __name__ == '__main__':
    main()
