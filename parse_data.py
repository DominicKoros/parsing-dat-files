import pandas as pd
file_to_be_parsed = ''

def parse_dat_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    tables = {}
    current_table = None
    current_data = []

    for line in lines:
        if line.startswith('table'):
            if current_table is not None:
                tables[current_table] = pd.DataFrame(current_data)
            current_table = line.strip()
            current_data = []
        else:
            # Split the line and remove the last element (newline character)
            data = line.split(';')[:-1]
            current_data.append(data)

    if current_table is not None:
        tables[current_table] = pd.DataFrame(current_data)

    return tables