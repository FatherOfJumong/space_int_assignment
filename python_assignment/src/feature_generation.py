"""Feature generation functions for the contracts data."""

from datetime import timedelta, datetime
import pandas as pd


def generate_features(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate features from the contracts data."""
    df = convert_date_columns(df)
    # Group by id and application_date
    grouped = df.groupby(['id', 'application_date'])
    # Calculate features
    features = pd.DataFrame({
        'tot_claim_cnt_l180d': grouped.apply(calculate_tot_claim_cnt_l180d),
        'disb_bank_loan_wo_tbc': grouped.apply(calculate_disb_bank_loan_wo_tbc),
        'day_sinlastloan': grouped.apply(calculate_day_sinlastloan),
        'avg_loan_amnt': grouped.apply(calculate_avg_loan_amount),
        'loan_frequency': grouped.apply(calculate_loan_frequency)
    }).reset_index()
    return features


def convert_date_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert date columns to datetime and remove timezone info."""
    date_columns = ['application_date', 'claim_date', 'contract_date']
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce').dt.tz_localize(None)
    return df


""" >>>>>>>>>>>>>>>>>> Feature generation functions <<<<<<<<<<<<<<<<<<< (Required) """

def calculate_tot_claim_cnt_l180d(group: pd.DataFrame) -> int:
    """Calculate the number of claims in the last 180 days."""
    application_date = group['application_date'].iloc[0]
    # last_180_days = application_date - timedelta(days=180)
    last_180_days = datetime.now() - timedelta(days=180)
    
    claims_count = group[(group['claim_date'] >= last_180_days) & 
                         (group['claim_date'] <= application_date)].shape[0]
    return claims_count if claims_count > 0 else -3


def calculate_disb_bank_loan_wo_tbc(group: pd.DataFrame) -> float:
    """Calculate the sum of exposure of loans without TBC and other specified banks."""
    excluded_banks = ['TBC', 'LIZ', 'LOM', 'MKO', 'SUG']
    valid_loans = group[
        (group['bank'].notna()) & 
        (~group['bank'].isin(excluded_banks)) & 
        (group['loan_summa'].notna()) &
        (group['contract_date'].notna())
    ]
    if valid_loans.empty:
        return -1 if group['bank'].isna().all() else -3
    total_summa = valid_loans['loan_summa'].sum()
    return total_summa if total_summa > 0 else -3


def calculate_day_sinlastloan(group: pd.DataFrame) -> int:
    """Calculate the number of days since the last loan."""
    application_date = group['application_date'].iloc[0]
    valid_loans = group[group['summa'].notna()]  
    if valid_loans.empty:
        return -1 if group.empty else -3
    last_contract_date = valid_loans['contract_date'].max()
    if pd.isnull(last_contract_date):
        return -3
    days_since_last_loan = (application_date - last_contract_date).days
    return days_since_last_loan if days_since_last_loan > 0 else -3


""" >>>>>>>>>>>>>>>>>> Feature generation functions <<<<<<<<<<<<<<<<<<< (Not Required) """

def calculate_avg_loan_amount(group: pd.DataFrame) -> float:
    """Calculate the average loan amount for the client."""
    valid_loans = group[group['loan_summa'].notna()]
    if valid_loans.empty:
        return -1 
    return valid_loans['loan_summa'].mean()


def calculate_loan_frequency(group: pd.DataFrame) -> float:
    """Calculate the loan frequency (loans per year) for the client."""
    valid_loans = group[group['contract_date'].notna()]
    if valid_loans.empty:
        return -1  
    earliest_date = valid_loans['contract_date'].min()
    latest_date = valid_loans['contract_date'].max()
    years_diff = (latest_date - earliest_date).days / 365.25
    if years_diff <= 0:
        return -3
    return len(valid_loans) / years_diff if years_diff > 0 else len(valid_loans)
