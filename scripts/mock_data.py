from typing import Any
import requests
from faker import Faker
import random

# Initialize Faker
faker = Faker()

# Your API endpoint for prefabs
API_URL = "http://localhost:8000/prefabs"  # <- replace with your real endpoint

# VRChat-specific options
use_case_options = ["Worlds", "Avatars"]
category_options = ["Udon", "PhysBones", "Animators", "Audio", "Shaders", "Props"]

def generate_prefab() -> dict[str, Any]:
    """Generates a fake VRChat prefab JSON object"""
    prefab: dict[str, Any] = {
        "name": faker.unique.word().capitalize() + "Prefab",
        "description": faker.sentence(),
        "content": faker.text(max_nb_chars=200),
        "use_cases": random.sample(use_case_options, k=1),  # pick 1
        "categories": random.sample(category_options, k=random.randint(1, 2)),
        "tags": [faker.word() for _ in range(random.randint(2, 5))],
        "external_links": [
            {
                "type": "documentation",
                "url": faker.url()
            }
        ]
    }
    return prefab

def post_prefab(prefab: dict[str, Any]):
    """Posts a prefab to the API"""
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(API_URL, json=prefab, headers=headers)
    if response.status_code == 201:
        print(f"Prefab '{prefab['name']}' posted successfully!")
    else:
        print(f"Failed to post '{prefab['name']}': {response.status_code}, {response.text}")

def main():
    for _ in range(20):
        prefab = generate_prefab()
        post_prefab(prefab)

if __name__ == "__main__":
    main()
