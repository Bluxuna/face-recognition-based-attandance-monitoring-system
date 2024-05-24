import cv2
import os
import face_recognition
import time

# Define the path to save images
save_path = "PATH"
cap = cv2.VideoCapture(0)

# Function to save captured image
def save_image(image, name):
  filename = f"{name}_{int(time.time())}.jpg"
  full_path = os.path.join(save_path, filename)
  # Save the image
  cv2.imwrite(full_path, image)
  print(f"Image saved successfully: {full_path}")

while True:
  # Capture frame-by-frame
  ret, frame = cap.read()

  # Convert frame to RGB for face recognition
  rgb_frame = frame[:, :, ::-1]

  # Find all faces in the frame
  face_locations = face_recognition.face_locations(rgb_frame)

  # Loop through detected faces
  for (top, right, bottom, left) in face_locations:
    # Draw rectangle around detected face
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    # Start a 5-second timer
    start_time = time.time()
    time_left = 5

    while time_left > 0:
      # Display countdown on frame
      cv2.putText(frame, f"Capture in: {int(time_left)} seconds", (left, top - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

      # Update remaining time
      time_left = 5 - (time.time() - start_time)
      cv2.imshow('Face Detection', frame)
      cv2.waitKey(1)

    # User input for name after timer finishes
    name = input("Enter name for captured image: ")

    # Capture the face region of interest (ROI)
    roi = frame[top:bottom, left:right]

    # Save the captured face image with the user-provided name
    save_image(roi, name)

  # Display the resulting frame
  cv2.imshow('Face Detection', frame)

  # Exit on 'q' press
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

# Release capture object and close all windows
cap.release()
cv2.destroyAllWindows()
