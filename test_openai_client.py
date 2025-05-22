import unittest
from unittest.mock import patch, Mock
from openai_client import get_openai_response
import openai # To reference openai specific exceptions
import httpx # Required for mocking response objects for exceptions

class TestOpenAIClient(unittest.TestCase):

    @patch('openai_client.openai.OpenAI')
    def test_get_openai_response_success(self, mock_openai_class):
        mock_client_instance = mock_openai_class.return_value
        mock_response_obj = Mock()
        mock_response_obj.choices = [Mock()]
        mock_response_obj.choices[0].message = Mock()
        mock_response_obj.choices[0].message.content = "Test response content"
        mock_client_instance.chat.completions.create.return_value = mock_response_obj

        api_key = "test_key"
        base_url = "test_url"
        model_name = "test_model"
        prompt = "Test prompt"
        temperature = 0.5
        max_tokens = 100

        response = get_openai_response(api_key, base_url, model_name, prompt, temperature, max_tokens)

        self.assertEqual(response, "Test response content")
        mock_openai_class.assert_called_once_with(api_key=api_key, base_url=base_url)
        mock_client_instance.chat.completions.create.assert_called_once_with(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )

    def _prepare_mock_http_response(self, status_code):
        mock_http_response = Mock(spec=httpx.Response)
        mock_http_response.status_code = status_code
        mock_http_response.headers = Mock()
        mock_http_response.headers.get.return_value = "test-request-id" # For x-request-id
        # Add a request attribute to the response, as APIStatusError might try to access it.
        mock_http_response.request = Mock(spec=httpx.Request)
        return mock_http_response

    @patch('openai_client.openai.OpenAI')
    def test_get_openai_response_authentication_error(self, mock_openai_class):
        mock_client_instance = mock_openai_class.return_value
        mock_http_response = self._prepare_mock_http_response(401)
        mock_client_instance.chat.completions.create.side_effect = openai.AuthenticationError(message="Auth error", response=mock_http_response, body=None)

        response = get_openai_response("key", "url", "model", "prompt", 0.5, 100)
        self.assertTrue(response.startswith("Error: OpenAI API authentication failed:"))

    @patch('openai_client.openai.OpenAI')
    def test_get_openai_response_rate_limit_error(self, mock_openai_class):
        mock_client_instance = mock_openai_class.return_value
        mock_http_response = self._prepare_mock_http_response(429)
        mock_client_instance.chat.completions.create.side_effect = openai.RateLimitError(message="Rate limit", response=mock_http_response, body=None)

        response = get_openai_response("key", "url", "model", "prompt", 0.5, 100)
        self.assertTrue(response.startswith("Error: OpenAI API request exceeded rate limit:"))

    @patch('openai_client.openai.OpenAI')
    def test_get_openai_response_api_connection_error(self, mock_openai_class):
        mock_client_instance = mock_openai_class.return_value
        mock_request = Mock(spec=httpx.Request)
        mock_client_instance.chat.completions.create.side_effect = openai.APIConnectionError(message="Connection error", request=mock_request)

        response = get_openai_response("key", "url", "model", "prompt", 0.5, 100)
        self.assertTrue(response.startswith("Error: Failed to connect to OpenAI API:"))

    @patch('openai_client.openai.OpenAI')
    def test_get_openai_response_bad_request_error(self, mock_openai_class):
        mock_client_instance = mock_openai_class.return_value
        mock_http_response = self._prepare_mock_http_response(400)
        mock_client_instance.chat.completions.create.side_effect = openai.BadRequestError(message="Bad request", response=mock_http_response, body=None)

        response = get_openai_response("key", "url", "model", "prompt", 0.5, 100)
        self.assertTrue(response.startswith("Error: OpenAI API request was invalid:"))

    @patch('openai_client.openai.OpenAI')
    def test_get_openai_response_api_error(self, mock_openai_class):
        mock_client_instance = mock_openai_class.return_value
        # From the error: APIError.__init__() missing 1 required keyword-only argument: 'body'
        # And it likely also needs 'request' and 'message'.
        mock_request = Mock(spec=httpx.Request)
        mock_client_instance.chat.completions.create.side_effect = openai.APIError(
            message="Generic API error from SDK",
            request=mock_request,
            body=None # Adding the missing 'body' argument
        )

        response = get_openai_response("key", "url", "model", "prompt", 0.5, 100)
        self.assertTrue(response.startswith("Error: An unexpected error occurred with the OpenAI API:"))


    @patch('openai_client.openai.OpenAI')
    def test_get_openai_response_general_exception(self, mock_openai_class):
        mock_client_instance = mock_openai_class.return_value
        mock_client_instance.chat.completions.create.side_effect = Exception("Generic error")

        response = get_openai_response("key", "url", "model", "prompt", 0.5, 100)
        self.assertTrue(response.startswith("Error: An unexpected error occurred:"))

if __name__ == '__main__':
    unittest.main()
