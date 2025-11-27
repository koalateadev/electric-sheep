import io
import zipfile
import pandas as pd
import streamlit as st

from process.map_inputs import generate_output

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
    df_a = pd.read_csv(file_a)
    df_b = pd.read_json(file_b)
    df_c = pd.read_json(file_c)

    outputs = run_mappings(df_a, df_b, df_c)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for filename, df in outputs.items():
            csv_bytes = df.encode("utf-8")
            zf.writestr(filename, csv_bytes)

    zip_buffer.seek(0)

    st.download_button(
        label="Download results as ZIP",
        data=zip_buffer,
        file_name="results.zip",
        mime="application/zip",
    )
else:
    st.info("Upload all three input files to generate the ZIP.")
