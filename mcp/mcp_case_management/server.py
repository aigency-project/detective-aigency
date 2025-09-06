# server.py
import logging
from mcp.server.fastmcp import FastMCP
from mcp.types import PromptMessage, TextContent
from typing import List, Dict, Any, Optional, Union
import json
import uuid
import datetime

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8080
SERVER_PATH = "/mcp"

logger = logging.getLogger(__name__)

mcp = FastMCP(
    name="Case Management MCP", port=SERVER_PORT, host=SERVER_HOST, log_level="DEBUG"
)

logger.info("Case Management FastMCP server object created")

# In-memory database for cases
CASES_DB = {}
EVIDENCE_DB = {}
REPORTS_DB = {}

# Sample data
SAMPLE_CASES = [
    {
        "id": "CASE-001",
        "title": "El Diamante Jewelry Store Robbery",
        "type": "theft",
        "status": "open",
        "description": "Nighttime robbery at downtown jewelry store. Forced entry, safe opened.",
        "date_created": "2025-09-01",
        "priority": "high",
        "assigned_detective": "Detective García",
        "evidence_ids": ["EVID-001", "EVID-002"],
        "suspects": ["Unknown suspect - fingerprints"],
        "location": "Mayor Street 15, Downtown",
    },
    {
        "id": "CASE-002",
        "title": "TechCorp Corporate Fraud",
        "type": "fraud",
        "status": "under_investigation",
        "description": "Possible embezzlement of funds in technology company.",
        "date_created": "2025-08-28",
        "priority": "high",
        "assigned_detective": "Detective Martínez",
        "evidence_ids": ["EVID-003", "EVID-004"],
        "suspects": ["Carlos Mendoza - CFO", "Ana López - Accountant"],
        "location": "TechCorp Offices, Industrial Park",
    },
    {
        "id": "CASE-003",
        "title": "María González Disappearance",
        "type": "disappearance",
        "status": "open",
        "description": "28-year-old woman missing for 3 days. Last seen at shopping mall.",
        "date_created": "2025-09-02",
        "priority": "critical",
        "assigned_detective": "Detective Ruiz",
        "evidence_ids": ["EVID-005"],
        "suspects": [],
        "location": "Plaza Norte Shopping Mall",
    },
]

SAMPLE_EVIDENCE = [
    {
        "id": "EVID-001",
        "case_id": "CASE-001",
        "type": "fingerprints",
        "description": "Fingerprints found on the safe",
        "location_found": "Main safe",
        "date_collected": "2025-09-01",
        "status": "pending_analysis",
        "chain_of_custody": ["Detective García", "Forensic Laboratory"],
        "analysis_results": None,
    },
    {
        "id": "EVID-002",
        "case_id": "CASE-001",
        "type": "security_video",
        "description": "Recording from exterior security cameras",
        "location_found": "Exterior camera Mayor Street",
        "date_collected": "2025-09-01",
        "status": "analyzed",
        "chain_of_custody": ["Detective García", "IT Technician"],
        "analysis_results": "Hooded figure, approximately 1.75m, entry at 02:30",
    },
    {
        "id": "EVID-003",
        "case_id": "CASE-002",
        "type": "financial_documents",
        "description": "Accounting records from the last 6 months",
        "location_found": "TechCorp accounting office",
        "date_collected": "2025-08-28",
        "status": "under_analysis",
        "chain_of_custody": ["Detective Martínez", "Forensic Auditor"],
        "analysis_results": "Discrepancies in transfers for €250,000",
    },
    {
        "id": "EVID-004",
        "case_id": "CASE-002",
        "type": "bank_records",
        "description": "Bank statements from corporate accounts",
        "location_found": "Central Bank",
        "date_collected": "2025-08-29",
        "status": "analyzed",
        "chain_of_custody": ["Detective Martínez", "Financial Specialist"],
        "analysis_results": "Unauthorized transfers to offshore accounts",
    },
    {
        "id": "EVID-005",
        "case_id": "CASE-003",
        "type": "security_video",
        "description": "Last recording of María González at shopping mall",
        "location_found": "Plaza Norte Shopping Center - Main entrance",
        "date_collected": "2025-09-02",
        "status": "analyzed",
        "chain_of_custody": ["Detective Ruiz", "Security Technician"],
        "analysis_results": "Last seen at 18:45, leaving alone through main entrance",
    },
]


