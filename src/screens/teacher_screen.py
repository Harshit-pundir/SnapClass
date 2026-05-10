import streamlit as st
from src.components.dialog_create_subject import create_subject_dialog
from src.components.footer import footer_dashboard
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.database.db import (
    check_teacher_exists,
    create_teacher,
    get_teacher_subjects,
    teacher_login
)

def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    if "teacher_data" in st.session_state:
        teacher_dashboard()

    elif (
        'teacher_login_type' not in st.session_state
        or st.session_state.teacher_login_type == "login"
    ):
        teacher_screen_login()

    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()

def teacher_dashboard():
    teacher_data = st.session_state.teacher_data

    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')

    with c1:
        header_dashboard()

    with c2:
        st.subheader(f"""Welcome, {teacher_data["name"]}""")

        if st.button("Logout", type='secondary', key='loginbackbtn', shortcut='control + backspace'):
            st.session_state['login_type'] = None
            del st.session_state.teacher_data
            st.rerun()

    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"

    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == "take_attendance" else "tertiary"

        if st.button('Take Attendance', type=type1, width='stretch', icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = "take_attendance"
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == "manage_subjects" else "tertiary"

        if st.button('Manage Subjects', type=type2, width='stretch', icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = "manage_subjects"
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == "attendance_records" else "tertiary"

        if st.button('Attendance Records', type=type3, width='stretch', icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = "attendance_records"
            st.rerun()

    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()

    if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()

    if st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()

    footer_dashboard()

def teacher_tab_take_attendance():
    st.header('Take AI Attendance')

def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']

    col1, col2 = st.columns(2)

    with col1:
        st.header('Manage Subjects')

    with col2:
        if st.button('Create New Subject', width='stretch'):
            create_subject_dialog(teacher_id)

    subjects = get_teacher_subjects(teacher_id)

    if subjects:
        for sub in subjects:
            st.write(sub)

    else:
        st.info("No subjects found")

def teacher_tab_attendance_records():
    st.header('Attendance Records')

def login_teacher(username, password):
    if not username or not password:
        return False

    teacher = teacher_login(username, password)

    if teacher:
        st.session_state.user_role = "teacher"
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True

    return False

def teacher_screen_login():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')

    with c1:
        header_dashboard()

    with c2:
        if st.button("Go back to Home", type='secondary', key='loginbackbtn', shortcut='control + backspace'):
            st.session_state['login_type'] = None
            st.rerun()

    st.header("Login using password", text_alignment='center')

    st.space()
    st.space()

    teacher_username = st.text_input("Enter username", placeholder="Harshit Pundir")
    teacher_password = st.text_input("Enter password", type='password')

    st.divider()

    btc1, btc2 = st.columns(2)

    with btc1:
        if st.button('Login', type='secondary', icon=':material/passkey:', shortcut='control+enter', width='stretch'):
            if login_teacher(teacher_username, teacher_password):
                st.toast("Welcome back 👏")

                import time
                time.sleep(2)

                st.rerun()

            else:
                st.error("Invalid username or password")

    with btc2:
        if st.button('Register Instead', type='primary', icon=':material/passkey:', width='stretch'):
            st.session_state.teacher_login_type = 'register'

    footer_dashboard()

def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_confirm_pass):
    if not (
        teacher_name
        and teacher_username
        and teacher_pass
        and teacher_confirm_pass
    ):
        return False, "All fields must be filled"

    if check_teacher_exists(teacher_username):
        return False, "Username already taken"

    if teacher_pass != teacher_confirm_pass:
        return False, "Passwords should match"

    try:
        create_teacher(teacher_username, teacher_name, teacher_pass)
        return True, "Successfully created"

    except Exception:
        return False, "Unexpected error"

def teacher_screen_register():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')

    with c1:
        header_dashboard()

    with c2:
        if st.button("Go back to Home", type='secondary', key='loginbackbtn', shortcut='control + backspace'):
            st.session_state['login_type'] = None
            st.rerun()

    st.header("Register your teacher profile")

    st.space()
    st.space()

    teacher_username = st.text_input("Enter username", placeholder="@HarshitPundir")
    teacher_name = st.text_input("Enter name", placeholder="Harshit Pundir")
    teacher_password = st.text_input("Enter password", type='password')
    confirm_teacher_password = st.text_input("Confirm your password", type='password')

    st.divider()

    btc1, btc2 = st.columns(2)

    with btc1:
        if st.button('Register Now', type='secondary', icon=':material/passkey:', width='stretch'):
            success, message = register_teacher(teacher_username, teacher_name, teacher_password, confirm_teacher_password)

            if success:
                st.success(message)

                import time
                time.sleep(2)

                st.session_state.teacher_login_type = "login"
                st.rerun()

            else:
                st.error(message)

    with btc2:
        if st.button('Login Instead', type='primary', icon=':material/passkey:', shortcut='control+enter', width='stretch'):
            st.session_state.teacher_login_type = 'login'

    footer_dashboard()