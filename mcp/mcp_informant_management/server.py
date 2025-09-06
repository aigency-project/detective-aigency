# server.py
import logging
from mcp.server.fastmcp import FastMCP
from mcp.types import PromptMessage, TextContent
from typing import List, Dict, Any, Optional, Union
import json
import uuid
import datetime
import random

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8080
SERVER_PATH = "/mcp"

logger = logging.getLogger(__name__)

mcp = FastMCP(
    name="Informant Management MCP",
    port=SERVER_PORT,
    host=SERVER_HOST,
    log_level="DEBUG",
)

logger.info("Informant Management FastMCP server object created")

# In-memory database for informants
INFORMANTS_DB = {}
MEETINGS_DB = {}
INFORMATION_DB = {}

# Available meeting times
MEETING_TIMES = ["08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00", "22:00"]

# Safe locations for meetings
SAFE_LOCATIONS = [
    "Café Central - Mesa del fondo",
    "Parque Municipal - Banco junto al lago",
    "Biblioteca Pública - Sala de lectura",
    "Centro Comercial - Food Court",
    "Estación de Tren - Sala de espera",
    "Hotel Plaza - Lobby",
    "Museo de Arte - Sala Medieval",
]

# Sample data
SAMPLE_INFORMANTS = [
    {
        "id": "INF-001",
        "code_name": "Cuervo",
        "specialty": "drug_trafficking",
        "reliability_level": "high",
        "contact_method": "secure_phone",
        "date_registered": "2025-01-15",
        "handler": "Detective García",
        "status": "active",
        "location_area": "centro_ciudad",
        "information_count": 12,
        "successful_tips": 9,
    },
    {
        "id": "INF-002",
        "code_name": "Sombra",
        "specialty": "financial_fraud",
        "reliability_level": "medium",
        "contact_method": "encrypted_email",
        "date_registered": "2025-02-20",
        "handler": "Detective Martínez",
        "status": "active",
        "location_area": "distrito_financiero",
        "information_count": 8,
        "successful_tips": 5,
    },
    {
        "id": "INF-003",
        "code_name": "Fantasma",
        "specialty": "jewelry_theft",
        "reliability_level": "high",
        "contact_method": "in_person_contact",
        "date_registered": "2024-11-10",
        "handler": "Detective Ruiz",
        "status": "active",
        "location_area": "centro_comercial",
        "information_count": 15,
        "successful_tips": 13,
    },
    {
        "id": "INF-004",
        "code_name": "Eco",
        "specialty": "disappearances",
        "reliability_level": "low",
        "contact_method": "secure_phone",
        "date_registered": "2025-03-01",
        "handler": "Detective López",
        "status": "inactive",
        "location_area": "suburbios",
        "information_count": 3,
        "successful_tips": 1,
    },
]

SAMPLE_MEETINGS = [
    {
        "id": "MEET-001",
        "informant_id": "INF-001",
        "informant_code_name": "Cuervo",
        "date": "2025-09-05",
        "time": "18:00",
        "location": "Café Central - Mesa del fondo",
        "purpose": "Information about distribution network",
        "status": "scheduled",
        "handler": "Detective García",
        "security_level": "high",
    },
    {
        "id": "MEET-002",
        "informant_id": "INF-002",
        "informant_code_name": "Sombra",
        "date": "2025-09-04",
        "time": "14:00",
        "location": "Biblioteca Pública - Sala de lectura",
        "purpose": "TechCorp case follow-up",
        "status": "completed",
        "handler": "Detective Martínez",
        "security_level": "medium",
    },
    {
        "id": "MEET-003",
        "informant_id": "INF-003",
        "informant_code_name": "Fantasma",
        "date": "2025-09-03",
        "time": "10:00",
        "location": "Café Central - Mesa del fondo",
        "purpose": "Information about jewelry",
        "status": "scheduled",
        "handler": "Detective Ruiz",
        "security_level": "high",
    },
]

SAMPLE_INFORMATION = [
    {
        "id": "INFO-001",
        "informant_id": "INF-001",
        "informant_code_name": "Cuervo",
        "information_type": "suspect_location",
        "content": "Jewelry robbery suspect seen in industrial district",
        "credibility": "high",
        "date_received": "2025-09-03",
        "case_related": "CASE-001",
        "verification_status": "pendiente",
        "handler": "Detective García",
    },
    {
        "id": "INFO-002",
        "informant_id": "INF-002",
        "informant_code_name": "Sombra",
        "information_type": "suspicious_transactions",
        "content": "Anomalous bank movements detected in TechCorp accounts",
        "credibility": "medium",
        "date_received": "2025-09-01",
        "case_related": "CASE-002",
        "verification_status": "verified",
        "handler": "Detective Martínez",
    },
]


