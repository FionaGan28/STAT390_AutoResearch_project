"""
EDITABLE -- The agent modifies this file.
Define the clustering model and prediction logic.
The function build_predict_fn(train_df) must return a function that takes a 
list of visible skills and returns a list of top predicted skills.
"""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from collections import Counter

def build_predict_fn(train_df):
    """
    Trains a clustering model and returns a prediction function.
    """
    train_df = train_df.copy()
    train_df['skills_str'] = train_df['skills_list'].apply(lambda x: ' '.join(x))
    
    # 1. More features to capture specific skills
    vectorizer = TfidfVectorizer(max_features=1000)
    X = vectorizer.fit_transform(train_df['skills_str'])
    
    # 2. More clusters for finer-grained skill taxonomies
    n_clusters = 100
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto')
    train_df['cluster'] = kmeans.fit_predict(X)
    
    # 3. Precompute top skills per cluster
    cluster_top_skills = {}
    for i in range(n_clusters):
        cluster_data = train_df[train_df['cluster'] == i]
        all_skills = [skill for skills in cluster_data['skills_list'] for skill in skills]
        top_skills = [skill for skill, count in Counter(all_skills).most_common(20)]
        cluster_top_skills[i] = top_skills

    # Global top skills as fallback
    global_all_skills = [skill for skills in train_df['skills_list'] for skill in skills]
    global_top_skills = [skill for skill, count in Counter(global_all_skills).most_common(20)]

    def predict_masked_skill(visible_skills):
        if not visible_skills:
            return global_top_skills[:3]
            
        visible_str = ' '.join(visible_skills)
        v_vec = vectorizer.transform([visible_str])
        cluster = kmeans.predict(v_vec)[0]
        
        candidates = cluster_top_skills.get(cluster, global_top_skills)
        
        preds = []
        for s in candidates:
            if s not in visible_skills:
                preds.append(s)
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
