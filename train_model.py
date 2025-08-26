# Complete training script for Oxford-IIIT Pets dataset
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import pickle
import json
import os
import sys

# Add the parent directory to the path so we can import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *
from utils import generate_breed_info

# Set random seed for reproducibility
tf.random.set_seed(42)
np.random.seed(42)

def load_and_preprocess_data():
    """Load and preprocess the Oxford-IIIT Pets dataset"""
    print("Loading and preprocessing data...")
    
    # Create data generators
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        validation_split=0.2  # Use 20% for validation
    )
    
    # Load images from directory
    train_generator = train_datagen.flow_from_directory(
        IMAGES_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training'
    )
    
    validation_generator = train_datagen.flow_from_directory(
        IMAGES_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation'
    )
    
    # Get class names
    class_names = list(train_generator.class_indices.keys())
    
    return train_generator, validation_generator, class_names

def create_model():
    """Create the model architecture"""
    print("Creating model architecture...")
    
    # Load pre-trained ResNet50 without the top layers
    base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3))
    
    # Freeze the base model layers
    for layer in base_model.layers:
        layer.trainable = False
    
    # Add custom layers on top
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    x = Dropout(0.5)(x)
    predictions = Dense(NUM_CLASSES, activation='softmax')(x)
    
    # Create the model
    model = Model(inputs=base_model.input, outputs=predictions)
    
    # Compile the model
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def train_model():
    """Train the model"""
    print("Starting model training...")
    
    # Load data
    train_generator, validation_generator, class_names = load_and_preprocess_data()
    
    # Create model
    model = create_model()
    
    # Callbacks
    callbacks = [
        EarlyStopping(patience=10, restore_best_weights=True),
        ModelCheckpoint(MODEL_PATH, save_best_only=True),
        ReduceLROnPlateau(factor=0.2, patience=5)
    ]
    
    # Train the model
    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=validation_generator,
        callbacks=callbacks,
        verbose=1
    )
    
    # Save class names
    with open(CLASS_NAMES_PATH, 'wb') as f:
        pickle.dump(class_names, f)
    
    # Generate breed info if it doesn't exist
    if not os.path.exists(BREED_INFO_PATH):
        generate_breed_info()
    
    print("Model training completed successfully!")
    print(f"Model saved to: {MODEL_PATH}")
    print(f"Class names saved to: {CLASS_NAMES_PATH}")

if __name__ == "__main__":
    # Check if dataset is downloaded
    if not os.path.exists(IMAGES_DIR) or len(os.listdir(IMAGES_DIR)) == 0:
        print("Please download the dataset first by running: python data/download_data.py")
    else:
        train_model()