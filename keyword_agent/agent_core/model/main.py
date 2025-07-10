from langchain_openai import ChatOpenAI # Updated import
from langchain.agents import initialize_agent, AgentType
import os
import sys

# Import your system prompt and tool
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from prompts.system_prompt import keyword_agent_system_prompt
from tools.top_performing_keyword import top_performing_keyword
from tools.top_converting_keyword import top_converting_keyword


# Set API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


# Initialize ChatOpenAI model
llm = ChatOpenAI(model_name="gpt-4", temperature=0, verbose=True)


# Initialize the agent with tool(s), LLM, and the modified prefix
agent = initialize_agent(
    tools=[top_performing_keyword, top_converting_keyword],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    agent_kwargs={
        "prefix": keyword_agent_system_prompt
    }
)


def main():
    vertical_sector = "Educational Services"
    

    task_prompt = (
        f"Generate a comprehensive keyword insights report for the vertical sector: '{vertical_sector}'. "
        f"Autonomously select and use available tools to gather the necessary data (like top performing and top converting keywords), "
        f"then synthesize this data into a concise, actionable report."
    )

    print(f"Running agent with task: {task_prompt}")

    # Run agent
    response = agent.run(task_prompt)

    print("\nAgent Response:\n", response)

    # Create output directory if it doesn't exist
    output_dir = os.path.join("vertical_insights", "keyword_agent")
    os.makedirs(output_dir, exist_ok=True)

    # Define output file path
    output_filename = f"keyword_insights_{vertical_sector.replace(' ', '_').lower()}.md"
    output_path = os.path.join(output_dir, output_filename)

    # Write the report to the file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Keyword Insights Report\n\n")
        f.write(f"**Vertical Sector:** {vertical_sector}\n\n")
        f.write(response)

    print(f"\n✅ Report saved to: {output_path}")

if __name__ == "__main__":
    main()
