# API Design

This document outlines the specifications for the REST and WebSocket APIs used in the application.

## 1. REST API

The REST API is responsible for managing conversations.

| Purpose | HTTP Method | URL | Description |
| :--- | :--- | :--- | :--- |
| **Get Conversation List** | `GET` | `/api/conversations` | Fetches a list of all conversations, returning their `id`, `title`, and `updated_at`. |
| **Get Single Conversation** | `GET` | `/api/conversations/{conversation_id}` | Retrieves all messages and their branching structure for a specific conversation. |
| **Delete Conversation** | `DELETE`| `/api/conversations/{conversation_id}` | Deletes an entire conversation, including all its messages and branches. |
| **Update Conversation Title**| `PUT` | `/api/conversations/{conversation_id}` | Updates the title of a specific conversation. The new title is sent in the request body. |

## 2. WebSocket API

The WebSocket API handles real-time chat communication.

*   **Endpoint**: `ws://your-domain/ws/chat/{conversation_id}`

### 2.1. Client-to-Server Messages

When a user sends a message, the client sends a JSON object with the following structure.

*   **Message Type**: `chat_message`

```json
{
  "type": "chat_message",
  "parent_message_id": "PARENT_MESSAGE_ID_IF_FORKING", // Optional
  "content": "User's message text",
  "files": [
    {
      "file_name": "example.pdf",
      "gemini_file_uri": "URI_FROM_GOOGLE_FILE_API"
    }
    // ... more files
  ]
}
```

### 2.2. Server-to-Client Messages

The server sends messages to the client to stream the AI's response.

*   **Message Type**: `stream_chunk`
    *   **Payload**: A piece of the AI's response.
    ```json
    {
      "type": "stream_chunk",
      "content": "... part of the AI response ..."
    }
    ```

*   **Message Type**: `stream_end`
    *   **Payload**: Indicates that the full response has been sent. Includes the final message object to be saved in the client's state.
    ```json
    {
      "type": "stream_end",
      "message": {
        "id": "NEW_MESSAGE_ID",
        "conversation_id": "CURRENT_CONVERSATION_ID",
        "parent_message_id": "PARENT_MESSAGE_ID",
        "role": "model",
        "content": "The complete AI response.",
        "node_summary": "AI-generated summary for tree view.",
        "created_at": "TIMESTAMP"
      }
    }
    ```
