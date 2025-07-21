# Fork Chat: Gemini API Powered Conversational Chat Application

## 1. Project Overview

This is a web-based chat application for personal use that utilizes the Google Gemini API. Its core feature allows users to branch conversations from any point in the dialogue history, enabling exploration of different conversational paths.

## 2. Core Features

*   **Standard Chat Functionality**: Engage in one-on-one conversations with the Gemini AI.
*   **Conversation Forking**: Right-click (or long-press on mobile) any message to start a new conversation branch from that point.
*   **Tree View**: Visualize the entire branching structure of a conversation.
*   **Multimodal Inpu**: Interact with the AI by attaching PDF or image files.

## 3. Getting Started (Local Execution)

This application is managed using Docker Compose. To run it on your local machine, follow these steps:

1.  **Prerequisites**:
    *   Docker and Docker Compose must be installed on your system.
    *   A Google Gemini API key is required.

2.  **Configuration**:
    *   Copy the example environment file:
        ```bash
        cp .env.example .env
        ```
    *   Add your Gemini API key to the `.env` file:
        ```
        GEMINI_API_KEY="YOUR_API_KEY_HERE"
        ```

3.  **Running the Application**:
    *   Execute the following command in the project root directory:
        ```bash
        docker-compose up -d --build
        ```

4.  **Accessing the Application**:
    *   Once the containers are running, open your web browser and navigate to `http://localhost:3000`.

5.  **Stopping the Application**:
    *   To stop the application, run:
        ```bash
        docker-compose down
        ```

## 4. Documentation

The `docs/` directory contains detailed documentation for the project:

*   **`architecture.md`**: Overview of the system architecture, technology stack, non-functional requirements, and database design.
*   **`api_design.md`**: Specifications for the REST and WebSocket APIs.
*   **`coding_guide.md`**: Coding conventions and development process for AI agents.
*   **`development_guide.md`**: Instructions for setting up the development environment and key development practices.
*   **`requirements.md`**: Functional and non-functional requirements of the chat application.
