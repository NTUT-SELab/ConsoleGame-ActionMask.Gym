import pytest
import numpy as np

from env.Galaxian.action_mask_env import ActionMaskEnv

def setup_function():
    pytest.env = ActionMaskEnv(high=11, width=11)
    pytest.env.reset()

def test_step():
    original_obs = pytest.env.reset()
    original_enemy_approach_progress = pytest.env.enemies[0].approach_progress
    number_of_bullets = len(pytest.env.bullets)
    original_steps = pytest.env.current_step
    pytest.env.galaxian.position[1] = 2

    new_obs, _, _, info = pytest.env.step(0)

    #Galaxian = 2, Bullet = 4, Bonus = 5
    galaxain_step_result = np.array(np.where(new_obs == 2)) - np.array(np.where(original_obs == 2))
    bullet_step_result = np.array(np.where(new_obs == 4)) - np.array(np.where(new_obs == 2))
    bonus_step_result = np.array(np.where(new_obs == 5)) - np.array(np.where(original_obs == 5))

    np.testing.assert_array_equal(galaxain_step_result, np.array([[0], [-4], [0]]))
    np.testing.assert_array_equal(bullet_step_result, np.array([[-1], [0], [0]]))
    np.testing.assert_array_equal(info.get('action_mask'), [0, 1])
    
    #BONUS MOVE TOWARD RANDOM DIRECTION, RESULT MIGHT BE 1 OR -1
    assert np.array_equal(bonus_step_result, np.array([[0], [1], [0]])) or np.array_equal(bonus_step_result, np.array([[0], [-1], [0]]))
    
    assert len(pytest.env.bullets) - number_of_bullets == 1
    assert pytest.env.current_step - original_steps == 1
    assert pytest.env.enemies[0].approach_progress - original_enemy_approach_progress == 1
    
def test_compute_action_mask():
    left_end = 1
    right_end = pytest.env.map.width - 2
    
    pytest.env.galaxian.position[1] = left_end
    action_mask = pytest.env.compute_action_mask(False)
    np.testing.assert_array_equal(action_mask, [0, 1])

    pytest.env.galaxian.position[1] = right_end
    action_mask = pytest.env.compute_action_mask(False)
    np.testing.assert_array_equal(action_mask, [1, 0])

    action_mask = pytest.env.compute_action_mask(True)
    np.testing.assert_array_equal(action_mask, [1, 1])
    