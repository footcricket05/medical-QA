# Medical QA Project

This project is a **Medical Question Answering System**, designed to provide users with **informative and ethical responses** to medical questions. It includes both a **backend** (FastAPI-based API) and a **frontend** (ReactJS-based web application) for a seamless user experience.

---

## Features

- **Medical Expertise Simulation**:
  - Classifies medical questions into relevant specialties.
  - Generates grounded answers based on symptoms, lifestyle, and suggested remedies.
- **Ethical Compliance**:
  - Does not prescribe medications or treatments.
  - Encourages consulting healthcare professionals for medical advice.
- **Easy Deployment**:
  - Backend API and frontend are containerized using **Docker**.
  - Fully orchestrated with **Docker Compose** for seamless deployment.
- **Frontend Hosting**:
  - The frontend is hosted on **Netlify**, enabling easy access to users.
- **Local Deployment**:
  - Backend runs efficiently on standard hardware, with no need for GPUs.

---

## Project Structure

```plaintext
medical-QA/
├── docker-compose.yml                 # Orchestrates backend and frontend services
├── Dockerfile.backend                 # Dockerfile for the backend
├── Dockerfile.frontend                # Dockerfile for the frontend
├── label_encoder.pkl                  # Pre-trained label encoder for specialties
├── LICENSE                            # Project license file
├── ngrok.exe                          # Utility for exposing local services
├── Problem Statement 2 - Medical SLM.pdf  # Problem statement document
├── SECURITY.md                        # Security policy for the project
├── README.md                          # Project documentation (this file)
├── src/                               # Backend source folder
│   ├── app/                           # FastAPI application
│   ├── requirements.txt               # Backend dependencies
│   └── model/                         # Trained models and utilities
├── medical-qa-frontend/               # Frontend React app
│   ├── src/                           # React app source files
│   ├── public/                        # Static files for the React app
│   └── package.json                   # Frontend dependencies
├── model/                             # Model training and fine-tuning scripts
│   └── model.safetensors              # Trained model file (download separately)
├── data/                              # Dataset for training and testing
└── README.md                          # This documentation file
```

---

## Prerequisites

Before running this project, ensure you have the following installed:

1. **Docker**: For containerizing and running the backend and frontend.
2. **Docker Compose**: To orchestrate multi-container applications.
3. **ngrok** (optional): For exposing local backend to the internet during testing.
4. **Node.js** (v16 or above): For frontend development.

---

## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/footcricket05/medical-QA.git
cd medical-QA
```

### 2. Download the Trained Model

The `model.safetensors` file is not included in this repository due to its size. Download the trained model file from [Google Drive](https://drive.google.com/drive/folders/1PgTasOUeE2AMugYG7zI1h7sygAOvfMRv?usp=sharing).

1. Download the file from the provided Google Drive link.
2. Save the `model.safetensors` file in the `model` folder:
   ```plaintext
   medical-QA/
   └── model/
       └── model.safetensors
   ```

---

### Dockerized Setup

#### 1. Build and Start the Project

Use Docker Compose to build and run both backend and frontend services:

```bash
docker-compose up --build
```

- The **backend** will be available at `http://localhost:8000`.
- The **frontend** will be available at `http://localhost:3000`.

---

#### 2. Expose Backend Locally (Optional)

To access the backend from a public device (like a mobile phone):

1. Start `ngrok`:
   ```bash
   ngrok http 8000
   ```
2. Use the public URL provided by `ngrok` to replace the backend URL in the frontend (`medical-qa-frontend/src/App.js`).

---

### Manual Setup

If you prefer running the project without Docker:

#### 1. Backend Setup

1. Navigate to the `src/` folder:
   ```bash
   cd src
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the FastAPI server:
   ```bash
   uvicorn app.combined_api:app --host 0.0.0.0 --port 8000 --reload
   ```

#### 2. Frontend Setup

1. Navigate to the frontend folder:
   ```bash
   cd medical-qa-frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the frontend locally:
   ```bash
   npm start
   ```

---

## Deployment

### Frontend Hosting on Netlify

1. Build the React app:
   ```bash
   npm run build
   ```
2. Deploy using the **Netlify CLI**:
   ```bash
   npm install -g netlify-cli
   netlify deploy --prod
   ```

---

## API Documentation

### Base URL

The backend is served at `http://localhost:8000`.

### Endpoints

#### 1. `/`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "message": "Welcome to Medical QA API"
  }
  ```

#### 2. `/answer`
- **Method**: `POST`
- **Request**:
  ```json
  {
    "question": "What should I do if I have a headache?"
  }
  ```
- **Response**:
  ```json
  {
    "specialty": "Neurology",
    "answer": "Based on your symptoms, you may be dealing with a tension headache. Some home remedies include resting and using a cold compress. Consider consulting a neurologist."
  }
  ```

---

## Ethical Compliance

- **Does Not Prescribe Medication**: The model avoids providing specific treatments or drugs.
- **Promotes Professional Advice**: Encourages users to consult healthcare professionals.
- **Safe Responses**: Responses are constrained to be ethical, grounded, and non-harmful.

---

## Security Policy

Refer to the [SECURITY.md](SECURITY.md) file for the security policy, which includes:
- Responsible disclosure guidelines for vulnerabilities.
- Contact information for reporting security concerns.

---

## License

This project is licensed under the [MIT License](LICENSE).

