"""
FROZEN -- Do not modify this file.
Run one experiment: load data, train agent's model, evaluate, log result.
"""
import sys
import time
import os
import ast
import pandas as pd
from sklearn.model_selection import train_test_split

# Add the agent_workspace to the path so we can import its code
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'agent_workspace'))
from train_cluster import build_predict_fn
from evaluator import evaluate_model

RESULTS_FILE = "logs/run_history.tsv"

def log_result(val_accuracy, status, description, runtime):
    os.makedirs("logs", exist_ok=True)
    file_exists = os.path.exists(RESULTS_FILE)
    with open(RESULTS_FILE, "a") as f:
        if not file_exists:
            f.write("val_accuracy\tstatus\tdescription\truntime\n")
        f.write(f"{val_accuracy:.4f}\t{status}\t{description}\t{runtime:.2f}s\n")

def main():
    # Parse terminal arguments
    args = sys.argv[1:]
    status = "keep"
    description = " ".join(args) if args else "experiment"
    
    if "--discard" in args:
        status = "discard"
        description = description.replace(" --discard", "")

    # 1. Load Data
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
    TRAIN_DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'processed', 'train_sample.csv')
    
    df = pd.read_csv(TRAIN_DATA_PATH)
    df['skills_list'] = df['skills_list'].apply(ast.literal_eval)
    train_df, val_df = train_test_split(df, test_size=0.20, random_state=42)

    print(f"Data: {len(train_df)} train, {len(val_df)} val")

    # 2. Train Agent's Model
    print("Training agent's clustering model...")
    t0 = time.time()
    predict_fn = build_predict_fn(train_df)
    train_time = time.time() - t0

    # 3. Evaluate
    print("Evaluating...")
    accuracy = evaluate_model(predict_fn, val_df)
    
    print(f"val_accuracy: {accuracy:.4f}")
    print(f"Training time: {train_time:.2f}s")

    # 4. Log
    log_result(accuracy, status, description, train_time)
    print(f"Result logged to {RESULTS_FILE} (status={status})")

if __name__ == "__main__":
    main()