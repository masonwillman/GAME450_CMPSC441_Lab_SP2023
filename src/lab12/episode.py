''' 
Lab 12: Beginnings of Reinforcement Learning
We will modularize the code in pygrame_combat.py from lab 11 together.

Then it's your turn!
Create a function called run_episode that takes in two players
and runs a single episode of combat between them. 
As per RL conventions, the function should return a list of tuples
of the form (observation/state, action, reward) for each turn in the episode.
Note that observation/state is a tuple of the form (player1_health, player2_health).
Action is simply the weapon selected by the player.
Reward is the reward for the player for that turn.
'''
import sys
from pathlib import Path
sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))

# Imports used within the run_episode function
from lab11.turn_combat import Combat
from lab11.pygame_combat import run_turn, PyGameComputerCombatPlayer
from lab11.pygame_ai_player import PyGameAICombatPlayer

# run_episode runs a combat that 
def run_episode(player, opponent):

    # Creates an episode of combat 
    episode = Combat()

    # Creates an empty list for our rewards
    rewards = []

    # While the episode is not over (neither player has lost yet)
    while not episode.gameOver:
        # We append the return information from the run_turn function. 
        # This provides a tuple that is [[player.health, opponent.health], player.weapon, player.reward]
        rewards.append(run_turn(episode, player, opponent))

    # We return the rewards list after successfully completing an episode (combat is finished)
    return rewards


# Main to test function
if __name__ == "__main__":

    # Creates an human AI player
    player = PyGameAICombatPlayer("Human")
    
    # Creates a computer opponent
    opponent = PyGameComputerCombatPlayer("Computer")

    # Creates an empty rewards list
    rewards = []

    # Gets the rewards list from the episode
    rewards = run_episode(player, opponent)
    
    # Prints the list for testing
    print(rewards)



