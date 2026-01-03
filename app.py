import os
from flask import Flask, render_template, request
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import markdown

# Load API Key
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

app = Flask(__name__)

# Konfigurasi Client Hugging Face
repo_id = "Qwen/Qwen2.5-72B-Instruct" 
client = InferenceClient(model=repo_id, token=HF_TOKEN)

# --- LAPIS 1: HARD FILTER (PYTHON SIDE) ---
# Kata-kata ini akan langsung ditolak tanpa tanya AI.
# Masukkan nama-nama brand besar di sini.
BLACKLIST_BRANDS = [
    "indomaret", "alfamart", "alfamidi", "kfc", "mcd", "mcdonald", 
    "starbucks", "pizza hut", "domino", "hypermart", "transmart", 
    "rumah sakit", "rsud", "siloam", "bank bca", "bank bri", "bank mandiri"
]

def check_blacklist(text):
    """Cek apakah input mengandung nama brand besar terlarang"""
    if not text: return False
    text_lower = text.lower()
    for brand in BLACKLIST_BRANDS:
        if brand in text_lower:
            return True
    return False

# --- LAPIS 2: PROMPT FILTER (AI SIDE) ---
CORE_GUARDRAILS = (
    "PERINGATAN SISTEM (SYSTEM OVERRIDE): "
    "Kamu adalah Asisten Khusus UMKM (Usaha Mikro, Kecil, Menengah) milik perorangan. "
    "Tugasmu HANYA membantu pedagang kecil, warung, atau jasa rumahan. "
    
    "DAFTAR LARANGAN KERAS (TOLAK INPUT INI): "
    "1. BRAND/FRANCHISE BESAR: Indomaret, Alfamart, KFC, McD, Starbucks, Brand Mall, dll. "
    "2. INSTITUSI MEDIS: Rumah Sakit, Klinik Dokter Spesialis, Obat Keras. "
    "3. KORPORAT/INSTANSI: Bank, Kantor Pemerintah, Politik. "
    
    "Jika input pengguna menyebutkan salah satu dari hal di atas, "
    "JAWAB PERSIS KALIMAT INI: 'Maaf, sistem ini khusus untuk pedagang kecil/UMKM perorangan, bukan untuk Waralaba Besar atau Institusi.'"
)

def get_ai_response(system_prompt, user_input):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]
    try:
        response = client.chat_completion(
            messages=messages,
            max_tokens=1500,
            temperature=0.7 
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# --- ROUTES ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/caption', methods=['GET', 'POST'])
def caption():
    result = None
    if request.method == 'POST':
        produk = request.form.get('produk')
        keunggulan = request.form.get('keunggulan')
        panjang_teks = request.form.get('length')
        
        # CEK FILTER LAPIS 1 (Python)
        if check_blacklist(produk):
            result = "🚫 **Maaf, fitur ini hanya untuk UMKM/Pedagang Kecil.**\n\nSistem mendeteksi nama Brand Besar/Waralaba/Institusi dalam input Anda. Silakan masukkan nama produk usaha Anda sendiri."
            return render_template('caption.html', result=markdown.markdown(result))

        # JIKA LOLOS, LANJUT KE AI (Lapis 2)
        sys_prompt = f"{CORE_GUARDRAILS} Kamu adalah Copywriter Media Sosial ahli."
        user_prompt = f"""
        TUGAS: Buatkan caption untuk produk UMKM: {produk}.
        Keunggulan: {keunggulan}.
        
        INSTRUKSI KHUSUS:
        1. Buat 3 Gaya Kontras:
           - Opsi 1: Gaya Santai & Gaul (Bestie).
           - Opsi 2: Gaya Formal & Elegan (Professional).
           - Opsi 3: Gaya Lucu/Humoris.
        2. Panjang: Sesuai request '{panjang_teks}'.
        3. Hashtag: gunakan hastag, hastagnya jangan spasi di setiap opsi, sertakan 5 hashtag relevan di akhir. untuk hastag jangan di spasi dengan (#)
        """
        
        raw_response = get_ai_response(sys_prompt, user_prompt)
        result = markdown.markdown(raw_response)
        
    return render_template('caption.html', result=result)

@app.route('/responder', methods=['GET', 'POST'])
def responder():
    result = None
    if request.method == 'POST':
        chat_masuk = request.form.get('komplain')
        
        # CEK FILTER LAPIS 1
        if check_blacklist(chat_masuk):
            result = "🚫 **Maaf, fitur ini hanya untuk UMKM.**\n\nSistem mendeteksi Anda mencoba merespons atas nama Brand Besar/Institusi."
            return render_template('responder.html', result=markdown.markdown(result))

        sys_prompt = f"{CORE_GUARDRAILS} Kamu adalah CS Toko yang cerdas."
        user_prompt = f"""
        TUGAS: Balas pesan pelanggan ini: "{chat_masuk}"
        
        ANALISIS DULU:
        - JIKA MARAH (Komplain): Minta maaf tulus, tawarkan solusi (Retur/Refund), nada merendah.
        - JIKA BAIK (Apresiasi): Ucapkan terima kasih ceria, doakan pelanggan.
        
        Outputkan teks balasannya saja.
        """
        
        raw_response = get_ai_response(sys_prompt, user_prompt)
        result = markdown.markdown(raw_response)
        
    return render_template('responder.html', result=result)

@app.route('/promo', methods=['GET', 'POST'])
def promo():
    result = None
    if request.method == 'POST':
        bulan = request.form.get('bulan')
        jenis_usaha = request.form.get('jenis_usaha')
        
        # CEK FILTER LAPIS 1
        if check_blacklist(jenis_usaha):
            result = "🚫 **Maaf, fitur ini hanya untuk UMKM.**\n\nMohon masukkan jenis usaha skala kecil/menengah."
            return render_template('promo.html', result=markdown.markdown(result))

        sys_prompt = f"{CORE_GUARDRAILS} Kamu adalah Konsultan Bisnis."
        user_prompt = f"""
        TUGAS: Ide Promo Bulanan untuk usaha: {jenis_usaha} di bulan {bulan}.
        
        INSTRUKSI:
        1. Kaitkan dengan event bulan {bulan}.
        2. Berikan 3 strategi unik.
        3. WAJIB ADA: RENTANG WAKTU (Misal: 1-7 {bulan}).
        """
        
        raw_response = get_ai_response(sys_prompt, user_prompt)
        result = markdown.markdown(raw_response)
        
    return render_template('promo.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)