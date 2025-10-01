import urllib.request
import urllib.parse

def search_duckduckgo_html(query: str) -> str:
    """
    Performs a search on DuckDuckGo and returns the raw HTML result.
    This version uses only the Python standard library.

    Args:
        query: The search term to look up.

    Returns:
        The raw HTML content of the search results page as a string,
        or an error message if the search fails.
    """
    try:
        encoded_query = urllib.parse.urlencode({'q': query})
        # We use the 'html' endpoint of DuckDuckGo to get a simpler, non-JavaScript page
        url = f"https://duckduckgo.com/html/?{encoded_query}"

        # It's good practice to set a User-Agent to mimic a browser
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        request = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(request) as response:
            # Read the response and decode it from bytes to a string
            html_content = response.read().decode('utf-8')
            return html_content
    except urllib.error.URLError as e:
        return f"An error occurred while trying to fetch the URL: {e.reason}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def get_url_content_html(url: str) -> str:
    """
    Retrieves the HTML content of a given URL.

    Args:
        url: The URL to fetch the content from.

    Returns:
        The raw HTML content of the page as a string,
        or an error message if the fetch fails.
    """
    try:
        # It's good practice to set a User-Agent to mimic a browser
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        request = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(request) as response:
            # Read the response and decode it from bytes to a string
            html_content = response.read().decode('utf-8')
            return html_content
    except urllib.error.URLError as e:
        return f"An error occurred while trying to fetch the URL: {e.reason}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# Example of how to use the tool
if __name__ == '__main__':
    search_query = "What is the Strands Agents SDK?"
    results = search_duckduckgo_html(search_query)
    print(results)