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
```