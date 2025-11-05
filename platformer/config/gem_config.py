"""
Centralized gem configurations.
Define gem types and their properties.
"""

# Gem type definitions
GEM_TYPES = {
    "standard": {
        "name": "Standard Gem",
        "image": "gem.png",
        "value": 1,  # How many gem points it's worth
        "size_multiplier": 1,
    },
    "heart": {
        "name": "Heart (Extra Life)",
        "image": "heart_02.png",
        "value": 1,  # In the current system, gems represent lives
        "size_multiplier": 1,
    },
    # Future gem types can be added here
    "gold": {
        "name": "Gold Gem",
        "image": "gem.png",  # Could use a different image
        "value": 3,  # Worth 3 gems
        "size_multiplier": 1.5,
    },
}


def get_gem_config(gem_type="standard", **overrides):
    """
    Get gem configuration with optional overrides.

    Args:
        gem_type: Type of gem from GEM_TYPES (default: "standard")
        **overrides: Any parameters to override (e.g., x, y, value)

    Returns:
        Dictionary with complete gem configuration

    Example:
        get_gem_config('gold', x=100, y=50)
    """
    if gem_type not in GEM_TYPES:
        raise ValueError(
            f"Unknown gem type: {gem_type}. Available types: {list(GEM_TYPES.keys())}"
        )

    config = GEM_TYPES[gem_type].copy()
    config.update(overrides)

    return config
