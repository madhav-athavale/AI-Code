# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Module 1 of the AWS Agentic AI Learning Series: An AWS Infrastructure Agent built with the AWS Strands framework. This agent observes and analyzes AWS infrastructure (ECS, EC2, RDS, Lambda) in a read-only mode, implementing the Phase 1 "Assist" pattern where the agent observes and recommends, but humans act.

**Core Architecture:** Three-layer agent design
- **Reasoning Layer:** Claude Sonnet 4 via Amazon Bedrock (or Hugging Face models via Bedrock Marketplace)
- **Orchestration Layer:** AWS Strands Agent with Think → Act → Observe loop
- **Tools Layer:** 5 read-only AWS tools + human-in-the-loop escalation

**Key Design Principle:** Model-agnostic architecture - swap between Anthropic and Hugging Face models with a single line change while keeping all other components identical.

## Architecture

### Three Layers in Practice

1. **Reasoning Layer** (`config/models.py`):
   - `get_bedrock_model()` - Claude Sonnet 4 via Bedrock (default)
   - `get_hf_bedrock_model(endpoint_arn)` - Hugging Face models via Bedrock Marketplace
   - Temperature 0.1 for deterministic infrastructure analysis

2. **Orchestration Layer** (`agent.py`):
   - `create_agent()` - Factory that assembles all components
   - `SlidingWindowConversationManager(window_size=10)` - Short-term memory (last 10 turns)
   - `LoopObserver` - Callback handler that prints Think → Act → Observe steps
   - System prompt defines strict read-only constraints and HITL pattern

3. **Tools Layer** (`tools/aws_tools.py`):
   - `list_aws_resources(service_type, region)` - List ECS/EC2/RDS/Lambda resources
   - `describe_resource(service_type, resource_name, region)` - Detailed drill-down
   - `check_resource_health(service_type, resource_name, region)` - Health verdict
   - `get_environment_summary(region)` - Cross-service overview
   - `request_human_review(...)` - Human-in-the-loop escalation (ONLY action path)

### Agent Loop Flow

```
USER REQUEST → Agent initialized
     ↓
🧠 THINK  (model reasons over context)
     ↓
🔧 ACT    (calls tool: list_aws_resources)
     ↓
✓ OBSERVE (tool result added to context)
     ↓
🧠 THINK  (reasons with new data)
     ↓
🔧 ACT    (calls tool: check_resource_health)
     ↓
✓ OBSERVE (health data added)
     ↓
🧠 THINK  (synthesis)
     ↓
RESPONSE (structured findings + recommendations)
```

## Running the Code

### Development Mode

```bash
# Mock mode (no AWS credentials needed - uses realistic simulated data)
AGENT_MOCK_AWS=true python app.py
# Serves HTTP server on http://localhost:8080

# Test locally with curl
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Give me a health summary of us-east-1"}'

# Interactive test with verbose output
AGENT_MOCK_AWS=true python -c "
from module1.agent import create_agent
agent = create_agent(verbose=True)
response = agent('Give me a health summary of us-east-1')
print(response)
"
```

### Live AWS Mode

```bash
# Prerequisites:
# 1. AWS credentials configured (aws configure)
# 2. Bedrock model access enabled for Anthropic in AWS Console

# Run against real AWS
python app.py

# Test with real resources
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "List all ECS services in us-west-2"}'
```

### Running Tests

```bash
# Run all Module 1 tests in mock mode
AGENT_MOCK_AWS=true pytest ../tests/test_tools.py -v

# Run specific test
AGENT_MOCK_AWS=true pytest ../tests/test_tools.py::test_list_ecs_services -v
```

### Demo Sections

```bash
# Run full workshop demo (6 sections)
AGENT_MOCK_AWS=true python ../demos/module1_demo.py

# Run specific section (1-6)
AGENT_MOCK_AWS=true python ../demos/module1_demo.py --section 4

# Sections:
# 1. Architecture anatomy
# 2. The Think→Act→Observe loop
# 3. Multi-step reasoning
# 4. Human-in-the-loop pattern
# 5. Model swap (Anthropic ↔ Hugging Face)
# 6. Context window management
```

