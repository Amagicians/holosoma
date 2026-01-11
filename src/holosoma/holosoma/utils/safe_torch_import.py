# Ensure that torch is imported after isaacgym, if isaacgym is installed.
try:
    import isaacgym  # noqa: F401
except ImportError:
    pass

import torch
import torch.nn.functional as F
from tensordict import TensorDict
from torch import nn, optim
# from torch.amp import GradScaler, autocast
try:
    from torch.amp import autocast  # torch 2.x 常见可用
except Exception:
    from torch.cuda.amp import autocast  # torch 1.x fallback

try:
    from torch.amp import GradScaler  # 部分 torch 2.x 才有
except Exception:
    from torch.cuda.amp import GradScaler  # torch 1.x / torch 2.0.x

from torch.utils.tensorboard import SummaryWriter as TensorboardSummaryWriter

__all__ = ["F", "GradScaler", "TensorDict", "TensorboardSummaryWriter", "autocast", "nn", "optim", "torch"]
