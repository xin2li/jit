from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import exc


SQLALCHEMY_DATABASE_URL = "sqlite:///./dmvtest.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

Base = declarative_base()




class JITerror(Base):
    __tablename__ = "JIT_ERROR"
    id = Column(Integer, primary_key=True, autoincrement=True)
    error_statusN = Column(Boolean)
    error_status0 = Column(Integer)
    error_plant = Column(String(2))
    error_tma = Column(String(3))
    error_ta = Column(String(4))
    error_fehler = Column(String(3))
    error_anzahl = Column(Integer)
    error_referenzen = Column(Integer)
    error_pn = Column(String(18))
    error_bemerkung = Column(Text)
    error_type = Column(String(8))
    error_statusF = Column(Boolean)
    error_inlist = Column(DateTime)
    error_timestamp = Column(DateTime)




class FX0810o(Base):
    __tablename__ = "FX_0810O"
    # __mapper_args__ = {
    #     "primary_key": ["fx_tma", "fx_ta", "fx_timestamp"]
    # }
    fx_status = Column(Boolean)

    fx_tma = Column(String(3),primary_key=True)
    fx_ta = Column(String(4),primary_key=True)
    fx_remark= Column(String(40))
    fx_fistag = Column(String(4))

    fx_testmode = Column(String(1))

    fx_partkind = Column(Integer)
    fx_min  = Column(Integer)
    fx_max = Column(Integer)
    fx_timestamp = Column(DateTime,primary_key=True)


class FX0810u(Base):
    __tablename__ = "FX_0810U"
    id = Column(Integer, primary_key=True, autoincrement=True)
    fx_status = Column(Boolean)

    fx_tma = Column(String(3),ForeignKey("FX_0810O.fx_tma"))
    fx_ta = Column(String(4),ForeignKey("FX_0810O.fx_ta"))
    fx_my = Column(Integer)

    fx_vaild = Column(String(8))
    fx_invalid = Column(String(8))
    fx_pr = Column(String(81))

    fx_timestamp = Column(DateTime,ForeignKey("FX_0810O.fx_timestamp"))

class FX0812(Base):
    __tablename__ = "FX_0812"
    id = Column(Integer, primary_key=True, autoincrement=True)
    fx_status = Column(Boolean)

    fx_tma = Column(String(3),ForeignKey("FX_0810O.fx_tma"))
    fx_ta = Column(String(4),ForeignKey("FX_0810O.fx_ta"))
    fx_pn = Column(String(18))

    fx_timestamp = Column(DateTime,ForeignKey("FX_0810O.fx_timestamp"))

class FXlog(Base):
    __tablename__ = "FX_LOG"
    id = Column(Integer, primary_key=True, autoincrement=True)
    fx_log0 = Column(Boolean)
    fx_logtag = Column(String(3))
    fx_logstr = Column(Text)
    fx_log08xx = Column(String(11))
    fx_logtimestamp = Column(DateTime)



Base.metadata.create_all(bind=engine)