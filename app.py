import io
import json
import os
import tempfile
import zipfile
import streamlit as st

from process.generate_docx_output import write_to_docx
from process.generate_excel_output import write_to_excel
from process.map_inputs import generate_output
from process.parse_responses import parse_responses

st.title("Futurekind Fellowship Response Mapper")

file_a = st.file_uploader("Responses (CSV)", type=["csv"], key="file_a")
file_b = st.file_uploader("Cohort (JSON)", type=["json"], key="file_b")
file_c = st.file_uploader("Name Mapping (JSON)", type=["json"], key="file_c")

if file_a and file_b and file_c:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(file_a.read())
        temp_path = tmp.name

    df_a = parse_responses(temp_path)
    df_b = json.load(file_b)
    df_c = json.load(file_c)

    outputs, missing = generate_output(df_a, df_b, df_c)

    write_to_docx(outputs, "./process/output/")
    write_to_excel(outputs, "./process/output/")

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk("./process/output/"):
            for f in files:
                full = os.path.join(root, f)
                rel = os.path.relpath(full, "./process/output/")
                z.write(full, rel)

    zip_buffer.seek(0)

    st.error(
        f"The following students were found in teachable results but not cohort/airtable mapping: {missing}",
    )
    st.download_button(
        label="Download results as ZIP",
        data=zip_buffer,
        file_name="results.zip",
        mime="application/zip",
    )
else:
    st.info("Upload all three input files to generate the ZIP.")
