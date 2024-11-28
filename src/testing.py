import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import pickle

# Load model, tokenizer, and label encoder
model_name = "./model"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

with open("label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

# Test input
question = "What are the treatments for diabetes?"
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# Tokenize and infer
inputs = tokenizer(question, return_tensors="pt", padding=True, truncation=True).to(device)
outputs = model(**inputs)
prediction = outputs.logits.argmax(dim=-1).item()

# Map prediction to specialty
specialty = label_encoder.inverse_transform([prediction])[0]
print(f"Question: {question}")
print(f"Predicted Specialty: {specialty}")
