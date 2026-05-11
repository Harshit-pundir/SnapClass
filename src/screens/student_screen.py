import numpy as np
import streamlit as st
import time

from src.components.dialog_enroll import enroll_dialog
from src.database.db import get_all_students, create_student, get_student_attendance, get_student_subjects
from src.pipelines.voice_pipeline import get_voice_embedding
from src.ui.base_layout import style_background_dashboard, style_base_layout
from PIL import Image
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard

from src.pipelines.face_pipeline import (
    get_face_embeddings,
    predict_attendance,
    train_classifier
)

def student_dashboard():
    student_data = st.session_state.student_data

    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')

    with c1:
        header_dashboard()

    with c2:
        st.subheader(f"""Welcome, {student_data["name"]}""")

        if st.button("Logout", type='secondary', key='loginbackbtn', shortcut='control + backspace'):
            st.session_state['login_type'] = None
            del st.session_state.student_data
            st.rerun()

    st.space()

    c1 , c2 = st.columns(2)
    with c1:
        st.header("Your enrolled subject")
    with c2:
        if st.button('Enroll in subject' , type = 'primary' , width='stretch'):
            enroll_dialog()


    st.divider()
    with st.spinner('Loading your enrolled subjects'):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)
    footer_dashboard()        

def student_screen():

    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    if 'show_registration' not in st.session_state:
        st.session_state.show_registration = False

    c1, c2 = st.columns(
        2,
        vertical_alignment='center',
        gap='xxlarge'
    )

    with c1:
        header_dashboard()

    with c2:
        if st.button(
            "Go back to Home",
            type='secondary',
            key='loginbackbtn',
            shortcut="control+backspace"
        ):
            st.session_state['login_type'] = None
            st.rerun()

    st.header('Login using FaceID', text_alignment='center')

    st.space()
    st.space()

    photo_source = st.camera_input(
        "Position your face in the center"
    )

    if photo_source:

        img = np.array(Image.open(photo_source))

        with st.spinner('AI is scanning'):

            detected, all_ids, num_faces = predict_attendance(img)

            if num_faces == 0:
                st.warning('Face not found')

            elif num_faces > 1:
                st.warning('Multiple face found')

            else:

                if detected:

                    student_id = list(detected.keys())[0]

                    all_students = get_all_students()

                    student = next(
                        (
                            s for s in all_students
                            if s['student_id'] == student_id
                        ),
                        None
                    )

                    if student:

                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student

                        st.toast(f"Welcome Back {student['name']}")

                        time.sleep(1)

                        st.rerun()

                else:

                    st.info(
                        'Face not recognised! You might be a new student!'
                    )

                    st.session_state.show_registration = True

    if st.session_state.show_registration:

        with st.container(border=True):

            st.header('Register new Profile')

            new_name = st.text_input(
                "Enter your name",
                placeholder='E.g. Harshit Pundir'
            )

            st.subheader('Optional : Voice Enrollment')

            st.info(
                "Enroll your voice for voice-only attendance"
            )

            audio_data = None

            try:

                audio_data = st.audio_input(
                    'Record a short phrase like I am present'
                )

            except Exception as e:

                st.error(f'Audio data failed: {e}')

            if st.button(
                'Create Account',
                type='primary'
            ):

                if new_name:

                    with st.spinner('Create profile ..'):

                        img = np.array(Image.open(photo_source))

                        encoding = get_face_embeddings(img)

                        if encoding and len(encoding) > 0:

                            face_emb = encoding[0].tolist()

                            voice_emb = None

                            if audio_data:
                                voice_emb = get_voice_embedding(
                                    audio_data.read()
                                )

                            response_data = create_student(
                                new_name,
                                face_embedding=face_emb,
                                voice_embedding=voice_emb
                            )

                            if response_data:

                                train_classifier()

                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'

                                st.session_state.student_data = (
                                    response_data[0]
                                )

                                st.toast(f'Welcome Back {new_name}')

                                time.sleep(1)

                                st.rerun()

                        else:

                            st.error(
                                "Couldn't capture your face properly"
                            )

                else:

                    st.error("Please type your name")

    footer_dashboard()