# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
如果API错误，不要停止，继续重试

## Running the Game

```bash
cd lord_of_mysteries
python3 main.py
```

**Requirements:** Python 3.x, Pygame (`pip install pygame`)

## Architecture Overview

This is a real-time action RPG based on "Lord of Mysteries" (诡秘之主), built with Pygame.

### Core Game Loop (game.py)

```
State Management → Event Handling → Update → Render
```

Game states: `MENU` → `PATHWAY_SELECT` → `PATHWAY_CONFIRM` → `PLAYING` → `GAME_OVER` (+ `PAUSED`, `INVENTORY`, `DIALOG`)

### Directory Structure

| Directory | Purpose |
|-----------|---------|
| `entities/` | Player and enemy classes |
| `systems/` | Core mechanics: inventory, potions, quests, lighting, sprites, weapons, save |
| `ui/` | All UI screens: menu, pathway selection, HUD, inventory, quests, dialogue, weapons, boss, save |
| `data/` | Static game data: pathways, enemies, items, quests, weapons |
| `img/charactor/` | Character sprite PNGs (one per pathway, 2x5 grid = 10 sequences) |
| `saves/` | JSON save files |

### Key Systems

**Pathway System (data/pathways.py)**
- 22 pathways, each with 10 sequences (S9→S0)
- Each sequence has: name, skills, HP, attack, defense, speed
- Pathway types: melee, magic, control, special, support, wisdom

**Sprite System (systems/sprites.py)**
- Loads character sprites at startup with progress bar
- Pre-scales to 4 sizes: tiny(50,65), small(60,80), medium(120,160), large(180,240)
- Maps Chinese pathway names to English filenames via `PATHWAY_FILE_NAMES` dict

**Combat System**
- Wave-based enemy spawning with progressive difficulty
- Real-time collision detection
- Enemies drop materials and weapons on death
- Boss enemies with multi-phase battles, clones, and special mechanics

**Weapon System (data/weapons.py, systems/weapon.py)**
- 7 weapon types: Sword, Dagger, Staff, Bow, Revolver, Cane, Fist
- Quality tiers: Common → Uncommon → Rare → Epic → Legendary
- Each weapon has: attack bonus, crit rate, crit damage, special effects

**Inventory/Potion System (systems/inventory.py, systems/potion.py)**
- Materials collected from enemy drops
- Crafting system for sequence advancement potions
- 30-second digestion period after crafting

**Save System (systems/save_system.py)**
- JSON-based save files in `saves/` directory
- Multiple save slots (max 5) + auto-save slot
- Stores: player state, inventory, quest progress, statistics

**Quest System (systems/quest.py, data/quests.py)**
- Quest types: Main, Side, Daily, Weekly
- Objective tracking: kill counts, material collection, boss kills, etc.

### Configuration (settings.py)

- Window: 1024x768 @ 60 FPS
- Color constants for UI consistency
- `GameState` enum for state machine
- `FONT_SIZES` dict for text rendering

### Adding New Content

**New Pathway:**
1. Add to `PATHWAY_FILE_NAMES` in `systems/sprites.py`
2. Add pathway data (name, god, color, sequences) to `PATHWAYS` in `data/pathways.py`
3. Place sprite PNG in `img/charactor/`

**New Enemy Type:** Add to enemy data in `data/enemies.py`

**New Items/Materials:** Add to `MATERIALS`/`CONSUMABLES` in `data/items.py`

**New Weapon:** Add to `WEAPONS` in `data/weapons.py` with type, quality, and stats

**New Quest:** Add to quest data in `data/quests.py` with objectives and rewards

### Controls

- WASD/Arrows: Move
- J/Left Mouse: Attack
- K/Right Mouse: Dodge
- 1-4: Skills
- I: Inventory
- Q: Quests
- ESC: Pause

### Rendering Order (in _draw_playing)

1. Background
2. Drops (items)
3. Enemies
4. Projectiles
5. Player
6. Damage numbers
7. Floating text
8. Lighting effects
9. HUD overlay
