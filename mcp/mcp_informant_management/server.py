# server.py
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

mcp = FastMCP(
    name="Informant Management MCP",
    port=SERVER_PORT,
    host=SERVER_HOST,
    log_level="DEBUG",
)

print("Informant Management FastMCP server object created.")

# Base de datos en memoria para informantes
INFORMANTS_DB = {}
MEETINGS_DB = {}
INFORMATION_DB = {}

# Horarios de encuentro disponibles
MEETING_TIMES = ["08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00", "22:00"]

# Ubicaciones seguras para encuentros
SAFE_LOCATIONS = [
    "Café Central - Mesa del fondo",
    "Parque Municipal - Banco junto al lago",
    "Biblioteca Pública - Sala de lectura",
    "Centro Comercial - Food Court",
    "Estación de Tren - Sala de espera",
    "Hotel Plaza - Lobby",
    "Museo de Arte - Sala Medieval",
]

# Datos de ejemplo
SAMPLE_INFORMANTS = [
    {
        "id": "INF-001",
        "code_name": "Cuervo",
        "specialty": "tráfico_drogas",
        "reliability_level": "alto",
        "contact_method": "teléfono_seguro",
        "date_registered": "2025-01-15",
        "handler": "Detective García",
        "status": "activo",
        "location_area": "centro_ciudad",
        "information_count": 12,
        "successful_tips": 9,
    },
    {
        "id": "INF-002",
        "code_name": "Sombra",
        "specialty": "fraude_financiero",
        "reliability_level": "medio",
        "contact_method": "email_encriptado",
        "date_registered": "2025-02-20",
        "handler": "Detective Martínez",
        "status": "activo",
        "location_area": "distrito_financiero",
        "information_count": 8,
        "successful_tips": 5,
    },
    {
        "id": "INF-003",
        "code_name": "Fantasma",
        "specialty": "robos_joyerías",
        "reliability_level": "alto",
        "contact_method": "contacto_presencial",
        "date_registered": "2024-11-10",
        "handler": "Detective Ruiz",
        "status": "activo",
        "location_area": "centro_comercial",
        "information_count": 15,
        "successful_tips": 13,
    },
    {
        "id": "INF-004",
        "code_name": "Eco",
        "specialty": "desapariciones",
        "reliability_level": "bajo",
        "contact_method": "teléfono_seguro",
        "date_registered": "2025-03-01",
        "handler": "Detective López",
        "status": "inactivo",
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
        "purpose": "Información sobre red de distribución",
        "status": "programado",
        "handler": "Detective García",
        "security_level": "alto",
    },
    {
        "id": "MEET-002",
        "informant_id": "INF-002",
        "informant_code_name": "Sombra",
        "date": "2025-09-04",
        "time": "14:00",
        "location": "Biblioteca Pública - Sala de lectura",
        "purpose": "Seguimiento caso TechCorp",
        "status": "completado",
        "handler": "Detective Martínez",
        "security_level": "medio",
    },
]

SAMPLE_INFORMATION = [
    {
        "id": "INFO-001",
        "informant_id": "INF-001",
        "informant_code_name": "Cuervo",
        "information_type": "ubicación_sospechoso",
        "content": "Sospechoso del robo joyería visto en barrio industrial",
        "credibility": "alta",
        "date_received": "2025-09-03",
        "case_related": "CASE-001",
        "verification_status": "pendiente",
        "handler": "Detective García",
    },
    {
        "id": "INFO-002",
        "informant_id": "INF-002",
        "informant_code_name": "Sombra",
        "information_type": "transacciones_sospechosas",
        "content": "Movimientos bancarios anómalos en cuentas TechCorp detectados",
        "credibility": "media",
        "date_received": "2025-09-01",
        "case_related": "CASE-002",
        "verification_status": "verificado",
        "handler": "Detective Martínez",
    },
]


