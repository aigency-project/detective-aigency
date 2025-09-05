# server.py
from mcp.server.fastmcp import FastMCP
from mcp.types import PromptMessage, TextContent
from typing import List, Dict, Any, Optional, Union
import json
import uuid
import datetime

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8080
SERVER_PATH = "/mcp"

mcp = FastMCP(
    name="Case Management MCP", port=SERVER_PORT, host=SERVER_HOST, log_level="DEBUG"
)

print("Case Management FastMCP server object created.")

# Base de datos en memoria para casos
CASES_DB = {}
EVIDENCE_DB = {}
REPORTS_DB = {}

# Datos de ejemplo
SAMPLE_CASES = [
    {
        "id": "CASE-001",
        "title": "Robo en Joyería El Diamante",
        "type": "robo",
        "status": "abierto",
        "description": "Robo nocturno en joyería del centro. Entrada forzada, caja fuerte abierta.",
        "date_created": "2025-09-01",
        "priority": "alta",
        "assigned_detective": "Detective García",
        "evidence_ids": ["EVID-001", "EVID-002"],
        "suspects": ["Sospechoso desconocido - huellas dactilares"],
        "location": "Calle Mayor 15, Centro",
    },
    {
        "id": "CASE-002",
        "title": "Fraude Empresarial TechCorp",
        "type": "fraude",
        "status": "en_investigacion",
        "description": "Posible malversación de fondos en empresa tecnológica.",
        "date_created": "2025-08-28",
        "priority": "alta",
        "assigned_detective": "Detective Martínez",
        "evidence_ids": ["EVID-003", "EVID-004"],
        "suspects": ["Carlos Mendoza - CFO", "Ana López - Contadora"],
        "location": "TechCorp Offices, Polígono Industrial",
    },
    {
        "id": "CASE-003",
        "title": "Desaparición María González",
        "type": "desaparicion",
        "status": "abierto",
        "description": "Mujer de 28 años desaparecida hace 3 días. Última vez vista en centro comercial.",
        "date_created": "2025-09-02",
        "priority": "crítica",
        "assigned_detective": "Detective Ruiz",
        "evidence_ids": ["EVID-005"],
        "suspects": [],
        "location": "Centro Comercial Plaza Norte",
    },
]

SAMPLE_EVIDENCE = [
    {
        "id": "EVID-001",
        "case_id": "CASE-001",
        "type": "huellas_dactilares",
        "description": "Huellas dactilares encontradas en la caja fuerte",
        "location_found": "Caja fuerte principal",
        "date_collected": "2025-09-01",
        "status": "pendiente_análisis",
        "chain_of_custody": ["Detective García", "Laboratorio Forense"],
        "analysis_results": None,
    },
    {
        "id": "EVID-002",
        "case_id": "CASE-001",
        "type": "video_seguridad",
        "description": "Grabación de cámaras de seguridad del exterior",
        "location_found": "Cámara exterior calle Mayor",
        "date_collected": "2025-09-01",
        "status": "analizado",
        "chain_of_custody": ["Detective García", "Técnico IT"],
        "analysis_results": "Figura encapuchada, aproximadamente 1.75m, entrada a las 02:30",
    },
    {
        "id": "EVID-003",
        "case_id": "CASE-002",
        "type": "documentos_financieros",
        "description": "Registros contables de los últimos 6 meses",
        "location_found": "Oficina de contabilidad TechCorp",
        "date_collected": "2025-08-28",
        "status": "en_análisis",
        "chain_of_custody": ["Detective Martínez", "Auditor Forense"],
        "analysis_results": "Discrepancias en transferencias por €250,000",
    },
    {
        "id": "EVID-004",
        "case_id": "CASE-002",
        "type": "registros_bancarios",
        "description": "Extractos bancarios de cuentas corporativas",
        "location_found": "Banco Central",
        "date_collected": "2025-08-29",
        "status": "analizado",
        "chain_of_custody": ["Detective Martínez", "Especialista Financiero"],
        "analysis_results": "Transferencias no autorizadas a cuentas offshore",
    },
    {
        "id": "EVID-005",
        "case_id": "CASE-003",
        "type": "video_seguridad",
        "description": "Última grabación de María González en centro comercial",
        "location_found": "Centro Comercial Plaza Norte - Entrada principal",
        "date_collected": "2025-09-02",
        "status": "analizado",
        "chain_of_custody": ["Detective Ruiz", "Técnico Seguridad"],
        "analysis_results": "Última vez vista a las 18:45, saliendo sola por entrada principal",
    },
]


def initialize_data():
    """Inicializa la base de datos con datos de ejemplo"""
    for case in SAMPLE_CASES:
        CASES_DB[case["id"]] = case

    for evidence in SAMPLE_EVIDENCE:
        EVIDENCE_DB[evidence["id"]] = evidence


initialize_data()


@mcp.tool()
def get_case_details(case_id: str) -> Dict[str, Any]:
    """
    Obtiene detalles completos de un caso específico por su ID.
    """
    print(f"Tool call: get_case_details for case ID: {case_id}")

    if case_id not in CASES_DB:
        return {"error": f"Caso con ID '{case_id}' no encontrado."}

    case = CASES_DB[case_id].copy()

    # Agregar evidencias relacionadas
    case_evidence = []
    for evid_id in case.get("evidence_ids", []):
        if evid_id in EVIDENCE_DB:
            case_evidence.append(EVIDENCE_DB[evid_id])

    case["evidence_details"] = case_evidence
    return case


