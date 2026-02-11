"""
HybridAI - Multimodal AI Assistant
===================================
Hybrid AI App combining Local LLM (Gemma 2B Int4) with Internet Search.
Optimized for Poco M6 Plus (Snapdragon 4 Gen 2).

Features:
- Local LLM inference via MediaPipe GenAI (Gemma 2B int4)
- Internet search via Google Custom Search API
- Camera capture for multimodal input
- Voice input via microphone
- Persistent settings via JsonStore
- Robust error handling for graceful degradation
"""

import os
import sys
import json
import time
import threading
import traceback
from pathlib import Path
from functools import partial

# ──────────────────────────────────────────────
# SAFE IMPORTS WITH FALLBACK
# ──────────────────────────────────────────────

# Core Kivy - These MUST work or the app can't start at all
from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.metrics import dp, sp
from kivy.properties import (
    StringProperty, BooleanProperty, NumericProperty,
    ListProperty, ObjectProperty, DictProperty
)
from kivy.storage.jsonstore import JsonStore
from kivy.utils import platform
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image as KivyImage
from kivy.core.image import Image as CoreImage

# KivyMD imports
try:
    from kivymd.app import MDApp
    from kivymd.uix.screen import MDScreen
    from kivymd.uix.screenmanager import MDScreenManager
    from kivymd.uix.toolbar import MDTopAppBar
    from kivymd.uix.button import (
        MDRaisedButton, MDFlatButton, MDIconButton,
        MDFillRoundFlatButton, MDFloatingActionButton,
        MDRoundFlatIconButton
    )
    from kivymd.uix.textfield import MDTextField
    from kivymd.uix.label import MDLabel, MDIcon
    from kivymd.uix.card import MDCard
    from kivymd.uix.dialog import MDDialog
    from kivymd.uix.list import (
        MDList, OneLineListItem, TwoLineListItem,
        ThreeLineListItem, OneLineIconListItem,
        TwoLineIconListItem, IconLeftWidget
    )
    from kivymd.uix.selectioncontrol import MDSwitch, MDCheckbox
    from kivymd.uix.menu import MDDropdownMenu
    from kivymd.uix.snackbar import Snackbar
    from kivymd.uix.spinner import MDSpinner
    from kivymd.uix.tab import MDTabs, MDTabsBase
    from kivymd.uix.boxlayout import MDBoxLayout
    from kivymd.uix.floatlayout import MDFloatLayout
    from kivymd.uix.gridlayout import MDGridLayout
    from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
    from kivymd.toast import toast as md_toast
    KIVYMD_AVAILABLE = True
    Logger.info("HybridAI: KivyMD loaded successfully")
except ImportError as e:
    KIVYMD_AVAILABLE = False
    Logger.error(f"HybridAI: KivyMD import failed: {e}")
    sys.exit("KivyMD is required. Cannot continue.")

# ──────────────────────────────────────────────
# MEDIAPIPE - WRAPPED IN TRY/EXCEPT (CRITICAL)
# This is the most fragile import. On some devices,
# the native .so libraries may fail to load.
# ──────────────────────────────────────────────
MEDIAPIPE_AVAILABLE = False
LlmInference = None
MEDIAPIPE_ERROR = ""

try:
    from mediapipe.tasks.python.genai import llm_inference
    LlmInference = llm_inference.LlmInference
    MEDIAPIPE_AVAILABLE = True
    Logger.info("HybridAI: MediaPipe LLM loaded successfully")
except ImportError as e:
    MEDIAPIPE_ERROR = f"ImportError: {e}"
    Logger.warning(f"HybridAI: MediaPipe import failed: {e}")
    Logger.warning("HybridAI: Local LLM will be UNAVAILABLE")
except Exception as e:
    MEDIAPIPE_ERROR = f"Exception: {e}"
    Logger.error(f"HybridAI: MediaPipe load error: {e}")
    Logger.error(traceback.format_exc())

# ──────────────────────────────────────────────
# REQUESTS - For Internet Search
# ──────────────────────────────────────────────
REQUESTS_AVAILABLE = False
try:
    import requests
    REQUESTS_AVAILABLE = True
    Logger.info("HybridAI: requests library loaded")
except ImportError:
    Logger.warning("HybridAI: requests not available, internet search disabled")

# ──────────────────────────────────────────────
# NUMPY - For potential data processing
# ──────────────────────────────────────────────
NUMPY_AVAILABLE = False
try:
    import numpy as np
    NUMPY_AVAILABLE = True
    Logger.info("HybridAI: numpy loaded")
except ImportError:
    Logger.warning("HybridAI: numpy not available")

# ──────────────────────────────────────────────
# ANDROID-SPECIFIC IMPORTS
# ──────────────────────────────────────────────
ANDROID_AVAILABLE = False
android_permissions = None
android_activity = None

if platform == "android":
    try:
        from android.permissions import request_permissions, Permission, check_permission
        from android.storage import primary_external_storage_path, app_storage_path
        from android import activity as android_activity_module
        from jnius import autoclass, cast
        android_permissions = {
            "INTERNET": Permission.INTERNET,
            "CAMERA": Permission.CAMERA,
            "RECORD_AUDIO": Permission.RECORD_AUDIO,
            "READ_STORAGE": Permission.READ_EXTERNAL_STORAGE,
            "WRITE_STORAGE": Permission.WRITE_EXTERNAL_STORAGE,
        }
        ANDROID_AVAILABLE = True
        Logger.info("HybridAI: Android modules loaded")
    except ImportError as e:
        Logger.warning(f"HybridAI: Android imports failed: {e}")

# ──────────────────────────────────────────────
# PLYER - Cross-platform hardware access
# ──────────────────────────────────────────────
PLYER_AVAILABLE = False
plyer_camera = None
plyer_tts = None
plyer_stt = None
plyer_vibrator = None

try:
    from plyer import camera as plyer_camera_module
    from plyer import tts as plyer_tts_module
    from plyer import vibrator as plyer_vibrator_module
    plyer_camera = plyer_camera_module
    plyer_tts = plyer_tts_module
    plyer_vibrator = plyer_vibrator_module
    PLYER_AVAILABLE = True
    Logger.info("HybridAI: Plyer loaded")
except ImportError as e:
    Logger.warning(f"HybridAI: Plyer import partial: {e}")

# ──────────────────────────────────────────────
# CONSTANTS
# ──────────────────────────────────────────────
APP_NAME = "HybridAI"
APP_VERSION = "1.0.0"

# Model paths (user must place model file here)
DEFAULT_MODEL_DIR = "/sdcard/Download/"
DEFAULT_MODEL_NAME = "gemma-2b-it-gpu-int4.bin"
SETTINGS_FILE = "hybridai_settings.json"

# Google Custom Search API (user configures in settings)
DEFAULT_SEARCH_API_KEY = ""
DEFAULT_SEARCH_ENGINE_ID = ""
GOOGLE_SEARCH_URL = "https://www.googleapis.com/customsearch/v1"

# LLM Configuration
DEFAULT_MAX_TOKENS = 512
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_K = 40
DEFAULT_TOP_P = 0.9

# Chat History
MAX_CHAT_HISTORY = 100

# ──────────────────────────────────────────────
# KV 
