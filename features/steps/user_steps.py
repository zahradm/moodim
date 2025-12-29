"""
Step definitions for User feature tests.
"""

from behave import given, then, when
from fastapi.testclient import TestClient


# ============== Given Steps ==============


@given("the API server is running")
def step_api_server_running(context):
    """Verify the API server is accessible."""
    assert context.client is not None


@given("the database is clean")
def step_database_clean(context):
    """Ensure the database is in a clean state."""
    # In a real implementation, this would truncate tables
    pass


@given("I have valid user data")
def step_valid_user_data(context):
    """Set up valid user data from the data table."""
    for row in context.table:
        context.request_data = {
            "email": row["email"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "password": row["password"],
        }


@given("I have user data with invalid email")
def step_user_data_invalid_email(context):
    """Set up user data with an invalid email."""
    for row in context.table:
        context.request_data = {
            "email": row["email"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "password": row["password"],
        }


@given("I have user data with weak password")
def step_user_data_weak_password(context):
    """Set up user data with a weak password."""
    for row in context.table:
        context.request_data = {
            "email": row["email"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "password": row["password"],
        }


@given('I have user data with password "{password}"')
def step_user_data_with_password(context, password):
    """Set up user data with a specific password."""
    context.request_data = {
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": password,
    }


@given("a user exists with id {user_id:d}")
def step_user_exists(context, user_id):
    """Create a user with the specified ID."""
    # Create a test user first
    user_data = {
        "email": f"user{user_id}@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "SecurePass123!",
    }
    response = context.client.post("/v1/users/", json=user_data)
    context.created_user_id = user_id


@given("the following users exist")
def step_multiple_users_exist(context):
    """Create multiple users from a data table."""
    for row in context.table:
        user_data = {
            "email": row["email"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "password": "SecurePass123!",
        }
        context.client.post("/v1/users/", json=user_data)


@given("I have updated user data")
def step_updated_user_data(context):
    """Set up updated user data from the data table."""
    for row in context.table:
        context.request_data = {
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "password": row["password"],
        }


# ============== When Steps ==============


@when('I send a POST request to "{endpoint}"')
def step_send_post_request(context, endpoint):
    """Send a POST request to the specified endpoint."""
    context.response = context.client.post(endpoint, json=context.request_data)


@when('I send a GET request to "{endpoint}"')
def step_send_get_request(context, endpoint):
    """Send a GET request to the specified endpoint."""
    context.response = context.client.get(endpoint)


@when('I send a PUT request to "{endpoint}"')
def step_send_put_request(context, endpoint):
    """Send a PUT request to the specified endpoint."""
    context.response = context.client.put(endpoint, json=context.request_data)


@when('I send a DELETE request to "{endpoint}"')
def step_send_delete_request(context, endpoint):
    """Send a DELETE request to the specified endpoint."""
    context.response = context.client.delete(endpoint)


# ============== Then Steps ==============


@then("the response status code should be {status_code:d}")
def step_check_status_code(context, status_code):
    """Verify the response status code."""
    assert (
        context.response.status_code == status_code
    ), f"Expected {status_code}, got {context.response.status_code}: {context.response.text}"


@then('the response should contain the user email "{email}"')
def step_response_contains_email(context, email):
    """Verify the response contains the expected email."""
    response_data = context.response.json()
    assert (
        response_data.get("email") == email
    ), f"Expected email {email}, got {response_data.get('email')}"


@then('the response should contain the first name "{first_name}"')
def step_response_contains_first_name(context, first_name):
    """Verify the response contains the expected first name."""
    response_data = context.response.json()
    assert (
        response_data.get("first_name") == first_name
    ), f"Expected first_name {first_name}, got {response_data.get('first_name')}"


@then('the response should contain the last name "{last_name}"')
def step_response_contains_last_name(context, last_name):
    """Verify the response contains the expected last name."""
    response_data = context.response.json()
    assert (
        response_data.get("last_name") == last_name
    ), f"Expected last_name {last_name}, got {response_data.get('last_name')}"


@then("the response should contain a validation error")
def step_response_contains_validation_error(context):
    """Verify the response contains a validation error."""
    response_data = context.response.json()
    assert "detail" in response_data, "Expected validation error in response"


@then("the response should contain a password validation error")
def step_response_contains_password_error(context):
    """Verify the response contains a password validation error."""
    response_data = context.response.json()
    assert "detail" in response_data, "Expected password validation error in response"


@then("the response should contain user details")
def step_response_contains_user_details(context):
    """Verify the response contains user details."""
    response_data = context.response.json()
    assert "email" in response_data, "Expected email in response"
    assert "first_name" in response_data, "Expected first_name in response"
    assert "last_name" in response_data, "Expected last_name in response"


@then('the response should contain "{message}"')
def step_response_contains_message(context, message):
    """Verify the response contains the expected message."""
    response_text = context.response.text
    assert (
        message in response_text
    ), f"Expected '{message}' in response, got: {response_text}"


@then("the response should contain {count:d} users")
def step_response_contains_user_count(context, count):
    """Verify the response contains the expected number of users."""
    response_data = context.response.json()
    assert (
        len(response_data) == count
    ), f"Expected {count} users, got {len(response_data)}"
