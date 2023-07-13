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
        self.main_character = main_character
        self.enemy = enemy
        self.print_sound = print_sound
        self.additional_good_characters = list(additional_good_characters)

    def player_is_hitting(self):
        if self.main_character.energy == 0:
            print("The character has no energy to attack or defend.")
            return
        player_speed, player_strength, armor_efficiency = self.main_character.attack()
        enemy_speed, enemy_shield_strength = self.enemy.defend()
        if player_speed >= enemy_speed:
            self.enemy.life = player_strength*armor_efficiency
            if self.print_sound:
                print(self.main_character.weapon.sound())
        else:
            self.enemy.life = max(1, enemy_shield_strength - player_strength * armor_efficiency)
            self.main_character.energy = (False, 1) # Indicating to decline the energy specifically for offence action
            # Currently, armor's efficiency doesn't decline every time it's used
            # self.players_character.armor_efficiency_update(0.99)
            if self.print_sound:
                print(self.main_character.weapon.sound())
                print(self.enemy.shield.sound())
        for c in self.additional_good_characters:
            player_speed, player_strength, armor_efficiency = c.attack()
            if player_speed >= enemy_speed:
                self.enemy.life = player_strength * armor_efficiency
                if self.print_sound:
                    print(c.weapon.sound())
            else:
                self.enemy.life = max(1, enemy_shield_strength - player_strength * armor_efficiency)
                c.energy = (False, 1)
                if self.print_sound:
                    print(c.weapon.sound())
                    print(self.enemy.shield.sound())
        print("Enemy has {!r} life left!".format(self.enemy.life))
        if not self.enemy.alive:
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
            if self.print_sound:
                print(self.enemy.weapon.sound())
        else:
            self.main_character.life = max(1, player_strength * armor_efficiency - enemy_strength)
            self.main_character.energy = (False, 0)  # Indicating to decline the energy specifically for defence action
            # Currently, armor's efficiency doesn't decline every time it's used
            # self.players_character.armor_efficiency_update(0.99)
            if self.print_sound:
                print(self.enemy.weapon.sound())
                print(self.main_character.shield.sound())
        additional_characters_left = []
        for c in self.additional_good_characters:
            player_speed, player_strength = c.defend()
            if player_speed < enemy_speed:
                c.life = enemy_strength
                if self.print_sound:
                    print(self.enemy.weapon.sound())
            else:
                c.life = max(1, player_strength * armor_efficiency - enemy_strength)
                c.energy = (False, 0)
                if self.print_sound:
                    print(self.enemy.weapon.sound())
                    print(c.shield.sound())
            if c.alive:
                additional_characters_left.append(c)
        self.additional_good_characters = additional_characters_left
        if not self.main_character.alive:
            print("You are defeated!")
            print("GAME OVER!")
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
        self.main_character = main_char
        # self.additional_good_characters = list(help_char) THIS MEANS THAT CURRENTLY THERE'S NO OPTION TO USE THE AIDS
        #                                                   ON THE HELPING CHARACTERS
