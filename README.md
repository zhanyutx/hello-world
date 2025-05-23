# OpenAI Q&A Web Application

## Overview

This application provides a web-based interface, powered by Streamlit, for interacting with OpenAI's chat completion models. Users can input their API credentials, configure model parameters, ask questions, and receive answers directly within the web application.

## Features

*   Web interface powered by Streamlit for interacting with OpenAI's chat models.
*   User-configurable API parameters located in the sidebar:
    *   **API Key**: Securely entered (input is masked).
    *   **Base URL**: Defaults to `https://api.openai.com/v1`.
    *   **Model Name**: Defaults to `gpt-3.5-turbo`.
*   Adjustable settings via interactive sliders in the sidebar:
    *   **Temperature**: Controls randomness (0.0 to 2.0).
    *   **Max Reply Length**: Sets maximum tokens for the response (50 to 8192).
*   Configuration Persistence: API Key, Base URL, and Model Name can be saved using the "Save Configuration" button in the sidebar. These are stored locally in a `config.json` file (base64 encoded).
*   Chat history is displayed in the main panel.
*   User input is provided via a chat input box at the bottom of the main panel.
*   Displays AI's responses in the chat history.
*   Provides error messages within the interface for issues like missing API keys or API call failures.
*   Input validation for Temperature and Max Reply Length is handled by the Streamlit sliders' range.

## Prerequisites

*   Python 3.x
*   An OpenAI API Key. You can obtain one from [OpenAI](https://platform.openai.com/account/api-keys).

## Setup and Installation

1.  **Clone the repository (optional):**
    If you have cloned this repository, navigate to its root directory. Otherwise, ensure all project files (`app.py`, `openai_client.py`, `requirements.txt`) are in the same directory.
    ```bash
    # Example if cloned:
    # git clone https://your-repository-url.git
    # cd your-repository-directory
    ```

2.  **Create a virtual environment (recommended):**
    It's highly recommended to use a virtual environment to manage project dependencies.

    *   Create the virtual environment:
        ```bash
        python -m venv venv
        ```
    *   Activate the virtual environment:
        *   On Linux/macOS:
            ```bash
            source venv/bin/activate
            ```
        *   On Windows:
            ```bash
            venv\Scripts\activate
            ```

3.  **Install dependencies:**
    Install the required Python packages using `pip`. The `requirements.txt` file includes `streamlit` and `openai`.
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

Once the setup is complete and the virtual environment is activated, run the application using:

```bash
streamlit run app.py
```

This will launch the web application in your default web browser.

## How to Use

The application interface is divided into a sidebar for configuration and a main panel for chat interaction.

**Configuration (Sidebar):**
All configuration options are located in the sidebar:

*   **API Key**: Enter your OpenAI API key here. The input is masked.
*   **Base URL**: The base URL for the OpenAI API. It defaults to `https://api.openai.com/v1`.
*   **Model Name**: Specify the model you want to use (e.g., `gpt-3.5-turbo`, `gpt-4`). Defaults to `gpt-3.5-turbo`.
*   **Temperature**: Adjust the slider to control the randomness of the output (0.0-2.0). Default is 0.7.
*   **Max Reply Length**: Adjust the slider to set the maximum number of tokens for the AI's response. Default is 150.
*   **Save Configuration**: Click this button to save the current API Key, Base URL, and Model Name to a local `config.json` file for future sessions. Temperature and Max Reply Length are not saved and will reset to their defaults.

**Chatting (Main Panel):**

*   **Entering a Question**: Type your question or prompt into the chat input box located at the bottom of the main panel and press Enter or click the send icon.
*   **Viewing Chat History**: Your messages and the AI's responses will appear sequentially in the main panel, creating a conversation history.
*   **Error Messages**: If there are issues (e.g., missing API key, API errors), error messages will be displayed within the chat interface or sidebar.

## Running Tests

Unit tests are provided for the OpenAI API client logic. To run these tests, navigate to the project's root directory in your terminal (ensure your virtual environment is activated and dependencies are installed) and run:

```bash
python -m unittest test_openai_client.py
```

## Files

*   `app.py`: The main application file, built with Streamlit, containing the UI and logic for the chat interface and configuration sidebar.
*   `openai_client.py`: This module contains the `get_openai_response` function, responsible for making requests to the OpenAI API and handling potential errors.
*   `test_openai_client.py`: Contains unit tests for the `get_openai_response` function in `openai_client.py`.
*   `requirements.txt`: Lists Python dependencies (`openai`, `streamlit`).
*   `config.json`: Stores the saved API Key, Base URL, and Model Name (base64 encoded). Automatically created when "Save Configuration" is used.

---
This README provides a comprehensive guide for users and developers of the OpenAI Q&A Web Application.
