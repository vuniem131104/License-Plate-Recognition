import easyocr 
import string
# Initialize the OCR reader
reader = easyocr.Reader(['en'], gpu=False)

# Mapping dictionaries for character conversion
dict_char_to_int = {'O': '0',
                    'I': '1',
                    'J': '3',
                    'A': '4',
                    'G': '6',
                    'S': '5'}

dict_int_to_char = {'0': 'O',
                    '1': 'I',
                    '3': 'J',
                    '4': 'A',
                    '6': 'G',
                    '5': 'S'}

def license_complies_formate(text):
    
    if len(text) != 7:
        return False
    
    if (text[0] in dict_int_to_char.keys() or text[0] in string.ascii_uppercase) and \
        (text[1] in dict_int_to_char.keys() or text[1] in string.ascii_uppercase) and \
        (text[2] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[2] in dict_char_to_int.keys()) and \
        (text[3] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[3] in dict_char_to_int.keys()) and \
        (text[4] in dict_int_to_char.keys() or text[4] in string.ascii_uppercase) and \
        (text[5] in dict_int_to_char.keys() or text[5] in string.ascii_uppercase) and \
        (text[6] in dict_int_to_char.keys() or text[6] in string.ascii_uppercase):
            return True 
    else:
        return False
            
def format_license(text):
    
    license = ''
    for i in range(7):
        if i == 2 or i == 3:
            if text[i] in dict_char_to_int.keys():
                license += dict_char_to_int[text[i]]
            else:
                license += text[i]
        else:
            if text[i] in dict_int_to_char.keys():
                license += dict_int_to_char[text[i]]
            else:
                license += text[i]
    return license

def read_license_plate(image):
    
    results = reader.readtext(image)
    
    for result in results:
        bbox, text, score = result 
        text = text.upper().replace(' ', '')
        if license_complies_formate(text):
            return format_license(text), score 
    return None, None

def get_car(license_plate, track_ids):
    
    x1, y1, x2, y2, score, class_id = license_plate
    found = False
    for i in range(len(track_ids)):
        xcar1, ycar1, xcar2, ycar2, score = track_ids[i]
        if xcar1 < x1 and ycar1 < y1 and xcar2 > x2 and ycar2 > y2:
            idx = i
            found = True
    if found:
        return track_ids[idx]
    return -1, -1, -1, -1, -1

def write_csv(results, path):
    
    with open(path, 'w') as f:
        f.write('{},{},{},{},{},{},{}\n'.format('frame_nmr', 'car_id', 'car_bbox', 'license_plate_bbox', 'license_plate_bbox_score', 'license_number', 'license_number_score'))
        
        for frame in results.keys():
            if results[frame] != {}:
                for car in results[frame].keys():
                    f.write('{},{},{},{},{},{},{}\n'.format(frame, car, '[{} {} {} {}]'.format(
                                                                results[frame][car]['car']['bbox'][0],
                                                                results[frame][car]['car']['bbox'][1],
                                                                results[frame][car]['car']['bbox'][2],
                                                                results[frame][car]['car']['bbox'][3]), 
                                                            '[{} {} {} {}]'.format( 
                                                                                   results[frame][car]['license_plate']['bbox'][0],
                                                                                   results[frame][car]['license_plate']['bbox'][1],
                                                                                   results[frame][car]['license_plate']['bbox'][2],
                                                                                   results[frame][car]['license_plate']['bbox'][3]), 
                                                            results[frame][car]['license_plate']['bbox_score'],
                                                            results[frame][car]['license_plate']['text'], 
                                                            results[frame][car]['license_plate']['text_score']))
                    
        f.close()