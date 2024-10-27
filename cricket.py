import random

class CricketGame:
    def __init__(self, team1_name, team2_name, team1_batting_skill, team1_bowling_skill, team2_batting_skill, team2_bowling_skill):
        self.team1_name = team1_name
        self.team2_name = team2_name
        self.team1_batting_skill = team1_batting_skill
        self.team1_bowling_skill = team1_bowling_skill
        self.team2_batting_skill = team2_batting_skill
        self.team2_bowling_skill = team2_bowling_skill
        self.team1_score = 0
        self.team2_score = 0

    def play_innings(self, batting_skill, bowling_skill):
        score = 0
        for ball in range(6):
           
            run = random.randint(0, 6) if random.random() < batting_skill - bowling_skill else random.randint(0, 3)
            score += run
        return score

    def play_game(self):
        print(f"{self.team1_name} is batting first!")
        self.team1_score = self.play_innings(self.team1_batting_skill, self.team2_bowling_skill)
        print(f"{self.team1_name} scored: {self.team1_score} runs")

        print(f"{self.team2_name} is batting now!")
        self.team2_score = self.play_innings(self.team2_batting_skill, self.team1_bowling_skill)
        print(f"{self.team2_name} scored: {self.team2_score} runs")

        if self.team1_score > self.team2_score:
            print(f"{self.team1_name} wins by {self.team1_score - self.team2_score} runs!")
        elif self.team2_score > self.team1_score:
            print(f"{self.team2_name} wins by {self.team2_score - self.team1_score} runs!")
        else:
            print("The match is a draw!")


game = CricketGame("india", "australia", 80,90,70,100)
game.play_game()
 
 
 

 
 
 








        
    


