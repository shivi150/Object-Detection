from imageai.Detection import ObjectDetection
import os
import cv2
from time import sleep
from tkinter import *

items = ["person","handbag","tie","bottle","cup","fork","knife","spoon","bowl","clock","toothbrush","hairdryer","teddy bear","scissors","vase"]
price = [ 2000   , 450      , 250   ,100    , 40  , 30   , 30    , 20    , 80   , 400  , 40         , 600       , 1200       , 150      ,  350 ]


def alert_popup(title, message):
    """Generate a pop-up window for special messages."""
    root = Tk()
    root.title(title)
    w = 400     # popup window width
    h = 200     # popup window height
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - w)/2
    y = (sh - h)/2
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    m = message
    w = Label(root, text=m, width=120, height=10)
    w.pack()
    b = Button(root, text="OK", command=root.destroy, width=10)
    b.pack()
    mainloop()

print("Starting....")
key = cv2. waitKey(1)
webcam = cv2.VideoCapture(0)
sleep(2)
while True:

    try:
        check, frame = webcam.read()
        #print(check) #prints true as long as the webcam is running
        #print(frame) #prints matrix values of each framecd 
        cv2.imshow("Capturing", frame)
        key = cv2.waitKey(1)
        if key == ord('s'):
            execution_path = os.getcwd()
            filename_input = execution_path + '\image_input.jpg'
            filename_output = execution_path + '\image_output.jpg'
            cv2.imwrite(filename_input, img=frame)
            print (filename_input)
            print (filename_output)
            webcam.release()
            print("Processing image...")
            #img_ = cv2.imread('saved_img.jpg', cv2.IMREAD_ANYCOLOR)
            print("Image saved!")

            detector = ObjectDetection()
            detector.setModelTypeAsRetinaNet()
            detector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.0.1.h5"))
            detector.loadModel()

            detections = detector.detectObjectsFromImage(input_image=filename_input, output_image_path=filename_output)

            root = Tk()
            root.title("Item Summary and Cost")
            w = 400     # popup window width
            h = 200     # popup window height
            sw = root.winfo_screenwidth()
            sh = root.winfo_screenheight()
            x = (sw - w)/2
            y = (sh - h)/2
            root.geometry('%dx%d+%d+%d' % (w, h, x, y))
            Lb1 = Listbox(root)

            index = 0
            cost = 0
            items_detected = []
            print("Item          :Cost   \n");
            for eachObject in detections:
                if eachObject["name"] in items:
                    #print(eachObject["name"] , "    : " , price[items.index(eachObject["name"])] )
                    cost = cost + price[items.index(eachObject["name"])]
                    #items_detected.append(eachObject["name"])
                    index = index + 1
                    cap_item=eachObject["name"]
                    l1=len(cap_item)
                    print(l1)
                    for i in range(l1,16):
                        cap_item = cap_item + " "
                    print(cap_item , ": " , price[items.index(eachObject["name"])] )
                    Lb1.insert(index, cap_item + ": " + str(price[items.index(eachObject["name"])]))

            Lb1.insert(index, "Total Cost     : " + str(cost))
            Lb1.pack()
            b = Button(root, text="OK", command=root.destroy, width=10)
            b.pack()
            mainloop()

            print("\nTotal Cost     : " + str(cost));

            #alert_popup("Summary", items_detected)
                
            
            
            break
        
        elif key == ord('q'):
            webcam.release()
            cv2.destroyAllWindows()
            break
    
    except(KeyboardInterrupt):
        print("Turning off camera.")
        webcam.release()
        print("Camera off.")
        print("Program ended.")
        cv2.destroyAllWindows()
        break
