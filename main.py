import threading
import os
import requests
from kivy.lang import Builder
from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock

# Permissions (Android 10+ Compatible)
if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([
        Permission.INTERNET,
        Permission.READ_EXTERNAL_STORAGE,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.CAMERA,
        Permission.RECORD_AUDIO
    ])

# MediaPipe Safe Import
MEDIAPIPE_READY = False
try:
    from mediapipe.tasks.python.genai import LlmInference, LlmInferenceOptions
    MEDIAPIPE_READY = True
except ImportError:
    print("MediaPipe Library not found or incompatible.")

KV = '''
<ChatMessage@MDBoxLayout>:
    adaptive_height: True
    orientation: 'vertical'
    padding: dp(10)
    spacing: dp(5)

    MDLabel:
        text: root.sender
        theme_text_color: "Secondary"
        font_style: "Caption"
        size_hint_y: None
        height: self.texture_size[1]

    MDLabel:
        text: root.text
        theme_text_color: "Primary"
        size_hint_y: None
        height: self.texture_size[1]
        text_size: self.width, None

<HomeScreen>:
    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "Poco Gemma AI"
            right_action_items: [["cog", lambda x: app.open_settings()]]

        ScrollView:
            MDBoxLayout:
                id: chat_list
                orientation: 'vertical'
                adaptive_height: True
                padding: dp(10)
                spacing: dp(10)

        MDBoxLayout:
            adaptive_height: True
            padding: dp(10)
            spacing: dp(10)
            md_bg_color: 0.95, 0.95, 0.95, 1

            MDSwitch:
                id: net_switch
                active: False
                width: dp(40)
            
            MDLabel:
                text: "Web"
                size_hint_x: None
                width: dp(40)
                valign: "center"

            MDTextField:
                id: user_input
                hint_text: "Ask Local AI..."
                mode: "round"
                multiline: False

            MDIconButton:
                icon: "send"
                on_release: app.send_message()

<SettingsScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)

        MDTopAppBar:
            title: "Settings"
            left_action_items: [["arrow-left", lambda x: app.close_settings()]]

        MDTextField:
            id: api_key
            hint_text: "Google Search API Key"

        MDTextField:
            id: cx_id
            hint_text: "Search Engine ID (CX)"

        MDTextField:
            id: model_path
            hint_text: "Model Path (.bin)"
            text: "/sdcard/Download/gemma.bin"

        MDRaisedButton:
            text: "Save Configuration"
            pos_hint: {"center_x": .5}
            on_release: app.save_settings()

        Widget:
'''

class ChatMessage(MDBoxLayout):
    text = StringProperty()
    sender = StringProperty()

class HomeScreen(MDScreen):
    pass

class SettingsScreen(MDScreen):
    pass

class GenAIApp(MDApp):
    store = JsonStore('config.json')
    llm = None

    def build(self):
        self.theme_cls.primary_palette = "Indigo"
        self.sm = MDScreenManager()
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(SettingsScreen(name='settings'))
        return self.sm

    def on_start(self):
        # Load settings
        if self.store.exists('settings'):
            cfg = self.store.get('settings')
            self.api_key = cfg.get('api_key', '')
            self.cx_id = cfg.get('cx_id', '')
            model_path = cfg.get('model_path', '/sdcard/Download/gemma.bin')
            threading.Thread(target=self.load_model, args=(model_path,), daemon=True).start()
        else:
            self.open_settings()

    def load_model(self, path):
        if not MEDIAPIPE_READY:
            Clock.schedule_once(lambda x: self.add_chat("System", "MediaPipe lib not compatible with this Android build."))
            return

        if not os.path.exists(path):
            Clock.schedule_once(lambda x: self.add_chat("System", f"Model file missing at: {path}"))
            return

        try:
            options = LlmInferenceOptions(
                model_path=path,
                max_tokens=512,
                top_k=40,
                temperature=0.7
            )
            self.llm = LlmInference.create_from_options(options)
            Clock.schedule_once(lambda x: self.add_chat("System", "Gemma Model Loaded Locally!"))
        except Exception as e:
            Clock.schedule_once(lambda x: self.add_chat("System", f"Model Load Failed: {e}"))

    def send_message(self):
        screen = self.sm.get_screen('home')
        query = screen.ids.user_input.text
        use_web = screen.ids.net_switch.active
        
        if not query: return
        
        self.add_chat("You", query)
        screen.ids.user_input.text = ""
        
        threading.Thread(target=self.process_query, args=(query, use_web)).start()

    def process_query(self, query, use_web):
        context = ""
        if use_web:
            context = self.web_search(query)
        
        prompt = f"{context}\nUser: {query}\nAI:"
        
        if self.llm:
            try:
                response = self.llm.generate(prompt)
                Clock.schedule_once(lambda x: self.add_chat("Gemma", response))
            except Exception as e:
                Clock.schedule_once(lambda x: self.add_chat("Error", str(e)))
        else:
            Clock.schedule_once(lambda x: self.add_chat("Bot", "AI not loaded. Check model path."))

    def web_search(self, query):
        if not hasattr(self, 'api_key') or not self.api_key:
            return "[No API Key]"
        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {'q': query, 'key': self.api_key, 'cx': self.cx_id}
            data = requests.get(url, params=params).json()
            snippets = [item.get('snippet','') for item in data.get('items', [])[:2]]
            return "Web Context: " + " ".join(snippets)
        except:
            return "[Search Failed]"

    def add_chat(self, sender, text):
        screen = self.sm.get_screen('home')
        msg = ChatMessage(sender=sender, text=str(text))
        screen.ids.chat_list.add_widget(msg)

    def open_settings(self):
        self.sm.current = 'settings'

    def close_settings(self):
        self.sm.current = 'home'

    def save_settings(self):
        screen = self.sm.get_screen('settings')
        api = screen.ids.api_key.text
        cx = screen.ids.cx_id.text
        path = screen.ids.model_path.text
        
        self.store.put('settings', api_key=api, cx_id=cx, model_path=path)
        self.api_key = api
        self.cx_id = cx
        threading.Thread(target=self.load_model, args=(path,), daemon=True).start()
        self.close_settings()

if __name__ == '__main__':
    GenAIApp().run()
