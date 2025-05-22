# OpenAI Q&A GUI Tool

## Overview

This application provides a graphical user interface (GUI) for interacting with OpenAI's chat completion models. Users can input their API credentials and question, configure model parameters, and receive answers directly within the tool.

## Features

*   GUI for interacting with OpenAI's chat models.
*   User-configurable API parameters:
    *   API Key (securely masked in the input field)
    *   Base URL (defaults to `https://api.openai.com/v1`)
    *   Model Name (defaults to `gpt-3.5-turbo`)
*   Adjustable settings for Temperature and Max Response Length.
*   Displays AI's answers in a dedicated text area.
*   Provides status messages for ongoing operations, errors, and success.
*   Basic input validation for Temperature and Max Response Length.
*   API calls are made in a separate thread to keep the GUI responsive.

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
    Install the required Python packages using `pip`:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

Once the setup is complete and the virtual environment is activated, run the application using:

```bash
python app.py
```

This will launch the GUI window.

## How to Use

The GUI provides several fields to configure your API request:

*   **API Key**: Enter your OpenAI API key here. The input is masked for security.
*   **Base URL**: The base URL for the OpenAI API. It defaults to `https://api.openai.com/v1`. You generally don't need to change this unless you are using a proxy or a different API endpoint.
*   **Model Name**: Specify the model you want to use for generation (e.g., `gpt-3.5-turbo`, `gpt-4`, `gpt-4-turbo`). It defaults to `gpt-3.5-turbo`.
*   **Temperature**: This setting controls the randomness of the output. It accepts values between 0.0 and 2.0. Lower values (e.g., 0.2) make the output more deterministic and focused, while higher values (e.g., 0.8) make it more random and creative. The default is 0.7.
*   **Max Response Length**: This sets the maximum number of tokens (words and parts of words) that the AI will generate in its response. The default is 150 tokens. The valid range is between 1 and 8192.
*   **Your Question**: Type the question or prompt you want to send to the AI in this text area.

**Submitting a Question:**
After filling in the fields, click the "Submit" button.

**Getting Results:**
*   The AI's answer will appear in the "AI's Answer" text area.
*   The status bar at the bottom of the window will display messages like "Submitting...", "Done.", or any error messages encountered during the process.

## Running Tests

Unit tests are provided for the OpenAI API client logic. To run these tests, navigate to the project's root directory in your terminal (ensure your virtual environment is activated and dependencies are installed) and run:

```bash
python -m unittest test_openai_client.py
```

## Files

*   `app.py`: The main application file. It contains the Tkinter GUI code, event handling, and logic for interacting with the user and the `openai_client`.
*   `openai_client.py`: This module contains the `get_openai_response` function, which is responsible for making requests to the OpenAI API and handling potential errors.
*   `test_openai_client.py`: Contains unit tests for the `get_openai_response` function in `openai_client.py`.
*   `requirements.txt`: Lists the Python dependencies required for the project (currently, just `openai`).

---
This README provides a comprehensive guide for users and developers of the OpenAI Q&A GUI Tool.
