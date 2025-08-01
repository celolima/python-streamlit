import streamlit as st
import openai
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

openai = openai.Client()

def transcreve_audio(file_audio, prompt=None):
    """Função para transcreve o áudio usando a API da OpenAI"""
    if(file_audio):
        transcription = openai.audio.transcriptions.create(
            model="whisper-1",
            language="pt",
            response_format="text",
            file=file_audio,
            prompt=prompt
        )
        return transcription

def main():
    st.header('🎤App Transcript', divider=True)
    st.subheader('Transcreva áudios e vídeos')    
    tab_video, tab_audio = st.tabs(['Vídeos', 'Áudio'])
    with tab_video:
        st.markdown('Teste em vídeo')
    with tab_audio:
        st.markdown('Teste em audio')
        prompt_audio = st.text_input('Digite o seu prompt')
        file_audio = st.file_uploader('Adicione um arquivo de áudio .mp3', type=['mp3'])
        if file_audio:
            transcricao_audio = transcreve_audio(file_audio, prompt_audio)
            if transcricao_audio:
                st.write(transcricao_audio)
            else:
                st.error('Erro ao transcrever o audio')
                
if __name__ == "__main__":
    main()