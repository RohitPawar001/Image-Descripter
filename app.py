import streamlit as st
from PIL import Image
import numpy as np
import io
import requests
from io import BytesIO
from image_descripter.image_recognizer.image_recognization import ImagePredicator
from image_descripter.image_description.image_descripter import DescriptionGenerator


def main():
    st.title("Image Upload App")
    st.write("Upload an image to see it displayed with some basic information.")
    
    options = ["Upload The Local Image", "Upload The Image URL"]
    choice = st.selectbox("Choose an option:", options)

    st.write(f"You selected: {choice}")

    uploaded_file = None

    if choice == "Upload The Local Image":
        uploaded_file = st.file_uploader("Choose an image file", type=['jpg', 'jpeg', 'png', 'bmp', 'webp'])
    elif choice == "Upload The Image URL":
        url = st.text_area("Enter your image URL:")
        if url:
            try:
                response = requests.get(url)
                response.raise_for_status()  
                uploaded_file = BytesIO(response.content)
                uploaded_file.name = url.split("/")[-1]  
            except requests.exceptions.RequestException as e:
                st.error("Please upload a valid image URL")
                st.error(f"Error: {e}")

    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)  
            
          
            results = ImagePredicator.predict_image(image, top_k=5)
            pred = results[0]['class']
            st.write(f"Predicated Image : {pred}")
            
            
            description = DescriptionGenerator()
            information = description.generate_description(pred)
            
            with st.expander("**Image Description:**", expanded=True):
                
                width, height = image.size
                format_type = image.format if hasattr(image, 'format') else "Unknown"
                mode = image.mode
                
          
                img_array = np.array(image)
                
               
                st.write(information)
                
                    
                
                img_buffer = io.BytesIO()
                image.save(img_buffer, format=image.format if hasattr(image, 'format') else 'PNG')
                st.download_button(
                    label="Download Image",
                    data=img_buffer.getvalue(),
                    file_name=f"processed_{uploaded_file.name}",
                    mime=f"image/{format_type.lower() if format_type != 'Unknown' else 'png'}"
                )
        except Exception as e:
            st.error(f"Error processing: {e}")
            
            import traceback
            st.error(traceback.format_exc())
   
    else:
        st.info("Please upload an image to get started.")

if __name__ == "__main__":
    main()