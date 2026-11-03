import re

with open('src/data/hunter-x-hunter/characters.ts', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace hxh-043, hxh-046, hxh-049
# Melody (Senritsu)
melody_block = """  {
    id: 'hxh-043',
    name: 'Melody',
    acceptedAnswers: ['melody', 'senritsu'],
    aliases: ['Senritsu', 'Music Hunter'],
    image: '/assets/characters/hunter-x-hunter/hxh-043.jpg',
    anime: 'hunter-x-hunter',
    arc: 'Yorknew City Arc',
    affiliation: 'Hunters Association / Nostrade Family',
    nenType: 'Emission',
    abilities: ['Sonata of Darkness research', 'Superhuman Hearing', 'Flute Calming Melodies'],
    description: 'A gentle Music Hunter whose body was disfigured by the Sonata of Darkness. She has extraordinary hearing capable of reading emotional heartbeats.',
    difficulty: 'hard',
    spoilerLevel: 1,
    hints: [
      { time: 30, text: 'I am a Music Hunter whose body was cursed after hearing the legendary Sonata of Darkness.' },
      { time: 60, text: 'My hearing is so acute I can detect changes in heartbeats to determine lies and mental states.' },
      { time: 90, text: 'I served as a bodyguard alongside Kurapika for Neon Nostrade during the Yorknew auction.' },
    ],
  },"""

# Razor (Reiza)
razor_block = """  {
    id: 'hxh-046',
    name: 'Razor',
    acceptedAnswers: ['razor', 'reiza'],
    aliases: ['Reiza'],
    image: '/assets/characters/hunter-x-hunter/hxh-046.jpg',
    anime: 'hunter-x-hunter',
    arc: 'Greed Island Arc',
    affiliation: 'Greed Island Game Masters',
    nenType: 'Emission',
    abilities: ['14 Devils Nen Beasts', 'High-velocity Nen Ball Spike'],
    description: 'A convicted criminal reformed by Ging Freecss who serves as one of the 11 Game Masters managing Greed Island spells and trials.',
    difficulty: 'hard',
    spoilerLevel: 1,
    hints: [
      { time: 30, text: 'I was a death-row convict given a second chance by Ging Freecss.' },
      { time: 60, text: 'I control emissions and the spell card systems as a Game Master on Greed Island.' },
      { time: 90, text: 'I challenged Gon, Killua, and Hisoka to an unforgettable, deadly Nen dodgeball battle.' },
    ],
  },"""

# Ikalgo
ikalgo_block = """  {
    id: 'hxh-049',
    name: 'Ikalgo',
    acceptedAnswers: ['ikalgo'],
    aliases: ['Squid'],
    image: '/assets/characters/hunter-x-hunter/hxh-049.jpg',
    anime: 'hunter-x-hunter',
    arc: 'Chimera Ant Arc',
    affiliation: 'Chimera Ants (defected) / Extermination Team',
    nenType: 'Manipulation',
    abilities: ['Living Dead Dolls (corpse host)', 'Flea Bullets Sniper Rifle'],
    description: 'An octopus-like Chimera Ant who wishes he were a squid. He becomes a loyal brother and comrade to Killua during the palace invasion.',
    difficulty: 'hard',
    spoilerLevel: 2,
    hints: [
      { time: 30, text: 'I am a Chimera Ant who resembles an octopus, though I deeply wish I was a squid.' },
      { time: 60, text: 'I can inhabit corpses with Living Dead Dolls and transform my tentacles into sniper rifles.' },
      { time: 90, text: 'Killua spared my life and called me cool, inspiring me to join the Hunters palace assault.' },
    ],
  },"""

# Replace in text
text = re.sub(r'\{\s*id:\s*\'hxh-043\'[\s\S]*?\n  \},', melody_block, text)
text = re.sub(r'\{\s*id:\s*\'hxh-046\'[\s\S]*?\n  \},', razor_block, text)
text = re.sub(r'\{\s*id:\s*\'hxh-049\'[\s\S]*?\n  \},', ikalgo_block, text)

# Promote Illumi, Chrollo, Ging, Netero, Biscuit to 'easy' so easy has 10 iconic characters
for cid in ['hxh-006', 'hxh-007', 'hxh-008', 'hxh-009', 'hxh-011']:
    text = re.sub(
        r'(id:\s*\'' + cid + r'\'[\s\S]*?difficulty:\s*\')medium(\')',
        r'\g<1>easy\g<2>',
        text
    )

with open('src/data/hunter-x-hunter/characters.ts', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated src/data/hunter-x-hunter/characters.ts successfully!")

