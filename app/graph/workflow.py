from langgraph.graph import StateGraph, END
from typing import TypedDict

from app.rag.vectorstore import build_vectorstore
from app.rag.retriever import retrieve_context
from app.pipeline import run_pipeline


class State(TypedDict):
    rubric: str
    teaching: str
    students: list
    vectorstore: object
    result: dict


# ----------------------------
# STEP 1: Build RAG index
# ----------------------------
def build_index(state: State):
    texts = [state["rubric"], state["teaching"]]
    vs = build_vectorstore(texts)
    return {"vectorstore": vs}


# ----------------------------
# STEP 2: Retrieve context
# ----------------------------
def enrich_students(state: State):
    vs = state["vectorstore"]

    enriched = []
    for s in state["students"]:
        context = retrieve_context(vs, s)
        enriched.append(f"{s}\n\n[CONTEXT]\n{context}")

    return {"students": enriched}


# ----------------------------
# STEP 3: Run your pipeline
# ----------------------------
def run_eval(state: State):
    result = run_pipeline(
        state["rubric"],
        state["teaching"],
        state["students"]
    )
    return {"result": result}


# ----------------------------
# BUILD GRAPH
# ----------------------------
def build_workflow():

    graph = StateGraph(State)

    graph.add_node("build_index", build_index)
    graph.add_node("enrich_students", enrich_students)
    graph.add_node("run_eval", run_eval)

    graph.set_entry_point("build_index")

    graph.add_edge("build_index", "enrich_students")
    graph.add_edge("enrich_students", "run_eval")
    graph.add_edge("run_eval", END)

    return graph.compile()