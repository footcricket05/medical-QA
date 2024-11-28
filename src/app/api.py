from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from pydantic import BaseModel
import torch
import pickle

app = FastAPI()

# Load the trained classification model and tokenizer
classification_model_name = "./model"  # Path to your saved model
classification_tokenizer = AutoTokenizer.from_pretrained(classification_model_name)
classification_model = AutoModelForSequenceClassification.from_pretrained(classification_model_name)

# Load the label encoder used during training
with open("label_encoder.pkl", "rb") as f:  # Ensure this matches the path where you saved it
    label_encoder = pickle.load(f)

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def read_root():
    return {"message": "Welcome to Medical QA API"}

@app.post("/answer")
def get_answer(request: QuestionRequest):
    # Step 1: Tokenize the input question
    inputs = classification_tokenizer(request.question, return_tensors="pt", padding=True, truncation=True).to("cuda" if torch.cuda.is_available() else "cpu")
    classification_model.to("cuda" if torch.cuda.is_available() else "cpu")
    
    # Step 2: Perform classification
    outputs = classification_model(**inputs)
    prediction = outputs.logits.argmax(dim=-1).item()  # Get the predicted class (specialty)

    # Step 3: Map the prediction to the specialty
    predicted_specialty = label_encoder.inverse_transform([prediction])[0]

    return {"specialty": predicted_specialty}
