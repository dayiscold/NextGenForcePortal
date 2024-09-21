from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, relationship

SQLALCHEMY_DATABASE_URL = "sqlite:///./site_info.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    updated_at = Column(DateTime, nullable=True)
    id = Column(Integer, primary_key=True, index=True,  autoincrement=True)


class SpecialityForStudent(Base):
    __tablename__ = "specialities"
    name_speciality = Column(String)


class Enterprise(Base):  # Предприятие
    __tablename__ = "enterprises"
    name_enterprise = Column(String)
    address_enterprise = Column(String)


class Requirements(Base):  # Условия трудоустройства
    __tablename__ = "requirements"
    company_id = Column(Integer, ForeignKey('enterprises.id'))
    price_work = Column(Integer, nullable=True)
    work_time = Column(Integer)
    employement_time = Column(Integer, nullable=True)

    company = relationship("Enterprise", back_populates="requirements")


Enterprise.requirements = relationship("Requirements", order_by=Requirements.id, back_populates="company")

Base.metadata.create_all(engine)
