import pandas as pd
import re

def clean_text(text):
    text = re.sub(r"[^a-zA-Z0-9\s.,?]", "", text)  # Remove special characters
    text = re.sub(r"\s+", " ", text)  # Normalize whitespace
    return text.strip()

def preprocess_data(input_file, output_file):
    df = pd.read_csv(input_file)
    df['cleaned_text'] = df['text'].apply(clean_text)
    df.to_csv(output_file, index=False)
    print("Preprocessing complete. Cleaned data saved to:", output_file)

if __name__ == "__main__":
    preprocess_data("data/medical_questions.csv", "data/cleaned_medical_questions.csv")
