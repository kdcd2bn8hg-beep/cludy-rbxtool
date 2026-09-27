import random
import time
import os
import string
import sys
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import init, Fore, Back, Style
import ctypes
import sys


kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')
hWnd = kernel32.GetConsoleWindow()


GWL_STYLE = -16
WS_SIZEBOX = 0x00040000  
WS_MAXIMIZEBOX = 0x00010000  


style = user32.GetWindowLongW(hWnd, GWL_STYLE)


style &= ~WS_SIZEBOX
style &= ~WS_MAXIMIZEBOX


user32.SetWindowLongW(hWnd, GWL_STYLE, style)


user32.SetWindowPos(hWnd, None, 0, 0, 0, 0, 0x0027)

init(autoreset=True)



COLOR_PRIMARY = Fore.CYAN  
COLOR_ACCENT = Fore.MAGENTA  
COLOR_INFO = Fore.BLUE  
COLOR_SUCCESS = Fore.GREEN 
COLOR_WARNING = Fore.YELLOW 
COLOR_ERROR = Fore.RED 
COLOR_TEXT = Fore.WHITE
COLOR_HIGHLIGHT = Style.BRIGHT 


BACK_PROGRESS_PC = Back.BLUE
BACK_PROGRESS_MOBILE = Back.MAGENTA

