import argparse
import os
import sys

from strands import Agent
from strands.models.openai import OpenAIModel
from strands.tools import tool
from tools.search import search_duckduckgo_html

@tool
def web_search(query: str) -> str:
    """
    Performs a web search using DuckDuckGo for the given query and returns the raw HTML of the search results page.
    Use this tool to find information on the web to answer the user's question.
    The returned HTML contains a list of search results with titles, snippets, and URLs.
    """
    return search_duckduckgo_html(query)

def main():
    """
    This script takes a user's question, uses an AI agent to search the web for an answer,
    and prints a comprehensive response with source links.
    """
    # Check for OpenAI API key
    if "OPENAI_API_KEY" not in os.environ:
        print("Error: The OPENAI_API_KEY environment variable is not set.", file=sys.stderr)
        print("Please set it to your OpenAI API key.", file=sys.stderr)
        sys.exit(1)

    # Set up argument parser
    parser = argparse.ArgumentParser(description="An AI agent that searches the web to answer your questions.")
    parser.add_argument("--prompt", type=str, required=True, help="The question or topic to search for.")
    args = parser.parse_args()

    try:
        # 1. Configure the model provider
        model = OpenAIModel(model_id="gpt-4o-mini")

        # 2. Define the system prompt for the agent
        system_prompt = """\
You are a helpful research assistant. Your goal is to answer the user's question accurately and concisely.
To do this, you must:
1. Use the `web_search` tool with the user's prompt as the query.
2. Carefully analyze the returned HTML search results.
3. Synthesize the information from the most relevant search snippets to formulate a comprehensive answer.
4. Conclude your answer by listing the URLs of the sources you used, formatted as a "Sources" list. For example:

Sources:
- https://example.com/source1
- https://example.com/source2
"""

        # 3. Create the agent
        agent = Agent(
            model=model,
            tools=[web_search],
            system_prompt=system_prompt
        )

        # 4. Interact with the agent
        print(f"User: {args.prompt}")
        print("\\nAgent is thinking...")
        response = agent(args.prompt)
        print("\\nAgent Response:")
        print(response)

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()