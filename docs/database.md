# Database Design (SQLite)

This document details the schema for the SQLite database used to persist all application data.

## 1. `conversations` Table

Stores the top-level information for each distinct conversation thread.

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `id` | INTEGER | **Primary Key** (Auto-incrementing) |
| `title` | TEXT | The title of the conversation. |
| `created_at`| TIMESTAMP | Timestamp of when the conversation was created. |
| `updated_at`| TIMESTAMP | Timestamp of the last update to the conversation. |

## 2. `messages` Table

Stores every message from both the user and the AI model. This table is the core of the branching logic.

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `id` | INTEGER | **Primary Key** (Auto-incrementing) |
| `conversation_id`| INTEGER | Foreign Key to `conversations.id`. |
| `parent_message_id`| INTEGER | Foreign Key to `messages.id`. This is the cornerstone of the tree structure, linking a message to its predecessor. A `NULL` value indicates it is a root message of a branch. |
| `role` | TEXT | The author of the message. Either "user" or "model". |
| `content` | TEXT | The main body of the message. |
| `node_summary`| TEXT | A brief, AI-generated summary of the message content, used for display in the tree view. |
| `created_at`| TIMESTAMP | Timestamp of when the message was created. |

## 3. `attached_files` Table

Stores metadata for files uploaded by the user.

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `id` | INTEGER | **Primary Key** (Auto-incrementing) |
| `message_id` | INTEGER | Foreign Key to `messages.id`, linking a file to a specific user message. |
| `file_name` | TEXT | The original name of the uploaded file. |
| `gemini_file_uri` | TEXT | The unique URI returned by the Google File API, used to reference the file in Gemini API calls. |
| `created_at`| TIMESTAMP | Timestamp of when the file was attached. |
