import os
import json
from typing import TypedDict, List
from pydantic import BaseModel, Field

try:
    from langchain_groq import ChatGroq
    from langgraph.graph import StateGraph, START, END
    from langchain_core.prompts import ChatPromptTemplate
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False

class AgentState(TypedDict):
    project_data: dict
    risk_data: dict
    swot_data: dict
    
    project_analysis: str
    risk_analysis: str
    
    recommendations: List[dict]
    mitigations: List[dict]
    improvements: List[dict]
    
    final_response: str
    workflow_steps: List[dict]

def analyze_project(state: AgentState):
    llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)
    prompt = ChatPromptTemplate.from_template(
        "Analyze the following project data and provide a brief executive summary:\n{project_data}"
    )
    res = (prompt | llm).invoke({"project_data": state["project_data"]})
    return {"project_analysis": res.content}

def analyze_risks(state: AgentState):
    llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)
    prompt = ChatPromptTemplate.from_template(
        "Analyze the following risks and SWOT data:\nRisks: {risk_data}\nSWOT: {swot_data}\n"
        "Provide a summary of the most critical vulnerabilities."
    )
    res = (prompt | llm).invoke({"risk_data": state["risk_data"], "swot_data": state["swot_data"]})
    return {"risk_analysis": res.content}

def generate_recommendations(state: AgentState):
    llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)
    prompt = ChatPromptTemplate.from_template(
        "Based on the project analysis: {project_analysis}\n"
        "And risk analysis: {risk_analysis}\n"
        "Generate strategic recommendations. Return ONLY a valid JSON object with a 'recommendations' key containing a list of objects. "
        "Each object must have:\n"
        "- 'category' (string: Overall, Risk-Based, Market, Technical, Financial, Operational, Short-Term, Long-Term)\n"
        "- 'title' (string)\n"
        "- 'priority' (string: Critical, High, Medium)\n"
        "- 'description' (string: what the problem is, why it matters, what action to take, how it reduces risk)"
    )
    res = (prompt | llm).invoke({
        "project_analysis": state["project_analysis"], 
        "risk_analysis": state["risk_analysis"]
    })
    
    try:
        content = res.content.strip()
        if content.startswith("```json"): content = content[7:-3].strip()
        elif content.startswith("```"): content = content[3:-3].strip()
        recs = json.loads(content).get("recommendations", [])
    except Exception:
        recs = []
        
    return {"recommendations": recs}

def generate_mitigation(state: AgentState):
    llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)
    prompt = ChatPromptTemplate.from_template(
        "Based on the risks: {risk_analysis}\n"
        "Generate mitigation strategies. Return ONLY a valid JSON object with a 'mitigations' key containing a list of objects. "
        "Each object must have:\n"
        "- 'risk_name' (string)\n"
        "- 'category' (string: Financial, Market, Technical, Operational)\n"
        "- 'description' (string)\n"
        "- 'impact' (string: Critical, High, Medium)\n"
        "- 'priority' (string: Critical, High, Medium)\n"
        "- 'mitigation_strategy' (string)\n"
        "- 'preventive_action' (string)\n"
        "- 'contingency_action' (string)"
    )
    res = (prompt | llm).invoke({"risk_analysis": state["risk_analysis"]})
    
    try:
        content = res.content.strip()
        if content.startswith("```json"): content = content[7:-3].strip()
        elif content.startswith("```"): content = content[3:-3].strip()
        mits = json.loads(content).get("mitigations", [])
    except Exception:
        mits = []
        
    return {"mitigations": mits}

