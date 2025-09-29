import argparse
import os
import sys

from strands import Agent
from strands.models import OpenAI

def main():
    """
    Takes a prompt from the command line, sends it to an OpenAI LLM using the Strands library,
    and prints the response.
    """
    # Check for OpenAI API key
    if "OPENAI_API_KEY" not in os.environ:
        print("Error: The OPENAI_API_KEY environment variable is not set.", file=sys.stderr)
        print("Please set it to your OpenAI API key.", file=sys.stderr)
        sys.exit(1)

    # Set up argument parser
    parser = argparse.ArgumentParser(description="A simple Strands app to interact with an OpenAI LLM.")
    parser.add_argument("--prompt", type=str, required=True, help="The prompt to send to the LLM.")
    args = parser.parse_args()

    try:
        # 1. Configure the model provider
        # The OpenAI model will automatically use the OPENAI_API_KEY environment variable.
        model = OpenAI()

        # 2. Create the agent and provide it with the model
        agent = Agent(model=model)

        # 3. Interact with the agent
        print(f"User: {args.prompt}")
        response = agent(args.prompt)
        print(f"Agent: {response}")

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()