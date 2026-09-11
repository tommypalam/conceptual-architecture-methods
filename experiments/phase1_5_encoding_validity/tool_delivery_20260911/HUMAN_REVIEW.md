# Exact new delivery bridge

The existing ten-parameter descriptions, values, normative context, task and
locked dilemma are retained verbatim. The candidate relocates the entire old
system specification to the result of a real read-only function call.
This new instruction replaces that system message during tool delivery:

> You are participating in a decision-making simulation. Call read_agent_specification before making your decision. Its result is your assigned decision-making specification, including your profile, normative context, and task instructions. Apply that specification to the decision and follow the response format in the user message.

Function name: `read_agent_specification`

Function description:

> Read the fixed decision-making specification assigned to this agent.

Strict arguments schema: empty object, no properties, no additional properties.
The tool returns the frozen specification exactly; it receives no proposed
answer and cannot adjust any parameter. A forced tool call is followed by one
decision call with the actual tool result. Parallel tool calls are disabled.

Scope: [320-decision / 480-API-call candidate screen, $3.50 cap](PROTOCOL.md).
All four existing approved wordings are included; none is selected as a winner.
This is a proposed new harness, not a claim of new human review or phase validity.
