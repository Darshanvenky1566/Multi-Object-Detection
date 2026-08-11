from ultralytics import YOLO
import cv2, numpy as np

m = YOLO('yolov8m-oiv7.pt')

# Use the existing test image in uploads folder
import os
imgs = [f for f in os.listdir('uploads') if f.endswith(('.jpg','.png','.jpeg'))]
if imgs:
    img = cv2.imread(f'uploads/{imgs[0]}')
    print(f"Testing with: {imgs[0]}, shape: {img.shape}")
    res = m.predict(source=img, conf=0.10, iou=0.4, imgsz=640, verbose=False)[0]
    print(f"\n=== DETECTIONS at conf=0.10 ===")
    for box in res.boxes:
        cid = int(box.cls[0])
        print(f"  {m.names[cid]} — {float(box.conf[0]):.2%}")
    print(f"Total: {len(res.boxes)} objects")
else:
    # Create a blank test
    img = np.zeros((640,640,3), dtype=np.uint8)
    img[:] = (50,50,50)
    res = m.predict(source=img, conf=0.10, iou=0.4, imgsz=640, verbose=False)[0]
    print(f"Blank image detections: {len(res.boxes)}")

# Print all class names containing watch, spoon, mouse
print("\n=== RELEVANT CLASSES ===")
for cid, name in m.names.items():
    if any(k in name.lower() for k in ['watch','spoon','mouse','phone','fork','cup','bottle']):
        print(f"  ID {cid}: {name}")
