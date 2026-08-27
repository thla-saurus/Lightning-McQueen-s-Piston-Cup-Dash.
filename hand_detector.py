from ultralytics import YOLO
import cv2
from multiprocessing.shared_memory import SharedMemory
from settings import Settings
import numpy as np

# 1. Initialize the webcam stream (0 is usually the default built-in camera)4

MEMORY_SIZE = 4
SHM_NAME = "lane_number_shm"
CAPTURE_START = 150
CAPTURE_END = 550
num_of_lanes = Settings().NUM_LANES
slope  = -(num_of_lanes-1)/(CAPTURE_END-CAPTURE_START)
y_intercept = slope*-CAPTURE_END
cap = cv2.VideoCapture(0)


cap_w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
cap_h = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

# 2. Load your custom trained YOLO weights
model = YOLO("ai_model/best.pt")

print("Press 'q' to exit the video stream.")

# 3. Create a continuous loop to handle live frames
try:
    shm  = SharedMemory(name = SHM_NAME,create=True,size=MEMORY_SIZE)
except FileExistsError:
    shm = SharedMemory(name = SHM_NAME)

buffer = np.ndarray((MEMORY_SIZE),dtype = np.uint8,buffer=shm.buf)
buffer.fill(0)

try:
    while cap.isOpened():
        # Capture frame-by-frame from the webcam
        ret, frame = cap.read()

        # If the webcam fails to provide a frame, break the loop
        if not ret:
            print("Error: Failed to grab frame from webcam.")
            break

        # 4. Run real-time inference on the active 'frame' array
        # stream=True optimizes memory management for live feeds
        results = model.predict(source=frame, imgsz=640, conf=0.5, stream=True,verbose= False)
        peace_detected = 0

        # 5. Extract results and plot the bounding boxes onto the frame
        for result in results:
            annotated_frame = result.plot()
            for box in result.boxes:
                x_center, y_center, _, _ = box.xywh[0].tolist()
                lane_number = int(slope*x_center+y_intercept)
                buffer[0] = lane_number
                print(buffer[0])
                #peace sign detection
                class_id = int(box.cls[0])
                if class_id == 0:
                    peace_detected = 1
            # 6. Display the live annotated video feed
            cv2.imshow("YOLO Detection", annotated_frame)
        buffer[1] = peace_detected    

        # 7. Check if the user pressed the 'q' key to quit
        
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # 8. Clean up and close all windows after exiting the loop
finally:
    shm.close()
    shm.unlink()
    cap.release()
    cv2.destroyAllWindows()
