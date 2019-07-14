import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import os
import xlsxwriter


def end_pt(input_give):
    return (len(input_give)+1)

#using the google drive api
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('D:/Cbackup/Users/mahan.das/AppData/Local/Programs/Python/Python36/client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open("DateSchedule 2018").sheet1

#getting values from sheet 

currency = sheet.col_values(1)
Tenor = sheet.col_values(2)
Trade_date = sheet.col_values(3)
Issue_date = sheet.col_values(4)
Final_fixing_date = sheet.col_values(5)
Maturity_date = sheet.col_values(6)
First_call = sheet.col_values(7)
First_KO = sheet.col_values(8)

#define variables

count = 0
start_pt = 2
T_0 = datetime.datetime.today().strftime('%d-%b-%y')
T_1 = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%d-%b-%y')
T_2 = (datetime.datetime.today() + datetime.timedelta(days=2)).strftime('%d-%b-%y')
currency_len = len(list(set(currency)))-1
print("Values imported and dates defined correctly.")

#start making changes in dateSchedule

for i in range(0, currency_len):
    for j in range(i*30, (i+1)*30):
        if (j < ((30*i)+10)):
            Trade_date[j+1] = T_0
        elif(j>(9+(30*i)) and j<(20+(30*i))):
            Trade_date[j+1] = T_1
        elif(j<(30+(30*i)) and j>(19+(30*i))):
            Trade_date[j+1] = T_2
        Issue_date[j+1] =  (datetime.datetime.strptime(Trade_date[j+1], '%d-%b-%y') + datetime.timedelta(days=6)).strftime('%d-%b-%y')
        Final_fixing_date[j+1] = (datetime.datetime.strptime(Issue_date[j+1], '%d-%b-%y') + relativedelta(months=int(Tenor[j+1]))).strftime('%d-%b-%y')
        Maturity_date[j+1] = (datetime.datetime.strptime(Final_fixing_date[j+1], '%d-%b-%y') + datetime.timedelta(days=3)).strftime('%d-%b-%y')
        First_call[j+1] = (datetime.datetime.strptime(Issue_date[j+1], '%d-%b-%y') + relativedelta(months=1)).strftime('%d-%b-%y')
        First_KO[j+1] = (datetime.datetime.strptime(First_call[j+1], '%d-%b-%y') + datetime.timedelta(days=3)).strftime('%d-%b-%y')
print("Successful in changing the data from sheets.")


# Create a Pandas dataframe from the data.
d_data={'0':currency,'1':Tenor,'2':Trade_date,'3':Issue_date,'4':Final_fixing_date,'5':Maturity_date,'6':First_call,'7':First_KO}
df = pd.DataFrame(d_data)
# Create a Pandas Excel writer using XlsxWriter as the engine.
if(os.path.isfile('D:/Cbackup/Users/mahan.das/AppData/Local/Programs/Python/Python36/DateScheduleSAMPLE.xlsx')):
    os.remove('D:/Cbackup/Users/mahan.das/AppData/Local/Programs/Python/Python36/DateScheduleSAMPLE.xlsx')
writer = pd.ExcelWriter('D:/Cbackup/Users/mahan.das/AppData/Local/Programs/Python/Python36/DateScheduleSAMPLE.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Sheet1')

# Close the Pandas Excel writer and output the Excel file.
writer.save()

print("Schedule date created successfully.")





