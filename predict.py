import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image

# Load the trained model
model = tf.keras.models.load_model('leaf_model_with_unknown.h5')
classes = ['Blight', 'Healthy', 'Mosaic', 'Rust', 'Unknown']
threshold = 0.3  # confidence threshold for unknown prediction

def predict_image(img_path):
    img = image.load_img(img_path, target_size=(128, 128))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    pred = model.predict(img_array)
    max_prob = np.max(pred)
    if max_prob < threshold:
        pred_class = "Unknown"
    else:
        pred_class = classes[np.argmax(pred)]
    
    return pred_class

if __name__ == "__main__":
    test_img_path = 'C:/Users/suhan/Downloads/archive/PlantVillage/Tomato_healthy/e6fdaad9-b536-46c3-a819-faf414cfbf47___GH_HL Leaf 500.2.JPG'
    prediction = predict_image(test_img_path)
    print(f"Prediction class: {prediction}")
