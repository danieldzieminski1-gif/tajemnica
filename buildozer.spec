[app]
title = Tajemnica o 3 w Nocy
package.name = tajemnica3
package.domain = org.ziomek
source.dir = .
source.include_exts = py,png
version = 1.0
requirements = python3,kivy==2.3.0
orientation = landscape
fullscreen = 1
icon.filename = %(source.dir)s/assets/icon.png
android.archs = arm64-v8a
android.api = 33
android.minapi = 24
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