## Deployment

### AgentCore Runtime Deployment

```bash
# 1. Install CLI toolkit
pip install bedrock-agentcore-starter-toolkit

# 2. Configure deployment (run once)
agentcore configure --entrypoint app.py --disable-memory

# 3. Test locally (serves on http://localhost:8080)
AGENT_MOCK_AWS=true python app.py

# 4. Deploy to AWS (CodeBuild, no Docker needed)
agentcore launch

# 5. Invoke deployed agent
agentcore invoke '{"prompt": "List ECS services in us-east-1"}'

# 6. Invoke via boto3 (see ../scripts/invoke_agentcore.py)
export AGENTCORE_ARN="arn:aws:bedrock-agentcore:..."
python ../scripts/invoke_agentcore.py --prompt "Health check us-east-1"
```

## Environment Variables

- `AGENT_MOCK_AWS` - Set to `true` for mock mode (no AWS credentials needed)
- `AWS_REGION` / `AWS_DEFAULT_REGION` - AWS region (defaults to us-east-1)
- `HF_ENDPOINT_ARN` - SageMaker endpoint ARN for Hugging Face models

## Mock Data Reference

With `AGENT_MOCK_AWS=true`, tools return realistic simulated data:

**Healthy Resources:**
- `api-gateway-svc` (ECS) - 3/3 tasks running
- `auth-service` (ECS) - 2/2 tasks running  
- `prod-postgres-01` (RDS) - Multi-AZ, available

**Degraded Resources (trigger HITL):**
- `notification-svc` (ECS) - 1/2 tasks, EssentialContainerExited event
- `reporting-mysql` (RDS) - Single-AZ, no failover

**Other:**
- 4 EC2 instances (3 running, 1 stopped)
- 3 Lambda functions (all active)

## Key Constraints & Patterns

### Read-Only Phase 1 Pattern

**ALL tools are read-only.** The agent CANNOT create, modify, or delete AWS resources directly.

- To propose infrastructure changes: agent MUST use `request_human_review()` tool
- Agent never describes what it "would" do - it raises a formal review request
- This implements the "Assist" phase of adoption (observe → recommend → human acts)

### Human-in-the-Loop (HITL)

When the agent identifies degraded or critical resources:
1. Agent calls `check_resource_health()` to get structured verdict
2. Agent analyzes findings and formulates recommendation
3. Agent calls `request_human_review()` with:
   - `issue_summary` - One-sentence description
   - `urgency` - critical/high/medium/low
   - `full_context` - All findings and tool outputs
   - `recommended_action` - Specific steps for human to execute
4. Tool returns ticket ID and logs to console (future: SNS/Slack integration)

### Model Swapping

To swap between Anthropic and Hugging Face models:

```python
# In agent.py create_agent():
if hf_endpoint_arn:
    model = get_hf_bedrock_model(endpoint_arn=hf_endpoint_arn, region=aws_region)
else:
    model = get_bedrock_model(region=aws_region)

# ALL other components unchanged:
# - System prompt (SYSTEM_PROMPT)
# - Tools (ALL_TOOLS)
# - Conversation manager (SlidingWindowConversationManager)
# - Callback handler (LoopObserver)
```

Only the model provider changes. Tools, prompts, and orchestration remain identical.

## Code Organization

```
module1/
├── agent.py              # Core agent factory (create_agent)
│                        # - Assembles three layers
│                        # - SYSTEM_PROMPT definition
│                        # - LoopObserver callback handler
│
├── app.py               # AgentCore Runtime entrypoint
│                        # - BedrockAgentCoreApp wrapper
│                        # - HTTP server (POST /invocations, GET /ping)
│                        # - Fallback server if AgentCore not installed
│
├── config/
│   └── models.py        # Model provider configuration
│                        # - get_bedrock_model() (Anthropic)
│                        # - get_hf_bedrock_model() (Hugging Face)
│                        # - Model constants and provider info
│
└── tools/
    └── aws_tools.py     # 5 tools + mock data
                         # - All tools return JSON with consistent envelope
                         # - Mock mode triggered by AGENT_MOCK_AWS=true
                         # - Live mode uses boto3 clients
```

