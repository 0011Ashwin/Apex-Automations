import os
from typing import List, Dict, Any
from google.cloud import aiplatform
from googleapiclient.discovery import build
from google.cloud import discoveryengine_v1 as discoveryengine
import google.auth

def search_google(query: str) -> str:
    """Performs a Google Search using Vertex AI Grounding or a custom tool."""
    # In a real Vertex AI environment, this is often handled automatically by the model's 'google_search_retrieval' tool.
    # We will define the tool metadata for the model in agents.py.
    return f"SEARCH_TRIGGERED: {query}"

def get_calendar_events(time_min: str = None) -> List[Dict[str, Any]]:
    """Retrieves upcoming calendar events from Google Calendar."""
    try:
        # Note: In a production hackathon, you'd use OAuth2 credentials here.
        # For the prototype, we assume local default credentials.
        creds, project = google.auth.default(scopes=['https://www.googleapis.com/auth/calendar.readonly'])
        service = build('calendar', 'v3', credentials=creds)
        
        events_result = service.events().list(calendarId='primary', timeMin=time_min,
                                            maxResults=10, singleEvents=True,
                                            orderBy='startTime').execute()
        return events_result.get('items', [])
    except Exception as e:
        return [{"error": str(e)}]

def create_task(title: str, notes: str = "") -> Dict[str, Any]:
    """Creates a new task in Google Tasks."""
    try:
        creds, project = google.auth.default(scopes=['https://www.googleapis.com/auth/tasks'])
        service = build('tasks', 'v1', credentials=creds)
        
        task = {
            'title': title,
            'notes': notes
        }
        result = service.tasks().insert(tasklist='@default', body=task).execute()
        return result
    except Exception as e:
        return {"error": str(e)}

def query_vertex_search(query: str) -> str:
    """Performs a real-time search against a Vertex AI Search Data Store."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "global")
    data_store_id = os.getenv("DATA_STORE_ID")

    if not all([project_id, data_store_id]):
        return "Vertex AI Search not configured. Falling back to local knowledge base."

    try:
        client = discoveryengine.SearchServiceClient()
        # Full resource name of the serving config
        serving_config = f"projects/{project_id}/locations/{location}/collections/default_collection/engines/{data_store_id}/servingConfigs/default_search"

        request = discoveryengine.SearchRequest(
            serving_config=serving_config,
            query=query,
            page_size=3,
        )

        response = client.search(request)
        
        results = []
        for result in response.results:
            # Extract snippets or derived data
            data = result.document.derived_struct_data
            title = data.get("title", "Untitled")
            snippets = data.get("snippets", [])
            snippet_text = snippets[0].get("snippet") if snippets else "No snippet available."
            results.append(f"--- SOURCE: {title} ---\n{snippet_text}")

        if not results:
            return "No relevant information found in Vertex AI Search."
            
        return "\n\n".join(results)
    except Exception as e:
        return f"Vertex AI Search Error: {str(e)}"

def query_knowledge_base(query: str) -> str:
    """Orchestrates knowledge retrieval by trying Vertex Search then local fallbacks."""
    # Try Enterprise-grade Vertex Search first
    vertex_result = query_vertex_search(query)
    if "not configured" not in vertex_result and "Error" not in vertex_result:
        return f"--- CLOUD KNOWLEDGE BASE ---\n{vertex_result}"
    
    # Fallback to local files for the hackathon demo
    data_dir = os.path.join(os.getcwd(), "data")
    all_context = []
    
    try:
        if not os.path.exists(data_dir):
            return "No knowledge base directory found."
            
        for filename in os.listdir(data_dir):
            if filename.endswith(".txt"):
                with open(os.path.join(data_dir, filename), "r") as f:
                    content = f.read()
                    all_context.append(f"--- LOCAL SOURCE: {filename} ---\n{content}")
        
        if not all_context:
            return "Local knowledge base is empty."
            
        return "\n\n".join(all_context)
    except Exception as e:
        return f"Error reading local data: {str(e)}"
