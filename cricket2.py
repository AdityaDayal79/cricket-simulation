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

    def play_innings(self, batters, opposing_bowling_skill, target_score=None):
        scores = {}
        wickets = 0
        striker_index = 0
        non_striker_index = 1
        total_score = 0

        for ball in range(6):  # Each innings consists of 6 balls
            if wickets >= 2:  # Stop if 2 wickets have been lost
                break
            
            input("Press Enter to simulate the next ball...")
            striker = batters[striker_index]
            run = random.randint(0, 6) if random.random() < (striker.batting_skill - opposing_bowling_skill) / 100 else random.randint(0, 3)

            # Random chance to lose a wicket
            if random.random() < 0.1:  # 10% chance to lose a wicket on any ball
                wickets += 1
                print(f"{striker.name} is out!")
                striker_index = non_striker_index  # The non-striker becomes the new striker
                non_striker_index = wickets + 1  # Move to the next available batter
                if non_striker_index >= len(batters):  # No more batters available
                    break
                continue  # Skip score update if batter is out
            
            # Add runs to striker's score
            scores[striker.name] = scores.get(striker.name, 0) + run  # Halve the runs scored
            total_score += run   # Update total score
            print(f"{striker.name} scored: {run} runs (Total: {total_score}/{wickets})")
            
            # Rotate strike if odd number of runs scored
            if (run) % 2 != 0:
                striker_index, non_striker_index = non_striker_index, striker_index

            # Check if Team 2 has surpassed Team 1’s score
            if target_score is not None and total_score > target_score:
                print(f"{self.team2_name} has surpassed {self.team1_name}'s score and wins the game!")
                return scores, wickets, total_score  # Early end of innings if Team 2 wins

        return scores, wickets, total_score

    def play_game(self):
        # Team 1 innings
        print(f"{self.team1_name} is batting first!")
        team1_batters = [self.team1_players[0], self.team1_players[1], self.team1_players[2]]
        team1_scores, self.team1_wickets, self.team1_score = self.play_innings(
            team1_batters, self.team2_players[3].bowling_skill
        )
        
        print(f"{self.team1_name} total score: {self.team1_score}/{self.team1_wickets} runs/wickets\n")

        # Team 2 innings
        print(f"{self.team2_name} is batting now!")
        team2_batters = [self.team2_players[0], self.team2_players[1], self.team2_players[2]]
        team2_scores, self.team2_wickets, self.team2_score = self.play_innings(
            team2_batters, self.team1_players[3].bowling_skill, target_score=self.team1_score
        )

        if self.team2_score <= self.team1_score:
            # If the loop completes without surpassing Team 1, we check for the winner
            print(f"{self.team2_name} total score: {self.team2_score}/{self.team2_wickets} runs/wickets")
            if self.team1_score > self.team2_score:
                print(f"{self.team1_name} wins by {self.team1_score - self.team2_score} runs!")
            elif self.team2_score > self.team1_score:
                print(f"{self.team2_name} wins by {self.team2_score - self.team1_score} runs!")
            else:
                print("The match is a draw!")

# Create players for each team
team1_players = [
    Player("Player1", 80, 0),
    Player("Player2", 70, 0),
    Player("Player3", 75, 0),
    Player("Bowler1", 0, 90)
]

team2_players = [
    Player("PlayerA", 65, 0),
    Player("PlayerB", 60, 0),
    Player("PlayerC", 68, 0),
    Player("BowlerA", 0, 95)
]

# Initialize and play the game
game = CricketGame("India", "Australia", team1_players, team2_players)
game.play_game()