## Important Implementation Notes

### Tool Output Format

All tools return JSON with consistent structure:
```json
{
  "tool": "tool_name",
  "timestamp": "2025-02-20T14:05:00Z",
  "region": "us-east-1",
  "mock_mode": false,
  "data": { /* tool-specific payload */ }
}
```

This helps the agent parse and cite results accurately.

### Context Window Management

`SlidingWindowConversationManager(window_size=10)`:
- Keeps last 10 conversation turns in context
- After turn 11, turn 1 is dropped (sliding window)
- This is "short-term memory" - long-term memory comes in Module 7
- For multi-turn conversations, increase window_size if needed

### System Prompt Structure

The system prompt (`SYSTEM_PROMPT` in `agent.py`) defines:
1. **Role** - AWS Infrastructure Agent in OBSERVE AND ANALYSE mode
2. **Capabilities** - 5 operations (observe, analyze, reason, recommend, escalate)
3. **Hard Constraints** - No write operations, all changes go through HITL
4. **Tool Usage Guidance** - When to use each tool
5. **Response Format** - Summary / Findings / Recommendations structure

When modifying the system prompt:
- Keep constraints explicit and specific (not vague)
- Provide examples of good vs. bad behavior
- Define severity language (critical/degraded/healthy)
- Emphasize grounding (always call tools, never guess)

## Extending the Agent

### Adding a New AWS Service

To add support for a new service (e.g., S3, DynamoDB):

1. **Add mock data** in `tools/aws_tools.py`:
   ```python
   _MOCK_S3 = {
       "us-east-1": [
           {"bucket": "prod-data", "region": "us-east-1", "versioning": True, ...},
       ],
   }
   ```

2. **Add live AWS function**:
   ```python
   def _live_list_s3(region: str) -> str:
       s3 = _client("s3", region)
       buckets = s3.list_buckets()["Buckets"]
       resources = [{"bucket": b["Name"], ...} for b in buckets]
       return _wrap({"service_type": "s3", ...}, "list_aws_resources")
   ```

3. **Update tool logic** in `list_aws_resources()`:
   ```python
   if svc == "s3":
       return _live_list_s3(region)
   ```

4. **Update mock_map** to include the new service

5. **Add corresponding describe/health logic** if needed

6. **Update system prompt** to mention the new service

### Modifying the Loop Observer

The `LoopObserver` class intercepts Strands lifecycle events. To customize:

```python
def __call__(self, **event: Any) -> None:
    event_type = event.get("event_type", "").lower()
    
    # Add custom logging for specific events
    if "tool_use_end" in event_type:
        tool_name = event.get("tool_name")
        # Log to CloudWatch, write to file, etc.
```

For production, replace console prints with structured logging (CloudWatch Logs, X-Ray).

## Common Issues

### Missing AWS Credentials
```
RuntimeError: AWS credentials not found.
```
**Fix:** Run `aws configure` OR set `AGENT_MOCK_AWS=true` for demo mode

### Bedrock Model Access Denied
```
botocore.exceptions.ClientError: ... access denied ...
```
**Fix:** AWS Console → Amazon Bedrock → Model Access → Enable Anthropic models

### Context Window Exceeded
If the agent fails with context errors on long multi-turn conversations:
```python
# In create_agent():
conversation_manager = SlidingWindowConversationManager(window_size=20)  # Increase
```

### Agent Not Using Tools
If agent responds without calling tools, check:
1. System prompt emphasizes "always call a tool" for infrastructure queries
2. Tools are registered in `ALL_TOOLS` list
3. Tool signatures have clear docstrings (Strands uses them for tool selection)
