import pygame
import random
import json

from pygame import key

from events import *
from fights import *
from enemes import *

import time

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((1128, 634))
pygame.display.set_caption("Adventure Game")
# Load the background image
background = pygame.image.load("images//start.png")
arrow_image = pygame.image.load("images//arrow.png")

# Create font objects
font_name_options_screens = "fonts//BlackChancery.ttf"
font_name_inventory_health_spells = "fonts//DragonHunter.otf"
font_size_options_screens = 22
font_size_health_spells = 20
font_size_inventory = 16
tip_text = ""

option_index = 0

screen_font = pygame.font.Font(font_name_options_screens, font_size_options_screens)
options_font = pygame.font.Font(font_name_options_screens, font_size_options_screens)
health_mana_gold_font = pygame.font.Font(font_name_inventory_health_spells, font_size_health_spells)
inventory_font = pygame.font.Font(font_name_inventory_health_spells, font_size_inventory)

text_height = screen_font.get_height()

# Set up the clock
clock = pygame.time.Clock()

# Set the desired frame rate (in FPS)
frame_rate = 10

# Global veriables
screen_id = "intro" # While Debugging
watch_screen = "intro" # While Debugging
previous_store_screen = ""
running = False
action = 0 
inventory_location = ""
location = ""
enemy = 0 

location_to_move = ""
location_of_end = ""
pay_for_rest = 20

# Read screens file

"""
 In this dictionary stored "screens". 
 "Screen" has a text that corresponds to game event, options and function.

 Option is a tuple: first element is option text, second element is a screen
 that will be displayed after clicking the corresponding option.

 Function: this is a certain fuction that changes text on screens
 or player state or other game events which happen or will happen  
 while player doing simething in the coresponding screen.

"""
with open("screens.json", "r") as file:
    screens = json.load(file)

# FLags to events
flags = {"hero_saw_bandits": False,
         "you_are_drunk": False,
         "party_in_tavern": False,
         "you_know_Jacob": False,
         "church_quest": False,
         "church_quest_done": False,
         "bandits_near_tavern": True, 
         "troll": False,
         "inventory_open": False,
         "spell_book_open": False,
         "you_know_where_jacob_live": False, 
         "beer": False,
         "conversation_done": False,
         "path_to_shadow_peaks": False,
         "guards_near_swamps": True,
         "fight_guards": False,
         "fight_creature": False,
         "fight_goblin": False,
         "troll_in_forest": True,
         "fight_troll": False,
         "bear_lair": False,
         "fight_bear": False,
         "berries": False,
         "fight_wolves": False,
         "buy_merchant_open": False,
         "buy_store_open": False,
         "sell_open": False,
         "allow_to_open_inventory": False} 

# NOTE: for testing["Bastion Sword", "equip", {"type_of_weapon": "sword", "damage": 20}]
"""
NOTE: 
      all weapons in the store should looks like this:
        {"name": "", "price": 0, "type": ("weapon", "weapon"), "stats": {"type": "(axe or sword)", "damage": 0}}
      
      all counted items in the store should looks like this:
        {"name": "", "price": 0, "type": ("counted", "")}
      
      all spells in the store should looks like this:
        {"name": "", "price": 0, "type": ("spell", "spell"), "stats": {"effect": "", "damage": 0, "mana_cost": 0}}
      
      all tools in the store should looks like this:
        {"name": "", "price": 0, "type": ("tools", "tool")}
      
      all armor in the store should looks like this:
        {"name": "", "price": 0, "type": ("armor", (for which part of body)), "stats": {(all stats that this item has)}}

"""


store = [{"name": "Bastard sword", "price": 40, "type": ("weapon", "weapon"), "stats": {"type": "sword", "damage": 30}}, 
        {"name": "Heal Potion", "price": 10, "type": ("counted", "potion")}, 
        {"name": "Mana Potion", "price": 10, "type": ("counted", "potion")}, 
        {"name": "Hunting Bow", "price": 30, "type": ("tools", "tool")}, 
        {"name": "Axe's Axe", "price": 30, "type": ("weapon", "weapon"), "stats": {"type": "axe", "damage": 20}}, 
        {"name": "FireBall", "price": 40, "type": ("spell", "spell"), "stats": {"effect": "fire", "damage": 30, "mana_cost": 60}}, 
        {"name": "FrostBall", "price": 30, "type": ("spell", "spell"), "stats": {"effect": "ice", "damage": 25, "mana_cost": 40}}]

merchant_store = \
    [{"name": "Lighting Bolt", "price": 30, "type": ("spell", "spell"), "stats": {"effect": "light", "damage": 20, "mana_cost": 35}},
     {"name": "Heal Potion", "price": 10, "type": ("counted", "potion")}, 
     {"name": "Mana Potion", "price": 10, "type": ("counted", "potion")},
     {"name": "Oak staff", "price": 100, "type": ("armor", "body"), "stats": {"mana": 10, "magic_damage": 10}},
     {"name": "Hunting knife", "price": 60, "type": ("tools", "tool")},
     {"name": "Herbs", "price": 20, "type": ("counted", "leaves")},
     {"name": "Magic flute", "price": 150, "type": ("tools", "tool")}]

current_store = store

items_sell_prices = [{"item": "Heal Potion", "sell_price": 5},
                     {"item": "Mana Potion", "sell_price": 5},
                     {"item": "Metal sword", "sell_price": 10},
                     {"item": "Axe's Axe", "sell_price": 15},
                     {"item": "Bastard sword", "sell_price": 20},
                     {"item": "Dead snake", "sell_price": 5},
                     {"item": "Purple flowers", "sell_price": 5},
                     {"item": "Gem", "sell_price": 50},
                     {"item": "Rusty sword", "sell_price": 5},
                     {"item": "Fine sword", "sell_price": 30},
                     {"item": "Golden Locket", "sell_price": 100},
                     {"item": "Long sword", "sell_price": 100},
                     {"item": "Berries", "sell_price": 10},
                     {"item": "Silver ring", "sell_price": 30},
                     {"item": "Warm coat", "sell_price": 10},
                     {"item": "Herbs", "sell_price": 5},
                     {"item": "Old backpack", "sell_price": 15},
                     {"item": "Crafting tools", "sell_price": 30},
                     {"item": "Rusty dagger", "sell_price": 5},
                     {"item": "Boar meat", "sell_price": 10},
                     {"item": "Boar leather", "sell_price": 10},
                     {"item": "Beer", "sell_price": 5},
                     {"item": "Troll hide", "sell_price": 100},
                     {"item": "Bear hide", "sell_price": 80},
                     {"item": "Bastion Sword", "sell_price": 20},
                     {"item": "Wolven hide", "sell_price": 15},
                     {"item": "Pork", "sell_price": 10},
                     {"item": "", "sell_price": 0},
                     {"item": "", "sell_price": 0},
                     {"item": "", "sell_price": 0},
                     {"item": "", "sell_price": 0}]


