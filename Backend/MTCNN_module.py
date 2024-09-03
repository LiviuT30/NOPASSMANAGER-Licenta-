import base64
import cv2
import numpy as np
import tensorflow as tf
from mtcnn import MTCNN


def get_image_tensor(json):
    # Decode the image from the JSON
    image = json['image']
    image_as_bytes = image.encode('utf-8')
    image_original = base64.b64decode(image_as_bytes)
    image_as_np = np.frombuffer(image_original, dtype=np.uint8)
    image_buffer = cv2.imdecode(image_as_np, flags=1)

    detector = MTCNN()

    # Convert the image from BGR to RGB
    image_rgb = cv2.cvtColor(image_buffer, cv2.COLOR_BGR2RGB)

    # Detect faces in the image
    results = detector.detect_faces(image_rgb)

    if results:
        # Assuming the first detected face is the one we want to use
        x, y, width, height = results[0]['box']
        # Add some padding to the bounding box (optional)
        padding = 10
        x = max(0, x - padding)
        y = max(0, y - padding)
        width += padding * 2
        height += padding * 2

        # Crop the face from the image
        face = image_rgb[y:y + height, x:x + width]

        # Resize the face to the size expected by your model
        img_size = 160  # Or whatever size your model expects
        face_resized = cv2.resize(face, (img_size, img_size))

        # Convert the face to a TensorFlow tensor and preprocess it
        face_tensor = tf.convert_to_tensor(face_resized, dtype=tf.float32)
        face_tensor = face_tensor / 255.0  # Normalize to [0, 1]
        face_tensor = tf.expand_dims(face_tensor, axis=0)  # Add batch dimension

        # Return the shape of the tensor
        print("Face tensor shape:", face_tensor.shape)
        return face_tensor
    else:
        print("No face detected in the image.")
        return None
