[app]

# (str) Title of your application
title = HybridAI

# (str) Package name
package.name = hybridai

# (str) Package domain (needed for android/ios packaging)
package.domain = org.hybridai

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json,bin,tflite

# (list) List of inclusions using pattern matching
source.include_patterns = assets/*,images/*,models/*

# (list) Source files to exclude (let empty to not exclude anything)
source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
source.exclude_dirs = tests,bin,venv,.git,.github,__pycache__

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
# CRITICAL: Order matters. pillow must come before kivy for image support.
requirements = python3==3.11.6,hostpython3==3.11.6,kivy==2.3.0,kivymd==1.2.0,materialyou,mediapipe,numpy,requests,urllib3,charset-normalizer,idna,certifi,pillow,plyer,pyjnius,android,openssl

# (str) Custom source folders for requirements
# Sets custom recipe paths if you need overrides
# requirements.source.mediapipe = ./recipes/mediapipe

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (int) Target Android API, should be as high as possible.
android.api = 34

# (int) Minimum API your APK / AAB will support.
android.minapi = 26

# (int) Android SDK version to use
android.sdk = 34

# (str) Android NDK version to use
android.ndk = 25b

# (int) Android NDK API to use. This is the minimum API your app will support.
android.ndk_api = 26

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# CRITICAL: MediaPipe C++ native libraries ONLY support 64-bit ARM.
# Building for armeabi-v7a WILL fail with linker errors.
# DO NOT add armeabi-v7a here under any circumstances.
android.archs = arm64-v8a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) Android entry point, default is ok for Kivy-based app
# android.entrypoint = org.kivy.android.PythonActivity

# (str) Full name including package path of the Java class that implements
# @android.activity = org.kivy.android.PythonActivity

# (list) Permissions - CRITICAL for camera, mic, storage, and network access
android.permissions = INTERNET,ACCESS_NETWORK_STATE,CAMERA,RECORD_AUDIO,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,READ_MEDIA_IMAGES,READ_MEDIA_VIDEO,READ_MEDIA_AUDIO,MANAGE_EXTERNAL_STORAGE,WAKE_LOCK,FOREGROUND_SERVICE

# (list) features (adds uses-feature -loss-)
android.features = android.hardware.camera,android.hardware.camera.autofocus

# (int) overrides automatic versionCode computation (used in determine android versionCode)
# android.numeric_version = 1

# (bool) Use --hierarchical-resource-flags (default false)
# android.use_resource_flags = 0

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Android logcat only display log for activity's pid
android.logcat_id = 0

# (str) Android additional adb arguments
# android.adb_args = -H host.docker.internal

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (bool) enables AndroidX support. Enable when targeting api 31+
android.enable_androidx = True

# (bool) Accept SDK license agreements automatically
android.accept_sdk_license = True

# (str) The format used to package the app for release mode (aab or apk or aar).
android.release_artifact = apk

# (str) The format used to package the app for debug mode (apk or aar).
android.debug_artifact = apk

# (list) The Android meta-data to set (key=value format)
# android.meta_data =

# (bool) If True, the APK will contain the compiled .pyo files.
android.no_compile_pyo = 0

# (list) Java classes to add as activities to the manifest
# android.add_activities = com.example.ExampleActivity

# (str) Gradle dependencies to add
android.gradle_dependencies = com.google.mediapipe:tasks-genai:0.10.14,com.google.android.material:material:1.11.0,androidx.core:core:1.12.0,androidx.appcompat:appcompat:1.6.1

# (bool) Enable AndroidManifest.xml additions
# android.add_manifest_xml = ./extras/AndroidManifest_additions.xml

# (list) add java compile options
# android.add_compile_options = "sourceCompatibility = 1.8", "targetCompatibility = 1.8"

# (list) Gradle repositories to add {can be necessary for} some dependencies
android.add_gradle_repositories = google(),mavenCentral(),maven { url 'https://dl.google.com/dl/android/maven2/' }

# (list) packaging options to add
# Prevent duplicate files from crashing the build
android.add_packaging_options = exclude 'META-INF/DEPENDENCIES',exclude 'META-INF/NOTICE',exclude 'META-INF/LICENSE',exclude 'META-INF/LICENSE.txt',exclude 'META-INF/NOTICE.txt',doNotStrip '**/*.so'

# (list) Java .jar files to add
# android.add_jars = foo.jar,bar.jar

# (list) Java files to add
# android.add_src =

# (str) python-for-android branch / commit to use
p4a.branch = develop

# (str) Bootstrap to use for android builds
p4a.bootstrap = sdl2

# (str) Extra command line arguments to pass to p4a
# p4a.extra_args =

# (list) python-for-android recipes to use (forces compile from source)
# p4a.local_recipes = ./p4a-recipes

# (str) python-for-android specific hooks
# p4a.hook =

# (str) Filename to the hook for p4a
# p4a.hook =

# (int) Maximum number of parallel jobs for compilation
# Limit to prevent OOM on CI runners
p4a.jobs = 2

#
# iOS specific
#
# (ignored for Android builds)

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 0

# (str) Path to build artifact storage, absolute or relative to spec file
build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
bin_dir = ./bin
