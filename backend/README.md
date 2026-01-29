# Spy Cat Agency Backend

REST API for managing spy cats, missions, and targets.

## Tech Stack

- FastAPI
- SQLite + SQLAlchemy
- Pydantic

## Quick Start

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload
```

API will be available at `http://localhost:8000`

Interactive docs: `http://localhost:8000/docs`

## API Endpoints

### Cats
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/cats` | Create cat (breed validated via TheCatAPI) |
| GET | `/cats` | List all cats |
| GET | `/cats/{id}` | Get single cat |
| PATCH | `/cats/{id}` | Update salary |
| DELETE | `/cats/{id}` | Delete cat |

### Missions
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/missions` | Create mission with 1-3 targets |
| GET | `/missions` | List all missions |
| GET | `/missions/{id}` | Get mission with targets |
| DELETE | `/missions/{id}` | Delete (if not assigned) |
| POST | `/missions/{id}/assign/{cat_id}` | Assign cat |
| PATCH | `/missions/{id}/targets/{target_id}` | Update target notes/complete |

## Business Rules

- **Breed Validation**: Cat breeds validated against TheCatAPI
- **One Mission Per Cat**: Cat can only have one active mission
- **Target Count**: Missions require 1-3 targets
- **Notes Freeze**: Cannot update notes if target or mission is completed
- **Auto-Complete**: Mission completes when all targets are completed
