import face_recognition
import os

known_encodings = []
images = os.listdir('./face_dataset/')  # Path to your dataset

for image_file in images:
    image_path = f'./face_dataset/{image_file}'
    image = face_recognition.load_image_file(image_path)
    face_encodings = face_recognition.face_encodings(image)
    if face_encodings:  # Check if face was detected
        known_encodings.append(face_encodings[0])

# Save the encodings
import pickle
with open('face_encodings.dat', 'wb') as f:
    pickle.dump(known_encodings, f)
