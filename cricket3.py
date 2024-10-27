import random

class Player:
    def __init__(self, name, batting_skill, bowling_skill):
        self.name = name
        self.batting_skill = batting_skill
        self.bowling_skill = bowling_skill

class CricketGame:
    def __init__(self, team1_name, team2_name, team1_players, team2_players):
        self.team1_name = team1_name
        self.team2_name = team2_name
        self.team1_players = team1_players
        self.team2_players = team2_players
        self.team1_score = 0
        self.team2_score = 0
        self.team1_wickets = 0
        self.team2_wickets = 0

    def play_innings(self, batting_team_name, batters, bowlers, target_score=None):
        scores = {}
        wickets = 0
        striker_index = 0
        non_striker_index = 1
        total_score = 0
        overs = 20  # Each innings consists of 20 overs
        balls_per_over = 6
        
        # Bowling rotation among bowlers (7 to 11)
        bowler_index = 0
        bowler_overs = {bowler.name: 0 for bowler in bowlers}

        for over in range(overs):
            if wickets >= 10:  # Stop if 10 wickets have been lost
                break

            for ball in range(balls_per_over):
                # Select current bowler based on rotation and overs limit
                current_bowler = bowlers[bowler_index]
                if bowler_overs[current_bowler.name] >= 4:
                    bowler_index = (bowler_index + 1) % len(bowlers)
                    current_bowler = bowlers[bowler_index]

                input("Press Enter to simulate the next ball...")
                striker = batters[striker_index]
                run = random.randint(0, 6) if random.random() < (striker.batting_skill - current_bowler.bowling_skill) / 100 else random.randint(0, 3)

                # Random chance to lose a wicket
                if random.random() < 0.1:  # 10% chance to lose a wicket on any ball
                    wickets += 1
                    print(f"{striker.name} is out!")
                    striker_index = non_striker_index  # Non-striker becomes new striker
                    non_striker_index = wickets + 1  # Move to the next batter
                    if non_striker_index >= len(batters):  # No more batters available
                        break
                    continue  # Skip score update if batter is out
                
                # Add runs to striker's score
                scores[striker.name] = scores.get(striker.name, 0) + run
                total_score += run
                print(f"{striker.name} scored: {run} runs (Total: {total_score}/{wickets})")

                # Rotate strike if odd number of runs scored
                if (run % 2) != 0:
                    striker_index, non_striker_index = non_striker_index, striker_index

                # Check if Team 2 has surpassed Team 1’s score
                if target_score is not None and total_score > target_score:
                    print(f"{self.team2_name} has surpassed {self.team1_name}'s score and wins the game!")
                    return scores, wickets, total_score  # Early end of innings if Team 2 wins

                # Last ball of over logic
                if ball == balls_per_over - 1:  # Last ball of the over
                    if run == 0 or run % 2 == 0:
                        striker_index, non_striker_index = non_striker_index, striker_index
            
            # End of over display
            print(f"End of Over {over + 1}: {batting_team_name} - {total_score}/{wickets} (runs/wickets)")

            # Update bowler’s overs and rotate if necessary
            bowler_overs[current_bowler.name] += 1
            bowler_index = (bowler_index + 1) % len(bowlers)

        return scores, wickets, total_score

    def play_game(self):
        # Randomize which team bats first
        toss_winner = random.choice([self.team1_name, self.team2_name])
        
        if toss_winner == self.team1_name:
            print(f"{self.team1_name} won the toss and chose to bat first!")
            batting_team, bowling_team = (self.team1_name, self.team2_name)
            team1_batters = self.team1_players[:11]
            team1_bowlers = self.team2_players[6:11]
            team1_scores, self.team1_wickets, self.team1_score = self.play_innings(
                self.team1_name, team1_batters, team1_bowlers
            )
            print(f"{self.team1_name} total score: {self.team1_score}/{self.team1_wickets} runs/wickets\n")

            # Team 2 innings
            print(f"{self.team2_name} is batting now!")
            team2_batters = self.team2_players[:11]
            team2_bowlers = self.team1_players[6:11]
            team2_scores, self.team2_wickets, self.team2_score = self.play_innings(
                self.team2_name, team2_batters, team2_bowlers, target_score=self.team1_score
            )

        else:
            print(f"{self.team2_name} won the toss and chose to bat first!")
            batting_team, bowling_team = (self.team2_name, self.team1_name)
            team2_batters = self.team2_players[:11]
            team2_bowlers = self.team1_players[6:11]
            team2_scores, self.team2_wickets, self.team2_score = self.play_innings(
                self.team2_name, team2_batters, team2_bowlers
            )
            print(f"{self.team2_name} total score: {self.team2_score}/{self.team2_wickets} runs/wickets\n")

            # Team 1 innings
            print(f"{self.team1_name} is batting now!")
            team1_batters = self.team1_players[:11]
            team1_bowlers = self.team2_players[6:11]
            team1_scores, self.team1_wickets, self.team1_score = self.play_innings(
                self.team1_name, team1_batters, team1_bowlers, target_score=self.team2_score
            )

        # Display the final result
        if self.team2_score <= self.team1_score:
            print(f"{self.team2_name} total score: {self.team2_score}/{self.team2_wickets} runs/wickets")
            if self.team1_score > self.team2_score:
                print(f"{self.team1_name} wins by {self.team1_score - self.team2_score} runs!")
            elif self.team2_score > self.team1_score:
                print(f"{self.team2_name} wins by {self.team2_score - self.team1_score} runs!")
            else:
                print("The match is a draw!")

# Create players for each team
team1_players = [
    Player("Player1", 80, 0), Player("Player2", 70, 0), Player("Player3", 75, 0),
    Player("Player4", 68, 0), Player("Player5", 72, 0), Player("Player6", 60, 0),
    Player("Bowler1", 30, 90), Player("Bowler2", 32, 85), Player("Bowler3", 28, 88),
    Player("Bowler4", 35, 87), Player("Bowler5", 30, 92)
]

team2_players = [
    Player("PlayerA", 65, 0), Player("PlayerB", 60, 0), Player("PlayerC", 68, 0),
    Player("PlayerD", 70, 0), Player("PlayerE", 55, 0), Player("PlayerF", 62, 0),
    Player("BowlerA", 25, 95), Player("BowlerB", 26, 90), Player("BowlerC", 27, 89),
    Player("BowlerD", 30, 86), Player("BowlerE", 33, 92)
]

# Initialize and play the game
game = CricketGame("India", "Australia", team1_players, team2_players)
game.play_game()


