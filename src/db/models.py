import datetime
import uuid

from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Integer, String, Boolean, UUID

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID, primary_key=True, index=True, unique=True, default=uuid.uuid4)
    username = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    role = Column(String, nullable=False, default="user")


class Ecg(Base):
    __tablename__ = 'ecg'

    id = Column(UUID, primary_key=True, index=True, nullable=False, unique=True, default=uuid.uuid4)
    date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    user_id = Column(UUID, ForeignKey('users.id'), nullable=False)
    analysed = Column(Boolean, nullable=False, default=False)

    user = relationship(User)


class EcgLead(Base):
    __tablename__ = 'ecg_lead'

    id = Column(UUID, primary_key=True, index=True, nullable=False, unique=True, default=uuid.uuid4)
    ecg_id = Column(UUID, ForeignKey('ecg.id'), index=True)
    name = Column(String, index=True, nullable=False)
    number_of_samples = Column(Integer, index=True, nullable=True)
    signal = Column(ARRAY(Integer), default=[])

    ecg = relationship(Ecg)


class EcgAnalysis(Base):
    __tablename__ = 'ecg_analysis'

    id = Column(UUID, primary_key=True, index=True, nullable=False, unique=True, default=uuid.uuid4)
    ecg_id = Column(UUID, ForeignKey('ecg.id'))
    zero_crosses_count = Column(Integer, default=0)

    ecg = relationship(Ecg)
