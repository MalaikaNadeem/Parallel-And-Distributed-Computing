import cv2
import os
import time
import numpy as np

input_dir = "data_set"
output_dir = "output_seq"

start_time = time.time()

for class_name in os.listdir(input_dir):
    class_path = os.path.join(input_dir, class_name)
    if not os.path.isdir(class_path):
        continue

    output_class_path = os.path.join(output_dir, class_name)
    os.makedirs(output_class_path, exist_ok=True)

    for img_name in os.listdir(class_path):
        if not img_name.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        img_path = os.path.join(class_path, img_name)
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

        save_path = os.path.join(output_class_path, img_name)
        cv2.imwrite(save_path, watermarked)

end_time = time.time()
print(f"Sequential Processing Time: {end_time - start_time:.2f} seconds")
