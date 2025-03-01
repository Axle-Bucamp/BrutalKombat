import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# RLAgent class implementing Q-learning with epsilon-greedy policy
class RLAgent:
    def __init__(self, state_size, action_size, learning_rate=0.1, discount_factor=0.95, epsilon=0.1):
        self.q_table = np.zeros((state_size, action_size))
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.action_size = action_size

    def get_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.randint(self.action_size)
        return np.argmax(self.q_table[state])

    def update(self, state, action, reward, next_state):
        current_q = self.q_table[state, action]
        max_next_q = np.max(self.q_table[next_state])
        new_q = current_q + self.lr * (reward + self.gamma * max_next_q - current_q)
        self.q_table[state, action] = new_q

# Simple game environment
class Game:
    def __init__(self, size=10):
        self.size = size
        self.reset()

    def reset(self):
        self.state = np.random.randint(self.size)
        return self.state

    def step(self, action):
        if action == 0:  # move left
            self.state = max(0, self.state - 1)
        elif action == 1:  # move right
            self.state = min(self.size - 1, self.state + 1)
        
        reward = 1 if self.state == self.size // 2 else 0
        done = (self.state == 0) or (self.state == self.size - 1)
        return self.state, reward, done

# Training function for self-play
def train_agents(episodes, game):
    agent1 = RLAgent(game.size, 2)
    agent2 = RLAgent(game.size, 2)
    best_battle = []
    best_reward = -float('inf')

    for episode in tqdm(range(episodes)):
        state = game.reset()
        total_reward = 0
        battle = [state]

        while True:
            action1 = agent1.get_action(state)
            next_state, reward, done = game.step(action1)
            agent1.update(state, action1, reward, next_state)
            total_reward += reward
            battle.append(next_state)

            if done:
                break

            action2 = agent2.get_action(next_state)
            state, reward, done = game.step(action2)
            agent2.update(next_state, action2, -reward, state)  # Note the negative reward for agent2
            total_reward -= reward
            battle.append(state)

            if done:
                break

        if total_reward > best_reward:
            best_reward = total_reward
            best_battle = battle

        if (episode + 1) % 100 == 0:
            visualize_battle(best_battle, episode + 1)

    return agent1, agent2, best_battle

# Visualization function
def visualize_battle(battle, episode):
    plt.figure(figsize=(10, 5))
    plt.plot(battle, marker='o')
    plt.title(f"Best Battle (Episode {episode})")
    plt.xlabel("Time Step")
    plt.ylabel("Position")
    plt.grid(True)
    plt.savefig(f"best_battle_episode_{episode}.png")
    plt.close()

# Main execution
if __name__ == "__main__":
    game = Game(size=10)
    episodes = 10000
    
    print("Training agents...")
    agent1, agent2, best_battle = train_agents(episodes, game)
    
    print("Final Q-table for Agent 1:")
    print(agent1.q_table)
    print("\nFinal Q-table for Agent 2:")
    print(agent2.q_table)
    
    print(f"\nBest battle: {best_battle}")
    visualize_battle(best_battle, episodes)
    print(f"Best battle visualization saved as 'best_battle_episode_{episodes}.png'")