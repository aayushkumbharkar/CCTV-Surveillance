import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from uuid import uuid4
from app.db import get_db_connection

def create_camera(camera):
    conn = get_db_connection()
    cur = conn.cursor()

    camera_id = str(uuid4())

    cur.execute("""
        INSERT INTO cameras (
            camera_id,
            site_id,
            name,
            location,
            status,
            created_at
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        camera_id,
        camera.site_id,
        camera.name,
        camera.location,
        "offline",
        datetime.utcnow()
    ))

    conn.commit()
    cur.close()
    conn.close()

    return camera_id

def heartbeat(camera_id: str):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE cameras
        SET status = 'online',
            last_heartbeat = %s
        WHERE camera_id = %s
    """, (datetime.utcnow(), camera_id))

    conn.commit()
    cur.close()
    conn.close()

def list_cameras():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM cameras")
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows
