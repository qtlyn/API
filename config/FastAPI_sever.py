from fastapi import FastAPI, Depends, HTTPException, status,UploadFile, File
from sqlalchemy.orm import Session
import database
from database import User, get_db
from pydantic import BaseModel
import time
from jose import jwt, JWTError 
import os
from dotenv import load_dotenv
from typing import Optional
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API đang chạy!"}

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

class LoginRequest(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    Id: int
    Ten: str
    DiaChi: str
    Email: str

class UserUpdate(BaseModel):
    Ten: Optional[str] = None
    DiaChi: Optional[str] = None
    Email: Optional[str] = None

# API tạo token
@app.post("/token")
def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == "admin" and form_data.password == "password":
        token_payload = {"sub": form_data.username, "exp": time.time() + 3600}
        access_token = jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sai tài khoản hoặc mật khẩu")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token không hợp lệ",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ hoặc đã hết hạn",
            headers={"WWW-Authenticate": "Bearer"},
        )

# API lấy danh sách user
@app.get("/users")
def get_users(db: Session = Depends(get_db), username: str = Depends(verify_token)):
    return db.query(User).all()

@app.get("/users/{user_id}")  
def get_user(user_id: int, db: Session = Depends(get_db), username: str = Depends(verify_token)):
    user = db.query(User).filter(User.Id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User khong ton tai")
    return user

# API thêm user
@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db), username: str = Depends(verify_token)):
    new_user = User(Id=user.Id, Ten=user.Ten, DiaChi=user.DiaChi, Email=user.Email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# API cập nhật user
@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db),username: str = Depends(verify_token)):
    db_user = db.query(User).filter(User.Id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Khong tim thay User!!!")
    if not any([user.Ten, user.DiaChi, user.Email]):
        raise HTTPException(status_code=400, detail="Khong co du lieu de cap nhat")
    if user.Ten is not None:
        db_user.Ten = user.Ten
    if user.DiaChi is not None:
        db_user.DiaChi = user.DiaChi
    if user.Email is not None:
        db_user.Email = user.Email
    db.commit()
    db.refresh(db_user)
    return db_user

# API xóa user
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db),username: str = Depends(verify_token)):
    db_user = db.query(User).filter(User.Id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Khong tim thay User")
    db.delete(db_user)
    db.commit()
    return {"message": "xoa User thanh cong"}