def initialize_data():
    """Inicializa la base de datos con datos de ejemplo"""
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
    Registra un nuevo informante en el sistema.
    Especialidades: tráfico_drogas, fraude_financiero, robos_joyerías, desapariciones, corrupción, cibercriminalidad
    Niveles de confianza: bajo, medio, alto
    Métodos de contacto: teléfono_seguro, email_encriptado, contacto_presencial
    """
    print(f"Tool call: register_new_informant - {code_name}, specialty: {specialty}")

    valid_specialties = [
        "tráfico_drogas",
        "fraude_financiero",
        "robos_joyerías",
        "desapariciones",
        "corrupción",
        "cibercriminalidad",
    ]
    valid_reliability = ["bajo", "medio", "alto"]
    valid_contact_methods = [
        "teléfono_seguro",
        "email_encriptado",
        "contacto_presencial",
    ]

    if specialty not in valid_specialties:
        return {
            "error": f"Especialidad '{specialty}' no válida. Especialidades válidas: {', '.join(valid_specialties)}"
        }

    if reliability_level not in valid_reliability:
        return {
            "error": f"Nivel de confianza '{reliability_level}' no válido. Niveles válidos: {', '.join(valid_reliability)}"
        }

    if contact_method not in valid_contact_methods:
        return {
            "error": f"Método de contacto '{contact_method}' no válido. Métodos válidos: {', '.join(valid_contact_methods)}"
        }

    # Verificar que el nombre clave no exista
    for informant in INFORMANTS_DB.values():
        if informant["code_name"].lower() == code_name.lower():
            return {
                "error": f"Ya existe un informante con el nombre clave '{code_name}'"
            }

    informant_id = f"INF-{str(uuid.uuid4().hex[:3]).upper()}"
    new_informant = {
        "id": informant_id,
        "code_name": code_name,
        "specialty": specialty,
        "reliability_level": reliability_level,
        "contact_method": contact_method,
        "date_registered": datetime.datetime.now().strftime("%Y-%m-%d"),
        "handler": "Sistema Automático",
        "status": "activo",
        "location_area": "por_determinar",
        "information_count": 0,
        "successful_tips": 0,
    }

    INFORMANTS_DB[informant_id] = new_informant

    return {
        "status": "success",
        "message": f"Informante '{code_name}' registrado exitosamente",
        "informant": new_informant,
    }


@mcp.tool()
def schedule_informant_meeting(
    informant_id: str, date: str, time: str, location: str, purpose: str
) -> Dict[str, Any]:
    """
    Programa un encuentro con un informante.
    Formato fecha: YYYY-MM-DD
    Horarios disponibles: 08:00, 10:00, 12:00, 14:00, 16:00, 18:00, 20:00, 22:00
    """
    print(
        f"Tool call: schedule_informant_meeting for {informant_id} on {date} at {time}"
    )

    if informant_id not in INFORMANTS_DB:
        return {"error": f"Informante con ID '{informant_id}' no encontrado"}

    # Validar formato de fecha
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return {"error": f"Formato de fecha '{date}' incorrecto. Usa YYYY-MM-DD"}

    if time not in MEETING_TIMES:
        return {
            "error": f"Horario '{time}' no disponible. Horarios válidos: {', '.join(MEETING_TIMES)}"
        }

    # Verificar disponibilidad (no dos encuentros al mismo tiempo)
    for meeting in MEETINGS_DB.values():
        if (
            meeting["date"] == date
            and meeting["time"] == time
            and meeting["status"] == "programado"
        ):
            return {"error": f"Ya hay un encuentro programado para {date} a las {time}"}

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
        "status": "programado",
        "handler": informant["handler"],
        "security_level": "medio",
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

    MEETINGS_DB[meeting_id] = new_meeting

    return {
        "status": "success",
        "message": f"Encuentro programado con '{informant['code_name']}'",
        "meeting": new_meeting,
        "security_instructions": f"Código de encuentro: {meeting_id}. Ubicación: {location}. Mantener protocolo de seguridad nivel {new_meeting['security_level']}.",
    }


@mcp.tool()
def check_meeting_availability(date: str, time: str, location: str) -> Dict[str, Any]:
    """
    Verifica disponibilidad para programar un encuentro en fecha, hora y ubicación específicas.
    """
    print(f"Tool call: check_meeting_availability for {date} at {time} in {location}")

    # Validar formato de fecha
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return {"error": f"Formato de fecha '{date}' incorrecto. Usa YYYY-MM-DD"}

    if time not in MEETING_TIMES:
        return {
            "error": f"Horario '{time}' no disponible. Horarios válidos: {', '.join(MEETING_TIMES)}"
        }

    # Verificar conflictos
    conflicts = []
    for meeting in MEETINGS_DB.values():
        if meeting["status"] == "programado":
            if meeting["date"] == date and meeting["time"] == time:
                conflicts.append(
                    f"Encuentro con {meeting['informant_code_name']} ya programado"
                )
            if meeting["date"] == date and meeting["location"] == location:
                time_diff = abs(int(meeting["time"][:2]) - int(time[:2]))
                if time_diff < 2:  # Menos de 2 horas de diferencia
                    conflicts.append(
                        f"Ubicación ocupada cerca del horario por {meeting['informant_code_name']}"
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
        "message": f"Disponible para encuentro el {date} a las {time} en {location}",
        "security_recommendations": f"Ubicación segura confirmada. Nivel de seguridad recomendado: medio.",
    }


@mcp.tool()
def find_informants_by_specialty(specialty: str) -> List[Dict[str, Any]]:
    """
    Busca informantes por área de especialización.
    """
    print(f"Tool call: find_informants_by_specialty for {specialty}")

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
            "message": f"No se encontraron informantes especializados en '{specialty}'"
        }
    )


@mcp.tool()
def get_informant_profile(informant_id: str) -> Dict[str, Any]:
    """
    Obtiene el perfil completo de un informante específico.
    """
    print(f"Tool call: get_informant_profile for {informant_id}")

    if informant_id not in INFORMANTS_DB:
        return {"error": f"Informante con ID '{informant_id}' no encontrado"}

    informant = INFORMANTS_DB[informant_id].copy()

    # Agregar estadísticas adicionales
    informant["success_rate"] = (
        f"{(informant['successful_tips'] / max(informant['information_count'], 1)) * 100:.1f}%"
    )

    # Agregar encuentros recientes
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
    Lista informantes filtrados por nivel de confiabilidad.
    Niveles: bajo, medio, alto
    """
    print(f"Tool call: get_informants_by_reliability for level {reliability_level}")

    valid_levels = ["bajo", "medio", "alto"]
    if reliability_level not in valid_levels:
        return {
            "error": f"Nivel de confiabilidad '{reliability_level}' no válido. Niveles válidos: {', '.join(valid_levels)}"
        }

    matching_informants = []
    for informant in INFORMANTS_DB.values():
        if (
            informant["reliability_level"] == reliability_level
            and informant["status"] == "activo"
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
            "message": f"No se encontraron informantes activos con confiabilidad '{reliability_level}'"
        }
    )