def generate_improvements(state: AgentState):
    llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)
    prompt = ChatPromptTemplate.from_template(
        "Based on project analysis: {project_analysis}\n"
        "Generate improvement suggestions. Return ONLY a valid JSON object with an 'improvements' key containing a list of objects. "
        "Each object must have:\n"
        "- 'category' (string: Product, Market, Technical, Financial, Operational, Marketing)\n"
        "- 'improvement' (string)\n"
        "- 'reason' (string)\n"
        "- 'expected_benefit' (string)\n"
        "- 'priority' (string: Critical, High, Medium, Low)"
    )
    res = (prompt | llm).invoke({"project_analysis": state["project_analysis"]})
    
    try:
        content = res.content.strip()
        if content.startswith("```json"): content = content[7:-3].strip()
        elif content.startswith("```"): content = content[3:-3].strip()
        imps = json.loads(content).get("improvements", [])
    except Exception:
        imps = []
        
    return {"improvements": imps}

def generate_final_response(state: AgentState):
    llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)
    prompt = ChatPromptTemplate.from_template(
        "Based on all previous data, generate a final strategic assessment text summarizing the core findings.\n"
        "Recommendations count: {rec_len}\nMitigations count: {mit_len}\nImprovements count: {imp_len}\n"
    )
    res = (prompt | llm).invoke({
        "rec_len": len(state.get("recommendations", [])),
        "mit_len": len(state.get("mitigations", [])),
        "imp_len": len(state.get("improvements", []))
    })
    return {"final_response": res.content}

def create_workflow():
    workflow = StateGraph(AgentState)
    workflow.add_node("analyze_project", analyze_project)
    workflow.add_node("analyze_risks", analyze_risks)
    workflow.add_node("generate_recommendations", generate_recommendations)
    workflow.add_node("generate_mitigation", generate_mitigation)
    workflow.add_node("generate_improvements", generate_improvements)
    workflow.add_node("generate_final_response", generate_final_response)
    
    workflow.add_edge(START, "analyze_project")
    workflow.add_edge("analyze_project", "analyze_risks")
    workflow.add_edge("analyze_risks", "generate_recommendations")
    workflow.add_edge("generate_recommendations", "generate_mitigation")
    workflow.add_edge("generate_mitigation", "generate_improvements")
    workflow.add_edge("generate_improvements", "generate_final_response")
    workflow.add_edge("generate_final_response", END)
    
    return workflow.compile()

def run_agent(project_data, risk_data, swot_data):
    workflow_steps_data = [
        {"name": "analyze_project", "icon": "📂", "desc": "Analyze Project"},
        {"name": "analyze_risks", "icon": "📊", "desc": "Analyze Risks"},
        {"name": "generate_recommendations", "icon": "💡", "desc": "Recommendations"},
        {"name": "generate_mitigation", "icon": "🛡️", "desc": "Mitigations"},
        {"name": "generate_improvements", "icon": "📈", "desc": "Improvements"},
        {"name": "generate_final_response", "icon": "📄", "desc": "Final Response"}
    ]

    api_key = os.environ.get("GROQ_API_KEY")
    if not LANGGRAPH_AVAILABLE or not api_key or api_key == "your_groq_api_key_here":
        # Mock data for demo
        return {
            "recommendations": [{"category": "Overall", "title": "Secure Funding", "priority": "High", "description": "Needs money"}],
            "mitigations": [{"risk_name": "Competition", "category": "Market", "description": "High comp", "impact": "High", "priority": "High", "mitigation_strategy": "Differentiate", "preventive_action": "Monitor", "contingency_action": "Pivot"}],
            "improvements": [{"category": "Product", "improvement": "Add AI", "reason": "Trend", "expected_benefit": "More users", "priority": "High"}],
            "final_response": "This is a demo final assessment.",
            "workflow_steps": workflow_steps_data
        }
        
    app = create_workflow()
    initial_state = {
        "project_data": project_data,
        "risk_data": risk_data,
        "swot_data": swot_data
    }
    result = app.invoke(initial_state)
    
    return {
        "recommendations": result.get("recommendations", []),
        "mitigations": result.get("mitigations", []),
        "improvements": result.get("improvements", []),
        "final_response": result.get("final_response", ""),
        "workflow_steps": workflow_steps_data
    }