@mcp.tool()
def search_cases_by_type(case_type: str) -> List[Dict[str, Any]]:
    """
    Busca casos por tipo (robo, fraude, desaparicion, homicidio, etc.).
    """
    print(f"Tool call: search_cases_by_type for type: {case_type}")

    matching_cases = []
    for case in CASES_DB.values():
        if case["type"].lower() == case_type.lower():
            matching_cases.append(case)

    return (
        matching_cases
        if matching_cases
        else {"message": f"No se encontraron casos de tipo '{case_type}'."}
    )


@mcp.tool()
def search_cases_by_status(status: str) -> List[Dict[str, Any]]:
    """
    Busca casos por estado (abierto, cerrado, en_investigacion, archivado).
    """
    print(f"Tool call: search_cases_by_status for status: {status}")

    matching_cases = []
    for case in CASES_DB.values():
        if case["status"].lower() == status.lower():
            matching_cases.append(case)

    return (
        matching_cases
        if matching_cases
        else {"message": f"No se encontraron casos con estado '{status}'."}
    )


@mcp.tool()
def get_evidence_details(evidence_id: str) -> Dict[str, Any]:
    """
    Obtiene detalles de una evidencia específica por su ID.
    """
    print(f"Tool call: get_evidence_details for evidence ID: {evidence_id}")

    if evidence_id not in EVIDENCE_DB:
        return {"error": f"Evidencia con ID '{evidence_id}' no encontrada."}

    return EVIDENCE_DB[evidence_id]


@mcp.tool()
def analyze_evidence(evidence_id: str, analysis_type: str) -> Dict[str, Any]:
    """
    Realiza análisis específico de una evidencia.
    Tipos de análisis: forense, digital, financiero, psicológico.
    """
    print(
        f"Tool call: analyze_evidence for evidence ID: {evidence_id}, analysis type: {analysis_type}"
    )

    if evidence_id not in EVIDENCE_DB:
        return {"error": f"Evidencia con ID '{evidence_id}' no encontrada."}

    evidence = EVIDENCE_DB[evidence_id]

    # Simular análisis basado en tipo
    analysis_results = {
        "evidence_id": evidence_id,
        "analysis_type": analysis_type,
        "date_analyzed": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "analyst": f"Especialista en {analysis_type}",
        "status": "completado",
    }

    if analysis_type.lower() == "forense":
        if evidence["type"] == "huellas_dactilares":
            analysis_results["findings"] = (
                "Huellas parciales identificadas, 12 puntos de comparación disponibles"
            )
            analysis_results["confidence"] = "85%"
        elif evidence["type"] == "video_seguridad":
            analysis_results["findings"] = (
                "Análisis de movimiento y características físicas completado"
            )
            analysis_results["confidence"] = "70%"
    elif analysis_type.lower() == "digital":
        analysis_results["findings"] = (
            "Metadatos extraídos, análisis de integridad completado"
        )
        analysis_results["confidence"] = "95%"
    elif analysis_type.lower() == "financiero":
        analysis_results["findings"] = "Patrones de transacción anómalos identificados"
        analysis_results["confidence"] = "90%"

    # Actualizar evidencia con resultados
    EVIDENCE_DB[evidence_id]["analysis_results"] = analysis_results
    EVIDENCE_DB[evidence_id]["status"] = "analizado"

    return analysis_results


@mcp.tool()
def create_case_report(
    case_id: str, findings: str, recommendations: str
) -> Dict[str, Any]:
    """
    Crea un informe oficial del caso con hallazgos y recomendaciones.
    """
    print(f"Tool call: create_case_report for case ID: {case_id}")

    if case_id not in CASES_DB:
        return {"error": f"Caso con ID '{case_id}' no encontrado."}

    report_id = f"RPT-{uuid.uuid4().hex[:8].upper()}"
    report = {
        "id": report_id,
        "case_id": case_id,
        "case_title": CASES_DB[case_id]["title"],
        "date_created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "author": "Sistema de Gestión de Casos",
        "findings": findings,
        "recommendations": recommendations,
        "status": "draft",
        "case_status_at_report": CASES_DB[case_id]["status"],
    }

    REPORTS_DB[report_id] = report

    return {
        "status": "success",
        "message": "Informe creado exitosamente",
        "report": report,
    }


@mcp.tool()
def get_case_status(case_id: str) -> Dict[str, Any]:
    """
    Verifica el estado actual de un caso.
    """
    print(f"Tool call: get_case_status for case ID: {case_id}")

    if case_id not in CASES_DB:
        return {"error": f"Caso con ID '{case_id}' no encontrado."}

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
    Actualiza el estado de un caso con notas explicativas.
    Estados válidos: abierto, en_investigacion, cerrado, archivado.
    """
    print(
        f"Tool call: update_case_status for case ID: {case_id} to status: {new_status}"
    )

    if case_id not in CASES_DB:
        return {"error": f"Caso con ID '{case_id}' no encontrado."}

    valid_statuses = ["abierto", "en_investigacion", "cerrado", "archivado"]
    if new_status.lower() not in valid_statuses:
        return {
            "error": f"Estado '{new_status}' no válido. Estados válidos: {', '.join(valid_statuses)}"
        }

    old_status = CASES_DB[case_id]["status"]
    CASES_DB[case_id]["status"] = new_status.lower()
    CASES_DB[case_id]["last_updated"] = datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M"
    )

    # Agregar nota al historial
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
        "message": f"Estado del caso {case_id} actualizado de '{old_status}' a '{new_status.lower()}'",
        "case_id": case_id,
        "new_status": new_status.lower(),
        "notes": notes,
    }


# --- SECCIÓN PARA INICIAR EL SERVIDOR ---
if __name__ == "__main__":
    print(
        f"Attempting to start Case Management FastMCP server on {SERVER_HOST}:{SERVER_PORT}{SERVER_PATH} with streamable-http transport"
    )
    try:
        mcp.run(transport="streamable-http")
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    except Exception as e:
        print(f"An error occurred while starting the server: {e}")
