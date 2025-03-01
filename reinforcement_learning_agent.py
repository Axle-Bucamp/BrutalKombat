import numpy as np
import tensorflow as tf
from tensorflow import keras

class ReinforcementLearningAgent:
    """
    A reinforcement learning agent with neural network capabilities.

    This class implements a reinforcement learning agent using a neural network
    for function approximation. It uses the Deep Q-Network (DQN) algorithm to
    learn optimal policies in complex environments.

    Attributes:
        state_size (int): The size of the state space.
        action_size (int): The number of possible actions.
        memory (list): A list to store experience replay tuples.
        gamma (float): The discount factor for future rewards.
        epsilon (float): The exploration rate.
        epsilon_min (float): The minimum exploration rate.
        epsilon_decay (float): The decay rate for epsilon.
        learning_rate (float): The learning rate for the neural network.
        model (keras.Model): The neural network model for Q-value approximation.

    Methods:
        build_model(): Constructs the neural network model.
        remember(state, action, reward, next_state, done): Stores experience in memory.
        act(state): Chooses an action using an epsilon-greedy policy.
        replay(batch_size): Trains the agent using experience replay.
        load(name): Loads the neural network weights from a file.
        save(name): Saves the neural network weights to a file.
    """

    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = []
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0   # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self.build_model()

    def build_model(self):
        """
        Constructs the neural network model for Q-value approximation.

        Returns:
            keras.Model: The compiled neural network model.
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
        Stores a transition in the replay memory.

        Args:
            state: The current state.
            action: The action taken.
            reward: The reward received.
            next_state: The resulting state.
            done: Whether the episode has ended.
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
            return np.random.randint(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        """
        Trains the agent using experience replay.

        Args:
            batch_size (int): The number of samples to use for training.
        """
        minibatch = np.random.choice(len(self.memory), batch_size, replace=False)
        for i in minibatch:
            state, action, reward, next_state, done = self.memory[i]
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
# agent = ReinforcementLearningAgent(state_size=4, action_size=2)
# for episode in range(1000):
#     state = env.reset()
#     for time in range(500):
#         action = agent.act(state)
#         next_state, reward, done, _ = env.step(action)
#         agent.remember(state, action, reward, next_state, done)
#         state = next_state
#         if done:
#             break
#     if len(agent.memory) > 32:
#         agent.replay(32)