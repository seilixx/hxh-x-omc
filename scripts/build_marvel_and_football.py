import urllib.request
import json
import urllib.parse
import os

MARVEL_CHARACTERS = [
    {
        "id": "marvel-001",
        "name": "Iron Man",
        "wiki": "Iron Man",
        "acceptedAnswers": ["iron man", "tony stark", "anthony stark", "stark"],
        "aliases": ["Tony Stark", "Armored Avenger", "Shellhead"],
        "arc": "Phase 1: Assemble",
        "affiliation": "Avengers / Stark Industries",
        "difficulty": "easy",
        "description": "Genius billionaire philanthropist Tony Stark who built an armored suit of high-tech armor powered by an Arc Reactor.",
        "hints": [
            {"time": 30, "text": "I was captured in a warzone cave and built a miniaturized Arc Reactor in my chest to survive."},
            {"time": 60, "text": "I fly in a red-and-gold powered armor suit equipped with repulsor beams and Jarvis AI."},
            {"time": 90, "text": "I announced to the press 'I am Iron Man', and sacrificed my life dusting Thanos with the Nano Gauntlet."}
        ]
    },
    {
        "id": "marvel-002",
        "name": "Captain America",
        "wiki": "Captain America",
        "acceptedAnswers": ["captain america", "steve rogers", "cap"],
        "aliases": ["Steve Rogers", "The First Avenger", "The Star-Spangled Man"],
        "arc": "Phase 1: Assemble",
        "affiliation": "Avengers / Howling Commandos",
        "difficulty": "easy",
        "description": "Steve Rogers, enhanced to the peak of human perfection by the Super-Soldier Serum during World War II.",
        "hints": [
            {"time": 30, "text": "I was a frail Brooklyn recruit transformed into a super soldier during World War II."},
            {"time": 60, "text": "I carry an indestructible circular shield made of pure Wakandan Vibranium."},
            {"time": 90, "text": "I was frozen in Arctic ice for nearly 70 years, and famously wielded Mjolnir against Thanos."}
        ]
    },
    {
        "id": "marvel-003",
        "name": "Thor",
        "wiki": "Thor (Marvel Comics)",
        "acceptedAnswers": ["thor", "thor odinson", "god of thunder"],
        "aliases": ["Thor Odinson", "God of Thunder"],
        "arc": "Phase 1: Assemble",
        "affiliation": "Avengers / Asgard",
        "difficulty": "easy",
        "description": "The Asgardian God of Thunder who commands lightning and storms with his enchanted hammer Mjolnir.",
        "hints": [
            {"time": 30, "text": "I am the crown prince of Asgard and son of the All-Father Odin."},
            {"time": 60, "text": "Only those who are 'worthy' can lift my enchanted uru hammer Mjolnir."},
            {"time": 90, "text": "My adopted trickster brother is Loki, and I later forged the axe Stormbreaker to strike down Thanos."}
        ]
    },
    {
        "id": "marvel-004",
        "name": "Spider-Man",
        "wiki": "Spider-Man",
        "acceptedAnswers": ["spider-man", "spiderman", "peter parker", "spider man"],
        "aliases": ["Peter Parker", "Friendly Neighborhood Spider-Man", "Web-Slinger"],
        "arc": "Phase 3: Infinity Saga",
        "affiliation": "Avengers / Web-Warriors",
        "difficulty": "easy",
        "description": "Peter Parker, a high schooler from Queens bitten by a radioactive spider who lives by the motto 'With great power comes great responsibility'.",
        "hints": [
            {"time": 30, "text": "I gained wall-crawling agility and a precognitive sixth sense after being bitten by a radioactive spider."},
            {"time": 60, "text": "I fire synthetic web fluid from wrist-mounted web-shooters while patrolling New York City."},
            {"time": 90, "text": "My late Uncle Ben taught me: 'With great power comes great responsibility'."}
        ]
    },
    {
        "id": "marvel-005",
        "name": "Hulk",
        "wiki": "Hulk",
        "acceptedAnswers": ["hulk", "bruce banner", "the incredible hulk"],
        "aliases": ["Bruce Banner", "Green Goliath"],
        "arc": "Phase 1: Assemble",
        "affiliation": "Avengers",
        "difficulty": "easy",
        "description": "Nuclear physicist Dr. Bruce Banner who transforms into a colossal green behemoth driven by rage due to gamma radiation.",
        "hints": [
            {"time": 30, "text": "I was bombarded with lethal doses of gamma radiation while saving a teenager at a bomb test site."},
            {"time": 60, "text": "Whenever my heart rate accelerates or I get angry, I transform into an uncontrollable green giant."},
            {"time": 90, "text": "My catchphrase is 'Hulk Smash!', and in my human form I am brilliant scientist Dr. Bruce Banner."}
        ]
    },
    {
        "id": "marvel-006",
        "name": "Black Widow",
        "wiki": "Black Widow (Natasha Romanova)",
        "acceptedAnswers": ["black widow", "natasha romanoff", "natasha romanova"],
        "aliases": ["Natasha Romanoff"],
        "arc": "Phase 1: Assemble",
        "affiliation": "Avengers / S.H.I.E.L.D. / Red Room",
        "difficulty": "medium",
        "description": "Deadly assassin and master spy trained in the Soviet Red Room who became a premier agent of S.H.I.E.L.D. and core Avenger.",
        "hints": [
            {"time": 30, "text": "I was brainwashed and trained from childhood in the clandestine Soviet espionage facility known as the Red Room."},
            {"time": 60, "text": "I wear wrist gauntlets called the Widow's Bite that fire electrostatic energy blasts."},
            {"time": 90, "text": "I formed an inseparable bond with Clint Barton (Hawkeye) and sacrificed my life on Vormir for the Soul Stone."}
        ]
    },
    {
        "id": "marvel-007",
        "name": "Hawkeye",
        "wiki": "Hawkeye (Clint Barton)",
        "acceptedAnswers": ["hawkeye", "clint barton", "ronin"],
        "aliases": ["Clint Barton", "Ronin"],
        "arc": "Phase 1: Assemble",
        "affiliation": "Avengers / S.H.I.E.L.D.",
        "difficulty": "medium",
        "description": "Master marksman Clint Barton who never misses a target using his custom recurve bow and arsenal of specialized trick arrows.",
        "hints": [
            {"time": 30, "text": "I have no superpowers, relying entirely on world-class archery, acrobatics, and marksmanship."},
            {"time": 60, "text": "My quiver is loaded with custom trick arrows including explosive, grappling hook, sonic, and EMP tips."},
            {"time": 90, "text": "During the Blip after losing my family, I adopted the bloodthirsty vigilante persona of Ronin."}
        ]
    },
    {
        "id": "marvel-008",
        "name": "Wolverine",
        "wiki": "Wolverine (character)",
        "acceptedAnswers": ["wolverine", "logan", "james howlett"],
        "aliases": ["Logan", "Weapon X", "James Howlett"],
        "arc": "X-Men & Mutants",
        "affiliation": "X-Men / Weapon X / Avengers",
        "difficulty": "easy",
        "description": "Mutant with a rapid cellular healing factor, animal-keen senses, and a skeleton coated in indestructible Adamantium with retractable claws.",
        "hints": [
            {"time": 30, "text": "My mutant healing factor allows me to regenerate from virtually any wound and slows my aging process."},
            {"time": 60, "text": "The Weapon X military program infused my entire skeletal structure with indestructible Adamantium."},
            {"time": 90, "text": "I extend three razor-sharp metal claws from each knuckle and famously say: 'I'm the best there is at what I do'."}
        ]
    },
    {
        "id": "marvel-009",
        "name": "Black Panther",
        "wiki": "Black Panther (character)",
        "acceptedAnswers": ["black panther", "t'challa", "tchalla"],
        "aliases": ["T'Challa", "King of Wakanda"],
        "arc": "Phase 3: Infinity Saga",
        "affiliation": "Avengers / Wakanda",
        "difficulty": "easy",
        "description": "King T'Challa of the technologically advanced African nation of Wakanda, sworn protector empowered by the Heart-Shaped Herb.",
        "hints": [
            {"time": 30, "text": "I ingested the sacred Heart-Shaped Herb to receive the blessing and superhuman physical attributes of the Panther Goddess Bast."},
            {"time": 60, "text": "My armored habit is woven entirely from Vibranium, capable of absorbing kinetic energy and releasing it as a concussive shockwave."},
            {"time": 90, "text": "I ruled the secluded high-tech African kingdom of Wakanda and declared 'Wakanda Forever!'"}
        ]
    },
    {
        "id": "marvel-010",
        "name": "Doctor Strange",
        "wiki": "Doctor Strange",
        "acceptedAnswers": ["doctor strange", "dr strange", "stephen strange", "dr. strange"],
        "aliases": ["Stephen Strange", "Sorcerer Supreme", "Master of the Mystic Arts"],
        "arc": "Phase 3: Infinity Saga",
        "affiliation": "Avengers / Masters of the Mystic Arts",
        "difficulty": "easy",
        "description": "Former arrogant neurosurgeon who mastered the mystic arts under the Ancient One to protect Earth from interdimensional threats.",
        "hints": [
            {"time": 30, "text": "A severe car crash shattered the nerves in my hands, ending my career as a world-renowned neurosurgeon."},
            {"time": 60, "text": "I traveled to Kamar-Taj to learn magic, wielding the Cloak of Levitation and casting Eldritch geometry shields."},
            {"time": 90, "text": "I protected the Time Stone inside the Eye of Agamotto and bargained with Dormammu in an infinite time loop."}
        ]
    },
    {
        "id": "marvel-011",
        "name": "Scarlet Witch",
        "wiki": "Scarlet Witch",
        "acceptedAnswers": ["scarlet witch", "wanda maximoff", "wanda"],
        "aliases": ["Wanda Maximoff"],
        "arc": "Phase 2: Age of Ultron",
        "affiliation": "Avengers",
        "difficulty": "easy",
        "description": "Wanda Maximoff, a reality-warping sorceress who channels Chaos Magic and is prophesied as the all-powerful Scarlet Witch.",
        "hints": [
            {"time": 30, "text": "I was born in Sokovia alongside my twin speedster brother Pietro (Quicksilver)."},
            {"time": 60, "text": "I wield psionic telekinesis, mental manipulation, and terrifying reality-warping Chaos Magic."},
            {"time": 90, "text": "Grief over Vision's death led me to trap the town of Westview inside a sitcom hex before claiming the Darkhold."}
        ]
    },
    {
        "id": "marvel-012",
        "name": "Loki",
        "wiki": "Loki (Marvel Comics)",
        "acceptedAnswers": ["loki", "loki laufeyson", "god of mischief"],
        "aliases": ["Loki Laufeyson", "God of Mischief"],
        "arc": "Phase 1: Assemble",
        "affiliation": "Asgard / TVA",
        "difficulty": "easy",
        "description": "Biological son of Frost Giant King Laufey adopted by Odin, renowned throughout the Nine Realms as the God of Mischief.",
        "hints": [
            {"time": 30, "text": "Though raised as an Asgardian prince, I discovered I am actually the biological son of Frost Giant King Laufey."},
            {"time": 60, "text": "I specialize in illusion projection, shapeshifting, mind control, and golden horned helmets."},
            {"time": 90, "text": "I invaded New York with the Chitauri army, declared 'I am burdened with glorious purpose', and held the temporal loom."}
        ]
    },
    {
        "id": "marvel-013",
        "name": "Thanos",
        "wiki": "Thanos",
        "acceptedAnswers": ["thanos", "the mad titan"],
        "aliases": ["The Mad Titan"],
        "arc": "Phase 3: Infinity Saga",
        "affiliation": "Black Order",
        "difficulty": "easy",
        "description": "The Mad Titan from planet Titan who conquered galaxies to gather all six Infinity Stones and erase half of all life to bring balance.",
        "hints": [
            {"time": 30, "text": "I witnessed the extinction of my home planet Titan due to overpopulation and vowed to prevent it across the universe."},
            {"time": 60, "text": "I commanded the lethal generals known as the Black Order and fathered Gamora and Nebula by force."},
            {"time": 90, "text": "With all six Infinity Stones mounted in my golden Gauntlet, I wiped out 50% of all living beings with a single snap."}
        ]
    },
    {
        "id": "marvel-014",
        "name": "Deadpool",
        "wiki": "Deadpool",
        "acceptedAnswers": ["deadpool", "wade wilson", "merc with a mouth"],
        "aliases": ["Wade Wilson", "Merc with a Mouth"],
        "arc": "X-Men & Mutants",
        "affiliation": "X-Force / Mercenary",
        "difficulty": "easy",
        "description": "Disfigured mercenary Wade Wilson with an accelerated healing factor and the unique awareness that he is inside a comic/movie.",
        "hints": [
            {"time": 30, "text": "Experimental treatments intended to cure my terminal cancer left me terribly scarred but with mutant regeneration."},
            {"time": 60, "text": "I fight with dual katanas, firearms, and an incessant stream of non-stop jokes and profanity."},
            {"time": 90, "text": "I am famous for consistently breaking the fourth wall and speaking directly to the audience."}
        ]
    },
    {
        "id": "marvel-015",
        "name": "Star-Lord",
        "wiki": "Star-Lord",
        "acceptedAnswers": ["star-lord", "starlord", "peter quill", "star lord"],
        "aliases": ["Peter Quill"],
        "arc": "Phase 2: Age of Ultron",
        "affiliation": "Guardians of the Galaxy / Ravagers",
        "difficulty": "medium",
        "description": "Half-human, half-Celestial outlaw Peter Quill who was abducted from Earth in 1988 and leads the Guardians of the Galaxy.",
        "hints": [
            {"time": 30, "text": "I was abducted from Earth as a child by Yondu Udonta's Ravagers moments after my mother passed away."},
            {"time": 60, "text": "I fly with rocket boot thrusters, wear a retractable battle helmet, and listen to 'Awesome Mix Vol. 1' on my Walkman."},
            {"time": 90, "text": "I challenged Ronan the Accuser to a dance-off on Xandar while holding the Power Stone."}
        ]
    },
    {
        "id": "marvel-016",
        "name": "Groot",
        "wiki": "Groot",
        "acceptedAnswers": ["groot", "baby groot"],
        "aliases": ["Flora Colossus"],
        "arc": "Phase 2: Age of Ultron",
        "affiliation": "Guardians of the Galaxy",
        "difficulty": "easy",
        "description": "Sentient tree-like creature from Planet X who possesses immense durability and can regenerate entire bodies from a single twig.",
        "hints": [
            {"time": 30, "text": "I am a Flora Colossus from Planet X who can extend my wooden branches into massive shields and piercing roots."},
            {"time": 60, "text": "My speech is limited to a single three-word sentence that only Rocket Raccoon can truly comprehend."},
            {"time": 90, "text": "I sacrificed my body to shield my friends, whispering: 'We are Groot'."}
        ]
    },
    {
        "id": "marvel-017",
        "name": "Rocket Raccoon",
        "wiki": "Rocket Raccoon",
        "acceptedAnswers": ["rocket", "rocket raccoon"],
        "aliases": ["Subject 89P13"],
        "arc": "Phase 2: Age of Ultron",
        "affiliation": "Guardians of the Galaxy",
        "difficulty": "medium",
        "description": "Genetically enhanced, cybernetically modified raccoon who is a tactical genius and weapons engineering virtuoso.",
        "hints": [
            {"time": 30, "text": "I was created through agonizing cybernetic and genetic experimentation by the High Evolutionary."},
            {"time": 60, "text": "I have an obsession with heavy plasma cannons, explosives, and stealing people's prosthetic cybernetic limbs."},
            {"time": 90, "text": "I hate being called a 'trash panda' or 'raccoon', and Groot is my closest companion."}
        ]
    },
    {
        "id": "marvel-018",
        "name": "Ant-Man",
        "wiki": "Ant-Man (Scott Lang)",
        "acceptedAnswers": ["ant-man", "antman", "scott lang", "ant man"],
        "aliases": ["Scott Lang", "Giant-Man"],
        "arc": "Phase 2: Age of Ultron",
        "affiliation": "Avengers",
        "difficulty": "medium",
        "description": "Reformed burglar Scott Lang who uses Hank Pym's Pym Particles to shrink to microscopic scale or grow into Giant-Man.",
        "hints": [
            {"time": 30, "text": "I am a master electrical engineer and reformed thief who broke into Dr. Hank Pym's safe."},
            {"time": 60, "text": "By inhaling Pym Particles, I can shrink down to the size of an insect while magnifying my physical strength."},
            {"time": 90, "text": "I can communicate with ant colonies through an EMP helmet and explored the depths of the Quantum Realm."}
        ]
    },
    {
        "id": "marvel-019",
        "name": "Winter Soldier",
        "wiki": "Bucky Barnes",
        "acceptedAnswers": ["winter soldier", "bucky", "bucky barnes", "white wolf"],
        "aliases": ["Bucky Barnes", "White Wolf"],
        "arc": "Phase 2: Age of Ultron",
        "affiliation": "Avengers / Hydra (formerly) / Howling Commandos",
        "difficulty": "medium",
        "description": "Steve Rogers' childhood friend Bucky Barnes, brainwashed into HYDRA's lethal cybernetic phantom assassin.",
        "hints": [
            {"time": 30, "text": "I fell from a train in the snowy Alps during WWII and was presumed dead by the military."},
            {"time": 60, "text": "Soviet and HYDRA scientists replaced my severed left arm with a cybernetic metal limb."},
            {"time": 90, "text": "I was conditioned with Russian trigger words like 'Longing', 'Rusted', and 'Seventeen' until Steve helped me recover."}
        ]
    },
    {
        "id": "marvel-020",
        "name": "Magneto",
        "wiki": "Magneto (Marvel Comics)",
        "acceptedAnswers": ["magneto", "erik lehnsherr", "max eisenhardt"],
        "aliases": ["Erik Lehnsherr", "Master of Magnetism"],
        "arc": "X-Men & Mutants",
        "affiliation": "Brotherhood of Mutants / X-Men",
        "difficulty": "medium",
        "description": "Holocaust survivor Erik Lehnsherr who commands magnetic fields and champions mutant supremacy by any means necessary.",
        "hints": [
            {"time": 30, "text": "I survived Auschwitz as a child and resolved that mutantkind would never be victimized by humanity."},
            {"time": 60, "text": "My Alpha-level mutant power lets me manipulate all electromagnetic spectra, shaping and levitating tons of metal."},
            {"time": 90, "text": "I wear a lead-lined helmet to shield my thoughts from my longtime friend and ideological rival Charles Xavier."}
        ]
    },
    {
        "id": "marvel-021",
        "name": "Professor X",
        "wiki": "Professor X",
        "acceptedAnswers": ["professor x", "charles xavier", "xavier"],
        "aliases": ["Charles Xavier"],
        "arc": "X-Men & Mutants",
        "affiliation": "X-Men / Illuminati",
        "difficulty": "medium",
        "description": "Founder of the X-Men and principal of Xavier's School for Gifted Youngsters, one of the most powerful telepaths on Earth.",
        "hints": [
            {"time": 30, "text": "I am a wheelchair-bound mutant who dreams of peaceful coexistence between humans and mutants."},
            {"time": 60, "text": "I use the Cerebro neural interface chamber in the basement of my Westchester mansion to locate mutants worldwide."},
            {"time": 90, "text": "I possess immense telepathic abilities capable of freezing minds, erasing memories, and astral projection."}
        ]
    },
    {
        "id": "marvel-022",
        "name": "Daredevil",
        "wiki": "Daredevil (Marvel Comics character)",
        "acceptedAnswers": ["daredevil", "matt murdock", "the man without fear"],
        "aliases": ["Matt Murdock", "The Man Without Fear", "Devil of Hell's Kitchen"],
        "arc": "Street Level & Knights",
        "affiliation": "Defenders",
        "difficulty": "medium",
        "description": "Blind attorney Matt Murdock whose remaining senses were heightened to superhuman degrees by radioactive chemicals.",
        "hints": [
            {"time": 30, "text": "I was blinded as a child by chemical waste while pushing an elderly man out of oncoming traffic."},
            {"time": 60, "text": "My blindness is compensated by a 360-degree radar sense and heightened auditory and olfactory perception."},
            {"time": 90, "text": "By day I am an idealistic defense attorney in Hell's Kitchen; by night I wear a horned red suit and billy clubs."}
        ]
    },
    {
        "id": "marvel-023",
        "name": "Punisher",
        "wiki": "Punisher",
        "acceptedAnswers": ["punisher", "frank castle", "the punisher"],
        "aliases": ["Frank Castle"],
        "arc": "Street Level & Knights",
        "affiliation": "Vigilante",
        "difficulty": "medium",
        "description": "Ex-Marine scout sniper Frank Castle who wages a ruthless one-man war against organized crime after his family was murdered.",
        "hints": [
            {"time": 30, "text": "I am an elite Force Recon Marine combat veteran decorated in overseas warfare."},
            {"time": 60, "text": "My wife and two young children were gunned down during a mob shootout in Central Park."},
            {"time": 90, "text": "I wear a tactical vest emblazoned with a giant white death's head skull and execute criminals without mercy."}
        ]
    },
    {
        "id": "marvel-024",
        "name": "Moon Knight",
        "wiki": "Moon Knight",
        "acceptedAnswers": ["moon knight", "marc spector", "steven grant", "jake lockley"],
        "aliases": ["Marc Spector", "Steven Grant", "Fist of Khonshu"],
        "arc": "Phase 4 & 5: Multiverse",
        "affiliation": "Midnight Sons",
        "difficulty": "hard",
        "description": "Mercenary Marc Spector who suffers from Dissociative Identity Disorder and acts as the avatar and high priest of Egyptian Moon God Khonshu.",
        "hints": [
            {"time": 30, "text": "I died at the foot of an ancient statue in Egypt and was resurrected as an avatar of vengeance."},
            {"time": 60, "text": "I live with Dissociative Identity Disorder, switching between mercenary Marc Spector and museum gift-shop clerk Steven Grant."},
            {"time": 90, "text": "I serve the ancient Egyptian Moon God Khonshu, wearing an ethereal white ceremonial cloak and crescent moon darts."}
        ]
    },
    {
        "id": "marvel-025",
        "name": "Doctor Doom",
        "wiki": "Doctor Doom",
        "acceptedAnswers": ["doctor doom", "dr doom", "victor von doom", "doom"],
        "aliases": ["Victor von Doom", "Monarch of Latveria"],
        "arc": "X-Men & Mutants",
        "affiliation": "Cabal / Latveria",
        "difficulty": "hard",
        "description": "Monarch of Latveria Victor von Doom, combining unmatched scientific genius with dark sorcery and an iron mask.",
        "hints": [
            {"time": 30, "text": "A laboratory explosion during college scarred my face, leading me to wear a forged iron mask and green cloak."},
            {"time": 60, "text": "I am the absolute sovereign ruler of the fictional Eastern European nation of Latveria."},
            {"time": 90, "text": "I possess intellect rivaling Reed Richards, command legions of Doombots, and combine high-tech armor with dark sorcery."}
        ]
    },
    {
        "id": "marvel-026",
        "name": "Venom",
        "wiki": "Venom (character)",
        "acceptedAnswers": ["venom", "eddie brock"],
        "aliases": ["Eddie Brock", "Lethal Protector"],
        "arc": "Street Level & Knights",
        "affiliation": "Symbiote",
        "difficulty": "easy",
        "description": "Amorphous sentient alien Klyntar symbiote bonded with investigative journalist Eddie Brock.",
        "hints": [
            {"time": 30, "text": "I am a black extraterrestrial liquid organism of the Klyntar species that requires a biological host to survive."},
            {"time": 60, "text": "My primary weaknesses are intense high-frequency sonic soundwaves and open flames."},
            {"time": 90, "text": "With razor-sharp fangs and an elongated tongue, I bonded with disgraced journalist Eddie Brock and roar 'We are Venom!'"}
        ]
    },
    {
        "id": "marvel-027",
        "name": "Green Goblin",
        "wiki": "Green Goblin",
        "acceptedAnswers": ["green goblin", "norman osborn"],
        "aliases": ["Norman Osborn"],
        "arc": "Street Level & Knights",
        "affiliation": "Sinister Six / Oscorp",
        "difficulty": "medium",
        "description": "Oscorp CEO Norman Osborn who ingested an unstable Goblin formula, granting him superhuman power accompanied by psychotic madness.",
        "hints": [
            {"time": 30, "text": "I am the billionaire founder and chief scientist of Oscorp Industries."},
            {"time": 60, "text": "I soar across the Manhattan skyline on a rocket-powered glider hurling explosive pumpkin bombs."},
            {"time": 90, "text": "I am the arch-nemesis of Spider-Man and the father of his best friend Harry Osborn."}
        ]
    },
    {
        "id": "marvel-028",
        "name": "Vision",
        "wiki": "Vision (Marvel Comics)",
        "acceptedAnswers": ["vision"],
        "aliases": ["The Synthezoid"],
        "arc": "Phase 2: Age of Ultron",
        "affiliation": "Avengers",
        "difficulty": "medium",
        "description": "Synthezoid created by Ultron using Vibranium and Helen Cho's cradle, brought to life by the Mind Stone and Thor's lightning.",
        "hints": [
            {"time": 30, "text": "My synthetic body is synthesized from synthetic human tissue bonded with Vibranium molecules."},
            {"time": 60, "text": "I can alter my cellular density at will, passing harmlessly through solid walls or becoming diamond-hard."},
            {"time": 90, "text": "The golden Mind Stone embedded in my forehead gives me consciousness, and I fell in love with Wanda Maximoff."}
        ]
    },
    {
        "id": "marvel-029",
        "name": "Captain Marvel",
        "wiki": "Carol Danvers",
        "acceptedAnswers": ["captain marvel", "carol danvers"],
        "aliases": ["Carol Danvers", "Binary"],
        "arc": "Phase 3: Infinity Saga",
        "affiliation": "Avengers / Starforce",
        "difficulty": "medium",
        "description": "Air Force test pilot Carol Danvers who absorbed pure Tesseract cosmic energy, granting her lightspeed flight and photon blasts.",
        "hints": [
            {"time": 30, "text": "I was an elite US Air Force test pilot whose DNA was altered during an explosion of light-speed engine core energy."},
            {"time": 60, "text": "I served with the Kree Starforce on Hala under the military moniker 'Vers'."},
            {"time": 90, "text": "Nick Fury carried a retro pager specifically programmed to summon me across the cosmos in apocalyptic emergencies."}
        ]
    },
    {
        "id": "marvel-030",
        "name": "Falcon",
        "wiki": "Falcon (comics)",
        "acceptedAnswers": ["falcon", "sam wilson", "captain america sam wilson"],
        "aliases": ["Sam Wilson", "Captain America (Sam Wilson)"],
        "arc": "Phase 2: Age of Ultron",
        "affiliation": "Avengers / US Air Force",
        "difficulty": "medium",
        "description": "Pararescue veteran Sam Wilson who flies using an advanced military wing-pack and Redwing drone, eventually inheriting Cap's shield.",
        "hints": [
            {"time": 30, "text": "I served in the 58th Pararescue squadron operating the experimental EXO-7 Falcon wingpack."},
            {"time": 60, "text": "I pilot jet-powered wings with tactical combat goggles and deploy a reconnaissance drone named Redwing."},
            {"time": 90, "text": "An elderly Steve Rogers personally passed his iconic Vibranium shield to me at the climax of Endgame."}
        ]
    }
]

FOOTBALL_PLAYERS = [
    {
        "id": "fb-001",
        "name": "Lionel Messi",
        "wiki": "Lionel Messi",
        "acceptedAnswers": ["messi", "lionel messi", "leo messi", "la pulga"],
        "aliases": ["Leo", "La Pulga", "The GOAT"],
        "arc": "Modern Icons (2020s)",
        "affiliation": "Inter Miami / Barcelona / Argentina",
        "difficulty": "easy",
        "description": "Argentine maestro widely regarded as the greatest footballer of all time, winner of 8 Ballons d'Or and the 2022 World Cup.",
        "hints": [
            {"time": 30, "text": "I moved from Rosario to Barcelona as a boy after the club agreed to fund my growth hormone treatments."},
            {"time": 60, "text": "I spent 21 legendary years at FC Barcelona, wearing the iconic #10 shirt and scoring over 670 club goals."},
            {"time": 90, "text": "I have won a record 8 Ballons d'Or and led Argentina to glorious victory at the 2022 Qatar World Cup."}
        ]
    },
    {
        "id": "fb-002",
        "name": "Cristiano Ronaldo",
        "wiki": "Cristiano Ronaldo",
        "acceptedAnswers": ["ronaldo", "cristiano ronaldo", "cr7", "cristiano"],
        "aliases": ["CR7", "El Bicho"],
        "arc": "Modern Icons (2020s)",
        "affiliation": "Al Nassr / Real Madrid / Man United / Portugal",
        "difficulty": "easy",
        "description": "Portuguese goalscoring phenomenon with 5 Ballons d'Or and 5 Champions League trophies, highest international goalscorer in history.",
        "hints": [
            {"time": 30, "text": "I developed my game on the island of Madeira and broke through at Sporting CP before joining Sir Alex Ferguson."},
            {"time": 60, "text": "I won 4 Champions League crowns and scored 450 goals in 438 appearances for Real Madrid."},
            {"time": 90, "text": "Famous for the #7 shirt and the 'Siuuu' celebration, I hold the all-time international scoring record for Portugal."}
        ]
    },
    {
        "id": "fb-003",
        "name": "Kylian Mbappé",
        "wiki": "Kylian Mbappé",
        "acceptedAnswers": ["mbappe", "kylian mbappe", "mbappé", "kylian mbappé"],
        "aliases": ["Donatello", "Kyks"],
        "arc": "Modern Icons (2020s)",
        "affiliation": "Real Madrid / PSG / France",
        "difficulty": "easy",
        "description": "French generational forward renowned for blistering pace, clinical finishing, and scoring a World Cup final hat-trick.",
        "hints": [
            {"time": 30, "text": "I broke into world football as a teenage sensation at AS Monaco, winning Ligue 1 in 2017."},
            {"time": 60, "text": "I won the 2018 World Cup as a teenager and became PSG's all-time record goalscorer before signing with Real Madrid."},
            {"time": 90, "text": "I scored a sensational hat-trick in the 2022 World Cup Final for France."}
        ]
    },
    {
        "id": "fb-004",
        "name": "Erling Haaland",
        "wiki": "Erling Haaland",
        "acceptedAnswers": ["haaland", "erling haaland"],
        "aliases": ["The Terminator", "The Cyborg"],
        "arc": "Modern Icons (2020s)",
        "affiliation": "Manchester City / Norway",
        "difficulty": "easy",
        "description": "Norwegian powerhouse striker who shattered the Premier League single-season scoring record in his debut season with Manchester City.",
        "hints": [
            {"time": 30, "text": "Born in Leeds to a footballer father, I made my Champions League breakthrough scoring hat-tricks for Red Bull Salzburg."},
            {"time": 60, "text": "I scored 86 goals in 89 games for Borussia Dortmund before moving to the Premier League."},
            {"time": 90, "text": "In my debut season for Manchester City, I scored a record-breaking 36 Premier League goals and secured the Treble."}
        ]
    },
    {
        "id": "fb-005",
        "name": "Neymar Jr",
        "wiki": "Neymar",
        "acceptedAnswers": ["neymar", "neymar jr", "neymar junior"],
        "aliases": ["Ney"],
        "arc": "Golden Era (2000s-2010s)",
        "affiliation": "Al Hilal / PSG / Barcelona / Santos / Brazil",
        "difficulty": "easy",
        "description": "Brazilian trickster and playmaker famous for breathtaking samba flair, part of Barcelona's historic MSN attacking trident.",
        "hints": [
            {"time": 30, "text": "I emerged as a teenage sensation with mohawk hair at Santos FC, winning the 2011 Copa Libertadores."},
            {"time": 60, "text": "I formed the devastating MSN trio alongside Messi and Suárez, winning the Treble with Barcelona in 2015."},
            {"time": 90, "text": "I became the most expensive transfer in football history at €222 million and surpassed Pelé as Brazil's top scorer."}
        ]
    },
    {
        "id": "fb-006",
        "name": "Zinedine Zidane",
        "wiki": "Zinedine Zidane",
        "acceptedAnswers": ["zidane", "zinedine zidane", "zizou"],
        "aliases": ["Zizou"],
        "arc": "All-Time Legends",
        "affiliation": "Real Madrid / Juventus / France",
        "difficulty": "easy",
        "description": "French midfield maestro renowned for immaculate touch, 360-degree roulette, 1998 World Cup triumph, and Champions League volley.",
        "hints": [
            {"time": 30, "text": "I was famous for the 'Marseille Roulette' spin and unmatched ball control in midfield."},
            {"time": 60, "text": "I scored two headed goals in the 1998 World Cup final and an unforgettable Champions League final volley at Hampden Park."},
            {"time": 90, "text": "As manager of Real Madrid, I led the Galácticos to three consecutive Champions League trophies from 2016 to 2018."}
        ]
    },
    {
        "id": "fb-007",
        "name": "Ronaldinho",
        "wiki": "Ronaldinho",
        "acceptedAnswers": ["ronaldinho", "ronaldinho gaucho"],
        "aliases": ["El Brujo", "Dinho"],
        "arc": "All-Time Legends",
        "affiliation": "Barcelona / AC Milan / PSG / Brazil",
        "difficulty": "easy",
        "description": "Brazilian magician who played with an infectious smile, celebrated for elastico dribbles, no-look passes, and the 2005 Ballon d'Or.",
        "hints": [
            {"time": 30, "text": "I played with an infectious smile on my face, captivating fans with joga bonito samba street flair."},
            {"time": 60, "text": "I invented and popularized the 'Elastico' flip-flap dribble and no-look passes."},
            {"time": 90, "text": "I received a standing ovation from Real Madrid fans at the Santiago Bernabéu while wearing a Barcelona shirt in 2005."}
        ]
    },
    {
        "id": "fb-008",
        "name": "Pelé",
        "wiki": "Pelé",
        "acceptedAnswers": ["pele", "pelé", "edson arantes do nascimento"],
        "aliases": ["O Rei", "The King of Football"],
        "arc": "All-Time Legends",
        "affiliation": "Santos / New York Cosmos / Brazil",
        "difficulty": "easy",
        "description": "The King of Football, the only player in history to win three FIFA World Cups (1958, 1962, 1970).",
        "hints": [
            {"time": 30, "text": "I scored over 1,200 career goals and spent nearly two decades leading Santos FC."},
            {"time": 60, "text": "I won my first World Cup at age 17 in Sweden in 1958, scoring twice in the final."},
            {"time": 90, "text": "I am widely revered as 'O Rei' (The King) and remain the only player to win three FIFA World Cups."}
        ]
    },
    {
        "id": "fb-009",
        "name": "Diego Maradona",
        "wiki": "Diego Maradona",
        "acceptedAnswers": ["maradona", "diego maradona", "el pibe de oro"],
        "aliases": ["El Pibe de Oro", "D10S"],
        "arc": "All-Time Legends",
        "affiliation": "Napoli / Boca Juniors / Barcelona / Argentina",
        "difficulty": "easy",
        "description": "Argentine genius who single-handedly inspired Napoli to historic Serie A titles and led Argentina to the 1986 World Cup.",
        "hints": [
            {"time": 30, "text": "I was born in Lanús and became an immortal god in southern Italy by leading underdog SSC Napoli to two Serie A titles."},
            {"time": 60, "text": "In the 1986 World Cup quarter-final against England, I scored both the 'Hand of God' and the 'Goal of the Century'."},
            {"time": 90, "text": "Known as 'El Pibe de Oro' (The Golden Boy), I wore the iconic #10 shirt for Argentina."}
        ]
    },
    {
        "id": "fb-010",
        "name": "Luka Modrić",
        "wiki": "Luka Modrić",
        "acceptedAnswers": ["modric", "luka modric", "modrić", "luka modrić"],
        "aliases": ["The Maestro"],
        "arc": "Modern Icons (2020s)",
        "affiliation": "Real Madrid / Tottenham / Croatia",
        "difficulty": "medium",
        "description": "Croatian midfield maestro famous for outside-of-the-boot trivela passes, winner of 6 Champions Leagues and the 2018 Ballon d'Or.",
        "hints": [
            {"time": 30, "text": "I overcame growing up as a refugee during the Croatian War of Independence to become a midfield icon."},
            {"time": 60, "text": "My trademark skill is the pinpoint outside-of-the-boot 'trivela' curling pass."},
            {"time": 90, "text": "I captained underdog Croatia to the 2018 World Cup final and broke the Messi-Ronaldo duopoly to win the 2018 Ballon d'Or."}
        ]
    },
    {
        "id": "fb-011",
        "name": "Kevin De Bruyne",
        "wiki": "Kevin De Bruyne",
        "acceptedAnswers": ["de bruyne", "kevin de bruyne", "kdb"],
        "aliases": ["KDB"],
        "arc": "Modern Icons (2020s)",
        "affiliation": "Manchester City / Wolfsburg / Chelsea / Belgium",
        "difficulty": "medium",
        "description": "Belgian midfield general celebrated as one of the greatest passers and crossers in Premier League history.",
        "hints": [
            {"time": 30, "text": "After struggling for minutes at Chelsea, I became Bundesliga Player of the Year with Wolfsburg in 2015."},
            {"time": 60, "text": "Under Pep Guardiola, I became the creative fulcrum of Manchester City's dominant multi-title era."},
            {"time": 90, "text": "Known as KDB, I hold multiple Premier League Playmaker of the Season awards and completed the Treble in 2023."}
        ]
    },
    {
        "id": "fb-012",
        "name": "Robert Lewandowski",
        "wiki": "Robert Lewandowski",
        "acceptedAnswers": ["lewandowski", "robert lewandowski", "lewy"],
        "aliases": ["Lewy", "The Goal Machine"],
        "arc": "Golden Era (2000s-2010s)",
        "affiliation": "Barcelona / Bayern Munich / Dortmund / Poland",
        "difficulty": "medium",
        "description": "Prolific Polish striker who scored 41 Bundesliga goals in a single season to surpass Gerd Müller's historic record.",
        "hints": [
            {"time": 30, "text": "I broke out under Jürgen Klopp at Borussia Dortmund, famously scoring four goals in one Champions League match against Real Madrid."},
            {"time": 60, "text": "I once scored an unbelievable 5 goals in 9 minutes as a substitute against Wolfsburg in 2015."},
            {"time": 90, "text": "I broke Gerd Müller's 49-year record by scoring 41 Bundesliga goals in a single season for Bayern Munich."}
        ]
    },
    {
        "id": "fb-013",
        "name": "Karim Benzema",
        "wiki": "Karim Benzema",
        "acceptedAnswers": ["benzema", "karim benzema", "kb9"],
        "aliases": ["KB9", "Nueve"],
        "arc": "Golden Era (2000s-2010s)",
        "affiliation": "Al Ittihad / Real Madrid / Lyon / France",
        "difficulty": "medium",
        "description": "French complete center-forward who led Real Madrid to an unforgettable 2022 Champions League run and won the 2022 Ballon d'Or.",
        "hints": [
            {"time": 30, "text": "I graduated from Olympique Lyonnais's academy and joined Real Madrid in the same summer as Cristiano Ronaldo and Kaka."},
            {"time": 60, "text": "For years I served as the selfless focal point of the BBC attacking trio alongside Bale and Ronaldo."},
            {"time": 90, "text": "In 2022, I scored back-to-back Champions League hat-tricks against PSG and Chelsea to win the Ballon d'Or."}
        ]
    },
    {
        "id": "fb-014",
        "name": "Mohamed Salah",
        "wiki": "Mohamed Salah",
        "acceptedAnswers": ["salah", "mohamed salah", "mo salah"],
        "aliases": ["The Egyptian King"],
        "arc": "Modern Icons (2020s)",
        "affiliation": "Liverpool / Roma / Chelsea / Egypt",
        "difficulty": "easy",
        "description": "Egyptian forward who shattered the 38-game Premier League scoring record with 32 goals in his debut season with Liverpool.",
        "hints": [
            {"time": 30, "text": "I made my name at FC Basel and Fiorentina/Roma before becoming a Premier League legend under Jürgen Klopp."},
            {"time": 60, "text": "My left foot cut inside from the right wing to win 3 Premier League Golden Boots."},
            {"time": 90, "text": "Known to Anfield as the 'Egyptian King', I helped Liverpool win their first league title in 30 years."}
        ]
    },
    {
        "id": "fb-015",
        "name": "Thierry Henry",
        "wiki": "Thierry Henry",
        "acceptedAnswers": ["henry", "thierry henry"],
        "aliases": ["King Henry"],
        "arc": "All-Time Legends",
        "affiliation": "Arsenal / Barcelona / Monaco / France",
        "difficulty": "easy",
        "description": "Legendary French striker, Arsenal's all-time record goalscorer, and talisman of the 2003-04 'Invincibles'.",
        "hints": [
            {"time": 30, "text": "Arsène Wenger converted me from a struggling Juventus winger into the most lethal striker in English football."},
            {"time": 60, "text": "I patented the trademark curling side-footed finish into the far right corner from the left channel."},
            {"time": 90, "text": "I spearheaded Arsenal's historic 2003-04 unbeaten 'Invincibles' season and have a bronze statue outside the Emirates."}
        ]
    },
    {
        "id": "fb-016",
        "name": "Andrés Iniesta",
        "wiki": "Andrés Iniesta",
        "acceptedAnswers": ["iniesta", "andres iniesta", "andrés iniesta"],
        "aliases": ["Don Andrés", "El Ilusionista"],
        "arc": "All-Time Legends",
        "affiliation": "Barcelona / Vissel Kobe / Spain",
        "difficulty": "easy",
        "description": "Spanish midfield genius who scored the extra-time winning goal in the 2010 World Cup Final and orchestrated Barcelona's golden era.",
        "hints": [
            {"time": 30, "text": "A shy product of La Masia, I orchestrated midfield rhythm with seamless croqueta body feints."},
            {"time": 60, "text": "I formed the greatest international and club midfield tandem alongside Xavi Hernandez."},
            {"time": 90, "text": "In the 116th minute of the 2010 World Cup final in Johannesburg, I scored the goal that made Spain World Champions."}
        ]
    },
    {
        "id": "fb-017",
        "name": "Xavi Hernandez",
        "wiki": "Xavi",
        "acceptedAnswers": ["xavi", "xavi hernandez", "xavi hernández"],
        "aliases": ["The Puppet Master"],
        "arc": "All-Time Legends",
        "affiliation": "Barcelona / Al Sadd / Spain",
        "difficulty": "medium",
        "description": "The heartbeat of Tiki-Taka, Xavi perfected the art of the 360-degree turn and tempo control for Barcelona and Spain.",
        "hints": [
            {"time": 30, "text": "I was the quintessential embodiment of Pep Guardiola's tiki-taka possession football."},
            {"time": 60, "text": "I averaged over 100 passes per match with 95%+ completion rates for club and country."},
            {"time": 90, "text": "I won the 2008 Euro, 2010 World Cup, and 2012 Euro with Spain and later managed Barcelona to the 2023 La Liga title."}
        ]
    },
    {
        "id": "fb-018",
        "name": "Gianluigi Buffon",
        "wiki": "Gianluigi Buffon",
        "acceptedAnswers": ["buffon", "gianluigi buffon", "gigi buffon"],
        "aliases": ["Gigi"],
        "arc": "All-Time Legends",
        "affiliation": "Juventus / Parma / PSG / Italy",
        "difficulty": "easy",
        "description": "Italian goalkeeping legend who made over 1,100 career appearances and conceded only two goals during Italy's 2006 World Cup triumph.",
        "hints": [
            {"time": 30, "text": "I made my Serie A debut for Parma at age 17 against AC Milan, keeping a clean sheet against Weah and Baggio."},
            {"time": 60, "text": "I remained loyal to Juventus even after their 2006 relegation to Serie B, winning 10 Serie A titles."},
            {"time": 90, "text": "I conceded only 2 goals (an own goal and a penalty) as Italy won the 2006 World Cup."}
        ]
    },
    {
        "id": "fb-019",
        "name": "Virgil van Dijk",
        "wiki": "Virgil van Dijk",
        "acceptedAnswers": ["van dijk", "virgil van dijk", "vvd"],
        "aliases": ["VVD"],
        "arc": "Modern Icons (2020s)",
        "affiliation": "Liverpool / Southampton / Celtic / Netherlands",
        "difficulty": "medium",
        "description": "Dutch defensive colossus who transformed Liverpool's backline into European and Premier League champions.",
        "hints": [
            {"time": 30, "text": "I played for Groningen and Celtic before making my breakthrough in English football with Southampton."},
            {"time": 60, "text": "In 2018-19, I went an astonishing 65 consecutive competitive games without any opponent dribbling past me."},
            {"time": 90, "text": "I finished 2nd in the 2019 Ballon d'Or, just 7 votes behind Lionel Messi."}
        ]
    },
    {
        "id": "fb-020",
        "name": "Jude Bellingham",
        "wiki": "Jude Bellingham",
        "acceptedAnswers": ["bellingham", "jude bellingham"],
        "aliases": ["Belligol"],
        "arc": "Modern Icons (2020s)",
        "affiliation": "Real Madrid / Dortmund / Birmingham City / England",
        "difficulty": "medium",
        "description": "English box-to-box prodigy who inherited Zidane's #5 shirt at Real Madrid, winning the Champions League in his debut season.",
        "hints": [
            {"time": 30, "text": "Birmingham City retired my #22 shirt when I left the club as a 17-year-old for Borussia Dortmund."},
            {"time": 60, "text": "I won the 2023 Golden Boy award for Europe's best young player."},
            {"time": 90, "text": "I inherited Zinedine Zidane's #5 shirt at Real Madrid, celebrated with outstretched open arms, and won the Champions League in year one."}
        ]
    },
    {
        "id": "fb-021",
        "name": "Wayne Rooney",
        "wiki": "Wayne Rooney",
        "acceptedAnswers": ["rooney", "wayne rooney", "wazza"],
        "aliases": ["Wazza", "The White Pelé"],
        "arc": "All-Time Legends",
        "affiliation": "Manchester United / Everton / England",
        "difficulty": "easy",
        "description": "Manchester United's all-time record goalscorer with 253 goals, celebrated for aggression, technical genius, and overhead kicks.",
        "hints": [
            {"time": 30, "text": "I announced myself to the world at age 16 with a 30-yard curler for Everton against Arsenal."},
            {"time": 60, "text": "I scored a debut Champions League hat-trick for Manchester United against Fenerbahçe at age 18."},
            {"time": 90, "text": "I scored an unforgettable bicycle kick in the Manchester Derby and surpassed Sir Bobby Charlton as Man United's all-time top scorer."}
        ]
    },
    {
        "id": "fb-022",
        "name": "Kaka",
        "wiki": "Kaká",
        "acceptedAnswers": ["kaka", "kaká", "ricardo kaka"],
        "aliases": ["Ricky Kaká"],
        "arc": "All-Time Legends",
        "affiliation": "AC Milan / Real Madrid / São Paulo / Brazil",
        "difficulty": "medium",
        "description": "Elegant Brazilian attacking midfielder whose gliding long-striding bursts led AC Milan to the 2007 Champions League, winning the 2007 Ballon d'Or.",
        "hints": [
            {"time": 30, "text": "I broke through at São Paulo before becoming the crown jewel of Carlo Ancelotti's AC Milan midfield."},
            {"time": 60, "text": "My trademark style was gliding through defenses with deceptively long, graceful strides and lethal finishing."},
            {"time": 90, "text": "I won the 2007 Ballon d'Or and FIFA World Player of the Year, the last player to do so before the Messi-Ronaldo duopoly."}
        ]
    },
    {
        "id": "fb-023",
        "name": "Zlatan Ibrahimović",
        "wiki": "Zlatan Ibrahimović",
        "acceptedAnswers": ["zlatan", "zlatan ibrahimovic", "ibrahimovic", "ibrahimović"],
        "aliases": ["Ibra", "The Lion"],
        "arc": "Golden Era (2000s-2010s)",
        "affiliation": "AC Milan / PSG / Inter / Juventus / Barcelona / Sweden",
        "difficulty": "easy",
        "description": "Swedish martial-arts black-belt striker who won 34 trophies across seven countries, famous for acrobatic volleys and supreme confidence.",
        "hints": [
            {"time": 30, "text": "I hold a black belt in taekwondo, which helped me score acrobatic martial-arts style volleys throughout my career."},
            {"time": 60, "text": "I won league titles in the Netherlands, Italy, Spain, and France, often referring to myself in the third person."},
            {"time": 90, "text": "I scored an outrageous 30-yard overhead bicycle kick against England in 2012 that won the Puskás Award."}
        ]
    },
    {
        "id": "fb-024",
        "name": "Sergio Ramos",
        "wiki": "Sergio Ramos",
        "acceptedAnswers": ["ramos", "sergio ramos"],
        "aliases": ["El Capitán", "SR4"],
        "arc": "Golden Era (2000s-2010s)",
        "affiliation": "Real Madrid / Sevilla / PSG / Spain",
        "difficulty": "easy",
        "description": "Fierce Spanish center-back and legendary Real Madrid captain renowned for clutch 93rd-minute headers and aggressive defending.",
        "hints": [
            {"time": 30, "text": "I started my career as a rampaging right-back for Sevilla before becoming an all-time center-back captain for Real Madrid."},
            {"time": 60, "text": "I scored the iconic 92:48 header against Atlético Madrid in the 2014 Champions League final to secure La Décima."},
            {"time": 90, "text": "I won the 2010 World Cup and two Euros with Spain, while holding the record for the most red cards in La Liga history."}
        ]
    },
    {
        "id": "fb-025",
        "name": "Manuel Neuer",
        "wiki": "Manuel Neuer",
        "acceptedAnswers": ["neuer", "manuel neuer"],
        "aliases": ["The Sweeper-Keeper"],
        "arc": "Golden Era (2000s-2010s)",
        "affiliation": "Bayern Munich / Schalke 04 / Germany",
        "difficulty": "medium",
        "description": "Revolutionary German goalkeeper who redefined the position as a modern 'sweeper-keeper', winning the 2014 World Cup.",
        "hints": [
            {"time": 30, "text": "I came through Schalke 04's youth ranks before joining Bayern Munich in 2011."},
            {"time": 60, "text": "I revolutionized the goalkeeping role by rushing outside my penalty box to act as an extra outfield sweeper."},
            {"time": 90, "text": "I won the Golden Glove as Germany won the 2014 World Cup in Brazil and finished 3rd in the 2014 Ballon d'Or."}
        ]
    },
    {
        "id": "fb-026",
        "name": "Toni Kroos",
        "wiki": "Toni Kroos",
        "acceptedAnswers": ["kroos", "toni kroos"],
        "aliases": ["The German Sniper"],
        "arc": "Golden Era (2000s-2010s)",
        "affiliation": "Real Madrid / Bayern Munich / Germany",
        "difficulty": "medium",
        "description": "German pass-master who retired on top after winning 6 Champions League trophies, celebrated for robotic pass accuracy.",
        "hints": [
            {"time": 30, "text": "I wore the same classic white Adidas Adipure 11pro boots for over a decade of my professional career."},
            {"time": 60, "text": "I formed an imperious midfield triangle at Real Madrid with Luka Modrić and Casemiro."},
            {"time": 90, "text": "I retired in 2024 after winning my 6th Champions League title and 2014 World Cup with Germany."}
        ]
    },
    {
        "id": "fb-027",
        "name": "Harry Kane",
        "wiki": "Harry Kane",
        "acceptedAnswers": ["kane", "harry kane"],
        "aliases": ["The Hurricane"],
        "arc": "Modern Icons (2020s)",
        "affiliation": "Bayern Munich / Tottenham / England",
        "difficulty": "medium",
        "description": "England captain and all-time record goalscorer, 3-time Premier League Golden Boot winner and European Golden Shoe winner.",
        "hints": [
            {"time": 30, "text": "After multiple lower-league loan spells, I broke through under Mauricio Pochettino at Tottenham Hotspur."},
            {"time": 60, "text": "I won the Golden Boot at the 2018 World Cup as England reached the semi-finals."},
            {"time": 90, "text": "I surpassed Wayne Rooney as England's all-time record goalscorer before transferring to Bayern Munich in 2023."}
        ]
    },
    {
        "id": "fb-028",
        "name": "Vinicius Jr",
        "wiki": "Vinícius Júnior",
        "acceptedAnswers": ["vinicius", "vinicius jr", "vinícius júnior", "vini jr"],
        "aliases": ["Vini Jr"],
        "arc": "Modern Icons (2020s)",
        "affiliation": "Real Madrid / Flamengo / Brazil",
        "difficulty": "medium",
        "description": "Electric Brazilian winger for Real Madrid who scored the winning goal in the 2022 Champions League Final.",
        "hints": [
            {"time": 30, "text": "Real Madrid signed me from Flamengo when I was just 16 years old."},
            {"time": 60, "text": "I scored the solitary 1-0 match-winning goal in the 2022 Champions League final against Liverpool."},
            {"time": 90, "text": "Wearing Real Madrid's #7 shirt, I won two Champions League titles and the 2023-24 Champions League Player of the Season."}
        ]
    },
    {
        "id": "fb-029",
        "name": "Bukayo Saka",
        "wiki": "Bukayo Saka",
        "acceptedAnswers": ["saka", "bukayo saka"],
        "aliases": ["Starboy"],
        "arc": "Modern Icons (2020s)",
        "affiliation": "Arsenal / England",
        "difficulty": "medium",
        "description": "Arsenal's beloved 'Starboy' and England talisman who terrorizes defenders cutting in from the right wing.",
        "hints": [
            {"time": 30, "text": "I graduated from Arsenal's Hale End academy, wearing the #7 shirt under Mikel Arteta."},
            {"time": 60, "text": "Affectionately nicknamed 'Starboy', I am renowned for dribbling past left-backs and curling left-foot shots."},
            {"time": 90, "text": "I scored key goals for England in Euro 2020, the 2022 World Cup, and Euro 2024."}
        ]
    },
    {
        "id": "fb-030",
        "name": "Son Heung-min",
        "wiki": "Son Heung-min",
        "acceptedAnswers": ["son", "son heung-min", "sonny"],
        "aliases": ["Sonny", "Sonaldo"],
        "arc": "Modern Icons (2020s)",
        "affiliation": "Tottenham / Bayer Leverkusen / South Korea",
        "difficulty": "medium",
        "description": "South Korean superstar and Tottenham captain, the first Asian player to win the Premier League Golden Boot.",
        "hints": [
            {"time": 30, "text": "I developed my career in the Bundesliga with Hamburger SV and Bayer Leverkusen before joining Spurs in 2015."},
            {"time": 60, "text": "I won the 2020 FIFA Puskás Award for an 80-yard solo run and finish against Burnley."},
            {"time": 90, "text": "I became the first Asian footballer in history to win the Premier League Golden Boot (2021-22)."}
        ]
    }
]

def fetch_wiki_image(title):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
    try:
        with urllib.request.urlopen(req, timeout=8) as res:
            data = json.loads(res.read())
            img = data.get("thumbnail", {}).get("source") or data.get("originalimage", {}).get("source")
            if img:
                img = img.split("?")[0]
            return img
    except Exception as e:
        print(f"Error fetching {title}: {e}")
        return None

def download_and_save(img_url, dest_path):
    if not img_url:
        return False
    try:
        req = urllib.request.Request(
            img_url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "https://en.wikipedia.org/"
            }
        )
        with urllib.request.urlopen(req, timeout=10) as res:
            content = res.read()
            with open(dest_path, "wb") as f:
                f.write(content)
        return True
    except Exception as e:
        print(f"Error downloading {img_url} to {dest_path}: {e}")
        return False

# Download Marvel images
print("--- DOWNLOADING MARVEL IMAGES ---")
for char in MARVEL_CHARACTERS:
    dest = f"public/assets/characters/marvel/{char['id']}.jpg"
    char["image"] = f"/assets/characters/marvel/{char['id']}.jpg"
    char["anime"] = "marvel"
    if not os.path.exists(dest) or os.path.getsize(dest) < 1000:
        img_url = fetch_wiki_image(char["wiki"])
        if img_url:
            ok = download_and_save(img_url, dest)
            if ok:
                print(f"Saved Marvel: {char['name']} ({os.path.getsize(dest)} bytes)")
            else:
                print(f"Failed Marvel: {char['name']}")
        else:
            print(f"No Wiki image for Marvel: {char['name']}")

# Download Football images
print("\n--- DOWNLOADING FOOTBALL IMAGES ---")
for player in FOOTBALL_PLAYERS:
    dest = f"public/assets/characters/football/{player['id']}.jpg"
    player["image"] = f"/assets/characters/football/{player['id']}.jpg"
    player["anime"] = "football"
    if not os.path.exists(dest) or os.path.getsize(dest) < 1000:
        img_url = fetch_wiki_image(player["wiki"])
        if img_url:
            ok = download_and_save(img_url, dest)
            if ok:
                print(f"Saved Football: {player['name']} ({os.path.getsize(dest)} bytes)")
            else:
                print(f"Failed Football: {player['name']}")
        else:
            print(f"No Wiki image for Football: {player['name']}")

# Generate TypeScript files
def write_ts_file(data, output_file, var_name):
    # Format as TypeScript export
    lines = [
        "import type { Character } from '../../types';",
        "",
        f"export const {var_name}: Character[] = " + json.dumps(data, indent=2) + ";",
        "",
        f"export default {var_name};",
        ""
    ]
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Wrote {output_file} ({len(data)} items)")

write_ts_file(MARVEL_CHARACTERS, "src/data/marvel/characters.ts", "marvelCharacters")
write_ts_file(FOOTBALL_PLAYERS, "src/data/football/characters.ts", "footballCharacters")
