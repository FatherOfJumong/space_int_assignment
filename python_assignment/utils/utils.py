""" Utility functions for data processing. """


import json
from typing import List, Dict, Any
import pandas as pd


def load_and_filter_data(file_path: str) -> pd.DataFrame:
    """Load and filter the data from a CSV file."""
    df = pd.read_csv(file_path)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    #df = df[df['id'].isin(["2925211", "2925220"])]
    return df


def parse_json(json_str: str) -> List[Dict[Any, Any]]:
    """Safely parse JSON string to a list of dictionaries."""
    try:
        return json.loads(json_str) if json_str else []
    except json.JSONDecodeError:
        return []


def process_contracts(df: pd.DataFrame) -> pd.DataFrame:
    """Process the data by exploding and normalizing contracts."""
    # Parsing json strings
    df['contracts'] = df['contracts'].fillna('')
    df['contracts'] = df['contracts'].apply(parse_json)

    # Exploding contracts
    df_exploded = df.explode('contracts').reset_index(drop=True)
    # Normalizing contracts
    df_normalized = pd.json_normalize(df_exploded['contracts']).reset_index(drop=True)
    # Combining the results
    result = pd.concat([df_exploded[['id', 'application_date']], df_normalized], axis=1)
    # Changing date column names
    date_columns = ['claim_date', 'contract_date']
    for col in date_columns:
        if col in result.columns:
            result[col] = pd.to_datetime(result[col], format='%d.%m.%Y')
    # Changing numeric column types
    numeric_columns = ['contract_id', 'summa', 'loan_summa', 'claim_id']
    for col in numeric_columns:
        if col in result.columns:
            result[col] = pd.to_numeric(result[col], errors='coerce')
    return result
