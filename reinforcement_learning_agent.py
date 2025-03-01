import numpy as np
import tensorflow as tf
from tensorflow import keras
from collections import deque
import random

class ReinforcementLearningAgent:
    """
    A reinforcement learning agent that uses a neural network for Q-value approximation.

    This agent implements the Deep Q-Network (DQN) algorithm, a popular reinforcement
    learning technique that combines Q-learning with deep neural networks. The agent
    uses experience replay to improve learning stability and efficiency.

    Attributes:
        state_size (int): The size of the state space.
        action_size (int): The number of possible actions.
        memory (deque): A replay memory to store experiences.
        gamma (float): Discount factor for future rewards.
        epsilon (float): Exploration rate for the epsilon-greedy policy.
        epsilon_min (float): Minimum value for epsilon.
        epsilon_decay (float): Decay rate for epsilon.
        learning_rate (float): Learning rate for the neural network.
        model (keras.Model): The neural network model for Q-value approximation.

    Methods:
        build_model(): Constructs the neural network for Q-value approximation.
        remember(state, action, reward, next_state, done): Stores an experience in memory.
        act(state): Chooses an action using an epsilon-greedy policy.
        replay(batch_size): Trains the agent using experience replay.
        load(name): Loads the neural network weights from a file.
        save(name): Saves the neural network weights to a file.
    """

    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0   # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self.build_model()

    def build_model(self):
        """
        Constructs and returns a neural network model for Q-value approximation.

        The model architecture consists of two hidden layers with ReLU activation
        and an output layer with linear activation.

        Returns:
            keras.Model: The constructed neural network model.
        """
        model = keras.Sequential([
            keras.layers.Dense(24, input_dim=self.state_size, activation='relu'),
            keras.layers.Dense(24, activation='relu'),
            keras.layers.Dense(self.action_size, activation='linear')
        ])
        model.compile(loss='mse', optimizer=keras.optimizers.Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        """
        Stores an experience tuple in the replay memory.

        Args:
            state: The current state.
            action: The action taken.
            reward: The reward received.
            next_state: The resulting state.
            done: Boolean indicating if the episode has ended.
        """
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        """
        Chooses an action using an epsilon-greedy policy.

        Args:
            state: The current state.

        Returns:
            int: The chosen action.
        """
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        """
        Trains the agent using experience replay.

        Args:
            batch_size (int): The number of experiences to sample from memory.
        """
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

    def load(self, name):
        """
        Loads the neural network weights from a file.

        Args:
            name (str): The filename to load the weights from.
        """
        self.model.load_weights(name)

    def save(self, name):
        """
        Saves the neural network weights to a file.

        Args:
            name (str): The filename to save the weights to.
        """
        self.model.save_weights(name)

# Example usage:
# agent = ReinforcementLearningAgent(state_size, action_size)
# for e in range(n_episodes):
#     state = env.reset()
#     for time in range(max_time):
#         action = agent.act(state)
#         next_state, reward, done, _ = env.step(action)
#         agent.remember(state, action, reward, next_state, done)
#         state = next_state
#         if done:
#             break
#     if len(agent.memory) > batch_size:
#         agent.replay(batch_size)