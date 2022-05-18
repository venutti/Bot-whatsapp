from selenium import webdriver
from selenium.webdriver.common.by import By # Para poder buscar elementos es necesario tener la clase By
from selenium.webdriver.common.keys import Keys # Para poder importar la key ENTER y otras keys de teclado (ojo: también pueso obviar esto y escribir el codigo de la key)
from selenium.webdriver.firefox.service import Service # Para poder instalar el driver desde el mismo código, sin tener que extraer archivos adicionales
from webdriver_manager.firefox import GeckoDriverManager # Para poder instalar el driver desde el mismo código, sin tener que extraer archivos adicionales
import time

XPATH_CHATBOX = "/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]"

browser = webdriver.Firefox(service=Service(GeckoDriverManager().install())) # Crea el driver para navegar

def enviar_mensaje(mensaje: str):
    """Pre: se ha autenticado correctamente a la sesión de WhatsApp y se tiene un chat abierto.
    Busca el chatbox mediante un XPATH, escribe el mensaje pasado por parametro y lo manda al chat.
    Post: se ha mandado el mensaje."""
    chatbox = browser.find_element(by=By.XPATH, value=XPATH_CHATBOX)
    chatbox.send_keys(mensaje)
    chatbox.send_keys(Keys.ENTER)

def seleccionarChat(nombre: str):
    """Pre: se ha autenticado correctamente a la sesión de WhatsApp.
    Busca al chat <nombre> y lo clickea, pudiendo luego poder escribir cualquier mensaje que querramos.
    Post: devuelve True si lo encontró, False si no."""
    print("Buscando chat...")
    elements = browser.find_elements(by=By.TAG_NAME, value="span")
    for element in elements:
        if element.text == nombre:
            element.click()
            print("Encontramos el chat buscado")
            return True
    return False

def validarQR():
    """Valida el QR que se presenta en la ventana del navegador.
    Mientras este presente, significa que aun no se inicio sesion en WhatsApp.
    Devuelve True si esta presente, False si no."""
    try:
        element = browser.find_element(by=By.TAG_NAME, value="canvas")
    except:
        return False
    return True

def botWhatsapp():
    browser.get("https://web.whatsapp.com/") # Abre la página pasada por parámetro
    time.sleep(5)

    # Bucle que espera la autenticación del usuario al leer el QR
    espera = True
    while espera:
        print("Esperando...")
        espera = validarQR()
        time.sleep(2)
        if espera == False:
            print("Te has autenticado!")
    time.sleep(5)

    if not seleccionarChat("Yo"):
        return
    
    # Spameo de frases sacadas de internet
    with open("resource/frases.txt","r") as f:
        for linea in f.readlines():
            enviar_mensaje(linea.rstrip())
            time.sleep(2)
    
botWhatsapp()