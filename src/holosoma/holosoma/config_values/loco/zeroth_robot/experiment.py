"""Locomotion experiment presets for zeroth_robot.

Usage examples:
    # Fast SAC, single env, visual (for debugging):
    python src/holosoma/holosoma/train_agent.py \\
        exp:zeroth-robot-fast-sac \\
        simulator:isaacgym \\
        terrain:terrain-locomotion-plane \\
        --algo.config.compile=False \\
        --training.seed 1 \\
        --training.num-envs=1 \\
        --training.headless=False

    # PPO, full training:
    python src/holosoma/holosoma/train_agent.py \\
        exp:zeroth-robot \\
        simulator:isaacgym \\
        terrain:terrain-locomotion-plane \\
        --algo.config.compile=False \\
        --training.seed 1 \\
        --training.num-envs=1048 \\
        --training.headless=True
"""

from dataclasses import replace

from holosoma.config_types.experiment import ExperimentConfig, NightlyConfig, TrainingConfig
from holosoma.config_types.simulator import VirtualGantryCfg
from holosoma.config_values import (
    action,
    algo,
    command,
    curriculum,
    observation,
    randomization,
    reward,
    robot,
    simulator,
    termination,
    terrain,
)

# zeroth_robot's base link is named 'draft__speaker_mount', which is not in the
# default VirtualGantryCfg candidate list, so we supply it explicitly.
_zeroth_robot_simulator = replace(
    simulator.isaacgym,
    config=replace(
        simulator.isaacgym.config,
        virtual_gantry=VirtualGantryCfg(
            attachment_body_names=["draft__speaker_mount"],
        ),
    ),
)
from holosoma.config_values.loco.zeroth_robot.action import zeroth_robot_joint_pos
from holosoma.config_values.loco.zeroth_robot.command import zeroth_robot_command
from holosoma.config_values.loco.zeroth_robot.curriculum import (
    zeroth_robot_curriculum,
    zeroth_robot_curriculum_fast_sac,
)
from holosoma.config_values.loco.zeroth_robot.observation import zeroth_robot_loco_single_wolinvel
from holosoma.config_values.loco.zeroth_robot.randomization import zeroth_robot_randomization
from holosoma.config_values.loco.zeroth_robot.reward import zeroth_robot_loco, zeroth_robot_loco_fast_sac
from holosoma.config_values.loco.zeroth_robot.termination import zeroth_robot_termination

zeroth_robot = ExperimentConfig(
    env_class="holosoma.envs.locomotion.locomotion_manager.LeggedRobotLocomotionManager",
    training=TrainingConfig(project="hv-zeroth-robot", name="zeroth_robot_manager"),
    algo=replace(algo.ppo, config=replace(algo.ppo.config, num_learning_iterations=25000, use_symmetry=True)),
    simulator=_zeroth_robot_simulator,
    robot=robot.zeroth_robot,
    terrain=terrain.terrain_locomotion_mix,
    observation=zeroth_robot_loco_single_wolinvel,
    action=zeroth_robot_joint_pos,
    termination=zeroth_robot_termination,
    randomization=zeroth_robot_randomization,
    command=zeroth_robot_command,
    curriculum=zeroth_robot_curriculum,
    reward=zeroth_robot_loco,
    nightly=NightlyConfig(
        iterations=5000,
        metrics={"Episode/rew_tracking_ang_vel": [0.7, "inf"], "Episode/rew_tracking_lin_vel": [0.55, "inf"]},
    ),
)

zeroth_robot_fast_sac = ExperimentConfig(
    env_class="holosoma.envs.locomotion.locomotion_manager.LeggedRobotLocomotionManager",
    training=TrainingConfig(project="hv-zeroth-robot", name="zeroth_robot_fast_sac_manager"),
    algo=replace(algo.fast_sac, config=replace(algo.fast_sac.config, num_learning_iterations=50000, use_symmetry=True)),
    simulator=_zeroth_robot_simulator,
    robot=robot.zeroth_robot,
    terrain=terrain.terrain_locomotion_mix,
    observation=zeroth_robot_loco_single_wolinvel,
    action=zeroth_robot_joint_pos,
    termination=zeroth_robot_termination,
    randomization=zeroth_robot_randomization,
    command=zeroth_robot_command,
    curriculum=zeroth_robot_curriculum_fast_sac,
    reward=zeroth_robot_loco_fast_sac,
    nightly=NightlyConfig(
        iterations=50000,
        metrics={"Episode/rew_tracking_ang_vel": [0.8, "inf"], "Episode/rew_tracking_lin_vel": [0.95, "inf"]},
    ),
)

__all__ = ["zeroth_robot", "zeroth_robot_fast_sac"]
