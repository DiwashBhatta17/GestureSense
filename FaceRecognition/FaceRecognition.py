import cv2
import os

# Load the pre-trained Haar Cascade model for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')

# Initialize the video capture object
cap = cv2.VideoCapture(0)

# Create a directory to store the captured images
dataset_path = './face_dataset/'
os.makedirs(dataset_path, exist_ok=True)

# Enter your name or identifier
face_id = input("Enter your name: ")

# Initialize counter for the image number
img_number = 0

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        continue

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Loop over the face detections
    for (x, y, w, h) in faces:
        # Draw rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Save the captured face into the datasets folder
        face_img = gray[y:y + h, x:x + w]
        face_filename = f"{dataset_path}/{face_id}_img_{img_number}.jpg"
        cv2.imwrite(face_filename, face_img)
        img_number += 1

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Break the loop with the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q') or img_number >= 100:  # Limit to 100 images for example
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
