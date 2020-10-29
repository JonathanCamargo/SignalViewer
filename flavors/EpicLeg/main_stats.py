from kivy.app import App

from kivy.properties import ObjectProperty

from statslayout.statslayout import StatsLayout


class main_statsApp(App):
    gui=ObjectProperty(StatsLayout)
    def build(self):
        self.gui =StatsLayout()
        return self.gui
    def on_start(self):
        pass
    def on_pause(self):
        #To do: save your work here resume is not guaranteed
        pass
    def on_resume(self):
        #To do: app is back alive
        pass

    def build_config(self,config):
        config.setdefaults('section1',{
        'Key1':'12',
        'key2':'42'
        })

    def build_settings(self,settings):
        settings.add_json_panel('Settings', self.config,'settings/signals.json')

if __name__ == '__main__':
    main_statsApp().run()
