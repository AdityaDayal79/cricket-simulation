import random

class Player:
    def __init__(self, name, batting_skill, bowling_skill):
        self.name = name
        self.batting_skill = batting_skill
        self.bowling_skill = bowling_skill

class CricketGame:
    def __init__(self, team1_name, team2_name, team1_players, team2_players, pitch_condition="balanced"):
        self.team1_name = team1_name
        self.team2_name = team2_name
        self.team1_players = team1_players
        self.team2_players = team2_players
        self.team1_score = 0
        self.team2_score = 0
        self.team1_wickets = 0
        self.team2_wickets = 0
        self.pitch_condition = pitch_condition
        self.batting_aggression = "normal"  # Default setting
        self.field_setting = "normal"  # Default setting

    def adjust_skills_for_pitch(self, players):
        for player in players:
            if self.pitch_condition == "batting":
                player.batting_skill += 10
            elif self.pitch_condition == "bowling":
                player.bowling_skill += 10

    def calculate_run_wicket_probability(self, batter, bowler):
        run_prob = (batter.batting_skill - bowler.bowling_skill) / 100
        wicket_prob = 0.1

        if self.batting_aggression == "defensive":
            run_prob *= 0.8
            wicket_prob *= 0.6
        elif self.batting_aggression == "aggressive":
            run_prob *= 1.2
            wicket_prob *= 1.4

        if self.field_setting == "defensive":
            run_prob *= 0.8
            wicket_prob *= 0.8
        elif self.field_setting == "aggressive":
            run_prob *= 1.2
            wicket_prob *= 1.2

        return run_prob, wicket_prob

    def toggle_batting_aggression(self, choice):
        if choice == 'd':
            self.batting_aggression = "defensive"
        elif choice == 'n':
            self.batting_aggression = "normal"
        elif choice == 'a':
            self.batting_aggression = "aggressive"
        print(f"Batting aggression set to: {self.batting_aggression}")

    def toggle_field_setting(self, choice):
        if choice == 'd':
            self.field_setting = "defensive"
        elif choice == 'n':
            self.field_setting = "normal"
        elif choice == 'a':
            self.field_setting = "aggressive"
        print(f"Field setting set to: {self.field_setting}")

    def play_innings(self, batting_team_name, batters, bowlers, target_score=None):
        scores = {}
        wickets = 0
        striker_index = 0
        non_striker_index = 1
        total_score = 0
        overs = 20
        balls_per_over = 6

        bowler_index = 0
        bowler_overs = {bowler.name: 0 for bowler in bowlers}

        for over in range(overs):
            if wickets >= 10:
                break

            # Display current settings and allow the user to change them at the start of each over
            print(f"\n--- Over {over + 1} ---")
            print(f"Current Batting Aggression: {self.batting_aggression}")
            print(f"Current Field Setting: {self.field_setting}")

            change_settings = input("Would you like to change settings? (y/n): ").strip().lower()
            if change_settings == 'y':
                batting_input = input("Enter batting aggression (d for defensive, n for normal, a for aggressive): ").strip().lower()
                if batting_input in {'d', 'n', 'a'}:
                    self.toggle_batting_aggression(batting_input)

                field_input = input("Enter field setting (d for defensive, n for normal, a for aggressive): ").strip().lower()
                if field_input in {'d', 'n', 'a'}:
                    self.toggle_field_setting(field_input)

            for ball in range(balls_per_over):
                if bowler_overs[bowlers[bowler_index].name] >= 4:
                    bowler_index = (bowler_index + 1) % len(bowlers)

                current_bowler = bowlers[bowler_index]
                striker = batters[striker_index]

                run_prob, wicket_prob = self.calculate_run_wicket_probability(striker, current_bowler)

                if random.random() < wicket_prob:
                    wickets += 1
                    print(f"{striker.name} is out!")
                    striker_index = non_striker_index
                    non_striker_index = wickets + 1
                    if non_striker_index >= len(batters):
                        break
                    continue
                
                run = random.randint(0, 6) if random.random() < run_prob else random.randint(0, 3)
                scores[striker.name] = scores.get(striker.name, 0) + run
                total_score += run
                print(f"Ball {ball + 1}: {striker.name} scored {run} runs (Total: {total_score}/{wickets})")

                if (run % 2) != 0:
                    striker_index, non_striker_index = non_striker_index, striker_index

                if target_score is not None and total_score > target_score:
                    print(f"{self.team2_name} has surpassed {self.team1_name}'s score and wins the game!")
                    return scores, wickets, total_score

                if ball == balls_per_over - 1:
                    if run == 0 or run % 2 == 0:
                        striker_index, non_striker_index = non_striker_index, striker_index
            
            print(f"End of Over {over + 1}: {batting_team_name} - {total_score}/{wickets}")

            bowler_overs[current_bowler.name] += 1
            bowler_index = (bowler_index + 1) % len(bowlers)

        return scores, wickets, total_score

    def play_game(self):
        print(f"Pitch Condition: {self.pitch_condition}")
        self.adjust_skills_for_pitch(self.team1_players)
        self.adjust_skills_for_pitch(self.team2_players)

        print(f"{self.team1_name} is batting first!")
        self.batting_aggression = "normal"  # Reset batting aggression for Team 1
        self.field_setting = "normal"  # Reset field setting for Team 2
        team1_batters = self.team1_players[:11]
        team1_bowlers = self.team2_players[6:11]
        team1_scores, self.team1_wickets, self.team1_score = self.play_innings(
            self.team1_name, team1_batters, team1_bowlers
        )
        print(f"{self.team1_name} total score: {self.team1_score}/{self.team1_wickets} runs/wickets\n")

        print(f"{self.team2_name} is batting now!")
        self.batting_aggression = "normal"  # Reset batting aggression for Team 2
        self.field_setting = "normal"  # Reset field setting for Team 1
        team2_batters = self.team2_players[:11]
        team2_bowlers = self.team1_players[6:11]
        team2_scores, self.team2_wickets, self.team2_score = self.play_innings(
            self.team2_name, team2_batters, team2_bowlers, target_score=self.team1_score
        )

        if self.team2_score < self.team1_score and self.team2_wickets == 10:
            print(f"{self.team2_name} is all out and did not surpass {self.team1.name}'s score. {self.team1_name} wins by {self.team1_score - self.team2_score} runs!")
        elif self.team2_score <= self.team1_score:
            print(f"{self.team2_name} total score: {self.team2_score}/{self.team2_wickets} runs/wickets")
            if self.team1_score > self.team2_score:
                print(f"{self.team1_name} wins by {self.team1_score - self.team2_score} runs!")
            elif self.team2_score > self.team1_score:
                print(f"{self.team2_name} wins by {self.team2_score - self.team1_score} runs!")
            else:
                print("The match is a draw!")

# Create players and initialize the game
team1_players = [
    Player("Player1", 80, 0), Player("Player2", 70, 0), Player("Player3", 75, 0),
    Player("Player4", 68, 0), Player("Player5", 72, 0), Player("Player6", 60, 0),
    Player("Bowler1", 30, 90), Player("Bowler2", 32, 85), Player("Bowler3", 28, 88),
    Player("Bowler4", 35, 87), Player("Bowler5", 30, 92)
]

team2_players = [
    Player("PlayerA", 65, 0), Player("PlayerB", 60, 0), Player("PlayerC", 68, 0),
    Player("PlayerD", 70, 0), Player("PlayerE", 62, 0), Player("PlayerF", 75, 0),
    Player("BowlerA", 30, 89), Player("BowlerB", 28, 90), Player("BowlerC", 26, 91),
    Player("BowlerD", 30, 86), Player("BowlerE", 33, 92)
]

pitch_condition = "batting"
game = CricketGame("India", "Australia", team1_players, team2_players, pitch_condition=pitch_condition)
game.play_game()
