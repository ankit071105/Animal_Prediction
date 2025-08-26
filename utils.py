import json

def load_breed_info(file_path):
    """Load breed information from JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Return some default data if file doesn't exist
        return {
            "Siamese Cat": {
                "animal_type": "Cat",
                "origin": "Thailand",
                "size": "Medium",
                "lifespan": "15-20 years",
                "coat": "Short",
                "colors": "Cream with brown points",
                "distinctive_features": "Blue almond-shaped eyes, color points on ears, face, paws and tail",
                "physical_traits": ["Slender body", "Wedged-shaped head", "Large ears"],
                "temperament": ["Vocal", "Social", "Intelligent", "Demanding of attention"],
                "care_requirements": ["Regular grooming", "Interactive play", "High-quality diet"],
                "danger_level": "Low",
                "potential_risks": ["Scratches if provoked", "Allergies for some people"],
                "safety_precautions": ["Proper socialization", "Regular nail trimming", "Supervision with small children"],
                "description": "The Siamese cat is one of the first distinctly recognized breeds of Asian cat. Derived from the Wichianmat landrace, one of several varieties of cat native to Thailand."
            },
            "Golden Retriever": {
                "animal_type": "Dog",
                "origin": "Scotland",
                "size": "Large",
                "lifespan": "10-12 years",
                "coat": "Double coat, water-repellent",
                "colors": "Various shades of gold",
                "distinctive_features": "Friendly eyes, muscular build, feathery tail",
                "physical_traits": ["Broad head", "Friendly expression", "Powerful jaw"],
                "temperament": ["Intelligent", "Friendly", "Devoted", "Gentle"],
                "care_requirements": ["Regular exercise", "Frequent grooming", "Training and mental stimulation"],
                "danger_level": "Low",
                "potential_risks": ["Knocking over small children", "Jumping on people"],
                "safety_precautions": ["Proper training", "Socialization", "Supervision with very small children"],
                "description": "The Golden Retriever is a Scottish breed of retriever dog of medium size. It is characterized by a gentle and affectionate nature and a striking golden coat."
            }
        }

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
    if breed_data:
        for key in default_features:
            if key in breed_data:
                default_features[key] = breed_data[key]
    
    return default_features