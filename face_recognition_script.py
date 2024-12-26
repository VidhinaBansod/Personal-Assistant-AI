import cv2
import face_recognition

# Load multiple images for each known person
known_images_nishchay = [
    face_recognition.load_image_file("C:\\Studies\\Python\\PA\\assets\\person1.jpg"),
    face_recognition.load_image_file("C:\\Studies\\Python\\PA\\assets\\nishchay2.jpg"),
    face_recognition.load_image_file("C:\\Studies\\Python\\PA\\assets\\nishchay3.jpg")
]

known_images_devesh = [
    face_recognition.load_image_file("C:\\Studies\\Python\\PA\\assets\\devesh1.jpg"),
    face_recognition.load_image_file("C:\\Studies\\Python\\PA\\assets\\devesh2.jpg"),
    face_recognition.load_image_file("C:\\Studies\\Python\\PA\\assets\\devesh3.jpg")
]

# Encode all images for each person
nishchay_encodings = [face_recognition.face_encodings(image)[0] for image in known_images_nishchay]
devesh_encodings = [face_recognition.face_encodings(image)[0] for image in known_images_devesh]

# Combine all encodings and names
known_face_encodings = nishchay_encodings + devesh_encodings
known_face_names = ["Nishchay Thepadiya"] * len(nishchay_encodings) + ["Devesh Khanchane"] * len(devesh_encodings)

# Access the webcam
video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    # Grab a single frame from the video
    ret, frame = video_capture.read()

    # Convert the frame to RGB (face_recognition uses RGB, OpenCV uses BGR)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect face locations and face encodings
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Loop through each face found in the frame
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Check for matches with known faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"  # Default if no match found

        # Calculate face distances to find the closest match
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = face_distances.argmin()

        if matches[best_match_index]:
            name = known_face_names[best_match_index]

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
