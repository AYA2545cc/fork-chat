# Developer Guide

This guide provides instructions for setting up the development environment and outlines key development practices.

## 1. Environment Setup (Docker)

The entire application is containerized using Docker Compose, simplifying the setup process.

### 1.1. Prerequisites

*   **Docker & Docker Compose**: Ensure they are installed on your system.
*   **Google API Key**: You must have a valid Google API key with the Gemini API enabled.

### 1.2. Configuration

1.  **Clone the Repository**: `git clone [repository-url]`
2.  **Create Environment File**: In the project root, create a file named `.env`.
3.  **Set API Key**: Add your Google API key to the `.env` file. This key is passed to the backend service.
    ```
    GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    ```

### 1.3. Running the Application

*   **Build and Start**: Run the following command from the project root. The `-d` flag runs the containers in detached mode.
    ```bash
    docker-compose up --build -d
    ```
*   **Access**: 
    *   Frontend: `http://localhost:3000`
    *   Backend API: `http://localhost:8000/docs` (for FastAPI Swagger UI)

### 1.4. Common Docker Commands

*   **Stop Containers**: `docker-compose down`
*   **View Logs**: `docker-compose logs -f [service_name]` (e.g., `backend`, `frontend`)
*   **Access a Service Shell**: `docker-compose exec [service_name] bash`

## 2. Project Structure

```
/Users/aya/sandbox/gemini_project/fork_chat/
├── .gemini/
├── data/                     # Persisted data (mounted volume)
│   ├── chat_database.sqlite
│   └── uploaded_files/
├── docs/
│   ├── architecture.md
│   ├── api_design.md
│   ├── database.md
│   ├── development_guide.md
│   └── requirements.md
├── backend/                  # FastAPI Application
│   ├── app/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                 # Next.js Application
│   ├── app/
│   ├── public/
│   ├── Dockerfile
│   └── package.json
├── .env                      # Local environment variables (Git-ignored)
├── docker-compose.yml        # Docker Compose configuration
└── README.md                 # Project overview and setup
```

## 3. Coding Style & Conventions

*   **Python (Backend)**: Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) standards. Use a linter like `ruff` or `flake8` to enforce consistency.
*   **TypeScript/React (Frontend)**: Adhere to standard TypeScript and React best practices. Use a formatter like `Prettier`.
*   **Naming**: Use clear and descriptive names for variables, functions, and classes.
