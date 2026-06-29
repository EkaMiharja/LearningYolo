import cv2
import numpy as np
from mss import mss
from ultralytics import YOLO

# 1. Muat model YOLO
model = YOLO("yolov8n.pt")

# 2. Atur area layar YouTube
monitor = {"top": 100, "left": 100, "width": 800, "height": 600}

# 3. Tentukan posisi garis horizontal (y = 350)
LINE_Y = 350

# Variabel untuk menyimpan data hitungan
counter = 0
already_counted = set()  # Menyimpan ID mobil yang sudah lewat agar tidak dihitung 2 kali

cv2.namedWindow("YOLO Manual Vehicle Counter", cv2.WINDOW_NORMAL)

with mss() as sct:
    while True:
        screen_img = np.array(sct.grab(monitor))
        frame = cv2.cvtColor(screen_img, cv2.COLOR_BGRA2BGR)

        # 4. Jalankan tracking untuk kelas 2 (Mobil)
        results = model.track(frame, persist=True, show=False, classes=[2], verbose=False)

        # Gambar garis pembatas warna merah di layar
        cv2.line(frame, (0, LINE_Y), (800, LINE_Y), (0, 0, 255), 3)

        # 5. Ambil data kotak (boxes) dan ID tracking
        if results[0].boxes is not None and results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()  # Koordinat kotak [x1, y1, x2, y2]
            track_ids = results[0].boxes.id.cpu().numpy().astype(int)  # ID Unik Mobil

            for box, track_id in zip(boxes, track_ids):
                x1, y1, x2, y2 = box

                # Hitung titik tengah bagian bawah dari kotak mobil
                center_x = int((x1 + x2) / 2)
                center_y = int(y2)

                # Gambar titik tengah mobil di layar
                cv2.circle(frame, (center_x, center_y), 4, (0, 255, 0), -1)

                # Gambar kotak dan nomor ID mobil
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
                cv2.putText(frame, f"ID: {track_id}", (int(x1), int(y1) - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                # LOGIKA HITUNGAN:
                # Jika titik bawah mobil melewati garis LINE_Y, dan ID belum pernah dihitung
                if center_y > LINE_Y and track_id not in already_counted:
                    counter += 1
                    already_counted.add(track_id)

        # 6. Tampilkan teks total hitungan di pojok layar
        cv2.putText(frame, f"Jumlah Mobil: {counter}", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

        cv2.imshow("YOLO Manual Vehicle Counter", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()