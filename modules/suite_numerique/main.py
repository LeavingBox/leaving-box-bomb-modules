from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from modules.suite_numerique import suite_numerique


class GameLayout(BoxLayout):

    def generate_code(self):
        serial = self.ids.serial.text
        ram = int(self.ids.ram.text)

        try:
            code = suite_numerique(serial, ram)
            self.ids.result.text = f"Code : {code}"
        except Exception:
            self.ids.result.text = "Erreur de saisie"


class SuiteNumeriqueApp(App):
    def build(self):
        return GameLayout()


if __name__ == "__main__":
    SuiteNumeriqueApp().run()
