import json
import os
import requests
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PRIVARO_API_KEY = os.getenv("PRIVARO_API_KEY")
PRIVARO_PIPELINE_ID = os.getenv("PRIVARO_PIPELINE_ID")
PRIVARO_BASE_URL = os.getenv("PRIVARO_BASE_URL", "https://privaro-proxy-production.up.railway.app").rstrip("/")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

HEADERS = {"Content-Type": "application/json", "X-Privaro-Key": PRIVARO_API_KEY}

def privaro_post(path: str, payload: dict) -> dict:
    resp = requests.post(f"{PRIVARO_BASE_URL}{path}", headers=HEADERS, json=payload, timeout=60)
    data = resp.json()
    resp.raise_for_status()
    return data

def protect(prompt: str) -> dict:
    payload = {"prompt": prompt, "pipeline_id": PRIVARO_PIPELINE_ID, "conversation_id": "crewai-demo-001"}
    return privaro_post("/v1/proxy/protect", payload)

def reveal(content: str) -> dict:
    payload = {"conversation_id": "crewai-demo-001", "content": content}
    return privaro_post("/v1/proxy/reveal", payload)

def extract_protected_prompt(data: dict) -> str:
    return data.get("protected_prompt") or data.get("content") or json.dumps(data, ensure_ascii=False)

def main():
    raw_input = (
        "Client Juan Pérez from LegalCorp asks about unpaid invoice 45892. "
        "DNI 12345678A, IBAN ES7620770024003102575766."
    )

    print("\\n1) Protecting input with Privaro...")
    protected = protect(raw_input)
    print(json.dumps(protected, indent=2, ensure_ascii=False))
    protected_prompt = extract_protected_prompt(protected)

    llm = ChatOpenAI(model=OPENAI_MODEL, temperature=0.2)

    analyst = Agent(
        role="Enterprise AI assistant",
        goal="Draft a safe and concise response using sanitized placeholders only.",
        backstory="You help teams respond using privacy-safe data.",
        llm=llm,
        verbose=True,
    )

    task = Task(
        description=f"Prepare a short professional response to this request: {protected_prompt}",
        expected_output="A short email response that uses placeholders only.",
        agent=analyst,
    )

    crew = Crew(agents=[analyst], tasks=[task], verbose=True)

    print("\\n2) Running CrewAI on sanitized input...")
    result = crew.kickoff()
    result_text = str(result)
    print("\\nSanitized CrewAI output:")
    print(result_text)

    print("\\n3) Attempting reveal via Privaro...")
    try:
        revealed = reveal(result_text)
        print(json.dumps(revealed, indent=2, ensure_ascii=False))
    except Exception as e:
        print("Reveal endpoint not available or returned an error. This is OK for demo purposes.")
        print(str(e))

if __name__ == "__main__":
    main()
