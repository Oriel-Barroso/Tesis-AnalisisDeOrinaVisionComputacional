import time
import streamlit as st
import os
import base64
from pathlib import Path
import sys
import json
import pickle
import uuid
import re
import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
imgEjemplo = os.path.join(current_dir, 'imgEjemplo')
backend = os.path.join(current_dir, 'backend')
sys.path.append(backend)

import app


class Frontend():
    def __init__(self):
        self.resultadosOK = ""
        self.resultadosERROR = ""
        self.response = None

    def download_button(self, object_to_download, download_filename,
                        button_text,typeVal, pickle_it=False):
        if pickle_it:
            try:
                object_to_download = pickle.dumps(object_to_download)
            except pickle.PicklingError as e:
                st.write(e)
                return None

        else:
            if isinstance(object_to_download, bytes):
                pass

            elif isinstance(object_to_download, pd.DataFrame):
                object_to_download = object_to_download.to_csv(index=False)

            # Try JSON encode for everything else
            else:
                object_to_download = json.dumps(object_to_download)

        try:
            # some strings <-> bytes conversions necessary here
            b64 = base64.b64encode(object_to_download.encode()).decode()

        except AttributeError:
            b64 = base64.b64encode(object_to_download).decode()

        button_uuid = str(uuid.uuid4()).replace('-', '')
        button_id = re.sub('\d+', '', button_uuid)

        custom_css = f"""
            <style>
                #{button_id} {{
                    display: inline-flex;
                    -webkit-box-align: center;
                    align-items: center;
                    -webkit-box-pack: center;
                    justify-content: center;
                    font-weight: 400;
                    background-color: rgb(19, 23, 32);
                    color: rgb(250, 250, 250);
                    padding: 0.25rem 0.75rem;
                    line-height: 1.6;
                    height: 35px;
                    width: 132px;
                    color: inherit;
                    width: auto
                    position: relative;
                    text-decoration: none;
                    border-radius: 0.25rem;
                    border-top-left-radius: 0.25rem;
                    border-top-right-radius: 0.25rem;
                    border-bottom-right-radius: 0.25rem;
                    border-bottom-left-radius: 0.25rem;
                    border-width: 1px;
                    border-style: solid;
                    border-color: rgb(230, 234, 241, 0.2);
                    border-image: initial;
                }} 
                #{button_id}:hover {{
                    border-color: rgb(246, 51, 102);
                    color: rgb(246, 51, 102);
                }}
                #{button_id}:active {{
                    box-shadow: none;
                    background-color: rgb(246, 51, 102);
                    color: white;
                    }}
            </style> """
        if typeVal == "pdf":
            dl_link = custom_css + \
            f'<a download="{download_filename}" id="{button_id}" href="data:application/pdf;base64,{b64}">{button_text}</a><br></br>'
        else:
            dl_link = custom_css + \
                f'<a download="{download_filename}" id="{button_id}" href="data:application/vnd.ms-excel;base64,{b64}">{button_text}</a><br></br>'

        return dl_link

    def img_to_bytes(self, img_path):
        img_bytes = Path(img_path).read_bytes()
        encoded = base64.b64encode(img_bytes).decode()
        return encoded

    def img_to_html(self, img_path):
        img_html = "<img src='data:image/jpeg;base64,{}' class='img-fluid'>".\
                   format(
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
        if self.response['imagesOK'] != []:
            textOK = str(self.response['imagesOK'])
            self.resultadosOK = f"Las imagenes: {textOK[1:textOK.index(']')]} se han procesado correctamente"
        if self.response['imagesError'] != []:
            textERROR = str(self.response['imagesError'])
            self.resultadosERROR = f"Las imagenes: {textERROR[1:textERROR.index(']')]} no se han procesado correctamente"

    def descargar(self):
        archivo_pdf = 'resultados.pdf'
        archivo_excel = 'resultadosExcel.xlsx'
        if not os.path.isfile(archivo_pdf):
            raise NameError
        else:
            with open(archivo_pdf, 'rb') as file:
                contentsPDF = file.read()
            with open(archivo_excel, 'rb') as file:
                contentsExl = file.read()
            btnExl = self.download_button(
                contentsExl, 'resultadosExcel.xlsx', 'Descargar Excel', "pdf")
            st.markdown(btnExl, unsafe_allow_html=True)
            btnPDF = self.download_button(
                contentsPDF, 'resultadosPDF.pdf', 'Descargar PDF', "excel")
            st.markdown(btnPDF, unsafe_allow_html=True)

    def considerations(self):
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

        with st.expander("🚨 Consideraciones a tener en cuenta 🚨"):
            for texto in textos:
                st.markdown(f"- {texto}")
            ruta = imgEjemplo+'/imgEjemplo.jpeg'
            st.markdown("<p style='text-align: center; color: grey;'>" +
                        self.img_to_html(ruta)+"</p>", unsafe_allow_html=True)
            st.markdown(
                "<h6 style='text-align: center;'> Imagen ejemplo </h6>", unsafe_allow_html=True)

    def add_bg_from_local(self, image_file):
        with open(image_file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
            background-size: cover
        }}
        </style>
        """,
        unsafe_allow_html=True
        )

    def main(self):
        st.set_page_config(page_title="Testrine - Análisis de orina")
        self.add_bg_from_local('imgBack.png')
        st.title("Testrine - Análisis de orina")
        self.considerations()
        uploaded_file = st.file_uploader(
            "Buscar Imagen", accept_multiple_files=True, type=["jpg", "jpeg", "png"])
        if st.button("Analizar Imagen"):
            with st.spinner():
                if uploaded_file != []:
                    self.analizar_imagen(uploaded_file)
                    self.checkResponse()
                    if self.resultadosERROR != "":
                        st.error(self.resultadosERROR)
                    if self.resultadosOK != "":
                        st.success(
                        f'{self.resultadosOK}. Puedes ver los resultados en el pdf o en excel.')
                        self.descargar()
                else:
                    st.error("Por favor cargue una imagen.")


if __name__ == '__main__':
    front = Frontend()
    front.main()
