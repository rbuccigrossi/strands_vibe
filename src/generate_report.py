import argparse
from strands import Agent
from strands.multiagent import Swarm
from strands.models.openai import OpenAIModel
from tools import search_duckduckgo_html, get_url_content_html

# 1. Define System Prompts for Each Agent

RESEARCHER_PROMPT = """\
You are a research assistant. Your task is to find relevant information for the user's request.
1. Use the `search_duckduckgo_html` tool to find a few relevant sources.
2. Use the `get_url_content_html` tool to read the content of the most promising URLs.
3. Synthesize the key information and quotes from these sources into a "research_notes" section in the shared context. Include the source URLs for citation.
4. Handoff to the writer.
"""

WRITER_PROMPT = """\
You are a professional writer. Your task is to write a comprehensive report based on the "research_notes" provided in the shared context.
1. Read the research notes carefully.
2. Draft a well-structured and cohesive report that directly answers the user's original prompt.
3. Cite the sources (URLs or titles) provided in the notes.
4. Handoff to the editor.
"""

EDITOR_PROMPT = """\
You are an editor. Your job is to review the writer's draft.
1. Check the draft for clarity, accuracy, and completeness in addressing the user's prompt.
2. Ensure that sources are properly cited.
3. If the report is high-quality and complete, approve it by outputting the final report as your answer.
4. If it needs revisions, provide specific feedback and hand it back to the writer. If more information is needed, hand it off to the researcher.
"""

def main():
    # 2. Setup Command-Line Argument Parsing
    parser = argparse.ArgumentParser(description="Generate a report using a swarm of AI agents.")
    parser.add_argument("--prompt", type=str, required=True, help="The prompt for the report.")
    args = parser.parse_args()

    # 3. Configure the model provider
    model = OpenAIModel(model_id="gpt-4o-mini")

    # 4. Create the Agents
    researcher = Agent(
        id="researcher",
        role=RESEARCHER_PROMPT,
        model=model,
        tools=[search_duckduckgo_html, get_url_content_html]
    )

    writer = Agent(
        id="writer",
        role=WRITER_PROMPT,
        model=model
    )

    editor = Agent(
        id="editor",
        role=EDITOR_PROMPT,
        model=model
    )

    # 5. Instantiate the Swarm
    swarm = Swarm(
        agents=[researcher, writer, editor],
        # Using default handoff logic
    )

    # 6. Run the Swarm and Print the Result
    print("Running swarm to generate report...")
    final_report = swarm.run(args.prompt)
    print("\n--- Final Report ---")
    print(final_report)

if __name__ == "__main__":
    main()