from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoModelForSequenceClassification, AutoTokenizer, GPT2LMHeadModel, GPT2Tokenizer
from pydantic import BaseModel
import torch
import pickle

app = FastAPI()

# Load the classification model and tokenizer
classification_model_name = "./model"
classification_tokenizer = AutoTokenizer.from_pretrained(classification_model_name)
classification_model = AutoModelForSequenceClassification.from_pretrained(classification_model_name)

# Load the label encoder used during training
with open("label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

# Load GPT-2 for generating detailed answers
generation_model = GPT2LMHeadModel.from_pretrained("gpt2")
generation_tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Ensure pad_token_id is set
generation_tokenizer.pad_token = generation_tokenizer.eos_token

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
    # Set device to GPU if available, else CPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Move both models to the device (GPU/CPU)
    classification_model.to(device)
    generation_model.to(device)

    # Step 1: Tokenize the input question for classification
    inputs = classification_tokenizer(request.question, return_tensors="pt", padding=True, truncation=True).to(device)

    # Step 2: Perform classification to get the specialty
    with torch.no_grad():
        outputs = classification_model(**inputs)
        prediction = outputs.logits.argmax(dim=-1).item()
        predicted_specialty = label_encoder.inverse_transform([prediction])[0]

    # Step 3: Generate a detailed response using GPT-2 based on the predicted specialty
    # The prompt now guides the model to focus on giving structured and relevant advice
    prompt = f"As a professional {predicted_specialty}, please provide the treatment and advice for the following symptoms: {request.question}. Please respond clearly and concisely, with no irrelevant information or storytelling."

    generation_inputs = generation_tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, add_special_tokens=True).to(device)

    # Generate the answer with adjusted generation parameters
    with torch.no_grad():
        generation_outputs = generation_model.generate(
            generation_inputs["input_ids"].to(device),
            attention_mask=generation_inputs["attention_mask"].to(device),
            max_length=200,  # Reasonable length limit
            num_return_sequences=1,
            pad_token_id=generation_tokenizer.pad_token_id,
            temperature=0.5,  # Lower temperature for more deterministic responses
            top_p=0.8,        # Nucleus sampling to ensure diversity without going off-topic
            top_k=40,         # Limit the sampling pool to the top 40 tokens
            no_repeat_ngram_size=2,  # Prevent repetition of n-grams
            length_penalty=1.0,  # Penalize long responses to avoid excessive length
            eos_token_id=generation_tokenizer.eos_token_id  # Make sure the response stops at the end token
        )

    # Decode the generated text
    detailed_answer = generation_tokenizer.decode(generation_outputs[0], skip_special_tokens=True)

    return {"specialty": predicted_specialty, "answer": detailed_answer}
