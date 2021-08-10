import PyInstaller.__main__
import sys
import shutil
import os

if sys.version_info < (3, 0, 0):
    sys.exit("Python versions lower than 3 are not supported.")
elif (sys.version_info >= (3, 9, 0)) & (sys.platform == 'win32'):
    print("WARNING!!!! Building with python 3.9 will make your builds not run on windows 7 and previous versions.")

def is_64bit() -> bool:
    return sys.maxsize > 2**32

is_64bit = is_64bit()

try:
    print("Pyinstaller script to make everything a bit more conventient, just being able to run \"pyinstaller\" \
is a lot more useable than having to include all command line arguments every time.\n\
Some of the include files are specific to my instalation, so you might have to edit the file if you run into issues \:\(")

    delete_builddist = input("Delete build & dist folders? (Y/N): ")
    if delete_builddist.lower() == "y":
        try:
            shutil.rmtree('dist')
        except FileNotFoundError as e:
            print(e)
        try:
            shutil.rmtree('build')
        except FileNotFoundError as e:
            print(e)
    print("UPX can decently reduce filesize but builds might get flagged by anti-viruses more often. (+ it sometimes breaks QT's DLLs)")
    if input("Enable UPX? [N]: ").lower() == 'y':
        upx_enabled = True
    else:
        upx_enabled = False
        
    if upx_enabled == True:
        print("If upx is on your path you don't need to include anything here.")
        if is_64bit == True:
            upx_dir = input("UPX directory [D:\\upx-3.96-win64]: ")
            if upx_dir == '':
                upx_dir = "D:\\upx-3.96-win64" # Default dir for me :)
        else:
            upx_dir = input("UPX directory [D:\\upx-3.96-win32]: ")
            if upx_dir == '':
                upx_dir = "D:\\upx-3.96-win32" # Default dir for me :)
        print("upx_dir = " + upx_dir)
    else:
        upx_dir = ''
    if sys.platform == 'win32':
        print("\nUniversal CRT needs to be included if you don't want to run into compatibility issues when building on Windows 10. ( https://pyinstaller.readthedocs.io/en/stable/usage.html?highlight=sdk#windows )")
        if is_64bit == True:
            crt_path = input("Universal CRT: [C:\\Program Files (x86)\\Windows Kits\\10\\Redist\\10.0.19041.0\\ucrt\\DLLs\\x64]: ")
            if crt_path == '':
                crt_path = "C:\\Program Files (x86)\\Windows Kits\\10\\Redist\\10.0.19041.0\\ucrt\\DLLs\\x64" # Default directory.
        else:
            crt_path = input("Extra path: [C:\\Program Files (x86)\\Windows Kits\\10\\Redist\\10.0.19041.0\\ucrt\\DLLs\\x86]: ")
            if crt_path == '':
                crt_path = "C:\\Program Files (x86)\\Windows Kits\\10\\Redist\\10.0.19041.0\\ucrt\\DLLs\\x86" # Default directory.
        print("crt_path = " + crt_path)
except KeyboardInterrupt as e:
    sys.exit("KeyboardInterrupt")

exclude_modules = ['collections.sys',
        'collections._sre',
        'collections._json',
        'collections._locale',
        'collections._struct',
        'collections.array',
        'collections._weakref',
        'PyQt5.QtMultimedia',
        'PyQt5.QtDBus',
        'PyQt5.QtDeclarative',
        'PyQt5.QtHelp',
        'PyQt5.QtNetwork',
        'PyQt5.QtSql',
        'PyQt5.QtSvg',
        'PyQt5.QtTest',
        'PyQt5.QtWebKit',
#        'PyQt5.QtXml',
#        'PyQt5.QtXmlPatterns',
        'PyQt5.phonon',
        'PyQt5.QtAssistant',
        'PyQt5.QtDesigner',
        'PyQt5.QAxContainer',]

add_data = ['quirks;quirks',
        'smilies;smilies',
        'themes;themes',
        'docs;docs',
        'README.md;.',
        'LICENSE;.',
        'CHANGELOG.md;.',
        'PCskins.png;.',
        'Pesterchum.png;.',
        'logging.conf;.']

