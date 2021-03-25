# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
         ( "quirks", 'quirks' ),
         ( "smilies", 'smilies' ),
         ( "themes", 'themes' ),
         ( "docs", 'docs' ),
         ( "README.md", '.' ),
         ( "LICENSE", '.' ),
         ( "CHANGELOG.md", '.' ),
         ( "server.json", '.' ),
         ( "PCskins.png", '.' ),
         ( "Pesterchum.png", '.' )
         ]

a = Analysis(['pesterchum.py'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='pesterchum',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='pesterchum')