def initialize_data():
    """Initialize the database with sample data"""
    for informant in SAMPLE_INFORMANTS:
        INFORMANTS_DB[informant["id"]] = informant

    for meeting in SAMPLE_MEETINGS:
        MEETINGS_DB[meeting["id"]] = meeting

    for info in SAMPLE_INFORMATION:
        INFORMATION_DB[info["id"]] = info


initialize_data()


@mcp.tool()
def register_new_informant(
    code_name: str, specialty: str, reliability_level: str, contact_method: str
) -> Dict[str, Any]:
    """
    Registers a new informant in the system.
    Specialties: drug_trafficking, financial_fraud, jewelry_theft, disappearances, corruption, cybercrime
    Reliability levels: low, medium, high
    Contact methods: secure_phone, encrypted_email, in_person_contact
    """
    logger.info(f"Tool call: register_new_informant - {code_name}, specialty: {specialty}")

    valid_specialties = [
        "drug_trafficking",
        "financial_fraud",
        "jewelry_theft",
        "disappearances",
        "corruption",
        "cybercrime",
    ]
    valid_reliability = ["low", "medium", "high"]
    valid_contact_methods = [
        "secure_phone",
        "encrypted_email",
        "in_person_contact",
    ]

    if specialty not in valid_specialties:
        return {
            "error": f"Specialty '{specialty}' not valid. Valid specialties: {', '.join(valid_specialties)}"
        }

    if reliability_level not in valid_reliability:
        return {
            "error": f"Reliability level '{reliability_level}' not valid. Valid levels: {', '.join(valid_reliability)}"
        }

    if contact_method not in valid_contact_methods:
        return {
            "error": f"Contact method '{contact_method}' not valid. Valid methods: {', '.join(valid_contact_methods)}"
        }

    # Verify that the code name doesn't exist
    for informant in INFORMANTS_DB.values():
        if informant["code_name"].lower() == code_name.lower():
            return {
                "error": f"An informant with code name '{code_name}' already exists"
            }

    informant_id = f"INF-{str(uuid.uuid4().hex[:3]).upper()}"
    new_informant = {
        "id": informant_id,
        "code_name": code_name,
        "specialty": specialty,
        "reliability_level": reliability_level,
        "contact_method": contact_method,
        "date_registered": datetime.datetime.now().strftime("%Y-%m-%d"),
        "handler": "Automatic System",
        "status": "active",
        "location_area": "to_be_determined",
        "information_count": 0,
        "successful_tips": 0,
    }

    INFORMANTS_DB[informant_id] = new_informant

    return {
        "status": "success",
        "message": f"Informant '{code_name}' registered successfully",
        "informant": new_informant,
    }


