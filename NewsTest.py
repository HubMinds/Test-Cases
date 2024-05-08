import pytest
from news_test_source import fetch_news_headlines

# Mocking requests.get function
@pytest.fixture
def mock_requests_get(monkeypatch):
    class MockResponse:
        def __init__(self, status_code, json_data):
            self.status_code = status_code
            self.json_data = json_data

        def json(self):
            return self.json_data

    def mock_get(*args, **kwargs):
        return MockResponse(200, {"totalResults": 2, "articles": [{"title": "Article 1", "url": "http://example.com", "urlToImage": "http://example.com/image1.jpg"}, {"title": "Article 2", "url": "http://example.com", "urlToImage": "http://example.com/image2.jpg"}]})

    monkeypatch.setattr("requests.get", mock_get)

# Valid test cases
@pytest.mark.parametrize("country, source, category, query", [
    ("us", "", "", ""),  # Test valid country code
    ("", "bbc-news", "", ""),  # Test valid source
    ("", "", "business", ""),  # Test valid category
    ("", "", "", "technology"),  # Test valid keyword
])
def test_valid_inputs(mock_requests_get, country, source, category, query):
    headlines = fetch_news_headlines(country, source, category, query)
    assert headlines is not None
    assert len(headlines) == 2  # Assuming we always get 2 articles in the mock response
    print(f"Test passed for valid inputs: country={country}, source={source}, category={category}, query={query}")

# Invalid test cases
@pytest.mark.parametrize("country, source, category, query", [
    ("invalid", "", "", ""),  # Test invalid country code
    ("", "invalid-source", "", ""),  # Test invalid source
    ("", "", "invalid-category", ""),  # Test invalid category
    ("", "", "", ""),  # No parameters provided
])
def test_invalid_inputs(mock_requests_get, country, source, category, query):
    assert fetch_news_headlines(country, source, category, query) == []
    print(f"Test passed for invalid inputs: country={country}, source={source}, category={category}, query={query}")

# Test case for handling invalid API key
def test_invalid_api_key(monkeypatch):
    def mock_load_dotenv():
        pass  # No need to load dotenv for this test

    monkeypatch.setattr("news.load_dotenv", mock_load_dotenv)
    monkeypatch.setenv("NEWS_KEY", "")  # Set invalid API key

    assert fetch_news_headlines("us", "", "", "") is None
    print("Test passed for handling invalid API key")

# Test case for handling missing API key
def test_missing_api_key(monkeypatch):
    def mock_load_dotenv():
        pass  # No need to load dotenv for this test

    monkeypatch.setattr("news.load_dotenv", mock_load_dotenv)
    monkeypatch.delenv("NEWS_KEY", raising=False)  # Remove NEWS_KEY from environment

    assert fetch_news_headlines("us", "", "", "") is None
    print("Test passed for handling missing API key")