spells_description = {"Arcane Misile": "Manacost: 10 \\p Damage: 15 \\p Effect: None",
                      "FireBall": "Manacost: 60 \\p Damage: 30 \\p Effect: Fire",
                      "FrostBall": "Manacost: 40 \\p Damage: 25 \\p Effect: Ice",
                      "Lighting Bolt": "Manacost: 35 \\p Damage: 20 \\p Effect: Light",
                      "Water splash": "Manacost: 15 \\p Damage: 10 \\p Effect: Water"
                     }

weapons_description = {"Metal sword": "Damage: 10 \\p",
                       "Bastard sword": "Damage: 30 \\p",
                       "Rusty sword": "Damage: 5 \\p",
                       "Fine sword": "Damage: 15 \\p",
                       "Long sword": "Damage: 25 \\p",
                       "Bastion Sword": "Damage: 20 \\p",
                       "Axe's Axe": "Damage: 20 \\ p",
                       "Rusty dagger": "Damage: 8 \\p"
                      }

tools_and_armor_description = { "Magic flute": "Allows to charm animals",
                      "Hunting Bow": "Chance to hunt something +30%",
                      "Hunting knife": "Chance to hunt something +20%",
                      "Oak staff": "+10 max_mana and +10% to magic attacks",
                    }

# Player state, inventory, spells, store

# {"name": "Bastion Sword", "status": "equip", "stats": {"type_of_weapon": "sword", "damage": 20}}

"""
NOTE:
    all weapons in the store should looks like this:
        {"name": "", "status": [(equipped or equip), "weapon"], "stats":{"type_of_weapon": "(axe or sword)", "damage": 0}}
    
    all counted items in the store should looks like this:
        {"name": "", "status": ("counted",  (general definition: potion, leaves, meat ...)), "count": number of item},
      
    all tools in the store should looks like this:
        {"name": "", "status": ("tools", "tool")}
      
    all armor in the store should looks like this:
        {"name": "", "status": ("armor", ("part of body")), "stats": {(all stats that this item has)}} 
"""

# For tests {"name": "Tool", "status": ("tools", "tool")}

inventory = [{"name": "Metal sword", "status": ["equipped", "weapon"], "stats":{"type_of_weapon": "sword", "damage": 10}},
             {"name": "Bastion Sword", "status": ["equip", "weapon"], "stats": {"type_of_weapon": "sword", "damage": 20}},
             {"name": "Heal Potion", "status": ("counted", "potion"), "count": 2},
             {"name": "Mana Potion", "status": ("counted", "potion"), "count": 2},
             {"name": "Pork", "status": ("counted", "meat"), "count": 4},
             {"name": "Magic flute", "status": ("tools", "tool")}]


# NOTE: for testing ["FireBall", {"effect": "fire", "damage": 30, "mana_cost": 60}]
spells = [{"name": "Arcane Misile", "stats" :{"effect": "nothing", "damage": 15, "mana_cost": 10}}]

state = {"health": 1000,
         "max_mana": 1000,
         "mana": 1000,
         "gold": 1000}

# Explore events in swamps
swamp_events = ["statue", "obelisk", "rusted_sword", "purple_flowers_1", 
                "purple_flowers_2", "solid_ground", "creature", "goblin"]

swamps_events_weights = [10, 10, 20, 15, 15, 20, 15, 10]

# Explore events in forest
numbered_forest_events = {"herbs": 10, "boar": 10, "travelers": 3, "wolves": 4}

forest_events = ["villagers", "bear", "herbs", "boar", 
                 "travelers", "wolves", "mushrooms", "merchant", "stone", "bear_lair"]

forest_events_weights = [10, 10, numbered_forest_events["herbs"] * 3, 
                         numbered_forest_events["boar"] * 3,
                         numbered_forest_events["travelers"] * 10, 
                         numbered_forest_events["wolves"] * 4, 1, 15, 5, 0]

# Explore events bear lair

lair_events = ["ring", "coat", "gold_1", "lair_herbs", 
               "pendant", "backpack", "tools", "dagger", "gold_2", "lair_key"]
lair_weights = {"counter": 0, "bear_attack_chance": 0}
    
def inventory_screen():
    if flags["inventory_open"]:
        if len(screens["inventory"]["options"]) == 0:
            add_inventory_in_screen()
        else:
            del_all_options(screens["inventory"]["options"])
            add_inventory_in_screen()        

def current_spells_screen():
    if flags["spell_book_open"]:
        if len(screens["current_spells"]["options"]) == 0:
            add_spells_to_screen(screens["current_spells"])
        else:
            del_all_options(screens["current_spells"]["options"])
            add_spells_to_screen(screens["current_spells"])

# =========================================================== FIGHT_FUNCTIONS ======================================== #
def choose_guard():
    global screen_id
    global action
    global enemy
    if action - 1 < len(screens["choose_guard"]["options"]):
        if len(guards) > 1:
            if screens["choose_guard"]["options"][action - 1][0] == "Guard_1" or "Guard_2" or "Guard_3":
                if action == 1:
                    enemy = 1
                    screen_id = "attack"
                    screens["attack"]["text"] = "How do you want to attack"
                    action = 0
                elif action == 2:
                    enemy = 2
                    screen_id = "attack"
                    screens["attack"]["text"] = "How do you want to attack"
                    action = 0
                elif action == 3:
                    enemy = 3
                    screen_id = "attack"
                    screens["attack"]["text"] = "How do you want to attack"
                    action = 0
        else:
            enemy = 0

def choose_wolf():
    global screen_id
    global action
    global enemy
    if action - 1 < len(screens["choose_wolf"]["options"]):
        if len(wolves) > 1:
            if screens["choose_wolf"]["options"][action - 1][0] == "Black wolf" or "Grey wolf" or "Brown wolf":
                if action == 1:
                    enemy = 1
                    screen_id = "attack"
                    screens["attack"]["text"] = "How do you want to attack"
                    action = 0
                elif action == 2:
                    enemy = 2
                    screen_id = "attack"
                    screens["attack"]["text"] = "How do you want to attack"
                    action = 0
                elif action == 3:
                    enemy = 3
                    screen_id = "attack"
                    screens["attack"]["text"] = "How do you want to attack"
                    action = 0
        else:
            enemy = 0

def choose_bandit():
    global enemy
    global screen_id
    global action
    if action - 1 < len(screens["choose_bandit"]["options"]):
        if len(bandits) > 1:
            if screens["choose_bandit"]["options"][action - 1][0] == "Bandit_1" or "Bandit_2" or "Bandit_Leader":
                if action == 1:
                    enemy = 1
                    screen_id = "attack"
                    screens["attack"]["text"] = "How do you want to attack"
                    action = 0
                elif action == 2:
                    enemy = 2
                    screen_id = "attack"
                    screens["attack"]["text"] = "How do you want to attack"
                    action = 0
                elif action == 3:
                    enemy = 3
                    screen_id = "attack"
                    screens["attack"]["text"] = "How do you want to attack"
                    action = 0
        else:
            enemy = 0

