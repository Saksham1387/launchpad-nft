import os
import itertools
import json
from PIL import Image


TRAITS_DIR = "traits"  
IMAGE_SIZE = (800, 800)  
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
        "2.6": {"file": "2.6.png", "rarity": 0.2},
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
    #  "Neck Item": {
    #     "Beige Winter Scarf": {"file": "Beige Winter Scarf.png", "rarity": 0.4},
    #     "Dotted Bandana": {"file": "Dotted Bandana.png", "rarity": 0.2},
    #     "Lei": {"file": "Lei.png", "rarity": 0.2},
    #     "Pink Ribbon": {"file": "Pink Ribbon.png", "rarity": 0.2},
    # },
}

def generate_all_combinations(traits):
    
    trait_options = []
    for category, trait_dict in traits.items():
        trait_options.append([(category, trait_name, trait_data) 
                            for trait_name, trait_data in trait_dict.items()])
    
    
    all_combinations = list(itertools.product(*trait_options))
    images_and_metadata = []

    for combination in all_combinations:
        base_image = Image.new("RGBA", IMAGE_SIZE, (0, 0, 0, 0))
        metadata = {
            "attributes": []
        }


        for category, trait_name, trait_data in combination:
            metadata["attributes"].append({
                "trait_type": category,
                "value": trait_name
            })

            
            trait_image_path = os.path.join(TRAITS_DIR, category, trait_data["file"])
            try:
                trait_image = Image.open(trait_image_path).convert("RGBA")
                trait_image = trait_image.resize(IMAGE_SIZE)
                base_image = Image.alpha_composite(base_image, trait_image)
            except Exception as e:
                print(f"Error processing trait image {trait_image_path}: {str(e)}")
                continue

        images_and_metadata.append((base_image, metadata))

    return images_and_metadata

def save_images_and_metadata(images_and_metadata):
    for idx, (image, metadata) in enumerate(images_and_metadata):
        try:
            
            image_filename = f"output_{idx + 1}.png"
            image.save(os.path.join(OUTPUT_DIR, image_filename))

            
            # metadata_filename = f"output_{idx + 1}.json"
            with open(os.path.join(OUTPUT_DIR), "w") as metadata_file:
                json.dump(metadata, metadata_file, indent=4)
        except Exception as e:
            print(f"Error saving image/metadata {idx + 1}: {str(e)}")

def main():
    try:
        
        images_and_metadata = generate_all_combinations(TRAITS)
        
        
        save_images_and_metadata(images_and_metadata)
        
        print(f"Successfully generated {len(images_and_metadata)} images and metadata files.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()