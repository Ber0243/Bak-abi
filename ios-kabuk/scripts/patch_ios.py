#!/usr/bin/env python3
"""cap add ios ile üretilen iOS projesini TÜRKAİ kabuğu için yamalar."""
import plistlib, re, shutil, sys, glob, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
APP = os.path.join(ROOT, 'ios', 'App', 'App')
def p(*a): return os.path.join(APP, *a)

# 1) Info.plist
path = p('Info.plist')
with open(path, 'rb') as f: pl = plistlib.load(f)
pl.update({
  'CFBundleDisplayName': 'TÜRKAİ',
  'NSMicrophoneUsageDescription': 'TÜRKAİ seni dinleyip konuşabilmek için mikrofona ihtiyaç duyar.',
  'NSCameraUsageDescription': 'Kameradan gördüğünü anlatabilmem ve el kontrolü için kamera erişimi gerekir.',
  'NSPhotoLibraryUsageDescription': 'Seçtiğin fotoğrafları okuyabilmem için.',
  'NSLocationWhenInUseUsageDescription': 'Hava durumunu bulunduğun yere göre söylemek için.',
  'UIBackgroundModes': ['audio'],
  'ITSAppUsesNonExemptEncryption': False,
  'UIUserInterfaceStyle': 'Dark',
  # http://adres (Tailscale/yerel ağ) de açılabilsin; mikrofon yine yalnızca https'te çalışır
  'NSAppTransportSecurity': {'NSAllowsArbitraryLoads': True},
})
with open(path, 'wb') as f: plistlib.dump(pl, f)
print('Info.plist yamalandı')

# 2) Ses oturumu: sessiz anahtarında da ses çalsın, mikrofon açık kalsın
ad = p('AppDelegate.swift')
s = open(ad, encoding='utf-8').read()
if 'AVAudioSession' not in s:
    s = s.replace('import UIKit', 'import UIKit\nimport AVFoundation', 1)
    code = ('\n        do { let a = AVAudioSession.sharedInstance(); '
            'try a.setCategory(.playAndRecord, mode: .default, options: [.defaultToSpeaker, .allowBluetooth]); '
            'try a.setActive(true) } catch { print("TURKAI ses oturumu: \\(error)") }')
    s, n = re.subn(r'(didFinishLaunchingWithOptions[^{]*\{)', lambda m: m.group(1) + code, s, count=1)
    if n != 1: sys.exit('AppDelegate yamalanamadı')
    open(ad, 'w', encoding='utf-8').write(s)
print('AppDelegate yamalandı')

# 3) Simge ve açılış ekranı
icon = os.path.join(ROOT, 'resources', 'icon-1024.png')
splash = os.path.join(ROOT, 'resources', 'splash-2732.png')
for f in glob.glob(p('Assets.xcassets', 'AppIcon.appiconset', '*.png')): shutil.copy(icon, f)
for f in glob.glob(p('Assets.xcassets', 'Splash.imageset', '*.png')): shutil.copy(splash, f)
print('simge ve açılış ekranı değişti')
