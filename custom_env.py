import math
from typing import Optional, Tuple, Union

import numpy as np

import gymnasium as gym
from gymnasium import logger, spaces
from gymnasium.envs.classic_control import utils
from gymnasium.error import DependencyNotInstalled
from gymnasium.experimental.vector import VectorEnv
from gymnasium.vector.utils import batch_space


class CustomEnv(gym.Env[np.ndarray, Union[int, np.ndarray]]):
    """
    ## description:
    both start and target number is random (from -100 to 100)
    the agent can choose to increase or decrease the number based
    on the current and target number

    ## actions:
    - 0: decrease number
    - 1: increase number

    ## observations:
    ndarray with shape (2, )
    - 0: current number
    - 1: target number

    ## rewards:
    +1 for going towards target number (limit of 30)
    +50 for getting target number

    ## start state:
    random start and target number

    ## end state:
    1. current number is target number
    2. the current number goes outside of -200, 200 range
    """

    metadata = {
        "render_modes": ["human", "rgb_array"],
        "render_fps": 60,
    }

    def __init__(self, render_mode: Optional[str] = None):
        self.startRange = 100
        self.endRange = 300

        self.action_space = spaces.Discrete(2)
        high = np.array(
            [
                self.endRange,
                np.finfo(np.int32).max,
                self.endRange,
                np.finfo(np.int32).max,
            ],
            dtype=np.int32,
        )
        self.observation_space = spaces.Box(-high, high, dtype=np.int32)

        self.render_mode = render_mode
        self.screen_width = 600
        self.screen_height = 400

        # not sure what these do
        self.screen = None
        self.clock = None
        self.isopen = True
        self.state = None

        self.steps_beyond_terminated = None

    def step(self, action):
        raise NotImplementedError