def add_spells_to_screen(screen_to_add):
    global spells

    next_screen = ""
    if screen_id == "current_spells":
        next_screen = ""
    else:
        next_screen = "evade"

    if len(screen_to_add["options"]) != 0:
        del_all_options(screen_to_add["options"])
        for spell in spells:
            screen_to_add["options"].append((spell["name"], next_screen))
    else:
        for spell in spells:
            screen_to_add["options"].append((spell["name"], next_screen))

def attack_and_spell():
    global action
    global screen_id
    global location_to_move

    global guard_enemes
    global bandit_enemes
    global wolves_enemes
    
    global forest_events
    global forest_events_weights
    global numbered_forest_events
    global swamp_events
    global swamps_events_weights


    events = {"forest_events": {"events": forest_events, 
                                "weights": forest_events_weights, 
                                "numbered_events": numbered_forest_events},
              
              "swamp_events": {"events": swamp_events, 
                               "weights": swamps_events_weights}}

    add_spells_to_screen(screens["spells"])
    if action != 0 and action <= len(screens["spells"]["options"]):
        if flags["hero_saw_bandits"] and flags["bandits_near_tavern"]:
            if screen_id == "spells":
                bandit_enemes, screen_id, action, location_to_move, events = \
                    attack_enemy_in_multiple_fight_spell(enemy, bandits, bandit_enemes, 
                    "choose_bandit", spells, parameters, events)
            
            elif action == 1 and screen_id != "spells":
                bandit_enemes, screen_id, action, location_to_move, events = \
                        attack_enemy_in_multiple_fight_weapon(enemy, bandits, bandit_enemes, 
                        "choose_bandit", parameters, events)

        elif flags["guards_near_swamps"] and flags["fight_guards"]:
            if screen_id == "spells":
                guard_enemes, screen_id, action, location_to_move, events = \
                    attack_enemy_in_multiple_fight_spell(enemy, guards, guard_enemes, 
                    "choose_guard", spells, parameters, events)
            
            elif action == 1 and screen_id != "spells":
                guard_enemes, screen_id, action, location_to_move, events = \
                        attack_enemy_in_multiple_fight_weapon(enemy, guards, guard_enemes, 
                        "choose_guard", parameters, events)

        elif flags["fight_wolves"]:
            if screen_id == "spells":
                wolves_enemes, screen_id, action, location_to_move, events = \
                    attack_enemy_in_multiple_fight_spell(enemy, wolves, wolves_enemes, 
                    "choose_wolf", spells, parameters, events)
            
            elif action == 1 and screen_id != "spells":
                wolves_enemes, screen_id, action, location_to_move, events = \
                        attack_enemy_in_multiple_fight_weapon(enemy, wolves, wolves_enemes, 
                        "choose_wolf", parameters, events)

        elif flags["fight_creature"]:
            if screen_id == "spells":
                screen_id, action, location_to_move, events = \
                    attack_enemy_spell(creature, spells, parameters, events)
            elif action == 1 and screen_id != "spells":
                screen_id, action, location_to_move, events = \
                        attack_enemy_weapon(creature, parameters, events)

        elif flags["fight_goblin"]:
            if screen_id == "spells":
                screen_id, action, location_to_move, events = \
                    attack_enemy_spell(goblin, spells, parameters, events)
            elif action == 1 and screen_id != "spells":
                screen_id, action, location_to_move, events = \
                        attack_enemy_weapon(goblin, parameters, events)

        elif flags["fight_troll"]:
            if screen_id == "spells":
                screen_id, action, location_to_move, events = \
                    attack_enemy_spell(troll, spells, parameters, events)
            elif action == 1 and screen_id != "spells":
                screen_id, action, location_to_move, events = \
                        attack_enemy_weapon(troll, parameters, events)

        elif flags["fight_bear"]:
            if screen_id == "spells":
                screen_id, action, location_to_move, events = \
                    attack_enemy_spell(bear_enemy, spells, parameters, events)
            elif action == 1 and screen_id != "spells":
                screen_id, action, location_to_move, events = \
                        attack_enemy_weapon(bear_enemy, parameters, events)

    forest_events = events["forest_events"]["events"]
    forest_events_weights = events["forest_events"]["weights"]
    numbered_forest_events = events["forest_events"]["numbered_events"]
    swamp_events = events["swamp_events"]["events"]
    swamps_events_weights = events["swamp_events"]["weights"]

def evade():
    global bandit_enemes
    global guard_enemes
    global wolves_enemes

    global action
    global screen_id
   
    if action != 0 and action - 1 < len(screens["evade"]["options"]) and flags["hero_saw_bandits"] and \
        flags["bandits_near_tavern"]:
        if screens["evade"]["options"][0][1] == "attack":
            del_all_options(screens["evade"]["options"])
            screens["evade"]["options"].append(("Attempt to evade", "evade"))
            screens["evade"]["options"].append(("Try to parry", "evade"))
            screens["evade"]["options"].append(("Block with magic shield", "evade"))
        
        if bandit_enemes == 1:
            bandit_enemes, action = evade_enemes(bandits, bandit_enemes, "choose_bandit", parameters)
            if len(bandits) > 1:
                screen_id = "choose_bandit"
                action = 0
            else:
                screen_id = "attack"
                action = 0
        else:
            bandit_enemes, action = evade_enemes(bandits, bandit_enemes, "choose_bandit", parameters)
    
    if action != 0 and action - 1 < len(screens["evade"]["options"]) and flags["guards_near_swamps"] \
        and flags["fight_guards"]:
        
        if screens["evade"]["options"][0][1] == "attack":
            del_all_options(screens["evade"]["options"])
            screens["evade"]["options"].append(("Attempt to evade", "evade"))
            screens["evade"]["options"].append(("Try to parry", "evade"))
            screens["evade"]["options"].append(("Block with magic shield", "evade"))

        if guard_enemes == 1:
            guard_enemes, action = evade_enemes(guards, guard_enemes, "choose_guard", parameters)
            if len(guards) > 1:
                screen_id = "choose_guard"
                action = 0
            else:
                screen_id = "attack"
                action = 0
        else:
            guard_enemes, action = evade_enemes(guards, guard_enemes, "choose_guard", parameters)
    
    if action != 0 and action - 1 < len(screens["evade"]["options"]) and flags["fight_wolves"] :
        
        if screens["evade"]["options"][0][1] == "attack":
            del_all_options(screens["evade"]["options"])
            screens["evade"]["options"].append(("Attempt to evade", "evade"))
            screens["evade"]["options"].append(("Try to parry", "evade"))
            screens["evade"]["options"].append(("Block with magic shield", "evade"))

        if wolves_enemes == 1:
            wolves_enemes, action = evade_enemes(wolves, wolves_enemes, "choose_wolf", parameters)
            if len(wolves) > 1:
                screen_id = "choose_wolf"
                action = 0
            else:
                screen_id = "attack"
                action = 0
        else:
            wolves_enemes, action = evade_enemes(wolves, wolves_enemes, "choose_wolf", parameters)

    if action != 0 and action - 1 < len(screens["evade"]["options"]) and flags["fight_creature"]:
        if screens["evade"]["options"][0][1] == "evade":
            del_all_options(screens["evade"]["options"])
            screens["evade"]["options"].append(("Attempt to evade", "attack"))
            screens["evade"]["options"].append(("Try to parry", "attack"))
            screens["evade"]["options"].append(("Block with magic shield", "attack"))
        
        screen_id, action = evade_enemy(creature, parameters)
    
    if action != 0 and action - 1 < len(screens["evade"]["options"]) and flags["fight_goblin"]:
        if screens["evade"]["options"][0][1] == "evade":
            del_all_options(screens["evade"]["options"])
            screens["evade"]["options"].append(("Attempt to evade", "attack"))
            screens["evade"]["options"].append(("Try to parry", "attack"))
            screens["evade"]["options"].append(("Block with magic shield", "attack"))
        screen_id, action = evade_enemy(goblin, parameters)
    
    if action != 0 and action - 1 < len(screens["evade"]["options"]) and flags["fight_troll"]:
        if screens["evade"]["options"][0][1] == "evade":
            del_all_options(screens["evade"]["options"])
            screens["evade"]["options"].append(("Attempt to evade", "attack"))
            screens["evade"]["options"].append(("Try to parry", "attack"))
            screens["evade"]["options"].append(("Block with magic shield", "attack"))
        screen_id, action = evade_enemy(troll, parameters)
    
    if action != 0 and action - 1 < len(screens["evade"]["options"]) and flags["fight_bear"]:
        if screens["evade"]["options"][0][1] == "evade":
            del_all_options(screens["evade"]["options"])
            screens["evade"]["options"].append(("Attempt to evade", "attack"))
            screens["evade"]["options"].append(("Try to parry", "attack"))
            screens["evade"]["options"].append(("Block with magic shield", "attack"))
        
        screen_id, action = evade_enemy(bear_enemy, parameters)

