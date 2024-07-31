""" Main script to run the project. """

import os
from utils import load_and_filter_data, process_contracts
from src.feature_generation import generate_features

def main():
    """Main function to run the project."""
    # Define paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "data")
    input_file = os.path.join(data_dir, "data.csv")
    output_file = os.path.join(data_dir, "contract_features.csv")

    # loading and filtering data
    df = load_and_filter_data(input_file)
    # processing contracts
    df_processed = process_contracts(df)
    # generating features
    df_features = generate_features(df_processed)
    # saving features
    df_features.to_csv(output_file, index=False)
    print(f"Features generated and saved to '{output_file}'")
    
if __name__ == "__main__":
    main()