def initialize_data():
    """Initialize the database with sample data"""
    for case in SAMPLE_CASES:
        CASES_DB[case["id"]] = case

    for evidence in SAMPLE_EVIDENCE:
        EVIDENCE_DB[evidence["id"]] = evidence


initialize_data()


@mcp.tool()
def get_case_details(case_id: str) -> Dict[str, Any]:
    """
    Gets complete details of a specific case by its ID.
    """
    print(f"Tool call: get_case_details for case ID: {case_id}")

    if case_id not in CASES_DB:
        return {"error": f"Case with ID '{case_id}' not found."}

    case = CASES_DB[case_id].copy()

    # Add related evidence
    case_evidence = []
    for evid_id in case.get("evidence_ids", []):
        if evid_id in EVIDENCE_DB:
            case_evidence.append(EVIDENCE_DB[evid_id])

    case["evidence_details"] = case_evidence
    return case


@mcp.tool()
def search_cases_by_type(case_type: str) -> List[Dict[str, Any]]:
    """
    Search cases by type (theft, fraud, disappearance, homicide, etc.).
    """
    print(f"Tool call: search_cases_by_type for type: {case_type}")

    matching_cases = []
    for case in CASES_DB.values():
        if case["type"].lower() == case_type.lower():
            matching_cases.append(case)

    return (
        matching_cases
        if matching_cases
        else {"message": f"No cases found of type '{case_type}'."}
    )


@mcp.tool()
def search_cases_by_status(status: str) -> List[Dict[str, Any]]:
    """
    Search cases by status (open, closed, under_investigation, archived).
    """
    print(f"Tool call: search_cases_by_status for status: {status}")

    matching_cases = []
    for case in CASES_DB.values():
        if case["status"].lower() == status.lower():
            matching_cases.append(case)

    return (
        matching_cases
        if matching_cases
        else {"message": f"No cases found with status '{status}'."}
    )


@mcp.tool()
def get_evidence_details(evidence_id: str) -> Dict[str, Any]:
    """
    Gets details of a specific evidence by its ID.
    """
    print(f"Tool call: get_evidence_details for evidence ID: {evidence_id}")

    if evidence_id not in EVIDENCE_DB:
        return {"error": f"Evidence with ID '{evidence_id}' not found."}

    return EVIDENCE_DB[evidence_id]


@mcp.tool()
def analyze_evidence(evidence_id: str, analysis_type: str) -> Dict[str, Any]:
    """
    Performs specific analysis of evidence.
    Analysis types: forensic, digital, financial, psychological.
    """
    print(
        f"Tool call: analyze_evidence for evidence ID: {evidence_id}, analysis type: {analysis_type}"
    )

    if evidence_id not in EVIDENCE_DB:
        return {"error": f"Evidence with ID '{evidence_id}' not found."}

    evidence = EVIDENCE_DB[evidence_id]

    # Simulate analysis based on type
    analysis_results = {
        "evidence_id": evidence_id,
        "analysis_type": analysis_type,
        "date_analyzed": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "analyst": f"Specialist in {analysis_type}",
        "status": "completed",
    }

    if analysis_type.lower() == "forensic":
        if evidence["type"] == "fingerprints":
            analysis_results["findings"] = (
                "Partial fingerprints identified, 12 comparison points available"
            )
            analysis_results["confidence"] = "85%"
        elif evidence["type"] == "security_video":
            analysis_results["findings"] = (
                "Movement and physical characteristics analysis completed"
            )
            analysis_results["confidence"] = "70%"
    elif analysis_type.lower() == "digital":
        analysis_results["findings"] = (
            "Metadata extracted, integrity analysis completed"
        )
        analysis_results["confidence"] = "95%"
    elif analysis_type.lower() == "financial":
        analysis_results["findings"] = "Anomalous transaction patterns identified"
        analysis_results["confidence"] = "90%"

    # Update evidence with results
    EVIDENCE_DB[evidence_id]["analysis_results"] = analysis_results
    EVIDENCE_DB[evidence_id]["status"] = "analyzed"

    return analysis_results