# ======================================================= FIGHT_FUNCTIONS ============================================== #

# ======================================================= RenderTextFunction =========================================== #
def renderTextAt(text, font, colour, x, y, screen, allowed_width):
    # first, split the text into words
    words = text.split()

    # now, construct lines out of these words
    lines = []
    while len(words) > 0:
        # get as many words as will fit within allowed_width
        line_words = []
        while len(words) > 0:
            if words[0] == "\\p":
                words.pop(0)
                break
            else:
                line_words.append(words.pop(0))
            fw, fh = font.size(' '.join(line_words + words[:1]))
            
            if fw >= allowed_width:
                break

        # add a line consisting of those words
        line = ' '.join(line_words)
        lines.append(line)

    # now we've split our text into lines that fit into the width, actually
    # render them

    # we'll render each line below the last, so we need to keep track of
    # the culmative height of the lines we've rendered so far
    y_offset = 0
    for line in lines:
        fw, fh = font.size(line)

        # (tx, ty) is the top-left of the font surface
        tx = x
        ty = y + y_offset
        y_offset += fh

        font_surface = font.render(line, True, colour)
        screen.blit(font_surface, (tx, ty))
# ======================================================= END_RenderTextFunction ======================================= #

def showSpells():
    text = "Your spells: \\p\n"
    for spell in spells:
        text += spell["name"] + " \\p\n"
    
    renderTextAt(text, inventory_font, (0, 0, 0), 690, 320, screen, 800)
    renderTextAt("Spells ' S '", inventory_font, (0, 0, 0), 690, 490, screen, 800)
    

def check_mana_health_gold(screen_id):

    if state["health"] > 1000: # While Debugging
        state["health"] = 1000
    elif state["health"] <= 0:
        screen_id = "GAME_OVER"
    
    if state["mana"] > state["max_mana"]:
        state["mana"] = state["max_mana"]
    
    if state["gold"] <= 0:
        state["gold"] = 0
    
    return screen_id


def changeScreen(action):
    global screen_id
    if action != 0 and action <= len(watch_screen["options"]) and screen_id != "inventory" and\
        screen_id != "current_spells" and screen_id != "buy" and screen_id != "sell":
        screen_id = watch_screen["options"][action - 1][1]
        action = 0
    return action

def showHealth():
    state_text = "Health: {} / 100  Mana: {} / {}  Gold: {}".format(state["health"], 
                                                           state["mana"], 
                                                           state["max_mana"], 
                                                           state["gold"])
    renderTextAt(state_text, health_mana_gold_font, (0, 0, 0), 5, 5, screen, 800)


def showInventory():
    if screen_id != "inventory":
        text = "Inventory: \\p\n"
        for item in inventory:
            if item["status"][0] == "equipped":
                text += item["name"] + "(" + item["status"][0] + ")" + " \\p\n"
            elif item["status"][0] == "equip":
                    text += item["name"] + " \\p \n"
            elif item["status"][0] == "counted":
                text += item["name"] + " " + str(item["count"]) + " \\p\n"
            elif item["status"][0] == "tools":
                text += item["name"] + " \\p\n"
            elif item["status"][0] == "armor":
                text += item["name"] + " \\p\n"

        renderTextAt(text, inventory_font, (0, 0, 0), 865, 320, screen, 800)
    else:
        text = ""
        renderTextAt(text, inventory_font, (0, 0, 0), 865, 320, screen, 800)

# TODO: Move to the events.py
def add_inventory_in_screen():
    if screen_id == "inventory":
        for item in inventory:
            if item["status"][0] == "counted":
                screens["inventory"]["options"].append((item["name"] + " " + str(item["count"]), "inventory"))
            else:
                if item["status"][0] == "equipped":
                    screens["inventory"]["options"].append((item["name"] + " (" + item["status"][0] + ")", "inventory"))
       
                elif item["status"][0] == "equip":
                    screens["inventory"]["options"].append((item["name"], "inventory"))
       
                elif item["status"][0] == "items" or item["status"][0] == "tools" or item["status"][0] == "armor":
                    screens["inventory"]["options"].append((item["name"], "inventory"))
    else:
        pass
    

# TODO: BUGG ================================================= 3
def showingDescriptionForItemsAndSpells(index, items):
    item = items[index]
    text = ""
    if(flags["inventory_open"]):
        if(item["status"][1] == "weapon"):
            text = weapons_description[item["name"]]
        elif(item["status"][0] == "counted"):
            pass
        elif(item["status"][0] == "tools"):
            text = tools_and_armor_description[item["name"]]
        elif(item["status"][0] == "armor"):
            pass
    else:
        text = spells_description[item["name"]]
    renderTextAt(text, screen_font, (0, 0, 0), 380, 115, screen, 200)

