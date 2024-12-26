import cv2
import face_recognition
import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()


def greet_user(name):
    """Function to greet the user by name."""
    greeting = f"Hello, {name}!"
    engine.say(greeting)
    engine.runAndWait()


# Load known images and encode them (add more images if needed)
known_image1 = face_recognition.load_image_file("C:\\Studies\\Python\\PA\\assets\\person1.jpg")
known_image2 = face_recognition.load_image_file("C:\\Studies\\Python\\PA\\assets\\person2.jpg")

# Encode the known images
known_encoding1 = face_recognition.face_encodings(known_image1)[0]
known_encoding2 = face_recognition.face_encodings(known_image2)[0]

# List of known face encodings and their corresponding names
known_face_encodings = [known_encoding1, known_encoding2]
known_face_names = ["Nishchay Thepadiya", "Devesh Khanchane"]

# Access the webcam
video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

frame_skip = 5  # Process every 5th frame
frame_count = 0

while True:
    ret, frame = video_capture.read()

    if not ret:
        print("Failed to capture video")
        break

    # Skip frames
    if frame_count % frame_skip != 0:
        frame_count += 1
        continue

    frame_count += 1

    # Resize the frame for faster processing
    frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect face locations and face encodings
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    if face_encodings:  # Only process if any faces are found
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Calculate face distances to find the closest match
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = face_distances.argmin()

            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                greet_user(name)  # Call the greeting function when recognized

            # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            # Draw a label with the name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

    # Display the resulting frame
    cv2.imshow('Face Recognition', frame)

    # Press 'q' to exit the video stream
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the windows
video_capture.release()
cv2.destroyAllWindows()
