import json
from pathlib import Path
from uuid import uuid4

import streamlit as st
from openpyxl import load_workbook
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Template


if 'db_session' not in st.session_state:
    DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(DATABASE_URL, echo=True)
    Session = sessionmaker(bind=engine)
    st.session_state.db_session = Session()


@st.dialog('Create New Template')
def create_template():
    name = st.text_input('Template Name')
    file = st.file_uploader('Template File', type='xlsx')
    submitted = st.button('Submit')
    if submitted and len(name.strip()) > 0 and file is not None:
        file_path = Path(f'template/{uuid4().hex}.xlsx')
        with open(file_path, mode='wb') as f:
            f.write(file.getvalue())
        wb = load_workbook(file_path)
        meta_data = dict()
        for sheet in wb.sheetnames:
            meta_data[sheet] = {
                tb_name: ref
                for tb_name, ref in wb[sheet].tables.items()
            }
        template = Template(
            name=name,
            file_path=str(file_path),
            meta_data=json.dumps(meta_data)
        )
        st.session_state.db_session.add(template)
        st.session_state.db_session.commit()
        st.rerun()
        return True
    return False


st.title('Report Template')
if st.button('Create New Template'):
    submitted = create_template()
    if submitted:
        st.toast('Created new template!')


session = st.session_state.db_session
templates = session.query(Template).all()
for template in templates:
    st.write(template.name, template.file_path)