def processingInventoryEvents(index):
    item = inventory[index]    
    if item["status"][0] == "counted":
        if item["name"] == "Heal Potion":
            state["health"] += 20
            inventory[index]["count"] -= 1
            if inventory[index]["count"] == 0:
                del inventory[index]
        
        elif item["name"] == "Mana Potion":
            state["mana"] += 20
            inventory[index]["count"] -= 1
            if inventory[index]["count"] == 0:
                del inventory[index]

        elif item["name"] == "Beer":
            state["health"] += 10
            inventory[index]["count"] -= 1
            if inventory[index]["count"] == 0:
                del inventory[index]

    elif item["status"][0] == "equip":
        inventory[find_equipped_item_index_inventory(inventory)]["status"][0] = "equip"
        inventory[index]["status"][0] = "equipped"

def drawArrow(image, x, y, index, text_height):
    option_offset = text_height * index
    screen.blit(image, (x, y + option_offset))


def showScreen(screen, screen_font, options_font, tip_text):  
    global background
    global option_index
    if screen_id == "inventory":
        options_text = ""
        for opt in watch_screen["options"]:
            options_text += "{} \p ".format(opt[0])

        background = pygame.image.load("images//inventory.png")
        renderTextAt(watch_screen["text"], screen_font, (0, 0, 0), 40, 115, screen, 850)
        renderTextAt(options_text, options_font, (0, 0, 0), 80, 150, screen, 450)
        renderTextAt(tip_text, screen_font, (0, 0, 0), 685, 5, screen, 850)

        drawArrow(arrow_image, 40, 150, option_index, text_height)
    
    elif screen_id == "current_spells":
        options_text = ""
        for opt in watch_screen["options"]:
            options_text += "{} \p ".format(opt[0])

        background = pygame.image.load("images//spells_image.png")
        renderTextAt(watch_screen["text"], screen_font, (0, 0, 0), 40, 115, screen, 850)
        renderTextAt(options_text, options_font, (0, 0, 0), 80, 150, screen, 450)
        renderTextAt(tip_text, screen_font, (0, 0, 0), 685, 5, screen, 850)

        drawArrow(arrow_image, 40, 150, option_index, text_height)

    elif screen_id == "sell" or screen_id == "buy" or screen_id == "offer_troll":
        options_text = ""
        for opt in watch_screen["options"]:
            options_text += "{} \p ".format(opt[0])

        background = pygame.image.load("images//store.png")
        renderTextAt(watch_screen["text"], screen_font, (0, 0, 0), 40, 115, screen, 850)
        renderTextAt(options_text, options_font, (0, 0, 0), 80, 150, screen, 450)
        renderTextAt(tip_text, screen_font, (0, 0, 0), 685, 5, screen, 850)
    
        drawArrow(arrow_image, 40, 150, option_index, text_height)

    elif screen_id == "sell" or screen_id == "buy" or screen_id == "offer_troll":
        options_text = ""
        i = 1
        for opt in watch_screen["options"]:
            options_text += "{} . {} \p ".format(i, opt[0])
            i += 1

        background = pygame.image.load("images//store.png")
        renderTextAt(watch_screen["text"], screen_font, (0, 0, 0), 40, 115, screen, 850)
        renderTextAt(options_text, options_font, (0, 0, 0), 40, 150, screen, 450)
        renderTextAt(tip_text, screen_font, (0, 0, 0), 685, 5, screen, 850)
    
    elif screen_id == "spells":
        options_text = ""
        i = 1
        for opt in watch_screen["options"]:
            options_text += "{} . {} \p ".format(i, opt[0])
            i += 1

        background = pygame.image.load("images//spells_image.png")
        renderTextAt(watch_screen["text"], screen_font, (0, 0, 0), 40, 115, screen, 850)
        renderTextAt(options_text, options_font, (0, 0, 0), 40, 150, screen, 450)
        renderTextAt(tip_text, screen_font, (0, 0, 0), 685, 5, screen, 850)
    else:
        if screen_id == "forest":
            background = pygame.image.load("images//forest.png")
        elif screen_id == "move":
            background = pygame.image.load("images//map.png")
        elif screen_id == "swamps":
            background = pygame.image.load("images//swamps.png")
        elif screen_id == "shadow_peaks_path":
            background = pygame.image.load("images//bridge_forest.png")    
        else:
            background = pygame.image.load("images//text_box.png")
    
        options_text = ""
        i = 1
        for opt in watch_screen["options"]:
            options_text += "{} . {} \p ".format(i, opt[0])
            i += 1
        
        renderTextAt(watch_screen["text"], screen_font, (0, 0, 0), 30, 115, screen, 850)
        renderTextAt(options_text, options_font, (0, 0, 0), 30, 370, screen, 480)
        renderTextAt(tip_text, screen_font, (0, 0, 0), 685, 5, screen, 850)


