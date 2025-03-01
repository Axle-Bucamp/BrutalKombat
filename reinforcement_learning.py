import numpy as np
import tensorflow as tf
from tensorflow import keras
from collections import deque
import random
from bk_street_fighter import BKStreetFighter, Fighter, AIPlayer

class RLAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.model = self._build_model()

    def _build_model(self):
        model = keras.Sequential([
            keras.layers.Dense(24, input_dim=self.state_size, activation='relu'),
            keras.layers.Dense(24, activation='relu'),
            keras.layers.Dense(self.action_size, activation='linear')
        ])
        model.compile(loss='mse', optimizer=keras.optimizers.Adam(lr=0.001))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma *
                          np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

def train_agents(episodes, batch_size=32, visualize_every=100):
    game = BKStreetFighter()
    state_size = len(game.get_state())
    action_size = len(game.get_actions())
    
    agent1 = RLAgent(state_size, action_size)
    agent2 = RLAgent(state_size, action_size)
    
    best_score = -np.inf
    best_game_states = []

    for e in range(episodes):
        state = game.reset()
        state = np.reshape(state, [1, state_size])
        done = False
        while not done:
            action1 = agent1.act(state)
            action2 = agent2.act(state)
            next_state, reward1, reward2, done = game.step(action1, action2)
            next_state = np.reshape(next_state, [1, state_size])
            
            agent1.remember(state, action1, reward1, next_state, done)
            agent2.remember(state, action2, reward2, next_state, done)
            
            state = next_state

        if len(agent1.memory) > batch_size:
            agent1.replay(batch_size)
            agent2.replay(batch_size)

        if e % visualize_every == 0:
            score = game.get_score()
            if score > best_score:
                best_score = score
                best_game_states = game.get_game_states()
            print(f"Episode: {e}/{episodes}, Score: {score}, Best Score: {best_score}")
            visualize_best_game(best_game_states)

    return agent1, agent2

def visualize_best_game(game_states):
    # Implement visualization logic here
    # This could involve rendering the game states using Pygame
    pass

if __name__ == "__main__":
    trained_agent1, trained_agent2 = train_agents(episodes=10000, visualize_every=100)
    # Save the trained models if needed
    trained_agent1.model.save("trained_agent1.h5")
    trained_agent2.model.save("trained_agent2.h5")