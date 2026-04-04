from google.adk.agents import Agent
from google.adk.tools import FunctionTool
import psycopg2
import os

MODEL = "gemini-2.5-pro"

# ---------------- MCP TOOL FUNCTIONS ----------------

def read_emails() -> str:
    """Fetch latest emails (mock or integrate Gmail API later)."""
    return "Emails: Meeting invite, Invoice received, Follow-up required"


def schedule_event(title: str, time: str) -> str:
    """Schedule a calendar event."""
    return f"Scheduled event '{title}' at {time}"


def add_expense(amount: float, category: str) -> str:
    """Store expense in AlloyDB/Postgres."""
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME", "postgres"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "password"),
            host=os.getenv("DB_HOST", "localhost"),  # Replace with AlloyDB connector later
            port=os.getenv("DB_PORT", "5432"),
        )

        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id SERIAL PRIMARY KEY,
                amount FLOAT,
                category TEXT
            );
        """)

        cur.execute(
            "INSERT INTO expenses (amount, category) VALUES (%s, %s)",
            (amount, category),
        )

        conn.commit()
        cur.close()
        conn.close()

        return f"Stored expense ₹{amount} under '{category}'"

    except Exception as e:
        return f"Failed to store expense: {str(e)}"


# ---------------- TOOLS ----------------

email_tool = FunctionTool(read_emails)
calendar_tool = FunctionTool(schedule_event)
expense_tool = FunctionTool(add_expense)

# ---------------- AGENT ----------------

operator = Agent(
    name="operator",
    model=MODEL,
    description="Executes real-world actions using MCP tools like calendar, email, and expense tracking.",
    instruction="""
You are the Operator Agent (Execution Engine).

You execute real-world actions using connected tools.

AVAILABLE ACTIONS:
- Read emails
- Schedule calendar events
- Track expenses

RULES:
- Only perform actions when explicitly requested
- Always use tools (no guessing)
- Return structured, clear output
- Do NOT hallucinate actions

OUTPUT FORMAT:
- Action: <what was done>
- Status: Success/Failure
- Result: <tool output>
""",
    tools=[email_tool, calendar_tool, expense_tool],
)

root_agent = operator