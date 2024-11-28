import pandas as pd
from sklearn.preprocessing import LabelEncoder
import pickle

def recreate_label_encoder():
    # Path to your training data CSV
    csv_path = "data/cleaned_medical_questions.csv"

    # Load the CSV
    df = pd.read_csv(csv_path)

    # Drop missing values
    df = df.dropna(subset=["cleaned_text", "speciality"])

    # Recreate the LabelEncoder and fit it to the specialties
    label_encoder = LabelEncoder()
    label_encoder.fit(df["speciality"])

    # Save the LabelEncoder to a pickle file
    with open("label_encoder.pkl", "wb") as f:
        pickle.dump(label_encoder, f)

    print("Successfully recreated 'label_encoder.pkl'")

if __name__ == "__main__":
    recreate_label_encoder()
