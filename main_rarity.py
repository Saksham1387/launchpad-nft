import os
import random
import json
from PIL import Image

TRAITS_DIR = "traits"
IMAGE_SIZE = (3000, 3000)
OUTPUT_DIR = "output_images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

TRAITS = {
    "Background": {
        "1.3": {"file": "1.3.png", "rarity": 0.25},
        "1.4": {"file": "1.4.png", "rarity": 0.25},
        "1.5": {"file": "1.5.png", "rarity": 0.25},
    },
    "Element": {
        "2.5": {"file": "2.5.png", "rarity": 0.4},
        "2.6": {"file": "2.6.png", "rarity": 0.4},
        "2.7": {"file": "2.7.png", "rarity": 0.2},
    },
    "Body": {
        "4.5": {"file": "4.5.png", "rarity": 0.3},
        "4.6": {"file": "4.6.png", "rarity": 0.3},
        "4.7": {"file": "4.7.png", "rarity": 0.2},
    },
    "Tag": {
        "5.6": {"file": "5.6.png", "rarity": 0.4},
        "5.7": {"file": "5.7.png", "rarity": 0.2},
        "5.8": {"file": "5.8.png", "rarity": 0.2},
    },
}

def pick_trait_by_rarity(category_traits):
    """
    Randomly pick one trait from a category (dictionary)
    according to that trait's rarity probability.
    """
    # Example: category_traits = {
    #   "1.3": {"file": "1.3.png", "rarity": 0.25},
    #   "1.4": {"file": "1.4.png", "rarity": 0.25},
    #   ...
    # }
    
    
    

    rand_value = random.random()
    cumulative = 0.0
    for trait_name, trait_data in category_traits.items():
        cumulative += trait_data["rarity"]
        if rand_value <= cumulative:
            return trait_name, trait_data
    
    # Fallback (shouldn’t usually happen if rarities sum to 1.0, but just in case):
    # Return the last trait in the dictionary
    trait_name, trait_data = list(category_traits.items())[-1]
    return trait_name, trait_data


def generate_images_with_rarity(traits, num_images=10):
    """
    Generate `num_images` NFT images, picking each trait based on its rarity.
    """
    images_and_metadata = []
    
    for _ in range(num_images):
        base_image = Image.new("RGBA", IMAGE_SIZE, (0, 0, 0, 0))
        
        # We'll store the attributes for the metadata
        metadata = {"attributes": []}
        
        for category, category_traits in traits.items():
            # 1) Pick trait by rarity
            trait_name, trait_data = pick_trait_by_rarity(category_traits)
            
            # 2) Add the trait info to metadata
            metadata["attributes"].append({
                "trait_type": category,
                "value": trait_name
            })
            
            # 3) Open and composite the trait image
            trait_image_path = os.path.join(TRAITS_DIR, category, trait_data["file"])
            try:
                trait_image = Image.open(trait_image_path).convert("RGBA")
                trait_image = trait_image.resize(IMAGE_SIZE)
                base_image = Image.alpha_composite(base_image, trait_image)
            except Exception as e:
                print(f"Error processing trait image {trait_image_path}: {str(e)}")
        
        # Append the final composed image + metadata
        images_and_metadata.append((base_image, metadata))
    
    return images_and_metadata


def save_images_and_metadata(images_and_metadata):
    """
    Saves the images and metadata to OUTPUT_DIR.
    """
    for idx, (image, metadata) in enumerate(images_and_metadata):
        try:
            image_filename = f"output_{idx + 1}.png"
            metadata_filename = f"output_{idx + 1}.json"
            
            # Save image
            image.save(os.path.join(OUTPUT_DIR, image_filename))
            
            # Save metadata
            with open(os.path.join(OUTPUT_DIR, metadata_filename), "w") as metadata_file:
                json.dump(metadata, metadata_file, indent=4)
        except Exception as e:
            print(f"Error saving image/metadata {idx + 1}: {str(e)}")


def main():
    # How many images you want to generate:
    num_images_to_generate = 10
    
    try:
        # Generate the images with rarity
        images_and_metadata = generate_images_with_rarity(TRAITS, num_images_to_generate)
        
        # Save them
        save_images_and_metadata(images_and_metadata)
        
        print(f"Successfully generated {len(images_and_metadata)} images and metadata files.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
