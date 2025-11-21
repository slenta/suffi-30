#!/usr/bin/env python3
"""Test script to verify highscore API is working."""

import sys
import json
import asyncio

# Test the HTTP client
try:
    from platformer.core.http_highscore_client import (
        HTTPHighscoreClient,
        LocalStorageHighscoreClient,
    )
    from platformer.config.api_config import API_BASE_URL

    print("=" * 60)
    print("HIGHSCORE API TEST")
    print("=" * 60)
    print()

    # Show configuration
    print(f"API_BASE_URL configured: {API_BASE_URL}")
    print(f"Platform: {sys.platform}")
    print()

    # Create client
    client = HTTPHighscoreClient(api_base_url=API_BASE_URL)

    async def test_api():
        print("Testing API connection...")
        print()

        # Test data
        test_score = {
            "total_score": 999,
            "time_score": 500,
            "trophy_score": 300,
            "damage_score": 150,
            "life_score": 49,
        }

        # Test add highscore
        print("1. Testing add_highscore...")
        result = await client.add_highscore("test-level", "TestPlayer", test_score)
        print(f"   Result: {result}")
        print()

        # Test get top scores
        print("2. Testing get_top_scores...")
        scores = await client.get_top_scores("test-level", limit=5)
        print(f"   Found {len(scores)} scores")
        for i, score in enumerate(scores[:3], 1):
            print(f"   {i}. {score['player_name']}: {score['score']}")
        print()

        # Test is highscore
        print("3. Testing is_highscore...")
        is_high = await client.is_highscore("test-level", 1000)
        print(f"   Score of 1000 is highscore: {is_high}")
        print()

        print("=" * 60)
        print("All tests completed!")
        print("=" * 60)

    # Run tests
    asyncio.run(test_api())

except Exception as e:
    print(f"Error: {e}")
    import traceback

    traceback.print_exc()
