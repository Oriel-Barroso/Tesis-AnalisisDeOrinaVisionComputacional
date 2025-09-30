import time
import mysql
import pandas as pd
import streamlit as st
import os
import base64
from pathlib import Path
import sys
import json
import pickle
import uuid
import re
from datetime import datetime, time
from mysql.connector import Error
from backend.excelConverter import CreateExcel
from backend.mysql.src.services.user_service import UserService
from backend.pdfConverter import PdfConverter

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
        self.db_conn = None
        self.user_service = None
        self._init_db()

    def _init_db(self):
        try:
            self.db_conn = mysql.connector.connect(
                host=os.getenv("MYSQL_HOST", "localhost"),
                user=os.getenv("MYSQL_USER", "root"),
                password=os.getenv("MYSQL_PASSWORD", "1234"),
                database=os.getenv("MYSQL_DB", "testrine")
            )
            self._ensure_users_table()
            self.user_service = UserService(self.db_conn)
        except Error as e:
            st.warning(f"No se pudo conectar a MySQL: {e}")
    
    def _ensure_users_table(self):
        try:
            cursor = self.db_conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    dni VARCHAR(64) NOT NULL UNIQUE
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS resultados_test (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    dni VARCHAR(64) NOT NULL,
                    `Sangre` VARCHAR(50),
                    `Bilirruina` VARCHAR(50),
                    `Urobilinogeno` VARCHAR(50),
                    `Cuerpos cetonicos` VARCHAR(50),
                    `Glucosa` VARCHAR(50),
                    `Proteina` VARCHAR(50),
                    `Nitrito` VARCHAR(50),
                    `Leucocitos` VARCHAR(50),
                    `pH` VARCHAR(50),
                    `Densidad relativa` VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (dni) REFERENCES users(dni)
                      ON DELETE CASCADE ON UPDATE CASCADE
                )
            """)
            self.db_conn.commit()
        except Error as e:
            st.error(f"Error creando tabla users: {e}")
        finally:
            cursor.close()

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

    def descargar(self, data_file):
        archivo_pdf = 'resultados.pdf'
        archivo_excel = 'resultadosExcel.xlsx'
        if not os.path.isfile(archivo_pdf):
            raise NameError
        else:
            with open(archivo_pdf, 'rb') as file:
                contentsPDF = file.read()
            with open(archivo_excel, 'rb') as file:
                contentsExl = file.read()
            for data in data_file:
                name_file = data.name
                name_file = name_file.replace('.jpg', '')
                name_file = name_file.replace('.jpeg', '')
                name_file = name_file.replace('.png', '')
            actual_time = datetime.now()
            btnExl = self.download_button(
                contentsExl, f'testrine_results_{name_file}_{actual_time}.xlsx', 'Descargar Excel', "excel")
            st.markdown(btnExl, unsafe_allow_html=True)
            btnPDF = self.download_button(
                contentsPDF, f'testrine_results_{name_file}_{actual_time}.pdf', 'Descargar PDF', "pdf")
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

    def regenerate_pdf(self, dni):
        if not self.user_service:
            st.error("Servicio de usuarios no disponible.")
            return
        rows = self.user_service.get_test_results_by_dni(dni)
        if not rows:
            st.info("Sin resultados para ese DNI.")
            return
        pdf_data = {}
        for row in rows:
            lista = [
                f"La sangre tiene un valor: {row['Sangre']}",
                f"La bilirruina tiene un valor: {row['Bilirruina']}",
                f"El urobilinogeno tiene un valor: {row['Urobilinogeno']}",
                f"Los cuerpos cetonicos tienen un valor: {row['Cuerpos cetonicos']}",
                f"La glucosa tiene un valor: {row['Glucosa']}",
                f"La proteina tiene un valor: {row['Proteina']}",
                f"El nitrito tiene un valor: {row['Nitrito']}",
                f"Los leucocitos tienen un valor: {row['Leucocitos']}",
                f"El pH tiene un valor de: {row['pH']}",
                f"La densidad relativa tiene un valor de: {row['Densidad relativa']}",
            ]
            pdf_data[f"resultado_{dni}.jpeg"] = lista
        try:
            PdfConverter(pdf_data).createPDF()  
            pdf_path = "resultados.pdf"
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    st.download_button("Descargar PDF regenerado", f,
                                       file_name=f"resultados_{dni}.pdf",
                                       mime="application/pdf")
                st.success("PDF regenerado.")
            else:
                st.error("No se encontró el PDF generado.")
        except Exception as e:
            st.error(f"Error al regenerar PDF: {e}")

    def regenerate_excel(self, dni):
        if not self.user_service:
            st.error("Servicio de usuarios no disponible.")
            return
        rows = self.user_service.get_test_results_by_dni(dni)
        if not rows:
            st.info("Sin resultados para ese DNI.")
            return
        excel_data = {}
        for row in rows:
            excel_data[f"resultado_{dni}.jpeg"] = {
                'Sangre': row['Sangre'],
                'Bilirruina': row['Bilirruina'],
                'Urobilinogeno': row['Urobilinogeno'],
                'Cuerpos cetonicos': row['Cuerpos cetonicos'],
                'Glucosa': row['Glucosa'],
                'Proteina': row['Proteina'],
                'Nitrito': row['Nitrito'],
                'Leucocitos': row['Leucocitos'],
                'pH': row['pH'],
                'Densidad relativa': row['Densidad relativa'],
            }
        try:
            CreateExcel(excel_data).createExl()  # genera resultadosExcel.xlsx
            excel_path = "resultadosExcel.xlsx"
            if os.path.exists(excel_path):
                with open(excel_path, "rb") as f:
                    st.download_button("Descargar Excel regenerado", f,
                                       file_name=f"resultados_{dni}.xlsx",
                                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                st.success("Excel regenerado.")
            else:
                st.error("No se encontró el Excel generado.")
        except Exception as e:
            st.error(f"Error al regenerar Excel: {e}")

    def main(self):
        st.set_page_config(page_title="Testrine - Análisis de orina")
        self.add_bg_from_local('imgBack.png')
        st.title("Testrine - Análisis de orina")
        self.considerations()
        st.markdown("---")
        st.subheader("Regeneración de reportes")
        dni_reportes = st.text_input("DNI para regenerar PDF/Excel", key="dni_reportes")
        col_r1, col_r2 = st.columns(2)
        if col_r1.button("Regenerar PDF"):
            if dni_reportes.strip():
                self.regenerate_pdf(dni_reportes.strip())
            else:
                st.error("Ingrese un DNI.")
        if col_r2.button("Regenerar Excel"):
            if dni_reportes.strip():
                self.regenerate_excel(dni_reportes.strip())
            else:
                st.error("Ingrese un DNI.")
        st.markdown("---")
        st.subheader("Gestión de Usuarios")
        dni_input = st.text_input("Ingresar DNI (string)")
        colA, colB = st.columns([1,1])
        with colA:
            if st.button("Agregar Usuario"):
                if not self.user_service:
                    st.error("Servicio no disponible.")
                elif not dni_input.strip():
                    st.error("El DNI no puede estar vacío.")
                else:
                    try:
                        nuevo_id = self.user_service.add_user(dni_input.replace('.', '').strip())
                        st.success(f"Usuario agregado id {nuevo_id}")
                    except Error as e:
                        if "Duplicate" in str(e):
                            st.error("El DNI ya existe.")
                        else:
                            st.error(f"Error: {e}")
        with colB:
            ver_pacientes = st.button("Ver Pacientes")

        if ver_pacientes and self.user_service:
            try:
                users = self.user_service.get_all_users()
                if users:
                    st.dataframe(pd.DataFrame(users), use_container_width=True)
                else:
                    st.info("Sin usuarios.")
            except Error as e:
                st.error(f"Error: {e}")
        elif ver_pacientes and not self.user_service:
            st.error("Servicio no disponible.")

        
        st.markdown("---")
        st.subheader("Análisis de imágenes")
        dni_seleccionado = None
        if self.user_service:
            try:
                lista_users = self.user_service.get_all_users()
                dnis = [u['dni'] for u in lista_users] if lista_users else []
                if dnis:
                    dni_seleccionado = st.selectbox("Seleccionar DNI para asociar resultados", dnis)
                else:
                    st.info("Primero cargue un usuario para asociar resultados.")
            except Error as e:
                st.error(f"Error obteniendo usuarios: {e}")
        uploaded_file = st.file_uploader(
            "Buscar Imagen", accept_multiple_files=True, type=["jpg", "jpeg", "png"])
        if st.button("Analizar Imagen") and dni_seleccionado is not None:
            with st.spinner():
                if uploaded_file != []:
                    self.analizar_imagen(uploaded_file)
                    self.checkResponse()
                    if self.resultadosERROR:
                        st.error(self.resultadosERROR)
                    if self.resultadosOK:
                        st.success(f'{self.resultadosOK}. Puedes ver los resultados en PDF o Excel.')
                        # Insertar resultados en DB
                        if dni_seleccionado and 'resultExcel' in self.response:
                            inserciones = 0
                            for _, res_dict in self.response['resultExcel'].items():
                                try:
                                    self.user_service.add_test_results(dni_seleccionado, res_dict)
                                    inserciones += 1
                                except Error as e:
                                    st.error(f"Error guardando resultado: {e}")
                            if inserciones:
                                st.success(f"{inserciones} resultado(s) guardado(s) en la base.")
                        elif not dni_seleccionado:
                            st.warning("No se guardaron resultados en DB: no se seleccionó DNI.")
                        self.descargar(uploaded_file)
                else:
                    st.error("Por favor cargue una imagen.")
        else:
            if dni_seleccionado is None:
                st.warning("Seleccione un DNI para asociar resultados.")



if __name__ == '__main__':
    front = Frontend()
    front.main()
