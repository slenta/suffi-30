"""World objects - platforms, ladders, pipes, spikes, and decorative elements."""

from .platform_class import Platform
from .moving_platform import MovingPlatform
from .ladder import Ladder, LadderTop
from .pipe import Pipe
from .spike import Spike
from .waterfall import Waterfall, WaterfallTop

__all__ = [
    "Platform",
    "MovingPlatform",
    "Ladder",
    "LadderTop",
    "Pipe",
    "Spike",
    "Waterfall",
    "WaterfallTop",
]
