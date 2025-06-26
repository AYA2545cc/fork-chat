# Application Architecture

## 1. System Architecture

The application runs entirely within Docker containers on the user's local machine. It consists of a Next.js frontend and a FastAPI backend. All data is persisted in a SQLite database on a mounted volume.

### 1.1. System Diagram

```plaintext
[User's Browser (PC/Mobile)] via Tailscale
       ↑
       | (HTTP / WebSocket)
       ↓
+-------------------------------------------------------------+
| Docker on User's PC                                         |
|                                                             |
|  +---------------------+        +-------------------------+ |
|  | Frontend (Next.js)  |  <=>   | Backend (FastAPI)       | |
|  | Port: 3000          |        | Port: 8000              | |
|  +---------------------+        +-------------------------+ |
|                                       ↑      |              |
|                                       |      | (Gemini API) |
|                                       |      ↓              |
|  +---------------------------------+  |  [Google Cloud]    |
|  | data/ (Mounted Volume)          |  |                    |
|  |  - chat_database.sqlite         |--+                    |
|  |  - uploaded_files/              |                      |
|  +---------------------------------+                      |
|                                                             |
+-------------------------------------------------------------+
```

## 2. Technology Stack

| Category | Technology/Library | Role |
| :--- | :--- | :--- |
| **Frontend** | Next.js (React) | UI/UX Development |
| **UI Components**| Tailwind CSS + Shadcn/ui | Modern UI Implementation |
| **Tree View** | React Flow | Rendering the conversation tree |
| **Backend** | FastAPI (Python) | API Server, Business Logic |
| **Database** | SQLite | Data Persistence |
| **DB Interaction (ORM)** | SQLAlchemy | Database operations in Python |
| **Real-time Communication**| WebSocket | Streaming AI responses |
| **Multimodal** | Google AI Python SDK (File API) | File uploads and analysis |
| **Execution Environment** | Docker Compose | Container orchestration |

## 3. Non-Functional Requirements

### 3.1. UI/UX Design
*   Adopts a clean, modern design inspired by Google's official Gemini web application.
*   Employs a responsive design for optimal use on both desktop and mobile devices.

### 3.2. Performance
*   AI responses are streamed via WebSocket to reduce perceived user wait times.
*   The user interface must be fast and responsive.

### 3.3. Execution Environment
*   The entire application stack is managed by Docker Compose for local execution.
*   Remote access is intended to be handled via VPN tunneling services like `Tailscale`, not requiring cloud deployment.

### 3.4. Data Management
*   All application data (conversations, branches, files) is stored in a single SQLite database file.
*   This database file is persisted on the host machine using a Docker volume mount to the `data/` directory.
