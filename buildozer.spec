[app]

# App info
title = 加减法练习
package.name = mathgame
package.domain = com.mathgame
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0.0

# Requirements
requirements = python3,kivy

# Android
android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# Orientation
orientation = portrait
fullscreen = 0

# Build
log_level = 2

[buildozer]
warn_on_root = 0
