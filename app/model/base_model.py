from app.db import SessionLocal, engine


class BaseModel:
    def get_conn(self):
        return SessionLocal() # pragma: no cover

    def get_raw_conn(self):
        return engine.raw_connection() # pragma: no cover
