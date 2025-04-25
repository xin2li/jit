from typing import Optional

from fastapi import FastAPI, HTTPException,Depends
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError, NoResultFound, MultipleResultsFound
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from db import JITerror, FX0810o, FX0810u, FX0812, FXlog
from models import JITupdateTime, JITerrorCurrent, JITerrorFX0810uInfo, JITerrorFX0812Info, JITerrorFXInfo,JITerrorAll, JITerrorUpdate, ErrorUpdateSuccess

# 数据库连接
SQLALCHEMY_DATABASE_URL = "sqlite:///./dmvtest.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)







# 创建FastAPI应用
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# 依赖项，用于获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/" , response_class=FileResponse)
def get_index():
    return FileResponse("static/templates/index.html")
@app.get("/errorhistory" , response_class=FileResponse)
def get_errorhistory():
    return FileResponse("static/templates/errorhistory.html")
@app.get("/jitmaster" , response_class=FileResponse)
def get_jitmaster():
    return FileResponse("static/templates/jitmaster.html")
#
@app.get("/updatetime", response_model=JITupdateTime)
def update_time(db=Depends(get_db)):
    try:
        error_updatetime = db.query(JITerror.error_timestamp).filter(JITerror.error_status0 == 2).limit(1).scalar()

        fx_updatetime = db.query(FXlog.fx_logtimestamp).filter(fx_log0= False, fx_logtag='LOG', fx_logstr='OC,LOG,TIME,FX').one().scalar()

        time = JITupdateTime(error_updatetime=error_updatetime, fx_updatetime=fx_updatetime)

        return time


    except NoResultFound:

        raise HTTPException(status_code=404, detail="未找到符合条件的记录")

    except MultipleResultsFound:

        raise HTTPException(status_code=400, detail="找到多条符合条件的记录")

    except SQLAlchemyError as e:

        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/currenterrors", response_model=list[JITerrorCurrent])
def get_current_errors(db=Depends(get_db)):
    try:
        # 查询 error_status0 == 2 的记录
        current_errors = db.query(
            JITerror.error_statusN,
            JITerror.error_plant,
            JITerror.error_tma,
            JITerror.error_ta,
            JITerror.error_fehler,
            JITerror.error_anzahl,
            JITerror.error_referenzen,
            JITerror.error_pn,
            JITerror.error_bemerkung,
            JITerror.error_type,
            JITerror.error_inlist
        ).filter(JITerror.error_status0 == 2).all()

        # 查询 error_status0 == 1 的记录
        last_anzahl = db.query(
            JITerror.error_tma,
            JITerror.error_ta,
            JITerror.error_fehler,
            JITerror.error_anzahl
        ).filter(JITerror.error_status0 == 1).all()

        # 将 last_anzahl 转换为字典，方便匹配
        last_anzahl_dict = {
            (error.error_tma, error.error_ta, error.error_fehler): error.error_anzahl
            for error in last_anzahl
        }

        # 构建 JITerrorCurrent 对象列表
        result = []
        for error in current_errors:
            # 获取匹配的 last_anzahl
            last_anzahl_value = last_anzahl_dict.get((error.error_tma, error.error_ta, error.error_fehler), None)
            result.append(JITerrorCurrent(
                error_statusN=error.error_statusN,
                error_plant=error.error_plant,
                error_tma=error.error_tma,
                error_ta=error.error_ta,
                error_fehler=error.error_fehler,
                error_anzahl=error.error_anzahl,
                error_lastanzahl=last_anzahl_value,
                error_referenzen=error.error_referenzen,
                error_pn=error.error_pn,
                error_bemerkung=error.error_bemerkung,
                error_type=error.error_type,
                error_inlist=error.error_inlist
            ))

        return result

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/errorfxpn", response_model=list[JITerrorFX0812Info])
def get_error_fx_pn(tma: str, ta: str, db=Depends(get_db)):
    try:
        # 查询符合条件的记录，并确保结果有且只有一条
        fx_0812_results = db.query(FX0812.fx_pn).filter(
            FX0812.fx_status == 1,
            FX0812.fx_ta == ta,
            FX0812.fx_tma == tma
        ).all()

        if not fx_0812_results:
            raise NoResultFound("未找到符合条件的记录")

        fx_0812 = [JITerrorFX0812Info(fx_pn=fx_pn) for fx_pn, in fx_0812_results]
        return fx_0812

    except NoResultFound:
        raise HTTPException(status_code=404, detail="未找到符合条件的记录")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/errorfxinfo", response_model=JITerrorFXInfo)
def get_error_fx_info(tma: str, ta: str, db=Depends(get_db)):
    try:
        # 查询符合条件的记录，并确保结果有且只有一条
        fx0810o = db.query(FX0810o).filter(
            FX0810o.fx_status == 1,
            FX0810o.fx_ta == ta,
            FX0810o.fx_tma == tma
        ).one()


        # 查询 FX0810u 记录
        fx0810u_results = db.query(FX0810u.fx_my, FX0810u.fx_vaild, FX0810u.fx_invalid, FX0810u.fx_pr).filter(
            FX0810u.fx_status == 1,
            FX0810u.fx_ta == ta,
            FX0810u.fx_tma == tma
        ).all()

        # 将查询结果转换为 JITerrorFX0810uInfo 对象列表
        fx_0810u = [JITerrorFX0810uInfo(fx_my=fx_my, fx_vaild=fx_vaild, fx_invalid=fx_invalid, fx_pr=fx_pr)
                    for fx_my, fx_vaild, fx_invalid, fx_pr in fx0810u_results]

        # 查询 FX0812 记录


        # 构建 JITerrorFXInfo 对象
        fx_info = JITerrorFXInfo(
            fx_tma=fx0810o.fx_tma,
            fx_ta=fx0810o.fx_ta,
            fx_remark=fx0810o.fx_remark,
            fx_fistag=fx0810o.fx_fistag,
            fx_testmode=fx0810o.fx_testmode,
            fx_partkind=fx0810o.fx_partkind,
            fx_min=fx0810o.fx_min,
            fx_max=fx0810o.fx_max,
            fx_0810u=fx_0810u,
        )

        return fx_info

    except NoResultFound:
        raise HTTPException(status_code=404, detail="未找到符合条件的记录")
    except MultipleResultsFound:
        raise HTTPException(status_code=400, detail="找到多条符合条件的记录")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# 更新JITerror记录
@app.put("/errorupdate", response_model=ErrorUpdateSuccess)
def update_error_info(update_error: JITerrorUpdate, db=Depends(get_db)):
    # 查询符合条件的错误记录
    try:
        db_error = db.query(JITerror).filter(
            JITerror.error_tma == update_error.error_tma,
            JITerror.error_ta == update_error.error_ta,
            JITerror.error_fehler == update_error.error_fehler,
            JITerror.error_status0 == 2
        ).one()  # 获取第一条记录

        if not db_error:
            return ErrorUpdateSuccess(success=False, message="未找到符合条件的JIT错误记录")

        # 更新字段
        db_error.error_pn = update_error.error_pn
        db_error.error_bemerkung = update_error.error_bemerkung
        db_error.error_type = update_error.error_type


        db.commit()  # 提交事务
        return ErrorUpdateSuccess(success=True, message="更新成功")
    except Exception as e:
        db.rollback()  # 回滚事务
        return ErrorUpdateSuccess(success=False, message=f"更新失败: {str(e)}")
    except NoResultFound:
        raise HTTPException(status_code=404, detail="未找到符合条件的记录")
    except MultipleResultsFound:
        raise HTTPException(status_code=400, detail="找到多条符合条件的记录")




if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8120, reload=True)
