## Summary
- Use openCV and easyOCR to read text from license plate in a car detected by YOLO
- Train YOLO on a custom dataset to create model that can detect license plate easily (get the data [here](https://universe.roboflow.com/roboflow-universe-projects/license-plate-recognition-rxg4e/dataset/4))
- The video I used in this project can be downloaded [here](https://drive.google.com/file/d/12sBfgLICdQEnDSOkVFZiJuUE6d3BeanT/view?usp=sharing).
- You can see the result below: 
![Screenshot from 2024-03-01 17-48-36](https://github.com/vuniem131104/License-Plate-Recognition/assets/124224840/72b98f4c-36e7-4e06-ac28-cf60ff25c676)
![Screenshot from 2024-03-01 17-48-15](https://github.com/vuniem131104/License-Plate-Recognition/assets/124224840/70a337d1-99cf-4cc2-a3b6-91f2b5c19c34)
## Steps you should follow if you want to do the same: 
- Clone this repo into your local computer and open it in your IDE
- Download the license plate detector model [here](https://drive.google.com/file/d/114gq0wJI5yPzBKDUEPR1NMbeaqqpEdVl/view?usp=sharing)
- Clone [this repo](https://github.com/abewley/sort) and put it into the folder you have cloned
- Execute main.py to create output.csv, then add_missing_data to generate test_interpolated.csv
- To have a csv file named out2.csv, you should sort test_interpolated.csv by "frame_nmr" column and save in your local.
- Last, you run visualize.py to see the results.
- Good Luck!
