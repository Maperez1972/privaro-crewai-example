import json
import os
import uuid
import requests
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PRIVARO_API_KEY = os.getenv("PRIVARO_API_KEY")
PRIVARO_PIPELINE_ID = os.getenv("PRIVARO_PIPELINE_ID")
PRIVARO_BASE_URL = os.getenv("PRIVARO_BASE_URL", "https://api.privaro.ai").rstrip("/")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

HEADERS = {"Content-Type": "application/json", "X-Privaro-Key": PRIVARO_API_KEY}


def privaro_post(path: str, payload: dict) -> dict:
    resp = requests.post(f"{PRIVARO_BASE_URL}{path}", headers=HEADERS, json=payload, timeout=60)
    data = resp.json()
    resp.raise_for_status()
    return data


def protect(prompt: str, conversation_id: str) -> dict:
    payload = {"prompt": prompt, "pipeline_id": PRIVARO_PIPELINE_ID, "conversation_id": conversation_id}
    return privaro_post("/v1/proxy/protect", payload)


def detokenize(text: str, conversation_id: str) -> dict:
    # See the LangChain example's app.py for a longer explanation. In
    # short: this is /v1/proxy/detokenize, NOT /v1/proxy/reveal (which
    # does not exist) -- and conversation_id must be the exact same UUID
    # used in protect() above, since tokens are only unique within one
    # conversation, not globally.
    payload = {"text": text, "pipeline_id": PRIVARO_PIPELINE_ID, "conversation_id": conversation_id}
    return privaro_post("/v1/proxy/detokenize", payload)


def extract_protected_prompt(data: dict) -> str:
    return data.get("protected_prompt") or data.get("content") or json.dumps(data, ensure_ascii=False)


def main():
    conversation_id = str(uuid.uuid4())

    raw_input = (
        "Client Juan Pérez from LegalCorp asks about unpaid invoice 45892. "
        "DNI 12345678A, IBAN ES7620770024003102575766."
    )

    print("\n1) Protecting input with Privaro...")
    protected = protect(raw_input, conversation_id)
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

    print("\n2) Running CrewAI on sanitized input...")
    result = crew.kickoff()
    result_text = str(result)
    print("\nSanitized CrewAI output:")
    print(result_text)

    print("\n3) Detokenizing the crew's response via Privaro...")
    revealed = detokenize(result_text, conversation_id)
    print(json.dumps(revealed, indent=2, ensure_ascii=False))
    print("\nFinal, human-readable output:")
    print(revealed.get("detokenized_text", result_text))


if __name__ == "__main__":
    main()