"""
This function performs processes that occur in the game. 
It checks the event and calls the corresponding function to this event

"""
def processingEvents():

    global global_running

    global tip_text
    global screen_id
    global action
    global pay_for_rest
    global previous_store_screen
    global current_store
    global location_of_end

    if screen_id in screens:
        print(screen_id)
        # ===============================================================TAVERN======================================= #
        if state["health"] <= 0:
            location_of_end = "Tavern_bandits"
            screen_id = "GAME_OVER"
        
        if flags["you_know_Jacob"]:
            screens["sad_man"]["options"].append(("Ask him about Jacob", "man_jacob"))
            screens["church"]["options"].append(("Ask the monk if he knows where  \\p\n" \
                                                    "to find Jacob", "church_jacob"))
            screens["women"]["options"].append(("Ask if they know Jacob", "women_jacob"))
            flags["you_know_Jacob"] = False

        if flags["you_know_where_jacob_live"]:
            screens["village"]["options"].append(("Find Jacob's place", "jacob_home"))
            flags["you_know_where_jacob_live"] = False

        if screen_id == "village" or screen_id == "store" or \
                screen_id == "forest" or screen_id == "swamps" or screen_id == "swamps_path":
            tip_text = "To open an inventory press ' I ' \\p\n To move to another location press ' M '" 
        
        elif screen_id == "shadow_peaks_path":
            tip_text = "To open an inventory press ' I ' \\p\n To move back press ' M '" 
        
        elif screen_id == "fight" or screen_id == "attack" or \
            screen_id == "evade" or screen_id == "spells" or screen_id == "loot" or \
            screen_id == "choose_bandit" or screen_id == "choose_guard":
            tip_text = "To open an inventory press ' I ' \\p\n"
       
        elif screen_id == "buy" or screen_id == "sell":
            tip_text = "To  exit press ' Esc '"
        
        elif screen_id == "hunter_sells":
            tip_text = "To open an inventory press ' I ' \\p\n To move on press ' M '"

        elif screen_id == "move":
            tip_text = "To open an inventory press ' I ' \\p\n Cancel movement ' Esc '" 
        
        elif screen_id != "inventory":
            tip_text = "To open an inventory press ' I '" 

        if screen_id == "innkeeper_lose_10_gold":
            flags["allow_to_open_inventory"] = False
            func = eval(screens[screen_id]["function"])
            func(state, screens)
        
        if screen_id == "innkeeper_lose_30_gold":
            flags["allow_to_open_inventory"] = False
            func = eval(screens[screen_id]["function"])
            func(state, screens)

        elif screen_id == "innkeeper":
            flags["allow_to_open_inventory"] = True
            func = eval(screens[screen_id]["function"])
            func(action, screens, inventory, state)

        elif screen_id == "party":
            flags["allow_to_open_inventory"] = False
            func = eval(screens[screen_id]["function"])
            func(flags, screens)

        elif screen_id == "old_woman":
            flags["allow_to_open_inventory"] = False
            func = eval(screens[screen_id]["function"])
            func(flags, screens)
        
        elif screen_id == "village":
            flags["allow_to_open_inventory"] = True
            func = eval(screens[screen_id]["function"])
            func(screens)
 
        elif screen_id == "store":
            flags["allow_to_open_inventory"] = True
            func = eval(screens[screen_id]["function"])
            previous_store_screen =  func(screens, previous_store_screen)
        
        elif screen_id == "hunter_sells":
            flags["allow_to_open_inventory"] = True
            func = eval(screens[screen_id]["function"])
            previous_store_screen =  func(previous_store_screen)
        
        elif screen_id == "forest":
            flags["allow_to_open_inventory"] = True
            func = eval(screens[screen_id]["function"])
            screen_id, action = func(flags, screens, screen_id, action, inventory,
           forest_events, forest_events_weights, numbered_forest_events)
        
        elif screen_id == "villagers":
            flags["allow_to_open_inventory"] = False
            func = eval(screens[screen_id]["function"])
            screen_id, action = func(screen_id, action, inventory, flags, state, forest_events, forest_events_weights)
        
        elif screen_id == "herbs":
            flags["allow_to_open_inventory"] = False
            func = eval(screens[screen_id]["function"])
            func(action, inventory, numbered_forest_events, forest_events_weights, forest_events)
        
        elif screen_id == "boar":
            flags["allow_to_open_inventory"] = False
            func = eval(screens[screen_id]["function"])
            screen_id, action = func(action, screen_id, inventory, 
                        numbered_forest_events, forest_events_weights, forest_events)
        
        elif screen_id == "travelers":
            flags["allow_to_open_inventory"] = False
            func = eval(screens[screen_id]["function"])
            screen_id, action = func(action, screen_id, numbered_forest_events, 
                                    forest_events_weights, forest_events, state)

        elif screen_id == "mushrooms":
            flags["allow_to_open_inventory"] = False
            func = eval(screens[screen_id]["function"])
            screen_id, action, location_of_end = func(screen_id, action, location_of_end)
        
        elif screen_id == "bear":
            flags["allow_to_open_inventory"] = True
            func = eval(screens[screen_id]["function"])
            screen_id, action = func(screens, screen_id, action, inventory, flags, state)
        
        elif screen_id == "bear_lair":
            flags["allow_to_open_inventory"] = True
            func = eval(screens[screen_id]["function"])
            screen_id, action = func(screen_id, action, lair_events, lair_weights, forest_events, inventory, state)
        
        elif screen_id == "choose_wolf":
            flags["allow_to_open_inventory"] = True
            func = eval(screens[screen_id]["function"])
            func()

        elif screen_id == "wolves":
            flags["allow_to_open_inventory"] = True
            func = eval(screens[screen_id]["function"])
            screen_id, action = func(screens, screen_id, action, flags, state, inventory)

        elif screen_id == "stone":
            flags["allow_to_open_inventory"] = False
            func = eval(screens[screen_id]["function"])
            screen_id, action = func(screen_id, action, forest_events, forest_events_weights, state)

        elif screen_id == "buy" or screen_id == "sell":
            flags["allow_to_open_inventory"] = True
            if previous_store_screen == "store":
                current_store = store
                if screen_id == "buy":
                    flags["buy_store_open"] = True
                else:
                    flags["sell_open"] = True
                func = eval(screens[screen_id]["function"])
                action = func(screen_id, screens, state, inventory, spells, store, items_sell_prices, action)
           
            elif previous_store_screen == "hunter_sells":
                current_store = merchant_store
                if screen_id == "buy":
                    flags["buy_merchant_open"] = True
                else:
                    flags["sell_open"] = True
                func = eval(screens[screen_id]["function"])
                action = func(screen_id, screens, state, inventory, spells, merchant_store, items_sell_prices, action)
        
        elif screen_id == "women_jacob":
            flags["allow_to_open_inventory"] = False
            func = eval(screens[screen_id]["function"])
            func(flags, screens)

        elif screen_id == "man_jacob":
            flags["allow_to_open_inventory"] = False
            func = eval(screens[screen_id]["function"])
            func(screens)

        #TODO: BUGG
        elif screen_id == "find_path" and action == 1:
            flags["allow_to_open_inventory"] = True
           # func = eval(screens[screen_id]["function"])
            location_of_end = "Swamps: tried to find path"
        
        elif screen_id == "swamps":
            flags["allow_to_open_inventory"] = True
            func = eval(screens[screen_id]["function"])
            screen_id, action = func(screens, screen_id, flags, swamp_events, swamps_events_weights, action)
        
        elif screen_id == "swamps_path":
            flags["allow_to_open_inventory"] = True
            func = eval(screens[screen_id]["function"])
            action = func(screens, flags, action)

        elif screen_id == "church_jacob":
            flags["allow_to_open_inventory"] = False
            func = eval(screens[screen_id]["function"])
            func(screens)
        
        elif screen_id == "choose_guard":
            flags["allow_to_open_inventory"] = True
            func = eval(screens[screen_id]["function"])
            func()
        
        elif screen_id == "bribe_guards":
            flags["allow_to_open_inventory"] = False
            func = eval(screens[screen_id]["function"])
            func(state, flags)
        
        elif screen_id == "fight_guards":
            flags["allow_to_open_inventory"] = True
            func = eval(screens[screen_id]["function"])
            func(screens, flags, action)
        
        elif screen_id == "in_tavern":
            flags["allow_to_open_inventory"] = True
            func = eval(screens[screen_id]["function"])
            func(flags, screens)

        elif screen_id == "choose_bandit":
            flags["allow_to_open_inventory"] = True
            func = eval(screens[screen_id]["function"])
            func()

        elif (screen_id == "attack" or screen_id == "spells" or screen_id == "fight"):
            flags["allow_to_open_inventory"] = True
            func = eval(screens[screen_id]["function"])
            func()
        
        elif screen_id == "evade":
            flags["allow_to_open_inventory"] = True
            func = eval(screens[screen_id]["function"])
            func()
        
        elif screen_id == "inventory":
            flags["allow_to_open_inventory"] = False
            flags["inventory_open"] = True
            func = eval(screens[screen_id]["function"])
            func()
        
        elif screen_id == "current_spells":
            flags["allow_to_open_inventory"] = False
            func = eval(screens[screen_id]["function"])
            func()
        
        elif screen_id == "church":
            flags["allow_to_open_inventory"] = True
            func = eval(screens[screen_id]["function"]) 
            func(screens, flags, state, action, pay_for_rest)

        elif screen_id == "church_quest":
            flags["allow_to_open_inventory"] = False
            func = eval(screens[screen_id]["function"])
            # TODO: Fix rest action
            pay_for_rest = func(screens, flags, inventory, action, pay_for_rest)

        elif screen_id == "sad_man":
            flags["allow_to_open_inventory"] = False
            func = eval(screens[screen_id]["function"])
            screen_id, action = func(parameters)

        elif screen_id == "jacob_home" :
            flags["allow_to_open_inventory"] = False
            func = eval(screens[screen_id]["function"])
            action = func(screens, flags, action)
        
        elif screen_id == "inside_jacob_house":
            flags["allow_to_open_inventory"] = False
            func = eval(screens[screen_id]["function"])
            action = func(screens, flags, inventory, action)   

        elif screen_id == "you_got_drunk":
            flags["allow_to_open_inventory"] = False
            func = eval(screens[screen_id]["function"])
            func(flags, state, screens)   

        elif screen_id == "statue":
            flags["allow_to_open_inventory"] = False
            func = eval(screens[screen_id]["function"])
            func(screens, state, inventory, action)
       
        elif screen_id == "obelisk":
            flags["allow_to_open_inventory"] = False
            func = eval(screens[screen_id]["function"])
            func(screens, state, spells, action)
       
        elif screen_id == "rusted_sword":
            flags["allow_to_open_inventory"] = False
            func = eval(screens[screen_id]["function"])
            func(screens, state, inventory, action)
       
        elif screen_id == "purple_flowers_1":
            flags["allow_to_open_inventory"] = False
            func = eval(screens[screen_id]["function"])
            func(screens, state, inventory, action)
        
        elif screen_id == "purple_flowers_2":
            flags["allow_to_open_inventory"] = False
            func = eval(screens[screen_id]["function"])
            func(screens, state, inventory, action)
        
        elif screen_id == "solid_ground":
            flags["allow_to_open_inventory"] = False
            func = eval(screens[screen_id]["function"])
            func(screens, state, action)

        elif screen_id == "creature":
            flags["allow_to_open_inventory"] = True
            func = eval(screens[screen_id]["function"])
            func(screens, flags, state, action)
        
        elif screen_id == "goblin":
            flags["allow_to_open_inventory"] = True
            func = eval(screens[screen_id]["function"])
            func(screens, flags, action)
        
        elif screen_id == "shadow_peaks_path":
            flags["allow_to_open_inventory"] = True
            func = eval(screens[screen_id]["function"])
            screen_id, action = func(screens, screen_id, action, state, flags)
            
        elif screen_id == "negotiate_troll":
            flags["allow_to_open_inventory"] = False
            func = eval(screens[screen_id]["function"])
            func(screens)
        
        elif screen_id == "ask_troll":
            flags["allow_to_open_inventory"] = False
            func = eval(screens[screen_id]["function"])
            func(screens)
        
        elif screen_id == "pay_troll":
            flags["allow_to_open_inventory"] = False
            func = eval(screens[screen_id]["function"])
            func(screens)
 
        elif screen_id == "offer_troll": 
            flags["allow_to_open_inventory"] = False
            func = eval(screens[screen_id]["function"])
            func(screens, inventory, action)

        elif screen_id == "troll_golden_locket": 
            flags["allow_to_open_inventory"] = False
            func = eval(screens[screen_id]["function"])
            func(screens)
        
        elif screen_id == "fight_troll":
            flags["allow_to_open_inventory"] = True
            func = eval(screens[screen_id]["function"])
            func(screens, flags, action)