upx_exclude = ["qwindows.dll",
    "Qt5Core.dll",
    "Qt5Gui.dll",
    "vcruntime140.dll",
    "MSVCP140.dll",
    "MSVCP140_1.dll"
    "api-ms-win-core-console-l1-1-0.dll",\
    "api-ms-win-core-console-l1-1-0.dll",\
    "api-ms-win-core-console-l1-2-0.dll",\
    "api-ms-win-core-datetime-l1-1-0.dll",\
    "api-ms-win-core-debug-l1-1-0.dll",\
    "api-ms-win-core-errorhandling-l1-1-0.dll",\
    "api-ms-win-core-file-l1-1-0.dll",\
    "api-ms-win-core-file-l1-2-0.dll",\
    "api-ms-win-core-file-l2-1-0.dll",\
    "api-ms-win-core-handle-l1-1-0.dll",\
    "api-ms-win-core-heap-l1-1-0.dll",\
    "api-ms-win-core-interlocked-l1-1-0.dll",\
    "api-ms-win-core-libraryloader-l1-1-0.dll",\
    "api-ms-win-core-localization-l1-2-0.dll",\
    "api-ms-win-core-memory-l1-1-0.dll",\
    "api-ms-win-core-namedpipe-l1-1-0.dll",\
    "api-ms-win-core-processenvironment-l1-1-0.dll",\
    "api-ms-win-core-processthreads-l1-1-0.dll",\
    "api-ms-win-core-processthreads-l1-1-1.dll",\
    "api-ms-win-core-profile-l1-1-0.dll",\
    "api-ms-win-core-rtlsupport-l1-1-0.dll",\
    "api-ms-win-core-string-l1-1-0.dll",\
    "api-ms-win-core-synch-l1-1-0.dll",\
    "api-ms-win-core-synch-l1-2-0.dll",\
    "api-ms-win-core-sysinfo-l1-1-0.dll",\
    "api-ms-win-core-timezone-l1-1-0.dll",\
    "api-ms-win-core-util-l1-1-0.dll",\
    "API-MS-Win-core-xstate-l2-1-0.dll",\
    "api-ms-win-crt-conio-l1-1-0.dll",\
    "api-ms-win-crt-convert-l1-1-0.dll",\
    "api-ms-win-crt-environment-l1-1-0.dll",\
    "api-ms-win-crt-filesystem-l1-1-0.dll",\
    "api-ms-win-crt-heap-l1-1-0.dll",\
    "api-ms-win-crt-locale-l1-1-0.dll",\
    "api-ms-win-crt-math-l1-1-0.dll",\
    "api-ms-win-crt-multibyte-l1-1-0.dll",\
    "api-ms-win-crt-private-l1-1-0.dll",\
    "api-ms-win-crt-process-l1-1-0.dll",\
    "api-ms-win-crt-runtime-l1-1-0.dll",\
    "api-ms-win-crt-stdio-l1-1-0.dll",\
    "api-ms-win-crt-string-l1-1-0.dll",\
    "api-ms-win-crt-time-l1-1-0.dll",\
    "api-ms-win-crt-utility-l1-1-0.dll",\
    "ucrtbase.dll"]

