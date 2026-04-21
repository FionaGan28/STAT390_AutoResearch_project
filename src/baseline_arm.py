import os
import time
import ast
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
from sklearn.model_selection import train_test_split

# evaluator
from evaluator import evaluate_model

def load_and_split_train_data(filepath):
    """
    Loads the 80% processed data and splits it into train/val for the loop.
    """
    df = pd.read_csv(filepath)
    # parse the stringified lists back into lists
    df['skills_list'] = df['skills_list'].apply(ast.literal_eval)
    
    # create an internal 80/20 Train/Validation split from the available training data
    train_df, val_df = train_test_split(df, test_size=0.20, random_state=28)
    return train_df, val_df

def train_arm_model(train_df, min_support=0.05, min_confidence=0.1):
    """
    Trains the static ARM model.
    """
    print(f"Training ARM on {len(train_df)} rows...")
    
    # one-hot encode the skills for mlxtend
    te = TransactionEncoder()
    te_ary = te.fit(train_df['skills_list']).transform(train_df['skills_list'])
    onehot_df = pd.DataFrame(te_ary, columns=te.columns_)
    
    # find frequent itemsets and generate rules
    frequent_itemsets = apriori(onehot_df, min_support=min_support, use_colnames=True)
    
    if frequent_itemsets.empty:
        print("Warning: No frequent itemsets found.")
        return pd.DataFrame()
        
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
    return rules

def build_predict_fn(rules):
    """
    creates the prediction function for the evaluator.
    """
    def predict_masked_skill(visible_skills):
        if rules.empty:
            return []
            
        visible_set = frozenset(visible_skills)
        predictions = []
        
        # find rules where the antecedentsare a part of the visible skills and sort by confidence
        valid_rules = rules[rules['antecedents'].apply(lambda x: x.issubset(visible_set))]
        sorted_rules = valid_rules.sort_values(by='confidence', ascending=False)
        
        # extract the consequents as predictions
        for consequents in sorted_rules['consequents']:
            for skill in consequents:
                if skill not in predictions and skill not in visible_set:
                    predictions.append(skill)
                    
        return predictions
    return predict_masked_skill

def run_baseline():
    print("--- Starting Phase 1 Static Baseline ---")
    start_time = time.time()
    
    # setup csv paths relative to this script
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
    TRAIN_DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'processed', 'train_sample.csv')
    
    # load data
    train_df, val_df = load_and_split_train_data(TRAIN_DATA_PATH)
    
    # train model
    rules = train_arm_model(train_df, min_support=0.02, min_confidence=0.1)
    print(f"Generated {len(rules)} association rules.")
    
    # create prediction function
    predict_fn = build_predict_fn(rules)
    
    # evaluate
    print(f"Evaluating on {len(val_df)} validation postings...")
    accuracy = evaluate_model(predict_fn, val_df)
    
    end_time = time.time()
    runtime = end_time - start_time
    
    print("\n=== Baseline Results ===")
    print(f"Top-3 Accuracy: {accuracy:.4f}")
    print(f"Runtime Budget: {runtime:.2f} seconds")
    print("========================\n")

if __name__ == "__main__":
    run_baseline()