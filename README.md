# Detective Agency - Multi-Agent Investigation System

This example demonstrates a multi-agent system for a detective agency using the Aigency framework. The system is composed of three specialized agents that work in coordination to solve complex cases.

## 🕵️ System Architecture

### Specialized Agents

1. **`case_agent`** - Case Specialist Detective
   - Analyzes evidence and develops case theories
   - Creates suspect profiles
   - Produces detailed investigation reports
   - Manages case status

2. **`informant_agent`** - Informant Network Specialist
   - Manages the network of informants
   - Schedules secure meetings
   - Assesses the credibility of information
   - Maintains reliability records

3. **`detective_manager_agent`** - Chief Detective Orchestrator
   - Coordinates complex investigations
   - Delegates tasks to specialized agents
   - Integrates information from multiple sources
   - Manages the investigation workflow

### MCP Services (Model Context Protocol)

- **Case Management MCP**: Management of cases, evidence, and reports
- **Informant Management MCP**: Management of informants and meetings

## 🚀 How to Run

### Prerequisites

1. Docker and Docker Compose installed
2. Environment variables configured in `.env`:
   ```bash
   GOOGLE_GENAI_USE_VERTEXAI=FALSE
   GEMINI_API_KEY=your_gemini_api_key
   ```

### Run

```bash
# From the detective-aigency directory
docker-compose up --build
```

### Access Ports

- **Detective Manager Agent**: http://localhost:8085 (Main entry point)
- **Case Agent**: http://localhost:8082
- **Informant Agent**: http://localhost:8084
- **Phoenix Observability**: http://localhost:6006
- **A2A Inspector**: http://localhost:6007

## 💼 Use Cases

### 1. Simple Investigation
Interact directly with specialized agents:

**With Case Agent:**
```
"Analyze the robbery case at the 'El Diamante' jewelry store - evidence: fingerprints, security video, eyewitness"
```

**With Informant Agent:**
```
"Find informants specialized in jewelry store robberies in the city center"
```

### 2. Coordinated Investigation
Use the Detective Manager for complex cases:

```
"Investigate the corporate fraud case at TechCorp - I need analysis of financial evidence and contacts with informants from the technology sector"
```

The Detective Manager automatically:
1. Delegates evidence analysis to the Case Agent
2. Coordinates with the Informant Agent to obtain additional information
3. Integrates the results to provide a complete investigation

### 3. Typical Workflows

**Robbery Case:**
1. Case Agent analyzes physical and digital evidence
2. Informant Agent contacts local informants
3. Detective Manager coordinates information to identify suspects

**Fraud Case:**
1. Case Agent examines financial documents and patterns
2. Informant Agent searches for contacts in the financial sector
3. Detective Manager develops a comprehensive investigation strategy

## 🔧 Agent Configuration

### Case Agent
- **Specialization**: Forensic analysis, theory development, report creation
- **MCP Tools**: Case management, evidence analysis, reporting
- **Skills**: Case analysis, evidence investigation, suspect profiling

### Informant Agent
- **Specialization**: Contact network management, credibility assessment
- **MCP Tools**: Informant management, meeting scheduling
- **Skills**: Informant management, meeting scheduling, network analysis

### Detective Manager Agent
- **Specialization**: Orchestration and coordination
- **Capabilities**: Intelligent delegation, result integration
- **Skills**: Coordination of complex investigations, specialized delegation

## 📊 Monitoring and Observability

- **Phoenix**: Observability dashboard at http://localhost:6006
- **A2A Inspector**: Agent inspection tools at http://localhost:6007
- **Logs**: Each agent generates detailed logs for tracing

## 🔍 Interaction Examples

### Complete Investigation
```
User: "We have a missing person case - María González, 28 years old, has been missing for 3 days. Last seen at the shopping mall."

Detective Manager:
1. Delegates to Case Agent: "Analyze the missing person case of María González..."
2. Delegates to Informant Agent: "Find informants in the shopping mall area..."
3. Integrates results and provides an investigation plan
```

### Specialized Analysis
```
User: "Analyze these fingerprints found at the crime scene"

Case Agent:
1. Examines the provided evidence
2. Compares with databases
3. Develops the suspect profile
4. Generates a technical report
```

## 🛠️ Extensibility

The system can be easily expanded:

- **New Agents**: Forensic agent, cybersecurity agent, legal agent
- **New MCPs**: Criminal database, surveillance system, communications analysis
- **New Skills**: DNA analysis, digital investigation, social network analysis

## 📝 Development Notes

- Each agent maintains its specialization and does not perform tasks outside its domain
- The Detective Manager acts as an orchestrator without conducting direct investigations
- MCPs provide persistence and specialized tools
- The system is designed to be scalable and modular

## 🔐 Security Considerations

- Informants are handled with codes and codenames
- Sensitive information is protected in exchanges between agents
- Meetings are scheduled in safe and discreet locations
- Logs do not contain personally identifiable information
