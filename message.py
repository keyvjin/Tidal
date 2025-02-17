#!/usr/bin/env python3
print("Welcome to...... ")
print("████████╗ ██╗ ██████╗░ ░█████╗░ ██╗░░░░░")
print("╚══██╔══╝ ██║ ██╔══██╗ ██╔══██╗ ██║░░░░░")
print("░░░██║░░░ ██║ ██║░░██║ ███████║ ██║░░░░░")
print("░░░██║░░░ ██║ ██║░░██║ ██╔══██║ ██║░░░░░")
print("░░░██║░░░ ██║ ██████╔╝ ██║░░██║ ███████╗")
print("░░░╚═╝░░░ ╚═╝ ╚═════╝░ ╚═╝░░╚═╝ ╚══════╝")
print("A Mock Trading x Trivia game for all the family to enjoy")

import time

class QuantGame:
    def __init__(self):
        self.teams = []
        self.market_maker = None
        self.market_range = float('inf')
        self.team_values = {}  # Dictionary to track each team's gain/loss for the round

    def load_values(self, filepath):
        with open(filepath, 'r') as file:
            data = [line.strip().split(",") for line in file.readlines()]
        return [(int(entry[0]), entry[1], int(entry[2])) for entry in data]

    def start_game(self, value_description, value):
        print(f"\nToday, we are trading {value_description}.")
        self.get_team_count()
        self.run_auction()
        self.market_phase(value)
        self.final_calculation(value_description, value)

    def get_team_count(self):
        num_teams = int(input("Enter the number of teams playing: "))
        for i in range(num_teams):
            team_name = f"Team {i + 1}"
            self.teams.append(team_name)
            self.team_values[team_name] = 0  # Initialize each team's value for the round
        print(f"{len(self.teams)} teams registered.")

    def run_auction(self):
        active_teams = self.teams[:]
        previous_bidder = None

        while len(active_teams) > 1:
            print("\nAuction Phase: Teams bid for a smaller range or concede.")
            for team in active_teams[:]:  # Copy to avoid modification during iteration
                if team == previous_bidder:
                    continue

                action = input(f"{team}, enter your range bid (number) or 'c' to concede: ").strip().lower()
                if action == "c":
                    active_teams.remove(team)
                    print(f"{team} has conceded.")
                else:
                    try:
                        team_range = int(action)
                        if team_range < self.market_range:
                            self.market_range = team_range
                            self.market_maker = team
                            previous_bidder = team
                            print(f"{team} is now the market maker with a range of {self.market_range}.")
                        else:
                            print(f"{team}'s bid is too high and does not change the market maker.")
                    except ValueError:
                        print("Invalid input. Please enter a number for the range or 'c' to concede.")

        print(f"\n{self.market_maker} wins the auction with a range of {self.market_range}.")

    def market_phase(self, actual_value):
        print("\nMarket Phase: Market maker sets buying price within the range.")
        buying_price = int(input(f"{self.market_maker}, enter the market buying price (Higher Value): "))
        selling_price = buying_price - self.market_range
        
        print(f"\n{self.market_maker} sets a market from {selling_price} to {buying_price}.")
        
        for team in self.teams:
            if team != self.market_maker:
                while True:
                    choice = input(f"{team}, do you want to buy or sell at {buying_price} / {selling_price}? (b/s): ").strip().lower()
                    if choice in ["b", "s"]:
                        break
                    else:
                        print("Invalid input. Please enter 'b' for buy or 's' for sell.")

                if choice == "b":
                    player_value = self.calculate_value(actual_value, buying_price, "buy")
                elif choice == "s":
                    player_value = self.calculate_value(actual_value, selling_price, "sell")

                # Store player's result
                self.team_values[team] += player_value

                # Accumulate the inverse for the market maker
                self.team_values[self.market_maker] -= player_value

    def calculate_value(self, actual_value, price, action):
        if action == "sell":
            return price - actual_value
        elif action == "buy":
            return actual_value - price

    def final_calculation(self, value_description, value):
        print(f"\nRound Over! The actual value of {value_description} was {value}.")
        print("\nFinal values for each team:")
        for team, total_value in self.team_values.items():
            print(f"{team}: {total_value}")
        print("\nStarting a new round...\n")
        
        # Reset team values and market range for the next game
        self.team_values = {team: 0 for team in self.teams}
        self.market_range = float('inf')
        time.sleep(3)

# Define the filepath and load values from the file
filepath = 'Tidal.txt'
game = QuantGame()
values_data = game.load_values(filepath)

# Run the game indefinitely, iterating through the values in Tidal.txt
while True:
    for _, value_description, value in values_data:
        game.start_game(value_description, value)
