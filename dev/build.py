#!/usr/bin/env python3
"""Build the installable phone app (PWA) of «عُمق» from dev/umq.html.

Usage: python3 build.py <three.min.js> <fontsource-cairo dir> <fontsource-ibm-plex-mono dir> <firebase npm package dir>
Writes the app into the repository root, which GitHub Pages serves.
"""
import os, re, shutil, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'umq.html')
OUT = os.path.join(HERE, '..')
three, cairo, plex, fbdir = sys.argv[1:5]

os.makedirs(os.path.join(OUT, 'fonts'), exist_ok=True)
os.makedirs(os.path.join(OUT, 'vendor'), exist_ok=True)
shutil.copy(three, os.path.join(OUT, 'vendor', 'three.min.js'))
FBJS = ['firebase-app-compat.js', 'firebase-auth-compat.js', 'firebase-firestore-compat.js']
for f in FBJS:
    shutil.copy(os.path.join(fbdir, f), os.path.join(OUT, 'vendor', f))
shutil.copy(os.path.join(HERE, 'firebase-config.js'), os.path.join(OUT, 'firebase-config.js'))

faces = []
def face(family, path, name, weight, rng):
    shutil.copy(os.path.join(path, 'files', name), os.path.join(OUT, 'fonts', name))
    faces.append("@font-face{font-family:'%s';font-style:normal;font-display:swap;font-weight:%d;src:url(fonts/%s) format('woff2');unicode-range:%s}" % (family, weight, name, rng))
AR = 'U+0600-06FF,U+0750-077F,U+0870-088E,U+0890-0891,U+0898-08E1,U+08E3-08FF,U+200C-200E,U+2010-2011,U+204F,U+2E41,U+FB50-FDFF,U+FE70-FE74,U+FE76-FEFC'
LA = 'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD'
for w in (400, 500, 600, 700, 800):
    face('Cairo', cairo, 'cairo-arabic-%d-normal.woff2' % w, w, AR)
    face('Cairo', cairo, 'cairo-latin-%d-normal.woff2' % w, w, LA)
for w in (400, 500, 600):
    face('IBM Plex Mono', plex, 'ibm-plex-mono-latin-%d-normal.woff2' % w, w, LA)

src = open(SRC, encoding='utf-8').read()
# drop artifact-only lines and remote font/CDN references
src = re.sub(r'<title>.*?</title>\n', '', src, count=1)
src = re.sub(r'<meta name="claude:[^>]*>\n', '', src)
src = re.sub(r'<link rel="(preconnect|stylesheet)" href="https://fonts\.[^>]*>\n', '', src)
src = src.replace('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js', 'vendor/three.min.js')
assert 'fonts.googleapis' not in src and 'cdnjs' not in src

head = '''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>عُمق</title>
<meta name="description" content="لعبة استراتيجية لحفر آبار المياه والنفط بوقت حقيقي.">
<meta name="theme-color" content="#0c161c">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="عُمق">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icons/icon-192.png" type="image/png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<script src="vendor/firebase-app-compat.js"></script>
<script src="vendor/firebase-auth-compat.js"></script>
<script src="vendor/firebase-firestore-compat.js"></script>
<script src="firebase-config.js"></script>
<style>html,body{margin:0;background:#0c161c}''' + ''.join(faces) + '''</style>
</head>
<body>
'''
tail = '''
<script>
if('serviceWorker' in navigator){addEventListener('load',()=>{navigator.serviceWorker.register('sw.js').catch(()=>{});});}
</script>
</body>
</html>
'''
html = head + src + tail
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(html)

# service worker: cache every file of the app, versioned by content hash
files = ['./', 'index.html', 'manifest.webmanifest', 'firebase-config.js', 'vendor/three.min.js'] + ['vendor/' + f for f in FBJS] + \
        ['fonts/' + f for f in sorted(os.listdir(os.path.join(OUT, 'fonts')))] + \
        ['icons/' + f for f in sorted(os.listdir(os.path.join(OUT, 'icons')))]
h = hashlib.sha1()
for f in files[1:]:
    h.update(open(os.path.join(OUT, f), 'rb').read())
ver = h.hexdigest()[:10]
sw = '''const CACHE='umq-%s';
const FILES=%s;
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES)).then(()=>self.skipWaiting()));});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
self.addEventListener('fetch',e=>{
  if(e.request.method!=='GET')return;
  const u=new URL(e.request.url);if(u.origin!==location.origin)return;
  // page: network first so updates arrive, cache when offline; other files: cache first
  if(e.request.mode==='navigate'){e.respondWith(fetch(e.request).then(r=>{const c=r.clone();caches.open(CACHE).then(x=>x.put('index.html',c));return r;}).catch(()=>caches.match('index.html')));return;}
  e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request)));
});
''' % (ver, repr(files).replace("'", '"'))
open(os.path.join(OUT, 'sw.js'), 'w').write(sw)
print('built', OUT, 'cache', ver, 'files', len(files))
