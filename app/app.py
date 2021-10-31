from __future__ import print_function
from flask import Flask, render_template, request
import pandas as pd
import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of the spreadsheet.
SPREADSHEET_ID = '1SsF-DZRxTpxeWKLTr-RQVbVl7AxzGP1HH-fPd868FZ8'
DATA_TO_PULL = 'Sheet1'


app = Flask(__name__)


@app.route('/')
def form():
    return render_template('index.html')


@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'GET':
        return "Go to the homepage to enter your ID."

    if request.method == 'POST':
        id_str = request.form

        if len(id_str) > 20:
            return "Not a valid input. Input should be less than 20 characters."

        #id_str = id_str.upper()

        # The Magic
        raw = pull_sheet_data(SCOPES, SPREADSHEET_ID, DATA_TO_PULL)
        df = pd.DataFrame(raw[1:], columns=raw[0])  # Rows 1 and on are data, Row 0 is column labels
        result = df.loc[df['Student ID'] == id_str].to_dict('records')
        if result:
            return result[0]['Points']
        else:
            return "Requested ID is not in the record."


@app.route('/about')
def about():
    return render_template('index2.html')


if __name__ == '__main__':
    app.run()


# https://towardsdatascience.com/how-to-import-google-sheets-data-into-a-pandas-dataframe-using-googles-api-v4-2020-f50e84ea4530
def gsheet_api_check(SCOPES):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


def pull_sheet_data(SCOPES, SPREADSHEET_ID, DATA_TO_PULL):
    creds = gsheet_api_check(SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=DATA_TO_PULL).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        rows = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                  range=DATA_TO_PULL).execute()
        data = rows.get('values')
        print("COMPLETE: Data copied")
        return data

#import streamlit as st
#import pandas as pd

#def main():
    #IDstr = input("Enter UMBC Student ID: ")
    #if len(IDstr) > 20:
        #print("Not a valid input. Input should be less than 20 characters.\n")
        #return
    #IDstr = IDstr.upper()

    #df = pd.read_excel('C://Users/Emma/Downloads/hackumbc_cwit_test_spreadsheet.xlsx')

    #print(df.columns)
    # Index(['name', 'UMBC id', 'Points', 'Unnamed: 3', 'Unnamed: 4'], dtype='object')

    #result = df.loc[df['UMBC id'] == IDstr].to_dict('records')
    #if result:
        #print(result[0]['Points'])
    #else:
        #print(IDstr+" is not in the record.\n")
#Sheet1 = pd.read_excel("C://Users/Emma/Downloads/hackumbc_cwit_test_spreadsheet.xlsx", index_col=0, names=['UMBC id', 'Points'], sheet_name="Sheet1", usecols="B,C")
#while label in Sheet1.items() != "UMBC id":
#Sheet1.loc[Sheet1['UMBC id'] == IDstr]

#for label, content in Sheet1.items():
 #   print("label: "+label+'\n')
  #  if (content[0] == IDstr):
   #     print("hello\n")
    #    print(content+'\n')

    #print(f'label: {label}')
    #print(f'content: {content}', sep='\n')

#st.write("Hello World!")
