from __future__ import annotations

from random import randint
from components.ai import Dummy, GreedyEnemy, SimpleHostileEnemy, SpellCastingEnemy, MimicHostileEnemy
from components.fighter import Fighter
from components.equipment import Equipment
from components import consumable, equippable, interactable
from components.inventory import Inventory
from components.level import Level
from entity import Actor, Item, Object
import color

placeholder = Object(
    char = "=",
    color = color.anb_red,
    name = "OBJECT PLACEHOLDER",
    interaction = None,
)

placeholder1 = Object(
    char = "=",
    color = color.anb_red,
    name = "OBJECT NUMERO DOS",
    interaction = None,
)
placeholder2 = Object(
    char = "=",
    color = color.anb_red,
    name = "YET ANOTHER OBJECT",
    interaction = None,
)

'PLAYER AND NON HOSTILE ACTORS'
player = Actor(
    char = chr(0x263A), # string for visual representation on game map. Most ASCII symbols
    color = color.anb_white, # color of string representation format RGB(R, G, B)
    name = 'Player', # name displayed when taking actions/interacting
    ai_cls = SimpleHostileEnemy, # type of AI to use, player doesn't need it but it must be specified for all Actors
    equipment = Equipment(),
    fighter = Fighter(hp = 1000, base_defense = 100, base_power = 2), # base statistics for Actor
    inventory = Inventory(capacity = 26), # attach Inventory to actor with set size, size determines how many items actor can carry
    level = Level(level_up_base = 200),
)

dummy = Actor(
    char = 'D',
    color = color.anb_pink, # (63, 127, 63),
    name = 'Dummy',
    ai_cls = Dummy,
    equipment = Equipment(),
    fighter = Fighter(hp = 10, base_defense = 0, base_power = 3),
    inventory = Inventory(capacity = 0),
    level = Level(xp_given = 30),
)

'AI HOSTILE ACTORS'
caster = Actor(
    char = 'c',
    color = color.anb_pink, # (63, 127, 63),
    name = 'Caster',
    ai_cls = SpellCastingEnemy,
    equipment = Equipment(),
    fighter = Fighter(hp = 10, base_defense = 0, base_power = 3),
    inventory = Inventory(capacity = 0),
    level = Level(xp_given = 30),
)
orc = Actor(
    char = 'o',
    color = color.anb_light_brown, # (63, 127, 63),
    name = 'Orc',
    ai_cls = SimpleHostileEnemy,
    equipment = Equipment(),
    fighter = Fighter(hp = 10, base_defense = 0, base_power = 4),
    inventory = Inventory(capacity = 0),
    level = Level(xp_given = 30),
)
troll = Actor(
    char = 'T',
    color = color.anb_brown, # (0, 127, 0),
    name = 'Troll',
    ai_cls = SimpleHostileEnemy,
    equipment = Equipment(),
    fighter = Fighter(hp = 20, base_defense = 2, base_power = 5),
    inventory = Inventory(capacity = 0),
    level = Level(xp_given = 90),
)
goblin = Actor(
    char = 'g',
    color = color.anb_light_brown, # (0, 127, 0),
    name = 'Goblin',
    ai_cls = GreedyEnemy,
    equipment = Equipment(),
    fighter = Fighter(hp = 2, base_defense = 1, base_power = 4),
    inventory = Inventory(capacity = 2),
    level = Level(xp_given = 40),
)
# mimic_table = Actor(
#     char = '+',
#     color = color.anb_brown,
#     name = 'Table',
#     ai_cls = MimicHostileEnemy,
#     fighter = Fighter(hp = 15, defense = 2, power = 4),
#     inventory = Inventory(capacity = 0),
# )

# NON AI DESTROYABLE ACTORS
table = Actor(
    char = '+',
    color = color.anb_brown,
    name = 'Table',
    ai_cls = MimicHostileEnemy,
    equipment = Equipment(),
    fighter = Fighter(hp = 20, base_defense = 0, base_power = 0),
    inventory = Inventory(capacity = 0),
    level = Level(xp_given = 70),
)

'ITEMS'
big_health_potion = Item(
    char = '!',
    color = color.anb_light_brown,
    name = 'Health flask',
    consumable = consumable.MultiUseHealingConsumable(amount = randint(4, 10), uses = 3),
)
health_potion = Item(
    char = '!',
    color = color.anb_light_brown,
    name = 'Health potion',
    consumable = consumable.HealingConsumable(amount = randint(4, 10)),
)
lightning_scroll = Item(
    char = '~',
    color = color.anb_light_blue,
    name = 'Lightning scroll',
    consumable = consumable.LightningDamageConsumable(damage = 15, maximum_range = 5),
)
confusion_scroll = Item(
    char = '~',
    color = color.anb_purple,
    name = 'Confusion scroll',
    consumable = consumable.ConfusionConsumable(number_of_turns = 10),
)
fireball_scroll = Item(
    char = '~',
    color = color.anb_red,
    name = 'Fireball scroll',
    consumable = consumable.FireballDamageConsumable(damage = 12, radius = 3),
)
# gascloud_scroll = Item(
#     char = '~',
#     color = color.anb_green,
#     name = 'Gas cloud scroll',
#     consumable = consumable.GasDamageConsumable(damage = 12, radius = 3, turns_active = 3),
# )
bow = Item(
    char = ')',
    color = color.anb_green,
    name = 'Bow',
    consumable = consumable.MultiUseRangedConsumable(damage = 4, ammunition = 5),
)

# gas_cloud = Actor(
#     char = '8',
#     color = color.anb_green,
#     name = '',
#     ai_cls = TickingEntity,
#     fighter = Ticking(hp = 3, power = 3, radius = 3),
#     inventory = Inventory(capacity = 0),
#     level = Level(xp_given = 0)
# )

'EQUIPPABLES'
dagger = Item(
    char = '/',
    color = color.anb_brown,
    name = 'Dagger',
    equippable = equippable.Dagger()
)
sword = Item(
    char = '/',
    color = color.anb_light_brown,
    name = 'Sword',
    equippable = equippable.Sword()
)
leather_armor = Item(
    char = '[',
    color = color.anb_grey,
    name = 'Leather armor',
    equippable = equippable.LeatherArmor()
)
chain_mail = Item(
    char = '[',
    color = color.anb_white,
    name = 'Chain mail',
    equippable = equippable.ChainMail()
)
power_ring = Item(
    char = '°',
    color = color.anb_white,
    name = 'Ring of The Gorilla',
    equippable = equippable.PowerRing()
)
defense_ring = Item(
    char = '°',
    color = color.anb_white,
    name = 'Ring of The Wall',
    equippable = equippable.DefenseRing()
)
omni_ring = Item(
    char = '°',
    color = color.anb_white,
    name = 'Ring of Omni',
    equippable = equippable.OmniRing()
)