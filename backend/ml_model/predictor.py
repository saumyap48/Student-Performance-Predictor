import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import pickle
import os

# Features: study_hours, attendance, previous_score, assignments_completed
# Target: predicted_score (0-100)

def train_model():
    # Synthetic dataset for demonstration
    np.random.seed(42)
    n_samples = 1000
    
    study_hours = np.random.uniform(1, 10, n_samples)
    attendance = np.random.uniform(60, 100, n_samples)
    previous_score = np.random.uniform(30, 100, n_samples)
    assignments_completed = np.random.randint(0, 10, n_samples)
    
    # Simple linear combination with some noise
    # predicted_score = 3*study_hours + 0.2*attendance + 0.4*previous_score + 2*assignments_completed + noise
    noise = np.random.normal(0, 2, n_samples)
    predicted_score = (3 * study_hours + 0.2 * attendance + 0.4 * previous_score + 2 * assignments_completed + noise)
    
    # Clip scores to be between 0 and 100
    predicted_score = np.clip(predicted_score, 0, 100)
    
    df = pd.DataFrame({
        'study_hours': study_hours,
        'attendance': attendance,
        'previous_score': previous_score,
        'assignments_completed': assignments_completed,
        'predicted_score': predicted_score
    })
    
    X = df[['study_hours', 'attendance', 'previous_score', 'assignments_completed']]
    y = df['predicted_score']
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Save the model
    model_path = os.path.join(os.path.dirname(__file__), '../../student_model.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"Model trained and saved to {model_path}")
    return model

def load_model():
    model_path = os.path.join(os.path.dirname(__file__), '../../student_model.pkl')
    if not os.path.exists(model_path):
        return train_model()
    
    with open(model_path, 'rb') as f:
        return pickle.load(f)

def predict(study_hours, attendance, previous_score, assignments_completed):
    model = load_model()
    features = np.array([[study_hours, attendance, previous_score, assignments_completed]])
    prediction = model.predict(features)
    return float(prediction[0])

if __name__ == "__main__":
    train_model()
