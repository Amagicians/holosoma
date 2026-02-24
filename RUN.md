# Commands

```bash
source scripts/source_isaacgym_setup.sh 
python src/holosoma/holosoma/train_agent.py \
        exp:g1-29dof-fast-sac \
        simulator:isaacgym \
        terrain:terrain-locomotion-plane \
        --algo.config.compile=False \
        --training.seed 1 \
        --training.num-envs=1 \
        --training.headless=False


python src/holosoma/holosoma/train_agent.py \
        exp:g1-29dof \
        simulator:isaacgym \
        terrain:terrain-locomotion-plane \
        --algo.config.compile=False \
        --training.seed 1 \
        --training.num-envs=1048 \
        --training.headless=True


cd /home/markji/Documents/githubProject/holosoma && source scripts/source_isaacgym_setup.sh && python src/holosoma/holosoma/eval_agent.py --checkpoint=/home/markji/Documents/githubProject/holosoma/logs/hv-g1-manager/20260202_062223-g1_29dof_fast_sac_manager-locomotion/model_0050000.pt
```

```bash
任务性能指标

这些决定机器人走路的质量：

指标	                 当前值	  说明	                目标值
rew_tracking_lin_vel	0.0728	线速度跟踪 ⚠️ 很低	~0.95+
rew_tracking_ang_vel	0.0871	角速度跟踪 ⚠️ 很低	~0.80+
rew_alive	        1.5271	存活奖励  ✅ 好	      持续高
rew_feet_phase	        0.4511	步态质量  🟡 中等	~0.8+
rew_pose	        -0.2324	姿态惩罚  🟡 可接受	接近 0
解读：

# 运行这个命令实时查看训练日志
tail -f logs/hv-g1-manager/*/train.log
关注这些变化：

Mean reward: 21.65 → 期望涨到 50+
rew_tracking_lin_vel: 0.0728 → 期望涨到 0.8+
rew_tracking_ang_vel: 0.0871 → 期望涨到 0.7+
Mean episode length: 133 → 期望涨到 400+（更长的存活时间）
正常训练曲线预期

Iteration 0-5000    : 机器人学会站立、保持平衡
Iteration 5000-15000: 开始尝试移动，速度跟踪逐渐提升
Iteration 15000-30000: 步态逐渐优化，速度跟踪提升到 0.5+
Iteration 30000-50000: 精细调整，速度跟踪提升到 0.8+
```



```bash
直接从 URDF 提取的参数 ✅
结构参数

num_bodies=17 — 数了 URDF 里所有 <link> 标签，共 17 个
dof_obs_size=16 / actions_dim=16 — 数了所有 type="revolute" 的 <joint>，共 16 个
num_feet=2 — URDF 里有 foot_left 和 foot_right 两个足端 link
关节名称（完全来自 URDF joint name 属性）

dof_names 里的 16 个名字 — 全部照搬 URDF 中 <joint name="..."> 的值
body_names 里的 17 个名字 — 全部照搬 URDF 中 <link name="..."> 的值
key_bodies, foot_body_name, foot_height_name, knee_name, torso_name — 从 link 名推断
关节限位（完全来自 URDF <limit> 标签）

dof_pos_lower_limit_list — 每个关节的 lower= 值
dof_pos_upper_limit_list — 每个关节的 upper= 值
dof_vel_limit_list — 每个关节的 velocity=（全部是 10.0）
dof_effort_limit_list — 每个关节的 effort=（全部是 10.0）
我暂时填的参数 ⚠️（需要你确认或调整）
物理参数（没有标准来源，用的保守默认值）

dof_armature_list=[0.001]*16 — 电机转子惯量，G1 根据型号计算过，zeroth_robot 没有数据，先用通用小值
dof_joint_friction_list=[0.0]*16 — 关节摩擦，G1 也是全 0，暂时沿用
PD 控制参数（估算，需要调）

stiffness 和 damping — 根据 effort=10 Nm 这个小力矩范围估算的保守值，这是最需要调整的参数，直接影响训练效果
初始状态（估算）

init_state.pos[2]=0.35 — 初始高度，我根据髋关节原点 z=-0.156m 加上腿链估算的，第一次运行必须验证，高了机器人会掉落，低了会卡地面
default_joint_angles 里的角度值 — 典型双足微弯腿姿势（hip_pitch=-0.3, knee=0.6, ankle=-0.3），是通用估算
对称性参数（逻辑推断，需要验证）

symmetry_joint_names — 左右对称映射，逻辑上正确，但依赖 URDF 轴向定义
flip_sign_joint_names — roll/yaw 关节在左右腿物理方向相反需要翻转，具体哪些关节需要翻转取决于 URDF 轴向，如果对称奖励异常再来排查
功能分组（从关节名逻辑推断）

terminate_after_contacts_on / penalize_contacts_on — 用了 link 名的子串匹配，逻辑合理但未实测
has_torso=False — zeroth_robot 没有腰部关节，逻辑确定
has_upper_body_dof=True — 有手臂关节，逻辑确定
```

```bash
source scripts/source_isaacgym_setup.sh
python src/holosoma/holosoma/train_agent.py \
    exp:zeroth-robot-fast-sac \
    simulator:isaacgym \
    terrain:terrain-locomotion-plane \
    --algo.config.compile=False \
    --training.seed 1 \
    --training.num-envs=1 \
    --training.headless=False


cd /home/markji/Documents/githubProject/holosoma && source scripts/source_isaacgym_setup.sh && python src/holosoma/holosoma/train_agent.py \
    exp:zeroth-robot-fast-sac \
    simulator:isaacgym \
    terrain:terrain-locomotion-plane \
    --algo.config.compile=False \
    --training.seed 1 \
    --training.num-envs=1048 \
    --training.headless=True \
    --algo.config.num-learning-iterations=10000

cd /home/markji/Documents/githubProject/holosoma && source scripts/source_isaacgym_setup.sh && python src/holosoma/holosoma/eval_agent.py \
    --checkpoint=logs/hv-zeroth-robot/20260224_042337-zeroth_robot_fast_sac_manager-locomotion/model_0009000.pt

```