import time 
import streamlit as st
import os
import base64
from pathlib import Path
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
imgEjemplo = os.path.join(current_dir, 'imgEjemplo')
backend = os.path.join(current_dir, 'backend')
sys.path.append(backend)
import app


class Frontend():
    def __init__(self):
        self.resultados = None
        self.response = None
    

    def img_to_bytes(self, img_path):
        img_bytes = Path(img_path).read_bytes()
        encoded = base64.b64encode(img_bytes).decode()
        return encoded
    

    def img_to_html(self, img_path):
        img_html = "<img src='data:image/jpeg;base64,{}' class='img-fluid'>".format(
        self.img_to_bytes(img_path)
        )
        return img_html


    def analizar_imagen(self, filesData):
        image_data = {}
        for data in filesData:
            image_data[data.name] = data.getvalue()
        data = {'image': image_data}
        self.response = app.process_image(data)
        
    
    def checkResponse(self):
        if self.response['status'] == 'ok':
            self.resultados = self.response['pdf-name']
        elif self.response['status'] == 'error':
            text = str(self.response['images'])
            self.resultados =  f"Las imagenes: {text[1:text.index(']')]} no se han procesado correctamente"


    def descargarPDF(self, nombrePDF):
        archivo_pdf = nombrePDF
        if not os.path.isfile(archivo_pdf):
            raise NameError
        else:
            with open(archivo_pdf, 'rb') as file:
                contents = file.read()
            st.download_button(
                label="Descargar archivo",
                data=contents,
                file_name='resultados.pdf',
                mime='text/plain',
            )

    def considerations(self):
        st.markdown('***Consideraciones a tener en cuenta a la hora de usar la aplicación***')
        textos = ['La captura de la tira debe ser en forma vertical, dejando el lado del sosten de la tira '
                  'apuntando hacia nuestro cuerpo.',
                  'La tira debe ser de la marca **Combur 10 Test**, en caso de que se envien diferentes tiras'
                  ' el sistema enviara resultados erroneos.',
                  'La captura de la tira debe hacerse teniendo en cuenta que la misma debe estar a 90º '
                  '(activar cuadricula de asistencia en la camara del telefono para ayuda).',
                  'Utilizar una fuente de iluminación al momento de capturar la tira reactiva. La imagen no '
                  'debe incluir sombras que esten sobre la tira.',
                  'La tira debe estar posada sobre un fondo el cual no contenga formas geometricas que se asemejen a un cuadrado.'
                  ' Puede ser de correcto uso una toalla, una servilleta, etc. siempre y cuando se cumpla la primer condición.',
                  'En la captura debe salir solo la tira y la servilleta. Esto quiere decir que no puede salir parte de la mesa o'
                  ' de la base en donde se esten realizando los estudios, o algun otro elemento que interfiera en el analisis.']
        for texto in textos:
                st.markdown(f"- {texto}")
        ruta = imgEjemplo+'/imgEjemplo.jpeg'
        st.markdown("<p style='text-align: center; color: grey;'>"+self.img_to_html(ruta)+"</p>", unsafe_allow_html=True)
        st.markdown("<h6 style='text-align: center;'> Imagen ejemplo </h6>", unsafe_allow_html=True)

    def main(self):
        st.set_page_config(page_title="Testrine - Análisis de orina")
        st.title("Testrine - Análisis de orina")
        self.considerations()
        uploaded_file = st.file_uploader("Buscar Imagen" ,accept_multiple_files=True, type=["jpg","jpeg","png"])
        if st.button("Analizar Imagen"):
            with st.spinner():
                if uploaded_file != []:
                    inicio = time.time()
                    self.analizar_imagen(uploaded_file)
                    fin = time.time()
                    self.checkResponse()
                    try:
                        self.descargarPDF(self.resultados)
                        st.success('Analisis realizado con exito. Puedes ver los resultados en el pdf.')
                    except NameError:
                        st.error(self.resultados)
                    print('Tiempo transcurrido: ', fin - inicio)
                else:
                    st.error("Por favor cargue una imagen.")

if __name__ == '__main__':
    front = Frontend()
    front.main()