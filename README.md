# 🏥 **Medical QA Project**

This project involves developing, training, and deploying a small language model (SLM) capable of answering medical questions asked by end-users. The model provides informative, grounded answers while ensuring ethical compliance in its responses. The project includes both backend (FastAPI-based API) and frontend (React-based web app) components.

---

## 🌟 **Features**

- **Medical Question Answering**: The model answers medical questions related to symptoms, causes, home remedies, lifestyle changes, and recommendations for medical specialties.
- **Ethical Compliance**: The model adheres to ethical guidelines, never prescribing medications or treatments and always advising users to consult a healthcare professional.
- **Local Deployment**: The backend API is optimized to run on standard hardware without requiring GPUs for real-time inference.
- **Frontend Interface**: A simple, user-friendly chatbot interface hosted on Netlify for interacting with the backend API.

---

## 📋 **Project Overview**

This project aims to develop a language model that can answer medical questions, providing informative and grounded responses. The backend of the application uses **FastAPI** to handle HTTP requests, and the frontend is a **React**-based application hosted on **Netlify**. The model was trained using an open-source base model (e.g., GPT-2) and fine-tuned to answer medical questions while ensuring that no harmful or unethical medical advice is provided.

---

## 🛠️ **Tech Stack**

- **Backend:**
  - **FastAPI** for building the API.
  - **Hugging Face Transformers** for model implementation.
  - **PyTorch** for model training and inference.
  
- **Frontend:**
  - **ReactJS** for building the web interface.
  - **Netlify** for hosting the frontend.
  
- **Other Libraries:**
  - **torch**, **pickle**, **uvicorn** for backend API deployment.
  - **serve** for serving the frontend locally.

---

## 🏁 **Setup and Installation**

### 1. Clone the repository

Clone the repository to your local machine using:

```bash
git clone https://github.com/footcricket05/medicalQA.git
cd medicalQA
```

---

### 2. Install Backend Dependencies

Navigate to the backend folder and install the required dependencies:

```bash
cd src
pip install -r requirements.txt
```

---

### 3. Install Frontend Dependencies

Navigate to the frontend folder and install the required dependencies:

```bash
cd medical-qa-frontend
npm install
```

---

## 🧑‍💻 **Training the Model**

Before running the backend, you must first train or fine-tune the model. Here are the steps to do that:

1. **Activate the virtual environment** (if not already activated):

```bash
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

2. **Train the model** (this step might take a while depending on your machine's capacity):

```bash
python train_model.py
```

Once the model is trained and saved, you can proceed to run the backend.

---

## 🏃 **Running the Backend Locally**

To run the backend locally, follow these steps:

1. **Activate the virtual environment** (if not already activated):

```bash
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

2. **Start the FastAPI server**:

```bash
uvicorn src.app.combined_api:app --host=0.0.0.0 --port=8000 --reload
```

This will start the backend server on `http://127.0.0.1:8000`.

---

## 🌍 **Serve the Frontend Locally**

To test the frontend locally, navigate to the frontend folder and run:

```bash
serve -s build
```

The frontend will be accessible at `http://localhost:3000`.

---

## 🌐 **Frontend Hosting on Netlify**

1. Build the frontend:

```bash
npm run build
```

2. Install **Netlify CLI** if you don't have it already:

```bash
npm install -g netlify-cli
```

3. Login to Netlify:

```bash
netlify login
```

4. Link your project to Netlify:

```bash
netlify init
```

5. Deploy the site:

```bash
netlify deploy --prod
```

Follow the prompts to complete the deployment. Your frontend will be accessible at a public Netlify URL.

---

## 💻 **Model Development**

The model for answering medical questions was developed using an open-source base model from **Hugging Face Transformers**. A **classification model** is used to predict the medical specialty based on the question, and a **generation model (GPT-2)** is used to generate detailed, grounded answers.

---

## 🧹 **Data Preparation**

The medical question dataset used for training was sourced from public domain resources. Data preprocessing involved:

- **Cleaning** and formatting the text to remove unnecessary noise.
- **Handling imbalances** in question categories by ensuring an even distribution of medical specialties.
- **Splitting the data** into training, validation, and test sets.

---

## 🏋️ **Training and Fine-Tuning**

We used the **GPT-2 model** as a base for the question-answering task. The model was fine-tuned on the medical question dataset using **PyTorch**.

Training involved the following steps:

1. **Tokenizing the text** using the GPT-2 tokenizer.
2. **Fine-tuning the model** for a few epochs on a subset of the medical dataset.
3. Evaluating model performance on a separate validation set.

---

## ⚖️ **Ethical Compliance**

Ethical compliance is a critical part of this project. The model:

- Does not prescribe medications or specific treatments.
- Always advises users to **consult a healthcare professional**.
- Focuses on explaining symptoms, suggesting lifestyle changes, and recommending appropriate medical specialties.

---

## 📊 **Evaluation and Results**

The model’s performance was evaluated based on the following metrics:

- **Accuracy**: Correctness of the predicted specialty.
- **Relevance**: Appropriateness of the generated answer.
- **Ethical Compliance**: Ensuring the model doesn’t provide specific medical advice.

---

## 🛠️ **Challenges and Solutions**

### Challenge 1: Data Imbalance
**Solution**: We used data augmentation techniques and class balancing strategies during preprocessing to address this.

### Challenge 2: Ethical Compliance
**Solution**: We fine-tuned the model with constraints in the prompt to ensure responses were grounded in safety and avoided harmful medical advice.

---

## 📝 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### 📄 **Backend API Documentation**

---

# 🩺 **Medical QA Backend API Documentation**

## Introduction

The backend API is a **FastAPI** server that handles medical questions, classifies them into medical specialties, and generates relevant answers using **GPT-2**. The API is designed for local deployment on standard hardware without GPUs.

---

## 🌐 **Endpoints**

### 1. `/`
- **Method**: `GET`
- **Description**: A health check endpoint to verify the API is working.
- **Response:**
  ```json
  {
    "message": "Welcome to Medical QA API"
  }
  ```

### 2. `/answer`
- **Method**: `POST`
- **Description**: Takes a medical question and returns a recommended medical specialty and a detailed answer.
- **Request:**
  ```json
  {
    "question": "What should I do if I have a headache?"
  }
  ```
- **Response:**
  ```json
  {
    "specialty": "Neurology",
    "answer": "Based on your symptoms, you may be dealing with a tension headache. Some home remedies you can try include resting in a quiet, dark room and using a cold compress on your forehead. If the pain persists or worsens, consider consulting a neurologist."
  }
  ```
