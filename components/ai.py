from __future__ import annotations
from abc import abstractmethod
import random
from typing import List, Optional, Tuple, TYPE_CHECKING

import numpy as np
import tcod
import color

from actions import Action, BumpAction, MeleeAction, MovementAction, PickupAction, WaitAction
from entity import Actor

if TYPE_CHECKING:
    from entity import Actor

class BaseAI(Action):
    entity: Actor

    @abstractmethod
    def perform(self) -> None:
        pass

    def get_path_to(self, dest_x: int, dest_y: int) -> List[Tuple[int, int]]:
        # calculates path to target position or returns empty list if no valid path
        cost = np.array(self.entity.gamemap.tiles['walkable'], dtype = np.int8)
        x, y = np.where(self.engine.game_map.tiles['walkable'])

        for entity in self.entity.gamemap.entities:
            if entity.blocks_movement and cost[entity.x, entity.y]:
                # add to the cost of blocked position
                # lower means more entity crowding behind each other
                # higher incites them to take longer paths to surround player
                cost[entity.x, entity.y] += 10

        for i in range(len(x)):
            # if self.engine.game_map.tiles[x[i], y[i]]['walkable'] is True:
            cost[x[i], y[i]] += self.engine.game_map.tiles[x[i], y[i]]['weight']
                
        # create graph from the cost array (flat weight for all but active entities)
        # pass it to pathfinder
        graph = tcod.path.SimpleGraph(cost = cost, cardinal = 2, diagonal = 3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((self.entity.x, self.entity.y))

        # calculate path to the destination and remove starting point
        path: List[List[int]] = pathfinder.path_to((dest_x, dest_y))[1:].tolist()

        # convert from List[List] to List[Tuple]
        return [(index[0], index[1]) for index in path]
    
    def wander_around(self):
        # if there is no target to path to, entity will wander around randomly
        # also can bump into entities attacking them
        direction_x, direction_y = random.choice(
            [
                (-1, -1), # northwest
                (0, -1), # north
                (1, -1), # northeast
                (-1, 0), # west
                (1, 0), # east
                (-1, 1), # southwest
                (0, 1), # south
                (1, 1), # southeast
            ]
        )

        return BumpAction(self.entity, direction_x, direction_y).perform()
    
class Dummy(BaseAI):
    def __init__(self, entity: Actor) -> None:
        super().__init__(entity)

    def perform(self) -> None:
        return WaitAction(self.entity).perform()

class SimpleHostileEnemy(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path:  List[Tuple[int, int]] = []

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y

        distance = max(abs(dx), abs(dy))

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            if distance <= 1:
                return MeleeAction(self.entity, dx, dy).perform()

            self.path = self.get_path_to(target.x, target.y)

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(
                self.entity, dest_x - self.entity.x, dest_y - self.entity.y
            ).perform()

        self.wander_around()

        return WaitAction(self.entity).perform()

class SpellCastingEnemy(BaseAI):
    def __init__(self, entity: Actor) -> None:
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []
        self.spell_damage = 1
        self.spell_uses = 3
    
    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y

        distance = max(abs(dx), abs(dy))

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            if distance == 1:
                return MeleeAction(self.entity, dx, dy).perform()
            elif 1 < distance < 4 and self.spell_uses > 0:
                self.engine.message_log.add_message(
                    f'{self.entity.name} hurls projectile at {target.name} for {self.spell_damage} damage'
                )
                target.fighter.take_damage(self.spell_damage)
                self.spell_uses -= 1
            else:
                self.path = self.get_path_to(target.x, target.y)

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(self.entity, dest_x - self.entity.x, dest_y - self.entity.y).perform()

class GreedyEnemy(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path:  List[Tuple[int, int]] = []

    def perform(self) -> None:
        target = next(self.engine.game_map.items, None)

        # selects target from the items list, selects the first item in list
        # if there is one the goblin with path towards it and bump into things (in theory)
        # which should make him attack entities he stumbles into while going to pick item
        # when he is on top of the item he picks it up
        # currently each goblin enemy is omnipotent and always knows location of each item on given floor
        if target is not None and len(self.entity.inventory.items) < self.entity.inventory.capacity:
            dx = target.x - self.entity.x
            dy = target.y - self.entity.y

            distance = max(abs(dx), abs(dy))

            # path towards item only if it's in actors field of view
            # hopefully :v
            # if self.engine.game_map.visible[target.x, target.y]:
            if distance <= 0:
                return PickupAction(self.entity).perform()
            elif 1 < distance < 10:
                self.path = self.get_path_to(target.x, target.y)
            elif distance > 10:
                target = next(self.engine.game_map.items, None)
            else:
                print(f'nothing to target')
                self.wander_around()
                

            if self.path:
                dest_x, dest_y = self.path.pop(0)
                return BumpAction(
                    self.entity, dest_x - self.entity.x, dest_y - self.entity.y
                ).perform()
            else:
                self.wander_around()

        self.wander_around()

class ConfusedEnemy(BaseAI):
    # confused actor will stumble around for given number of turns, then return to normal
    # if it stumbles into another actor, it will attack
    def __init__(self, entity: Actor, previous_ai: Optional[BaseAI], turns_remaining: int):
        super().__init__(entity)

        self.previous_ai = previous_ai
        self.turns_remaining = turns_remaining

    def perform(self) -> None:
        # return to previous ai when the effect ends
        if self.turns_remaining <= 0:
            self.engine.message_log.add_message(
                f'The {self.entity.name} is no longer confused'
            )
            self.entity.ai = self.previous_ai
        else:
            # pick random direction
            direction_x, direction_y = random.choice(
                [
                    (-1, -1), # northwest
                    (0, -1), # north
                    (1, -1), # northeast
                    (-1, 0), # west
                    (1, 0), # east
                    (-1, 1), # southwest
                    (0, 1), # south
                    (1, 1), # southeast
                ]
            )

            self.turns_remaining -= 1

            return BumpAction(self.entity, direction_x, direction_y).perform()

class MimicHostileEnemy(BaseAI):
    # we grab on init original position of the entity
    # and if we showed message in log
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path:  List[Tuple[int, int]] = []
        self.message = False
        self.origin_x = 0
        self.origin_y = 0

    def get_origin_pos(self):
        self.origin_x = self.entity.x
        self.origin_y = self.entity.y

    def perform(self) -> None:
        self.get_origin_pos()
        # if message wasn't shown in log
        # check if the entity that is mimic was:
        # a) damaged
        # b) moved from original position
        # if any one of those is true, change appearance of the entity
        # to mimic and alter it's stats
        # change the message as added so we don't loop over that part again in future
        # which is super scuffed and hacked way of handling :)
        if not self.message:
            if self.entity.fighter.hp < self.entity.fighter.max_hp or self.entity.x != self.origin_x or self.entity.y != self.origin_y:
                self.entity.char = 'M'
                self.entity.color = color.anb_red
                self.entity.name = 'Mimic'
                self.entity.fighter.base_defense = 2
                self.entity.fighter.base_power = 4
                # self.entity.ai = HostileEnemy
                self.engine.message_log.add_message(
                    f'The {self.entity.name} reveals it\'s disguise'
                )
                self.message = True

        # if the message was added to log proceed as if it was normal HostileEnemy
        # simply changing AI for whatever reason bricks every AI driven Actor ¯\_(ツ)_/¯
        if self.message:
            self.entity.ai = SimpleHostileEnemy(self.entity)
        else:
            return WaitAction(self.entity).perform()


# class TickingEntity(BaseAI):
#     def __init__(self, entity: Actor):
#         super().__init__(entity)

#     def perform(self) -> None:
#         target_xy = self.entity.x, self.entity.y
#         print(f'Target xy: {target_xy}')
#         if self.entity.fighter.hp <= 0:
#             self.entity.ai = None
#         else:
#             for actor in set(self.engine.game_map.actors) - {self.entity}:
#                 if actor.distance(*target_xy) <= 3:
#                     self.engine.message_log.add_message(
#                         f'The {actor.name} coughs in toxic gas, taking {self.entity.fighter.power} damage'
#                     )
#                     actor.fighter.take_damage(self.entity.fighter.power)
#             self.entity.fighter.hp -= 1