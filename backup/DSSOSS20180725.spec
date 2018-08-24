# -*- mode: python -*-

block_cipher = None


a = Analysis(['DSSOSS20180725.py'],
             pathex=['C:\\python_work\\DSS_OSS'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='DSSOSS20180725',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
