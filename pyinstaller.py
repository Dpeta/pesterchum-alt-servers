import os
import sys
import shutil

import PyInstaller.__main__

is_64bit = sys.maxsize > 2**32
exclude_modules = []
add_data = ['quirks;quirks',
        'smilies;smilies',
        'themes;themes',
        'docs;docs',
        'README.md;.',
        'LICENSE;.',
        'CHANGELOG.md;.',
        'PCskins.png;.',
        'Pesterchum.png;.']
data_folders = {'quirks': 'quirks',
        'smilies': 'smilies',
        'themes': 'themes',
        'docs': 'docs'}
data_files = {'README.md': 'README.md.txt',
        'LICENSE': 'LICENSE.txt',
        'CHANGELOG.md': 'CHANGELOG.md.txt',
        'PCskins.png': '.',
        'Pesterchum.png': '.'}
# Some of these might not be required anymore,
# newer versions of PyInstaller claim to exclude certain problematic DDLs automatically.
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

delete_builddist = ''
upx_enabled = ''
package_universal_crt = ''
onefile = ''
windowed = ''

try:
    print("This is a script to make building with Pyinstaller a bit more conventient.")

    while (delete_builddist != 'y') and (delete_builddist != 'n'):
        delete_builddist = input("Delete build & dist folders? (Y/N): ").lower()
    if delete_builddist == "y":
        try:
            shutil.rmtree('dist')
        except FileNotFoundError as e:
            print(e)
        try:
            shutil.rmtree('build')
        except FileNotFoundError as e:
            print(e)
    
    while (upx_enabled != 'y') and (upx_enabled != 'n'):
        upx_enabled = input("Enable UPX? (Y/N): ").lower()
    if upx_enabled == 'y':
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
    elif upx_enabled == 'n':
        upx_dir = ''
    
    while (windowed != 'y') and (windowed != 'n'):
        windowed = input("Build with '--windowed'? (Y/N): ").lower()
    
    if sys.platform == 'win32':
        print("(https://pyinstaller.readthedocs.io/en/stable/usage.html?highlight=sdk#windows)")
        while (package_universal_crt != 'y') and (package_universal_crt != 'n'):
            package_universal_crt = input("Try to include universal CRT? (Y/N): ").lower()
        if package_universal_crt == 'y':
            if is_64bit == True:
                crt_path = input("Universal CRT: [C:\\Program Files (x86)\\Windows Kits\\10\\Redist\\10.0.19041.0\\ucrt\\DLLs\\x64]: ")
                if crt_path == '':
                    #crt_path = "C:\\Program Files (x86)\\Windows Kits\\10\\Redist\\10.0.19041.0\\ucrt\\DLLs\\x64" # Default directory.
                    crt_path = os.path.join('C:%s' % os.sep, 'Program Files (x86)', 'Windows Kits', '10', '10.0.19041.0', 'ucrt', 'DLLs', 'x64')
            else:
                crt_path = input("Extra path: [C:\\Program Files (x86)\\Windows Kits\\10\\Redist\\10.0.19041.0\\ucrt\\DLLs\\x86]: ")
                if crt_path == '':
                    #crt_path = "C:\\Program Files (x86)\\Windows Kits\\10\\Redist\\10.0.19041.0\\ucrt\\DLLs\\x86" # Default directory.
                    crt_path = os.path.join('C:%s' % os.sep, 'Program Files (x86)', 'Windows Kits', '10', '10.0.19041.0', 'ucrt', 'DLLs', 'x86')
            print("crt_path = " + crt_path)
            
    if (sys.platform == 'win32') or (sys.platform == 'linux'):
        while (onefile != 'y') and (onefile != 'n'):
            onefile = input("Build with '--onefile'? (Y/N): ").lower()
        
except KeyboardInterrupt:
    sys.exit("KeyboardInterrupt")

#Windows
if sys.platform == 'win32':
    run_win32 = [
        'pesterchum.py',
        '--name=Pesterchum',
        #'--noconfirm',               # Overwrite output directory.
        #'--windowed',                 # Hide console
        '--icon=pesterchum.ico',
        '--clean', # Clear cache
        
    ]

    if (sys.version_info.major == 3) & (sys.version_info.minor == 8):
        exclude_modules.append('tkinter')
    if upx_enabled == 'y':
        if os.path.isdir(upx_dir):
            run_win32.append('--upx-dir=%s' % upx_dir)
            for x in upx_exclude:
                run_win32.append('--upx-exclude=%s' % x )
                # Lower case variants are required.
                run_win32.append('--upx-exclude=%s' % x.lower() )
    elif upx_enabled == 'n':
        run_win32.append('--noupx')
    for x in exclude_modules:
        run_win32.append('--exclude-module=%s' % x )
    if windowed == 'y':
        run_win32.append('--windowed')
    if onefile == 'y':
        run_win32.append('--onefile')
    elif onefile == 'n':
        for x in add_data:
            run_win32.append('--add-data=%s' % x )

   
    if package_universal_crt == 'y':
        run_win32.append('--paths=\"%s\"' % crt_path)
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
    print(run_win32)
    PyInstaller.__main__.run(run_win32)
    
    if onefile == 'y':
        # There's more proper ways to do this, but this doesn't require changing our paths
        for x in data_folders:
            print(x)
            shutil.copytree(x, os.path.join('dist', data_folders[x]),
            ignore=shutil.ignore_patterns('*.psd',
                                           '*.xcf*',
                                           'ebg2.png',
                                           'ebg1.png'))
        for x in data_files:
            print(x)
            shutil.copy(x, os.path.join('dist', data_files[x]))
        
        files = os.listdir('dist')
        os.mkdir(os.path.join('dist', 'Pesterchum'))
        for x in files:
            shutil.move(os.path.join('dist',x), os.path.join('dist', 'Pesterchum'))
            
    #shutil.copy(os.path.join('build', 'Pesterchum', 'xref-Pesterchum.html'), 
    #            os.path.join('dist', 'Pesterchum', 'xref-Pesterchum.html'))
    #shutil.copy(os.path.join('build', 'Pesterchum', 'Analysis-00.toc'), 
    #            os.path.join('dist', 'Pesterchum', 'Analysis-00.toc'))

    
