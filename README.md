# ResumeTailor-AI: Agentic Resume Tailor & ATS Optimizer

I have build this application which will make a life easy while looking for other oppurtunities while I need to modify my resume based on my Job description and need to know my ats score and modify my resume accordingly .

---

## Key Features

- **Automated Skill & Keyword Extraction**: Extracts your candidate skills from existing resumes (DOCX, PDF, TXT) and compares them against target Job Descriptions to spot skill gaps.
- **Interactive Human-in-the-Loop (HITL) Review**: Pauses workflow for human approval. Add custom keywords, toggle suggested skills, and provide custom instructions before generating your resume.
- **Parametric DOCX Resume Generator**: Refactored `python-docx` generator tool that builds clean, 2-column layout resumes matching exact font sizes, line heights, and margins.
- **Real-Time ATS Match Scoring**: Computes an overall ATS Score (0-100%), Skills Match %, Keyword Density %, and Experience Relevance breakdown.
- **Multi-LLM Provider Support**: Supports Microsoft Azure OpenAI, Ollama (Local), LM Studio (Local), and OpenAI API.
- **NI Enterprise 3-Column UI Theme**: Built with React, Vite, and custom CSS following corporate enterprise design guidelines.

---

## System Requirements

- **Python**: `3.12+`
- **Package Manager**: `uv` (Recommended) or standard `pip`
- **Node.js**: `v18+` & `npm`

---

## Step-by-Step Installation & Setup Guide

### 1. Clone the Repository

```bash
git clone https://github.com/Arunxlr8/ResumeTailor-AI.git
cd ResumeTailor-AI
```

---

### 2. Environment Configuration (`.env`)

Copy `.env.example` inside the `backend/` directory to `.env`:

```bash
cd backend
cp .env.example .env
```

Open `backend/.env` in a text editor and configure your preferred LLM provider:

```env
# Choose provider: azure | ollama | lmstudio | openai
LLM_PROVIDER=azure

# If using Azure OpenAI:
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_KEY=your_actual_azure_api_key_here

# If using Ollama (Local):
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:14b

# If using LM Studio (Local):
LMSTUDIO_BASE_URL=http://localhost:1234/v1
LMSTUDIO_MODEL=qwen2.5-14b-instruct

# If using OpenAI API:
OPENAI_API_KEY=your_openai_api_key_here
```

---

### 3. Backend Setup (using `uv` or `pip`)

#### Option A: Using `uv` Package Manager (Recommended)

```bash
# Install uv if missing (Windows: winget install astral-sh.uv | Mac/Linux: curl -LsSf https://astral.sh/uv/install.sh)
uv venv .venv
.venv\Scripts\activate      # On Windows PowerShell
# source .venv/bin/activate # On Linux/macOS

uv pip install -r backend/requirements.txt
```

#### Option B: Using standard `pip`

```bash
python -m venv .venv
.venv\Scripts\activate      # On Windows PowerShell
pip install -r backend/requirements.txt
```

---

### 4. Frontend Setup

```bash
cd frontend
npm install
```

---

## Running the Application

### Step 1: Start the Backend API (FastAPI)

```bash
# From project root:
cd backend
..\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000
```
> The API will start at `http://127.0.0.1:8000`.

### Step 2: Start the Frontend UI (React + Vite)

In a second terminal:

```bash
cd frontend
npm run dev
```
> Open your browser to `http://localhost:5173`.

---

## Application Workflow & Usage

1. **Paste Job Description**: Paste the target job posting into the left input card.
2. **Upload Existing Resume**: Upload your candidate resume (`.docx`, `.pdf`, or `.txt`).
3. **Select LLM Provider**: Choose your preferred provider (`Azure OpenAI`, `Ollama`, `LM Studio`, or `OpenAI`).
4. **Click "Tailor & Analyze Resume"**: Triggers initial parsing and skill extraction.
5. **Human-in-the-Loop Review**:
   - Review candidate skills and suggested JD keywords.
   - Click chips to enable/disable keywords or add custom skills.
   - Click **"Approve & Generate Resume"**.
6. **Download & ATS Evaluation**:
   - View your calculated ATS Score (e.g. 94% Match) and category breakdowns.
   - Click **"Download Resume"** to get your tailored `.docx` file.

---

## Repository Structure

```
ResumeTailor-AI/
├── backend/
│   ├── api/             # FastAPI workflow router & endpoints
│   ├── core/            # LLM provider configs & app settings
│   ├── graph/           # LangGraph state graph, nodes (planner, generator)
│   ├── services/        # Resume parser & ATS evaluator modules
│   ├── templates/       # Parametric generate_resume.py docx builder tool
│   ├── main.py          # FastAPI application entry point
│   ├── requirements.txt # Python dependencies
│   └── .env.example     # Environment template (NO SECRETS)
├── frontend/
│   ├── public/          # Public static assets (profile picture)
│   ├── src/             # React components, pages, hooks, styling
│   ├── package.json     # Node dependencies
│   └── vite.config.js   # Vite configuration
├── understanding.txt    # Detailed technical architecture guide for interview prep
└── README.md            # Documentation & setup guide
```
