"""Builds the LangGraph workflow graph for resume tailoring.

Configures the state graph with planner and generator nodes, compiled with a MemorySaver checkpointer.
"""

from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver

from graph.state import ResumeGraphState
from graph.nodes.planner import planner_node
from graph.nodes.generator import generator_node


def build_graph():
    """Compile the LangGraph state graph for resume tailoring."""
    workflow = StateGraph(ResumeGraphState)

    workflow.add_node("planner", planner_node)
    workflow.add_node("generator", generator_node)

    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "generator")
    workflow.add_edge("generator", END)

    return workflow.compile(checkpointer=MemorySaver())