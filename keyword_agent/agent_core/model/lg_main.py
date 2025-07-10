from typing_extensions import TypedDict
from typing import Annotated
from langchain_openai import ChatOpenAI # Updated import
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import init_chat_model
from langgraph.graph.message import add_messages
import os
import sys

# Import your system prompt and tool
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from prompts.system_prompt import keyword_agent_system_prompt
from tools.top_performing_keyword import top_performing_keyword
from tools.top_converting_keyword import top_converting_keyword



# Set API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")




llm = init_chat_model("openai:gpt-4.1")
model_with_tools = llm.bind_tools([], parallel_tool_calls=False)


# sql_chain =  keyword_agent_system_prompt | llm


# -------------------------
# TOOL BINDING
# -------------------------
tools = [top_performing_keyword, top_converting_keyword]
model_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)


# -------------------------
# LANGGRAPH STATE + NODES
# -------------------------
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

# ---- State Type ----
class State(TypedDict):
    messages: Annotated[list, add_messages]

# ---- Node: Task Prompt into LLM ----
def run_task_prompt(state: State):
    print("\n[run_task_prompt] Received task.")
    result = model_with_tools.invoke(state["messages"])
    print("[run_task_prompt] Output message:", result)
    return {"messages": [result]}

# ---- Graph ----
graph_builder = StateGraph(State)

graph_builder.add_node("llm_task", run_task_prompt)
graph_builder.add_node("tools_node", ToolNode(tools=tools))

graph_builder.add_edge(START, "llm_task")
graph_builder.add_conditional_edges(
    "llm_task",
    tools_condition,
    {
        "tools": "tools_node",
        "default": END,
        "__end__": END,
    }
)
graph_builder.add_edge("tools_node", END)

graph = graph_builder.compile()



def main():
    vertical_sector = "Educational Services"

    task_prompt = (
        f"Generate a comprehensive keyword insights report for the vertical sector: '{vertical_sector}'. "
        f"Autonomously select and use available tools to gather the necessary data (like top performing and top converting keywords), "
        f"then synthesize this data into a concise, actionable report."
    )

    print(f"\n🟢 Running agent with task: {task_prompt}")

    # Set up initial message state
    initial_state = {
        "messages": [
            {"role": "system", "content": keyword_agent_system_prompt},
            {"role": "user", "content": task_prompt}
        ]
    }

    # Run the LangGraph agent
    events = graph.stream(initial_state)

    final_response = None
    for event in events:
        print("\n[GRAPH EVENT]")
        for key, value in event.items():
            print(f"Node: {key}")
            print("Value:", value)
            if "messages" in value:
                final_response = value["messages"][-1].content

    print("\n📝 Agent Response:\n", final_response)

    # Create output directory if it doesn't exist
    output_dir = os.path.join("keyword_agent", "insights")  # Change to store inside keyword_agent
    os.makedirs(output_dir, exist_ok=True)

    # Define output file path
    output_filename = f"keyword_insights_{vertical_sector.replace(' ', '_').lower()}.md"
    output_path = os.path.join(output_dir, output_filename)

    # Write the report to the file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Keyword Insights Report\n\n")
        f.write(f"**Vertical Sector:** {vertical_sector}\n\n")
        f.write(final_response or "[No response]")

    print(f"\n✅ Report saved to: {output_path}")

if __name__ == "__main__":
    main()
