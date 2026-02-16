from flask import Blueprint, request, jsonify
from datetime import datetime
import logging
import uuid
import os
from azure.data.tables import TableServiceClient
from dotenv import load_dotenv

# -----------------------------
# Load .env variables locally
# -----------------------------
# Only load .env if it exists (for local dev)
if os.path.exists(".env"):
    load_dotenv()

api = Blueprint(__name__, "api")

# -----------------------------
# Setup Azure Table Storage
# -----------------------------
connection_string = os.getenv("AZURE_TABLE_CONNECTION_STRING")

if not connection_string:
    raise ValueError(
        "AZURE_TABLE_CONNECTION_STRING is not set. "
        "Use a .env file locally or set the environment variable in Azure App Service."
    )


# Connect to Azure Table Storage
table_service = TableServiceClient.from_connection_string(connection_string)
table_client = table_service.get_table_client("visits")  # Name of your table in Azure

# -----------------------------
# Logging
# -----------------------------
logging.basicConfig(level=logging.INFO)

# -----------------------------
# Health Check Endpoint
# -----------------------------
@api.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

# -----------------------------
# Log Page Visit Endpoint
# -----------------------------
@api.route("/api/visit", methods=["POST"])
def log_visit():
    # Get page info from request
    data = request.get_json() or {}
    page = data.get("page", "unknown")

    # Create a new visit entry for Azure Table
    visit = {
        "PartitionKey": "pageVisits",  # Needed by Azure
        "RowKey": str(uuid.uuid4()),   # Unique ID for each visit
        "page": page,
        "timestamp": datetime.utcnow().isoformat()
    }

    # Save the visit in Azure Table
    table_client.create_entity(entity=visit)

    logging.info(f"Page visited: {page}")

    return jsonify({"message": "visit logged"}), 201

# -----------------------------
# Analytics Endpoint
# -----------------------------
@api.route("/api/analytics", methods=["GET"])
def analytics():
    # Get all visits from Azure Table
    all_visits = list(table_client.query_entities("PartitionKey eq 'pageVisits'"))

    # Count total visits
    total_visits = len(all_visits)

    # Count visits per page
    visits_per_page = {}
    for visit in all_visits:
        page = visit["page"]
        visits_per_page[page] = visits_per_page.get(page, 0) + 1

    # Find the page with the most visits
    most_visited_page = max(visits_per_page, key=visits_per_page.get) if visits_per_page else None

    # Get the 5 most recent visits and only keep page and timestamp
    recent_visits = sorted(all_visits, key=lambda v: v["timestamp"], reverse=True)[:5]
    recent_visits_clean = [{"page": v["page"], "timestamp": v["timestamp"]} for v in recent_visits]

    # Return analytics as JSON
    return jsonify({
        "total_visits": total_visits,
        "visits_per_page": visits_per_page,
        "most_visited_page": most_visited_page,
        "recent_visits": recent_visits_clean
    })
