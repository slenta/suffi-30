"""
Centralized trophy configurations.
Define trophy types and their properties.
"""

# Trophy type definitions
TROPHY_TYPES = {
    "standard": {
        "name": "Standard Trophy",
        "image": "trophy.png",
        "size_multiplier": 2,  # 2 * GRIDSIZE
    },
    "baby": {
        "name": "Baby Trophy",
        "image": "trophy.png",  # Could use baby-themed trophy image
        "size_multiplier": 2,
    },
    "trance": {
        "name": "Trance Trophy",
        "image": "trophy.png",  # Could use trance-themed trophy image
        "size_multiplier": 2,
    },
    # Future trophy types can be added here
    "golden": {
        "name": "Golden Trophy",
        "image": "trophy.png",  # Could use a different image
        "size_multiplier": 3,
    },
}


def get_trophy_config(trophy_type="standard", **overrides):
    """
    Get trophy configuration with optional overrides.
    
    Args:
        trophy_type: Type of trophy from TROPHY_TYPES (default: "standard")
        **overrides: Any parameters to override (e.g., x, y, image)
    
    Returns:
        Dictionary with complete trophy configuration
    
    Example:
        get_trophy_config('golden', x=100, y=50)
    """
    if trophy_type not in TROPHY_TYPES:
        raise ValueError(f"Unknown trophy type: {trophy_type}. Available types: {list(TROPHY_TYPES.keys())}")
    
    config = TROPHY_TYPES[trophy_type].copy()
    config.update(overrides)
    
    return config
