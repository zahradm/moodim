Feature: Mood Tracking
    As a user of the Moodim application
    I want to track my emotional moods
    So that I can monitor my emotional well-being over time

    Background:
        Given the API server is running
        And the database is clean
        And Redis cache is available
        And a user exists with id 1

    @mood @create
    Scenario: Successfully record a new mood entry
        Given I have valid mood data:
            | user_id | emotion   | percentage | date       |
            | 1       | HAPPINESS | 85.5       | 2024-12-26 |
        When I send a POST request to "/v1/mood/"
        Then the response status code should be 200
        And the response should contain emotion "HAPPINESS"
        And the response should contain percentage 85.5

    @mood @create @validation
    Scenario Outline: Record different emotion types
        Given I have mood data with emotion "<emotion>"
        When I send a POST request to "/v1/mood/"
        Then the response status code should be <status_code>

        Examples:
            | emotion   | status_code |
            | HAPPINESS | 200         |
            | SADNESS   | 200         |
            | FEAR      | 200         |
            | ANGER     | 200         |
            | INVALID   | 422         |

    @mood @create @validation
    Scenario: Fail to create mood with invalid percentage
        Given I have mood data with percentage 150
        When I send a POST request to "/v1/mood/"
        Then the response status code should be 422
        And the response should contain a validation error

    @mood @get @cache
    Scenario: Retrieve mood history for a date range
        Given the following mood entries exist for user 1:
            | emotion   | percentage | date       |
            | HAPPINESS | 80.0       | 2024-12-24 |
            | SADNESS   | 30.0       | 2024-12-25 |
            | HAPPINESS | 90.0       | 2024-12-26 |
        When I send a GET request to "/v1/mood/1/2024-12-24/2024-12-26"
        Then the response status code should be 200
        And the response should contain 3 mood entries
        And the cache should be populated for user 1

    @mood @get @cache
    Scenario: Retrieve mood history from cache
        Given the following mood entries exist for user 1:
            | emotion   | percentage | date       |
            | HAPPINESS | 75.0       | 2024-12-26 |
        And the mood data is cached for user 1
        When I send a GET request to "/v1/mood/1/2024-12-26/2024-12-26"
        Then the response status code should be 200
        And the response should be served from cache

    @mood @get
    Scenario: Fail to retrieve moods for non-existing user
        When I send a GET request to "/v1/mood/9999/2024-12-01/2024-12-31"
        Then the response status code should be 404
        And the response should contain "Mood not found"

    @mood @get
    Scenario: Return empty result for date range with no moods
        When I send a GET request to "/v1/mood/1/2020-01-01/2020-01-31"
        Then the response status code should be 404
        And the response should contain "Mood not found"

    @mood @update
    Scenario: Successfully update a mood entry
        Given a mood entry exists:
            | user_id | emotion   | percentage | date       |
            | 1       | HAPPINESS | 70.0       | 2024-12-26 |
        And I have updated mood data with percentage 95.0
        When I send a PUT request to "/v1/mood/1/2024-12-26/HAPPINESS"
        Then the response status code should be 200
        And the response should contain percentage 95.0

    @mood @update
    Scenario: Fail to update non-existing mood entry
        Given I have updated mood data with percentage 50.0
        When I send a PUT request to "/v1/mood/9999/2024-12-26/HAPPINESS"
        Then the response status code should be 404
        And the response should contain "Mood not found"

    @mood @delete
    Scenario: Successfully delete mood entries for a date
        Given a mood entry exists:
            | user_id | emotion   | percentage | date       |
            | 1       | HAPPINESS | 80.0       | 2024-12-26 |
        When I send a DELETE request to "/v1/mood/1/2024-12-26"
        Then the response status code should be 200
        And the response should contain "Mood deleted successfully"

    @mood @delete
    Scenario: Fail to delete moods for non-existing date
        When I send a DELETE request to "/v1/mood/1/2020-01-01"
        Then the response status code should be 404
        And the response should contain "User not found"

    @mood @analytics
    Scenario: Track mood patterns over a week
        Given the following mood entries exist for user 1:
            | emotion   | percentage | date       |
            | HAPPINESS | 60.0       | 2024-12-20 |
            | HAPPINESS | 70.0       | 2024-12-21 |
            | SADNESS   | 40.0       | 2024-12-22 |
            | HAPPINESS | 80.0       | 2024-12-23 |
            | HAPPINESS | 85.0       | 2024-12-24 |
            | FEAR      | 30.0       | 2024-12-25 |
            | HAPPINESS | 90.0       | 2024-12-26 |
        When I send a GET request to "/v1/mood/1/2024-12-20/2024-12-26"
        Then the response status code should be 200
        And the response should contain 7 mood entries
        And the predominant emotion should be "HAPPINESS"
