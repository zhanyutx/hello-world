import streamlit as st
import json
import os
import base64
from openai_client import get_openai_response

CONFIG_FILE = "config.json"

# --- Configuration Loading and Saving ---
def load_config_from_file():
    """Loads configuration from JSON file and decodes it."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                encoded_config = f.read()
                if encoded_config:
                    decoded_bytes = base64.b64decode(encoded_config)
                    decoded_str = decoded_bytes.decode('utf-8')
                    return json.loads(decoded_str)
        except (json.JSONDecodeError, ValueError, TypeError, base64.binascii.Error) as e:
            st.error(f"Error loading or decoding config file: {e}. Using defaults.")
            return {} # Return empty dict to use defaults
    return {} # No file or empty file, use defaults

def save_config_to_file(api_key, base_url, model_name):
    """Encodes and saves configuration to JSON file."""
    config = {
        "api_key": api_key,
        "base_url": base_url,
        "model_name": model_name
    }
    try:
        config_str = json.dumps(config)
        encoded_config = base64.b64encode(config_str.encode('utf-8')).decode('utf-8')
        with open(CONFIG_FILE, 'w') as f:
            f.write(encoded_config)
        st.sidebar.success("Configuration saved!")
    except Exception as e:
        st.sidebar.error(f"Error saving configuration: {e}")

# --- Initialize session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Load initial config from file or set defaults
loaded_config_values = load_config_from_file()

# Set session state from loaded config or defaults, only if not already set by user interaction
if "api_key" not in st.session_state:
    st.session_state.api_key = loaded_config_values.get("api_key", "")
if "base_url" not in st.session_state:
    st.session_state.base_url = loaded_config_values.get("base_url", "https://api.openai.com/v1")
if "model_name" not in st.session_state:
    st.session_state.model_name = loaded_config_values.get("model_name", "gpt-3.5-turbo")

# For temperature and max_length, we don't save them in config.json,
# so we just initialize them if they are not in session_state yet.
# Default values are used here directly.
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7
if "max_reply_length" not in st.session_state:
    st.session_state.max_reply_length = 150


# --- Sidebar for Configuration ---
st.sidebar.title("Configuration")

# Update session state directly from sidebar widgets
# The widgets' values will be the source of truth for these session state keys after first render.
st.session_state.api_key = st.sidebar.text_input(
    "API Key",
    type="password",
    value=st.session_state.api_key,
    key="sidebar_api_key" # Use a key to ensure widget state is managed correctly
)
st.session_state.base_url = st.sidebar.text_input(
    "Base URL",
    value=st.session_state.base_url,
    key="sidebar_base_url"
)
st.session_state.model_name = st.sidebar.text_input(
    "Model Name",
    value=st.session_state.model_name,
    key="sidebar_model_name"
)
st.session_state.temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0, max_value=2.0,
    value=float(st.session_state.temperature), # Ensure value is float for slider
    step=0.1,
    key="sidebar_temperature"
)
st.session_state.max_reply_length = st.sidebar.slider(
    "Max Reply Length",
    min_value=50, max_value=8192,
    value=int(st.session_state.max_reply_length), # Ensure value is int for slider
    step=10,
    key="sidebar_max_reply_length"
)

if st.sidebar.button("Save Configuration"):
    save_config_to_file(
        st.session_state.api_key,
        st.session_state.base_url,
        st.session_state.model_name
    )

# --- Main Chat Interface ---
st.title("OpenAI Chat Client (Streamlit)")

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to ask?"):
    # Validate inputs
    if not st.session_state.api_key:
        st.error("API Key is required. Please enter it in the sidebar.")
    elif not st.session_state.base_url:
        st.error("Base URL is required. Please enter it in the sidebar.")
    elif not st.session_state.model_name:
        st.error("Model Name is required. Please enter it in the sidebar.")
    elif not prompt:
        st.error("Prompt cannot be empty.")
    else:
        # Add user message to chat history and display it
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get AI response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Thinking...")
            
            ai_response = get_openai_response(
                api_key=st.session_state.api_key,
                base_url=st.session_state.base_url,
                model_name=st.session_state.model_name,
                prompt=prompt,
                temperature=st.session_state.temperature,
                max_tokens=st.session_state.max_reply_length
            )
            
            if ai_response.startswith("Error:"):
                st.error(f"API Error: {ai_response}")
                message_placeholder.markdown(f"Error: Could not get response. {ai_response}")
                # Optionally remove the placeholder or keep it to show error in place
                # If we want to add the error as a message in history:
                st.session_state.messages.append({"role": "assistant", "content": f"API Error: {ai_response}"})

            else:
                message_placeholder.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})

# For debugging session state (optional)
# st.sidebar.subheader("Session State")
# st.sidebar.json(st.session_state)
