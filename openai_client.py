import openai
import os

def get_openai_response(api_key: str, base_url: str, model_name: str, prompt: str, temperature: float, max_tokens: int) -> str:
    """
    Interacts with the OpenAI API to get a response to a given prompt.

    Args:
        api_key: The OpenAI API key.
        base_url: The base URL for the OpenAI API.
        model_name: The name of the model to use.
        prompt: The user's question or prompt.
        temperature: The sampling temperature to use.
        max_tokens: The maximum number of tokens to generate in the response.

    Returns:
        The AI's response as a string, or an error message if an API call fails.
    """
    try:
        client = openai.OpenAI(
            api_key=api_key,
            base_url=base_url,
        )

        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()
    except openai.APIConnectionError as e:
        error_message = f"Failed to connect to OpenAI API: {e}"
        print(error_message)
        return f"Error: {error_message}"
    except openai.AuthenticationError as e:
        error_message = f"OpenAI API authentication failed: {e}"
        print(error_message)
        return f"Error: {error_message}"
    except openai.RateLimitError as e:
        error_message = f"OpenAI API request exceeded rate limit: {e}"
        print(error_message)
        return f"Error: {error_message}"
    except openai.BadRequestError as e:
        error_message = f"OpenAI API request was invalid: {e}"
        print(error_message)
        return f"Error: {error_message}"
    except openai.APIError as e:
        error_message = f"An unexpected error occurred with the OpenAI API: {e}"
        print(error_message)
        return f"Error: {error_message}"
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        print(error_message)
        return f"Error: {error_message}"

if __name__ == '__main__':
    # Example usage (requires OPENAI_API_KEY environment variable to be set)
    # This is for testing the openai_client.py directly.
    # In the main application, the API key will be passed from the GUI.
    print("Testing get_openai_response function...")
    api_key_env = os.getenv("OPENAI_API_KEY")
    if not api_key_env:
        print("Error: OPENAI_API_KEY environment variable not set. Cannot run test.")
    else:
        test_prompt = "What is the capital of France?"
        print(f"Prompt: {test_prompt}")
        response = get_openai_response(
            api_key=api_key_env,
            base_url="https://api.openai.com/v1",
            model_name="gpt-3.5-turbo",
            prompt=test_prompt,
            temperature=0.7,
            max_tokens=50
        )
        print(f"Response: {response}")

        test_prompt_error = "This is a test prompt that should hopefully not cause a direct API error but tests the function."
        # Test with an invalid API key to trigger AuthenticationError
        print(f"\nTesting with an invalid API key...")
        response_auth_error = get_openai_response(
            api_key="invalid_key",
            base_url="https://api.openai.com/v1",
            model_name="gpt-3.5-turbo",
            prompt=test_prompt_error,
            temperature=0.7,
            max_tokens=50
        )
        print(f"Response (Auth Error): {response_auth_error}")

        # Test with an invalid model to trigger BadRequestError (though this might sometimes be caught by APIError or AuthenticationError depending on exact OpenAI client behavior)
        # For a more direct BadRequestError, one might need to send malformed request parameters.
        # Let's try an invalid model name.
        print(f"\nTesting with an invalid model name...")
        response_model_error = get_openai_response(
            api_key=api_key_env, # Assuming this is valid
            base_url="https://api.openai.com/v1",
            model_name="invalid-model-does-not-exist",
            prompt=test_prompt_error,
            temperature=0.7,
            max_tokens=50
        )
        print(f"Response (Invalid Model): {response_model_error}")
