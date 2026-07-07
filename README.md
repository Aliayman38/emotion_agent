# Jordanian Arabic Emotion Classification AI Agent

A production-grade AI Agent project leveraging **LangGraph**, **LangChain**, and **FastAPI** to classify emotions in Jordanian Arabic sentences into four discrete classes: `happy`, `sad`, `angry`, or `neutral`.

---

## System Architecture

The pipeline processes input through a structured graph configuration, preventing unverified or broken data structures from escaping to the outer user interface boundaries:

```text
START 
  │
  ▼
[Normalize Text Node] ──► Removes Harakat, normalizes characters, strips repetition.
  │
  ▼
[Classify Emotion Node] ──► Passes context to Cloud LLM through Structured Output binding.
  │
  ▼
[Validate Output Node] ──► Asserts verification logic (boundaries / target enumeration).
  │
  ├──► [Is Valid? True]  ──► END (Returns verified state)
  │
  └──► [Is Valid? False] ──► (Has Retry capacity?) ──► Loop back to Classify
```

---

## Local Setup

```bash
git clone https://github.com/Aliayman38/emotion_agent.git
cd emotion_agent
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
```

---

## Configuration

> You must provide your own Google Gemini API key from [Google AI Studio](https://aistudio.google.com) before starting the server.

```powershell
$env:GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
$env:MODEL_NAME="gemini-2.5-flash"
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

---

## How to Use the Interactive UI (Swagger)

1. Open your browser and navigate to `http://127.0.0.1:8000/docs`.
2. Locate the green **`POST /predict`** endpoint box and click to expand it.
3. Click the **"Try it out"** button on the right side.
4. Modify the placeholder JSON in the **Request body** with your Jordanian Arabic sentence:

```json
{
  "text": "والله اليوم مبسوط كثير"
}
```