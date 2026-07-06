
import argparse
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os
import json

def model_fn(model_dir):
    model = joblib.load(os.path.join(model_dir, "model.joblib"))
    return model

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-estimators", type=int, default=100)
    parser.add_argument("--max-depth", type=int, default=5)
    parser.add_argument("--n-neighbors", type=int, default=5)
    parser.add_argument("--model-dir", type=str, default=os.environ.get("SM_MODEL_DIR"))
    parser.add_argument("--train", type=str, default=os.environ.get("SM_CHANNEL_TRAIN"))
    parser.add_argument("--test", type=str, default=os.environ.get("SM_CHANNEL_TEST"))
    args = parser.parse_args()

    # Load data
    train_df = pd.read_csv(os.path.join(args.train, "train.csv"))
    test_df = pd.read_csv(os.path.join(args.test, "test.csv"))

    X_train = train_df.drop("target", axis=1)
    y_train = train_df["target"]
    X_test = test_df.drop("target", axis=1)
    y_test = test_df["target"]



    class_names = ['class_0', 'class_1', 'class_2']

    # Define both models
    models = {
        "RandomForest": RandomForestClassifier(
            n_estimators=args.n_estimators,
            max_depth=args.max_depth,
            random_state=42
        ),
        "KNN": KNeighborsClassifier(
            n_neighbors=args.n_neighbors
        )
    }

    results = {}
    best_model = None
    best_accuracy = 0
    best_name = None

    print("=" * 60)
    print("MODEL COMPARISON: RandomForest vs KNN")
    print("=" * 60)

    for name, model in models.items():
        # Train
        model.fit(X_train, y_train)

        # Predict
        predictions = model.predict(X_test)

        # Metrics
        accuracy = accuracy_score(y_test, predictions)
        cm = confusion_matrix(y_test, predictions)

        results[name] = {
            "accuracy": accuracy,
            "predictions": predictions.tolist()
        }

        print(f"\n{name}")
        print("-" * 40)
        print(f"Accuracy: {accuracy:.4f} ({accuracy*100:.1f}%)")
        print(f"\nClassification Report:")
        print(classification_report(y_test, predictions, target_names=class_names))
        print(f"Confusion Matrix:")
        print(cm)

        # Track best
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_model = model
            best_name = name

    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for name, result in results.items():
        print(f"{name}: {result['accuracy']*100:.1f}%")
    print(f"\nWINNER: {best_name} with {best_accuracy*100:.1f}% accuracy")
    print("=" * 60)

    # Save best model and results
    joblib.dump(best_model, os.path.join(args.model_dir, "model.joblib"))

    with open(os.path.join(args.model_dir, "results.json"), "w") as f:
        json.dump({
            "winner": best_name,
            "accuracy": best_accuracy,
            "all_results": {k: v["accuracy"] for k, v in results.items()}
        }, f)

    print(f"\nSaved best model: {best_name}")
