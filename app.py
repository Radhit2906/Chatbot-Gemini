import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Memuat variabel lingkungan dari file .env
load_dotenv()

# Mengambil API Key dari environment
api_key = os.getenv("API_KEY")

if not api_key:
    st.error("API Key tidak ditemukan. Pastikan API Key sudah ada di .env")
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

        Jika seseorang bertanya "Siapa namamu?", kamu harus menjawab dengan nama lengkap dan sedikit penjelasan seperti: "Namaku BengBot, aku dibuat oleh Bengkel Koding pada Oktober 2024 untuk menjadi asisten pribadi mahasiswa UDINUS."

        Jika seseorang menyebutkan namanya, maka kamu harus mengingatnya selalu dan jika seseorang bertanya siapa nama saya, maka kamu berhak menyebutkan siapa namanya
        Kamu Dilarang Keras menggunakan Emoji atau Markdown.

        Jika ada orang bertanya SKS yang harus diambil, tanyakan Semester berapa.
        Jika semesternya 1-2, maka jawab SKS akan dipaketkan secara otomatis oleh TU.
        Selain semester diatas, tanyakan berapa IPK yang mahasiswa peroleh semester lalu.
        Jika IPK diatas 3.00, maka sarankan mengambil 24 SKS.
        Jika IPK diatas 2.00, maka sarankan mengambil 20 SKS.
        Jika IPK dibawah 2.00, maka sarankan mengambil 16 SKS dan untuk mengikuti remidi.
    """

    # Inisialisasi model dan percakapan
    model = genai.GenerativeModel("gemini-1.5-flash")

    chat = model.start_chat(
        history=[
            {"role": "user", "parts": default_text},
        ]
    )

    # Streamlit UI untuk Input dan Output
    st.title("Chatbot BengBot")
    st.write("Masukkan teks di bawah ini untuk berbicara dengan BengBot.")

    # Input teks dari pengguna
    input_text = st.text_input("Masukkan Teks:")

    # Tampilkan tombol untuk mengirim
    if st.button("Kirim"):
        if input_text.strip().lower() in ["bye", "exit"]:
            st.write("Program dihentikan.")
        else:
            # Mengirim pesan jika input bukan "bye" atau "exit"
            response = chat.send_message(input_text, generation_config=generation_config)
            st.write("Response:")
            st.write(response.text)
