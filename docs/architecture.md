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

## 4. Database Design (SQLite)

### 4.1. `conversations` Table
| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `id` | INTEGER | Primary Key (Auto-increment) |
| `title` | TEXT | Conversation title |
| `created_at`| TIMESTAMP | Creation timestamp |
| `updated_at`| TIMESTAMP | Last updated timestamp |

### 4.2. `messages` Table
| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `id` | INTEGER | Primary Key (Auto-increment) |
| `conversation_id`| INTEGER | Foreign key to `conversations.id` |
| `parent_message_id`| INTEGER | ID of the parent message (`messages.id`). Core of the tree structure. |
| `role` | TEXT | Speaker ("user" or "model") |
| `content` | TEXT | Message body |
| `node_summary`| TEXT | Summary text for overview (tree view) |
| `created_at`| TIMESTAMP | Creation timestamp |

### 4.3. `attached_files` Table
| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `id` | INTEGER | Primary Key (Auto-increment) |
| `message_id` | INTEGER | Foreign key to `messages.id` |
| `file_name` | TEXT | Original file name |
| `gemini_file_uri` | TEXT | Reference URI from Google File API |
| `created_at`| TIMESTAMP | Creation timestamp |

## 5. Technology Stack

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

## 6. Non-Functional Requirements

### 6.1. UI/UX Design
*   Adopts a clean, modern design inspired by Google's official Gemini web application.
*   Employs a responsive design for optimal use on both desktop and mobile devices.

### 6.2. Performance
*   AI responses are streamed via WebSocket to reduce perceived user wait times.
*   The user interface must be fast and responsive.

### 6.3. Execution Environment
*   The entire application stack is managed by Docker Compose for local execution.
*   Remote access is intended to be handled via VPN tunneling services like `Tailscale`, not requiring cloud deployment.

### 6.4. Data Management
*   All application data (conversations, branches, files) is stored in a single SQLite database file.
*   This database file is persisted on the host machine using a Docker volume mount to the `data/` directory.
