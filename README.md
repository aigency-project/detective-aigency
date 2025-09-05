# Detective Agency - Multi-Agent Investigation System

Este ejemplo demuestra un sistema multi-agente para una agencia de detectives usando el framework Aigency. El sistema está compuesto por tres agentes especializados que trabajan en coordinación para resolver casos complejos.

## 🕵️ Arquitectura del Sistema

### Agentes Especializados

1. **`case_agent`** - Detective Especialista en Casos
   - Analiza evidencias y desarrolla teorías del caso
   - Crea perfiles de sospechosos
   - Genera informes detallados de investigación
   - Gestiona el estado de los casos

2. **`informant_agent`** - Especialista en Red de Informantes
   - Gestiona la red de informantes
   - Programa encuentros seguros
   - Evalúa la credibilidad de la información
   - Mantiene registros de confiabilidad

3. **`detective_manager_agent`** - Detective Jefe Orquestador
   - Coordina investigaciones complejas
   - Delega tareas a agentes especializados
   - Integra información de múltiples fuentes
   - Gestiona el flujo de trabajo de investigación

### Servicios MCP (Model Context Protocol)

- **Case Management MCP**: Gestión de casos, evidencias y reportes
- **Informant Management MCP**: Gestión de informantes y encuentros

## 🚀 Cómo Ejecutar

### Prerrequisitos

1. Docker y Docker Compose instalados
2. Variables de entorno configuradas en `.env`:
   ```bash
   GIT_TOKEN=your_github_token
   GEMINI_API_KEY=your_gemini_api_key
   ```

### Ejecución

```bash
# Desde el directorio detective_agency
docker-compose up --build
```

### Puertos de Acceso

- **Detective Manager Agent**: http://localhost:8085 (Punto de entrada principal)
- **Case Agent**: http://localhost:8082
- **Informant Agent**: http://localhost:8084
- **Phoenix Observability**: http://localhost:6006
- **A2A Inspector**: http://localhost:6007

## 💼 Casos de Uso

### 1. Investigación Simple
Interactúa directamente con agentes especializados:

**Con Case Agent:**
```
"Analiza el caso de robo en la joyería 'El Diamante' - evidencias: huellas dactilares, video de seguridad, testigo ocular"
```

**Con Informant Agent:**
```
"Busca informantes especializados en robos de joyerías en el centro de la ciudad"
```

### 2. Investigación Coordinada
Usa el Detective Manager para casos complejos:

```
"Investiga el caso de fraude empresarial en TechCorp - necesito análisis de evidencias financieras y contactos con informantes del sector tecnológico"
```

El Detective Manager automáticamente:
1. Delega el análisis de evidencias al Case Agent
2. Coordina con el Informant Agent para obtener información adicional
3. Integra los resultados para proporcionar una investigación completa

### 3. Flujos de Trabajo Típicos

**Caso de Robo:**
1. Case Agent analiza evidencias físicas y digitales
2. Informant Agent contacta informantes del área
3. Detective Manager coordina la información para identificar sospechosos

**Caso de Fraude:**
1. Case Agent examina documentos financieros y patrones
2. Informant Agent busca contactos en el sector financiero
3. Detective Manager desarrolla estrategia de investigación integral

## 🔧 Configuración de Agentes

### Case Agent
- **Especialización**: Análisis forense, desarrollo de teorías, creación de informes
- **Herramientas MCP**: Gestión de casos, análisis de evidencias, reportes
- **Skills**: Análisis de casos, investigación de evidencias, perfilado de sospechosos

### Informant Agent
- **Especialización**: Gestión de red de contactos, evaluación de credibilidad
- **Herramientas MCP**: Gestión de informantes, programación de encuentros
- **Skills**: Gestión de informantes, programación de encuentros, análisis de red

### Detective Manager Agent
- **Especialización**: Orquestación y coordinación
- **Capacidades**: Delegación inteligente, integración de resultados
- **Skills**: Coordinación de investigaciones complejas, delegación especializada

## 📊 Monitoreo y Observabilidad

- **Phoenix**: Dashboard de observabilidad en http://localhost:6006
- **A2A Inspector**: Herramientas de inspección de agentes en http://localhost:6007
- **Logs**: Cada agente genera logs detallados para seguimiento

## 🔍 Ejemplos de Interacción

### Investigación Completa
```
Usuario: "Tenemos un caso de desaparición - María González, 28 años, desapareció hace 3 días. Última vez vista en el centro comercial."

Detective Manager:
1. Delega al Case Agent: "Analiza el caso de desaparición de María González..."
2. Delega al Informant Agent: "Busca informantes en el área del centro comercial..."
3. Integra resultados y proporciona plan de investigación
```

### Análisis Especializado
```
Usuario: "Analiza estas huellas dactilares encontradas en la escena del crimen"

Case Agent:
1. Examina las evidencias proporcionadas
2. Compara con bases de datos
3. Desarrolla perfil del sospechoso
4. Genera reporte técnico
```

## 🛠️ Extensibilidad

El sistema puede expandirse fácilmente:

- **Nuevos Agentes**: Agente forense, agente de ciberseguridad, agente legal
- **Nuevos MCPs**: Base de datos criminal, sistema de vigilancia, análisis de comunicaciones
- **Nuevas Skills**: Análisis de ADN, investigación digital, análisis de redes sociales

## 📝 Notas de Desarrollo

- Cada agente mantiene su especialización y no realiza tareas fuera de su dominio
- El Detective Manager actúa como orquestador sin realizar investigaciones directas
- Los MCPs proporcionan persistencia y herramientas especializadas
- El sistema está diseñado para ser escalable y modular

## 🔐 Consideraciones de Seguridad

- Los informantes se manejan con códigos y nombres clave
- La información sensible se protege en los intercambios entre agentes
- Los encuentros se programan en ubicaciones seguras y discretas
- Los logs no contienen información personal identificable
