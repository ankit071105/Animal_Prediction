#!/usr/bin/env python3
"""
Setup script for Animal Breed Identification System
This script will download a pre-trained model and set up the environment
"""

import os
import urllib.request
import zipfile
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
import pickle
import json

# Create directories
os.makedirs('models', exist_ok=True)
os.makedirs('data', exist_ok=True)

def download_pretrained_model():
    """Download a pre-trained model or create a simple one"""
    print("Setting up pre-trained model...")
    
    # Use MobileNetV2 with pre-trained weights
    base_model = MobileNetV2(weights='imagenet', 
                            include_top=False, 
                            input_shape=(224, 224, 3))
    
    # Add custom layers
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    predictions = Dense(37, activation='softmax')(x)  # 37 classes for Oxford Pets
    
    # Create model
    model = Model(inputs=base_model.input, outputs=predictions)
    
    # Save model
    model.save('models/animal_classifier.h5')
    print("Model saved to models/animal_classifier.h5")
    
    return model

def create_class_names():
    """Create class names for Oxford-IIIT Pets dataset"""
    class_names = [
        'Abyssinian', 'American Bulldog', 'American Pit Bull Terrier', 'Basset Hound',
        'Beagle', 'Bengal', 'Birman', 'Bombay', 'Boxer', 'British Shorthair',
        'Chihuahua', 'Egyptian Mau', 'English Cocker Spaniel', 'English Setter',
        'German Shorthaired', 'Great Pyrenees', 'Havanese', 'Japanese Chin', 'Keeshond',
        'Leonberger', 'Maine Coon', 'Miniature Pinscher', 'Newfoundland', 'Persian',
        'Pomeranian', 'Pug', 'Ragdoll', 'Russian Blue', 'Saint Bernard', 'Samoyed',
        'Scottish Terrier', 'Shiba Inu', 'Siamese', 'Sphynx', 'Staffordshire Bull Terrier',
        'Wheaten Terrier', 'Yorkshire Terrier'
    ]
    
    with open('models/class_names.pkl', 'wb') as f:
        pickle.dump(class_names, f)
    
    print("Class names saved to models/class_names.pkl")
    return class_names

def create_breed_info():
    """Create breed information JSON file"""
    breeds = [
        'Abyssinian', 'American Bulldog', 'American Pit Bull Terrier', 'Basset Hound',
        'Beagle', 'Bengal', 'Birman', 'Bombay', 'Boxer', 'British Shorthair',
        'Chihuahua', 'Egyptian Mau', 'English Cocker Spaniel', 'English Setter',
        'German Shorthaired', 'Great Pyrenees', 'Havanese', 'Japanese Chin', 'Keeshond',
        'Leonberger', 'Maine Coon', 'Miniature Pinscher', 'Newfoundland', 'Persian',
        'Pomeranian', 'Pug', 'Ragdoll', 'Russian Blue', 'Saint Bernard', 'Samoyed',
        'Scottish Terrier', 'Shiba Inu', 'Siamese', 'Sphynx', 'Staffordshire Bull Terrier',
        'Wheaten Terrier', 'Yorkshire Terrier'
    ]
    
    breed_info = {}
    for breed in breeds:
        animal_type = "Cat" if breed in [
            'Abyssinian', 'Bengal', 'Birman', 'Bombay', 'British Shorthair',
            'Egyptian Mau', 'Maine Coon', 'Persian', 'Ragdoll', 'Russian Blue',
            'Siamese', 'Sphynx'
        ] else "Dog"
        
        breed_info[breed] = {
            "animal_type": animal_type,
            "origin": "Various",
            "size": "Medium" if animal_type == "Cat" else "Varies",
            "lifespan": "12-15 years" if animal_type == "Cat" else "10-13 years",
            "coat": "Short" if breed in ['Bombay', 'Russian Blue', 'Sphynx'] else "Medium to Long",
            "colors": "Varies",
            "distinctive_features": "Varies by breed",
            "physical_traits": ["Varies by breed"],
            "temperament": ["Varies by breed"],
            "care_requirements": ["Regular grooming", "Balanced diet", "Veterinary check-ups"],
            "danger_level": "Low",
            "potential_risks": ["Scratches", "Bites if provoked", "Allergies"],
            "safety_precautions": ["Proper socialization", "Supervision with children", "Training"],
            "description": f"The {breed} is a {'cat' if animal_type == 'Cat' else 'dog'} breed with unique characteristics."
        }
    
    with open('data/breed_info.json', 'w') as f:
        json.dump(breed_info, f, indent=4)
    
    print("Breed info saved to data/breed_info.json")
    return breed_info

if __name__ == "__main__":
    print("Setting up Animal Breed Identification System...")
    
    # Install required packages
    print("Installing required packages...")
    os.system("pip install tensorflow pillow numpy streamlit")
    
    # Create model files
    download_pretrained_model()
    create_class_names()
    create_breed_info()
    
    print("\nSetup completed successfully!")
    print("You can now run the application with: streamlit run app.py")