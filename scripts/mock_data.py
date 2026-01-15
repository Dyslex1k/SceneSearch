import random
import requests
from faker import Faker
from enum import Enum

fake = Faker()

# ---------- Your enums (simplified for random generation) ----------
class UseCase(str, Enum):
    WORLDS = "Worlds"
    AVATARS = "Avatars"
    OSC = "Osc"

class Categories(str, Enum):
    MODELS_3D = "3D Models"
    ANIMATION = "Animations"
    MATERIALS = "Materials"
    AUDIO = "Audio"
    VFX = "Visual Effects"
    PARTICLES = "Particles"
    TOOLING = "Tooling"
    LIGHTING = "Lighting"
    UI = "UI"
    UDON = "Udon"
    SHADERS = "Shaders"

class LinkType(str, Enum):
    GUMROAD = "Gumroad"
    BOOTH = "Booth"
    JINXY = "Jinxy"
    GITHUB = "Github"
    GITLAB = "Gitlab"

class Licencing(str, Enum):
    OPENSOURCE = "Open Source"
    PROPRIETARY = "Proprietary"
    CUSTOM = "Custom"

# ---------- Config ----------
API_URL = "http://localhost:8000/prefabs/"
AUTH_TOKEN = ""
NUM_PREFABS = 500  # how many fake prefabs to create

# ---------- Helper functions ----------
def random_external_links(): # type: ignore
    num_links = random.randint(1, 2)
    links = []
    for _ in range(num_links):
        links.append({ # type: ignore
            "type": random.choice(list(LinkType)),
            "url": fake.url()
        })
    return links # type: ignore

def random_prefab_data(): # type: ignore
    return {
        "name": fake.sentence(nb_words=3).rstrip('.'),
        "description": fake.text(max_nb_chars=200),
        "content": fake.text(max_nb_chars=500),
        "use_cases": random.sample([uc.value for uc in UseCase], k=random.randint(1, 2)),
        "categories": random.sample([cat.value for cat in Categories], k=random.randint(1, 2)),
        "external_links": random_external_links(),
        "licence_type": random.choice([lic.value for lic in Licencing]),
        "is_free": random.choice([True, False])
    } # type: ignore

# ---------- Create prefabs ----------
headers = {
    "accept": "application/json",
    "Authorization": AUTH_TOKEN,
    "Content-Type": "application/json"
}

for _ in range(NUM_PREFABS):
    data = random_prefab_data() # type: ignore
    response = requests.post(API_URL, headers=headers, json=data) # type: ignore
    if response.status_code == 200 or response.status_code == 201:
        print(f"Created prefab: {data['name']}")
    else:
        print(f"Failed to create prefab: {response.status_code} {response.text}")
