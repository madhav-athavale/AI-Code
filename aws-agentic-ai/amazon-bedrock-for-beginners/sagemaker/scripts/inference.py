
import joblib
import numpy as np
import os
import json

def model_fn(model_dir):
    model = joblib.load(os.path.join(model_dir, "model.joblib"))
    return model

def input_fn(request_body, request_content_type):
    """Handle both json and numpy formats"""
    if request_content_type == "application/json":
        data = json.loads(request_body)
        # handle both {"instances": [...]} and direct array
        if isinstance(data, dict):
            return np.array(data["instances"])
        return np.array(data)

    elif request_content_type == "application/x-npy":
        import io
        return np.load(io.BytesIO(request_body), allow_pickle=True)

    elif request_content_type == "text/csv":
        import io
        return np.loadtxt(io.StringIO(request_body), delimiter=",")

    raise ValueError(f"Unsupported content type: {request_content_type}")

def predict_fn(input_data, model):
    predictions = model.predict(input_data)
    probabilities = model.predict_proba(input_data)
    return {
        "predictions": predictions.tolist(),
        "probabilities": probabilities.tolist()
    }

def output_fn(prediction, content_type):
    return json.dumps(prediction)
