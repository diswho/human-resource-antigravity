# HR Management System

A modern, full-stack Human Resource management system with automated data migration from ZKTime Lite (SQLite) to a robust PostgreSQL database.

## ⚡ Technology Stack

- **Backend**: FastAPI (Python 3.12)
- **Database**: PostgreSQL with SQLModel (ORM)
- **Frontend**: React + Vite + TypeScript
- **Styling**: Tailwind CSS + shadcn/ui
- **Icons**: Lucide React
- **Reverse Proxy**: Traefik
- **Environment**: Docker & Docker Compose

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose installed
- `ZKTimeNet08.db` file in the root directory (for data migration)

### Installation & Setup

1. **Clone the repository** (if not already done).
2. **Configure Environment Variables**:
   Copy the example environment settings (or edit the existing `.env` file):
   ```bash
   # Make sure .env contains your database and secret key configs
   ```
3. **Build and Run with Docker Compose**:
   ```bash
   docker-compose up -d --build
   ```

### 🗄️ Database Initialization

After the containers are running, you must initialize the database schema and migrate initial data:

1. **Migrate Data from SQLite to Postgres**:
   ```bash
   docker-compose exec backend python -m app.migrate
   ```
   *This command creates the schema and imports departments, positions, employees, and the 10,000 most recent attendance logs.*

2. **Create Initial Admin User**:
   ```bash
   docker-compose exec backend python -m app.initial_data
   ```
   *Default user: `admin@example.com` / `changethis` (configurable in `.env`)*

## 🛠️ Development & Testing

### API Access

- **Web Dashboard**: [http://localhost](http://localhost)
- **API Documentation (Swagger UI)**: [http://localhost/docs](http://localhost/docs)
- **Direct Backend (Testing/Postman)**: [http://localhost:8000](http://localhost:8000)

### Database Management

The database port is exposed at `5432` for external tools (e.g., DBeaver):
- **Host**: `localhost`
- **Port**: `5432`
- **User/Pass**: See `.env` (`POSTGRES_USER`/`POSTGRES_PASSWORD`)

### Key Features Implemented

- **Automated Migration**: seamless sync from legacy ZKTime SQLite databases.
- **Modern Auth**: JWT-based authentication with secure password hashing (bcrypt).
- **Employee Management**: view and edit employee details synced from hardware logs.
- **Attendance Tracking**: browse and filter punch-in/out logs.
- **Dark Mode**: support for modern UI aesthetics.

## 📄 License

Internal Project - All Rights Reserved.
