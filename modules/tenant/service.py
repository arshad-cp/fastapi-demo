from fastapi import Depends
from sqlalchemy.orm import Session

import models
from database import database


class TenantService:
    def __init__(self, db: Session = Depends(database.get_db_default)):
        self.db = db

    def get_all(self):

        user = self.db.query(models.Tenant).all()
        return user
