""" Main script to run the project. """

import os
from utils import load_and_filter_data, process_contracts
from src.feature_generation import generate_features

script_dir = os.path.dirname(os.path.abspath(__file__))
io_path = os.path.join(script_dir, "data")

def main():
    """Main function to run the project."""
    # loading and filtering data
    df = load_and_filter_data(os.path.join(io_path, "data.csv"))
    # processing contracts
    df_processed = process_contracts(df)
    # generating features
    df_features = generate_features(df_processed)
    # saving features
    output_path = os.path.join(io_path, "contract_features.csv")
    df_features.to_csv(output_path, index=False)
    print(f"Features generated and saved to '{output_path}'")
    
if __name__ == "__main__":
    main()