import psycopg2
from psycopg2.extras import Json, RealDictCursor
from app.schemas.event import Event
from typing import Optional

# -------------------------
# Database configuration
# -------------------------
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "cctv_db",
    "user": "cctv_user",
    "password": "cctv_password"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# -------------------------
# WRITE: Save Event
# -------------------------
def save_event(event: Event):
    """
    Stores a validated event into the database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO events (
            event_id,
            event_type,
            timestamp,
            source,
            site_id,
            camera_id,
            severity,
            confidence,
            status,
            snapshot_url,
            clip_url,
            metadata
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (
            str(event.event_id),              # UUID → string
            event.event_type,
            event.timestamp,
            event.source,
            event.site_id,
            event.camera_id,
            event.severity,
            event.confidence,
            event.status,
            event.evidence.snapshot_url if event.evidence else None,
            event.evidence.clip_url if event.evidence else None,
            Json(event.metadata) if event.metadata else None
        )
    )

    conn.commit()
    cursor.close()
    conn.close()

    return event.event_id

# -------------------------
# READ: Fetch Events (Pagination + Filters)
# -------------------------
def fetch_events(
    limit: int = 50,
    offset: int = 0,
    site_id: Optional[str] = None,
    camera_id: Optional[str] = None,
    event_type: Optional[str] = None,
    severity: Optional[str] = None,
    source: Optional[str] = None,
    from_timestamp: Optional[str] = None,
    to_timestamp: Optional[str] = None
):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    base_query = """
        SELECT
            event_id,
            event_type,
            timestamp,
            source,
            site_id,
            camera_id,
            severity,
            confidence,
            status,
            snapshot_url,
            clip_url,
            metadata
        FROM events
        WHERE 1=1
    """

    params = []

    if site_id:
        base_query += " AND site_id = %s"
        params.append(site_id)

    if camera_id:
        base_query += " AND camera_id = %s"
        params.append(camera_id)

    if event_type:
        base_query += " AND event_type = %s"
        params.append(event_type)

    if severity:
        base_query += " AND severity = %s"
        params.append(severity)

    if source:
        base_query += " AND source = %s"
        params.append(source)

    if from_timestamp:
        base_query += " AND timestamp >= %s"
        params.append(from_timestamp)

    if to_timestamp:
        base_query += " AND timestamp <= %s"
        params.append(to_timestamp)

    base_query += """
        ORDER BY timestamp DESC
        LIMIT %s OFFSET %s
    """

    params.extend([limit, offset])

    cursor.execute(base_query, tuple(params))
    events = cursor.fetchall()

    cursor.close()
    conn.close()

    return events