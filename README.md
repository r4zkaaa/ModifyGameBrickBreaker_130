
# ⚔️ Breakout: Edisi Pedang & Sarung Pedang

Selamat datang di proyek **Breakout: Sword Edition**! Ini adalah game klasik *Breakout / Brick Breaker* yang dibuat menggunakan bahasa pemrograman **Python** dan *library* **Tkinter**.

Game ini mengusung tema unik: kamu mengendalikan **Sarung Pedang** untuk memantulkan **Pedang** yang melayang menghancurkan barisan balok neon di layar.

---

## 🌟 Fitur Utama

1. **🎨 Tampilan Dark Mode Neon**
   - Latar belakang hitam pekat dengan balok-balok neon berwarna cerah yang estetis dan nyaman di mata.

2. **⚔️ Objek Kustom (Pedang & Sarung Pedang)**
   - Bola klasik diganti menjadi **Pedang Perak** berlis emas.
   - Papan (*Paddle*) diganti menjadi **Sarung Pedang** dari bahan kayu/kulit dengan lis emas.

3. **🖱️ Kontrol Mouse Responsif**
   - Sarung pedang bergerak mengikuti arah kursor mouse secara otomatis, membuat kontrol permainan terasa mulus dan mudah dimainkan.

4. **🔊 Efek Suara (Sound Effects) Tanpa Lag**
   - Menggunakan fitur *multithreading* bawaan Python agar nada bip (`winsound`) saat memantulkan bola atau menghancurkan balok tidak membuat layar patah-patah (*lag*).

5. **🔄 Fitur Restart Cepat**
   - Cukup tekan tombol `R` di *keyboard* untuk mengulang permainan kapan saja tanpa harus menutup aplikasi.

---

## 🎮 Cara Memainkan

### Kontrol Permainan:
* **Gerakkan Mouse (Kiri / Kanan)**: Menggerakkan Sarung Pedang.
* **Tombol `Space`**: Memulai permainan (meluncurkan pedang).
* **Tombol `R`**: Merestart game jika terkena *Game Over* atau ingin mulai dari awal.


## 🧩 Struktur Singkat Kodingan

* **`GameObject`**: Kelas dasar (induk) yang mengatur koordinat, pergerakan, dan penghapusan objek di canvas.
* **`Ball`**: Turunan dari `GameObject` yang menggambar pedang, mengatur arah gerakan, dan mendeteksi tabrakan.
* **`Paddle`**: Turunan dari `GameObject` yang menggambar sarung pedang dan mengatur gerakan mengikuti mouse.
* **`Brick`**: Turunan dari `GameObject` yang menggambar balok dan mengurangi ketahanan balok saat dipukul.
* **`Game`**: Kelas utama (`Frame`) tempat seluruh sistem game dijalankan, seperti pembuatan canvas, *game loop*, skor/nyawa, serta deteksi tombol keyboard.
