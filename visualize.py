import pandas as pd
import csv
import cv2

def overlay_image(background, overlay, x, y):
    overlay_height, overlay_width, _ = overlay.shape
    overlay_image = background.copy()
    overlay_image[y:y+overlay_height, x:x+overlay_width] = overlay
    return overlay_image

data = pd.read_csv('test_interpolated.csv')
idx = data.groupby('car_id')['license_number_score'].idxmax()
result_df = data.loc[idx]
df = result_df.iloc[:, [1, 5]]
data_dict = {}
for i in df.values:
    data_dict[i[0]] = i[1]

results = {}
with open('out2.csv', 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    for row in csv_reader:
        if int(row[0]) not in results.keys():
            results[int(row[0])] = {}
        results[int(row[0])][int(row[1])] = {} 
        results[int(row[0])][int(row[1])]['bbox1'] = [int(float(s)) for s in row[2].split(' ')]
        results[int(row[0])][int(row[1])]['bbox2'] = [int(float(s)) for s in row[3].split(' ')]
     
video = cv2.VideoCapture('sample.mp4')
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter('test.mp4', cv2.VideoWriter_fourcc(*'mp4v'), video.get(cv2.CAP_PROP_FPS), (width, height))
n = -1
check = results.keys()
while True:
    ret, frame = video.read()
    n += 1
    if ret:
        if n in check:
            info = results[n]
            for car in info.keys():
                xcar1, ycar1, xcar2, ycar2 = info[car]['bbox1'][0], info[car]['bbox1'][1], info[car]['bbox1'][2], info[car]['bbox1'][3]
                x1, y1, x2, y2 = info[car]['bbox2'][0], info[car]['bbox2'][1], info[car]['bbox2'][2], info[car]['bbox2'][3]
                license_plate_crop = frame[y1:y2, x1:x2, :]
                license_plate_crop = cv2.resize(license_plate_crop, (xcar2 - xcar1, 250))
                cv2.rectangle(frame, (xcar1, ycar1), (xcar2, ycar2), (0,255,0), 5)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,0,255), 4)
                cv2.rectangle(frame, (xcar1, ycar1 - 420), (xcar2, ycar1 - 250), (255,255,255), -1)
                text_size = cv2.getTextSize(data_dict[car], cv2.FONT_HERSHEY_SIMPLEX, 4.3, 17)[0]
                text_x = int((xcar1 + xcar2 - text_size[0]) / 2)
                text_y = int((ycar1 + ycar1 - 670 + text_size[1]) / 2)
                cv2.putText(frame, data_dict[car], (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 4.3, (0, 0, 0), 9)
                if xcar2 <= width:
                    frame = overlay_image(frame, license_plate_crop, xcar1, ycar1 - 250)
        out.write(frame)      
        if cv2.waitKey(1) & 0xFF == 27:
            break 
    else:
        break 

video.release()
out.release()
cv2.destroyAllWindows()