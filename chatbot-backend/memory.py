import redis
import json

r = redis.Redis(host="redis", port=6379, decode_responses=True)

def get_history(session_id):
    data = r.get(session_id)
    return json.loads(data) if data else []

def save_history(session_id, messages):
    r.set(session_id, json.dumps(messages), ex=3600)