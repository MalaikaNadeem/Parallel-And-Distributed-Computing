import cv2
import os
import time
import numpy as np
from concurrent.futures import ThreadPoolExecutor

input_dir = "data_set"
output_dir = "output_parallel"
os.makedirs(output_dir, exist_ok=True)

tasks = []
for class_name in os.listdir(input_dir):
    class_path = os.path.join(input_dir, class_name)
    if not os.path.isdir(class_path):
        continue
    for img_name in os.listdir(class_path):
        if img_name.lower().endswith(('.jpg', '.jpeg', '.png')):
            tasks.append((class_name, img_name))

workers_list = [1, 2, 4, 8]
results = []

def process_image(task):
    class_name, img_name = task
    img_path = os.path.join(input_dir, class_name, img_name)
    output_class_path = os.path.join(output_dir, class_name)
    os.makedirs(output_class_path, exist_ok=True)
    save_path = os.path.join(output_class_path, img_name)

    image = cv2.imread(img_path)
    if image is None:
        return

    image = cv2.resize(image, (128, 128))

    overlay = image.copy()
    text = "WATERMARK"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    thickness = 2

    color = (220, 220, 220)

    (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, thickness)
    x = image.shape[1] - text_w
    y = image.shape[0] - 10

    cv2.putText(overlay, text, (x, y), font, font_scale, color, thickness, cv2.LINE_AA)

    alpha = 0.55 
    watermarked = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)

    cv2.imwrite(save_path, watermarked)


if __name__ == "__main__":
    print("Processing images in parallel")

    for num_workers in workers_list:
        start = time.time()

        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            executor.map(process_image, tasks)

        end = time.time()
        elapsed = end - start
        results.append((num_workers, elapsed))

    print("Workers | Time (s) | Speedup")
    print("-------- | -------- | -------")

    baseline = results[0][1]
    for workers, t in results:
        speedup = baseline / t
        print(f"{workers:<8} | {t:>8.2f} | {speedup:>6.2f}x")
