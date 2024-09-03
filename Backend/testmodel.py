import tensorflow as tf
from mtcnn import MTCNN
import cv2
import time
from tensorflow.keras.layers import Activation, Dropout, Flatten, Dense, Input, Layer, Lambda, BatchNormalization
from tensorflow.keras.optimizers import Adam

from tensorflow.keras import metrics

model = tf.keras.models.load_model('finetuned_facenet_model.h5')
model.load_weights('finetuned_facenet.h5')
model.compile()

image_path = 'users_images/liviu.jpg'


def get_image_tensor(image_path):

    detector = MTCNN()

    # Load the image using OpenCV (or any other image loading method)
    x = cv2.imread(image_path)
    image = cv2.cvtColor(x, cv2.COLOR_BGR2RGB)  # Convert to RGB

    # Detect faces in the image
    results = detector.detect_faces(image)

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
        face = image[y:y + height, x:x + width]

        # Resize the face to the size expected by your model
        img_size = 160  # or whatever size your model expects
        face_resized = cv2.resize(face, (img_size, img_size))

        # Convert the face to a TensorFlow tensor and preprocess it
        face_tensor = tf.convert_to_tensor(face_resized, dtype=tf.float32)
        face_tensor = face_tensor / 255.0  # Normalize to [0, 1]
        face_tensor = tf.expand_dims(face_tensor, axis=0)  # Add batch dimension

        # Now 'face_tensor' is ready to be fed into your model
        print("Face tensor shape:", face_tensor.shape)
        return face_tensor
    else:
        print("No face detected in the image.")


x = get_image_tensor(image_path)

start_time = time.time()

print(model.predict(x))

end_time = time.time()
duration = end_time - start_time
print(f"Duration: {duration} seconds")