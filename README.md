# Spy Cat Agency Management System

A full-stack application for managing spy cats, their missions, and targets.

## Repositories

- **Backend**: `backend/`
- **Frontend**: `frontend/`

## API Documentation

A complete Postman collection is available here: [postman_collection.json](./postman_collection.json).
You can import this file directly into Postman to test all endpoints.

## Quick Start (Recommended)

Since the project uses modern versions of Node.js and Python, the easiest way to run it is via Docker.

**Important:** If you have any old files or build artifacts, it's best to clean them first.

```bash
# Clean up old containers and images (optional but recommended if you had errors)
docker-compose down --rmi all --volumes

# Build and run
docker-compose up --build
```

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Features

### Spy Cats Dashboard (Frontend)
- View all active spy cats in a premium dashboard
- Recruit new cats (with breed validation via TheCatAPI)
- Update cat salaries
- Retire (delete) cats from service
- Real-time animations and responsive design

### Backend API
- **Cats Management**: CRUD operations with validations
- **Mission Control**: Assign missions, update targets, freeze notes on completion
- **Business Logic**:
  - Validates breeds against [TheCatAPI](https://api.thecatapi.com/v1/breeds)
  - Prevents deleting missions assigned to cats
  - Auto-completes missions when all targets are done
  - Prevents editing notes on completed missions

## Manual Setup (Development)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Create .env file (optional, defaults provided in code)
echo "CAT_API_URL=https://api.thecatapi.com/v1/breeds" > .env
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```
*Note: Requires Node.js 20+*
