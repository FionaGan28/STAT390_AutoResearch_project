import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from collections import Counter

def build_predict_fn(train_df):
    """
    Trains a global ExtraTreesClassifier on a baseline TF-IDF feature matrix 
    to predict missing Data Analyst skills.
    
    Args:
        train_df (pd.DataFrame): The training data containing 'skills_list'.
        
    Returns:
        Callable: A function that takes a list of visible skills and 
                  returns the top 3 predicted masked skills.
    """
    train_df = train_df.copy()
    train_df['skills_str'] = train_df['skills_list'].apply(lambda x: ' '.join(x))
    
    # 1. Feature engineering (Baseline)
    vectorizer = TfidfVectorizer(max_features=2000, token_pattern=r"\S+")
    X = vectorizer.fit_transform(train_df['skills_str'])
    
    # 2. Target engineering
    mlb = MultiLabelBinarizer()
    y = mlb.fit_transform(train_df['skills_list'])
    
    # 3. Model: Extra Trees
    skill_counts = Counter([s for skills in train_df['skills_list'] for s in skills])
    top_skills = [s for s, _ in skill_counts.most_common(200)]
    
    top_indices = [i for i, class_name in enumerate(mlb.classes_) if class_name in top_skills]
    y_top = y[:, top_indices]
    top_classes = mlb.classes_[top_indices]
    
    model = ExtraTreesClassifier(n_estimators=100, max_depth=30, n_jobs=-1, random_state=42)
    model.fit(X, y_top)
    
    global_top_skills = [s for s, _ in skill_counts.most_common(20)]

    def predict_masked_skill(visible_skills):
        if not visible_skills:
            return global_top_skills[:3]
            
        visible_str = ' '.join(visible_skills)
        v_vec = vectorizer.transform([visible_str])
        
        probs_list = model.predict_proba(v_vec)
        # ExtraTrees with MultiOutput yields list of arrays
        probs = np.array([p[0][1] if p[0].shape[0] > 1 else 0 for p in probs_list])
        
        top_prob_indices = np.argsort(probs)[::-1]
        
        preds = []
        for idx in top_prob_indices:
            skill = top_classes[idx]
            if skill not in visible_skills:
                preds.append(skill)
            if len(preds) == 3:
                break
        
        if len(preds) < 3:
            for s in global_top_skills:
                if s not in visible_skills and s not in preds:
                    preds.append(s)
                if len(preds) == 3:
                    break
                    
        return preds
        
    return predict_masked_skill
