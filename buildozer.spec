[app]

title = Expense Tracker
package.name = expensetracker
package.domain = org.example

source.dir = .
source.include_exts = py,csv,png,jpg,kv,atlas

version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.api = 34
android.minapi = 23

# Let Buildozer handle the exact NDK pairing automatically
# android.ndk = 25b

android.accept_sdk_license = True
android.archs = armeabi-v7a, arm64-v8a

[buildozer]

log_level = 2
warn_on_root = 1
