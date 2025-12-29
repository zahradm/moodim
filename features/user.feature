Feature: User Management
    As an API consumer
    I want to manage user accounts
    So that users can be created, updated, retrieved, and deleted

    Background:
        Given the API server is running
        And the database is clean

    @user @create
    Scenario: Successfully create a new user
        Given I have valid user data:
            | email                | first_name | last_name | password       |
            | john.doe@example.com | John       | Doe       | SecurePass123! |
        When I send a POST request to "/v1/users/"
        Then the response status code should be 200
        And the response should contain the user email "john.doe@example.com"
        And the response should contain the first name "John"
        And the response should contain the last name "Doe"

    @user @create @validation
    Scenario: Fail to create user with invalid email
        Given I have user data with invalid email:
            | email           | first_name | last_name | password       |
            | invalid-email   | John       | Doe       | SecurePass123! |
        When I send a POST request to "/v1/users/"
        Then the response status code should be 422
        And the response should contain a validation error

    @user @create @validation
    Scenario: Fail to create user with weak password
        Given I have user data with weak password:
            | email                | first_name | last_name | password |
            | john.doe@example.com | John       | Doe       | weak     |
        When I send a POST request to "/v1/users/"
        Then the response status code should be 422
        And the response should contain a password validation error

    @user @create @validation
    Scenario Outline: Password validation rules
        Given I have user data with password "<password>"
        When I send a POST request to "/v1/users/"
        Then the response status code should be <status_code>

        Examples:
            | password        | status_code | reason                    |
            | Short1!         | 422         | Too short                 |
            | alllowercase1!  | 422         | Missing uppercase         |
            | ALLUPPERCASE1!  | 422         | Missing lowercase         |
            | NoDigitsHere!   | 422         | Missing digit             |
            | NoSpecial123    | 422         | Missing special character |
            | ValidPass123!   | 200         | All requirements met      |

    @user @get
    Scenario: Successfully retrieve an existing user
        Given a user exists with id 1
        When I send a GET request to "/v1/users/1"
        Then the response status code should be 200
        And the response should contain user details

    @user @get
    Scenario: Fail to retrieve non-existing user
        When I send a GET request to "/v1/users/9999"
        Then the response status code should be 404
        And the response should contain "User not found"

    @user @list
    Scenario: Successfully retrieve all users
        Given the following users exist:
            | email                 | first_name | last_name |
            | user1@example.com     | User       | One       |
            | user2@example.com     | User       | Two       |
        When I send a GET request to "/v1/users/"
        Then the response status code should be 200
        And the response should contain 2 users

    @user @update
    Scenario: Successfully update user information
        Given a user exists with id 1
        And I have updated user data:
            | first_name | last_name | password       |
            | Jane       | Smith     | NewSecure123!  |
        When I send a PUT request to "/v1/users/1"
        Then the response status code should be 200
        And the response should contain the first name "Jane"
        And the response should contain the last name "Smith"

    @user @delete
    Scenario: Successfully delete a user
        Given a user exists with id 1
        When I send a DELETE request to "/v1/users/1"
        Then the response status code should be 200
        And the response should contain "User deleted successfully"

    @user @delete
    Scenario: Fail to delete non-existing user
        When I send a DELETE request to "/v1/users/9999"
        Then the response status code should be 404
        And the response should contain "User not found"
