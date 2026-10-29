[app]

# (str) Title of your application
title = Space Invaders

# (str) Package name
package.name = spaceinvaders

# (str) Package domain (needed for android packaging)
package.domain = org.space

# (str) Source where the app lives
source.dir = .

# (str) Application versioning
version = 1.0

# (list) Source files to include (let it empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,wav,ogg

# (list) Application requirements
requirements = python3,pygame,sdl2_image,sdl2_mixer,sdl2_ttf

# (str) Supported orientations (portrait, landscape, all)
orientation = landscape

# (int) Target Android API
android.api = 31

# (int) Minimum API your APK will support
android.minapi = 21
