def json_to_image(json):
  #Read and load
  image = json['img']
  image_as_bytes = image.encode('utf-8')
  image_original = base64.b64decode(image_as_bytes)
  image_as_np = np.frombuffer(image_original, dtype=np.uint8)
  image_buffer = cv2.imdecode(image_as_np, flags=1)
  print(image_buffer.shape)
  #resizing and scaling