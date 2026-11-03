import type { Character } from '../types';
import type { Movie } from '../data/movies/movies';

// ============================================================
// MULTI-LANGUAGE CANONICAL ALIAS DICTIONARY
// Covers English, French, and Japanese (Romaji transliteration)
// for all characters across Hunter x Hunter, Naruto, JJK, and One Piece.
// ============================================================
export const MULTI_LANG_ALIASES: Record<string, string[]> = {
  // ─── HUNTER × HUNTER ─────────────────────────────────────────
  'hxh-001': ['gon', 'gon freecss', 'gon freecs', 'gon furikusu', 'furikusu'],
  'hxh-002': ['killua', 'killua zoldyck', 'kirua', 'kirua zoldik', 'kirua zoldyck', 'kirua zorudikku', 'kil', 'zoldyck', 'zoldik', 'zorudikku'],
  'hxh-003': ['kurapika', 'kurapica', 'kurapika kurta', 'kuruta'],
  'hxh-004': ['leorio', 'léorio', 'leorio paradinight', 'leorio paladiknight', 'leorio paradinaito', 'reorio', 'leolio'],
  'hxh-005': ['hisoka', 'hisoka morow', 'hisoka morrow', 'hisoka morou'],
  'hxh-006': ['illumi', 'illumi zoldyck', 'irumi', 'irumi zoldik', 'irumi zorudikku', 'gittarackur'],
  'hxh-007': ['chrollo', 'chrollo lucilfer', 'chrollo lucifer', 'kuroro', 'kuroro lucilfer', 'kuroro lucifer', 'kuroro rushirufuru'],
  'hxh-008': ['ging', 'ging freecss', 'jin', 'jin freecss', 'jin furikusu'],
  'hxh-009': ['netero', 'isaac netero', 'nettero', 'aizakku netero', 'president netero'],
  'hxh-010': ['kite', 'kaito'],
  'hxh-011': ['biscuit', 'bisky', 'biscuit krueger', 'bisket', 'bisuke kuruugaa', 'bisuke'],
  'hxh-012': ['meruem', 'meryem', 'meluem', 'le roi', 'roi des fourmis', 'chimera ant king'],
  'hxh-013': ['pitou', 'neferpitou', 'neferupitou'],
  'hxh-014': ['pouf', 'shaiapouf', 'shaiapwafu', 'shaapouf'],
  'hxh-015': ['youpi', 'yupi', 'menthuthuyoupi', 'montoutoyoupi', 'mentyutiyupi'],
  'hxh-016': ['komugi'],
  'hxh-017': ['knuckle', 'knuckle bine', 'nakkuru bain', 'nakkuru'],
  'hxh-018': ['shoot', 'shoot mcmahon', 'shuuto makumahon', 'shuuto'],
  'hxh-019': ['morel', 'morel mackernasey', 'morau makanaasii', 'morau'],
  'hxh-020': ['palm', 'palm siberia', 'paamu'],
  'hxh-021': ['zeno', 'zeno zoldyck', 'zeno zorudikku'],
  'hxh-022': ['silva', 'silva zoldyck', 'shiruba zorudikku', 'shiruba'],
  'hxh-023': ['alluka', 'alluka zoldyck', 'aruka', 'aruka zorudikku', 'nanika'],
  'hxh-024': ['kalluto', 'kalluto zoldyck', 'karuto zorudikku', 'karuto'],
  'hxh-025': ['nobunaga', 'nobunaga hazama'],
  'hxh-026': ['feitan', 'feitan portor', 'feitang'],
  'hxh-027': ['machi', 'machi komacine'],
  'hxh-028': ['shalnark', 'sharunaaku'],
  'hxh-029': ['uvogin', 'uvo', 'ubougin'],
  'hxh-030': ['bonolenov', 'bonolenov ndongo'],
  'hxh-031': ['pakunoda', 'paku'],
  'hxh-032': ['franklin', 'franklin bordeau'],
  'hxh-033': ['kortopi', 'korutopi'],
  'hxh-034': ['phinks', 'phinks magcub', 'finks'],
  'hxh-035': ['cheadle', 'cheadle yorkshire'],
  'hxh-036': ['pariston', 'pariston hill'],
  'hxh-037': ['satotz', 'satotsu'],
  'hxh-038': ['menchi'],
  'hxh-039': ['hanzo', 'hanzou'],
  'hxh-040': ['pokkle', 'pokkuru'],
  'hxh-041': ['goreinu', 'goleinu'],
  'hxh-042': ['tsezguerra', 'tsezgerra'],
  'hxh-043': ['kurapika', 'kurapica', 'kurapika kurta'],
  'hxh-044': ['knov', 'nov', 'nobu'],
  'hxh-045': ['genthru', 'the bomber', 'boomer', 'bomber'],
  'hxh-046': ['gon', 'adult gon', 'gon adulte', 'gon freecss'],
  'hxh-047': ['meleoron', 'meleolon', 'meruoron', 'jail', 'gods accomplice'],
  'hxh-048': ['mito', 'mito freecss', 'tante mito', 'aunt mito'],
  'hxh-049': ['killua', 'kirua', 'godspeed killua', 'kanmuru'],
  'hxh-050': ['tonpa', 'casseur de nouveaux', 'rookie crusher', 'shinjin tsubushi'],

  // ─── JUJUTSU KAISEN ──────────────────────────────────────────
  'jjk-001': ['yuji', 'yuuji', 'itadori', 'yuji itadori', 'yuuji itadori', 'itadori yuuji'],
  'jjk-002': ['megumi', 'fushiguro', 'megumi fushiguro', 'fushiguro megumi'],
  'jjk-003': ['nobara', 'kugisaki', 'nobara kugisaki', 'kugisaki nobara'],
  'jjk-004': ['gojo', 'gojou', 'satoru', 'satoru gojo', 'satoru gojou', 'gojo satoru', 'gojou satoru'],
  'jjk-005': ['sukuna', 'ryomen sukuna', 'ryoumen sukuna', 'roi des fleaux', 'king of curses'],
  'jjk-006': ['nanami', 'kento nanami', 'nanamin', 'nanami kento'],
  'jjk-007': ['mahito'],
  'jjk-008': ['geto', 'getou', 'suguru geto', 'suguru getou', 'kenjaku'],
  'jjk-009': ['todo', 'toudou', 'aoi todo', 'aoi toudou'],
  'jjk-010': ['inumaki', 'toge', 'toge inumaki'],
  'jjk-011': ['panda'],
  'jjk-012': ['yuta', 'yuuta', 'okkotsu', 'yuta okkotsu', 'yuuta okkotsu', 'okkotsu yuta'],
  'jjk-013': ['maki', 'maki zenin', 'zenin maki'],
  'jjk-014': ['hanami'],
  'jjk-015': ['yaga', 'masamichi yaga'],
  'jjk-016': ['choso', 'chousou'],
  'jjk-017': ['miwa', 'kasumi miwa'],
  'jjk-018': ['mechamaru', 'kokichi muta', 'muta'],
  'jjk-019': ['mei mei', 'meimei'],
  'jjk-020': ['kamo', 'noritoshi kamo'],
  'jjk-021': ['mai', 'mai zenin'],
  'jjk-022': ['dagon'],
  'jjk-023': ['naobito', 'naobito zenin'],
  'jjk-024': ['toji', 'toji fushiguro', 'toji zenin', 'fushiguro toji', 'sorcerer killer'],
  'jjk-025': ['jogo', 'jougo', 'curse jogo', 'disaster curse'],

  // ─── NARUTO ──────────────────────────────────────────────────
  'naruto-001': ['naruto', 'naruto uzumaki', 'uzumaki naruto', 'nanadaime', 'septieme hokage'],
  'naruto-002': ['sasuke', 'sasuke uchiha', 'uchiha sasuke'],
  'naruto-003': ['sakura', 'sakura haruno', 'sakura uchiha', 'haruno sakura'],
  'naruto-004': ['kakashi', 'kakashi hatake', 'hatake kakashi', 'ninja copieur', 'copy ninja', 'kakashi sensei'],
  'naruto-005': ['itachi', 'itachi uchiha', 'uchiha itachi'],
  'naruto-006': ['minato', 'minato namikaze', 'namikaze minato', 'eclair jaune', 'leclair jaune', 'leclair jaune de konoha', 'yellow flash', 'yondaime', 'quatrieme hokage'],
  'naruto-007': ['jiraiya', 'jiraya', 'lermite pas net', 'ermite pas net', 'ermite des crapauds', 'ero sennin', 'pervy sage', 'gama sennin'],
  'naruto-008': ['tsunade', 'tsunade senju', 'godaime', 'cinquieme hokage'],
  'naruto-009': ['orochimaru'],
  'naruto-010': ['lee', 'rock lee'],
  'naruto-011': ['neji', 'neji hyuga', 'neji hyuuga', 'hyuuga neji'],
  'naruto-012': ['gaara', 'gaara du desert', 'sabaku no gaara'],
  'naruto-013': ['pain', 'pein', 'nagato', 'nagato uzumaki'],
  'naruto-014': ['konan', 'ange de papier'],
  'naruto-015': ['obito', 'obito uchiha', 'tobi', 'uchiha obito'],
  'naruto-016': ['madara', 'madara uchiha', 'uchiha madara'],
  'naruto-017': ['hashirama', 'hashirama senju', 'shodaime', 'premier hokage', 'dieu des shinobi'],
  'naruto-018': ['guy', 'gai', 'might guy', 'gai maito', 'maito gai', 'guy sensei', 'gai sensei'],
  'naruto-019': ['hinata', 'hinata hyuga', 'hinata hyuuga', 'hyuuga hinata'],
  'naruto-020': ['shikamaru', 'shikamaru nara'],
  'naruto-021': ['zabuza', 'zabuza momochi', 'demon du brouillard', 'demon of the mist'],
  'naruto-022': ['haku'],
  'naruto-023': ['deidara'],
  'naruto-024': ['sasori', 'sasori du sable rouge'],
  'naruto-025': ['kisame', 'kisame hoshigaki'],
  'naruto-026': ['killer bee', 'killer b', 'bee', 'abeille tueuse', 'labeille tueuse', 'hachibi'],
  'naruto-027': ['temari'],
  'naruto-028': ['kankuro', 'kankurou'],
  'naruto-029': ['yamato', 'tenzo'],
  'naruto-030': ['sai'],

  // ─── ONE PIECE ───────────────────────────────────────────────
  'op-001': ['luffy', 'monkey d luffy', 'chapeau de paille', 'mugiwara', 'mugiwara no luffy', 'rufi', 'ruffy', 'straw hat'],
  'op-002': ['zoro', 'zorro', 'roronoa zoro', 'roronoa zorro', 'chasseur de pirates', 'pirate hunter', 'kaizoku gari'],
  'op-003': ['nami', 'chatte voleuse', 'la chatte voleuse', 'cat burglar'],
  'op-004': ['usopp', 'ussop', 'pipo', 'sogeking', 'roi des snipers', 'sniper king', 'god usopp'],
  'op-005': ['sanji', 'vinsmoke sanji', 'jambe noire', 'la jambe noire', 'black leg', 'kuroashi'],
  'op-006': ['chopper', 'tony chopper', 'tony tony chopper', 'tony-tony chopper'],
  'op-007': ['robin', 'nico robin', 'enfant demoniaque', 'lenfant demoniaque', 'devil child'],
  'op-008': ['franky', 'cutty flam', 'cyborg franky'],
  'op-009': ['brook', 'soul king'],
  'op-010': ['jinbe', 'jimbei', 'jinbei', 'jimbe', 'paladin des mers'],
  'op-011': ['garp', 'monkey d garp', 'heros de la marine', 'hero of the marines'],
  'op-012': ['akainu', 'sakazuki', 'chien rouge', 'red dog'],
  'op-013': ['whitebeard', 'barbe blanche', 'barbeblanche', 'shirohige', 'edward newgate'],
  'op-014': ['shanks', 'shanks le roux', 'le roux', 'red haired shanks', 'akagami', 'akagami no shanks'],
  'op-015': ['kaido', 'kaidou', 'kaido aux cent betes', 'cent betes', 'hyakujuu no kaidou'],
  'op-016': ['big mom', 'charlotte linlin', 'linlin'],
  'op-017': ['ace', 'portgas d ace', 'poing ardent', 'hiken', 'hiken no ace', 'gol d ace'],
  'op-018': ['law', 'trafalgar law', 'trafalgar d water law', 'chirurgien de la mort', 'surgeon of death', 'torafarugaa roo'],
  'op-019': ['mihawk', 'dracule mihawk', 'oeil de faucon', 'hawk eyes', 'taka no me'],
  'op-020': ['hancock', 'boa hancock', 'imperatrice pirate', 'hebihime', 'pirate empress'],
  'op-021': ['crocodile', 'sir crocodile', 'mr 0', 'mister 0'],
  'op-022': ['doflamingo', 'donquixote doflamingo', 'don quichotte doflamingo', 'don quichotte', 'doffy', 'joker'],
  'op-023': ['blackbeard', 'marshall d teach', 'barbe noire', 'barbenoire', 'teach', 'kurohige'],
  'op-024': ['rayleigh', 'silvers rayleigh', 'dark king', 'seigneur des tenebres', 'meio rayleigh'],
  'op-025': ['kuzan', 'aokiji', 'faisan bleu', 'blue pheasant'],
  'op-026': ['sabo', 'empereur des flammes', 'flame emperor'],
  'op-027': ['dragon', 'monkey d dragon', 'le rebelle', 'revolutionary'],
  'op-028': ['yamato', 'kozuki oden'],
  'op-029': ['buggy', 'baggy', 'buggy le clown', 'baggy le clown', 'buggy the clown', 'bagii'],
  'op-030': ['katakuri', 'charlotte katakuri'],
};

