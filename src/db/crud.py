from typing import Type
from uuid import UUID

from sqlalchemy import exc
from sqlalchemy.orm import Session

from src.db import models
from src.db.database import get_db_celery
from src.schemas import ECGSubmission, ECGUserCreate


# ECG transactions (ECGRepo)
def ecg_create(ecg: ECGSubmission,
               user_id: UUID,
               db=get_db_celery) -> None:
    ecg_model = models.Ecg(id=ecg.id,
                           date=ecg.date,
                           user_id=user_id)

    ecg_leads_model = [models.EcgLead(ecg_id=ecg.id,
                                      name=lead.name,
                                      number_of_samples=lead.number_of_samples,
                                      signal=lead.signal)
                       for lead in ecg.leads]

    with db() as db_session:
        db_session.add(ecg_model)
        db_session.commit()
        db_session.refresh(ecg_model)
        db_session.add_all(ecg_leads_model)
        db_session.commit()


def ecg_update_analysed_by_id(ecg_id: UUID,
                              db=get_db_celery) -> None:
    with db() as db_session:
        try:
            db_session.query(models.Ecg).filter(models.Ecg.id == ecg_id).update({'analysed': True})
            db_session.commit()
        except exc.SQLAlchemyError:
            return None


def ecg_get_by_id_and_user_id(id_: UUID,
                              user_id: UUID,
                              db: Session) -> Type[models.Ecg] | None:
    try:
        return db.query(models.Ecg).where(models.Ecg.id == id_).where(models.Ecg.user_id == user_id).first()
    except exc.SQLAlchemyError:
        return None


# ECG Analysis transactions (ECGAnalysisRepo)

def ecg_create_analysis(ecg_id: UUID,
                        zero_crosses_count: int,
                        db=get_db_celery) -> None:
    ecg_analysis = models.EcgAnalysis(ecg_id=ecg_id,
                                      zero_crosses_count=zero_crosses_count)
    with db() as db_session:
        db_session.add(ecg_analysis)
        db_session.commit()


def ecg_get_analysis_by_id(id_: UUID,
                           db: Session) -> Type[models.EcgAnalysis] | None:
    try:
        return db.query(models.EcgAnalysis).where(models.EcgAnalysis.ecg_id == id_).first()
    except exc.NoResultFound:
        return None


# User transactions (UserRepo)
def user_create(user: ECGUserCreate,
                db: Session) -> models.User | None:
    user = models.User(id=user.id,
                       username=user.username,
                       password=user.hashed_password)

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except exc.IntegrityError:
        return None


def user_get_by_username(username: str,
                         db: Session) -> Type[models.User] | None:
    try:
        return db.query(models.User).where(models.User.username == username).first()
    except exc.NoResultFound:
        return None
