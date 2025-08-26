# This script would be used to train the actual model
# For demonstration purposes, we're using a pre-trained ResNet50 with custom layers

import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import numpy as np
import pickle

# This is a placeholder function - in a real scenario, you would train on actual animal data
def create_and_train_model():
    # Load pre-trained ResNet50 without the top layers
    base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    
    # Freeze the base model layers
    for layer in base_model.layers:
        layer.trainable = False
    
    # Add custom layers on top
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    x = Dropout(0.5)(x)
    predictions = Dense(120, activation='softmax')(x)  # 120 classes for demonstration
    
    # Create the model
    model = Model(inputs=base_model.input, outputs=predictions)
    
    # Compile the model
    model.compile(optimizer=Adam(learning_rate=0.001), 
                  loss='categorical_crossentropy', 
                  metrics=['accuracy'])
    
    # In a real scenario, you would train the model here with your animal dataset
    # For demonstration, we'll just save the untrained model architecture
    
    return model

# Create class names (in a real scenario, these would come from your dataset)
class_names = [
    "Siamese Cat", "Golden Retriever", "German Shepherd", "Maine Coon",
    "Persian Cat", "Bulldog", "Beagle", "Poodle", "Ragdoll", "Sphynx Cat"
    # Add more breeds as needed
]

# Create and save model
model = create_and_train_model()
model.save('model/animal_classifier.h5')

# Save class names
with open('model/class_names.pkl', 'wb') as f:
    pickle.dump(class_names, f)

print("Model and class names saved successfully!")