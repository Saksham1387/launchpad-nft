import os
import random
from PIL import Image
import itertools


# Directory structure for traits
TRAITS_DIR = "traits"  # Root directory where trait folders are stored
OUTPUT_DIR = "output"  # Directory to save generated images
IMAGE_SIZE = (512, 512)  # Size of the output images

# Define traits and their rarities based on your structure
TRAITS = {
    "Background": {
        "Beach": {"file": "Beach.png", "rarity": 0.25},  # 25% chance
        "Black": {"file": "Black.png", "rarity": 0.25},  # 25% chance
        "Blue Blur": {"file": "Blue Blur.png", "rarity": 0.25},  # 25% chance
        "Blue Gradient": {"file": "Blue Gradient.png", "rarity": 0.25},  # 25% chance
    },
    "Body": {
        "Blue Gemstone": {"file": "Blue Gemstone.png", "rarity": 0.3},  # 30% chance
        "Original": {"file": "Original.png", "rarity": 0.3},  # 30% chance
        "Pastel Purple": {"file": "Pastel Purple.png", "rarity": 0.2},  # 20% chance
        "Pink Trippy": {"file": "Pink Trippy.png", "rarity": 0.2},  # 20% chance
    },
    "Expression": {
        "Curious": {"file": "Curious.png", "rarity": 0.4},  # 40% chance
        "Distracted with Eyelashes": {"file": "Distracted with Eyelashes.png", "rarity": 0.2},  # 20% chance
        "Emotional": {"file": "Emotional.png", "rarity": 0.2},  # 20% chance
        "Happy": {"file": "Happy.png", "rarity": 0.2},  # 20% chance
    },
}

# Create the output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)


def weighted_choice(choices):
    """Select a trait based on its rarity."""
    total = sum(choices[trait]["rarity"] for trait in choices)
    rand = random.uniform(0, total)
    upto = 0
    for trait, data in choices.items():
        if upto + data["rarity"] >= rand:
            return trait, data
        upto += data["rarity"]
    raise RuntimeError("Should not reach here")


def generate_image(traits, token_id):
    """Generate a unique image by combining selected traits."""
    base_image = Image.new("RGBA", IMAGE_SIZE, (0, 0, 0, 0))  # Transparent base

    metadata = {
        "name": f"NFT #{token_id}",
        "attributes": []
    }

    for trait_type, options in traits.items():
        # Pick a trait based on rarity
        selected_trait, data = weighted_choice(options)

        # Add the trait to metadata
        metadata["attributes"].append({
            "trait_type": trait_type,
            "value": selected_trait
        })

        # Load the trait image
        trait_image_path = os.path.join(TRAITS_DIR, trait_type, data["file"])
        trait_image = Image.open(trait_image_path).convert("RGBA")
        
        # Resize the trait image to match the base image dimensions
        trait_image = trait_image.resize(IMAGE_SIZE)

        # Composite the trait onto the base image
        base_image = Image.alpha_composite(base_image, trait_image)

    return base_image, metadata


def save_image_and_metadata(image, metadata, token_id):
    """Save generated image and metadata."""
    # Save image
    image_path = os.path.join(OUTPUT_DIR, f"{token_id}.png")
    image.save(image_path, format="PNG")

    # Save metadata
    metadata_path = os.path.join(OUTPUT_DIR, f"{token_id}.json")
    with open(metadata_path, "w") as metadata_file:
        import json
        json.dump(metadata, metadata_file, indent=4)


def main(total_images):
    """Main function to generate images and metadata."""
    generated_hashes = set()  # Keep track of generated combinations to ensure uniqueness

    for token_id in range(total_images):
        while True:
            # Generate unique traits combination
            traits_combination = []
            for trait_type in TRAITS.keys():
                selected_trait, _ = weighted_choice(TRAITS[trait_type])
                traits_combination.append(selected_trait)

            # Check for uniqueness
            combination_hash = tuple(traits_combination)
            if combination_hash not in generated_hashes:
                generated_hashes.add(combination_hash)
                break

        # Generate image and metadata
        image, metadata = generate_image(TRAITS, token_id)

        # Save to disk
        save_image_and_metadata(image, metadata, token_id)

        print(f"Generated NFT #{token_id} with traits: {traits_combination}")


if __name__ == "__main__":
    # Specify the number of images to generate
    total_images_to_generate = 10
    main(total_images_to_generate)

