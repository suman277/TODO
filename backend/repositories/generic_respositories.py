from typing import TypeVar, Generic, Type, Optional, Dict, Any
from sqlmodel import SQLModel, Session, select
from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
T = TypeVar("T", bound=SQLModel)

class CommonRepository(Generic[T]):
    def __init__(self, model : Type[T]):
        self.model = model
    
    def create(self, session: Session, instance: T) -> T:
        try:
            session.add(instance)
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
    
    def update(self, session:Session, instance:T, filters:Optional[dict]= None)->Optional[T]:
        try:
            if filters is not None:
                existing_instance = self.get_by_column(session, filters)
            else:
                existing_instance = self.get_by_id(session, instance.id)
            
            if not existing_instance:
                return None
            
            instance_dump = instance.model_dump(exclude_unset= True)

            for key, value in instance_dump.items():
                if hasattr(existing_instance, key):
                    setattr(existing_instance, key, value)
            
            merged_instance = session.merge(existing_instance)

            return merged_instance
        
        except Exception as e:
            raise HTTPException(
                status_code = HTTP_500_INTERNAL_SERVER_ERROR,
                detail = "An internal error occured"
            )
        

        