from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph

from .agents.qa_agent import ask_question
from .agents.summarizer import summarize
from .agents.timestamp_agent import extract_timestamp


class GraphState(TypedDict, total=False):
    question: str
    context: str
    transcript: str
    topic: str
    intent: Literal["qa", "summarize", "timestamp"]
    answer: str


def supervisor_node(state: GraphState) -> GraphState:
    question = (state.get("question") or "").lower()

    if any(word in question for word in ["summary", "summarize", "brief"]):
        return {"intent": "summarize"}

    if any(word in question for word in ["timestamp", "time", "when"]):
        return {"intent": "timestamp"}

    return {"intent": "qa"}


def qa_node(state: GraphState) -> GraphState:
    answer = ask_question(state.get("context", ""), state.get("question", ""))
    return {"answer": answer}


def summarize_node(state: GraphState) -> GraphState:
    text = state.get("context") or state.get("transcript", "")
    answer = summarize(text)
    return {"answer": answer}


def timestamp_node(state: GraphState) -> GraphState:
    transcript = state.get("transcript") or state.get("context", "")
    topic = state.get("topic") or state.get("question", "")
    answer = extract_timestamp(transcript, topic)
    return {"answer": answer}


workflow = StateGraph(GraphState)
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("qa_agent", qa_node)
workflow.add_node("summarizer_agent", summarize_node)
workflow.add_node("timestamp_agent", timestamp_node)

workflow.add_edge(START, "supervisor")
workflow.add_conditional_edges(
    "supervisor",
    lambda state: state["intent"],
    {
        "qa": "qa_agent",
        "summarize": "summarizer_agent",
        "timestamp": "timestamp_agent",
    },
)
workflow.add_edge("qa_agent", END)
workflow.add_edge("summarizer_agent", END)
workflow.add_edge("timestamp_agent", END)

app = workflow.compile()


def run_multi_agent(payload: GraphState) -> GraphState:
    return app.invoke(payload)