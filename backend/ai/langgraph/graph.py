from langgraph.graph import StateGraph, END
from ai.langgraph.state import WorkflowState
from ai.langgraph.nodes.intent import detect_intent_node
from ai.langgraph.nodes.extraction import extraction_node
from ai.langgraph.nodes.editing import editing_node
from ai.langgraph.nodes.doc_extraction import doc_extraction_node
from ai.langgraph.nodes.risk_assessment import risk_assessment_node
from ai.langgraph.nodes.db_save import db_save_node

def route_by_intent(state: WorkflowState) -> str:
    if state.get("error"):
        return END
        
    intent = state.get("intent")
    if intent == "log":
        return "extract"
    elif intent == "edit":
        return "edit"
    elif intent == "upload":
        return "doc_extract"
    return "extract"

def build_graph() -> StateGraph:
    workflow = StateGraph(WorkflowState)
    
    workflow.add_node("detect_intent", detect_intent_node)
    workflow.add_node("extract", extraction_node)
    workflow.add_node("edit", editing_node)
    workflow.add_node("doc_extract", doc_extraction_node)
    workflow.add_node("assess_risk", risk_assessment_node)
    workflow.add_node("save_db", db_save_node)
    
    workflow.set_entry_point("detect_intent")
    
    workflow.add_conditional_edges(
        "detect_intent",
        route_by_intent,
        {
            "extract": "extract",
            "edit": "edit",
            "doc_extract": "doc_extract",
            END: END
        }
    )
    
    workflow.add_edge("extract", "assess_risk")
    workflow.add_edge("edit", "assess_risk")
    workflow.add_edge("doc_extract", "assess_risk")
    workflow.add_edge("assess_risk", "save_db")
    workflow.add_edge("save_db", END)
    
    return workflow.compile()

complaint_graph = build_graph()
