import numpy as np
import joblib
import json
import os
import pandas as pd
# from tensorflow.keras.models import load_model

# Load encoders and model once at import
organism_encoder_path = "ML/predictor/Organism_encodemap.json"
subsequence_encoder_path = "ML/predictor/subsequence_encodemap.json"
scaler_path = "ML/predictor/scaler.pkl"
label_encoder_path = "ML/predictor/label_encoder.pkl"
model_path = "ML/predictor/nn_model.pkl"

with open(organism_encoder_path, "r") as f:
    organism_encoder = json.load(f)
    
with open(subsequence_encoder_path, "r") as f:
    subsequence_encoder = json.load(f)

scaler = joblib.load(scaler_path)
label_encoder = joblib.load(label_encoder_path)
model = joblib.load(model_path)

def sliding_windows(sequence, min_len=3, max_len=7):
    windows = []
    n = len(sequence)
    for length in range(min_len, max_len + 1):
        for start in range(0, n - length + 1):
            end = start + length
            subseq = sequence[start:end]
            windows.append((start, end, subseq))
    return windows

def iou(start1, end1, start2, end2):
    # Intersection-over-Union for 1D intervals
    inter_start = max(start1, start2)
    inter_end = min(end1, end2)
    inter = max(0, inter_end - inter_start)
    union = (end1 - start1) + (end2 - start2) - inter
    if union == 0:
        return 0
    return inter / union

def filter_overlapping(predictions, iou_threshold=0.2):
    # Sort by confidence descending
    predictions = sorted(predictions, key=lambda x: -x["confidence"])
    
    selected = []
    
    while predictions:
        best = predictions.pop(0)
        selected.append(best)
        
        new_predictions = []
        for pred in predictions:
            overlap = iou(best["start"], best["end"], pred["start"], pred["end"])
            if overlap < iou_threshold:
                new_predictions.append(pred)
        
        predictions = new_predictions
    
    return selected

def on_predict(organism_name, full_sequence):
    full_sequence = full_sequence.strip()

    org_encoded = organism_encoder.get(organism_name, None)
    if org_encoded is None:
        raise ValueError(f"Organism '{organism_name}' not found in encoder.")


    windows = sliding_windows(full_sequence)
    X = []
    for start, end, subseq in windows:
        subseq_encoded = subsequence_encoder.get(subseq, None)
        if subseq_encoded is None:
            subseq_encoded = 0  # or maybe better: skip or raise warning for unseen subsequences?

        length_scaled = scaler.transform(pd.DataFrame({"length_sub_seq": [len(subseq)]}))[0][0]
        X.append([org_encoded, subseq_encoded, length_scaled])

    X = np.array(X)

    probs = model.predict(X, verbose=0)
    pred_labels = np.argmax(probs, axis=1)
    confidences = np.max(probs, axis=1)

    decoded_labels = label_encoder.inverse_transform(pred_labels)

    predictions = []
    for (start, end, _), label, confidence in zip(windows, decoded_labels, confidences):
        predictions.append({
            "start": start,
            "end": end,
            "label": label,
            "confidence": confidence
        })

    final_predictions = filter_overlapping(predictions)
    
    print(f"Prediction algo final predictions: {final_predictions}")

    return final_predictions
