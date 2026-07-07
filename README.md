# Jordanian Arabic Emotion Classification AI Agent

A production-grade AI Agent project leveraging **LangGraph**, **LangChain**, and **FastAPI** to classify emotions in Jordanian Arabic sentences into four discrete classes: `happy`, `sad`, `angry`, or `neutral`.

---

## 🚀 System Architecture

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