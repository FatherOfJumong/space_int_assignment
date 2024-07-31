""" Main script to run the project. """


from utils import load_and_filter_data, process_contracts
from src.feature_generation import generate_features

io_path = "./python_assignment/data"

def main():
    """Main function to run the project."""
    # loding and filtering data
    df = load_and_filter_data(f"{io_path}/data.csv")
    # processing contracts
    df_processed = process_contracts(df)
    # generating features
    df_features = generate_features(df_processed)
    # saving features
    df_features.to_csv(f"{io_path}/contract_features.csv", index=False)
    print(f"Features generated and saved to '{io_path}/contract_features.csv'")
    
if __name__ == "__main__":
    main()
