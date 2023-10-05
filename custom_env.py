import math
from typing import Optional, Tuple, Union

import numpy as np
import random

import gymnasium as gym
from gymnasium import logger, spaces
from gymnasium.envs.classic_control import utils
from gymnasium.error import DependencyNotInstalled
from gymnasium.experimental.vector import VectorEnv
from gymnasium.vector.utils import batch_space


class CustomEnv(gym.Env):
    """
    ## description:
    both start and target number is random (from -100 to 100)
    the agent can choose to increase or decrease the number based
    on the current and target number

    ## actions:
    - 0 to 8: put marker in spot

    ## observations:
    an array of ints:
    0 | 1 | 2
    ---------
    3 | 4 | 5
    ---------
    6 | 7 | 8

    ## rewards:
    + 1 if 3 in a row
    - 1 if end in a tie
    - 2 if loose

    ## start state:
    board is cleared, ai goes first

    ## end state:
    1. there is a 3 in a row
    2. board is filled
    """

    metadata = {
        "render_modes": ["human", "rgb_array"],
        "render_fps": 60,
    }

    def __init__(self, render_mode: Optional[str] = None):
        self.board = 9 * [0]  # 3 by 3 board

        # able to choose between 9 spots
        self.action_space = spaces.Discrete(9)

        # all 9 spots have 3 states: empty, X, or O
        self.observation_space = spaces.MultiDiscrete(9 * [3])

        self.render_mode = render_mode
        self.done = False
        self.state = None

        self.steps_beyond_terminated = None

    def step(self, action):
        print("action", action)
        """
        # Map the action (element of {0,1,2,3}) to the direction we walk in
        direction = self._action_to_direction[action]
        # We use `np.clip` to make sure we don't leave the grid
        self._agent_location = np.clip(
            self._agent_location + direction, 0, self.size - 1
        )
        # An episode is done iff the agent has reached the target
        terminated = np.array_equal(self._agent_location, self._target_location)
        reward = 1 if terminated else 0  # Binary sparse rewards
        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, False, info
        """
        raise NotImplementedError

    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random (not sure why)
        super().reset(seed=seed)

        # We will sample the target's location randomly until it does not coincide with the agent's location
        self.target_num = self.agent_num = 0
        while self.target_num == self.agent_num:
            self.target_num = random.randrange(-self.startRange, self.startRange)
            self.agent_num = random.randrange(-self.startRange, self.startRange)

        observation = self.GetObservation()
        info = self.GetInfo()

        # if self.render_mode == "human":
        #    self.render()

        print(
            "observation:",
            type(observation),
            observation,
        )

        return observation, info

    def GetObservation(self):  # not sure if done
        return {"agent": self.agent_num, "target": self.target_num}

    def GetInfo(self):  # idk what the point of it is
        return {"distance:": abs(self.target_num - self.agent_num)}

    def render(self):
        # nothing to render yet
        return

    def close(self):
        # nothing to clean up yet
        return
