from ultralytics import YOLO 

model = YOLO("models/best.pt")

res = model.predict("Inputs_Videos/football_video_01.mp4",save=True)
print(res[0])
print('=====================================')
for box in res[0].boxes:
    print(box)