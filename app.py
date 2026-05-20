import os
import sys
from pathlib import Path

from flask import Flask, request, render_template
from dotenv import load_dotenv

from playbook_product_review.retriever_generation import (
    data_ingestion,
    generation,
)

from langchain_groq import ChatGroq


# =========================================================
# Enforce project virtual environment
# =========================================================

project_root = Path(__file__).resolve().parent
expected_venv = project_root / "venv" / "Scripts" / "python.exe"
if expected_venv.exists():
    current_python = Path(sys.executable).resolve()
    if current_python != expected_venv.resolve():
        raise RuntimeError(
            "Please run this app with the project virtual environment. "
            "Use .\\venv\\Scripts\\activate or "
            "venv\\Scripts\\python.exe app.py."
        )


# =========================================================
# Load Environment Variables
# =========================================================

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise EnvironmentError("GROQ_API_KEY environment variable is required")

os.environ["GROQ_API_KEY"] = groq_api_key


# =========================================================
# Load LLM
# =========================================================

model = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0.5
)


# =========================================================
# Load Vector Store
# =========================================================

vstore = data_ingestion("done")


# =========================================================
# Create Conversational RAG Chain
# =========================================================

chain = generation(vstore)


# =========================================================
# Flask App
# =========================================================

app = Flask(__name__)


# =========================================================
# Home Route
# =========================================================

@app.route("/")
def index():

    return render_template("chat.html")


# =========================================================
# Chat Route
# =========================================================

@app.route("/get", methods=["POST"])
def chat():

    msg = request.form["msg"]

    result = chain.invoke(

        {
            "input": msg
        },

        config={
            "configurable": {
                "session_id": "justinfi.info"
            }
        }

    )["answer"]

    return str(result)


# =========================================================
# Run Application
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )