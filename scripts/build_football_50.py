import json

with open('src/data/football/characters.ts', 'r', encoding='utf-8') as f:
    text = f.read()

prefix = 'export const footballCharacters: Character[] = '
start = text.find(prefix) + len(prefix)
end = text.find('];', start) + 1
existing = json.loads(text[start:end])

# Rebalance some existing difficulties so hard exists in first 30 too
for p in existing:
    if p['id'] in ['fb-026']: # Kroos
        p['difficulty'] = 'hard'
    elif p['id'] in ['fb-008', 'fb-009']: # Pele, Maradona
        p['difficulty'] = 'easy'
    elif p['id'] in ['fb-011', 'fb-012', 'fb-013', 'fb-014', 'fb-015', 'fb-016', 'fb-017', 'fb-018', 'fb-019', 'fb-020', 'fb-021', 'fb-022', 'fb-023', 'fb-024', 'fb-025', 'fb-027', 'fb-028', 'fb-029', 'fb-030']:
        p['difficulty'] = 'medium'

new_players = [
    {
        "id": "fb-031",
        "name": "Lev Yashin",
        "wiki": "Lev Yashin",
        "acceptedAnswers": ["yashin", "lev yashin", "the black spider"],
        "aliases": ["The Black Spider", "The Black Panther"],
        "arc": "Vintage Legends (Pre-1980s)",
        "affiliation": "Dynamo Moscow / Soviet Union",
        "difficulty": "expert",
        "nationality": "Soviet Union",
        "description": "The only goalkeeper in football history to win the Ballon d'Or (1963), revolutionizing goalkeeping with athletic reflexes and commanding the penalty area.",
        "hints": [
            {"time": 30, "text": "I was universally known as 'The Black Spider' due to my all-black attire and seemingly eight-armed shot-stopping reach."},
            {"time": 60, "text": "I saved over 150 penalty kicks and kept over 270 clean sheets throughout my historic career with Dynamo Moscow and the USSR."},
            {"time": 90, "text": "I remain the one and only goalkeeper to ever win the prestigious Ballon d'Or, awarded to me in 1963."}
        ],
        "image": "/assets/characters/football/fb-031.jpg",
        "anime": "football"
    },
    {
        "id": "fb-032",
        "name": "Ferenc Puskas",
        "wiki": "Ferenc Puskás",
        "acceptedAnswers": ["puskas", "ferenc puskas", "puskás", "ferenc puskás"],
        "aliases": ["The Galloping Major", "Pancho"],
        "arc": "Vintage Legends (Pre-1980s)",
        "affiliation": "Real Madrid / Budapest Honvéd / Hungary",
        "difficulty": "expert",
        "nationality": "Hungary",
        "description": "Hungarian genius of the Mighty Magyars who scored 84 goals in 85 games for Hungary and led Real Madrid to three European Cups. FIFA's goal of the year award is named in his honor.",
        "hints": [
            {"time": 30, "text": "I was the talisman of Hungary's legendary 1950s 'Mighty Magyars' team, nicknamed 'The Galloping Major'."},
            {"time": 60, "text": "I joined Real Madrid at age 31, scoring four goals in the famous 1960 European Cup Final at Hampden Park."},
            {"time": 90, "text": "FIFA created an annual world award in 2009 named after me to honor the most aesthetically beautiful goal of the season."}
        ],
        "image": "/assets/characters/football/fb-032.jpg",
        "anime": "football"
    },
    {
        "id": "fb-033",
        "name": "Alfredo Di Stefano",
        "wiki": "Alfredo Di Stéfano",
        "acceptedAnswers": ["di stefano", "alfredo di stefano", "di stéfano", "alfredo di stéfano"],
        "aliases": ["Saeta Rubia", "The Blond Arrow"],
        "arc": "Vintage Legends (Pre-1980s)",
        "affiliation": "Real Madrid / Millonarios / Argentina / Spain",
        "difficulty": "expert",
        "nationality": "Argentina / Spain",
        "description": "The 'Blond Arrow' who inspired Real Madrid to win the first five consecutive European Cups (1956-1960), the only recipient of the Super Ballon d'Or.",
        "hints": [
            {"time": 30, "text": "Nicknamed 'La Saeta Rubia' (The Blond Arrow), I was capable of defending, orchestrating midfield, and finishing like a poacher."},
            {"time": 60, "text": "I scored in all five consecutive European Cup Finals won by Real Madrid from 1956 to 1960."},
            {"time": 90, "text": "France Football awarded me the one and only 'Super Ballon d'Or' in 1989, honoring the greatest European footballer of three decades."}
        ],
        "image": "/assets/characters/football/fb-033.jpg",
        "anime": "football"
    },
    {
        "id": "fb-034",
        "name": "Eusebio",
        "wiki": "Eusébio",
        "acceptedAnswers": ["eusebio", "eusébio", "eusebio da silva ferreira"],
        "aliases": ["The Black Panther", "O Rei"],
        "arc": "Vintage Legends (Pre-1980s)",
        "affiliation": "Benfica / Portugal",
        "difficulty": "hard",
        "nationality": "Portugal",
        "description": "Mozambique-born Portuguese scoring phenomenon who guided Benfica to European glory and won the 1965 Ballon d'Or and 1966 World Cup Golden Boot.",
        "hints": [
            {"time": 30, "text": "Born in Mozambique, I became Portugal's greatest national sporting icon, known as 'The Black Panther'."},
            {"time": 60, "text": "I scored 473 goals in 440 competitive matches for SL Benfica, leading them to European Cup triumph in 1962."},
            {"time": 90, "text": "I scored nine goals at the 1966 World Cup in England, single-handedly turning a 3-0 deficit against North Korea into a 5-3 win."}
        ],
        "image": "/assets/characters/football/fb-034.jpg",
        "anime": "football"
    },
    {
        "id": "fb-035",
        "name": "George Best",
        "wiki": "George Best",
        "acceptedAnswers": ["george best", "best"],
        "aliases": ["El Beatle", "Belfast Boy"],
        "arc": "Vintage Legends (Pre-1980s)",
        "affiliation": "Manchester United / Northern Ireland",
        "difficulty": "hard",
        "nationality": "Northern Ireland",
        "description": "Belfast winger celebrated for dazzling balance, audacious dribbling, and rockstar charisma, winning the 1968 European Cup and Ballon d'Or with Manchester United.",
        "hints": [
            {"time": 30, "text": "With long hair and popstar charisma, Portuguese media dubbed me 'El Beatle' after a masterclass against Benfica in 1966."},
            {"time": 60, "text": "Along with Bobby Charlton and Denis Law, I formed Manchester United's celebrated 'United Trinity'."},
            {"time": 90, "text": "Pelé famously stated that I was the greatest footballer in the world; a famous quote about me is: 'Maradona good; Pelé better; George Best'."}
        ],
        "image": "/assets/characters/football/fb-035.jpg",
        "anime": "football"
    },
    {
        "id": "fb-036",
        "name": "Franz Beckenbauer",
        "wiki": "Franz Beckenbauer",
        "acceptedAnswers": ["beckenbauer", "franz beckenbauer", "der kaiser"],
        "aliases": ["Der Kaiser"],
        "arc": "Classic Eras (1980s-1990s)",
        "affiliation": "Bayern Munich / West Germany",
        "difficulty": "hard",
        "nationality": "Germany",
        "description": "German defensive mastermind 'Der Kaiser' who invented the modern attacking sweeper (libero) role, winning the World Cup as captain (1974) and manager (1990).",
        "hints": [
            {"time": 30, "text": "Revered as 'Der Kaiser' (The Emperor), I carried myself on the pitch with effortless elegance and regal authority."},
            {"time": 60, "text": "I revolutionized football tactics by transforming the traditional sweeper role into a creative deep-lying playmaker."},
            {"time": 90, "text": "I captained Bayern Munich to three consecutive European Cups and won the FIFA World Cup as both player (1974) and manager (1990)."}
        ],
        "image": "/assets/characters/football/fb-036.jpg",
        "anime": "football"
    },
    {
        "id": "fb-037",
        "name": "Johan Cruyff",
        "wiki": "Johan Cruyff",
        "acceptedAnswers": ["cruyff", "johan cruyff", "cruijff", "johan cruijff"],
        "aliases": ["The Flying Dutchman", "El Salvador"],
        "arc": "Classic Eras (1980s-1990s)",
        "affiliation": "Ajax / Barcelona / Netherlands",
        "difficulty": "hard",
        "nationality": "Netherlands",
        "description": "Three-time Ballon d'Or winner and visionary philosopher of 'Total Football' who transformed Ajax, Barcelona, and the tactical landscape of world football.",
        "hints": [
            {"time": 30, "text": "Famous for wearing the unconventional #14 shirt, I patented the iconic 180-degree turn feint named the 'Cruyff Turn'."},
            {"time": 60, "text": "Under coach Rinus Michels, I was the on-pitch orchestra conductor of 'Total Football' with Ajax and the Netherlands."},
            {"time": 90, "text": "As Barcelona manager, I created the 'Dream Team', established the La Masia youth academy philosophy, and won the 1992 European Cup."}
        ],
        "image": "/assets/characters/football/fb-037.jpg",
        "anime": "football"
    },
    {
        "id": "fb-038",
        "name": "Michel Platini",
        "wiki": "Michel Platini",
        "acceptedAnswers": ["platini", "michel platini"],
        "aliases": ["Le Roi Michel"],
        "arc": "Classic Eras (1980s-1990s)",
        "affiliation": "Juventus / Saint-Étienne / France",
        "difficulty": "hard",
        "nationality": "France",
        "description": "French midfield maestro who won three consecutive Ballons d'Or (1983-1985) and scored a record 9 goals in 5 games at Euro 1984.",
        "hints": [
            {"time": 30, "text": "Known as 'Le Roi' (The King), I was the master free-kick specialist and playmaker of Juventus and France in the 1980s."},
            {"time": 60, "text": "I achieved the unprecedented feat of winning three consecutive Ballons d'Or in 1983, 1984, and 1985."},
            {"time": 90, "text": "I captained France to Euro 1984 glory, scoring a tournament-record nine goals across just five matches."}
        ],
        "image": "/assets/characters/football/fb-038.jpg",
        "anime": "football"
    },
    {
        "id": "fb-039",
        "name": "Marco van Basten",
        "wiki": "Marco van Basten",
        "acceptedAnswers": ["van basten", "marco van basten"],
        "aliases": ["The Swan of Utrecht"],
        "arc": "Classic Eras (1980s-1990s)",
        "affiliation": "AC Milan / Ajax / Netherlands",
        "difficulty": "hard",
        "nationality": "Netherlands",
        "description": "Three-time Ballon d'Or Dutch marksman regarded as the complete center-forward, famed for his impossible dipping volley in the Euro 1988 final.",
        "hints": [
            {"time": 30, "text": "Known as 'The Swan of Utrecht', my predatory instincts and acrobatic volleys made me the ultimate complete #9 striker."},
            {"time": 60, "text": "I formed Milan's dominant Dutch trio alongside Ruud Gullit and Frank Rijkaard, winning back-to-back European Cups."},
            {"time": 90, "text": "I scored what many call the greatest goal in international history: an impossible dipping volley from an acute angle in the Euro 1988 Final."}
        ],
        "image": "/assets/characters/football/fb-039.jpg",
        "anime": "football"
    },
    {
        "id": "fb-040",
        "name": "Franco Baresi",
        "wiki": "Franco Baresi",
        "acceptedAnswers": ["baresi", "franco baresi"],
        "aliases": ["Piscinin", "Kaiser Franz of Milan"],
        "arc": "Classic Eras (1980s-1990s)",
        "affiliation": "AC Milan / Italy",
        "difficulty": "expert",
        "nationality": "Italy",
        "description": "Legendary one-club sweeper who captained Arrigo Sacchi's untouchable AC Milan, anchoring a backline that conceded only 14 goals in an entire Serie A season.",
        "hints": [
            {"time": 30, "text": "I spent my entire 20-year professional career with AC Milan, wearing the immortal #6 jersey which was subsequently retired."},
            {"time": 60, "text": "I marshaled the offside trap with an raised left arm, anchoring the impenetrable Milan defense alongside Maldini and Costacurta."},
            {"time": 90, "text": "At the 1994 World Cup, I underwent meniscus surgery and returned in just 25 days to deliver a man-of-the-match masterclass in the final against Brazil."}
        ],
        "image": "/assets/characters/football/fb-040.jpg",
        "anime": "football"
    },
    {
        "id": "fb-041",
        "name": "Paolo Maldini",
        "wiki": "Paolo Maldini",
        "acceptedAnswers": ["maldini", "paolo maldini"],
        "aliases": ["Il Capitano"],
        "arc": "Golden Era (2000s-2010s)",
        "affiliation": "AC Milan / Italy",
        "difficulty": "hard",
        "nationality": "Italy",
        "description": "The quintessential gentleman defender who played 25 seasons for AC Milan, winning 5 Champions League trophies and 7 Serie A titles.",
        "hints": [
            {"time": 30, "text": "I played 25 glorious seasons exclusively for AC Milan, spanning over 900 competitive appearances until age 41."},
            {"time": 60, "text": "Famous for the art of defending without needing to foul: 'If I have to make a tackle, then I have already made a mistake'."},
            {"time": 90, "text": "I contested eight European Cup/Champions League finals, winning five titles across three different decades."}
        ],
        "image": "/assets/characters/football/fb-041.jpg",
        "anime": "football"
    },
    {
        "id": "fb-042",
        "name": "Andrea Pirlo",
        "wiki": "Andrea Pirlo",
        "acceptedAnswers": ["pirlo", "andrea pirlo"],
        "aliases": ["The Architect", "Maestro"],
        "arc": "Golden Era (2000s-2010s)",
        "affiliation": "Juventus / AC Milan / Italy",
        "difficulty": "medium",
        "nationality": "Italy",
        "description": "Cool-headed deep-lying midfield architect renowned for pinpoint passes, free-kicks, nonchalant penalties, and the 2006 World Cup triumph.",
        "hints": [
            {"time": 30, "text": "With flowing hair and a calm demeanor, I played football with effortless elegance as the 'Regista' deep in midfield."},
            {"time": 60, "text": "I was named Man of the Match in the 2006 World Cup Final as Italy lifted the trophy in Berlin."},
            {"time": 90, "text": "I famously chipped Joe Hart with a cool Panenka penalty at Euro 2012, saying: 'I saw him jumping around, so I waited and chipped it'."}
        ],
        "image": "/assets/characters/football/fb-042.jpg",
        "anime": "football"
    },
    {
        "id": "fb-043",
        "name": "David Beckham",
        "wiki": "David Beckham",
        "acceptedAnswers": ["beckham", "david beckham", "becks"],
        "aliases": ["Goldenballs", "Becks"],
        "arc": "Golden Era (2000s-2010s)",
        "affiliation": "Manchester United / Real Madrid / LA Galaxy / England",
        "difficulty": "medium",
        "nationality": "England",
        "description": "Global football cultural icon famous for wicked curling crosses, legendary free-kicks ('Bend It Like Beckham'), and the 1999 Treble with Manchester United.",
        "hints": [
            {"time": 30, "text": "I broke onto the world stage by scoring from the halfway line against Wimbledon in 1996 for Manchester United."},
            {"time": 60, "text": "My right-foot curling technique was so celebrated it inspired the hit global film title 'Bend It Like Beckham'."},
            {"time": 90, "text": "I scored a stoppage-time free-kick against Greece in 2001 to send England to the World Cup, and won the historic 1999 Treble."}
        ],
        "image": "/assets/characters/football/fb-043.jpg",
        "anime": "football"
    },
    {
        "id": "fb-044",
        "name": "Roberto Carlos",
        "wiki": "Roberto Carlos",
        "acceptedAnswers": ["roberto carlos", "carlos"],
        "aliases": ["The Bullet Man", "El Hombre Bala"],
        "arc": "Golden Era (2000s-2010s)",
        "affiliation": "Real Madrid / Brazil",
        "difficulty": "medium",
        "nationality": "Brazil",
        "description": "Brazilian dynamic left-back celebrated for massive 24-inch thighs, lightning pace, and thunderbolt free-kicks that defied the laws of physics.",
        "hints": [
            {"time": 30, "text": "I had famously tree-trunk 24-inch thighs and played with attacking joy on the left flank for Real Madrid and Brazil."},
            {"time": 60, "text": "I won three Champions League crowns with the Galácticos and the 2002 World Cup alongside Ronaldo and Rivaldo."},
            {"time": 90, "text": "At Le Tournoi in 1997, I scored the impossible 'banana' free-kick against Fabien Barthez, bending the ball around the wall from 35 meters."}
        ],
        "image": "/assets/characters/football/fb-044.jpg",
        "anime": "football"
    },
    {
        "id": "fb-045",
        "name": "Dennis Bergkamp",
        "wiki": "Dennis Bergkamp",
        "acceptedAnswers": ["bergkamp", "dennis bergkamp"],
        "aliases": ["The Non-Flying Dutchman", "The Iceman"],
        "arc": "Classic Eras (1980s-1990s)",
        "affiliation": "Arsenal / Ajax / Netherlands",
        "difficulty": "hard",
        "nationality": "Netherlands",
        "description": "Technically sublime Dutch second-striker renowned for telepathic vision, ethereal first touch, and leading Arsenal's 2003-04 Invincibles.",
        "hints": [
            {"time": 30, "text": "Due to a severe phobia of flying in airplanes, I was affectionately nicknamed 'The Non-Flying Dutchman'."},
            {"time": 60, "text": "I was the creative mastermind of Arsène Wenger's 2003-04 Arsenal 'Invincibles' that went undefeated all season."},
            {"time": 90, "text": "I scored one of the World Cup's greatest goals in 1998 against Argentina: three sublime touches from a 60-yard Frank de Boer pass."}
        ],
        "image": "/assets/characters/football/fb-045.jpg",
        "anime": "football"
    },
    {
        "id": "fb-046",
        "name": "Ruud Gullit",
        "wiki": "Ruud Gullit",
        "acceptedAnswers": ["gullit", "ruud gullit"],
        "aliases": ["The Black Tulip"],
        "arc": "Classic Eras (1980s-1990s)",
        "affiliation": "AC Milan / Chelsea / Netherlands",
        "difficulty": "hard",
        "nationality": "Netherlands",
        "description": "Versatile Dutch superstar with trademark dreadlocks who won the 1987 Ballon d'Or, captained the Netherlands to Euro 1988 glory, and won two European Cups with AC Milan.",
        "hints": [
            {"time": 30, "text": "Instantly recognizable for my dreadlocks and mustache, I was nicknamed 'The Black Tulip' by Italian tifosi."},
            {"time": 60, "text": "Capable of dominating as a striker, attacking midfielder, or sweeper, I was the complete athlete of Arrigo Sacchi's Milan."},
            {"time": 90, "text": "I won the 1987 Ballon d'Or (dedicating it to Nelson Mandela) and captained the Netherlands to their first major trophy at Euro 1988."}
        ],
        "image": "/assets/characters/football/fb-046.jpg",
        "anime": "football"
    },
    {
        "id": "fb-047",
        "name": "Lothar Matthaus",
        "wiki": "Lothar Matthäus",
        "acceptedAnswers": ["matthaus", "lothar matthaus", "matthäus", "lothar matthäus"],
        "aliases": ["Der Leitwolf"],
        "arc": "Classic Eras (1980s-1990s)",
        "affiliation": "Bayern Munich / Inter Milan / Germany",
        "difficulty": "hard",
        "nationality": "Germany",
        "description": "Box-to-box German titan who captained West Germany to 1990 World Cup victory, won the 1990 Ballon d'Or, and played in five World Cups.",
        "hints": [
            {"time": 30, "text": "Diego Maradona famously praised me as 'the best rival I've ever had in my entire career'."},
            {"time": 60, "text": "I played in a record five separate FIFA World Cup tournaments (1982 to 1998) and earned 150 caps for Germany."},
            {"time": 90, "text": "I captained West Germany to glory at Italia 90, earning both the Ballon d'Or and the inaugural FIFA World Player of the Year in 1991."}
        ],
        "image": "/assets/characters/football/fb-047.jpg",
        "anime": "football"
    },
    {
        "id": "fb-048",
        "name": "Oliver Kahn",
        "wiki": "Oliver Kahn",
        "acceptedAnswers": ["kahn", "oliver kahn"],
        "aliases": ["Der Titan", "The Volcano"],
        "arc": "Golden Era (2000s-2010s)",
        "affiliation": "Bayern Munich / Germany",
        "difficulty": "hard",
        "nationality": "Germany",
        "description": "Fierce German goalkeeper nicknamed 'Der Titan' who won the Golden Ball at the 2002 World Cup, renowned for unyielding intensity and match-winning saves.",
        "hints": [
            {"time": 30, "text": "Known as 'Der Titan' and 'The Volcano', I struck fear into opposing strikers with my ferocious screams and commanding presence."},
            {"time": 60, "text": "I saved three penalties in the shootout of the 2001 UEFA Champions League Final against Valencia for Bayern Munich."},
            {"time": 90, "text": "I became the only goalkeeper in history to win the Golden Ball as the best player of a FIFA World Cup (2002 in Korea/Japan)."}
        ],
        "image": "/assets/characters/football/fb-048.jpg",
        "anime": "football"
    },
    {
        "id": "fb-049",
        "name": "Dino Zoff",
        "wiki": "Dino Zoff",
        "acceptedAnswers": ["zoff", "dino zoff"],
        "aliases": ["Monumental Dino"],
        "arc": "Vintage Legends (Pre-1980s)",
        "affiliation": "Juventus / Napoli / Italy",
        "difficulty": "expert",
        "nationality": "Italy",
        "description": "Imperturbable Italian captain who became the oldest player ever to win the World Cup at age 40 in 1982, keeping a record 1,142 consecutive minutes without conceding.",
        "hints": [
            {"time": 30, "text": "I held a legendary world record of 1,142 consecutive minutes without conceding a single goal in international football."},
            {"time": 60, "text": "I spent eleven title-laden seasons as the serene, unruffled #1 goalkeeper of Juventus."},
            {"time": 90, "text": "At age 40, I captained Italy to 1982 World Cup triumph in Spain, famously lifting the trophy alongside president Sandro Pertini."}
        ],
        "image": "/assets/characters/football/fb-049.jpg",
        "anime": "football"
    },
    {
        "id": "fb-050",
        "name": "Garrincha",
        "wiki": "Garrincha",
        "acceptedAnswers": ["garrincha", "manoel francisco dos santos", "mane garrincha"],
        "aliases": ["The Joy of the People", "Anjo de Pernas Tortas"],
        "arc": "Vintage Legends (Pre-1980s)",
        "affiliation": "Botafogo / Brazil",
        "difficulty": "expert",
        "nationality": "Brazil",
        "description": "Brazilian dribbling genius born with deformed legs who brought pure joy to millions, inspiring Brazil to the 1962 World Cup after Pelé was injured.",
        "hints": [
            {"time": 30, "text": "Born with deformed bowlegs that bent in different directions, doctors claimed I would never walk properly."},
            {"time": 60, "text": "Known as 'Alegria do Povo' (The Joy of the People), Brazil never lost a single match when I and Pelé played together."},
            {"time": 90, "text": "When Pelé was injured in the 1962 World Cup, I carried Brazil to the title, finishing as top scorer and Golden Ball winner."}
        ],
        "image": "/assets/characters/football/fb-050.jpg",
        "anime": "football"
    }
]

all_50 = existing + new_players

output_text = "import type { Character } from '../../types';\n\nexport const footballCharacters: Character[] = " + json.dumps(all_50, indent=2) + ";\n\nexport default footballCharacters;\n"

with open('src/data/football/characters.ts', 'w', encoding='utf-8') as f:
    f.write(output_text)

print(f"Generated 50 football players successfully! Total: {len(all_50)}")
