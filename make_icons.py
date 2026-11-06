import os
from PIL import Image

SRC = "assets/icon.png"
ROOT = "android/app/src/main/res"

im = Image.open(SRC).convert("RGBA")
w, h = im.size
s = min(w, h)
im = im.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s))

densities = {
    "mdpi": (48, 108),
    "hdpi": (72, 162),
    "xhdpi": (96, 216),
    "xxhdpi": (144, 324),
    "xxxhdpi": (192, 432),
}

for d, (legacy, fg) in densities.items():
    out = os.path.join(ROOT, "mipmap-" + d)
    os.makedirs(out, exist_ok=True)
    im.resize((legacy, legacy), Image.LANCZOS).save(os.path.join(out, 'ic_launcher.png'))
    canvas = Image.new("RGBA", (fg, fg), (0, 0, 0, 0))
    inner = int(fg * 0.66)
    art = im.resize((inner, inner), Image.LANCZOS)
    canvas.paste(art, ((fg - inner) // 2, (fg - inner) // 2), art)
    canvas.save(os.path.join(out, "ic_launcher_foreground.png"))

anydpi = os.path.join(ROOT, "mipmap-anydpi-v26")
os.makedirs(anydpi, exist_ok=True)
XML = '<?xml version="1.0" encoding="utf-8"?>\n<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n    <background android:drawable="@color/ic_launcher_background" />\n    <foreground android:drawable="@mipmap/ic_launcher_foreground" />\n</adaptive-icon>\n'
for name in ("ic_launcher.xml", "ic_launcher_round.xml"):
    open(os.path.join(anydpi, name), "w", encoding="utf-8").write(XML)

vals = os.path.join(ROOT, "values")
os.makedirs(vals, exist_ok=True)
open(os.path.join(vals, "ic_launcher_background.xml"), "w", encoding="utf-8").write(
    '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#2B1A12</color>\n</resources>\n'
)

print("icons generated")

# 原生启动图：纯绿色，替换 Capacitor 默认的白底
_sp = Image.new("RGB", (1080, 1920), (46, 158, 107))
_dr = os.path.join(ROOT, "drawable")
os.makedirs(_dr, exist_ok=True)
_sp.save(os.path.join(_dr, "splash.png"))
print("splash generated")

# Android 12+ 系统启动画面：背景改绿、图标用 app 图标
import re
_styles = os.path.join(ROOT, "values", "styles.xml")
_s = open(_styles, encoding="utf-8").read()
if "windowSplashScreenBackground" not in _s:
    _key = '<style name="AppTheme.NoActionBarLaunch"'
    _i = _s.index(_key)
    _j = _s.index("</style>", _i)
    _inject = ('\n        <item name="windowSplashScreenBackground">#2E9E6B</item>'
               '\n        <item name="windowSplashScreenAnimatedIcon">@mipmap/ic_launcher</item>\n    ')
    _s = _s[:_j] + _inject + _s[_j:]
    open(_styles, "w", encoding="utf-8").write(_s)
    print("styles patched")
