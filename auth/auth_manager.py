from datetime import datetime, timezone
import streamlit as st
from models.user_model import User
from auth.password_utils import verify_password, hash_password
from services.activity_service import ActivityService

class AuthManager:
    @staticmethod
    def login(db, email: str, password: str):
        user = db.query(User).filter(User.email == email.lower().strip(), User.is_deleted == False).first()
        if not user or not user.is_active or not verify_password(password, user.password_hash):
            return None
        user.last_login_at = datetime.now(timezone.utc)
        db.commit()
        st.session_state["authenticated"] = True
        st.session_state["user"] = {
            "id": user.id,
            "name": user.full_name,
            "email": user.email,
            "role": user.role,
            "department_id": user.department_id,
        }
        ActivityService.log(db, user.id, "LOGIN", "User logged in")
        return user

    @staticmethod
    def logout(db=None):
        user = st.session_state.get("user")
        if db and user:
            db_user = db.query(User).filter(User.id == user["id"]).first()
            if db_user:
                db_user.last_logout_at = datetime.now(timezone.utc)
                db.commit()
                ActivityService.log(db, user["id"], "LOGOUT", "User logged out")
        st.session_state.clear()

    @staticmethod
    def change_password(db, user_id: int, old_password: str, new_password: str):
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not verify_password(old_password, user.password_hash):
            return False, "Old password is incorrect."
        user.password_hash = hash_password(new_password)
        user.reset_required = False
        db.commit()
        ActivityService.log(db, user_id, "PASSWORD_CHANGED", "User changed password")
        return True, "Password changed successfully."
