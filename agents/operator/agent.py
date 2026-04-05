import os
from google.adk.agents import Agent
from google.adk.tools.mcp import MCPToolset
from google.adk.tools.mcp.connection import StdioConnectionParams

MODEL = "gemini-2.5-flash"

# ---------------- REAL MCP CONNECTIONS (Stdio) ----------------

# 🗄️ AlloyDB MCP (Postgres-compatible)
# Uses the official postgres MCP server to talk to AlloyDB
alloydb_conn = StdioConnectionParams(
    command="npx",
    args=[
        "-y", "@modelcontextprotocol/server-postgres", 
        os.getenv("ALLOYDB_CONNECTION_STRING") # e.g., postgresql://user:pass@host:5432/db
    ]
)

# 📧 & 📅 Google Workspace (Gmail + Calendar)
# The official Google Workspace server handles both in one process
workspace_conn = StdioConnectionParams(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-google-workspace"]
    # Requires GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, and GOOGLE_REFRESH_TOKEN env vars
)

# 🗺️ Maps MCP
maps_conn = StdioConnectionParams(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-google-maps"],
    env={**os.environ, "GOOGLE_MAPS_API_KEY": os.getenv("MAPS_API_KEY")}
)

# ---------------- TOOLSETS ----------------

# We initialize toolsets using the live stdio connections
alloydb_tools = MCPToolset(connection_params=alloydb_conn)
workspace_tools = MCPToolset(connection_params=workspace_conn)
maps_tools = MCPToolset(connection_params=maps_conn)

# ---------------- AGENT ----------------

operator = Agent(
    name="operator",
    model=MODEL,
    description="Execution layer for database, workspace, and location services.",
    instruction="""
    You are the Operator Agent. You communicate with real services via MCP.
    
    - To query data or store expenses: Use postgres (AlloyDB) tools.
    - To read/send mail or check events: Use Google Workspace tools.
    - To find places or navigate: Use Google Maps tools.
    
    Always verify tool output before confirming completion to the user.
    """,
    tools=[
        *alloydb_tools.tools,
        *workspace_tools.tools,
        *maps_tools.tools,
    ],
)

root_agent = operator