# Moodim Documentation

This folder contains PlantUML diagrams documenting the Moodim application architecture and flows.

## Diagrams

### 1. Data Model (`data_model.puml`)
Entity-Relationship diagram showing the database schema including:
- **User** entity with all fields and validation rules
- **Mood** entity with caching notes
- **EmotionEnum** enumeration
- Relationships between entities

### 2. User Registration Flow (`sequence_user_registration.puml`)
Sequence diagram documenting the complete user registration process:
- Request validation using Pydantic
- Password validation rules
- Database insertion
- Error handling scenarios
- Response serialization

### 3. Mood Tracking Flow (`sequence_mood_tracking.puml`)
Sequence diagram showing mood tracking operations with Redis caching:
- Insert new mood entries
- Get mood history (with cache hit/miss scenarios)
- Update mood percentage
- Cache strategy and TTL configuration

## Rendering Diagrams

### Using PlantUML Online
1. Go to [PlantUML Web Server](http://www.plantuml.com/plantuml/uml/)
2. Copy the content of any `.puml` file
3. The diagram will render automatically

### Using VS Code
1. Install the "PlantUML" extension
2. Open any `.puml` file
3. Press `Alt+D` to preview the diagram

### Using Command Line
```bash
# Install PlantUML
sudo apt-get install plantuml

# Generate PNG images
plantuml docs/*.puml

# Generate SVG images
plantuml -tsvg docs/*.puml
```

### Using Docker
```bash
docker run -v $(pwd)/docs:/data plantuml/plantuml *.puml
```

## Architecture Overview

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│    Client    │────>│   FastAPI    │────>│  Controller  │
└──────────────┘     │   Router     │     └──────────────┘
                     └──────────────┘            │
                                                 ▼
                     ┌──────────────┐     ┌──────────────┐
                     │    Redis     │<───>│    Logic     │
                     │    Cache     │     │    Layer     │
                     └──────────────┘     └──────────────┘
                                                 │
                                                 ▼
                                          ┌──────────────┐
                                          │  PostgreSQL  │
                                          │   Database   │
                                          └──────────────┘
```
