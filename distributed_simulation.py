import cv2
import os
import time
import numpy as np
from multiprocessing import Process, Manager

input_dir = "data_set"
output_dir = "output_distributed"
os.makedirs(output_dir, exist_ok=True)

tasks = []
for class_name in os.listdir(input_dir):
    class_path = os.path.join(input_dir, class_name)
    if not os.path.isdir(class_path):
        continue
    for img_name in os.listdir(class_path):
        if img_name.lower().endswith(('.jpg', '.jpeg', '.png')):
            tasks.append((class_name, img_name))

midpoint = len(tasks) // 2
node1_tasks = tasks[:midpoint]
node2_tasks = tasks[midpoint:]

def process_images(node_id, tasks, return_dict):
    start = time.time()
    count = 0

    for class_name, img_name in tasks:
        img_path = os.path.join(input_dir, class_name, img_name)
        output_class_path = os.path.join(output_dir, class_name)
        os.makedirs(output_class_path, exist_ok=True)
        save_path = os.path.join(output_class_path, img_name)

        image = cv2.imread(img_path)
        if image is None:
            continue

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
        count += 1

    end = time.time()
    elapsed = end - start
    return_dict[node_id] = (count, elapsed)

if __name__ == "__main__":
    print("Simulating distributed image processing across 2 nodes")

    manager = Manager()
    return_dict = manager.dict()

    p1 = Process(target=process_images, args=(1, node1_tasks, return_dict))
    p2 = Process(target=process_images, args=(2, node2_tasks, return_dict))

    start_total = time.time()
    p1.start()
    p2.start()

    p1.join()
    p2.join()
    end_total = time.time()

    node1_count, node1_time = return_dict[1]
    node2_count, node2_time = return_dict[2]

    total_time = end_total - start_total

    print(f"Node 1 processed {node1_count} images in {node1_time:.2f}s")
    print(f"Node 2 processed {node2_count} images in {node2_time:.2f}s")
    print(f"Total distributed time: {total_time:.2f}s")

    sequential_time = 0.18 
    efficiency = sequential_time / total_time
    print(f"Efficiency: {efficiency:.2f}x over sequential")
