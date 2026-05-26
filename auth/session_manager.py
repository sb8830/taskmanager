from datetime import datetime, timedelta, timezone
import streamlit as st
from config import SESSION_TIMEOUT_MINUTES

class SessionManager:
    @staticmethod
    def init():
        st.session_state.setdefault("authenticated", False)
        st.session_state.setdefault("user", None)
        st.session_state.setdefault("last_seen", datetime.now(timezone.utc))

    @staticmethod
    def touch():
        st.session_state["last_seen"] = datetime.now(timezone.utc)

    @staticmethod
    def expired() -> bool:
        last_seen = st.session_state.get("last_seen")
        if not last_seen:
            return True
        return datetime.now(timezone.utc) - last_seen > timedelta(minutes=SESSION_TIMEOUT_MINUTES)

    @staticmethod
    def require_role(*roles):
        return st.session_state.get("authenticated") and st.session_state.get("user", {}).get("role") in roles
