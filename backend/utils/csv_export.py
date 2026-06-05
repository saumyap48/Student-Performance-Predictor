import csv
import io
from typing import List
import models

def generate_csv(predictions: List[models.PredictionHistory]) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow([
        "ID", "Study Hours", "Attendance", "Previous Score", 
        "Assignments Completed", "Predicted Score", "Created At"
    ])
    
    # Data
    for p in predictions:
        writer.writerow([
            p.id, p.study_hours, p.attendance, p.previous_score,
            p.assignments_completed, f"{p.predicted_score:.2f}",
            p.created_at.strftime("%Y-%m-%d %H:%M:%S")
        ])
    
    return output.getvalue()
