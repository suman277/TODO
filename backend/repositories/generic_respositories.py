from typing import TypeVar, Generic, Type, Optional, Dict, Any
from sqlmodel import SQLModel, Session, select
from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from sqlalchemy import asc, desc, or_
from sqlalchemy.sql.expression import nullslast
from models.hoc_models import HistoryOfChanges

from enums.enums import OrderByEnum
T = TypeVar("T", bound=SQLModel)

class CommonRepository(Generic[T]):
    def __init__(self, model : Type[T]):
        self.model = model
    
    def create(self, session: Session, instance: T) -> T:
        try:
            session.add(instance)
            session.flush()
            changes = {
            column.name: getattr(instance, column.name)
            for column in instance.__table__.columns
            }
            if instance.__tablename__ == "history_of_changes":
                session.add(instance)
                session.flush()
                return instance
            user_id, display_name = session.info["user_metadata"]

            history_payload = {
                "record": instance.id,
                "table_name": instance.__tablename__,
                "changes_json": changes,   
                "operation": "CREATE",
                "user_id": user_id,
                "display_name": display_name,
            }

            from repositories.hoc_repository import HistoryOfChangesRepo
            HistoryOfChangesRepo.create(
                session,
                HistoryOfChanges(**history_payload)
            )

            return instance
        except Exception as e:
            raise HTTPException(status_code = HTTP_500_INTERNAL_SERVER_ERROR,
            detail= "An internal Error Occured")
    
    def get_by_id(self, session: Session, id:int) -> Optional[T]:
        try:
            statement = select(self.model).where(self.model.id==id)
            result = session.exec(statement).first()
            return result
        except Exception as e:
            raise HTTPException(status_code = HTTP_500_INTERNAL_SERVER_ERROR, detail = "An internal Error Occured")
    
    def get_by_column(self, session: Session,filters: Optional[Dict[str, Any]] = None) -> Optional[T]:
        stmt = select(self.model)

        if filters:
            for column_name, value in filters.items():
                column = getattr(self.model, column_name)
                stmt = stmt.where(column == value)

        return session.exec(stmt).first()
    
    def delete(self, session, instance : T) -> Optional[T]:
        from repositories.hoc_repository import HistoryOfChangesRepo
        try:
            user_id, display_name= session.info["user_metadata"]
            history_payload = {
            "record": instance.id,
            "table_name": instance.__tablename__,
            "changes_json": {
                "todo": instance.todo,
                "description": instance.description,
                "is_completed": instance.is_completed,
                "user_id": instance.user_id,
            },
            "operation" : "DELETE",
            "user_id" : user_id,
            "display_name" : display_name
        }
            print(session.__dict__)
            session.delete(instance)
            print(session.__dict__)
            HistoryOfChangesRepo.create(session, 
                                        HistoryOfChanges(
                                            **history_payload
                                        ))
        except Exception as e:
            raise HTTPException(status_code = HTTP_500_INTERNAL_SERVER_ERROR, detail = "An internal Error Occured")
    
    # def update(self, session:Session, instance:T, filters:Optional[dict]= None)->Optional[T]:
    #     try:
    #         after ={}
    #         user_id, display_name= session.info["user_metadata"]
    #         history_payload = {
    #         "record": instance.id,
    #         "table_name": instance.__tablename__,
    #         "changes_json": {
    #             "before" :{
    #             "todo": instance.todo,
    #             "description": instance.description,
    #             "is_completed": instance.is_completed,
    #             "user_id": instance.user_id,
    #             }
    #         },
    #         "operation" : "UPDATE",
    #         "user_id" : user_id,
    #         "display_name" : display_name
    #     }
    #         if filters is not None:
    #             existing_instance = self.get_by_column(session, filters)
    #         else:
    #             existing_instance = self.get_by_id(session, instance.id)
            
    #         if not existing_instance:
    #             return None
            
    #         instance_dump = instance.model_dump(exclude_unset= True)
    #         print(session.__dict__)
    #         for key, value in instance_dump.items():
    #             if hasattr(existing_instance, key):
    #                 setattr(existing_instance, key, value)
    #             after ={}

    #         merged_instance = session.merge(existing_instance)
    #         print(session.__dict__)
    #         return merged_instance
        
    #     except Exception as e:
    #         raise HTTPException(
    #             status_code = HTTP_500_INTERNAL_SERVER_ERROR,
    #             detail = "An internal error occured"
    #         )


    def update(
    self,
    session: Session,
    instance: T,
    filters: Optional[dict] = None
) -> Optional[T]:
        try:
            user_id, display_name = session.info["user_metadata"]

            # 1. Fetch existing DB row
            if filters is not None:
                existing_instance = self.get_by_column(session, filters)
            else:
                existing_instance = self.get_by_id(session, instance.id)

            if not existing_instance:
                return None

            # 2. Capture BEFORE state (from DB, not input)
            before = {
                "todo": existing_instance.todo,
                "description": existing_instance.description,
                "is_completed": existing_instance.is_completed,
                "user_id": existing_instance.user_id,
            }

            # 3. Apply updates
            instance_dump = instance.model_dump(exclude_unset=True)
            for key, value in instance_dump.items():
                if hasattr(existing_instance, key):
                    setattr(existing_instance, key, value)

            # 4. Capture AFTER state
            after = {
                "todo": existing_instance.todo,
                "description": existing_instance.description,
                "is_completed": existing_instance.is_completed,
                "user_id": existing_instance.user_id,
            }

            # 5. Build changes ONLY if something changed
            changes = {}
            changes["todo"] = existing_instance.todo
            for key in before:
                if before[key] != after[key]:
                    changes[key] = {
                        "before": before[key],
                        "after": after[key],
                        "name": existing_instance.todo
                    }

            if not changes:
                return existing_instance  # nothing changed

            history_payload = {
                "record": existing_instance.id,
                "table_name": existing_instance.__tablename__,
                "changes_json": changes,
                "operation": "UPDATE",
                "user_id": user_id,
                "display_name": display_name,
            }

            # 6. Persist audit entry
            from repositories.hoc_repository import HistoryOfChangesRepo
            HistoryOfChangesRepo.create(
                session,
                HistoryOfChanges(**history_payload)
            )

            return existing_instance

        except Exception:
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An internal Error Occured"
            )
    
    def get_all_by_columns(self, session: Session, filters: Optional[Dict[str, Any]] = None, order_by: Optional[Dict[str, OrderByEnum]] = None,) -> list[T]:
        stmt = select(self.model)

        if filters:
            for name, value in filters.items():
                if name == "ILIKE":
                    ilike_conditions = []
                    for key, value in value.items():
                        column_name = getattr(self.model, key)
                        if column_name:
                            ilike_conditions.append(
                                column_name.ilike(f"%{value}%")
                            )
                    if ilike_conditions:
                        stmt = stmt.where(or_(*ilike_conditions))
                else :
                    column = getattr(self.model, name)
                    stmt = stmt.where(column == value)
        
        if order_by is not None:
                for column, direction in order_by.items():
                    if direction == OrderByEnum.ASCENDING:
                        stmt = stmt.order_by(
                            nullslast(asc(getattr(self.model, column)))
                        )
                    elif direction == OrderByEnum.DESCENDING:
                        stmt = stmt.order_by(
                            nullslast(desc(getattr(self.model, column)))
                        )

        results = session.exec(stmt).all()

        return results
        

        