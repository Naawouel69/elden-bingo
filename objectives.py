"""
Pool of Elden Ring bingo objectives.
Each entry: {"text": str, "category": str, "difficulty": "Easy"|"Medium"|"Hard"}

Feel free to edit this list directly to add your own house-rule objectives —
the app picks them up automatically on next server restart.
"""

OBJECTIVES = [
    # ---------------- BOSSES ----------------
    {"text": "Defeat Margit, the Fell Omen", "category": "Bosses", "difficulty": "Easy"},
    {"text": "Defeat Godrick the Grafted", "category": "Bosses", "difficulty": "Easy"},
    {"text": "Defeat the Soldier of Godrick", "category": "Bosses", "difficulty": "Easy"},
    {"text": "Defeat an Erdtree Avatar", "category": "Bosses", "difficulty": "Easy"},
    {"text": "Defeat Leonine Misbegotten", "category": "Bosses", "difficulty": "Easy"},
    {"text": "Defeat any Catacomb boss", "category": "Bosses", "difficulty": "Easy"},
    {"text": "Defeat a Crucible Knight", "category": "Bosses", "difficulty": "Easy"},
    {"text": "Defeat the Grafted Scion", "category": "Bosses", "difficulty": "Easy"},
    {"text": "Defeat Flying Dragon Agheel", "category": "Bosses", "difficulty": "Easy"},

    {"text": "Defeat a Godskin Apostle", "category": "Bosses", "difficulty": "Medium"},
    {"text": "Defeat a Godskin Noble", "category": "Bosses", "difficulty": "Medium"},
    {"text": "Defeat Mohg, the Omen", "category": "Bosses", "difficulty": "Medium"},
    {"text": "Defeat the Fire Giant", "category": "Bosses", "difficulty": "Medium"},
    {"text": "Defeat Loretta, Knight of the Haligtree", "category": "Bosses", "difficulty": "Medium"},
    {"text": "Defeat Astel, Naturalborn of the Void", "category": "Bosses", "difficulty": "Medium"},
    {"text": "Defeat Commander Niall", "category": "Bosses", "difficulty": "Medium"},
    {"text": "Defeat a Dragonkin Soldier", "category": "Bosses", "difficulty": "Medium"},
    {"text": "Defeat Starscourge Radahn", "category": "Bosses", "difficulty": "Medium"},

    {"text": "Defeat Malenia, Blade of Miquella", "category": "Bosses", "difficulty": "Hard"},
    {"text": "Defeat Radagon and the Elden Beast", "category": "Bosses", "difficulty": "Hard"},
    {"text": "Defeat Mohg, Lord of Blood", "category": "Bosses", "difficulty": "Hard"},
    {"text": "Defeat Maliketh, the Black Blade", "category": "Bosses", "difficulty": "Hard"},
    {"text": "Defeat Godfrey, First Elden Lord", "category": "Bosses", "difficulty": "Hard"},
    {"text": "Defeat Dragonlord Placidusax", "category": "Bosses", "difficulty": "Hard"},
    {"text": "Defeat the Godskin Duo", "category": "Bosses", "difficulty": "Hard"},
    {"text": "Defeat the Beast Clergyman", "category": "Bosses", "difficulty": "Hard"},

    # ---------------- EXPLORATION ----------------
    {"text": "Reach the Roundtable Hold", "category": "Exploration", "difficulty": "Easy"},
    {"text": "Discover a hidden cave entrance", "category": "Exploration", "difficulty": "Easy"},
    {"text": "Rest at any Site of Grace", "category": "Exploration", "difficulty": "Easy"},
    {"text": "Rest at 2 Churches", "category": "Exploration", "difficulty": "Easy"},
    {"text": "Reach Liurnia of the Lakes", "category": "Exploration", "difficulty": "Easy"},
    {"text": "Rest at a Grace in Siofra River", "category": "Exploration", "difficulty": "Easy"},
    {"text": "Get trapped in a Teleporter Trap and come back alive", "category": "Exploration", "difficulty": "Easy"},

    {"text": "Fully explore a Catacomb and defeat its boss", "category": "Exploration", "difficulty": "Medium"},
    {"text": "Find and open a hidden wall in a legacy dungeon", "category": "Exploration", "difficulty": "Medium"},
    {"text": "Discover a Divine Tower", "category": "Exploration", "difficulty": "Medium"},
    {"text": "Find a hidden painting and locate the place it depicts", "category": "Exploration", "difficulty": "Medium"},
    {"text": "Solve a lever or statue puzzle to open a shortcut", "category": "Exploration", "difficulty": "Medium"},
    {"text": "Reach the Consecrated Snowfield", "category": "Exploration", "difficulty": "Medium"},
    {"text": "Find a hidden illusory wall using a Stonesword Key door as a clue", "category": "Exploration", "difficulty": "Medium"},

    {"text": "Fully explore Miquella's Haligtree", "category": "Exploration", "difficulty": "Hard"},
    {"text": "Reach the Mountaintops of the Giants without fast travel", "category": "Exploration", "difficulty": "Hard"},
    {"text": "Find every Great Rune location in a single region", "category": "Exploration", "difficulty": "Hard"},
    {"text": "Reach the deepest point of Siofra River without dying", "category": "Exploration", "difficulty": "Hard"},
    {"text": "Fully map an optional legacy dungeon, side rooms included", "category": "Exploration", "difficulty": "Hard"},
    {"text": "Discover the hidden path into Ainsel River", "category": "Exploration", "difficulty": "Hard"},

    # ---------------- ITEMS & GEAR ----------------
    {"text": "Pick up any Talisman", "category": "Items", "difficulty": "Easy"},
    {"text": "Find any Ash of War", "category": "Items", "difficulty": "Easy"},
    {"text": "Acquire a Golden Seed", "category": "Items", "difficulty": "Easy"},
    {"text": "Find a Smithing Stone", "category": "Items", "difficulty": "Easy"},
    {"text": "Find any Spirit Ash", "category": "Items", "difficulty": "Easy"},
    {"text": "Pick up any Crystal Tear", "category": "Items", "difficulty": "Easy"},

    {"text": "Acquire a Somber Smithing Stone", "category": "Items", "difficulty": "Medium"},
    {"text": "Obtain a full matching armor set", "category": "Items", "difficulty": "Medium"},
    {"text": "Acquire a Sacred Tear", "category": "Items", "difficulty": "Medium"},
    {"text": "Find a Cookbook and learn a new recipe", "category": "Items", "difficulty": "Medium"},
    {"text": "Obtain a Larval Tear", "category": "Items", "difficulty": "Medium"},
    {"text": "Acquire a unique Colossal Weapon", "category": "Items", "difficulty": "Medium"},
    {"text": "Obtain a Memory Stone", "category": "Items", "difficulty": "Medium"},

    {"text": "Acquire a Remembrance from a major boss", "category": "Items", "difficulty": "Hard"},
    {"text": "Fully upgrade a weapon to its max level", "category": "Items", "difficulty": "Hard"},
    {"text": "Obtain both halves of the Haligtree Secret Medallion", "category": "Items", "difficulty": "Hard"},
    {"text": "Acquire a Great Rune and activate it", "category": "Items", "difficulty": "Hard"},
    {"text": "Obtain a Rune Arc", "category": "Items", "difficulty": "Hard"},
    {"text": "Complete a merchant's full Bell Bearing upgrade line", "category": "Items", "difficulty": "Hard"},

    # ---------------- CHALLENGE ----------------
    {"text": "Parry an enemy successfully", "category": "Challenge", "difficulty": "Easy"},
    {"text": "Stagger any boss", "category": "Challenge", "difficulty": "Easy"},
    {"text": "Summon a Spirit Ash in a boss fight", "category": "Challenge", "difficulty": "Easy"},
    {"text": "Backstab an enemy", "category": "Challenge", "difficulty": "Easy"},
    {"text": "Achieve Rune level 30", "category": "Challenge", "difficulty": "Easy"},
    {"text": "Clear the Gatefront Ruins", "category": "Challenge", "difficulty": "Easy"},

    {"text": "Defeat a boss using only spells or incantations", "category": "Challenge", "difficulty": "Medium"},
    {"text": "Defeat a field boss without taking damage", "category": "Challenge", "difficulty": "Medium"},
    {"text": "Beat a boss with a weapon you just picked up, unupgraded", "category": "Challenge", "difficulty": "Medium"},
    {"text": "Win a duel against an invading NPC or player", "category": "Challenge", "difficulty": "Medium"},
    {"text": "Parry-kill a boss on its final blow", "category": "Challenge", "difficulty": "Medium"},
    {"text": "Defeat a boss using a weapon art as your main damage source", "category": "Challenge", "difficulty": "Medium"},

    {"text": "Defeat a demigod boss without using Spirit Ashes", "category": "Challenge", "difficulty": "Hard"},
    {"text": "No-hit any legacy dungeon boss", "category": "Challenge", "difficulty": "Hard"},
    {"text": "Defeat a boss using fists only", "category": "Challenge", "difficulty": "Hard"},
    {"text": "Defeat a boss at Rune Level 1", "category": "Challenge", "difficulty": "Hard"},
    {"text": "Defeat a boss with no armor equipped", "category": "Challenge", "difficulty": "Hard"},
    {"text": "Solo a boss meant for co-op summons, no help", "category": "Challenge", "difficulty": "Hard"},
]
