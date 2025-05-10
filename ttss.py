import streamlit as st
import base64
import os
import tempfile
from gtts import gTTS
from io import BytesIO

def text_to_speech(text, language):
    """Convert text to speech using Google's TTS API"""
    tts = gTTS(text=text, lang=language, slow=False)

    # Save to BytesIO object
    audio_bytes = BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)  # Move to the beginning of BytesIO

    return audio_bytes

def get_audio_player(audio_bytes):
    """Create an HTML audio player for the generated speech"""
    audio_base64 = base64.b64encode(audio_bytes.read()).decode()
    audio_tag = f'<audio controls autoplay><source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3"></audio>'
    return audio_tag

def save_audio(audio_bytes, filename):
    """Save the audio to a file"""
    with open(filename, "wb") as f:
        f.write(audio_bytes.getvalue())

def main():
    # Set up the Streamlit page
    st.set_page_config(
        page_title="Text-to-Speech Converter",
        page_icon="🔊",
        layout="wide"
    )

    # Page title with styling
    st.markdown("""
    <style>
    .big-title {
        font-size: 42px;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 20px;
    }
    .subtitle {
        font-size: 20px;
        color: #424242;
        text-align: center;
        margin-bottom: 30px;
    }
    .success-text {
        color: #4CAF50;
        font-weight: bold;
    }
    .urdu-text {
        font-family: 'Noto Nastaliq Urdu', serif;
        font-size: 20px;
        direction: rtl;
    }
    </style>
    <div class="big-title">Text-to-Speech Converter</div>
    <div class="subtitle">Convert your text to natural-sounding speech in English or Urdu</div>
    """, unsafe_allow_html=True)

    # Create two columns for better layout
    col1, col2 = st.columns([2, 1])

    with col1:
        # Language selection with radio buttons
        language_option = st.radio(
            "Select Language",
            ["English", "Urdu (اردو)"],
            horizontal=True,
            help="Choose the language for text-to-speech conversion"
        )

        # Map the language selection to language code
        language_mapping = {
            "English": "en",
            "Urdu (اردو)": "ur"
        }
        language_code = language_mapping[language_option]

        # Text input area
        if language_option == "Urdu (اردو)":
            text_input = st.text_area("Enter your text here in URDU", height=200, key="text_input", help="Enter the text you want to convert to speech")
        else:
            text_input = st.text_area("Enter your text here in ENGLISH:", height=200, key="text_input", help="Enter the text you want to convert to speech")


        # Button to generate speech
        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            convert_button = st.button("Convert to Speech", type="primary", use_container_width=True)

    with col2:
        st.subheader("Instructions")
        st.markdown("""
        1. Select your preferred language
        2. Type or paste your text in the text area
        3. Click "Convert to Speech" to hear the text
        4. You can download the audio file if you want to save it
        """)

        st.markdown("---")

        # Information about the app
        with st.expander("About This App"):
            st.markdown("""
            This text-to-speech converter uses Google's Text-to-Speech (gTTS) API to convert text to natural-sounding speech. The app supports multiple languages, including English and Urdu.

            **Features:**
            - High-quality speech synthesis
            - Support for English and Urdu languages
            - Option to download the generated audio file

            **Note:** This application requires an internet connection to function as it uses Google's online service for speech synthesis.
            """)

    # Generate speech when button is clicked
    if convert_button and text_input:
        with st.spinner('Generating speech...'):
            try:
                # Generate speech
                audio_bytes = text_to_speech(text_input, language_code)

                # Display success message
                st.markdown('<p class="success-text">✅ Speech generated successfully!</p>', unsafe_allow_html=True)

                # Display audio player
                st.markdown(get_audio_player(audio_bytes), unsafe_allow_html=True)

                # Reset BytesIO position for download
                audio_bytes.seek(0)

                # Add download button
                st.download_button(
                    label="Download Audio",
                    data=audio_bytes,
                    file_name=f"speech_{language_code}.mp3",
                    mime="audio/mp3"
                )

            except Exception as e:
                st.error(f"Error generating speech: {str(e)}")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        Created with Streamlit and Google Text-to-Speech
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()