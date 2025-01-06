// Element DOM untuk UI dan respons
const voiceBtn = document.getElementById('voiceBtn');
const sendTextBtn = document.getElementById('sendTextBtn');
const chatBody = document.getElementById('chatBody'); // Tempat percakapan ditampilkan
const textInput = document.getElementById('textInput'); // Input teks manual

// Pengenalan suara (Speech Recognition)
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = 'id-ID'; // Set bahasa ke Indonesia

// Fungsi untuk menambahkan pesan ke UI
function addMessage(content, sender) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("chat-message", sender);
    const bubbleDiv = document.createElement("div");
    bubbleDiv.classList.add("message-bubble", sender);
    bubbleDiv.textContent = content;
    messageDiv.appendChild(bubbleDiv);

    // Tambahkan ke body chat dan scroll ke bawah
    chatBody.appendChild(messageDiv);
    chatBody.scrollTop = chatBody.scrollHeight;
}

// Fungsi untuk memulai pengenalan suara
voiceBtn.addEventListener('click', () => {
    console.log("Memulai pengenalan suara...");
    recognition.start();
    voiceBtn.innerText = 'Mendengarkan...';
});

// Ketika hasil dari pengenalan suara berhasil
recognition.onresult = (event) => {
    const speechToText = event.results[0][0].transcript;
    console.log("Teks yang diucapkan:", speechToText);
    addMessage(speechToText, "user"); // Tambahkan teks ke UI sebagai pesan user
    sendTextToServer(speechToText);  // Kirim teks ke server
};

// Ketika pengenalan suara berakhir
recognition.onend = () => {
    console.log("Pengenalan suara berakhir");
    voiceBtn.innerText = 'Mulai Bicara';
};

// Fungsi untuk mengirim teks yang diketik
sendTextBtn.addEventListener('click', () => {
    const inputText = textInput.value.trim();
    if (inputText !== "") {
        console.log("Teks yang diketik:", inputText);
        addMessage(inputText, "user"); // Tambahkan teks ke UI sebagai pesan user
        sendTextToServer(inputText);  // Kirim teks ke server
        textInput.value = "";  // Kosongkan input setelah dikirim
    } else {
        alert("Masukkan teks terlebih dahulu.");
    }
});

// Fungsi untuk mengirim teks ke Server dan memperoleh respons
function sendTextToServer(text) {
    console.log("Mengirim teks ke server:", text);

    fetch('http://127.0.0.1:5000/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text })
    })
    .then(response => {
        console.log("Respons dari server diterima");
        return response.json();
    })
    .then(data => {
        console.log("Data dari server:", data);
        addMessage(data.response, "bot"); // Tambahkan respons dari server sebagai pesan bot
        // speakResponse(data.response); // Membacakan respons
    })
    .catch(error => {
        console.error('Fetch error:', error);
        addMessage('Error: ' + error.message, "bot"); // Tampilkan pesan error di UI
    });
}

// Fungsi untuk membacakan respons menggunakan Speech Synthesis
function speakResponse(text) {
    console.log("Membacakan respons:", text);
    const speech = new SpeechSynthesisUtterance(text);
    speech.lang = 'id-ID';
    window.speechSynthesis.speak(speech);
}
