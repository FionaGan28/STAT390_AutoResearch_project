import pandas as pd
import os
from sklearn.model_selection import train_test_split
import ast

def process_create_split():
    """
    Processes raw data and creates the train-test split
    Frozen File
    """

    # error proofing paths
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
    RAW_DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'raw', 'full_data.csv')
    TRAIN_OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'data', 'processed', 'train_sample.csv')
    TEST_OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'data', 'locked_test', 'test_sample.csv')

    # security checks
    os.makedirs('../data/processed', exist_ok=True)
    os.makedirs('../data/locked_test', exist_ok=True)

    try:
        df = pd.read_csv(RAW_DATA_PATH)
    except FileNotFoundError:
        print(f"Error: Could not find dataset at {RAW_DATA_PATH}")
        return

    # drop NA rows, process string to list
    df.dropna(subset=['description_tokens'], inplace=True)
    df = df[df['description_tokens']!='[]']
    df['description_tokens_list'] = df['description_tokens'].apply(ast.literal_eval)
    df.rename(columns={'description_tokens_list': 'skills_list'}, inplace=True)

    # filter down to necessary columns only
    columns_to_keep = ['title', 'skills_list'] 
    df = df[columns_to_keep]

    # sampling 10000 rows, random_state = 28
    df = df.sample(n=10000, random_state=28)

    # 80-20 train-test split
    train_df, test_df = train_test_split(df, test_size=0.20, random_state=28)

    # save files
    train_df.to_csv(TRAIN_OUTPUT_PATH, index=False)
    test_df.to_csv(TEST_OUTPUT_PATH, index=False)

if __name__ == "__main__":
    process_create_split()