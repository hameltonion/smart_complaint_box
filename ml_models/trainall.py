import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib
import os
import logging

# Centralized paths
from paths import DATASET_PATH, TRAINED_DATA_DIR, SUBCATEGORY_MODELS_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load dataset
try:
    df = pd.read_csv(DATASET_PATH)
    logging.info("✅ Dataset loaded successfully.")
except FileNotFoundError:
    logging.error(f"❌ Dataset not found at {DATASET_PATH}")
    exit()

# Ensure dirs
os.makedirs(TRAINED_DATA_DIR, exist_ok=True)
os.makedirs(SUBCATEGORY_MODELS_DIR, exist_ok=True)


def train_and_save_model(data, target, filename):
    pipeline = Pipeline([("tfidf", TfidfVectorizer()), ("clf", MultinomialNB())])
    pipeline.fit(data, target)
    joblib.dump(pipeline, TRAINED_DATA_DIR / filename)
    logging.info(f"✅ {filename} model trained and saved.")
    return pipeline


# Train category + urgency
category_model = train_and_save_model(df["complaint_text"], df["category"], "category_model.pkl")
urgency_model = train_and_save_model(df["complaint_text"], df["urgency"], "urgency_model.pkl")

# Train subcategory models
logging.info("🔄 Training subcategory models...")
for cat in df["category"].unique():
    sub_df = df[df["category"] == cat].copy()
    if sub_df["subcategory"].nunique() > 1:
        pipeline = Pipeline([("tfidf", TfidfVectorizer()), ("clf", MultinomialNB())])
        pipeline.fit(sub_df["complaint_text"], sub_df["subcategory"])
        joblib.dump(pipeline, SUBCATEGORY_MODELS_DIR / f"subcategory_{cat.lower()}.pkl")
        logging.info(f"✅ Subcategory model for '{cat}' saved.")
    else:
        logging.warning(f"⚠ Skipping subcategory model for '{cat}' (insufficient data).")

logging.info("🎉 Training complete.")