@mcp.tool()
def schedule_informant_meeting(
    informant_id: str, date: str, time: str, location: str, purpose: str
) -> Dict[str, Any]:
    """
    Schedules a meeting with an informant.
    Date format: YYYY-MM-DD
    Available times: 08:00, 10:00, 12:00, 14:00, 16:00, 18:00, 20:00, 22:00
    """
    logger.info(
        f"Tool call: schedule_informant_meeting for {informant_id} on {date} at {time}"
    )

    if informant_id not in INFORMANTS_DB:
        return {"error": f"Informant with ID '{informant_id}' not found"}

    # Validate date format
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return {"error": f"Date format '{date}' incorrect. Use YYYY-MM-DD"}

    if time not in MEETING_TIMES:
        return {
            "error": f"Time '{time}' not available. Valid times: {', '.join(MEETING_TIMES)}"
        }

    # Check availability (no two meetings at the same time)
    for meeting in MEETINGS_DB.values():
        if (
            meeting["date"] == date
            and meeting["time"] == time
            and meeting["status"] == "scheduled"
        ):
            return {"error": f"There is already a meeting scheduled for {date} at {time}"}

    informant = INFORMANTS_DB[informant_id]
    meeting_id = f"MEET-{str(uuid.uuid4().hex[:3]).upper()}"

    new_meeting = {
        "id": meeting_id,
        "informant_id": informant_id,
        "informant_code_name": informant["code_name"],
        "date": date,
        "time": time,
        "location": location,
        "purpose": purpose,
        "status": "scheduled",
        "handler": informant["handler"],
        "security_level": "medium",
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

    MEETINGS_DB[meeting_id] = new_meeting

    return {
        "status": "success",
        "message": f"Meeting scheduled with '{informant['code_name']}'",
        "meeting": new_meeting,
        "security_instructions": f"Meeting code: {meeting_id}. Location: {location}. Maintain security protocol level {new_meeting['security_level']}.",
    }


@mcp.tool()
def check_meeting_availability(date: str, time: str, location: str) -> Dict[str, Any]:
    """
    Checks availability to schedule a meeting on specific date, time and location.
    """
    logger.info(f"Tool call: check_meeting_availability for {date} at {time} in {location}")

    # Validate date format
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return {"error": f"Date format '{date}' incorrect. Use YYYY-MM-DD"}

    if time not in MEETING_TIMES:
        return {
            "error": f"Time '{time}' not available. Valid times: {', '.join(MEETING_TIMES)}"
        }

    # Check conflicts
    conflicts = []
    for meeting in MEETINGS_DB.values():
        if meeting["status"] == "scheduled":
            if meeting["date"] == date and meeting["time"] == time:
                conflicts.append(
                    f"Meeting with {meeting['informant_code_name']} already scheduled"
                )
            if meeting["date"] == date and meeting["location"] == location:
                time_diff = abs(int(meeting["time"][:2]) - int(time[:2]))
                if time_diff < 2:  # Less than 2 hours difference
                    conflicts.append(
                        f"Location occupied near the time by {meeting['informant_code_name']}"
                    )

    if conflicts:
        return {
            "status": "unavailable",
            "conflicts": conflicts,
            "suggested_alternatives": {
                "alternative_times": [t for t in MEETING_TIMES if t != time][:3],
                "alternative_locations": random.sample(SAFE_LOCATIONS, 3),
            },
        }

    return {
        "status": "available",
        "message": f"Available for meeting on {date} at {time} in {location}",
        "security_recommendations": f"Safe location confirmed. Recommended security level: medium.",
    }


@mcp.tool()
def find_informants_by_specialty(specialty: str) -> List[Dict[str, Any]]:
    """
    Search informants by area of specialization.
    """
    logger.info(f"Tool call: find_informants_by_specialty for {specialty}")

    matching_informants = []
    for informant in INFORMANTS_DB.values():
        if informant["specialty"].lower() == specialty.lower():
            matching_informants.append(
                {
                    "id": informant["id"],
                    "code_name": informant["code_name"],
                    "reliability_level": informant["reliability_level"],
                    "status": informant["status"],
                    "information_count": informant["information_count"],
                    "successful_tips": informant["successful_tips"],
                    "success_rate": f"{(informant['successful_tips'] / max(informant['information_count'], 1)) * 100:.1f}%",
                }
            )

    return (
        matching_informants
        if matching_informants
        else {
            "message": f"No informants specialized in '{specialty}' were found"
        }
    )


@mcp.tool()
def get_informant_profile(informant_id: str) -> Dict[str, Any]:
    """
    Gets the complete profile of a specific informant.
    """
    logger.info(f"Tool call: get_informant_profile for {informant_id}")

    if informant_id not in INFORMANTS_DB:
        return {"error": f"Informant with ID '{informant_id}' not found"}

    informant = INFORMANTS_DB[informant_id].copy()

    # Add additional statistics
    informant["success_rate"] = (
        f"{(informant['successful_tips'] / max(informant['information_count'], 1)) * 100:.1f}%"
    )

    # Add recent meetings
    recent_meetings = []
    for meeting in MEETINGS_DB.values():
        if meeting["informant_id"] == informant_id:
            recent_meetings.append(meeting)

    informant["recent_meetings"] = sorted(
        recent_meetings, key=lambda x: x["date"], reverse=True
    )[:5]

    return informant


@mcp.tool()
def get_informants_by_reliability(reliability_level: str) -> List[Dict[str, Any]]:
    """
    Lists informants filtered by reliability level.
    Levels: low, medium, high
    """
    logger.info(f"Tool call: get_informants_by_reliability for level {reliability_level}")

    valid_levels = ["low", "medium", "high"]
    if reliability_level not in valid_levels:
        return {
            "error": f"Reliability level '{reliability_level}' not valid. Valid levels: {', '.join(valid_levels)}"
        }

    matching_informants = []
    for informant in INFORMANTS_DB.values():
        if (
            informant["reliability_level"] == reliability_level
            and informant["status"] == "active"
        ):
            matching_informants.append(
                {
                    "id": informant["id"],
                    "code_name": informant["code_name"],
                    "specialty": informant["specialty"],
                    "information_count": informant["information_count"],
                    "successful_tips": informant["successful_tips"],
                    "success_rate": f"{(informant['successful_tips'] / max(informant['information_count'], 1)) * 100:.1f}%",
                }
            )

    return (
        matching_informants
        if matching_informants
        else {
            "message": f"No active informants found with reliability '{reliability_level}'"
        }
    )


@mcp.tool()
def record_information_received(
    informant_id: str, information_type: str, content: str, credibility: str
) -> Dict[str, Any]:
    """
    Records information received from an informant.
    Types: suspect_location, suspicious_transactions, criminal_activity, witness_testimony
    Credibility: low, medium, high
    """
    logger.info(f"Tool call: record_information_received from {informant_id}")

    if informant_id not in INFORMANTS_DB:
        return {"error": f"Informant with ID '{informant_id}' not found"}

    valid_types = [
        "suspect_location",
        "suspicious_transactions",
        "criminal_activity",
        "witness_testimony",
    ]
    valid_credibility = ["low", "medium", "high"]

    if information_type not in valid_types:
        return {
            "error": f"Information type '{information_type}' not valid. Valid types: {', '.join(valid_types)}"
        }

    if credibility not in valid_credibility:
        return {
            "error": f"Credibility level '{credibility}' not valid. Valid levels: {', '.join(valid_credibility)}"
        }

    informant = INFORMANTS_DB[informant_id]
    info_id = f"INFO-{str(uuid.uuid4().hex[:3]).upper()}"

    new_information = {
        "id": info_id,
        "informant_id": informant_id,
        "informant_code_name": informant["code_name"],
        "information_type": information_type,
        "content": content,
        "credibility": credibility,
        "date_received": datetime.datetime.now().strftime("%Y-%m-%d"),
        "case_related": "to_be_determined",
        "verification_status": "pending",
        "handler": informant["handler"],
    }

    INFORMATION_DB[info_id] = new_information

    # Update informant counter
    INFORMANTS_DB[informant_id]["information_count"] += 1

    return {
        "status": "success",
        "message": f"Information recorded from '{informant['code_name']}'",
        "information": new_information,
    }


@mcp.tool()
def assess_information_credibility(
    information_id: str, verification_method: str
) -> Dict[str, Any]:
    """
    Evaluates the credibility of received information.
    Verification methods: cross_sources, physical_verification, technical_analysis
    """
    logger.info(f"Tool call: assess_information_credibility for {information_id}")

    if information_id not in INFORMATION_DB:
        return {"error": f"Information with ID '{information_id}' not found"}

    valid_methods = ["cross_sources", "physical_verification", "technical_analysis"]
    if verification_method not in valid_methods:
        return {
            "error": f"Verification method '{verification_method}' not valid. Valid methods: {', '.join(valid_methods)}"
        }

    information = INFORMATION_DB[information_id]

    # Simulate credibility evaluation
    assessment = {
        "information_id": information_id,
        "verification_method": verification_method,
        "date_assessed": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "assessor": "Verification System",
        "original_credibility": information["credibility"],
    }

    # Simplified evaluation logic
    if verification_method == "cross_sources":
        assessment["verification_result"] = "partially_confirmed"
        assessment["confidence_level"] = "75%"
    elif verification_method == "physical_verification":
        assessment["verification_result"] = "confirmed"
        assessment["confidence_level"] = "90%"
    elif verification_method == "technical_analysis":
        assessment["verification_result"] = "pending_additional_analysis"
        assessment["confidence_level"] = "60%"

    # Update information
    INFORMATION_DB[information_id]["verification_status"] = assessment[
        "verification_result"
    ]
    INFORMATION_DB[information_id]["verification_details"] = assessment

    return assessment


@mcp.tool()
def update_informant_reliability(
    informant_id: str, new_level: str, reason: str
) -> Dict[str, Any]:
    """
    Updates the reliability level of an informant.
    Levels: low, medium, high
    """
    logger.info(f"Tool call: update_informant_reliability for {informant_id} to {new_level}")

    if informant_id not in INFORMANTS_DB:
        return {"error": f"Informant with ID '{informant_id}' not found"}

    valid_levels = ["low", "medium", "high"]
    if new_level not in valid_levels:
        return {
            "error": f"Reliability level '{new_level}' not valid. Valid levels: {', '.join(valid_levels)}"
        }

    informant = INFORMANTS_DB[informant_id]
    old_level = informant["reliability_level"]

    INFORMANTS_DB[informant_id]["reliability_level"] = new_level
    INFORMANTS_DB[informant_id]["last_updated"] = datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M"
    )

    # Add to history
    if "reliability_history" not in INFORMANTS_DB[informant_id]:
        INFORMANTS_DB[informant_id]["reliability_history"] = []

    INFORMANTS_DB[informant_id]["reliability_history"].append(
        {
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "old_level": old_level,
            "new_level": new_level,
            "reason": reason,
        }
    )

    return {
        "status": "success",
        "message": f"Reliability of '{informant['code_name']}' updated from '{old_level}' to '{new_level}'",
        "informant_id": informant_id,
        "code_name": informant["code_name"],
        "new_reliability": new_level,
        "reason": reason,
    }