// Remove accents, punctuation, normalize spaces and case
export function normalize(str: string): string {
  return str
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '') // remove diacritics (é -> e, etc.)
    .toLowerCase()
    .trim()
    .replace(/['’`]/g, '')
    .replace(/[-_.:,/\\#]/g, ' ')
    .replace(/\s+/g, ' ');
}

// Convert Japanese Romaji / Phonetic variations:
// - ou/oo -> o, uu -> u
// - l -> r
// - c -> k
// - collapse duplicate consonants (rr -> r, ll -> l, ss -> s, etc.)
export function toPhoneticKey(str: string): string {
  return normalize(str)
    .replace(/ou/g, 'o')
    .replace(/uu/g, 'u')
    .replace(/oo/g, 'o')
    .replace(/aa/g, 'a')
    .replace(/ee/g, 'e')
    .replace(/l/g, 'r')
    .replace(/c/g, 'k')
    .replace(/(.)\1+/g, '$1') // collapse repeated letters
    .replace(/\s+/g, '');
}

// Levenshtein distance for typo tolerance
export function levenshtein(a: string, b: string): number {
  const m = a.length;
  const n = b.length;
  const dp: number[][] = Array.from({ length: m + 1 }, (_, i) =>
    Array.from({ length: n + 1 }, (_, j) => (i === 0 ? j : j === 0 ? i : 0))
  );
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      dp[i][j] =
        a[i - 1] === b[j - 1]
          ? dp[i - 1][j - 1]
          : 1 + Math.min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]);
    }
  }
  return dp[m][n];
}

