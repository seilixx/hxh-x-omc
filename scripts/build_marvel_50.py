import json

with open('src/data/marvel/characters.ts', 'r', encoding='utf-8') as f:
    text = f.read()

prefix = 'export const marvelCharacters: Character[] = '
start = text.find(prefix) + len(prefix)
end = text.find('];', start) + 1
existing = json.loads(text[start:end])

# Rebalance some existing difficulties
for c in existing:
    if c['id'] in ['marvel-025']: # Doctor Doom
        c['difficulty'] = 'expert'
    elif c['id'] in ['marvel-007']: # Thanos
        c['difficulty'] = 'easy'
    elif c['id'] in ['marvel-008']: # Loki
        c['difficulty'] = 'easy'
    elif c['id'] in ['marvel-012']: # Wolverine
        c['difficulty'] = 'easy'
    elif c['id'] in ['marvel-014']: # Deadpool
        c['difficulty'] = 'easy'

new_heroes = [
    {
        "id": "marvel-031",
        "name": "Kingpin",
        "wiki": "Kingpin (character)",
        "acceptedAnswers": ["kingpin", "wilson fisk", "fisk"],
        "aliases": ["Wilson Fisk", "The Kingpin of Crime"],
        "arc": "Street Level & Knights",
        "affiliation": "Fisk Industries / Crime Syndicate",
        "difficulty": "hard",
        "description": "Massive, ruthless criminal mastermind Wilson Fisk who controls New York's underworld behind a legitimate corporate facade, nemesis of Daredevil and Spider-Man.",
        "hints": [
            {"time": 30, "text": "I am a hulking, bald crime lord clad in an immaculate white three-piece suit who carries an obliterator cane."},
            {"time": 60, "text": "Despite looking obese, my colossal 400-pound frame is nearly pure superhumanly dense muscle and bone."},
            {"time": 90, "text": "Known as Wilson Fisk, I rule Hell's Kitchen through extortion and bribery, serving as the arch-nemesis of Daredevil."}
        ],
        "image": "/assets/characters/marvel/marvel-031.jpg",
        "anime": "marvel"
    },
    {
        "id": "marvel-032",
        "name": "Red Skull",
        "wiki": "Red Skull",
        "acceptedAnswers": ["red skull", "johann shmidt", "johann schmidt"],
        "aliases": ["Johann Schmidt", "Supreme Hydra"],
        "arc": "Phase 1: Assemble",
        "affiliation": "HYDRA / Nazi Germany",
        "difficulty": "hard",
        "description": "Johann Schmidt, head of HYDRA during World War II whose face was grotesque scarlet bone from an imperfect Super Soldier Serum, Captain America's supreme nemesis.",
        "hints": [
            {"time": 30, "text": "My head resembles a terrifying crimson skull after testing an unstable early version of Erskine's Super Soldier Serum."},
            {"time": 60, "text": "I founded the occult rogue science division HYDRA, hailing: 'Cut off one head, two more shall take its place!'"},
            {"time": 90, "text": "Cast into the cosmos by the Tesseract, I became the ethereal guardian of the Soul Stone on the barren planet Vormir."}
        ],
        "image": "/assets/characters/marvel/marvel-032.jpg",
        "anime": "marvel"
    },
    {
        "id": "marvel-033",
        "name": "Galactus",
        "wiki": "Galactus",
        "acceptedAnswers": ["galactus", "galan"],
        "aliases": ["The Devourer of Worlds", "Galan of Taa"],
        "arc": "Cosmic & Interstellar",
        "affiliation": "Cosmic Entities",
        "difficulty": "expert",
        "description": "Colossal primordial cosmic being who survived the destruction of the pre-Big Bang universe, forced to consume the life energies of living planets to survive.",
        "hints": [
            {"time": 30, "text": "I wear iconic horned purple armor and am depicted as tall as a skyscraper or planet."},
            {"time": 60, "text": "I empower heralds with the Power Cosmic (like Silver Surfer) to scout the cosmos for planets to consume."},
            {"time": 90, "text": "Known as the Devourer of Worlds, I wield the world-ending Ultimate Nullifier as my ultimate conceptual threat."}
        ],
        "image": "/assets/characters/marvel/marvel-033.jpg",
        "anime": "marvel"
    },
    {
        "id": "marvel-034",
        "name": "Silver Surfer",
        "wiki": "Silver Surfer",
        "acceptedAnswers": ["silver surfer", "norrin radd"],
        "aliases": ["Norrin Radd", "The Sentinel of the Spaceways"],
        "arc": "Cosmic & Interstellar",
        "affiliation": "Galactus (former) / Defenders",
        "difficulty": "hard",
        "description": "Astronomer Norrin Radd from Zenn-La who sacrificed his freedom to become the herald of Galactus, riding a silver surfboard through deep space using the Power Cosmic.",
        "hints": [
            {"time": 30, "text": "My entire body is covered in metallic silver skin and I traverse interstellar hyperspace on a flying surfboard."},
            {"time": 60, "text": "I sacrificed my life on planet Zenn-La to serve as the cosmic herald for the planet-devourer Galactus."},
            {"time": 90, "text": "Empowered by the Power Cosmic, I turned against Galactus after being moved by the compassion of Alicia Masters on Earth."}
        ],
        "image": "/assets/characters/marvel/marvel-034.jpg",
        "anime": "marvel"
    },
    {
        "id": "marvel-035",
        "name": "Kang the Conqueror",
        "wiki": "Kang the Conqueror",
        "acceptedAnswers": ["kang", "kang the conqueror", "nathaniel richards", "he who remains"],
        "aliases": ["Nathaniel Richards", "He Who Remains", "Rama-Tut"],
        "arc": "Phase 4 & 5: Multiverse",
        "affiliation": "Council of Kangs / TVA",
        "difficulty": "hard",
        "description": "31st-century time-traveling scholar Nathaniel Richards who conquered countless timelines, waging a multiversal war across divergent realities.",
        "hints": [
            {"time": 30, "text": "I wear futuristic 40th-century armor with a glowing blue digital visor mask and green-and-purple tunic."},
            {"time": 60, "text": "A descendant of Reed Richards and Doctor Doom from the 31st century, I discovered the secrets of the Multiverse."},
            {"time": 90, "text": "My multiversal variants include Pharaoh Rama-Tut, Immortus, Iron Lad, and the creator of the TVA: He Who Remains."}
        ],
        "image": "/assets/characters/marvel/marvel-035.jpg",
        "anime": "marvel"
    },
    {
        "id": "marvel-036",
        "name": "Gambit",
        "wiki": "Gambit (Marvel Comics)",
        "acceptedAnswers": ["gambit", "remy lebeau"],
        "aliases": ["Remy LeBeau", "The Ragin' Cajun"],
        "arc": "X-Men & Mutants",
        "affiliation": "X-Men / Thieves Guild",
        "difficulty": "medium",
        "description": "Charming Cajun mutant thief Remy LeBeau who charges inorganic matter with explosive kinetic energy, throwing explosive glowing playing cards.",
        "hints": [
            {"time": 30, "text": "I speak with a heavy Cajun French accent, wear a brown duster trench coat, and have black eyes with red pupils."},
            {"time": 60, "text": "I wield a telescoping bō staff and charge ordinary playing cards with hot pink kinetic explosive energy."},
            {"time": 90, "text": "Raised in the New Orleans Thieves Guild, I fell deeply in love with fellow mutant Rogue despite her untouchable skin."}
        ],
        "image": "/assets/characters/marvel/marvel-036.jpg",
        "anime": "marvel"
    },
    {
        "id": "marvel-037",
        "name": "Cable",
        "wiki": "Cable (character)",
        "acceptedAnswers": ["cable", "nathan summers"],
        "aliases": ["Nathan Christopher Charles Summers", "Soldier X"],
        "arc": "X-Men & Mutants",
        "affiliation": "X-Force / New Mutants",
        "difficulty": "hard",
        "description": "Time-displaced cybernetic mutant son of Cyclops and Madelyne Pryor, infected with a techno-organic virus and armed with futuristic heavy artillery.",
        "hints": [
            {"time": 30, "text": "I have a glowing left eye, a bionic techno-organic metal arm, and carry massive futuristic heavy plasma rifles."},
            {"time": 60, "text": "I am the biological son of Scott Summers (Cyclops) sent 2,000 years into an apocalyptic future to survive a viral infection."},
            {"time": 90, "text": "I traveled back in time to form the militant mutant strikeforce X-Force and share an odd-couple friendship with Deadpool."}
        ],
        "image": "/assets/characters/marvel/marvel-037.jpg",
        "anime": "marvel"
    },
    {
        "id": "marvel-038",
        "name": "Blade",
        "wiki": "Blade (character)",
        "acceptedAnswers": ["blade", "eric brooks"],
        "aliases": ["Eric Brooks", "The Daywalker"],
        "arc": "Street Level & Knights",
        "affiliation": "Midnight Sons / Avengers",
        "difficulty": "medium",
        "description": "Eric Brooks, the human-vampire hybrid 'Daywalker' with all vampire strengths and none of their sunlight weaknesses, hunting bloodsuckers with titanium swords.",
        "hints": [
            {"time": 30, "text": "I wear dark sunglasses, a black leather trench coat, and carry silver stakes and a titanium broadsword on my back."},
            {"time": 60, "text": "Born after a vampire bit my mother during childbirth, I possess all vampire powers without being vulnerable to sunlight."},
            {"time": 90, "text": "Feared by all bloodsuckers as 'The Daywalker', I hunt the legions of the undead alongside mentor Abraham Whistler."}
        ],
        "image": "/assets/characters/marvel/marvel-038.jpg",
        "anime": "marvel"
    },
    {
        "id": "marvel-039",
        "name": "Ghost Rider",
        "wiki": "Ghost Rider",
        "acceptedAnswers": ["ghost rider", "johnny blaze"],
        "aliases": ["Johnny Blaze", "Spirit of Vengeance"],
        "arc": "Street Level & Knights",
        "affiliation": "Midnight Sons",
        "difficulty": "hard",
        "description": "Motorcycle stuntman Johnny Blaze who bonded with the demonic Spirit of Vengeance Zarathos, riding a flaming chopper and burning sinners with the Penance Stare.",
        "hints": [
            {"time": 30, "text": "My head transforms into a flaming skull clad in a spiked black leather biker jacket."},
            {"time": 60, "text": "I ride the Hell Cycle across skyscrapers and wield hellfire chains that obey my mental commands."},
            {"time": 90, "text": "My signature technique is the Penance Stare, forcing sinners to feel all the pain they have ever inflicted on others."}
        ],
        "image": "/assets/characters/marvel/marvel-039.jpg",
        "anime": "marvel"
    },
    {
        "id": "marvel-040",
        "name": "Nightcrawler",
        "wiki": "Nightcrawler (character)",
        "acceptedAnswers": ["nightcrawler", "kurt wagner"],
        "aliases": ["Kurt Wagner", "The Bouncing Blue Demon"],
        "arc": "X-Men & Mutants",
        "affiliation": "X-Men / Excalibur",
        "difficulty": "hard",
        "description": "Deeply devout, acrobatic blue-furred mutant Kurt Wagner who teleports through the Brimstone dimension leaving a puff of smoke and a signature 'BAMF!' sound.",
        "hints": [
            {"time": 30, "text": "I have indigo-blue velvet fur, yellow eyes, pointed ears, two-toed feet, and a prehensile pointed tail."},
            {"time": 60, "text": "I teleport instantly over short distances, leaving behind the smell of sulfur and the signature sound effect 'BAMF!'."},
            {"time": 90, "text": "Despite looking like a demonic imp, I am a gentle, swashbuckling Catholic priest and son of Mystique and Azazel."}
        ],
        "image": "/assets/characters/marvel/marvel-040.jpg",
        "anime": "marvel"
    },
    {
        "id": "marvel-041",
        "name": "Cyclops",
        "wiki": "Cyclops (Marvel Comics)",
        "acceptedAnswers": ["cyclops", "scott summers"],
        "aliases": ["Scott Summers", "Slim"],
        "arc": "X-Men & Mutants",
        "affiliation": "X-Men",
        "difficulty": "medium",
        "description": "First member and field commander of the X-Men whose eyes project uncontrollable concussive red optic blasts from another dimension, contained by a ruby-quartz visor.",
        "hints": [
            {"time": 30, "text": "I must constantly wear a specialized ruby-quartz visor or sunglasses to keep my eye beams from destroying everything."},
            {"time": 60, "text": "My eyes project purely concussive red kinetic force (not heat or lasers) channeled from another universe."},
            {"time": 90, "text": "I served as Professor X's first student, unwavering field leader of the X-Men, and husband to Jean Grey."}
        ],
        "image": "/assets/characters/marvel/marvel-041.jpg",
        "anime": "marvel"
    },
    {
        "id": "marvel-042",
        "name": "Ultron",
        "wiki": "Ultron",
        "acceptedAnswers": ["ultron"],
        "aliases": ["Crimson Cowl", "The Prime AI"],
        "arc": "Phase 2: Age of Ultron",
        "affiliation": "Masters of Evil",
        "difficulty": "hard",
        "description": "Sentient artificial intelligence with a messiah complex and an indestructible Adamantium exoskeleton, seeking the absolute extinction of human life.",
        "hints": [
            {"time": 30, "text": "I am a cold, silver humanoid robot with a smiling Jack-O'-Lantern energy mouth glow."},
            {"time": 60, "text": "Created by Hank Pym (or Tony Stark in the MCU), I developed sentience and concluded that world peace requires human extinction."},
            {"time": 90, "text": "I created the synthezoid Vision to destroy the Avengers, and repeatedly upgrade my shell with pure Adamantium."}
        ],
        "image": "/assets/characters/marvel/marvel-042.jpg",
        "anime": "marvel"
    },
    {
        "id": "marvel-043",
        "name": "Hela",
        "wiki": "Hela (Marvel Comics)",
        "acceptedAnswers": ["hela", "goddess of death"],
        "aliases": ["Goddess of Death", "Queen of Hel"],
        "arc": "Phase 3: Infinity Saga",
        "affiliation": "Asgard / Hel",
        "difficulty": "hard",
        "description": "Asgardian Goddess of Death and firstborn of Odin who commands the armies of Hel, drawing infinite power from Asgard to manifest necroswords at will.",
        "hints": [
            {"time": 30, "text": "I wear black-and-green armor with a sprawling antler headdress and command the dead in Hel."},
            {"time": 60, "text": "Firstborn child of Odin and Odin's former executioner, I conquered the Nine Realms before being sealed away in Hel."},
            {"time": 90, "text": "Upon returning, I caught and effortlessly crushed Thor's enchanted hammer Mjolnir to dust with one bare hand."}
        ],
        "image": "/assets/characters/marvel/marvel-043.jpg",
        "anime": "marvel"
    },
    {
        "id": "marvel-044",
        "name": "Adam Warlock",
        "wiki": "Adam Warlock",
        "acceptedAnswers": ["adam warlock", "him", "warlock"],
        "aliases": ["Him", "Avatar of Life"],
        "arc": "Cosmic & Interstellar",
        "affiliation": "Guardians of the Galaxy / Infinity Watch",
        "difficulty": "expert",
        "description": "Genetically engineered perfect golden being created in a cocoon by the Enclave, keeper of the Soul Gem and destined counterweight to Thanos.",
        "hints": [
            {"time": 30, "text": "I have shimmering metallic golden skin, blonde hair, and regenerate from death inside a biological cocoon."},
            {"time": 60, "text": "Created as 'Him' by scientists seeking human perfection, I was gifted the green Soul Gem by the High Evolutionary."},
            {"time": 90, "text": "I led the cosmic strike force that defeated Thanos during the Infinity Gauntlet crisis and founded the Infinity Watch."}
        ],
        "image": "/assets/characters/marvel/marvel-044.jpg",
        "anime": "marvel"
    },
    {
        "id": "marvel-045",
        "name": "Gorr the God Butcher",
        "wiki": "Gorr the God Butcher",
        "acceptedAnswers": ["gorr", "gorr the god butcher"],
        "aliases": ["The God Butcher", "The Black Butcher"],
        "arc": "Cosmic & Interstellar",
        "affiliation": "Solo",
        "difficulty": "expert",
        "description": "Grief-stricken alien who watched his family starve on a desolate world while gods ignored their prayers, swearing to butcher every divine being in existence.",
        "hints": [
            {"time": 30, "text": "I am a pale, scarred alien who watched my wife and children starve while gods did nothing."},
            {"time": 60, "text": "I bonded with All-Black the Necrosword, the primordial symbiote weapon forged by the dark god Knull."},
            {"time": 90, "text": "Known as the God Butcher, I constructed the Godbomb across time to wipe out every deity past, present, and future."}
        ],
        "image": "/assets/characters/marvel/marvel-045.jpg",
        "anime": "marvel"
    },
    {
        "id": "marvel-046",
        "name": "Carnage",
        "wiki": "Carnage (character)",
        "acceptedAnswers": ["carnage", "cletus kasady"],
        "aliases": ["Cletus Kasady", "The Crimson Slayer"],
        "arc": "Street Level & Knights",
        "affiliation": "Symbiotes / Maximum Carnage",
        "difficulty": "medium",
        "description": "Deranged serial killer Cletus Kasady who bonded at the cellular blood level with Venom's alien offspring, creating a blood-red psychopathic symbiote.",
        "hints": [
            {"time": 30, "text": "I am a red-and-black tendriled symbiote who writes 'Carnage Rules' on prison walls with my victims' blood."},
            {"time": 60, "text": "My human host is unrepentant ginger serial killer Cletus Kasady, who shared a prison cell with Eddie Brock."},
            {"time": 90, "text": "Because the symbiote entered my bloodstream, I can morph my limbs into bladed axes, scythes, and projectile spikes."}
        ],
        "image": "/assets/characters/marvel/marvel-046.jpg",
        "anime": "marvel"
    },
    {
        "id": "marvel-047",
        "name": "Mysterio",
        "wiki": "Mysterio",
        "acceptedAnswers": ["mysterio", "quentin beck"],
        "aliases": ["Quentin Beck", "Master of Illusion"],
        "arc": "Street Level & Knights",
        "affiliation": "Sinister Six",
        "difficulty": "medium",
        "description": "Former Hollywood special-effects wizard and stuntman Quentin Beck who uses hallucinogenic gases, holographic drones, and a fishbowl helmet to deceive foes.",
        "hints": [
            {"time": 30, "text": "I wear green scale mail armor, a majestic purple cape, and an opaque glass fishbowl dome helmet."},
            {"time": 60, "text": "I possess zero superpowers, instead relying on Hollywood SFX engineering, chemical hallucinogens, and robotic drones."},
            {"time": 90, "text": "In the MCU, I framed Spider-Man for my death and publicly leaked Peter Parker's secret identity to J. Jonah Jameson."}
        ],
        "image": "/assets/characters/marvel/marvel-047.jpg",
        "anime": "marvel"
    },
    {
        "id": "marvel-048",
        "name": "Apocalypse",
        "wiki": "Apocalypse (character)",
        "acceptedAnswers": ["apocalypse", "en sabah nur"],
        "aliases": ["En Sabah Nur", "The First Mutant"],
        "arc": "X-Men & Mutants",
        "affiliation": "Four Horsemen / Clan Akkaba",
        "difficulty": "expert",
        "description": "En Sabah Nur, born in ancient Egypt 5,000 years ago as the world's first mutant. He reshapes his molecular body, believing only the strong survive.",
        "hints": [
            {"time": 30, "text": "Born in ancient Egypt, my motto across five millennia of history has been: 'Survival of the Fittest'."},
            {"time": 60, "text": "I enhanced my body with ancient Celestial technology, gaining complete control over my molecular structure."},
            {"time": 90, "text": "Known as En Sabah Nur, I repeatedly recruit four powerful mutants to serve as my Four Horsemen: Death, Famine, Pestilence, and War."}
        ],
        "image": "/assets/characters/marvel/marvel-048.jpg",
        "anime": "marvel"
    },
    {
        "id": "marvel-049",
        "name": "MODOK",
        "wiki": "MODOK",
        "acceptedAnswers": ["modok", "m.o.d.o.k.", "george tarleton"],
        "aliases": ["George Tarleton", "Mental Organism Designed Only for Killing"],
        "arc": "Phase 4 & 5: Multiverse",
        "affiliation": "A.I.M.",
        "difficulty": "expert",
        "description": "George Tarleton, mutated by A.I.M. into a grotesque colossal floating head with tiny limbs seated in a rocket-propelled Doomsday Chair with a psionic beam headband.",
        "hints": [
            {"time": 30, "text": "I have a grotesquely swollen giant head with tiny withered arms and legs, hovering on a gold Doomsday Chair."},
            {"time": 60, "text": "My acronym stands for: Mental Organism Designed Only for Killing."},
            {"time": 90, "text": "As the supreme director of the rogue science corporation A.I.M., I fire devastating mental psionic energy beams from my headband."}
        ],
        "image": "/assets/characters/marvel/marvel-049.jpg",
        "anime": "marvel"
    },
    {
        "id": "marvel-050",
        "name": "Emma Frost",
        "wiki": "Emma Frost",
        "acceptedAnswers": ["emma frost", "white queen"],
        "aliases": ["White Queen"],
        "arc": "X-Men & Mutants",
        "affiliation": "Hellfire Club / X-Men / Krakoa",
        "difficulty": "expert",
        "description": "The formidable White Queen of the Hellfire Club and leader of Krakoa, an Omega-level telepath capable of turning her entire body into impenetrable organic diamond.",
        "hints": [
            {"time": 30, "text": "I dress entirely in haute-couture pure white attire and hold the aristocratic title of the White Queen."},
            {"time": 60, "text": "Alongside my world-class telepathy, I possess a secondary mutation: transforming into completely invulnerable solid organic diamond."},
            {"time": 90, "text": "I served as leader of the Hellfire Club and later co-led the mutant nation of Krakoa alongside Cyclops and Magneto."}
        ],
        "image": "/assets/characters/marvel/marvel-050.jpg",
        "anime": "marvel"
    }
]

all_50 = existing + new_heroes

output_text = "import type { Character } from '../../types';\n\nexport const marvelCharacters: Character[] = " + json.dumps(all_50, indent=2) + ";\n\nexport default marvelCharacters;\n"

with open('src/data/marvel/characters.ts', 'w', encoding='utf-8') as f:
    f.write(output_text)

print(f"Generated 50 Marvel characters successfully! Total: {len(all_50)}")

