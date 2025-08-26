import json
import pickle
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import sys
import os

# Add the parent directory to the path so we can import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import IMG_SIZE

def load_breed_info(file_path):
    """Load breed information from JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return generate_breed_info()

def generate_breed_info():
    """Generate breed information for Oxford-IIIT Pets dataset"""
    # These are the 37 breeds in the Oxford-IIIT Pets dataset
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
        # Determine if it's a cat or dog
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
    
    # Save the generated info
    with open('data/breed_info.json', 'w') as f:
        json.dump(breed_info, f, indent=4)
    
    return breed_info

def get_animal_features(breed_name, breed_data):
    """Extract features from breed data"""
    default_features = {
        'animal_type': 'Unknown',
        'origin': 'Not specified',
        'size': 'Not specified',
        'lifespan': 'Not specified',
        'coat': 'Not specified',
        'colors': 'Not specified',
        'distinctive_features': 'Not specified',
        'physical_traits': [],
        'temperament': ['Information not available'],
        'care_requirements': ['Information not available'],
        'danger_level': 'Unknown',
        'potential_risks': ['Information not available'],
        'safety_precautions': ['Information not available']
    }
    
    # Update with actual data if available
    if breed_data and breed_name in breed_data:
        for key in default_features:
            if key in breed_data[breed_name]:
                default_features[key] = breed_data[breed_name][key]
    
    return default_features

def preprocess_image(img):
    """Preprocess image for model prediction"""
    img = img.resize(IMG_SIZE)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = tf.keras.applications.resnet50.preprocess_input(img_array)
    return img_array