# TODO: Replace this with functions and move into events.py

        elif screen_id == "church" or screen_id == "sad_man" or screen_id == "women":
            screens["village"]["text"] = '"Havencross" - a bustling settlement surrounded by fertile farmland and ' \
                                         'dotted with homes.'

        elif screen_id == "GAME_OVER":
            flags["allow_to_open_inventory"] = False
            if screen_id == "GAME_OVER" and action != 0 and action - 1 < len(screens["GAME_OVER"]["options"]):
                if screens["GAME_OVER"]["options"][action - 1][0] == "Close Game":
                    global_running = False
            elif location_of_end == "Swamps: tried to find path":
                type_of_death = random.randint(1, 3)
                if type_of_death == 1:
                    screens["GAME_OVER"]["text"] = "You ignored the guards' warning and ventured into the swamp." \
                                                    "Your steps sink into the murky water as hidden predator pulls you under." \
                                                    "The last thing you feel is the sharp teeth of a swamp monster piercing your skin."
                elif type_of_death == 2:
                    screens["GAME_OVER"]["text"] = "Despite the warnings, you forge ahead. Then the ground gives way beneath your" \
                                                    "feet and you fall. Struggling to escape, you slowly sink deeper and deeper" \
                                                    "into the swamp's murky depths, never to be seen again."
                elif type_of_death == 3:
                    screens["GAME_OVER"]["text"] = "You ignore the guards' warning and try to find a way around. Suddenly you" \
                                                    "feel a sharp pain in your leg. Looking down, you see a venomous snake has" \
                                                    "bitten you. You try to drag yourself to safety, but it's too late. The" \
                                                    "snake's venom is too strong and you collapse into the murky water."
                location_of_end = ""
            elif location_of_end == "Tavern_bandits":
                screens["GAME_OVER"]["text"] = "You was defited by bandits"
                location_of_end = ""
            
            elif location_of_end == "mushrooms":
                screens["GAME_OVER"]["text"] = "As you consume the magic mushrooms, you feel the world" \
                    " around you transform into something fantastical and otherworldly. The colors of the" \
                    " forest become brighter, and the sounds of the animals become more vibrant. Your mind" \
                    " begins to wander, and you find yourself questioning the purpose of your quest. You" \
                    " begin to feel that perhaps it is all meaningless, and that there is more to life than" \
                    " chasing after some grand goal. In this altered state, you decide to abandon your quest" \
                    " and instead spend your days exploring the natural wonders of the forest, living in the" \
                    " present moment and enjoying the simple pleasures of life."
                location_of_end = ""

# TODO: GOLDEN LOCKET BUGGG

# TODO: Tester using this function
#keys_combination = []
def randomAction(keys):
    amount = len(keys) - 1
    index = random.randint(0, amount)
 #   keys_combination.append(keys[index])
    key_down_event = pygame.event.Event(pygame.KEYDOWN, {'key': keys[index]})
    pygame.event.post(key_down_event)
    
    return keys[index]
    
keys = [pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_m, pygame.K_UP, pygame.K_DOWN, 
        pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, 
        pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_m, pygame.K_UP, pygame.K_DOWN, 
        pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_i]

test_keys = [pygame.K_ESCAPE, pygame.K_i, pygame.K_1, pygame.K_SPACE]

# Main game loop
global_running = True
start_time = time.time()
action_log = {"number": 0, "screen": "", "action": "", "time": 0}
# Open a file in write mode
file = open('log.txt', 'w')

