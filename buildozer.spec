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

android.api = 35
android.minapi = 23
android.ndk = 25b
android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 1