/**
 * Validates an examinee's guess against a character's canon identity,
 * taking into full account English, French, and Japanese (Romaji) names,
 * single-token (first/last name) matches, accents, and phonetic transliterations.
 */
export function validateAnswer(guess: string, character: Character): boolean {
  const rawGuess = guess.trim();
  if (rawGuess.length < 2) return false;

  const normGuess = normalize(rawGuess);
  const phoneticGuess = toPhoneticKey(rawGuess);

  // Gather all acceptable answers from character definition + aliases + multi-language dictionary
  const rawAnswers = [
    character.name,
    ...character.acceptedAnswers,
    ...character.aliases,
    ...(MULTI_LANG_ALIASES[character.id] || []),
  ];

  // Tokenize canonical names into standalone tokens (e.g., 'Killua', 'Zoldyck', 'Satoru', 'Gojo')
  const individualTokens: string[] = [];
  for (const ans of rawAnswers) {
    const parts = normalize(ans).split(' ');
    for (const part of parts) {
      if (part.length >= 3 && !['the', 'and', 'des', 'aux', 'von', 'del', 'san'].includes(part)) {
        individualTokens.push(part);
      }
    }
  }

  const allAnswers = Array.from(new Set([...rawAnswers, ...individualTokens]));

  // 1. Direct Normalized & Substring Matching
  for (const ans of allAnswers) {
    const normAns = normalize(ans);
    if (!normAns) continue;

    // Exact normalized match (e.g. 'kirua', 'leorio', 'barbe blanche', 'gojo')
    if (normGuess === normAns) return true;

    // Full name contained in guess, or guess contained in answer (if guess is at least 4 chars)
    if (normAns.length >= 3 && normGuess.includes(normAns)) return true;
    if (normGuess.length >= 4 && normAns.includes(normGuess)) return true;
  }

  // 2. Japanese Romaji / Phonetic Key Matching
  for (const ans of allAnswers) {
    const phoneticAns = toPhoneticKey(ans);
    if (phoneticAns.length >= 3 && phoneticGuess === phoneticAns) {
      return true;
    }
    // Sub-key matching for long compound names
    if (phoneticAns.length >= 4 && phoneticGuess.length >= 4) {
      if (phoneticGuess.includes(phoneticAns) || phoneticAns.includes(phoneticGuess)) {
        return true;
      }
    }
  }

  // 3. Typo Tolerance via Levenshtein Distance
  for (const ans of allAnswers) {
    const normAns = normalize(ans);
    if (normAns.length < 4) continue;

    const allowedDistance = normAns.length > 8 ? 2 : normAns.length >= 5 ? 1 : 0;
    if (allowedDistance > 0 && levenshtein(normGuess, normAns) <= allowedDistance) {
      return true;
    }
  }

  return false;
}

