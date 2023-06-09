import src.Common_general_functionalities.common_strings as cs


class Fight:

    def __init__(self, main_character, enemy):
        self.main_character = main_character
        self.enemy = enemy

    def player_is_hitting(self):
        if self.main_character.energy == 0:
            print("The character has no energy to attack or defend.")
            return
        player_speed, player_strength, armor_efficiency = self.main_character.attack()
        enemy_speed, enemy_strength = self.enemy.defend()
        if player_speed >= enemy_speed:
            print(player_strength)                              ##################################################
            print(armor_efficiency)
            self.enemy.life = player_strength*armor_efficiency
        else:
            self.enemy.life = max(1, enemy_strength - player_strength * armor_efficiency)
            self.main_character.energy = (False, 1)
            # self.players_character.armor_efficiency_update(0.99)
        print("Enemy has that much life left: ", self.enemy.life)
        if self.enemy.life == 0:
            print("Enemy is defeated!")
            return True
        else:
            return False

    def enemy_is_hitting(self):
        if self.main_character.energy == 0:
            print("The character has no energy to attack or defend.")
        player_speed, player_strength, armor_efficiency = self.main_character.defend()
        enemy_speed, enemy_strength = self.enemy.attack()
        if player_speed < enemy_speed:
            self.main_character.life = enemy_strength
        else:
            self.main_character.life = max(1, player_strength * armor_efficiency - enemy_strength)
            self.main_character.energy = (False, 0)
            # self.players_character.armor_efficiency_update(0.99)
        if self.main_character.life == 0:
            print("You are defeated!")
            print("GAME OVER!")
            return False
        else:
            return True


def use_aid(player, aid):
    aid_type, magnitude = aid.activate()
    if aid_type == cs.health:
        player.recharge_life(magnitude)
    elif aid_type == cs.energy:
        player.renew_energy()
    else:
        player.renew_energy()       # This is incorrect!! here we must update the weapon's/shield's strength
                                    # According to the inputs! we didn't chek the rest of the inputs.
    return player
