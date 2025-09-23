import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import os

# Paths to data directories
train_dir = 'train'
val_dir = 'validation'

# Parameters
image_size = (128, 128)
batch_size = 32
num_classes = 5  # 4 known classes + 1 unknown class
learning_rate = 1e-4
epochs = 10

# Training Data Augmentation including Unknown class
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.3,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Validation Data: Only rescale
val_datagen = ImageDataGenerator(rescale=1./255)

# Data generators for train and validation sets
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=image_size,
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=True
)

val_generator = val_datagen.flow_from_directory(
    val_dir,
    target_size=image_size,
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=False
)

# Base model - MobileNetV2 pretrained on ImageNet
base_model = MobileNetV2(input_shape=(*image_size, 3), include_top=False, weights='imagenet')
base_model.trainable = False  # Freeze base conv layers initially for transfer learning

# Add custom layers on top
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.4)(x)
predictions = Dense(num_classes, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

model.compile(optimizer=Adam(learning_rate), loss='categorical_crossentropy', metrics=['accuracy'])

print(model.summary())

# Train model
history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=epochs,
    verbose=1
)

# Save the trained model
model.save('leaf_model_with_unknown.h5')
