from pydantic import BaseModel
from typing import Optional


class JITupdateTime(BaseModel):
    error_updatetime: int
    fx_updatetime: int



class JITerrorCurrent(BaseModel):
    error_statusN :bool
    error_plant :str
    error_tma :str
    error_ta :str
    error_fehler :str
    error_anzahl :int
    error_lastanzahl :Optional[int] = None
    error_referenzen :int
    error_pn :Optional[str] = None
    error_bemerkung :Optional[str] = None
    error_type :Optional[str] = None
    error_inlist :int

class JITerrorFX0810uInfo(BaseModel):
    fx_my:Optional[int] = None
    fx_vaild :Optional[str] = None
    fx_invalid :Optional[str] = None
    fx_pr :Optional[str] = None



class JITerrorFX0812Info(BaseModel):
    fx_pn :str


class JITerrorFXInfo(BaseModel):
    fx_tma :str
    fx_ta :str
    fx_remark :Optional[str] = None
    fx_fistag :Optional[str] = None
    fx_testmode :Optional[str] = None
    fx_partkind :Optional[int] = None
    fx_min :Optional[int] = None
    fx_max :Optional[int] = None

    fx_0810u : Optional[list[JITerrorFX0810uInfo]] = None





class JITerrorAll(BaseModel):
    error_statusN :bool
    error_status0 :int
    error_plant :str
    error_tma :str
    error_ta :str
    error_fehler :str
    error_anzahl :int
    error_referenzen :int
    error_pn :Optional[str] = None
    error_bemerkung :Optional[str] = None
    error_type :Optional[str] = None
    error_statusF :Optional[bool] = None
    error_inlist :int
    error_timestamp :int

class JITerrorUpdate(BaseModel):

    error_tma: str
    error_ta: str
    error_fehler: str

    error_pn: Optional[str] = None
    error_bemerkung: Optional[str] = None
    error_type: Optional[str] = None

class ErrorUpdateSuccess(BaseModel):
    success: bool
    message: str | None = None