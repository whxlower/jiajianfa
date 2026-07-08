[app]

# App info
title = 加减法练习
package.name = mathgame
package.domain = com.mathgame
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0.0

# Requirements
requirements = python3,kivy,pillow

# Android
android.permissions =
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# Orientation: portrait for phone, sensor for tablet adapt
orientation = portrait
fullscreen = 0

# Adaptive icon
# icon.filename = %(source.dir)s/icon.png
# presplash.filename = %(source.dir)s/splash.png

# Build
android.release_artifact = apk
android.debug_artifact = apk

# Log level
log_level = 2

# P4A
p4a.branch = develop

[buildozer]
warn_on_root = 0
