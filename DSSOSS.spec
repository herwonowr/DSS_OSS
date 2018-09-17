# -*- mode: python -*-

block_cipher = None


a = Analysis(['DSSOSS20180906_2.py'],
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
          [('PyQt5/Qt/plugins/styles/qwindowsvistastyle.dll', 'C:\\Python\Lib\site-packages\PyQt5\Qt\plugins\styles\qwindowsvistastyle.dll', 'BINARY')],
          name='DSSOSS20180906_2',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True,icon='C:\python_work\DSS_OSS\ooopic_1526549922.ico' )
