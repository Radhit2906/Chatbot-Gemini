from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
from flask_cors import CORS
import traceback

# Memuat variabel lingkungan dari file .env
load_dotenv()

# Mengambil API Key dari environment
api_key = os.getenv("API_KEY")

if not api_key:
    raise Exception("API Key tidak ditemukan. Pastikan API Key sudah ada di .env")
else:
    genai.configure(api_key=api_key)


# Konfigurasi pengaturan generasi teks
generation_config = genai.types.GenerationConfig(
    candidate_count=1,       # Hanya mengembalikan 1 kandidat teks
    max_output_tokens=100,    # Jumlah token maksimal
    temperature=1.0           # Mengatur kreativitas teks (0.0 = lebih deterministik, 1.0 = lebih kreatif)
)

# Inisialisasi Flask
app = Flask(__name__)
CORS(app)

# Inisialisasi model
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(
    history=[
        {"role": "user", "parts": ["Halo"]},
        {"role": "model", "parts": ["Halo! Ada yang bisa saya bantu hari ini?"]},
    ]
)

# Route untuk memproses teks dari pengguna
@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.json  # Mendapatkan data JSON dari body request
    input_text = data.get('text')  # Ambil teks dari body request

    if not input_text:
        return jsonify({"error": "Teks tidak ditemukan pada body request."}), 400

    try:
        # Mengirim pesan ke model
        response = chat.send_message(input_text,generation_config=generation_config, stream=False)
        for chunk in response:
            result = chunk.text

        # Tambahkan konteks ke history chat
        chat.history.append({"role": "user", "parts": [input_text]})
        chat.history.append({"role": "model", "parts": [result]})

        # Mengembalikan respons dalam format JSON
        return jsonify({"response": result})
    except Exception as e:
        error_message = traceback.format_exc()
        print(f"Error: {error_message}")
        return jsonify({"error": "Terjadi kesalahan internal pada server.", "details": str(e), "trace": error_message}), 500

# Route untuk mengakhiri sesi chatbot
@app.route('/exit', methods=['GET'])
def exit_chat():
    global chat
    chat = model.start_chat(
        history=[
            {"role": "user", "parts": ["Halo"]},
            {"role": "model", "parts": ["Halo! Ada yang bisa saya bantu hari ini?"]},
        ]
    )
    return jsonify({"message": "Chatbot telah direset."}), 200

if __name__ == '__main__':
    app.run(debug=True)
