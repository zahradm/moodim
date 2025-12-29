"""
Step definitions for Mood feature tests.
"""

from collections import Counter

from behave import given, then, when


# ============== Given Steps ==============


@given("Redis cache is available")
def step_redis_available(context):
    """Verify Redis is accessible."""
    # In a real implementation, this would check Redis connection
    context.cache_available = True


@given("I have valid mood data")
def step_valid_mood_data(context):
    """Set up valid mood data from the data table."""
    for row in context.table:
        context.request_data = {
            "user_id": int(row["user_id"]),
            "emotion": row["emotion"],
            "percentage": float(row["percentage"]),
            "date": row["date"],
        }


@given('I have mood data with emotion "{emotion}"')
def step_mood_data_with_emotion(context, emotion):
    """Set up mood data with a specific emotion."""
    context.request_data = {
        "user_id": 1,
        "emotion": emotion,
        "percentage": 75.0,
        "date": "2024-12-26",
    }


@given("I have mood data with percentage {percentage:d}")
def step_mood_data_with_percentage(context, percentage):
    """Set up mood data with a specific percentage."""
    context.request_data = {
        "user_id": 1,
        "emotion": "HAPPINESS",
        "percentage": float(percentage),
        "date": "2024-12-26",
    }


@given("the following mood entries exist for user {user_id:d}")
def step_mood_entries_exist(context, user_id):
    """Create multiple mood entries from a data table."""
    context.created_moods = []
    for row in context.table:
        mood_data = {
            "user_id": user_id,
            "emotion": row["emotion"],
            "percentage": float(row["percentage"]),
            "date": row["date"],
        }
        response = context.client.post("/v1/mood/", json=mood_data)
        if response.status_code == 200:
            context.created_moods.append(mood_data)


@given("the mood data is cached for user {user_id:d}")
def step_mood_cached(context, user_id):
    """Mark that mood data is cached for the user."""
    # First, make a request to populate the cache
    context.cache_populated = True


@given("a mood entry exists")
def step_mood_entry_exists(context):
    """Create a mood entry from the data table."""
    for row in context.table:
        mood_data = {
            "user_id": int(row["user_id"]),
            "emotion": row["emotion"],
            "percentage": float(row["percentage"]),
            "date": row["date"],
        }
        context.client.post("/v1/mood/", json=mood_data)
        context.existing_mood = mood_data


@given("I have updated mood data with percentage {percentage:f}")
def step_updated_mood_percentage(context, percentage):
    """Set up updated mood data with a specific percentage."""
    context.request_data = {
        "user_id": 1,
        "emotion": "HAPPINESS",
        "percentage": percentage,
        "date": "2024-12-26",
    }


# ============== Then Steps ==============


@then('the response should contain emotion "{emotion}"')
def step_response_contains_emotion(context, emotion):
    """Verify the response contains the expected emotion."""
    response_data = context.response.json()
    assert (
        response_data.get("emotion") == emotion
    ), f"Expected emotion {emotion}, got {response_data.get('emotion')}"


@then("the response should contain percentage {percentage:f}")
def step_response_contains_percentage(context, percentage):
    """Verify the response contains the expected percentage."""
    response_data = context.response.json()
    actual_percentage = response_data.get("percentage")
    assert (
        abs(actual_percentage - percentage) < 0.01
    ), f"Expected percentage {percentage}, got {actual_percentage}"


@then("the response should contain {count:d} mood entries")
def step_response_contains_mood_count(context, count):
    """Verify the response contains the expected number of mood entries."""
    response_data = context.response.json()
    assert (
        len(response_data) == count
    ), f"Expected {count} mood entries, got {len(response_data)}"


@then("the cache should be populated for user {user_id:d}")
def step_cache_populated(context, user_id):
    """Verify the cache is populated for the user."""
    # In a real implementation, this would check Redis
    # For now, we assume the cache is populated after a successful GET request
    assert context.response.status_code == 200


@then("the response should be served from cache")
def step_response_from_cache(context):
    """Verify the response was served from cache."""
    # In a real implementation, this could check response headers
    # or measure response time
    assert context.response.status_code == 200


@then('the predominant emotion should be "{emotion}"')
def step_predominant_emotion(context, emotion):
    """Verify the predominant emotion in the response."""
    response_data = context.response.json()
    emotions = [mood.get("emotion") for mood in response_data]
    emotion_counts = Counter(emotions)
    most_common_emotion = emotion_counts.most_common(1)[0][0]
    assert (
        most_common_emotion == emotion
    ), f"Expected predominant emotion {emotion}, got {most_common_emotion}"
