#  -*- mode: python -*-
from kivy.tools.packaging.pyinstaller_hooks import install_hooks
install_hooks(globals())

import os
gst_plugin_path = os.environ.get('GST_PLUGIN_PATH').split(':')[0]

block_cipher = None


a = Analysis(['/Users/cropleyb/Dropbox/pente/main.py'],
             pathex=['/Users/cropleyb/pubsrc/pyinstaller/pai'],
             hiddenimports=[],
             #hiddenimports=['/Users/cropleyb/pubsrc/pyinstaller/pai'],
             runtime_hooks=None,
             cipher=block_cipher)
pyz = PYZ(a.pure,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='pai',
          debug=False,
          strip=None,
          upx=True,
          console=False )
coll = COLLECT(exe,
               # Tree('/Users/cropleyb/Dropbox/pente/media', prefix="media", excludes=".git*"),
               Tree('/Users/cropleyb/Dropbox/pente/media', prefix="media"),
               Tree(os.path.join(gst_plugin_path, '..')),
               a.binaries,
               a.zipfiles,
               a.datas + (("pentai/gui/pentai.kv", '/Users/cropleyb/Dropbox/pente/pentai/gui/pentai.kv', 'DATA'),),
               strip=None,
               upx=True,
               name='pai')
app = BUNDLE(coll,
             name='pai.app',
             icon=None)
