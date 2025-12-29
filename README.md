# Moodim

A mood tracking API built with FastAPI following clean architecture principles.

## Overview

Moodim is a RESTful API that allows users to track their emotional moods over time. The application implements clean architecture patterns, separating concerns into distinct layers for better maintainability and testability.

## Features

- 👤 **User Management**: Create, read, update, and delete users
- 😊 **Mood Tracking**: Record and track emotional moods (HAPPINESS, SADNESS, FEAR, ANGER)
- 📊 **Mood History**: Retrieve mood data for specific date ranges
- ⚡ **Redis Caching**: Fast mood retrieval with automatic cache invalidation
- 🏗️ **Clean Architecture**: Layered architecture with clear separation of concerns
- 🧪 **BDD Testing**: Behavior-driven development tests with Behave

## Project Structure

```
src/
├── configs/         # Configuration management
│   ├── runtime_config.py
│   ├── containers.py
│   └── dispatcher.py
├── controllers/     # API endpoints and request handling
│   ├── user/
│   │   └── v1/
│   └── mood/
│       └── v1/
├── logics/          # Business logic layer
│   ├── user/
│   └── mood/
├── models/          # Data models and schemas
│   ├── dtos/        # Data Transfer Objects
│   │   ├── user/
│   │   │   ├── domain/
│   │   │   └── repository/
│   │   └── mood/
│   │       ├── domain/
│   │       └── repository/
│   ├── entities/    # Database entities
│   └── types/       # Type definitions
├── repositories/    # Data access layer
│   ├── user/
│   │   └── adapters/
│   └── mood/
│       └── adapters/
├── utils/           # Utility functions
└── tests/           # Unit tests

features/            # BDD tests with Behave
├── user.feature
├── mood.feature
├── environment.py
└── steps/

docs/                # Documentation
├── data_model.puml
├── sequence_user_registration.puml
└── sequence_mood_tracking.puml
```

## Prerequisites

- Python 3.10+
- PostgreSQL 14+
- Redis 7+
- Poetry (for dependency management)
- Docker (optional)

## Getting Started

### 1. Setup the environment

```bash
# Install prerequisites
make setup

# Install project dependencies
make install

# Or for development dependencies:
make install-dev
```

### 2. Configure your environment

Create or update the configuration files:
- `src/core/settings.toml` - General settings
- `src/core/.secrets.toml` - Database credentials

### 3. Start dependencies

```bash
# Start PostgreSQL and Redis
make docker-up
```

### 4. Run migrations

```bash
make migrate
```

### 5. Run the application

```bash
make run
```

The API will be available at http://localhost:8000.

## API Documentation

Once running, access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### API Endpoints

#### Users
- `POST /api/v1/users/` - Create a new user
- `GET /api/v1/users/` - List all users
- `GET /api/v1/users/{user_id}` - Get user by ID
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

#### Moods
- `POST /api/v1/moods/` - Create a mood entry
- `GET /api/v1/moods/{user_id}/{start_date}/{end_date}` - Get mood history
- `PUT /api/v1/moods/{user_id}/{date}/{emotion}` - Update mood entry
- `DELETE /api/v1/moods/{user_id}/{date}` - Delete mood entries

## Development

```bash
# Format code
make format

# Run linters
make lint

# Run unit tests
make test

# Run tests with coverage
make test-cov

# Run BDD tests
make behave

# Run pre-commit hooks
make pre-commit

# Clean build artifacts
make clean
```

## Architecture

This project follows a clean architecture pattern with the following layers:

1. **Controllers** - Handle HTTP requests and responses
2. **Logics** - Business logic and orchestration
3. **Repositories** - Data access abstraction
4. **Adapters** - Concrete implementations for data sources

### Data Flow

```
Request → Controller → Logic → Repository → Adapter → Database
                                    ↓
                                  Cache
```

## Documentation

PlantUML diagrams are available in the `docs/` folder:

- `data_model.puml` - Entity-Relationship diagram
- `sequence_user_registration.puml` - User registration flow
- `sequence_mood_tracking.puml` - Mood tracking with caching

Generate SVG diagrams:
```bash
make docs
```

## Testing

### Unit Tests
```bash
make test
```

### BDD Tests
```bash
make behave
```

## License

This project is licensed under the MIT License.
