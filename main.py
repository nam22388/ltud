from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from openai import OpenAI
import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

app = Flask(__name__, static_folder="static")
CORS(app)


embedding = OllamaEmbeddings(model="nomic-embed-text")
DB_PATH = "./db"

if os.path.exists(DB_PATH) and os.listdir(DB_PATH):
    db = Chroma(persist_directory=DB_PATH, embedding_function=embedding)
else:
    files = ["tai_lieu/CSDL.pdf"]
    documents = []
    for file in files:
        loader = PyPDFLoader(file)
        documents.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(documents)
    db = Chroma.from_documents(chunks, embedding, persist_directory=DB_PATH)


client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

system_prompt = """Bạn là chatbot hỗ trợ học tập môn cơ sở dữ liệu.
Nhiệm vụ của bạn là trả lời các câu hỏi liên quan đến môn học này.
Nếu bạn không biết câu trả lời, hãy nói rõ ràng bạn không biết.
Tuyệt đối không bịa ra thông tin nếu không có ngữ cảnh liên quan được cung cấp."""


chat_histories = {}

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "").strip()
    session_id = data.get("session_id", "default")

    if not user_input:
        return jsonify({"error": "Tin nhắn trống"}), 400

    
    if session_id not in chat_histories:
        chat_histories[session_id] = [{"role": "system", "content": system_prompt}]

    messages = chat_histories[session_id]

    
    results = db.similarity_search(user_input, k=3)
    context = "\n\n".join([r.page_content for r in results])
    rag_prompt = f"Dựa trên tài liệu sau:\n{context}\n\nHãy trả lời: {user_input}"

    messages.append({"role": "user", "content": rag_prompt})

    response = client.chat.completions.create(
        model="gemma2:9b",
        messages=messages
    )

    bot_reply = response.choices[0].message.content

    messages.pop()
    messages.append({"role": "user", "content": user_input})
    messages.append({"role": "assistant", "content": bot_reply})

    return jsonify({"reply": bot_reply})

@app.route("/reset", methods=["POST"])
def reset():
    data = request.json
    session_id = data.get("session_id", "default")
    if session_id in chat_histories:
        del chat_histories[session_id]
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    app.run(debug=True, port=5000)