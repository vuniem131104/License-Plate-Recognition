from sort import sort 
import cv2 
from ultralytics import YOLO
import numpy as np 
from utils import *

vehicles = [2,3,5,7]
coco_model = YOLO('yolov8n.pt')
license_detector = YOLO('license_plate_detector.pt')
video = cv2.VideoCapture('sample.mp4')
mot_tracker = sort.Sort()
results = {}
frame_nums = -1

while True:
    frame_nums += 1
    results[frame_nums] = {}
    ret, frame = video.read()
    if ret:
        detections_ = []
        object_results = coco_model.predict(frame)[0]
        for object_result in object_results.boxes.data.tolist():
            xcar1, ycar1, xcar2, ycar2, score, car_id = object_result
            if int(car_id) in vehicles:
                detections_.append([xcar1, ycar1, xcar2, ycar2, score])
        track_ids = mot_tracker.update(np.asarray(detections_))
        
        license_results = license_detector.predict(frame)[0]
        for license_result in license_results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = license_result
            xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_result, track_ids)
            if car_id != -1:
                license_plate_crop = frame[int(y1):int(y2), int(x1):int(x2), :]
                gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                _, license_plate_crop_threshold = cv2.threshold(gray, 64, 255, cv2.THRESH_BINARY_INV)
                license_plate_crop_text, license_plate_crop_text_score = read_license_plate(license_plate_crop_threshold)
                if license_plate_crop_text is not None:
                    results[frame_nums][car_id] = {'car': {'bbox': [xcar1, ycar1, xcar2, ycar2]}, 
                                                   'license_plate': {
                                                        'bbox': [x1, y1, x2, y2],
                                                        'text': license_plate_crop_text, 
                                                        'bbox_score': score,
                                                        'text_score': license_plate_crop_text_score
                                                   }}
        if cv2.waitKey(1) & 0xFF == 27:
            break 
    else:
        break

write_csv(results, 'output.csv')
print(results)
video.release()
cv2.destroyAllWindows()