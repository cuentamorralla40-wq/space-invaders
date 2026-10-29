[app]
title = Space Invaders
package.name = spaceinvaders
package.domain = org.game
source.include_exts = py,png,jpg,kv,atlas
source.dir = .
version = 1.0
requirements = python3,pygame
orientation = portrait
fullscreen = 1
android.permissions = INTERNET

android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# Soportar ambas arquitecturas para evitar bloqueos de compilación
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