/**
 * Validates a movie title guess against the film's title, accepted answers,
 * with leading article stripping (the, a, le, etc.), subtitle handling, and typo tolerance.
 */
export function validateMovieGuess(guess: string, movie: Movie): boolean {
  const rawGuess = guess.trim();
  if (rawGuess.length < 2) return false;

  const stripArticles = (s: string) =>
    normalize(s).replace(/^(the|a|an|le|la|les|un|une)\s+/, '').trim();

  const normGuess = normalize(rawGuess);
  const strippedGuess = stripArticles(rawGuess);
  const normTitle = normalize(movie.title);
  const strippedTitle = stripArticles(movie.title);

  // Exact normalized or stripped match
  if (normGuess === normTitle || strippedGuess === strippedTitle) return true;

  // Subtitle / partial title matching (e.g., 'The Fellowship of the Ring' -> 'Lord of the Rings')
  if (strippedGuess.length >= 4 && strippedTitle.includes(strippedGuess)) return true;
  if (strippedTitle.length >= 4 && strippedGuess.includes(strippedTitle)) return true;

  // Check against all accepted answers
  for (const ans of movie.acceptedAnswers) {
    const normAns = normalize(ans);
    const strippedAns = stripArticles(ans);

    if (normGuess === normAns || strippedGuess === strippedAns) return true;
    if (strippedAns.length >= 4 && strippedGuess.includes(strippedAns)) return true;
    if (strippedGuess.length >= 4 && strippedAns.includes(strippedGuess)) return true;

    // Typo tolerance
    const maxDist = strippedAns.length > 8 ? 2 : strippedAns.length >= 5 ? 1 : 0;
    if (maxDist > 0 && levenshtein(strippedGuess, strippedAns) <= maxDist) {
      return true;
    }
  }

  // Typo tolerance on main title
  if (strippedTitle.length >= 5) {
    const maxDist = strippedTitle.length > 8 ? 2 : 1;
    if (levenshtein(strippedGuess, strippedTitle) <= maxDist) {
      return true;
    }
  }

  return false;
}

