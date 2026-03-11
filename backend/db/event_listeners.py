from sqlalchemy import event, inspect
from sqlalchemy.orm import Session
from models.hoc_models import HistoryOfChanges

@event.listens_for(Session, "before_flush")
def audit_all_operations(session, flush_context, instances):
    user_meta = session.info.get("user_metadata")
    if not user_meta:
        return

    user_id, display_name = user_meta

    # ───────────────── CREATE ─────────────────
    for obj in session.new:
        if not hasattr(obj, "__tablename__"):
            continue

        data = {
            col.name: getattr(obj, col.name)
            for col in obj.__table__.columns
        }

        session.add(
            HistoryOfChanges(
                table_name=obj.__tablename__,
                record_id=None,   # ID may not exist yet
                operation="CREATE",
                changes_json={"new": data},
                user_id=user_id,
                display_name=display_name,
            )
        )

    # ───────────────── UPDATE ─────────────────
    for obj in session.dirty:
        if not hasattr(obj, "__tablename__"):
            continue

        state = inspect(obj)

        changes = {}
        for attr in state.attrs:
            hist = attr.history
            if hist.has_changes():
                changes[attr.key] = {
                    "old": hist.deleted[0] if hist.deleted else None,
                    "new": hist.added[0] if hist.added else None,
                }

        if not changes:
            continue

        session.add(
            HistoryOfChanges(
                table_name=obj.__tablename__,
                record_id=obj.id,
                operation="UPDATE",
                changes_json=changes,
                user_id=user_id,
                display_name=display_name,
            )
        )

    # ───────────────── DELETE ─────────────────
    for obj in session.deleted:
        if not hasattr(obj, "__tablename__"):
            continue

        data = {
            col.name: getattr(obj, col.name)
            for col in obj.__table__.columns
        }

        session.add(
            HistoryOfChanges(
                table_name=obj.__tablename__,
                record_id=obj.id,
                operation="DELETE",
                changes_json={"old": data},
                user_id=user_id,
                display_name=display_name,
            )
        )
