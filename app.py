import streamlit as st
from streamlit_option_menu import option_menu

from database.seed import init_db
from database.database import get_session
from auth.auth_manager import AuthManager
from auth.session_manager import SessionManager
from models.notification_model import Notification
from pages import moderator_dashboard, agent_dashboard, task_management, reports_page, announcements, profile_page, settings_page
from utils.ui import apply_theme

st.set_page_config(page_title="TaskFlow Pro", page_icon="TF", layout="wide", initial_sidebar_state="expanded")
apply_theme()
init_db()
SessionManager.init()


def login_screen():
    left, center, right = st.columns([1, 1.2, 1])
    with center:
        st.markdown("# TaskFlow Pro")
        st.caption("Enterprise Task Assignment & Management Portal")
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="admin@taskflow.com")
            password = st.text_input("Password", type="password", placeholder="Admin@123")
            role_hint = st.radio("Login as", ["Moderator", "Agent"], horizontal=True)
            submitted = st.form_submit_button("Login", use_container_width=True)
        if submitted:
            db = get_session()
            try:
                user = AuthManager.login(db, email, password)
                if user and user.role == role_hint:
                    st.success("Login successful.")
                    st.rerun()
                elif user:
                    AuthManager.logout(db)
                    st.error("This account does not match the selected role.")
                else:
                    st.error("Invalid credentials or inactive account.")
            finally:
                db.close()
        with st.expander("Sample Login Credentials"):
            st.code("Moderator: admin@taskflow.com / Admin@123\nAgent: agent@taskflow.com / Agent@123")
        with st.expander("Forgot Password"):
            st.info("Contact your Moderator to reset your password. Moderators can reset passwords from Settings > Users.")


def sidebar(db, user):
    unread = db.query(Notification).filter(Notification.user_id == user["id"], Notification.is_read == False).count()
    with st.sidebar:
        st.markdown(f"### TaskFlow Pro")
        st.caption(f"{user['name']} | {user['role']}")
        st.caption(f"Unread notifications: {unread}")
        options = ["Dashboard", "Tasks", "Reports", "Announcements", "Profile"]
        icons = ["speedometer", "list-task", "bar-chart", "megaphone", "person"]
        if user["role"] == "Moderator":
            options.append("Settings")
            icons.append("gear")
        selected = option_menu(None, options, icons=icons, default_index=0)
        st.divider()
        if st.button("Logout", use_container_width=True):
            AuthManager.logout(db)
            st.rerun()
    return selected


def main_app():
    if SessionManager.expired():
        st.warning("Session expired. Please log in again.")
        AuthManager.logout()
        st.rerun()
    SessionManager.touch()
    user = st.session_state["user"]
    db = get_session()
    try:
        selected = sidebar(db, user)
        if selected == "Dashboard":
            if user["role"] == "Moderator":
                moderator_dashboard.render(db)
            else:
                agent_dashboard.render(db, user)
        elif selected == "Tasks":
            if user["role"] == "Moderator":
                task_management.render(db, user)
            else:
                agent_dashboard.render(db, user)
        elif selected == "Reports":
            if user["role"] == "Moderator":
                reports_page.render(db)
            else:
                st.error("Reports are available to Moderators only.")
        elif selected == "Announcements":
            announcements.render(db, user)
        elif selected == "Profile":
            profile_page.render(db, user)
        elif selected == "Settings":
            settings_page.render(db, user)
    finally:
        db.close()


if not st.session_state.get("authenticated"):
    login_screen()
else:
    main_app()