@mcp.tool()
def record_information_received(
    informant_id: str, information_type: str, content: str, credibility: str
) -> Dict[str, Any]:
    """
    Registra información recibida de un informante.
    Tipos: ubicación_sospechoso, transacciones_sospechosas, actividad_criminal, testimonio_testigo
    Credibilidad: baja, media, alta
    """
    print(f"Tool call: record_information_received from {informant_id}")

    if informant_id not in INFORMANTS_DB:
        return {"error": f"Informante con ID '{informant_id}' no encontrado"}

    valid_types = [
        "ubicación_sospechoso",
        "transacciones_sospechosas",
        "actividad_criminal",
        "testimonio_testigo",
    ]
    valid_credibility = ["baja", "media", "alta"]

    if information_type not in valid_types:
        return {
            "error": f"Tipo de información '{information_type}' no válido. Tipos válidos: {', '.join(valid_types)}"
        }

    if credibility not in valid_credibility:
        return {
            "error": f"Nivel de credibilidad '{credibility}' no válido. Niveles válidos: {', '.join(valid_credibility)}"
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
        "case_related": "por_determinar",
        "verification_status": "pendiente",
        "handler": informant["handler"],
    }

    INFORMATION_DB[info_id] = new_information

    # Actualizar contador del informante
    INFORMANTS_DB[informant_id]["information_count"] += 1

    return {
        "status": "success",
        "message": f"Información registrada de '{informant['code_name']}'",
        "information": new_information,
    }


