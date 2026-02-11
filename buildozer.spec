[app]

# (str) Title of your application
title = PocoGemma

# (str) Package name
package.name = pocogemma

# (str) Package domain (needed for android/ios packaging)
package.domain = org.ai

# (str) Source code where the main.py live
source.dir = .

# (str) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,json

# (str) Application versioning
version = 1.0

# (list) Application requirements
# YAHAN HAI MAGIC: Humne versions fix kar diye hain taaki error na aaye.
# mediapipe-genai specific package hai LLM ke liye.
requirements = python3==3.10.12,kivy==2.3.0,kivymd==1.2.0,requests,numpy,mediapipe

# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,CAMERA,RECORD_AUDIO,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target Android API (Android 14/15 ready)
android.api = 34

# (int) Minimum API (Android 7+)
android.minapi = 24

# (bool) If True, then skip trying to update the Android sdk
android.skip_update = False

# (bool) If True, process some hidden android imports
android.accept_sdk_license = True

# (str) The format used to package the app for release mode (aab or apk or aar).
android.release_artifact = apk

# (str) The format used to package the app for debug mode (apk or aar).
android.debug_artifact = apk

# (str) Bootstrap to use for android builds
p4a.branch = master

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
