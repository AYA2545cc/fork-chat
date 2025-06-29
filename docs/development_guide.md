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

To maintain code quality and consistency across the project, the following linters and formatters are used.

### 3.1. Python (Backend)

*   **Tool**: `ruff`
*   **Purpose**: Enforces PEP 8 compliant coding style and detects common errors and potential issues. It also covers import sorting (`isort`) and naming conventions (`pep8-naming`).
*   **Configuration**: Configured in `pyproject.toml`. Key settings are as follows:
    ```toml
    [tool.ruff]
    line-length = 88
    target-version = "py310"
    select = ["E", "F", "W", "I", "N", "D"] # Errors, Flake8, Warnings, Isort, Naming, Docstrings
    ignore = ["D100", "D104", "D105", "D107"] # Missing docstrings for modules, packages, functions, __init__
    ```
    *   `line-length`: Sets the maximum line length to 88 characters.
    *   `target-version`: Targets Python 3.10.
    *   `select`: Specifies the rule sets to enable.
        *   `E`: pycodestyle errors
        *   `F`: Pyflakes errors
        *   `W`: pycodestyle warnings
        *   `I`: isort (import sorting)
        *   `N`: pep8-naming (naming conventions)
        *   `D`: pydocstyle (Docstring)
    *   `ignore`: Ignores specific Docstring-related rules (`D100`, `D104`, `D105`, `D107`).
*   **Usage**:
    *   Check only: `ruff check .`
    *   Auto-fix: `ruff check . --fix`
    *   Format: `ruff format .`

### 3.2. TypeScript/React (Frontend)

*   **Tools**: `ESLint` (Linter), `Prettier` (Formatter)
*   **Purpose**: Adheres to TypeScript and React best practices, ensuring code quality and consistency. Prettier automatically formats code, reducing style-related discussions.
*   **Configuration**:
    *   **ESLint**: Based on `eslint-config-next` as configured in `frontend/package.json`.
    *   **Prettier**: Uses default settings, with `eslint-config-prettier` applied to avoid conflicts with ESLint.
*   **Usage**:
    *   Linter check: `npm run lint` (run inside `frontend` directory)
    *   Formatter run: `npm run format` (run inside `frontend` directory)

### 3.3. IDE/Editor Integration (VS Code Recommended Settings)

To enhance the development experience, the following VS Code settings are recommended:

1.  **Install Extensions**:
    *   `Python` (Microsoft)
    *   `Ruff` (charliermarsh)
    *   `ESLint` (Microsoft)
    *   `Prettier - Code formatter` (Prettier)
2.  **Add Settings (settings.json)**:
    ```json
    {
      "editor.formatOnSave": true,
      "editor.defaultFormatter": "esbenp.prettier-vscode",
      "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff"
      },
      "eslint.validate": [
        "javascript",
        "javascriptreact",
        "typescript",
        "typescriptreact"
      ]
    }
    ```
    *   `editor.formatOnSave`: Automatically formats the file on save.
    *   `editor.defaultFormatter`: Sets Prettier as the default formatter.
    *   `[python]`: For Python files, sets Ruff as the default formatter.
    *   `eslint.validate`: Specifies the language modes ESLint should validate.

*   **Naming**: Use clear and descriptive names for variables, functions, and classes.
