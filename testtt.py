from ultralytics import YOLO
import cv2

# 1. Initialize the webcam stream (0 is usually the default built-in camera)
cap = cv2.VideoCapture(0)

# 2. Load your custom trained YOLO weights
model = YOLO("runs/detect/train/weights/best.pt")

print("Press 'q' to exit the video stream.")

# 3. Create a continuous loop to handle live frames
while cap.isOpened():
    # Capture frame-by-frame from the webcam
    ret, frame = cap.read()
    
    # If the webcam fails to provide a frame, break the loop
    if not ret:
        print("Error: Failed to grab frame from webcam.")
        break

    # 4. Run real-time inference on the active 'frame' array
    # stream=True optimizes memory management for live feeds
    results = model.predict(
        source=frame,
        imgsz=640,
        conf=0.5,
        stream=True 
    )

    # 5. Extract results and plot the bounding boxes onto the frame
    for result in results:
        annotated_frame = result.plot()

        # 6. Display the live annotated video feed
        cv2.imshow("YOLO Detection", annotated_frame)

    # 7. Check if the user pressed the 'q' key to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 8. Clean up and close all windows after exiting the loop
cap.release()
cv2.destroyAllWindows()
