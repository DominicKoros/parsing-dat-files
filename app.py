from parse_data import parse_dat_file
from datetime import datetime
import xlsxwriter
import pandas as pd
import sys

filename = ""
file_to_be_parsed = ""

def get_seconds(t):
   h, m, s = map(int, t.split(':'))
   return h * 3600 + m * 60 + s

def get_nested_values(table3, table4, table5, table6, liberation_time):
    merged56 = table5.merge(table6, left_on=1, right_on=2, suffixes=('_left', '_right'))
    merged4 = merged56.merge(table4, left_on='0_left', right_on=1, suffixes=('_left_last', '_right_last'))
    murged_full = merged4.merge(table3, left_on='0_left', right_on=4, suffixes=('_left_full', '_right_full'))
    # column #2 is the distance

    short_id_list = []
    YPM_list = []
    distance_list = []
    sex_list = []
    color_list = []
    loft_list = []
    arrival_list = []

    #YPM = ((miles * 1760) / seconds) * 60
    for index, row in murged_full.iterrows():
        short_id = row['1_left']
        distance = row['2_left_full']
        arrival_time = row['5_left_full']
        sex = row['2_left']
        color = row['3_left']
        loft = row['0_right_full']
        calced_time = get_seconds(arrival_time)

        YPM = ((float(distance) * 1760) / int(calced_time - liberation_time)) * 60
        # key_matched.append({short_id: YPM, 'distance': distance})
        short_id = short_id.lstrip('0')
        short_id_list.append(short_id)
        YPM_list.append(YPM)
        distance_list.append(distance)
        sex_list.append(sex)
        color_list.append(color)
        loft_list.append(loft)
        arrival_list.append(arrival_time)
    
    df = pd.DataFrame({'short_id': short_id_list, 'YPM': YPM_list, 'distance': distance_list, 'sex': sex_list, 'color': color_list, 'loft name': loft_list})
    return df

def sort_by_YPM(data):
    return data.sort_values(by='Speed', ascending=False)

def write_to_excel(tables):
    pre_writen_data = pd.DataFrame()

    nested_vals = get_nested_values(tables["table3"], tables["table4"], tables["table5"], tables["table6"], get_seconds(tables["table2"][3].iloc[0] + ':00'))

    num_of_lofts = tables["table2"][5].iloc[0]
    num_of_birds = tables["table2"][6].iloc[0]

    pre_writen_data['Place'] = range(1, len(tables["table5"]) + 1)
    pre_writen_data['Race name'] = tables["table6"][0].str.replace("SUB", "")
    pre_writen_data['Race station'] = tables["table4"][0].str.replace("SUB", "")
    pre_writen_data['Race date'] = tables["table6"][1]
    pre_writen_data['Liberation time'] = ""
    pre_writen_data['Weather at start'] = "UNKNOWN"
    pre_writen_data['Loft name'] = nested_vals["loft name"]
    pre_writen_data['Air Line'] = nested_vals['distance'].astype(float)
    pre_writen_data['Pigeon number'] = nested_vals['short_id']
    pre_writen_data['sex'] = nested_vals['sex']
    pre_writen_data['color'] = nested_vals['color']
    pre_writen_data['Arrival time'] = tables['table6'][5]
    pre_writen_data['Speed'] = nested_vals['YPM']
    pre_writen_data['Weather at home'] = "UNKNOWN"
    pre_writen_data['Number of Lofts'] = int(num_of_lofts)
    pre_writen_data['Number of birds'] = int(num_of_birds)

    pre_writen_data.set_index('Place', inplace=True)
    pre_writen_data['Liberation time'] = pre_writen_data['Liberation time'].apply(lambda x: str(x) + (tables["table2"][3] + " AM"))

    ready_data = sort_by_YPM(pre_writen_data)
    writer = pd.ExcelWriter(filename.replace(".dat", ".xlsx"), engine="xlsxwriter")

    ready_data.to_excel(writer, sheet_name="Sheet1", startrow=1, header=False, index=False)

    workbook = writer.book
    worksheet = writer.sheets["Sheet1"]

    # Get the dimensions of the dataframe.
    (max_row, max_col) = ready_data.shape

    # Create a list of column headers, to use in add_table().
    column_settings = [{"header": column} for column in ready_data.columns]

    # Add the Excel table structure. Pandas will add the data.
    worksheet.add_table(0, 0, max_row, max_col - 1, {"columns": column_settings, 'style': 'Table Style Medium 2'},)

    # Make the columns wider for clarity.
    worksheet.set_column(0, max_col - 1, 12)

    writer.close()


# main
if(len(sys.argv) < 2):
    print("Please provide a .dat file to be parsed")
    sys.exit(1)

filename = sys.argv[1]
file_to_be_parsed = filename

write_to_excel(parse_dat_file(file_to_be_parsed))
print("File has been written to " + filename.replace(".dat", ".xlsx") + " successfully, bye bye :)")