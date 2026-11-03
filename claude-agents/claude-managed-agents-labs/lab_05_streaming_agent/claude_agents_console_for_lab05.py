#!/usr/bin/env python3
"""
Streaming console for Claude Managed Agents beta.
Creates an agent, session, and streams real-time events with live message printing.
"""

import anthropic


def format_cost(usage) -> str:
    """Calculate and format cost from usage data."""
    if not usage:
        return "$0.00"

    # Claude Haiku 4.5 pricing: $1/MTok input, $5/MTok output
    input_cost = (usage.input_tokens / 1_000_000) * 1.0
    output_cost = (usage.output_tokens / 1_000_000) * 5.0
    total_cost = input_cost + output_cost
    return f"${total_cost:.4f}"


def main():
    client = anthropic.Anthropic()

    print("=== Managed Agents Streaming Console ===\n")

    # 1. Create environment
    print("[ENV] Creating cloud environment...")
    environment = client.beta.environments.create(
        name="streaming-console-env",
        config={
            "type": "cloud",
            "networking": {"type": "unrestricted"},
        },
    )
    print(f"[ENV] Created: {environment.id}\n")

    # 2. Create agent
    print("[AGENT] Creating agent on claude-haiku-4-5-20251001...")
    agent = client.beta.agents.create(
        name="Streaming Console Agent",
        model="claude-haiku-4-5-20251001",
        system="You are a helpful assistant. Keep responses concise.",
        tools=[{"type": "agent_toolset_20260401", "default_config": {"enabled": True}}],
    )
    print(f"[AGENT] Created: {agent.id} (v{agent.version})\n")

    # 3. Create session
    print("[SESSION] Creating session...")
    session = client.beta.sessions.create(
        agent={"type": "agent", "id": agent.id, "version": agent.version},
        environment_id=environment.id,
    )
    print(f"[SESSION] {session.id} ({session.status})")
    print(f"[TRACE] https://platform.claude.com/workspaces/default/sessions/{session.id}\n")

    # 4. Stream events and send message
    print("[STREAM] Opening event stream and sending message...\n")
    print("-" * 60)

    with client.beta.sessions.events.stream(session_id=session.id) as stream:
        # Send a message while stream is live
        client.beta.sessions.events.send(
            session_id=session.id,
            events=[
                {
                    "type": "user.message",
                    "content": [{"type": "text", "text": "What can you help me with? List 3 capabilities."}],
                }
            ],
        )

        # Process events
        for event in stream:
            if event.type == "agent.message":
                # Print agent text live
                for block in event.content:
                    if block.type == "text":
                        print(block.text, end="", flush=True)

            elif event.type == "agent.tool_use":
                # Print tool calls
                print(f"\n[tool: {event.name}]", flush=True)

            elif event.type == "agent.custom_tool_use":
                # Print custom tool calls
                print(f"\n[tool: {event.name}]", flush=True)

            elif event.type == "session.status_idle":
                # Agent finished
                print("\n" + "-" * 60)
                print(f"\n[IDLE] Agent finished.")
                break

            elif event.type == "session.status_terminated":
                print("\n[TERMINATED] Session ended.")
                break

    # Fetch final session state for usage
    print("\n[FETCH] Retrieving session usage...")
    final_session = client.beta.sessions.retrieve(session_id=session.id)
    if final_session.usage:
        cost = format_cost(final_session.usage)
        print(
            f"[COST] Input: {final_session.usage.input_tokens} tokens | "
            f"Output: {final_session.usage.output_tokens} tokens | "
            f"Total: {cost}"
        )

    print("\n[DONE] Stream closed.\n")


if __name__ == "__main__":
    main()
