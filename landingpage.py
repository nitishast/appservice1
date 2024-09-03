import streamlit as st

def landingpage():
    st.title("Welcome to Our Multi-App Platform")
    
    st.write("""
    This is the landing page for our versatile application suite. Here's what you can do:
    
    - **Invoice**: Manage and process invoices efficiently
    - **QNA**: Ask questions and get answers from our AI
    - **Talk**: Interact with PDF documents
    - **GroQChat**: Experience high-performance document interaction
    
    Select an app from the navigation menu on the left to get started!
    """)
    
    st.image("https://placeholder.com/600x400", caption="Our Multi-App Platform", use_column_width=True)
    
    st.markdown("---")
    st.write("© 2024 Your Company Name. All rights reserved.")
    # Add a background image to the landing page using a local image file
    import base64

    def get_base64_of_bin_file(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()

    def set_png_as_page_bg(png_file):
        bin_str = get_base64_of_bin_file(png_file)
        page_bg_img = '''
        <style>
        .stApp {
            background-image: url("data:image/png;base64,%s");
            background-size: cover;
            background-attachment: fixed;
        }
        </style>
        ''' % bin_str
        st.markdown(page_bg_img, unsafe_allow_html=True)

    # Replace 'background.png' with the actual filename of your background image
    # set_png_as_page_bg('back.jpg')


# No need for the if __name__ == "__main__" block here