#MacOS
elif sys.platform == 'darwin' :
    run_darwin =[
        'pesterchum.py',
        '--name=Pesterchum',
        #'--windowed',             # Hide console
        #'--noconfirm',           # Overwrite output directory.
        '--icon=trayicon32.icns', # Icon
        '--onedir',
        '--clean', # Clear cache
        #'--noupx'
    ]

    if upx_enabled == 'y':
        if os.path.isdir(upx_dir):
            run_darwin.append('--upx-dir=%s' % upx_dir)
            for x in upx_exclude:
                run_darwin.append('--upx-exclude=%s' % x )
                # Lower case variants are required.
                run_darwin.append('--upx-exclude=%s' % x.lower() )
    elif upx_enabled == 'n':
        run_darwin.append('--noupx')
    if os.path.isdir(upx_dir):
        run_darwin.append('--upx-dir=%s' % upx_dir)
    for x in exclude_modules:
        run_darwin.append('--exclude-module=%s' % x )
    for x in add_data:
        run_darwin.append('--add-data=%s' % x.replace(';',':') )
    if windowed == 'y':
        run_win32.append('--windowed')
    PyInstaller.__main__.run(run_darwin)
    
#Linux
elif sys.platform == 'linux':
    run_linux =[
        'pesterchum.py',
        '--name=Pesterchum',
        #'--windowed',             # Hide console
        #'--noconfirm',           # Overwrite output directory.
        '--icon=trayicon32.icns', # Icon
        '--clean', # Clear cache
    ]

    if upx_enabled == 'y':
        if os.path.isdir(upx_dir):
            run_linux.append('--upx-dir=%s' % upx_dir)
            for x in upx_exclude:
                run_linux.append('--upx-exclude=%s' % x )
                # Lower case variants are required.
                run_linux.append('--upx-exclude=%s' % x.lower() )
    elif upx_enabled == 'n':
        run_linux.append('--noupx')
    for x in exclude_modules:
        run_linux.append('--exclude-module=%s' % x )
    if onefile == 'y':
        run_linux.append('--onefile')
    elif onefile == 'n':
        for x in add_data:
            run_linux.append('--add-data=%s' % x.replace(';',':') )
    if windowed == 'y':
        run_win32.append('--windowed')
        
    print(run_linux)
    PyInstaller.__main__.run(run_linux)
    
    if onefile == 'y':
        # There's more proper ways to do this, but this doesn't require changing our paths
        for x in data_folders:
            print(x)
            shutil.copytree(x, os.path.join('dist', data_folders[x]),
            ignore=shutil.ignore_patterns('*.psd',
                                           '*.xcf*',
                                           'ebg2.png',
                                           'ebg1.png'))
        for x in data_files:
            print(x)
            shutil.copy(x, os.path.join('dist', data_files[x]))
        
        files = os.listdir('dist')
        os.mkdir(os.path.join('dist', 'Pesterchum'))
        for x in files:
            shutil.move(os.path.join('dist',x), os.path.join('dist', 'Pesterchum'))
    #shutil.copy(os.path.join('build', 'Pesterchum', 'xref-Pesterchum.html'), 
    #            os.path.join('dist', 'Pesterchum', 'xref-Pesterchum.html'))
    #shutil.copy(os.path.join('build', 'Pesterchum', 'Analysis-00.toc'), 
    #            os.path.join('dist', 'Pesterchum', 'Analysis-00.toc'))
    
else:
    print("Unknown platform.")
    
    run_generic =[
        'pesterchum.py',
        '--name=Pesterchum'
        '--clean', # Clear cache
    ]

    if upx_enabled == 'y':
        if os.path.isdir(upx_dir):
            run_generic.append('--upx-dir=%s' % upx_dir)
    else:
        run_generic.append('--noupx')
    for x in upx_exclude:
        run_generic.append('--upx-exclude=%s' % x )
        # Lower case variants are required.
        run_generic.append('--upx-exclude=%s' % x.lower() )
    for x in exclude_modules:
        run_generic.append('--exclude-module=%s' % x )
    for x in add_data:
        run_generic.append('--add-data=%s' % x.replace(';',':') )
    if windowed == 'y':
        run_win32.append('--windowed')
        
    print(run_generic)
    
    PyInstaller.__main__.run(run_generic)
