import bcrypt

def genearte_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def fix_audit_log(audit_logs : list) -> list:
    audits = []
    activity_in_inserts = []
    activity_in_udpate = []
    activity_in_delete = []
    audit_init ={
        "id" : "",
        "changes_json": "",
        "user_id" : "",
        "display_name": ""
    }

    for log in audit_logs:
        if log.operation == "CREATE":
            activity_in_inserts.append(log)
        if log.operation == "UPDATE":
            activity_in_udpate.append(log)
        if log.operation == "DELETE":
            activity_in_delete.append(log)
    

    for log in activity_in_inserts:
        changes_log = log.changes_json
        is_completed = changes_log.get("is_completed")
        completed = "Completed" if is_completed else "Incompleted"
        audit_init = {
        "id": log.record,
        "display_name": log.display_name,
        "user_id": log.user_id,
        "changes_json": (
            f'{log.display_name} have created a todo '
            f'with name as {changes_log.get("todo")} '
            f'with description {changes_log.get("description")} '
            f'and marked as {completed}'
        )
    }
        
        audits.append(audit_init)
    
    return audits