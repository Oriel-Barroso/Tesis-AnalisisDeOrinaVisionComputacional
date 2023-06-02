import subprocess

def run_streamlit_app():
    comando = 'streamlit run frontend/frontendApp.py'
    
    proceso = subprocess.Popen(comando, shell=True)
    
    proceso.wait()

run_streamlit_app()