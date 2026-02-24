"""Locomotion action presets for zeroth_robot."""

from holosoma.config_types.action import ActionManagerCfg, ActionTermCfg

zeroth_robot_joint_pos = ActionManagerCfg(
    terms={
        "joint_control": ActionTermCfg(
            func="holosoma.managers.action.terms.joint_control:JointPositionActionTerm",
            params={},
            scale=1.0,
            clip=None,
        ),
    }
)

__all__ = ["zeroth_robot_joint_pos"]