@mcp.tool()
def get_informant_history(informant_id: str) -> Dict[str, Any]:
    """
    Gets the complete history of an informant including provided information and meetings.
    """
    logger.info(f"Tool call: get_informant_history for {informant_id}")

    if informant_id not in INFORMANTS_DB:
        return {"error": f"Informant with ID '{informant_id}' not found"}

    informant = INFORMANTS_DB[informant_id]

    # Collect provided information
    information_history = []
    for info in INFORMATION_DB.values():
        if info["informant_id"] == informant_id:
            information_history.append(info)

    # Collect meetings
    meeting_history = []
    for meeting in MEETINGS_DB.values():
        if meeting["informant_id"] == informant_id:
            meeting_history.append(meeting)

    return {
        "informant_profile": informant,
        "information_provided": sorted(
            information_history, key=lambda x: x["date_received"], reverse=True
        ),
        "meeting_history": sorted(
            meeting_history, key=lambda x: x["date"], reverse=True
        ),
        "total_information_count": len(information_history),
        "total_meetings": len(meeting_history),
    }


@mcp.tool()
def get_network_statistics() -> Dict[str, Any]:
    """
    Provides general statistics about the informant network.
    """
    logger.info("Tool call: get_network_statistics")

    total_informants = len(INFORMANTS_DB)
    active_informants = len(
        [i for i in INFORMANTS_DB.values() if i["status"] == "activo"]
    )

    # Statistics by reliability
    reliability_stats = {"low": 0, "medium": 0, "high": 0}
    for informant in INFORMANTS_DB.values():
        if informant["status"] == "activo":
            reliability_stats[informant["reliability_level"]] += 1

    # Statistics by specialty
    specialty_stats = {}
    for informant in INFORMANTS_DB.values():
        if informant["status"] == "activo":
            specialty = informant["specialty"]
            specialty_stats[specialty] = specialty_stats.get(specialty, 0) + 1

    total_information = len(INFORMATION_DB)
    total_meetings = len(MEETINGS_DB)

    return {
        "network_overview": {
            "total_informants": total_informants,
            "active_informants": active_informants,
            "inactive_informants": total_informants - active_informants,
        },
        "reliability_distribution": reliability_stats,
        "specialty_distribution": specialty_stats,
        "activity_stats": {
            "total_information_received": total_information,
            "total_meetings_scheduled": total_meetings,
            "average_info_per_informant": round(
                total_information / max(active_informants, 1), 1
            ),
        },
    }


@mcp.tool()
def get_active_informants_count() -> Dict[str, Any]:
    """
    Returns the number of active informants in the system.
    """
    logger.info("Tool call: get_active_informants_count")

    active_count = len([i for i in INFORMANTS_DB.values() if i["status"] == "active"])
    inactive_count = len(
        [i for i in INFORMANTS_DB.values() if i["status"] == "inactive"]
    )

    return {
        "active_informants": active_count,
        "inactive_informants": inactive_count,
        "total_informants": active_count + inactive_count,
        "activity_rate": f"{(active_count / max(active_count + inactive_count, 1)) * 100:.1f}%",
    }


# --- SERVER STARTUP SECTION ---
if __name__ == "__main__":
    logger.info(
        f"Attempting to start Informant Management FastMCP server on {SERVER_HOST}:{SERVER_PORT}{SERVER_PATH} with streamable-http transport"
    )
    try:
        mcp.run(transport="streamable-http")
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"An error occurred while starting the server: {e}")
