from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
import io
import librosa
import streamlit as st


@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()


def get_voice_embedding(audio_bytes):
    try:
        if not audio_bytes:
            st.error("No audio received")
            return None

        encoder = load_voice_encoder()

        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)

        # Empty audio check
        if audio is None or len(audio) == 0:
            st.error("Empty audio")
            return None

        # Silent audio check
        if np.max(np.abs(audio)) < 0.001:
            st.error("Silent audio detected")
            return None

        wav = preprocess_wav(audio)

        # Processed wav check
        if wav is None or len(wav) == 0:
            st.error("Processed wav empty")
            return None

        embedding = encoder.embed_utterance(wav)

        return embedding.tolist()

    except Exception as e:
        st.error(f'Voice recog error: {e}')
        return None


def identify_speaker(new_embedding, candidates_dict, threshold=0.65):

    if new_embedding is None or not candidates_dict:
        return None, 0.0

    best_sid = None
    best_score = -1.0

    for sid, stored_embedding in candidates_dict.items():

        if stored_embedding:

            similarity = np.dot(
                np.array(new_embedding),
                np.array(stored_embedding)
            )

            if similarity > best_score:
                best_score = similarity
                best_sid = sid

    if best_score >= threshold:
        return best_sid, best_score

    return None, best_score


def process_bulk_audio(audio_bytes, candidates_dict, threshold=0.65):

    try:
        if not audio_bytes:
            st.error("No audio received")
            return {}

        encoder = load_voice_encoder()

        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)

        # Empty audio check
        if audio is None or len(audio) == 0:
            st.error("Empty audio")
            return {}

        # Silent audio check
        if np.max(np.abs(audio)) < 0.001:
            st.error("Silent classroom audio")
            return {}

        segments = librosa.effects.split(audio, top_db=30)

        identified_results = {}

        for start, end in segments:

            # Ignore very short segments
            if (end - start) < sr * 0.5:
                continue

            segment_audio = audio[start:end]

            # Ignore silent segments
            if np.max(np.abs(segment_audio)) < 0.001:
                continue

            wav = preprocess_wav(segment_audio)

            if wav is None or len(wav) == 0:
                continue

            embedding = encoder.embed_utterance(wav)

            sid, score = identify_speaker(
                embedding,
                candidates_dict,
                threshold
            )

            if sid:
                if sid not in identified_results or score > identified_results[sid]:
                    identified_results[sid] = score

        return identified_results

    except Exception as e:
        st.error(f'Bulk process error: {e}')
        return {}