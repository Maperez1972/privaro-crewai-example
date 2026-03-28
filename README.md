# Privaro + CrewAI

![python](https://img.shields.io/badge/python-3.10+-blue)
![crewai](https://img.shields.io/badge/crewai-compatible-orange)
![license](https://img.shields.io/badge/license-MIT-green)

**Run AI agents with autonomy — without losing control of your data.**

---

## 🚀 What this is

This example shows how to integrate **Privaro** into a CrewAI workflow.

👉 Every agent step is protected before reaching the LLM.

---

## 🧩 Architecture

```
Agent Input
   ↓
Privaro (protect)
   ↓
CrewAI Agent
   ↓
LLM
   ↓
Privaro (reveal + audit)
```

---

## 🔥 Why this matters

AI agents:

- chain actions
- access multiple systems
- expand risk surface

👉 Privaro ensures:

- controlled data flow
- safe execution
- auditability

---

## ❌ Without Privaro

- Agents leak sensitive data
- No visibility
- No compliance guarantees

## ✅ With Privaro

- Tokenized interactions
- Scoped data per run
- Verifiable audit trail

---

## ⚡ Quickstart

```bash
git clone https://github.com/YOUR_REPO/privaro-crewai-example
cd privaro-crewai-example

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Run:

```bash
python app.py
```

---

## 🤖 Use with Agents

- Multi-agent systems
- Task delegation
- Tool execution

---

## 🧠 Who is this for

- Teams building agentic AI systems
- ISVs
- Enterprise architects

---

## 🔗 Related

- Proxy → https://github.com/Maperez1972/privaro-proxy
- LangChain example
- n8n example

---

## 🧭 Final Thought

Agents introduce autonomy.

Privaro introduces **boundaries**.
