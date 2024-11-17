import cv2
from ultralytics import YOLO
import os

# Cesty k videu a výsledkom
video_path = "data/akvarko1.mp4"  # Cesta k MP4 súboru
output_frames_dir = "frames"  # Adresár na ukladanie snímok
output_results_dir = "results"  # Adresár na ukladanie výsledkov

# Inicializácia modelu YOLO
model = YOLO("yolov8n.pt")  # Použi YOLOv8n (môžeš zmeniť model)

# Vytvor adresáre, ak neexistujú
os.makedirs(output_frames_dir, exist_ok=True)
os.makedirs(output_results_dir, exist_ok=True)

# Otvor video súbor
cap = cv2.VideoCapture(video_path)
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    if frame_count % 10 != 0:
        continue
    frame_filename = f"{output_frames_dir}/frame_{frame_count:04d}.jpg"
    
    # Uloženie snímky
    cv2.imwrite(frame_filename, frame)

    # Detekcia objektov pomocou YOLO
    results = model(frame)

    # Uloženie snímky s detekciou
    result_filename = f"{output_results_dir}/result_{frame_count:04d}.jpg"
    annotated_frame = results[0].plot()  # Annotovaná snímka s detekciou
    cv2.imwrite(result_filename, annotated_frame)

    print(f"Spracovaná snímka: {frame_filename} -> Detekcia uložená: {result_filename}")

cap.release()
print("Spracovanie dokončené.")

