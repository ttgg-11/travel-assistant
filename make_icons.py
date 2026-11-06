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

# 原生启动图：纯绿色（不留任何图），衔接网页启动页
_dr = os.path.join(ROOT, "drawable")
os.makedirs(_dr, exist_ok=True)
Image.new("RGB", (1080, 2340), (46, 158, 107)).save(os.path.join(_dr, "splash.png"))
# 透明图标：让 Android 12 系统启动页只剩纯色背景
Image.new("RGBA", (1, 1), (0, 0, 0, 0)).save(os.path.join(_dr, "transparent.png"))

# 系统启动页图标：圆角「蕊」+ 蕊之管家
_font_path = None
for _p in ["/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
           "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
           "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
           "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"]:
    if os.path.exists(_p):
        _font_path = _p
        break
if _font_path:
    from PIL import ImageDraw as _ID, ImageFont as _IF
    _S = 1080
    _img = Image.new("RGBA", (_S, _S), (0, 0, 0, 0))
    _d = _ID.Draw(_img)
    _box = 540
    _bx = (_S - _box) // 2
    _by = 170
    _d.rounded_rectangle([_bx, _by, _bx + _box, _by + _box], radius=126,
                         fill=(255, 255, 255, 46))
    _f = _IF.truetype(_font_path, 262)
    _bb = _d.textbbox((0, 0), "蕊", font=_f)
    _d.text((_S / 2 - (_bb[2] - _bb[0]) / 2 - _bb[0], _by + _box / 2 - (_bb[3] - _bb[1]) / 2 - _bb[1]),
            "蕊", font=_f, fill=(255, 255, 255, 255))
    _ft = _IF.truetype(_font_path, 100)
    _t = "蕊 之 管 家"
    _tb = _d.textbbox((0, 0), _t, font=_ft)
    _d.text((_S / 2 - (_tb[2] - _tb[0]) / 2 - _tb[0], _by + _box + 54),
            _t, font=_ft, fill=(255, 255, 255, 255))
    _img.save(os.path.join(_dr, "splash_icon.png"))
    print("splash icon generated")
else:
    Image.new("RGBA", (1080, 1080), (0, 0, 0, 0)).save(os.path.join(_dr, "splash_icon.png"))
    print("no CJK font found, fallback icon")
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
               '\n        <item name="windowSplashScreenAnimatedIcon">@drawable/splash_icon</item>\n    ')
    _s = _s[:_j] + _inject + _s[_j:]
    open(_styles, "w", encoding="utf-8").write(_s)
    print("styles patched")
