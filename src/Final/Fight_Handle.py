import time
import threading
import src.Common_general_functionalities.common_strings as cs
from src.Common_general_functionalities import Flexible_Attributes as fa
from src.Characters.Main_Character import MainCharacter
from src.Characters.Good_Character import GoodCharacter
from src.Characters.Regular_Enemies import Orc
from src.Characters.Boss_Enemy import Boss
from src.Characters.Bad_Character import BadCharacter


class Fight:

    """
    This object is created at the beginning of a fight. Everytime the main player hits, it will call the method
    player_is_hitting, and every time the enemy hits, it'll call the method enemy_is_hitting.
    This class shall continue until the method fight_ongoing returns False.
    In addition to getting the character's in a fight, this class will also have the option of printing the sound that
    the armor is making when used.
    The last input attributes are optional to have the additional good character's that are helping the main character.
    """

    def __init__(self, main_character, enemy, print_sound=True, *additional_good_characters):
        if not (isinstance(main_character, MainCharacter) and isinstance(enemy, (Orc, Boss, BadCharacter))):
            raise AttributeError("In a fight the characters fighting must consist of main character and an enemy "
                                 "that's either Orc or Boss.")
        if len(additional_good_characters) and not all(isinstance(c, GoodCharacter) for c in additional_good_characters):
            raise AttributeError("All helping characters must be from type GoodCharacter.")
        if type(print_sound) != bool:
            raise TypeError("Sound specification must be a boolean type.")
        if not (main_character.alive and enemy.alive and all(c.alive for c in additional_good_characters)):
            raise AttributeError("Some or all the input characters are not alive!")
        self.main_character = main_character
        self.enemy = enemy
        self.print_sound = print_sound
        a_g = list(additional_good_characters)
        id_ag = [id(i) for i in a_g]
        if len(id_ag) != len(set(id_ag)):
            a_g = [GoodCharacter(i.life, i.undercover, i.weapon, i.shield) for i in a_g]
        self.additional_good_characters = a_g
        del additional_good_characters, a_g, id_ag

    def player_is_hitting(self):
        """
        Updates the enemy's life after the main character and all the additional helper characters hit it.
        For each character that hits the enemy, there is a check whether the hit
        """
        if self.main_character.energy == 0:
            print(cs.drained_character)
            return
        player_speed, player_strength, armor_efficiency = self.main_character.attack()
        enemy_speed, enemy_shield_strength = self.enemy.defend()
        if player_speed >= enemy_speed:
            self.enemy.life = float(player_strength*armor_efficiency)
            if self.print_sound:
                print(self.main_character.weapon.sound())
        else:
            self.enemy.life = float(max(1, enemy_shield_strength - player_strength * armor_efficiency))
            self.main_character.energy = (False, 1) # Indicating to decline the energy specifically for offence action
            # Currently, armor's efficiency doesn't decline every time it's used
            # self.players_character.armor_efficiency_update(0.99)
            if self.print_sound:
                print(self.main_character.weapon.sound())
                print(self.enemy.shield.sound())
        for c in self.additional_good_characters:
            player_speed, player_strength, armor_efficiency = c.attack()
            if player_speed >= enemy_speed:
                self.enemy.life = float(player_strength * armor_efficiency)
                if self.print_sound:
                    print(c.weapon.sound())
            else:
                self.enemy.life = float(max(1, enemy_shield_strength - player_strength * armor_efficiency))
                c.energy = (False, 1)
                if self.print_sound:
                    print(c.weapon.sound())
                    print(self.enemy.shield.sound())
        print("Enemy has {!r} life left!".format(self.enemy.life))
        if not self.enemy.alive:
            print(cs.enemy_defeated)
            return True
        else:
            return False

    def enemy_is_hitting(self):
        if self.main_character.energy == 0:
            print(cs.drained_character)
        player_speed, player_strength, armor_efficiency = self.main_character.defend()
        enemy_speed, enemy_strength = self.enemy.attack()
        if player_speed < enemy_speed:
            self.main_character.life = float(enemy_strength)
            if self.print_sound:
                print(self.enemy.weapon.sound())
        else:
            defended = self.countdown(int((player_speed-enemy_speed)*fa.speed_factor)+1)
            if defended:
                self.main_character.life = float(max(1, enemy_strength - player_strength))
                self.main_character.energy = (False, 0)  # Indicating to decline the energy specifically for defence action
                # Currently, armor's efficiency doesn't decline every time it's used
                # self.players_character.armor_efficiency_update(0.99)
                if self.print_sound:
                    print(self.enemy.weapon.sound())
                    print(self.main_character.shield.sound())
            else:
                self.main_character.life = float(enemy_strength)
                if self.print_sound:
                    print(self.enemy.weapon.sound())
        additional_characters_left = []
        for c in self.additional_good_characters:
            player_speed, player_strength, armor_efficiency = c.defend()
            if player_speed < enemy_speed:
                c.life = float(enemy_strength)
                if self.print_sound:
                    print(self.enemy.weapon.sound())
            else:
                c.life = float(max(1, enemy_strength - player_strength * armor_efficiency))
                c.energy = (False, 0)
                if self.print_sound:
                    print(self.enemy.weapon.sound())
                    print(c.shield.sound())
            if c.alive:
                additional_characters_left.append(c)
        self.additional_good_characters = additional_characters_left
        if not self.main_character.alive:
            print(cs.you_lose)
            print(cs.game_over)
            return False
        else:
            return True

    def fight_ongoing(self):
        """
        This method returns True if the fight is still ongoing (i.e. both enemy and main character are still alive),
        False otherwise.
        """
        if self.main_character.alive and self.enemy.alive:
            return True
        else:
            return False

    def update_players(self, main_char):
        """
        In specific actions we need to change the main character that's fighting, and this method is built to do so.
        """
        self.main_character = main_char
        # self.additional_good_characters = list(help_char) THIS MEANS THAT CURRENTLY THERE'S NO OPTION TO USE THE AIDS
        #                                                   ON THE HELPING CHARACTERS

    @staticmethod
    def countdown(t):
        fail = False

        def time_expired():
            fail = True

        time = threading.Timer(t, time_expired)
        time.start()
        prompt = input("You have {} seconds to defend from enemy's attack.\n".format(str(t))).upper()

        if prompt in cs.defend_actions and not fail:
            time.cancel()
            return True
        else:
            print(cs.didnt_defend)
            return False