@mcp.tool()
def assess_information_credibility(
    information_id: str, verification_method: str
) -> Dict[str, Any]:
    """
    Evalúa la credibilidad de información recibida.
    Métodos de verificación: cruzar_fuentes, verificación_física, análisis_técnico
    """
    print(f"Tool call: assess_information_credibility for {information_id}")

    if information_id not in INFORMATION_DB:
        return {"error": f"Información con ID '{information_id}' no encontrada"}

    valid_methods = ["cruzar_fuentes", "verificación_física", "análisis_técnico"]
    if verification_method not in valid_methods:
        return {
            "error": f"Método de verificación '{verification_method}' no válido. Métodos válidos: {', '.join(valid_methods)}"
        }

    information = INFORMATION_DB[information_id]

    # Simular evaluación de credibilidad
    assessment = {
        "information_id": information_id,
        "verification_method": verification_method,
        "date_assessed": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "assessor": "Sistema de Verificación",
        "original_credibility": information["credibility"],
    }

    # Lógica de evaluación simplificada
    if verification_method == "cruzar_fuentes":
        assessment["verification_result"] = "confirmado_parcialmente"
        assessment["confidence_level"] = "75%"
    elif verification_method == "verificación_física":
        assessment["verification_result"] = "confirmado"
        assessment["confidence_level"] = "90%"
    elif verification_method == "análisis_técnico":
        assessment["verification_result"] = "pendiente_análisis_adicional"
        assessment["confidence_level"] = "60%"

    # Actualizar información
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
    Actualiza el nivel de confiabilidad de un informante.
    Niveles: bajo, medio, alto
    """
    print(f"Tool call: update_informant_reliability for {informant_id} to {new_level}")

    if informant_id not in INFORMANTS_DB:
        return {"error": f"Informante con ID '{informant_id}' no encontrado"}

    valid_levels = ["bajo", "medio", "alto"]
    if new_level not in valid_levels:
        return {
            "error": f"Nivel de confiabilidad '{new_level}' no válido. Niveles válidos: {', '.join(valid_levels)}"
        }

    informant = INFORMANTS_DB[informant_id]
    old_level = informant["reliability_level"]

    INFORMANTS_DB[informant_id]["reliability_level"] = new_level
    INFORMANTS_DB[informant_id]["last_updated"] = datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M"
    )

    # Agregar al historial
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
        "message": f"Confiabilidad de '{informant['code_name']}' actualizada de '{old_level}' a '{new_level}'",
        "informant_id": informant_id,
        "code_name": informant["code_name"],
        "new_reliability": new_level,
        "reason": reason,
    }


@mcp.tool()
def get_informant_history(informant_id: str) -> Dict[str, Any]:
    """
    Obtiene el historial completo de un informante incluyendo información proporcionada y encuentros.
    """
    print(f"Tool call: get_informant_history for {informant_id}")

    if informant_id not in INFORMANTS_DB:
        return {"error": f"Informante con ID '{informant_id}' no encontrado"}

    informant = INFORMANTS_DB[informant_id]

    # Recopilar información proporcionada
    information_history = []
    for info in INFORMATION_DB.values():
        if info["informant_id"] == informant_id:
            information_history.append(info)

    # Recopilar encuentros
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
    Proporciona estadísticas generales sobre la red de informantes.
    """
    print("Tool call: get_network_statistics")

    total_informants = len(INFORMANTS_DB)
    active_informants = len(
        [i for i in INFORMANTS_DB.values() if i["status"] == "activo"]
    )

    # Estadísticas por confiabilidad
    reliability_stats = {"bajo": 0, "medio": 0, "alto": 0}
    for informant in INFORMANTS_DB.values():
        if informant["status"] == "activo":
            reliability_stats[informant["reliability_level"]] += 1

    # Estadísticas por especialidad
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
    Devuelve el número de informantes activos en el sistema.
    """
    print("Tool call: get_active_informants_count")

    active_count = len([i for i in INFORMANTS_DB.values() if i["status"] == "activo"])
    inactive_count = len(
        [i for i in INFORMANTS_DB.values() if i["status"] == "inactivo"]
    )

    return {
        "active_informants": active_count,
        "inactive_informants": inactive_count,
        "total_informants": active_count + inactive_count,
        "activity_rate": f"{(active_count / max(active_count + inactive_count, 1)) * 100:.1f}%",
    }


# --- SECCIÓN PARA INICIAR EL SERVIDOR ---
if __name__ == "__main__":
    print(
        f"Attempting to start Informant Management FastMCP server on {SERVER_HOST}:{SERVER_PORT}{SERVER_PATH} with streamable-http transport"
    )
    try:
        mcp.run(transport="streamable-http")
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    except Exception as e:
        print(f"An error occurred while starting the server: {e}")
