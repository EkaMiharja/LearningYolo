# Real-Time Vehicle Counter menggunakan YOLOv8 dan OpenCV

Proyek ini adalah sistem penghitung mobil (*vehicle counting*) secara *real-time* berbasis Python. Program ini memanfaatkan **YOLOv8 Object Tracking** dari Ultralytics untuk mendeteksi dan melacak pergerakan mobil, serta **MSS (Multiple Screen Shot)** untuk menangkap input video langsung dari area layar tertentu (seperti memutar video lalu lintas di YouTube).

Sistem menghitung kendaraan menggunakan logika **Virtual Counting Line** (Garis Pembatas Virtual). Setiap mobil yang melewati garis merah yang ditentukan akan otomatis menambah angka total hitungan.

## 🚀 Fitur Utama
* **Screen Capture Real-Time**: Mengambil input gambar langsung dari koordinat layar monitor secara cepat tanpa membebani kinerja webcam.
* **Fokus Deteksi Spesifik**: Menggunakan filter kelas YOLOv8 agar sistem hanya fokus mendeteksi objek mobil (`car`) dan mengabaikan objek lain.
* **Object Tracking Mandiri**: Setiap mobil diberikan ID unik agar kendaraan yang sama tidak terhitung dua kali saat melintasi layar.
* **Logika Penghitung Kustom**: Penghitungan murni menggunakan fungsi geometri OpenCV (`cv2.line`), sehingga bebas dari ketergantungan modul eksternal yang sering berubah struktur kodenya.

## 🛠️ Prasyarat & Instalasi

Pastikan Anda sudah menginstal Python (disarankan versi 3.8 ke atas) dan menggunakan IDE seperti PyCharm.

Buka terminal di PyCharm Anda, lalu instal pustaka yang diperlukan dengan menjalankan perintah berikut:

```bash
pip install ultralytics opencv-python mss numpy

💻 Cara Penggunaan
1. Jalankan file Python Anda (counyolo.py) melalui terminal atau tombol Run di PyCharm.
2. Buka browser Anda dan cari video arus lalu lintas di YouTube (misalnya dengan kata kunci "Traffic camera live" atau "Highway traffic video").
3. Posisikan jendela video YouTube Anda di area kiri atas layar monitor agar masuk ke dalam jangkauan koordinat rekam layar program.
4. Jendela OpenCV bernama YOLO Manual Vehicle Counter akan muncul menampilkan garis merah horizontal.
5. Selesai! Perhatikan angka Jumlah Mobil di pojok kiri atas yang akan terus bertambah setiap kali titik hijau di bawah mobil melewati garis merah.
6. Tekan tombol 'q' pada keyboard untuk menghentikan program dan menutup jendela video.

📊 Cara Kerja Logika Kode
Perekaman Layar: Fungsi mss() mengambil potongan layar pada koordinat kotak {"top": 100, "left": 100, "width": 800, "height": 600}.
Pelacakan Objek: Perintah model.track(..., classes=[2]) menyaring deteksi agar hanya mendeteksi mobil (ID kelas 2) dan memberikan nomor track_id unik pada setiap mobil.
Titik Acuan (Trigger): Program mencari titik tengah paling bawah dari bounding box mobil (center_y = int(y2)).
Eksekusi Hitungan: Jika koordinat center_y bernilai lebih besar dari posisi koordinat garis merah (LINE_Y = 350) dan track_id mobil tersebut belum terdaftar di dalam set already_counted, maka variabel counter akan bertambah 1 angka.

##StillLearning
