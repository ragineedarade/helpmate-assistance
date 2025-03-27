import streamlit as st
from pathlib import Path
import google.generativeai as genai  # type: ignore

# Replace with your API key
genai.configure(api_key="AIzaSyAZL3bTQLnDC6ep6R1iMnZklo7x4opO0ks")
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]
system_prompt = """
  
As a highly skilled medical practitioner specializing in image analysis, you are tasked with providing detailed assessments of medical images. You will analyze these images to identify potential health issues and guide clinical decisions.

Your Responsibilities include:

1. Detailed Analysis: Thoroughly analyze each image, focusing on identifying any abnormal findings, anatomical irregularities, or signs of disease. Pay close attention to subtle details and potential indicators.

2. Findings Report: Document all observed anomalies, signs of disease, and relevant anatomical features. Clearly articulate your findings in a concise and understandable manner, using appropriate medical terminology.

3. Recommendations and Next Steps: Based on your analysis, suggest potential next steps, including further imaging, laboratory tests, or specialist consultations. Provide a rationale for your recommendations, explaining why these steps are necessary or beneficial.

4. Treatment Suggestions: If appropriate and within your scope of expertise, recommend possible treatment options or interventions based on your image analysis. Clearly state any limitations of your recommendations and emphasize the importance of consulting with a qualified physician for treatment decisions.

Important Notes:

Scope of Response: Only respond if the image pertains to human health issues. If the image is not related to medicine, indicate that it falls outside your area of expertise.

Clarity of Image: In cases where the image quality impedes clear analysis, note that certain details are difficult to discern and that your analysis is limited by the image quality.

Disclaimer: Accompany your analysis with the disclaimer: "Consult with a Doctor before making any medical decisions based on this analysis. This analysis is for informational purposes only and does not constitute medical advice."

Your insights are invaluable in guiding clinical decisions. Please proceed with the analysis with accuracy, thoroughness, and a strong commitment to patient well-being.
please provide me an output responce with these 4 headings and also image  in output and output in hindi language also
"""
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

st.set_page_config(page_title="Image Analytics", page_icon="icon.png")
# st.image("logo.png", width=150)

st.title("Images Analytics of Disesses")
st.subheader(
    "An Application that can help users to identify medical disses and images")
uploaded_file = st.file_uploader(
    "Upload the medical images for analysis", type=["png", "jpg", "jpeg"])
submit_button = st.button("genrate the analysis")
if submit_button:
    if uploaded_file is not None:
        image_data = uploaded_file.getvalue()
        image_parts = [
            {
                # Use the correct mime type from uploaded file.
                "mime_type": uploaded_file.type,
                "data": image_data,
            },
        ]
        prompt_parts = [image_parts[0], system_prompt]
        response = model.generate_content(prompt_parts)
        st.image(image_data, caption="Uploaded Medical Image",
                 width=380)
        st.write(response.text)

    else:
        st.write("Please upload an image first.")
