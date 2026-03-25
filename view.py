import flet as ft

class View(object):
    def __init__(self, page: ft.Page):
        # Page
        self.page = page
        self.page.title = "TdP 2024 - Lab 04 - SpellChecker ++" #titolo
        self.page.horizontal_alignment = 'CENTER'
        self.page.theme_mode = ft.ThemeMode.LIGHT #cambio tema
        # Controller
        self.__controller = None
        # UI elements
        self.__title = None
        self.__theme_switch = None

        # define the UI elements and populate the page

    def add_content(self):
        """Function that creates and adds the visual elements to the page. It also updates
        the page accordingly."""
        # title + theme switch
        self.__title = ft.Text("TdP 2024 - Lab 04 - SpellChecker ++", size=24, color="blue")
        self.__theme_switch = ft.Switch(label="Light theme", on_change=self.theme_changed)
        self.page.controls.append(
            ft.Row(spacing=30, controls=[self.__theme_switch, self.__title, ],
                   alignment=ft.MainAxisAlignment.START)
        )

        # Dropdown lingua, fa scegliere all'utente la lingua
        self.__dd_language = ft.Dropdown(label="Lingua",
                                         options=[ft.dropdown.Option("italian"), ft.dropdown.Option("english"),
                                                  ft.dropdown.Option("spanish")],
                                         value="italian")

        # Dropdown modalità
        self.__dd_mode = ft.Dropdown(label = "Modalità",
                                    options = [ft.dropdown.Option("Default"), ft.dropdown.Option("Linear"), ft.dropdown.Option("Dichotomic")],
                                    value = "Default")

        # Spazio dove l'utente inserisce il testo
        self._txt_input = ft.TextField(label = "Inserisci frase", width = 500)

        # creo bottone con la funzione correzione ortografica collegata
        self._btn_check = ft.ElevatedButton(text="Check", on_click = self.handle_check)

        # spazio output dove mostro parole errate e tempo
        self._lvOut = ft.ListView(expand=True)

        # impilo gli elementi verticalmente
        self.page.controls.append(ft.Column([self.__dd_language, self.__dd_mode, self._txt_input, self._btn_check, self._lvOut]))

        self.page.update()

    def handle_check(self, e):
        # prendo i dati leggendo ciò che ha scritto l'utente
        txt = self._txt_input.value
        language = self.__dd_language.value
        mode = self.__dd_mode.value

        # evito errori come imput vuoti o spazi
        if txt is None or txt.strip() == "":
            self._lvOut.controls.clear()
            self._lvOut.controls.append(ft.Text("Inserisci una frase"))
            self.update()
            return

        # chiamo il controller ( pulizia testo, split parole, scelta algoritmo, ricerca, tempo)
        # il controller restituisce stringa di parole sbagliate e tempo (dal return nella sua funzione)
        parole_errate, tempo = self.__controller.handleSentence(txt, language, mode)

        # mostro il risultato
        self._lvOut.controls.clear()

        self._lvOut.controls.append(ft.Text(f"Frase: {txt}"))
        self._lvOut.controls.append(ft.Text(f"Parole errate: {parole_errate}"))
        self._lvOut.controls.append(ft.Text(f"Tempo: {tempo:.6f} sec", color = "green"))

        self.page.update()


    def update(self):
        self.page.update()
    def setController(self, controller):
        self.__controller = controller
    def theme_changed(self, e):
        """Function that changes the color theme of the app, when the corresponding
        switch is triggered"""
        self.page.theme_mode = (
            ft.ThemeMode.DARK
            if self.page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        self.__theme_switch.label = (
            "Light theme" if self.page.theme_mode == ft.ThemeMode.LIGHT else "Dark theme"
        )
        # self.__txt_container.bgcolor = (
        #     ft.colors.GREY_900 if self.page.theme_mode == ft.ThemeMode.DARK else ft.colors.GREY_300
        # )
        self.page.update()