while global_running:
    if screen_id in screens:
        watch_screen = screens[screen_id]
    print(randomAction(keys))

    # Handle events
    # TestLOG
    print("1 Step" + action_log["action"])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global_running = False
        elif event.type == pygame.KEYDOWN:
            # A key was pressed
            if event.key == pygame.K_ESCAPE and running and flags["inventory_open"]:
                screen_id = inventory_location
                option_index = 0
                action = 0
                flags["inventory_open"] = False

                action_log["action"] = "ESC"
            
            elif event.key == pygame.K_ESCAPE and running and flags["spell_book_open"]:
                screen_id = inventory_location
                option_index = 0
                action = 0
                flags["spell_book_open"] = False
                action_log["action"] = "ESC"
            
            elif event.key == pygame.K_ESCAPE and running and (screen_id == "buy" or screen_id == "sell"):
                if(screen_id == "buy"):
                    flags["buy_merchant_open"] = False
                    flags["buy_store_open"] = False
                else:
                    flags["sell_open"] = False
                option_index = 0
                screen_id = previous_store_screen
                action_log["action"] = "ESC"
            
            elif event.key == pygame.K_ESCAPE and running and screen_id == "move":
                screen_id = location
                action_log["action"] = "ESC"
            
            elif event.key == pygame.K_SPACE:
                running = True
                action_log["action"] = "SPACE"
            
            elif event.key == pygame.K_RETURN and running and screen_id == "inventory":
                processingInventoryEvents(option_index)
                action_log["action"] = "ENTER"
            
            elif event.key == pygame.K_RETURN and running and (screen_id == "buy" or screen_id == "sell"):
                processingStoreEvents(screen_id, screens, state, inventory, spells, current_store, items_sell_prices, option_index)
                action_log["action"] = "ENTER"
                
            elif event.key == pygame.K_1:
                action = 1
                print("Key 1 pressed")
                action_log["action"] = "KEY_1"
            elif event.key == pygame.K_2:
                action = 2
                print("Key 2 pressed")
                action_log["action"] = "KEY_2"
            elif event.key == pygame.K_3:
                action = 3
                print("Key 3 pressed")
                action_log["action"] = "KEY_3"
            elif event.key == pygame.K_4:
                action = 4
                print("Key 4 pressed")
                action_log["action"] = "KEY_4"
            elif event.key == pygame.K_5:
                action = 5
                print("Key 5 pressed")
                action_log["action"] = "KEY_5"
            elif event.key == pygame.K_6:
                action = 6
                print("Key 6 pressed")
                action_log["action"] = "KEY_6"
            elif event.key == pygame.K_7:
                action = 7
                print("Key 7 pressed")
                action_log["action"] = "KEY_7"
            elif event.key == pygame.K_8:
                action = 8
                print("Key 8 pressed")
                action_log["action"] = "KEY_8"
            elif event.key == pygame.K_9:
                action = 9
                print("Key 9 pressed")
                action_log["action"] = "KEY_9"
            elif event.key == pygame.K_m and running and (screen_id == "village" or screen_id == "store" or
                                            screen_id == "forest" or screen_id == "swamps_path"):
                location = screen_id
                screen_id = "move"
                action_log["action"] = "KEY_M"
            
            elif event.key == pygame.K_m and screen_id == "hunter_sells":
                screen_id = "forest"
                action_log["action"] = "KEY_M"
            
            elif event.key == pygame.K_m and running and screen_id == "shadow_peaks_path":
                screen_id = "forest"
                action_log["action"] = "KEY_M"

            elif event.key == pygame.K_i and running and not flags["inventory_open"] and flags["allow_to_open_inventory"]:
                inventory_location = screen_id
                screen_id = "inventory"
                tip_text = "To close an inventory press ' Esc '" 
                flags["inventory_open"] = True
                flags["allow_to_open_inventory"] = False
                action_log["action"] = "KEY_I"

            elif event.key == pygame.K_s and running and not flags["spell_book_open"] and screen_id != "inventory":
                inventory_location = screen_id
                screen_id = "current_spells"
                tip_text = "To close an spellbook press ' Esc '" 
                flags["spell_book_open"] = True
                action_log["action"] = "KEY_S"
            
            elif event.key == pygame.K_UP and running:
                if(option_index > 0):
                    option_index -= 1
                print("up " + str(option_index) + "\n")   
                action_log["action"] = "KEY_UP"
            
            elif event.key == pygame.K_DOWN and running:
                if(option_index < len(inventory) - 1) and flags["inventory_open"]:
                    option_index += 1 
                
                if(option_index < len(spells) - 1) and flags["spell_book_open"]:
                    option_index += 1 
                
                if(option_index < len(store) - 1) and flags["buy_store_open"]:
                    option_index += 1

                if(option_index < len(merchant_store) - 1) and flags["buy_merchant_open"]:
                    option_index += 1
                
                if(option_index < len(screens["sell"]["options"]) - 1) and flags["sell_open"]:
                    option_index += 1


                print("down " + str(option_index) + "\n")   
                action_log["action"] = "KEY_DOWN"

    # TestLOG
    print("2 Step" + action_log["action"])

    if running:
        # Update game state
        screen_id = check_mana_health_gold(screen_id)
        # Global parameters that passes into fighting functions
        parameters = {"state": state, 
                "inventory": inventory,
                "screens": screens,
                "screen_id": screen_id,
                "flags": flags,
                "action": action,
                "location_to_move": location_to_move
                }
        # Blit the background image onto the screen
        screen.blit(background, (0, 0))
        
        # TestLOG
        print("3 Step" + action_log["action"])

        processingEvents()
        action = changeScreen(action)
        if screen_id in screens:
            watch_screen = screens[screen_id]
        

        # Draw to the screen
        showScreen(screen, screen_font, options_font, tip_text)
        showHealth()
        showInventory() 
        showSpells()
        if flags["inventory_open"]:
            showingDescriptionForItemsAndSpells(option_index, inventory)
        elif flags["spell_book_open"]:
            showingDescriptionForItemsAndSpells(option_index, spells)
    else:
        screen.blit(background, (0, 0))
    
    # TestLOG
    print("4 Step" + action_log["action"])

    pygame.display.flip()
    # Add drawing code here

    # Update the display
    pygame.display.update()

    action_log["number"] += 1
    action_log["screen"] = screen_id
    action_log["time"] = time.time() - start_time
    line = "{}. screen: {}, action: {}, time: {:.2f}".format(action_log["number"], action_log["screen"], action_log["action"], action_log["time"])
    file.write(line + '\n')
    
    # TestLOG
    print("5 Step" + action_log["action"])

    # Control the frame rate
    clock.tick(frame_rate)
    # TestLOG
    print("6 Step" + action_log["action"])

end_time = time.time()
total_time = end_time - start_time
print("Total program time:", total_time, "seconds")
file.close()

# Clean up
pygame.quit()