class UltimateRewardsAutomator:
    def __init__(self):
        self.edge_driver_path = self.get_edge_driver_path()
        self.driver = None
        self.mobile_driver = None
        self.wait = None
        self.mobile_wait = None
        self.searches_count = 0
        self.mobile_searches_count = 0
        self.completed_searches = set()
        self.mobile_completed_searches = set()
        self.total_pc_searches = 30
        self.total_mobile_searches = 20
        self.user_agent_mobile = "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36 EdgA/46.1.2.5140"
        self.is_headless = False
        self.accounts_dir = os.path.join(os.getcwd(), "accounts") 
        self.current_account_name = None 

        self.ensure_accounts_dir() 

    def ensure_accounts_dir(self):
        """Asegura que el directorio de cuentas exista."""
        if not os.path.exists(self.accounts_dir):
            os.makedirs(self.accounts_dir)
            print(COLOR_SUCCESS + f"✓ Directorio de cuentas creado en: {self.accounts_dir}")
            time.sleep(0.5)

    def print_header(self):
        """Muestra el encabezado principal del programa."""
        os.system('cls' if os.name == 'nt' else 'clear') 
        print(COLOR_ACCENT + r"""
                           ███▄ ▄███▓  ██████     ██▀███  ▓█████  █     █░ ▄▄▄       ██▀███  ▓█████▄   ██████
                          ▓██▒▀█▀ ██▒▒██    ▒    ▓██ ▒ ██▒▓█   ▀ ▓█░ █ ░█░▒████▄    ▓██ ▒ ██▒▒██▀ ██▌▒██    ▒
                          ▓██    ▓██░░ ▓██▄      ▓██ ░▄█ ▒▒███   ▒█░ █ ░█ ▒██  ▀█▄  ▓██ ░▄█ ▒░██   █▌░ ▓██▄
                          ▒██    ▒██   ▒   ██▒   ▒██▀▀█▄  ▒▓█  ▄ ░█░ █ ░█ ░██▄▄▄▄██ ▒██▀▀█▄  ░▓█▄   ▌  ▒   ██▒
                          ▒██▒   ░██▒▒██████▒▒   ░██▓ ▒██▒░▒████▒░░██▒██▓  ▓█   ▓██▒░██▓ ▒██▒░▒████▓ ▒██████▒▒
                          ░ ▒░   ░  ░▒ ▒▓▒ ▒ ░   ░ ▒▓ ░▒▓░░░ ▒░ ░░ ▓░▒ ▒   ▒▒   ▓▒█░░ ▒▓ ░ ▒▓░ ▒▒▓  ▒ ▒ ▒▓▒ ▒ ░
                          ░  ░      ░░ ░▒  ░ ░     ░▒ ░ ▒░ ░ ░  ░  ▒ ░ ░    ▒   ▒▒ ░  ░▒ ░ ▒░ ░ ▒  ▒ ░ ░▒  ░ ░
                          ░      ░   ░  ░  ░       ░░   ░    ░     ░   ░    ░   ▒     ░░   ░  ░ ░  ░ ░  ░  ░
                                 ░         ░        ░        ░  ░    ░          ░  ░   ░        ░          ░
                                                                    ░
        """ + Style.RESET_ALL)
        print(COLOR_SUCCESS + "   Cludy RbxTool" + Style.RESET_ALL)
        print(COLOR_SUCCESS + "  ==================" + Style.RESET_ALL)
        print("\n") 

    def show_menu(self):
        """Muestra el menú de opciones principal."""
        self.print_header()
        print(COLOR_PRIMARY + "╔═══════════════════════════════════════╗")
        print(COLOR_PRIMARY + "║        " + COLOR_TEXT + COLOR_HIGHLIGHT + "Menú Principal" + Style.NORMAL + "         " + COLOR_PRIMARY + "║")
        print(COLOR_PRIMARY + "╠═══════════════════════════════════════╣")
        print(COLOR_PRIMARY + "║ " + COLOR_ACCENT + "[1]" + COLOR_TEXT + " Búsquedas de PC solamente (Rápido)    " + COLOR_PRIMARY + "║")
        print(COLOR_PRIMARY + "║ " + COLOR_ACCENT + "[2]" + COLOR_TEXT + " Búsquedas móviles solamente             " + COLOR_PRIMARY + "║")
        print(COLOR_PRIMARY + "║ " + COLOR_ACCENT + "[3]" + COLOR_TEXT + " Búsquedas PC + Móvil (Completo)       " + COLOR_PRIMARY + "║")
        print(COLOR_PRIMARY + "╠═══════════════════════════════════════╣") # Separador visual
        print(COLOR_PRIMARY + "║ " + COLOR_ACCENT + "[4]" + COLOR_TEXT + " Configurar Opciones Avanzadas         " + COLOR_PRIMARY + "║")
        print(COLOR_PRIMARY + "║ " + COLOR_ACCENT + "[5]" + COLOR_TEXT + " Gestionar Cuentas (Login/Seleccionar) " + COLOR_PRIMARY + "║")
        print(COLOR_PRIMARY + "╠═══════════════════════════════════════╣")
        print(COLOR_PRIMARY + "║ " + COLOR_ERROR + COLOR_HIGHLIGHT + "[6]" + COLOR_TEXT + " Salir del Programa                    " + COLOR_PRIMARY + "║")
        print(COLOR_PRIMARY + "╚═══════════════════════════════════════╝\n")

        while True:
            choice = input(COLOR_WARNING + " > Ingresa tu opción [1-6]: " + Style.RESET_ALL).strip()
            if choice in ['1', '2', '3', '4', '5', '6']:
                return int(choice)
            print(COLOR_ERROR + "× Opción inválida. Por favor, ingresa un número entre 1 y 6.")
            time.sleep(1)

    def show_advanced_menu(self):
        """Muestra el menú de opciones avanzadas."""
        self.print_header()
        print(COLOR_PRIMARY + "╔═════════════════════════════════════════╗")
        print(COLOR_PRIMARY + "║        " + COLOR_TEXT + COLOR_HIGHLIGHT + "Opciones Avanzadas" + Style.NORMAL + "       " + COLOR_PRIMARY + "║")
        print(COLOR_PRIMARY + "╠═════════════════════════════════════════╣")
        print(COLOR_PRIMARY + f"║ {COLOR_ACCENT + '[1]' + COLOR_TEXT} {'DESACTIVAR' if self.is_headless else 'ACTIVAR'} modo headless (actual: {'ON' if self.is_headless else 'OFF'}){' '*(2 if self.is_headless else 1)} " + COLOR_PRIMARY + "║")
        print(COLOR_PRIMARY + f"║ {COLOR_ACCENT + '[2]' + COLOR_TEXT} Cambiar # búsquedas PC (actual: {self.total_pc_searches:2d})   " + COLOR_PRIMARY + "║")
        print(COLOR_PRIMARY + f"║ {COLOR_ACCENT + '[3]' + COLOR_TEXT} Cambiar # búsquedas móviles (actual: {self.total_mobile_searches:2d}) " + COLOR_PRIMARY + "║")
        print(COLOR_PRIMARY + "╠═════════════════════════════════════════╣")
        print(COLOR_PRIMARY + "║ " + COLOR_ERROR + COLOR_HIGHLIGHT + "[4]" + COLOR_TEXT + " Volver al Menú Principal                " + COLOR_PRIMARY + "║")
        print(COLOR_PRIMARY + "╚═════════════════════════════════════════╝\n")

        while True:
            choice = input(COLOR_WARNING + " > Ingresa tu opción [1-4]: " + Style.RESET_ALL).strip()
            if choice in ['1', '2', '3', '4']:
                return int(choice)
            print(COLOR_ERROR + "× Opción inválida. Por favor, ingresa un número entre 1 y 4.")
            time.sleep(1)

    def select_account_menu(self):
        """Permite al usuario seleccionar cuentas para ejecutar o iniciar sesión."""
        self.print_header()
        print(COLOR_PRIMARY + "╔══════════════════════════════════════════╗")
        print(COLOR_PRIMARY + "║       " + COLOR_TEXT + COLOR_HIGHLIGHT + "Gestión de Cuentas" + Style.NORMAL + "          " + COLOR_PRIMARY + "║")
        print(COLOR_PRIMARY + "╠══════════════════════════════════════════╣")
        print(COLOR_PRIMARY + "║ " + COLOR_ACCENT + "[1]" + COLOR_TEXT + " Iniciar sesión en una nueva cuenta    " + COLOR_PRIMARY + "║")
        print(COLOR_PRIMARY + "║ " + COLOR_ACCENT + "[2]" + COLOR_TEXT + " Seleccionar cuentas para ejecutar     " + COLOR_PRIMARY + "║")
        print(COLOR_PRIMARY + "╠══════════════════════════════════════════╣")
        print(COLOR_PRIMARY + "║ " + COLOR_ERROR + COLOR_HIGHLIGHT + "[3]" + COLOR_TEXT + " Volver al Menú Principal              " + COLOR_PRIMARY + "║")
        print(COLOR_PRIMARY + "╚══════════════════════════════════════════╝\n")

        while True:
            choice = input(COLOR_WARNING + " > Ingresa tu opción [1-3]: " + Style.RESET_ALL).strip()
            if choice == '1':
                account_name = input(COLOR_INFO + " > Ingresa un nombre único para la cuenta (ej. 'micuenta1' o tu email): " + Style.RESET_ALL).strip()
                if not account_name:
                    print(COLOR_ERROR + "× El nombre de la cuenta no puede estar vacío.")
                    time.sleep(1)
                    continue
                if account_name in self.get_account_names():
                    print(COLOR_WARNING + f"! La cuenta '{account_name}' ya existe. Se usará su perfil existente para iniciar sesión.")
                    time.sleep(2)
                self.login_to_bing(account_name)
                input(COLOR_WARNING + "\nPresiona Enter para continuar..." + Style.RESET_ALL)
                return [] 
            elif choice == '2':
                return self._show_run_accounts_selection()
            elif choice == '3':
                return [] 
            else:
                print(COLOR_ERROR + "× Opción inválida. Por favor, ingresa un número entre 1 y 3.")
                time.sleep(1)

    def _show_run_accounts_selection(self):
        """Muestra el menú para seleccionar cuentas para ejecutar búsquedas."""
        available_accounts = self.get_account_names()
        if not available_accounts:
            print(COLOR_WARNING + "\n! No hay cuentas configuradas aún.")
            print(COLOR_WARNING + "  Por favor, selecciona la opción [1] 'Iniciar sesión en una nueva cuenta' primero.")
            time.sleep(3)
            return []

        print(COLOR_PRIMARY + "\n╔═══════════════════════════════════════════════╗")
        print(COLOR_PRIMARY + "║       " + COLOR_TEXT + COLOR_HIGHLIGHT + "Seleccionar Cuentas a Ejecutar" + Style.NORMAL + "    " + COLOR_PRIMARY + "║")
        print(COLOR_PRIMARY + "╠═══════════════════════════════════════════════╣")
        print(COLOR_PRIMARY + "║ " + COLOR_TEXT + "Ingresa números (ej. '1,3') o 'all' para todas  " + COLOR_PRIMARY + "║")
        print(COLOR_PRIMARY + "╠═══════════════════════════════════════════════╣")
        for i, acc_name in enumerate(available_accounts):
            print(COLOR_PRIMARY + f"║   {COLOR_ACCENT}[{i+1}]{COLOR_TEXT} {acc_name:<34} " + COLOR_PRIMARY + "║")
        print(COLOR_PRIMARY + "╠═══════════════════════════════════════════════╣")
        print(COLOR_PRIMARY + "║ " + COLOR_ERROR + COLOR_HIGHLIGHT + "[0]" + COLOR_TEXT + " Volver al Menú Principal                      " + COLOR_PRIMARY + "║")
        print(COLOR_PRIMARY + "╚═══════════════════════════════════════════════╝\n")


        while True:
            selection = input(COLOR_WARNING + " > Ingresa tu selección: " + Style.RESET_ALL).strip().lower()
            if selection == '0':
                return []
            elif selection == 'all':
                print(COLOR_SUCCESS + "✓ Seleccionadas todas las cuentas disponibles.")
                time.sleep(1)
                return available_accounts
            else:
                selected_indices = []
                try:
                    parts = selection.split(',')
                    for part in parts:
                        idx = int(part.strip()) - 1
                        if 0 <= idx < len(available_accounts):
                            selected_indices.append(idx)
                        else:
                            print(COLOR_ERROR + f"× Número de cuenta '{part}' inválido. Por favor, intenta de nuevo.")
                            selected_indices = [] 
                            break
                except ValueError:
                    print(COLOR_ERROR + "× Entrada inválida. Por favor, usa números separados por coma (ej. '1,3') o escribe 'all'.")
                    time.sleep(1)
                    continue

                if selected_indices:
                    selected_final = [available_accounts[i] for i in sorted(list(set(selected_indices)))]
                    print(COLOR_SUCCESS + f"✓ Cuentas seleccionadas: {COLOR_ACCENT + ', '.join(selected_final) + COLOR_SUCCESS}")
                    time.sleep(1)
                    return selected_final
                else:
                    print(COLOR_ERROR + "× No se seleccionó ninguna cuenta válida. Intenta nuevamente.")
                    time.sleep(1)


    def login_to_bing(self, account_name):
        """
        Abre el navegador para que el usuario inicie sesión en Bing.
        Las cookies se guardarán automáticamente en el perfil de usuario.
        """
        print(COLOR_INFO + f"\n[INFO] Preparando configuración para la cuenta: '{COLOR_ACCENT + account_name + COLOR_INFO}'...")
        print(COLOR_WARNING + "╔═══════════════════════════════════════════════════════════╗")
        print(COLOR_WARNING + "║ " + COLOR_TEXT + COLOR_HIGHLIGHT + ">>> PASO IMPORTANTE: INICIO DE SESIÓN MANUAL <<<" + Style.NORMAL + "       " + COLOR_WARNING + "║")
        print(COLOR_WARNING + "╠═══════════════════════════════════════════════════════════╣")
        print(COLOR_WARNING + "║ " + COLOR_TEXT + "Se abrirá una ventana de Edge. Por favor, " + COLOR_ACCENT + "INICIA SESIÓN" + COLOR_TEXT + " " + COLOR_WARNING + "║")
        print(COLOR_WARNING + "║ " + COLOR_TEXT + "en tu cuenta de Microsoft/Bing Rewards en esa ventana." + COLOR_WARNING + "   " + COLOR_WARNING + "║")
        print(COLOR_WARNING + "║ " + COLOR_TEXT + "Una vez que veas tu saldo de puntos o el panel de" + COLOR_WARNING + "     " + COLOR_WARNING + "║")
        print(COLOR_WARNING + "║ " + COLOR_TEXT + "recompensas (rewards.bing.com), " + COLOR_ACCENT + "CIERRA" + COLOR_TEXT + " la ventana." + COLOR_WARNING + "     " + COLOR_WARNING + "║")
        print(COLOR_WARNING + "║ " + COLOR_TEXT + "¡Las credenciales se guardarán automáticamente para futuros usos! " + COLOR_WARNING + "║")
        print(COLOR_WARNING + "╚═══════════════════════════════════════════════════════════╝\n")
        time.sleep(3) 

        temp_driver = None
        try:
            options = Options()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)

            profile_path = os.path.join(self.accounts_dir, account_name)
            options.add_argument(f"user-data-dir={profile_path}")

            service = Service(executable_path=self.edge_driver_path)
            temp_driver = webdriver.Edge(service=service, options=options)

            temp_driver.get("https://rewards.bing.com/")
            print(COLOR_SUCCESS + "✓ Navegador abierto. Esperando que inicies sesión y cierres la ventana manualmente...")

            
            while True:
                try:
                    
                    temp_driver.current_url
                    time.sleep(1)
                except:
                    
                    print(COLOR_SUCCESS + "✓ Navegador cerrado. ¡Sesión guardada correctamente!")
                    break

        except Exception as e:
            print(COLOR_ERROR + f"× Error al iniciar sesión para '{account_name}': {e}")
            print(COLOR_ERROR + "  Asegúrate de que Edge y msedgedriver.exe estén actualizados.")
            time.sleep(2)
        finally:
            if temp_driver:
                try:
                    temp_driver.quit() 
                except:
                    pass

    def get_account_names(self):
        """Obtiene una lista de los nombres de las carpetas de perfiles de cuenta."""
        if not os.path.exists(self.accounts_dir):
            return []
        return [name for name in os.listdir(self.accounts_dir) if os.path.isdir(os.path.join(self.accounts_dir, name))]

    def get_edge_driver_path(self):
        """Obtiene la ruta del Edge WebDriver."""
        paths = [
            "msedgedriver.exe",
            os.path.join(os.environ.get('PROGRAMFILES', ''), "Microsoft", "Edge", "Application", "msedgedriver.exe"),
            os.path.join(os.getcwd(), "msedgedriver.exe")
        ]

        print(COLOR_INFO + "\n[INFO] Buscando msedgedriver.exe...")
        for path in paths:
            if os.path.exists(path):
                print(COLOR_SUCCESS + f"✓ Controlador de Edge encontrado en: {COLOR_ACCENT + path}")
                time.sleep(0.5)
                return path
        print(COLOR_ERROR + "× ERROR: No se encontró 'msedgedriver.exe'.")
        print(COLOR_ERROR + "  Asegúrate de que esté en la misma carpeta que este script o en tu PATH del sistema.")
        print(COLOR_ERROR + "  Puedes descargarlo desde: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/")
        sys.exit(1) 


    def setup_driver(self, mobile=False, account_name=None):
        """Configura el navegador para PC o móvil, y para una cuenta específica."""
        options = Options()

        if mobile:
            mobile_emulation = {
                "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
                "userAgent": self.user_agent_mobile
            }
            options.add_experimental_option("mobileEmulation", mobile_emulation)
            options.add_argument("--window-size=360,640")
        else:
            options.add_argument("--start-maximized")

        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        if self.is_headless:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--log-level=3") 

        if account_name:
            profile_path = os.path.join(self.accounts_dir, account_name)
            if not os.path.exists(profile_path):
                os.makedirs(profile_path) 
            options.add_argument(f"user-data-dir={profile_path}")
        else:
            
            print(COLOR_ERROR + "¡ADVERTENCIA! No se especificó un nombre de cuenta para el driver. Usando perfil genérico.")
            profile_path = os.path.join(os.getcwd(), "edge_profile_mobile" if mobile else "edge_profile_pc")
            options.add_argument(f"user-data-dir={profile_path}")

        service = Service(executable_path=self.edge_driver_path)
        driver = webdriver.Edge(service=service, options=options)

        if mobile:
            driver.execute_cdp_cmd("Network.setUserAgentOverride", {
                "userAgent": self.user_agent_mobile,
                "platform": "Android"
            })
            driver.execute_cdp_cmd("Emulation.setTouchEmulationEnabled", {
                "enabled": True,
                "configuration": "mobile"
            })

        return driver, WebDriverWait(driver, 10)

    def generate_random_term(self, mobile=False):
        """Genera términos de búsqueda aleatorios."""
        term_types = [
            lambda: ''.join(random.choices(string.ascii_lowercase, k=random.randint(4, 8))),
            lambda: ' '.join([''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 6))) for _ in range(random.randint(2, 3))]),
            lambda: str(random.randint(1000, 9999)),
            lambda: ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(5, 8))),
            lambda: f"qué es {random.choice(['inteligencia artificial', 'cuanto es 2+2', 'noticias de hoy', 'cambio climático', 'historia de españa', 'geografía mundial'])}",
            lambda: f"cómo hacer {random.choice(['pasta carbonara', 'un pastel de chocolate', 'un programa en python', 'meditación', 'un nudo marinero', 'un buen café'])}",
            lambda: f"{random.choice(['películas', 'libros', 'series'])} de {random.choice(['acción', 'ciencia ficción', 'comedia', 'drama', 'terror', 'animación'])}",
            lambda: f"capital de {random.choice(['francia', 'españa', 'italia', 'japón', 'canadá', 'alemania', 'méxico', 'argentina', 'colombia', 'perú'])}",
            lambda: f"recetas de {random.choice(['pollo', 'verduras', 'postres', 'sopas', 'ensaladas'])}",
            lambda: f"deportes {random.choice(['fútbol', 'baloncesto', 'tenis', 'natación', 'ciclismo'])}",
            lambda: f"personaje famoso {random.choice(['leonardo da vinci', 'marie curie', 'albert einstein', 'nelson mandela', 'frida kahlo', 'stephen hawking'])}",
            lambda: f"información sobre {random.choice(['agujeros negros', 'energía renovable', 'nanotecnología', 'blockchain', 'realidad virtual', 'criptomonedas'])}",
            lambda: f"significado de la palabra {random.choice(['serendipia', 'efímero', 'ubicuidad', 'melancolía', 'resiliencia', 'quimera'])}",
            lambda: f"últimos avances en {random.choice(['medicina', 'tecnología espacial', 'robótica', 'genética', 'inteligencia artificial'])}",
            lambda: f"clima en {random.choice(['madrid', 'barcelona', 'buenos aires', 'ciudad de méxico', 'lima', 'bogotá', 'santiago de chile', 'quito', 'nueva york', 'londres'])}"
        ]

        search_set = self.mobile_completed_searches if mobile else self.completed_searches

        attempts = 0
        max_attempts = 100 
        while attempts < max_attempts:
            term = random.choice(term_types)()
            if term not in search_set:
                search_set.add(term)
                return term
            attempts += 1
        
        return random.choice(term_types)()


    def perform_search(self, term, mobile=False):
        """Realiza una búsqueda en PC o móvil."""
        driver = self.mobile_driver if mobile else self.driver
        wait = self.mobile_wait if mobile else self.wait

        try:
            if mobile:
                driver.get(f"https://www.bing.com/search?q={term}&form=QBLH&qs=MB")
                try:

                    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

                except:
                    print(COLOR_WARNING + "\n  ! Advertencia: No se pudo verificar la carga de la página móvil o el diseño esperado.")
                    self.adjust_mobile_settings() 
                    return False
                self.mobile_searches_count += 1
                wait_time = random.uniform(2.5, 5.0) 

            else: # PC
                driver.get("https://www.bing.com/")
                search_input = wait.until(EC.presence_of_element_located((By.ID, "sb_form_q")))
                search_input.clear()
                search_input.send_keys(term)
                search_input.send_keys(Keys.ENTER)
                self.searches_count += 1
                wait_time = random.uniform(2.0, 4.0) 

            time.sleep(wait_time)
            return True

        except Exception as e:
            print(COLOR_ERROR + f"\n× Error en búsqueda {'móvil' if mobile else 'PC'} para '{self.current_account_name}': {str(e)[:150]}...")
            print(COLOR_ERROR + "  Intentando reintentar la búsqueda...")
            return False

    def adjust_mobile_settings(self):
        """Ajusta la configuración móvil dinámicamente."""
        if not self.mobile_driver:
            return

        try:
            self.mobile_driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
                "width": 360,
                "height": 640,
                "deviceScaleFactor": 3,
                "mobile": True
            })
            print(COLOR_SUCCESS + "  ✓ Configuración móvil reajustada.")
        except Exception as e:
            print(COLOR_ERROR + f"× Error al reajustar configuración móvil: {str(e)}")

    def run_pc_searches(self):
        """Ejecuta búsquedas de PC optimizadas."""
        print(COLOR_INFO + f"\n[INFO] Iniciando búsquedas de PC para '{COLOR_ACCENT + self.current_account_name + COLOR_INFO}'..." + Style.RESET_ALL)
        start_time = time.time()
        self.searches_count = 0 
        self.completed_searches.clear() 

        try:
            self.driver, self.wait = self.setup_driver(mobile=False, account_name=self.current_account_name)

            while self.searches_count < self.total_pc_searches:
                term = self.generate_random_term(mobile=False)

                
                sys.stdout.write(
                    f"\r{COLOR_TEXT + BACK_PROGRESS_PC} Búsquedas PC: {self.searches_count + 1:2d}/{self.total_pc_searches:2d} "
                    f"{COLOR_TEXT + BACK_PROGRESS_PC}| Término: '{term:<30}' {Style.RESET_ALL}" # Alinear para que no salte el texto
                )
                sys.stdout.flush()

                if self.perform_search(term, mobile=False):
                    pass 
                else:
                    print(COLOR_WARNING + "  ! Reintentando la búsqueda de PC...")
                    time.sleep(2) 
                    
                    continue 

                if self.searches_count < self.total_pc_searches: 
                    delay = random.uniform(3.0, 6.0) 
                    time.sleep(delay)

            total_time = time.time() - start_time
            
            print(f"\r{COLOR_SUCCESS}✓ Búsquedas PC completadas para '{COLOR_ACCENT + self.current_account_name + COLOR_SUCCESS}': {self.searches_count}/{self.total_pc_searches}{' '*20}")
            print(COLOR_WARNING + f"  Tiempo total en PC: {total_time:.1f} segundos")

        except Exception as e:
            print(COLOR_ERROR + f"\n× ERROR en búsquedas PC para '{COLOR_ACCENT + self.current_account_name + COLOR_ERROR}': {str(e)}")
            print(COLOR_ERROR + "  Por favor, verifica tu conexión a internet o el estado del navegador.")
        finally:
            if self.driver:
                self.driver.quit()
                self.driver = None
                print(COLOR_INFO + "  Navegador Edge (PC) cerrado." + Style.RESET_ALL)


    def run_mobile_searches(self):
        """Ejecuta búsquedas móviles con verificación mejorada."""
        print(COLOR_INFO + f"\n[INFO] Iniciando búsquedas móviles para '{COLOR_ACCENT + self.current_account_name + COLOR_INFO}'..." + Style.RESET_ALL)
        start_time = time.time()
        self.mobile_searches_count = 0 
        self.mobile_completed_searches.clear() 

        try:
            self.mobile_driver, self.mobile_wait = self.setup_driver(mobile=True, account_name=self.current_account_name)

            self.mobile_driver.get("https://www.bing.com/?mobile=1")
            time.sleep(2)
            if "mobile" not in self.mobile_driver.current_url.lower() and not self.is_headless:
                print(COLOR_WARNING + "  ! Ajustando configuración para móvil (la URL no parece móvil)...")
                self.adjust_mobile_settings()
                time.sleep(1) 

            while self.mobile_searches_count < self.total_mobile_searches:
                term = self.generate_random_term(mobile=True)

                
                sys.stdout.write(
                    f"\r{COLOR_TEXT + BACK_PROGRESS_MOBILE} Búsquedas Móvil: {self.mobile_searches_count + 1:2d}/{self.total_mobile_searches:2d} "
                    f"{COLOR_TEXT + BACK_PROGRESS_MOBILE}| Término: '{term:<30}' {Style.RESET_ALL}" 
                )
                sys.stdout.flush()

                if self.perform_search(term, mobile=True):
                    pass 
                else:
                    print(COLOR_WARNING + "  ! Reintentando la búsqueda móvil...")
                    time.sleep(2) 
                    self.adjust_mobile_settings()
                    continue 

                if self.mobile_searches_count < self.total_mobile_searches: 
                    delay = random.uniform(4.0, 8.0) 
                    time.sleep(delay)

            total_time = time.time() - start_time
            
            print(f"\r{COLOR_SUCCESS}✓ Búsquedas móviles completadas para '{COLOR_ACCENT + self.current_account_name + COLOR_SUCCESS}': {self.mobile_searches_count}/{self.total_mobile_searches}{' '*20}")
            print(COLOR_WARNING + f"  Tiempo total en Móvil: {total_time:.1f} segundos")

        except Exception as e:
            print(COLOR_ERROR + f"\n× ERROR general en búsquedas móviles para '{COLOR_ACCENT + self.current_account_name + COLOR_ERROR}': {str(e)}")
            print(COLOR_ERROR + "  Por favor, verifica tu conexión a internet o el estado del navegador móvil.")
        finally:
            if self.mobile_driver:
                self.mobile_driver.quit()
                self.mobile_driver = None
                print(COLOR_INFO + "  Navegador Edge (Móvil) cerrado." + Style.RESET_ALL)


    def run_for_account(self, account_name, mode):
        """Ejecuta las búsquedas para una cuenta específica y modo dado."""
        self.current_account_name = account_name 
        

        print(COLOR_PRIMARY + f"\n\n╔═══════════════════════════════════════════════╗")
        print(COLOR_PRIMARY + f"║ {COLOR_TEXT + COLOR_HIGHLIGHT}INICIANDO BÚSQUEDAS PARA LA CUENTA:{COLOR_ACCENT + Style.BRIGHT} {account_name.upper():<16} {COLOR_PRIMARY}║")
        print(COLOR_PRIMARY + f"╚═══════════════════════════════════════════════╝\n" + Style.RESET_ALL)
        account_start_time = time.time()
        time.sleep(1) 

        try:
            if mode in [1, 3]:  
                self.run_pc_searches()

            if mode in [2, 3]: 
                self.run_mobile_searches()

        except KeyboardInterrupt:
            print(COLOR_ERROR + f"\n! Ejecución interrumpida por el usuario para la cuenta {COLOR_WARNING + self.current_account_name}")
        finally:
            account_total_time = time.time() - account_start_time
            print(COLOR_PRIMARY + f"\n╔═══════════════════════════════════════════════╗")
            print(COLOR_PRIMARY + f"║ {COLOR_TEXT}Resumen para '{COLOR_ACCENT + self.current_account_name + COLOR_TEXT}':{' '*(29 - len(self.current_account_name))}║")
            print(COLOR_PRIMARY + f"║ {COLOR_SUCCESS}  Tiempo total de ejecución: {account_total_time:.1f} segundos{' '*(11 if account_total_time < 100 else 10)}║")
            print(COLOR_PRIMARY + f"╚═══════════════════════════════════════════════╝" + Style.RESET_ALL)
            time.sleep(2) 

    def run(self):
        """Ejecuta el automator según la selección del usuario."""
        while True:
            choice = self.show_menu()

            if choice == 6: 
                print(COLOR_WARNING + "\nSaliendo del programa... ¡Hasta pronto!")
                print(COLOR_PRIMARY + "==============================================\n")
                time.sleep(1)
                return
            elif choice == 4: 
                self.configure_advanced_options()
                continue
            elif choice == 5: 
                self.select_account_menu()
                continue 

           
            selected_accounts = self._show_run_accounts_selection()
            if not selected_accounts:
                print(COLOR_WARNING + "\n! No se seleccionaron cuentas para ejecutar. Volviendo al menú principal.")
                time.sleep(2)
                continue

            overall_start_time = time.time()
            for account_name in selected_accounts:
                self.run_for_account(account_name, choice)

            overall_total_time = time.time() - overall_start_time
            if len(selected_accounts) > 1:
                print(COLOR_SUCCESS + f"\n╔═══════════════════════════════════════════════╗")
                print(COLOR_SUCCESS + f"║ {COLOR_TEXT}¡Todas las cuentas procesadas! {COLOR_ACCENT}Tiempo Total General: {overall_total_time:.1f}s {COLOR_SUCCESS}║")
                print(COLOR_SUCCESS + f"╚═══════════════════════════════════════════════╝")
            else:
                print(COLOR_SUCCESS + f"\n✓ Búsquedas completadas para la cuenta seleccionada.")


            input(COLOR_WARNING + "\nPresiona Enter para continuar..." + Style.RESET_ALL)


    def configure_advanced_options(self):
        """Configura opciones avanzadas."""
        while True:
            choice = self.show_advanced_menu()

            if choice == 1:
                self.is_headless = not self.is_headless
                print(COLOR_SUCCESS + f"✓ Modo headless {'activado' if self.is_headless else 'desactivado'}")
                time.sleep(1)
            elif choice == 2:
                while True:
                    try:
                        new_count = int(input(COLOR_INFO + f" > Ingresa el nuevo número de búsquedas PC (actual: {self.total_pc_searches}): " + Style.RESET_ALL))
                        if new_count > 0:
                            self.total_pc_searches = new_count
                            print(COLOR_SUCCESS + f"✓ Número de búsquedas PC actualizado a {self.total_pc_searches}.")
                            time.sleep(1)
                            break
                        else:
                            print(COLOR_ERROR + "× El número debe ser mayor que cero.")
                    except ValueError:
                        print(COLOR_ERROR + "× Entrada inválida. Por favor, ingresa un número entero.")
                    time.sleep(1)
            elif choice == 3:
                while True:
                    try:
                        new_count = int(input(COLOR_INFO + f" > Ingresa el nuevo número de búsquedas móviles (actual: {self.total_mobile_searches}): " + Style.RESET_ALL))
                        if new_count > 0:
                            self.total_mobile_searches = new_count
                            print(COLOR_SUCCESS + f"✓ Número de búsquedas móviles actualizado a {self.total_mobile_searches}.")
                            time.sleep(1)
                            break
                        else:
                            print(COLOR_ERROR + "× El número debe ser mayor que cero.")
                    except ValueError:
                        print(COLOR_ERROR + "× Entrada inválida. Por favor, ingresa un número entero.")
                    time.sleep(1)
            elif choice == 4:
                return


if __name__ == "__main__":
    automator = UltimateRewardsAutomator()
    automator.run()