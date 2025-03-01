import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

class RLAgent:
    def __init__(self, state_size, action_size, epsilon=0.1, alpha=0.1, gamma=0.9):
        self.state_size = state_size
        self.action_size = action_size
        self.epsilon = epsilon  # Exploration rate
        self.alpha = alpha      # Learning rate
        self.gamma = gamma      # Discount factor
        self.q_table = np.zeros((state_size, action_size))

    def get_action(self, state):
        # Epsilon-greedy action selection
        if np.random.rand() < self.epsilon:
            return np.random.randint(self.action_size)
        return np.argmax(self.q_table[state])

    def update(self, state, action, reward, next_state):
        # Q-learning update
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.gamma * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.alpha * td_error

class Game:
    def __init__(self, size=10):
        self.size = size
        self.reset()

    def reset(self):
        self.player1 = self.size // 2 - 1
        self.player2 = self.size // 2
        return self.player1, self.player2

    def step(self, action1, action2):
        # Move players based on actions (0: left, 1: stay, 2: right)
        self.player1 += action1 - 1
        self.player2 += action2 - 1

        # Check for game over conditions
        if self.player1 < 0 or self.player1 >= self.size or self.player2 < 0 or self.player2 >= self.size:
            return (self.player1, self.player2), (-1, -1), True

        # Reward is the negative distance between players
        reward = -abs(self.player1 - self.player2)
        return (self.player1, self.player2), (reward, reward), False

def train_agents(episodes=10000, visualize_every=100):
    game = Game()
    agent1 = RLAgent(game.size, 3)
    agent2 = RLAgent(game.size, 3)
    best_battle = None
    best_reward = -np.inf

    for episode in tqdm(range(episodes)):
        state = game.reset()
        total_reward = 0
        battle_history = [state]

        while True:
            action1 = agent1.get_action(state[0])
            action2 = agent2.get_action(state[1])
            next_state, rewards, done = game.step(action1, action2)
            battle_history.append(next_state)

            agent1.update(state[0], action1, rewards[0], next_state[0])
            agent2.update(state[1], action2, rewards[1], next_state[1])

            state = next_state
            total_reward += rewards[0]

            if done:
                break

        if total_reward > best_reward:
            best_reward = total_reward
            best_battle = battle_history

        if (episode + 1) % visualize_every == 0:
            visualize_battle(best_battle, episode + 1)

    return agent1, agent2, best_battle

def visualize_battle(battle, episode):
    plt.figure(figsize=(10, 5))
    plt.plot([state[0] for state in battle], label='Player 1')
    plt.plot([state[1] for state in battle], label='Player 2')
    plt.xlabel('Time Step')
    plt.ylabel('Position')
    plt.title(f'Best Battle at Episode {episode}')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'best_battle_episode_{episode}.png')
    plt.close()

if __name__ == "__main__":
    agent1, agent2, best_battle = train_agents()
    print("Training completed. Final Q-tables:")
    print("Agent 1 Q-table:")
    print(agent1.q_table)
    print("\nAgent 2 Q-table:")
    print(agent2.q_table)
    visualize_battle(best_battle, 10000)