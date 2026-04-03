# Deployment Guide: Nexus - The Autonomous Venture OS

This guide will walk you through setting up **Nexus** on Google Cloud and running it locally for your hackathon demo.

## 1. Google Cloud Setup

> [!IMPORTANT]
> Ensure you have an active GCP Project with billing enabled (to use your $1000 credits).

### Enable Required APIs
Run these commands in your [Google Cloud Shell](https://shell.cloud.google.com/):
```bash
gcloud services enable aiplatform.googleapis.com \
                       discoveryengine.googleapis.com \
                       calendar-json.googleapis.com \
                       tasks.googleapis.com \
                       run.googleapis.com
```

### Vertex AI Search (Librarian)
1. Go to **Vertex AI Search and Conversation** in the GCP Console.
2. Create a new **Data Store** (Unstructured Data) and upload your demo PDFs/Notes.
3. Create a **Search App** and connect the data store.
4. Copy the **Data Store ID** for your backend config.

---

## 2. Local Backend Setup (Python)

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Set up environment variables in a `.env` file:
   ```env
   GOOGLE_CLOUD_PROJECT="your-project-id"
   GOOGLE_CLOUD_LOCATION="us-central1"
   DATA_STORE_ID="your-data-store-id"
   ```
4. Authenticate your local environment:
   ```bash
   gcloud auth application-default login
   ```
5. Run the server:
   ```bash
   python main.py
   ```

---

## 3. Local Frontend Setup (React)

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies (if not already done):
   ```bash
   npm install
   ```
3. Launch the development server:
   ```bash
   npm run dev
   ```
4. Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 4. Deployment to Cloud Run (Production)

To deploy the backend to Google Cloud Run:
```bash
gcloud run deploy nexus-backend \
    --source . \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars GOOGLE_CLOUD_PROJECT=your-project-id
```
Update the `fetch` URL in `frontend/src/App.tsx` to your new Cloud Run URL.
