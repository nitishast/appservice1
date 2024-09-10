import streamlit as st
from streamlit_option_menu import option_menu
from InvoiceExtracter.invoiceExtracter import run as invoiceapp
from TalkToYourPDF.talkToPDF import run as pdfapp
from QnABot.QnA import run as QnA
from QnABot.QnAUpdated import run as QnAUI
from FastInfrence.groqapp import run as groqapp
from FastInfrence.groqwithupload import run as groqappwithupload
from landingpage import landingpage
st.set_page_config(page_title="Homepage! Welcome.",layout="wide",)

st.logo("public/logo.jpg")



st.sidebar.text("Made with ❤️ by nitishast")

class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })

    def run(self):
        with st.sidebar:
            app = option_menu(
                menu_title='Navigation',
                options=['Home','Invoice','QNAUI', 'Talk','GroQChat','GroQChatWithUpload'],
                icons=['home','file-earmark-text','chat-dots','chat-dots', 'book','chat-dots','chat-dots'],
                menu_icon='list',
                default_index=0,
                styles={
                    "container": {"padding": "15px", "background-color": "#f8f9fa"},
                    "icon": {"color": "#495057", "font-size": "18px"},
                    "nav-link": {
                        "color": "#495057",
                        "font-size": "16px",
                        "text-align": "left",
                        "margin": "5px 0",
                        "padding": "10px",
                        "--hover-color": "#e9ecef"
                    },
                    "nav-link-selected": {"background-color": "#e9ecef", "color": "#212529"},
                    "menu-title": {"color": "#212529", "font-size": "20px", "font-weight": "bold"}
                }
            )
        
        if app == 'Home':
            landingpage()
        if app == 'Invoice':
            invoiceapp()
        # if app == 'QNA':
        #     QnA()
        if app== 'QNAUI':
            QnAUI()
        if app == 'Talk':
            pdfapp()
        if app == 'GroQChat':
            groqapp()
        if app == 'GroQChatWithUpload':
            groqappwithupload()

if __name__ == "__main__":
    multi_app = MultiApp()
    multi_app.add_app("Home", landingpage)
    multi_app.add_app("Invoice", invoiceapp)
    # multi_app.add_app("QNA", invoiceapp)
    multi_app.add_app("QNAUI", QnAUI)
    multi_app.add_app("Invoice", invoiceapp)
    multi_app.add_app("GroQChat", groqapp)
    multi_app.add_app("GroQChatWithUpload", groqappwithupload)
    multi_app.run()
