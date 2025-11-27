import io
import json
import tempfile
import zipfile
import pandas as pd
import streamlit as st

from process.map_inputs import generate_output
from process.parse_responses import parse_responses

st.title("Futurekind Fellowship Response Mapper")

file_a = st.file_uploader("Responses (CSV)", type=["csv"], key="file_a")
file_b = st.file_uploader("Cohort (JSON)", type=["json"], key="file_b")
file_c = st.file_uploader("Name Mapping (JSON)", type=["json"], key="file_c")

def run_mappings(df_a, df_b, df_c):
    results = generate_output(df_a, df_b, df_c)

    # Return a dict of {filename_in_zip: dataframe}
    return {
        "output.json": results
    }

if file_a and file_b and file_c:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(file_a.read())
        temp_path = tmp.name

    df_a = parse_responses(temp_path)
    df_b = json.load(file_b)
    df_c = json.load(file_c)

    outputs = run_mappings(df_a, df_b, df_c)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for filename, df in outputs.items():
            zf.writestr(filename, json.dumps(df, indent=4))

    zip_buffer.seek(0)

    st.download_button(
        label="Download results as ZIP",
        data=zip_buffer,
        file_name="results.zip",
        mime="application/zip",
    )
else:
    st.info("Upload all three input files to generate the ZIP.")
