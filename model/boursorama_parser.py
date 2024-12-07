import csv
import os
from datetime import datetime

def get_list_of_csv_files(data_folder):
    return [os.path.join(os.getcwd(), data_folder, file) for file in os.listdir(data_folder + '/') if file.endswith(".csv")]

def csv_file_to_list_of_dicts(csv_filepath):
    with open(csv_filepath, 'r') as csv_f:
        reader = csv.DictReader(csv_f, delimiter=';')

        return [row for row in reader]

def european_number_string_to_float(european_number: str):
    return float(european_number.replace(" ", "").replace('.', '').replace(',', '.'))

def normalize_dict_from_boursorama(boursorama_format_dict) -> dict:
    standard_format_dict = {
                            'date': datetime.fromisoformat(boursorama_format_dict['dateVal']),
                            'amount': european_number_string_to_float(boursorama_format_dict['amount']),
                            'description': boursorama_format_dict['label'],
                            'account_label': 'boursorama',
                            }
    return standard_format_dict

def normalize_dicts_from_boursorama(bourso_csv_filepaths: list) -> list[dict]: 
    normalized_dicts = []
    for csv_filepath in bourso_csv_filepaths:
        for dict_with_boursorama_data in csv_file_to_list_of_dicts(csv_filepath):
            # skip on-hold operations
            if "Autorisation paiement / retrait en cours" == dict_with_boursorama_data["category"]:
                continue

            normalized_dicts.append(normalize_dict_from_boursorama(dict_with_boursorama_data))

    return normalized_dicts


