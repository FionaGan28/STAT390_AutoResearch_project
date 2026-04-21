import random
import pandas as pd

def evaluate_model(predict_fn, validation_df, k=3, seed=28):
    """
    Evaluates a model's Top-K masked skill prediction accuracy.
    Frozen File
    
    Inputs:
        predict_fn: A function provided by the model. Takes a list of visible skills and returns a list of top predicted skills.
        validation_df: A pandas df containing a 'skills_list' column.
        k: The number of top predictions to consider (Top-K).
        seed: Random seed to ensure the exact same skills are masked every time.
        
    Returns:
        float: Top-K Accuracy score on the test set (0.0 to 1.0)
    """

    random.seed(seed)
    correct_predictions = 0
    total_valid_rows = 0

    for skills in validation_df['skills_list']:
        # skip rows with < 2 skills (need at least one known and one masked )
        if not isinstance(skills, list) or len(skills) < 2:
            continue

        total_valid_rows += 1
        
        # choose one skill to mask (deterministic)
        masked_index = random.randint(0, len(skills) - 1)
        target_skill = skills[masked_index]
        
        # create the visible skills list
        visible_skills = skills[:masked_index] + skills[masked_index+1:]
        
        # ask model for predictions
        top_predictions = predict_fn(visible_skills)
        
        # evaluate the prediction
        if target_skill in top_predictions[:k]:
            correct_predictions += 1
            
    # calculate final accuracy score
    if total_valid_rows == 0:
        return 0.0
        
    accuracy = correct_predictions / total_valid_rows
    return accuracy

if __name__ == "__main__":
    print("Evaluator module loaded successfully.")