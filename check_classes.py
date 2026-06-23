from ultralytics import YOLO
m = YOLO('yolov8m-oiv7.pt')
names = list(m.names.values())
print("TOTAL CLASSES:", len(names))
items = ['phone','mouse','spoon','fork','cup','bottle','laptop','keyboard','person','knife','watch','pen','book']
for i in items:
    matches = [n for n in names if i.lower() in n.lower()]
    print(f'{i}: {matches}')
