[app]
title = Ony Downloader
package.name = ony_downloader
package.domain = com.ony
source.dir = .
version = 1.0
requirements = python3,kivy,kivymd,youtube_dl,pytube
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 23b
android.archs = arm64-v8a, armeabi-v7a
android.gradle_dependencies = com.android.support:appcompat-v7:28.0.0
android.presplash_color = #000000
android.meta_data = android.max_aspect=2.4
android.allow_backup = True
p4a.branch = master
p4a.source_dir = 
p4a.bootstrap = sdl2
p4a.port = 8000

[buildozer]
log_level = 2
warn_on_root = 1