#Windows
if sys.platform == 'win32':
    run_win32 = [
        'pesterchum.py',
        '--name=Pesterchum',
        '--paths=%s' % crt_path,
        #'--noconfirm',               # Overwrite output directory.
        '--windowed',                 # Hide console
        #'--onefile',
        '--icon=pesterchum.ico',
        '--clean', # Clear cache
    ]

    if upx_enabled == True:
        if os.path.isdir(upx_dir):
            run_win32.append('--upx-dir=%s' % upx_dir)
    else:
        run_win32.append('--noupx')

    for x in upx_exclude:
        run_win32.append('--upx-exclude=%s' % x )
        # Lower case variants are required.
        run_win32.append('--upx-exclude=%s' % x.lower() )

    for x in exclude_modules:
        run_win32.append('--exclude-module=%s' % x )
    
    for x in add_data:
        run_win32.append('--add-data=%s' % x )

    if os.path.exists(crt_path):
        if is_64bit == False:
            run_win32.append('--add-binary=%s\\api-ms-win-core-console-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-console-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-console-l1-2-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-datetime-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-debug-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-errorhandling-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-file-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-file-l1-2-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-file-l2-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-handle-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-heap-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-interlocked-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-libraryloader-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-localization-l1-2-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-memory-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-namedpipe-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-processenvironment-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-processthreads-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-processthreads-l1-1-1.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-profile-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-rtlsupport-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-string-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-synch-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-synch-l1-2-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-sysinfo-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-timezone-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-util-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\API-MS-Win-core-xstate-l2-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-crt-conio-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-crt-convert-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-crt-environment-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-crt-filesystem-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-crt-heap-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-crt-locale-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-crt-math-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-crt-multibyte-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-crt-private-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-crt-process-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-crt-runtime-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-crt-stdio-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-crt-string-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-crt-time-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-crt-utility-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\ucrtbase.dll;.' % crt_path)
        elif is_64bit == True:
            run_win32.append('--add-binary=%s\\api-ms-win-core-console-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-console-l1-2-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-datetime-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-debug-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-errorhandling-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-file-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-file-l1-2-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-file-l2-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-handle-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-heap-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-interlocked-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-libraryloader-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-localization-l1-2-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-memory-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-namedpipe-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-processenvironment-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-processthreads-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-processthreads-l1-1-1.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-profile-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-rtlsupport-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-string-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-synch-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-synch-l1-2-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-sysinfo-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-timezone-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-core-util-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-crt-conio-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-crt-convert-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-crt-environment-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-crt-filesystem-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-crt-heap-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-crt-locale-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-crt-math-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-crt-multibyte-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-crt-private-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-crt-process-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-crt-runtime-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-crt-stdio-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-crt-string-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-crt-time-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\api-ms-win-crt-utility-l1-1-0.dll;.' % crt_path)
            run_win32.append('--add-binary=%s\\ucrtbase.dll;.' % crt_path)

    PyInstaller.__main__.run(run_win32)
#MacOS
elif sys.platform == 'darwin' :
    input("NOTE: Building with pyinstaller on MacOS doesn't seem to work for me.")
    run_darwin =[
        'pesterchum.py',
        '--name=Pesterchum',
        '--windowed',             # Hide console
        #'--noconfirm',           # Overwrite output directory.
        '--icon=trayicon32.icns', # Icon
        '--onedir',
        #'--noupx'
    ]

    if os.path.isdir(upx_dir):
        run_darwin.append('--upx-dir=%s' % upx_dir)
    
    for x in upx_exclude:
        run_darwin.append('--upx-exclude=%s' % x )
        # Lower case variants are required.
        run_darwin.append('--upx-exclude=%s' % x.lower() )

    for x in exclude_modules:
        run_darwin.append('--exclude-module=%s' % x )
    
    for x in add_data:
        run_darwin.append('--add-data=%s' % x.replace(';',':') )
    
    PyInstaller.__main__.run(run_darwin)
#Linux
elif sys.platform == 'linux':
    run_linux =[
        'pesterchum.py',
        '--name=Pesterchum',
        #'--windowed',             # Hide console
        #'--noconfirm',           # Overwrite output directory.
        '--icon=trayicon32.icns', # Icon
    ]

    
    if os.path.isdir(upx_dir):
        run_linux.append('--upx-dir=%s' % upx_dir)
        
    for x in upx_exclude:
        run_linux.append('--upx-exclude=%s' % x )
        # Lower case variants are required.
        run_linux.append('--upx-exclude=%s' % x.lower() )

    for x in exclude_modules:
        run_linux.append('--exclude-module=%s' % x )
    
    for x in add_data:
        run_linux.append('--add-data=%s' % x.replace(';',':') )
    
    PyInstaller.__main__.run(run_linux)
else:
    print("Unknown platform.")
    
    run_generic =[
        'pesterchum.py',
        '--name=Pesterchum',
        '--upx-dir=%s' % upx_dir  # Set Upx directory. (I think it also works from path.)
    ]
    
    for x in upx_exclude:
        run_generic.append('--upx-exclude=%s' % x )
        # Lower case variants are required.
        run_generic.append('--upx-exclude=%s' % x.lower() )

    for x in exclude_modules:
        run_generic.append('--exclude-module=%s' % x )
    
    for x in add_data:
        run_generic.append('--add-data=%s' % x.replace(';',':') )
    
    PyInstaller.__main__.run(run_generic)