@mcp.tool()
def create_case_report(
    case_id: str, findings: str, recommendations: str
) -> Dict[str, Any]:
    """
    Creates an official case report with findings and recommendations.
    """
    print(f"Tool call: create_case_report for case ID: {case_id}")

    if case_id not in CASES_DB:
        return {"error": f"Case with ID '{case_id}' not found."}

    report_id = f"RPT-{uuid.uuid4().hex[:8].upper()}"
    report = {
        "id": report_id,
        "case_id": case_id,
        "case_title": CASES_DB[case_id]["title"],
        "date_created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "author": "Case Management System",
        "findings": findings,
        "recommendations": recommendations,
        "status": "draft",
        "case_status_at_report": CASES_DB[case_id]["status"],
    }

    REPORTS_DB[report_id] = report

    return {
        "status": "success",
        "message": "Report created successfully",
        "report": report,
    }


@mcp.tool()
def get_case_status(case_id: str) -> Dict[str, Any]:
    """
    Checks the current status of a case.
    """
    print(f"Tool call: get_case_status for case ID: {case_id}")

    if case_id not in CASES_DB:
        return {"error": f"Case with ID '{case_id}' not found."}

    case = CASES_DB[case_id]
    return {
        "case_id": case_id,
        "title": case["title"],
        "status": case["status"],
        "priority": case["priority"],
        "assigned_detective": case["assigned_detective"],
        "date_created": case["date_created"],
        "evidence_count": len(case.get("evidence_ids", [])),
        "suspect_count": len(case.get("suspects", [])),
    }


@mcp.tool()
def update_case_status(case_id: str, new_status: str, notes: str) -> Dict[str, Any]:
    """
    Updates the status of a case with explanatory notes.
    Valid statuses: open, under_investigation, closed, archived.
    """
    print(
        f"Tool call: update_case_status for case ID: {case_id} to status: {new_status}"
    )

    if case_id not in CASES_DB:
        return {"error": f"Case with ID '{case_id}' not found."}

    valid_statuses = ["open", "under_investigation", "closed", "archived"]
    if new_status.lower() not in valid_statuses:
        return {
            "error": f"Status '{new_status}' not valid. Valid statuses: {', '.join(valid_statuses)}"
        }

    old_status = CASES_DB[case_id]["status"]
    CASES_DB[case_id]["status"] = new_status.lower()
    CASES_DB[case_id]["last_updated"] = datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M"
    )

    # Add note to history
    if "status_history" not in CASES_DB[case_id]:
        CASES_DB[case_id]["status_history"] = []

    CASES_DB[case_id]["status_history"].append(
        {
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "old_status": old_status,
            "new_status": new_status.lower(),
            "notes": notes,
        }
    )

    return {
        "status": "success",
        "message": f"Case {case_id} status updated from '{old_status}' to '{new_status.lower()}'",
        "case_id": case_id,
        "new_status": new_status.lower(),
        "notes": notes,
    }


# --- SERVER STARTUP SECTION ---
if __name__ == "__main__":
    logger.info(
        f"Attempting to start Case Management FastMCP server on {SERVER_HOST}:{SERVER_PORT}{SERVER_PATH} with streamable-http transport"
    )
    try:
        mcp.run(transport="streamable-http")
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"An error occurred while starting the server: {e}")
