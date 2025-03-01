import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

class RLAgent:
    def __init__(self, state_size, action_size, learning_rate=0.1, discount_factor=0.95, epsilon=0.1):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        
        # Initialize Q-table with zeros
        self.q_table = np.zeros((state_size, action_size))
    
    def get_action(self, state):
        # Epsilon-greedy action selection
        if np.random.rand() < self.epsilon:
            return np.random.randint(self.action_size)
        else:
            return np.argmax(self.q_table[state])
    
    def update(self, state, action, reward, next_state):
        # Q-learning update
        current_q = self.q_table[state, action]
        max_next_q = np.max(self.q_table[next_state])
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        self.q_table[state, action] = new_q

class Game:
    def __init__(self, size=5):
        self.size = size
        self.reset()
    
    def reset(self):
        self.state = np.random.randint(self.size)
        return self.state
    
    def step(self, action):
        # Simple game logic: move left or right, wrap around
        if action == 0:  # move left
            self.state = (self.state - 1) % self.size
        else:  # move right
            self.state = (self.state + 1) % self.size
        
        # Reward is 1 if at the center, -1 otherwise
        reward = 1 if self.state == self.size // 2 else -1
        
        return self.state, reward, False

def train_agents(num_episodes=10000, visualize_interval=100):
    game = Game()
    agent1 = RLAgent(game.size, 2)
    agent2 = RLAgent(game.size, 2)
    
    best_battle = []
    
    for episode in tqdm(range(num_episodes)):
        state = game.reset()
        total_reward1 = 0
        total_reward2 = 0
        battle = []
        
        while True:
            # Agent 1's turn
            action1 = agent1.get_action(state)
            next_state, reward1 = game.step(action1)
            agent1.update(state, action1, reward1, next_state)
            total_reward1 += reward1
            battle.append((state, action1, next_state, reward1, 1))
            
            state = next_state
            
            # Agent 2's turn
            action2 = agent2.get_action(state)
            next_state, reward2 = game.step(action2)
            agent2.update(state, action2, reward2, next_state)
            total_reward2 += reward2
            battle.append((state, action2, next_state, reward2, 2))
            
            state = next_state
            
            if len(battle) >= 20:  # Limit battle length
                break
        
        # Store the best battle for visualization
        if episode % visualize_interval == 0:
            if not best_battle or total_reward1 + total_reward2 > sum(r for _, _, _, r, _ in best_battle):
                best_battle = battle
    
    return agent1, agent2, best_battle

def visualize_battle(battle, game_size):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xlim(0, len(battle))
    ax.set_ylim(0, game_size - 1)
    ax.set_xlabel('Time Step')
    ax.set_ylabel('Game State')
    ax.set_title('Best Battle Visualization')
    
    states = [s for s, _, _, _, _ in battle]
    actions = [a for _, a, _, _, _ in battle]
    rewards = [r for _, _, _, r, _ in battle]
    agents = [ag for _, _, _, _, ag in battle]
    
    for i in range(len(battle) - 1):
        color = 'red' if agents[i] == 1 else 'blue'
        ax.arrow(i, states[i], 1, states[i+1] - states[i], color=color, head_width=0.1, head_length=0.1)
        ax.annotate(f'R:{rewards[i]}', (i, states[i]), xytext=(0, 5), textcoords='offset points')
    
    plt.show()

# Train the agents and visualize the best battle
agent1, agent2, best_battle = train_agents()
visualize_battle(best_battle, 5)

# Print final Q-tables
print("Agent 1 Q-table:")
print(agent1.q_table)
print("\nAgent 2 Q-table:")
print(agent2.q_table)