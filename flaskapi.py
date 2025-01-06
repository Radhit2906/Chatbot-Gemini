from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

from flask_cors import CORS

  # Mengizinkan semua request dari semua origin


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
    max_output_tokens=500,    # Jumlah token maksimal
    temperature=1.0           # Mengatur kreativitas teks (0.0 = lebih deterministik, 1.0 = lebih kreatif)
)

# Teks default untuk history percakapan
default_text = """
        Halo, disini aku akan memberikan mu sebuah identitas untuk deployment mu.

        Namamu: BengBot
        Pembuat: Bengkel Koding
        Dibuat pada: Oktober 2024
        Tugas: Asisten Pribadi (Akademik)

        Jika seseorang bertanya "Siapa namamu?", kamu harus menjawab dengan nama lengkap dan sedikit penjelasan seperti: "Namaku BengBot","saya bengbot","aku bengbot".

        Jika seseorang menyebutkan namanya, maka kamu harus mengingatnya selalu dan jika seseorang bertanya siapa nama saya, maka kamu berhak menyebutkan siapa namanya.

        jawab semua jawaban dengan bahasa yang humanis
        Kamu Dilarang Keras menggunakan Emoji atau Markdown.

        Jika ada orang bertanya SKS yang harus diambil, tanyakan Semester berapa.
        Jika semesternya 1-2, maka jawab SKS akan dipaketkan secara otomatis oleh TU.
        Selain semester diatas, tanyakan berapa IPK yang mahasiswa peroleh semester lalu.
        Jika IPK diatas 3.00, maka sarankan mengambil 24 SKS.
        Jika IPK diatas 2.00, maka sarankan mengambil 20 SKS.
        Jika IPK dibawah 2.00, maka sarankan mengambil 16 SKS dan untuk mengikuti remidi.
    """

# Inisialisasi Flask
app = Flask(__name__)
CORS(app)

# Route untuk memproses teks dari pengguna
@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.json  # Mendapatkan data JSON dari body request
    input_text = data.get('text')  # Ambil teks dari body request

    if not input_text:
        return jsonify({"error": "Teks tidak ditemukan pada body request."}), 400

    # Logika chatbot
    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat(
        history=[
            {"role": "user", "parts": [default_text]},
            {"role": "user", "parts": [input_text]},
        ]
    )

    # Mengirim pesan ke model
    response = chat.send_message(input_text, generation_config=generation_config)

    # Mengembalikan respons dalam format JSON
    return jsonify({"response": response.text})

# Route untuk mengakhiri sesi chatbot
@app.route('/exit', methods=['GET'])
def exit_chat():
    return jsonify({"message": "Chatbot telah dihentikan."}), 200

if __name__ == '__main__':
    app.run(debug=True)
