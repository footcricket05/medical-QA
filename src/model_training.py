from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset, Dataset
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import pickle
import warnings
import torch

# Check device availability
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Suppress warnings
warnings.filterwarnings("ignore")


def load_data(file_path):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)
    df = df.dropna(subset=["cleaned_text", "speciality"])  # Drop rows with missing values

    # Encode labels
    label_encoder = LabelEncoder()
    df['speciality'] = label_encoder.fit_transform(df['speciality'])

    # Save label encoder for future use
    with open("label_encoder.pkl", "wb") as f:
        pickle.dump(label_encoder, f)

    # Convert the DataFrame to HuggingFace Dataset
    dataset = Dataset.from_pandas(df[['cleaned_text', 'speciality']])
    return dataset.train_test_split(test_size=0.2), label_encoder


def tokenize(batch, tokenizer):
    texts = batch["cleaned_text"]
    return tokenizer(texts, padding=True, truncation=True)


def train_model():
    dataset, label_encoder = load_data("data/cleaned_medical_questions.csv")

    # Load pretrained model and tokenizer
    model_name = "dmis-lab/biobert-base-cased-v1.1"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        num_labels=len(label_encoder.classes_)  # Number of specialties
    ).to(device)

    # Tokenize the dataset
    dataset = dataset.map(lambda batch: tokenize(batch, tokenizer), batched=True)
    dataset = dataset.rename_column("speciality", "labels")

    # Training arguments
    training_args = TrainingArguments(
        output_dir="./model",
        evaluation_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=5,  # Adjust as needed
        weight_decay=0.01,
        save_total_limit=2,
        load_best_model_at_end=True
    )

    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset['train'],
        eval_dataset=dataset['test'],
        tokenizer=tokenizer,
    )

    # Train the model
    trainer.train()
    trainer.save_model("./model")
    tokenizer.save_pretrained("./model")
    print("Training complete, model saved to './model'")


if __name__ == "__main__":
    train_model()
