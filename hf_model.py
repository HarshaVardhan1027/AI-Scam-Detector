import os
import warnings

warnings.filterwarnings("ignore")

os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"

from transformers import pipeline, logging
logging.set_verbosity_error()

classifier = None

def load_model():
    global classifier
    if classifier is None:
        classifier = pipeline(
            "text-classification",
            model="mrm8488/bert-tiny-finetuned-sms-spam-detection"
        )

def hf_score(text):
    load_model()  # loads only when needed

    result = classifier(text[:200])[0]

    score = result['score'] * 100
    label = result['label'].lower()

    if label == 'spam':
        return score, "AI model detects spam/scam patterns"
    else:
        if score < 60:
            return score, "AI model uncertain about message safety"
        else:
            return score, "AI model leans toward safe message"
