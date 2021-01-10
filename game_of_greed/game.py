from game_logic import GameLogic
from banker import Banker
import sys

class Game:
    #game_of_greed.
    """Class for Game of Greed application
    """

    def __init__(self, num_rounds=20):
        self.banker = Banker()
        self.num_rounds = num_rounds

    def play(self, roller=None):
        """Entry point for playing (or declining) a game
        Args:
            roller (function, optional): Allows passing in a custom dice roller function.
                Defaults to None.
        """
        self.round_num = 0
        self.dice_num = 6
        self._roller = roller or GameLogic.roll_dice

        print("Welcome to Game of Greed")

        print("(y)es to play or (n)o to decline")

        response = input("> ")

        if response == "y" or response == "yes":
            self.start_game()
        else:
            self.decline_game()

    def decline_game(self):
        print("OK. Maybe another time")

    def thanks_for_playing(self):
        print(f"Thanks for playing. You earned {self.banker.balance} points")
        sys.exit()

    def shelf_dice(self, selected_die):   
        score = GameLogic.calculate_score(selected_die)
        self.banker.shelf(score)
        shelved = self.banker.shelved
        dice_remaining = self.dice_num - len(selected_die)
        print(f"You have {shelved} unbanked points and {dice_remaining} dice remaining")

    def roll_the_dice(self):
        ## Roll the dice
        print("Rolling 6 dice...")
        roll = self._roller(6)
        return roll

    def roll_again(self, selected_die):
        self.banker.clear_shelf()
        dice_remaining = self.dice_num - len(selected_die)
        int(dice_remaining)
        new_roll = GameLogic.roll_dice(dice_remaining)
        self.print_roll(new_roll)
        if GameLogic.calculate_score(new_roll) == 0:
            print("You Zilched, hoe")
            self.thanks_for_playing()
        else:
            new_score = GameLogic.calculate_score(new_roll)
            self.banker.shelf(new_score)
            user_input = input("Enter dice to keep, or (q)uit:\n> ")
            if user_input == "q":
                self.thanks_for_playing()
            else:
                tuple_die = self.user_input_to_tuple(user_input)
                self.roll_again(tuple_die)
            
    
        
    def print_roll(self, roll):
        formatted_roll = ' '.join(map(str, (roll)))
        print("*** ", formatted_roll, " ***")

    def bank_points(self):
        round_score = self.banker.shelved
        self.banker.bank()
        print(f"You banked {round_score} points in round {self.round_num}")
        print(f"Total score is {self.banker.balance} points")

    def user_input_to_tuple(self, input):
        selected_die = []
        for char in input:
            if char != ' ':
                selected_die.append(int(char))
        return tuple(selected_die)

    def new_round(self):
        ## Roll the dice
        roll = self.roll_the_dice()
        self.print_roll(roll)
        #ask user for values
        user_input = input("Enter dice to keep, or (q)uit:\n> ")
        #keep playing until the user quits
        
        while user_input != "q":  

            # convert input to tuple
            tuple_die = self.user_input_to_tuple(user_input)

            # validate the input
            if not GameLogic.validate_keepers(roll, tuple_die): 
                print("Cheater!!! Or possibly made a typo...")
                self.print_roll(roll)

                # ask for input again, restart loop
                user_input = input("Enter dice to keep, or (q)uit:\n> ")
            else:   
                self.shelf_dice(tuple_die)
                bank_decision = input("(r)oll again, (b)ank your points or (q)uit:\n> ")
                if bank_decision == "r" or bank_decision == "roll":
                    self.roll_again(tuple_die) 
                if bank_decision == "b" or bank_decision == "bank":
                    self.bank_points()
                    return
                if bank_decision == "q" or bank_decision == "quit":
                    self.thanks_for_playing()      
        # if they quit, print quit message
        self.thanks_for_playing()
    
    def start_game(self):
        for i in range(1, self.num_rounds):
            self.round_num += 1
            print(f"Starting round {self.round_num}")
            self.new_round()


if __name__ == "__main__":
    game = Game()
    game.play()