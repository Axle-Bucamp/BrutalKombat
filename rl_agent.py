import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

class RLAgent:
    def __init__(self, state_size, action_size, epsilon=0.1, alpha=0.1, gamma=0.9):
        self.q_table = np.zeros((state_size, action_size))
        self.epsilon = epsilon  # Exploration rate
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor

    def get_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.randint(self.q_table.shape[1])
        return np.argmax(self.q_table[state])

    def update(self, state, action, reward, next_state):
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
        return self.get_state()

    def get_state(self):
        return self.player1 * self.size + self.player2

    def step(self, action1, action2):
        # Move players: 0 = left, 1 = stay, 2 = right
        self.player1 += action1 - 1
        self.player2 += action2 - 1

        # Ensure players stay within bounds
        self.player1 = max(0, min(self.player1, self.size - 1))
        self.player2 = max(0, min(self.player2, self.size - 1))

        state = self.get_state()
        reward1 = 1 if self.player1 == self.size // 2 else 0
        reward2 = 1 if self.player2 == self.size // 2 - 1 else 0

        done = (self.player1 == 0 or self.player1 == self.size - 1 or
                self.player2 == 0 or self.player2 == self.size - 1)

        return state, reward1, reward2, done

def train_agents(episodes, visualize_every=100):
    game = Game()
    state_size = game.size ** 2
    action_size = 3

    agent1 = RLAgent(state_size, action_size)
    agent2 = RLAgent(state_size, action_size)

    best_battle = []
    best_reward = -float('inf')

    for episode in tqdm(range(1, episodes + 1)):
        state = game.reset()
        total_reward = 0
        battle = [state]

        while True:
            action1 = agent1.get_action(state)
            action2 = agent2.get_action(state)

            next_state, reward1, reward2, done = game.step(action1, action2)
            battle.append(next_state)

            agent1.update(state, action1, reward1, next_state)
            agent2.update(state, action2, reward2, next_state)

            state = next_state
            total_reward += reward1 + reward2

            if done:
                break

        if total_reward > best_reward:
            best_reward = total_reward
            best_battle = battle

        if episode % visualize_every == 0:
            visualize_battle(best_battle, episode)

    return agent1, agent2, best_battle

def visualize_battle(battle, episode):
    plt.figure(figsize=(12, 6))
    plt.plot(battle)
    plt.title(f"Best Battle (Episode {episode})")
    plt.xlabel("Time Step")
    plt.ylabel("Game State")
    plt.savefig(f"best_battle_episode_{episode}.png")
    plt.close()

if __name__ == "__main__":
    num_episodes = 10000
    agent1, agent2, best_battle = train_agents(num_episodes)

    print("Training complete. Final Q-tables:")
    print("Agent 1:")
    print(agent1.q_table)
    print("\nAgent 2:")
    print(agent2.q_table)

    visualize_battle(best_battle, num_episodes)
    print(f"Best battle visualization saved as 'best_battle_episode_{num_episodes}.png'")