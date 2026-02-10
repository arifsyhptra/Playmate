import pandas as pd
from openai import OpenAI
import pickle

# ============================
# 1. KONEKSI KE GROQ
# ============================
client = OpenAI(
    api_key="id grok         ",
    base_url="https://api.groq.com/openai/v1"
)

# ============================
# 2. DATASET FAQ
# ============================
df = pd.DataFrame([
    [1,"Apa itu DMS?","DMS adalah Document Management System untuk mengelola dokumen internal perusahaan."],
    [2,"Untuk apa DMS digunakan?","DMS digunakan untuk menyimpan, mencari, dan membagikan dokumen kerja dengan aman."],
    [3,"Siapa yang boleh menggunakan DMS?","Semua karyawan PT DIPO Mitsubishi yang memiliki akses akun."],
    [4,"Bagaimana cara login ke DMS?","Gunakan username dan password yang diberikan oleh IT atau HR."],
    [5,"Apa yang harus dilakukan jika lupa password DMS?","Hubungi tim IT Support untuk reset password."],
    [6,"Format dokumen apa yang bisa diupload ke DMS?","PDF,DOCX,XLSX,JPG,PNG."],
    [7,"Apakah ada batas ukuran file?","Ya,maksimal 10 MB per file."],
    [8,"Bagaimana cara upload dokumen?","Klik tombol Upload lalu pilih file dari komputer."],
    [9,"Kenapa upload gagal?","Biasanya karena ukuran file terlalu besar atau koneksi internet tidak stabil."],
    [10,"Bagaimana mencari dokumen di DMS?","Gunakan kolom pencarian dan ketik nama dokumen atau kata kunci."],
    [11,"Bisakah mengganti nama dokumen?","Ya,klik dokumen lalu pilih opsi Rename."],
    [12,"Apa fungsi folder di DMS?","Untuk mengorganisasi dokumen berdasarkan kategori atau divisi."],
    [13,"Bisakah membuat folder baru?","Ya,klik New Folder."],
    [14,"Siapa yang mengatur struktur folder?","Admin DMS atau kepala divisi."],
    [15,"Apa itu hak akses dokumen?","Hak akses menentukan siapa yang boleh melihat,mengedit,atau menghapus dokumen."],
    [16,"Siapa yang bisa mengatur hak akses?","Admin DMS atau atasan sesuai kebutuhan."],
    [17,"Bagaimana memberi akses dokumen ke rekan kerja?","Buka dokumen → Share → pilih nama karyawan."],
    [18,"Apa yang dimaksud dengan versioning?","Fitur untuk menyimpan dan melihat versi dokumen sebelumnya."],
    [19,"Apakah DMS otomatis menyimpan versi?","Ya,setiap ada upload revisi."],
    [20,"Bisa kah menghapus versi lama?","Ya,jika memiliki izin edit atau admin."],
    [21,"Bagaimana melihat riwayat dokumen?","Klik History pada detail dokumen."],
    [22,"Apa itu metadata dokumen?","Informasi tambahan seperti tanggal,uploader,divisi,dan kategori."],
    [23,"Bagaimana menambahkan metadata?","Saat upload dokumen,isi kolom metadata yang tersedia."],
    [24,"Apa itu dokumen publik?","Dokumen yang bisa dilihat semua karyawan."],
    [25,"Apa itu dokumen privat?","Dokumen yang hanya bisa diakses pemilik atau divisi tertentu."],
    [26,"Bagaimana membuat dokumen menjadi publik?","Ubah hak akses ke All Employees jika diizinkan."],
    [27,"Kenapa saya tidak bisa membuka dokumen tertentu?","Karena tidak memiliki hak akses."],
    [28,"Siapa yang bisa memberikan izin buka dokumen?","Pemilik dokumen atau admin."],
    [29,"Bagaimana cara mendownload dokumen?","Klik tombol Download pada detail dokumen."],
    [30,"Kenapa saya tidak bisa download?","Fitur download mungkin dibatasi untuk keamanan."],
    [31,"Bagaimana cara revisi dokumen?","Upload file baru dengan nama sama atau tombol Upload New Version."],
    [32,"Apakah bisa mengembalikan dokumen ke versi lama?","Ya,gunkan fitur Restore Version."],
    [33,"Apa fungsi recycle bin?","Menyimpan dokumen yang dihapus sementara."],
    [34,"Berapa lama dokumen di recycle bin?","30 hari sebelum dihapus permanen."],
    [35,"Bisa kah mengembalikan dokumen dari recycle bin?","Ya,klik Restore."],
    [36,"Kenapa dokumen tiba-tiba hilang?","Bisa jadi dipindah,terhapus,atau akses dicabut."],
    [37,"Bagaimana mengetahui siapa yang menghapus dokumen?","Lihat History."],
    [38,"Apakah DMS aman?","Ya,dilengkapi enkripsi dan kontrol akses."],
    [39,"Apakah DMS bisa diakses dari rumah?","Ya,selama menggunakan VPN perusahaan."],
    [40,"Bagaimana cara mendapatkan VPN?","Hubungi IT Support untuk instalasi."],
    [41,"Apakah DMS bisa diakses lewat HP?","Bisa,melalui browser mobile."],
    [42,"Browser apa yang disarankan?","Chrome atau Edge terbaru."],
    [43,"Kenapa DMS lambat?","Biasanya karena internet lambat atau server penuh."],
    [44,"Jam berapa maintenance DMS dilakukan?","Biasanya malam hari atau weekend."],
    [45,"Siapa PIC DMS?","Tim IT Infrastructure perusahaan."],
    [46,"Bagaimana melaporkan error?","Kirim email ke IT Support atau tiket internal."],
    [47,"Apa itu kategori dokumen?","Pengelompokan dokumen berdasarkan fungsi atau divisi."],
    [48,"Siapa yang menentukan kategori?","Admin atau kepala divisi."],
    [49,"Bagaimana memindahkan dokumen ke folder lain?","Gunakan fitur Move."],
    [50,"Kenapa saya tidak bisa memindahkan dokumen?","Karena tidak punya akses edit."],
    [51,"Siapa developernya?","Developernya Gerry, Tento, Ari, Adra dan Arief."]
])

# Ubah header
df.columns = ["id", "pertanyaan", "jawaban"]

# ============================
# 3. MEMBUAT EMBEDDING
# ============================
embeddings = []
for t in df["pertanyaan"]:
    res = client.embeddings.create(
        model="text-embedding-3-small",
        input=t
    )
    embeddings.append(res.data[0].embedding)

df["embedding"] = embeddings

# ============================
# 4. SIMPAN KE FILE
# ============================
df.to_pickle("faq.pkl")
print("Selesai membuat faq.pkl")

