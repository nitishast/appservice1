import streamlit as st
from streamlit_option_menu import option_menu
from InvoiceExtracter.invoiceExtracter import run as invoiceapp
from TalkToYourPDF.talkToPDF import run as pdfapp
from QnABot.QnA import run as QnA
from FastInfrence.groqapp import run as groqapp
from landingpage import landingpage
st.set_page_config(page_title="Homepage! Welcome.")


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
                options=['Home','Invoice', 'QNA', 'Talk','GroQChat'],
                icons=['home','file-earmark-text', 'chat-dots', 'book','chat-dots'],
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
        if app == 'QNA':
            QnA()
        if app == 'Talk':
            pdfapp()
        if app == 'GroQChat':
            groqapp()

if __name__ == "__main__":
    multi_app = MultiApp()
    multi_app.add_app("Home", landingpage)
    multi_app.add_app("Invoice", invoiceapp)
    multi_app.add_app("QNA", invoiceapp)
    multi_app.add_app("Invoice", invoiceapp)
    multi_app.add_app("GroQChat", groqapp)
    multi_app.run()