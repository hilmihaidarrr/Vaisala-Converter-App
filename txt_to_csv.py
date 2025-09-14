import pandas as pd
import re
import os

def extract_value(text, key):
    pattern = rf"{key}=([\d.]+[A-Z]?)"
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None

def convert_units(value, original_unit, new_unit):
    if value is not None:
        value = value.strip()
        if value.endswith(original_unit):
            return value[:-len(original_unit)] + new_unit
    return value

def process_txt(file_path, output_file_path=None):
    data = pd.read_csv(file_path, delimiter="\t", header=None)
    data_split = data.iloc[:, 0].str.split(',', expand=True)
    column_names = [f'Column{i}' for i in range(1, data_split.shape[1] + 1)]
    data_split.columns = column_names
    
    # Rename columns based on the parameter names
    column_mapping = {
        'Column1': 'Date',
        'Column2': 'Time',
        'Column3': 'Code',
        'Column4': 'Dn',  # Wind direction minimum
        'Column5': 'Dm',  # Wind direction average
        'Column6': 'Dx',  # Wind direction maximum
        'Column7': 'Sn',  # Wind speed minimum
        'Column8': 'Sm',  # Wind speed average
        'Column9': 'Sx',  # Wind speed maximum
        'Column10': 'Ta',  # Air temperature
        'Column11': 'Tp',  # Internal temperature
        'Column12': 'Ua',  # Relative humidity
        'Column13': 'Pa',  # Air pressure
        'Column14': 'Rc',  # Rain accumulation
        'Column15': 'Rd',  # Rain duration
        'Column16': 'Ri',  # Rain intensity
        'Column17': 'Hc',  # Hail accumulation
        'Column18': 'Hd',  # Hail duration
        'Column19': 'Hi',  # Hail intensity
        'Column20': 'Rp',  # Rain peak intensity
        'Column21': 'Hp',  # Hail peak intensity
        'Column22': 'Th',  # Heating temperature
        'Column23': 'Vh',  # Heating voltage
        'Column24': 'Vs',  # Supply voltage
        'Column25': 'Id'   # Identifier
    }
    data_renamed = data_split.rename(columns=column_mapping)
    
    # List of keys to extract (excluding Date, Time, and Code)
    keys = ['Dn', 'Dm', 'Dx', 'Sn', 'Sm', 'Sx', 'Ta', 'Tp', 'Ua', 'Pa', 'Rc', 'Rd', 'Ri', 'Hc', 'Hd', 'Hi', 'Rp', 'Hp', 'Th', 'Vh', 'Vs', 'Id']
    
    # Extract the values from the mixed columns
    for key in keys:
        data_renamed[key] = data_renamed.apply(lambda row: extract_value(','.join(row.dropna().astype(str)), key), axis=1)
    
    # Convert units
    data_renamed['Sn'] = data_renamed['Sn'].apply(lambda x: convert_units(x, 'M', ''))
    data_renamed['Sm'] = data_renamed['Sm'].apply(lambda x: convert_units(x, 'M', ''))
    data_renamed['Sx'] = data_renamed['Sx'].apply(lambda x: convert_units(x, 'M', ''))
    data_renamed['Dn'] = data_renamed['Dn'].apply(lambda x: convert_units(x, 'D', ''))
    data_renamed['Dm'] = data_renamed['Dm'].apply(lambda x: convert_units(x, 'D', ''))
    data_renamed['Dx'] = data_renamed['Dx'].apply(lambda x: convert_units(x, 'D', ''))
    data_renamed['Pa'] = data_renamed['Pa'].apply(lambda x: convert_units(x, 'B', ''))
    data_renamed['Ua'] = data_renamed['Ua'].apply(lambda x: convert_units(x, 'P', ''))
    data_renamed['Rc'] = data_renamed['Rc'].apply(lambda x: convert_units(x, 'M', ''))
    data_renamed['Rd'] = data_renamed['Rd'].apply(lambda x: convert_units(x, 's', ''))
    data_renamed['Ri'] = data_renamed['Ri'].apply(lambda x: convert_units(x, 'M', ''))
    data_renamed['Rp'] = data_renamed['Rp'].apply(lambda x: convert_units(x, 'M', ''))
    data_renamed['Hp'] = data_renamed['Hp'].apply(lambda x: convert_units(x, 'M', ''))
    data_renamed['Hc'] = data_renamed['Hc'].apply(lambda x: convert_units(x, 'M', ''))
    data_renamed['Ta'] = data_renamed['Ta'].apply(lambda x: convert_units(x, 'C', ''))
    data_renamed['Tp'] = data_renamed['Tp'].apply(lambda x: convert_units(x, 'C', ''))
    data_renamed['Hi'] = data_renamed['Hi'].apply(lambda x: convert_units(x, 'M', ''))
    data_renamed['Th'] = data_renamed['Th'].apply(lambda x: convert_units(x, 'C', ''))
    data_renamed['Vh'] = data_renamed['Vh'].apply(lambda x: convert_units(x, 'N', ''))
    data_renamed['Vs'] = data_renamed['Vs'].apply(lambda x: convert_units(x, 'V', ''))



    # # Debugging: Print rows with 0R2, 0R3, and 0R5 codes to check extraction
    # print("Debugging 0R2 rows:")
    # print(data_renamed[data_renamed['Code'] == '0R2'])
    # print("Debugging 0R3 rows:")
    # print(data_renamed[data_renamed['Code'] == '0R3'])
    # print("Debugging 0R5 rows:")
    # print(data_renamed[data_renamed['Code'] == '0R5'])
    
    # Drop rows with more than 50% null values
    threshold = len(data_renamed.columns) / 2
    data_renamed = data_renamed.dropna(thresh=threshold)
    
    # Fill the 'Id' column with 'DATA'
    data_renamed['Id'] = 'DATA'
    
    # Drop the original mixed columns
    columns_to_drop = [col for col in data_renamed.columns if col.startswith('Column')]
    data_renamed.drop(columns=columns_to_drop, inplace=True)
    
    # Reorder columns to match the keys list, with Date, Time, and Code first
    reordered_columns = ['Date', 'Time', 'Code'] + keys
    data_final = data_renamed[reordered_columns]
    
    # Rename columns at the end of the process
    final_column_mapping = {
        'Dn': 'min_winddirection',
        'Dm': 'avg_winddirection',
        'Dx': 'max_winddirection',
        'Sn': 'min_windspeed',
        'Sm': 'avg_windspeed',
        'Sx': 'max_windspeed',
        'Ta': 'air_temp',
        'Tp': 'internal_temp',
        'Ua': 'relative_humid',
        'Pa': 'air_pressure',
        'Rc': 'rain_accumulation',
        'Rd': 'rain_duration',
        'Ri': 'rain_intensity',
        'Hc': 'hail_accumulation',
        'Hd': 'hail_duration',
        'Hi': 'hail_intensity',
        'Rp': 'rain_peak_intensity',
        'Hp': 'hail_peak_intensity',
        'Th': 'heating_temp',
        'Vh': 'heating_voltage',
        'Vs': 'supply_voltage'
        # Add other renaming mappings if necessary
    }
    data_final.rename(columns=final_column_mapping, inplace=True)
    
    # Save the updated dataframe to a new CSV file
    if output_file_path is None:
        output_file_path = os.path.splitext(file_path)[0] + '_Formatted.csv'
    data_final.to_csv(output_file_path, index=False)
    
    return output_file_path

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Process a TXT file to extract weather data parameters and convert to CSV.")
    parser.add_argument("file", help="The path to the TXT file to be processed")
    args = parser.parse_args()
    
    processed_file = process_txt(args.file)
    print(f"Processed file saved as: {processed_file}")