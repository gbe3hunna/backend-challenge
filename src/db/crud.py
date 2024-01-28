from typing import Type
from uuid import UUID

from sqlalchemy import exc
from sqlalchemy.orm import Session

from src.db import models
from src.db.database import get_db
from src.schemas import ECGSubmission, ECGUserCreate


# ECG transactions (ECGRepo)
def ecg_create(ecg: ECGSubmission,
               user_id: UUID,
               db: Session = get_db()) -> None:
    ecg_model = models.Ecg(id=ecg.id,
                           date=ecg.date,
                           user_id=str(user_id))

    ecg_leads_model = [models.EcgLead(ecg_id=ecg.id,
                                      name=lead.name,
                                      number_of_samples=lead.number_of_samples,
                                      signal=lead.signal)
                       for lead in ecg.leads]

    with db as db_session:
        db_session.add(ecg_model)
        db_session.commit()
        db_session.refresh(ecg_model)
        db_session.add_all(ecg_leads_model)
        db_session.commit()


def ecg_update_analysed_by_id(ecg_id: UUID,
                              db: Session = get_db()) -> None:
    with db as db_session:
        try:
            db_session.query(models.Ecg).filter(models.Ecg.id == ecg_id).update({'analysed': True})
            db_session.commit()
        except exc.SQLAlchemyError:
            return None


def ecg_get_by_id_and_user_id(id_: UUID,
                              user_id: UUID,
                              db: Session = get_db()) -> Type[models.Ecg] | None:
    with db as db_session:
        try:
            return db_session.query(models.Ecg).where(models.Ecg.id == id_).where(models.Ecg.user_id == user_id).one()
        except exc.SQLAlchemyError:
            return None


# ECG Analysis transactions (ECGAnalysisRepo)

def ecg_create_analysis(ecg_id: UUID,
                        zero_crosses_count: int,
                        db: Session = get_db()) -> None:
    ecg_analysis = models.EcgAnalysis(ecg_id=ecg_id,
                                      zero_crosses_count=zero_crosses_count)
    with db as db_session:
        db_session.add(ecg_analysis)
        db_session.commit()


def ecg_get_analysis_by_id(id_: UUID,
                           db: Session = get_db()) -> Type[models.EcgAnalysis] | None:
    with db as db_session:
        try:
            return db_session.query(models.EcgAnalysis).where(models.EcgAnalysis.ecg_id == id_).one()
        except exc.NoResultFound:
            return None


# User transactions (UserRepo)
def user_create(user: ECGUserCreate,
                db: Session = get_db()) -> models.User | None:
    user = models.User(id=user.id,
                       username=user.username,
                       password=user.hashed_password)

    with db as db_session:
        try:
            db_session.add(user)
            db_session.commit()
            db_session.refresh(user)
            return user
        except exc.IntegrityError:
            return None


def user_get_by_username(username: str,
                         db: Session = get_db()) -> Type[models.User] | None:
    with db as db_session:
        try:
            return db_session.query(models.User).where(models.User.username == username).one()
        except exc.NoResultFound:
            return None
