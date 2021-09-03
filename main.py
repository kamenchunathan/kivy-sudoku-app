from kivymd.app import MDApp
from kivymd.uix.label import MDLabel


class MyApp(MDApp):
    def build(self, **kwargs):
        return MDLabel(
            text='Hello World',
            halign='center'
        )


if __name__ == '__main__':
    MyApp().run()
