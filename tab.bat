vswhere.exe -latest
for /f "usebackq delims=" %%i in (`vswhere.exe -latest -property installationPath`) do %comspec% /k "%%i\Common7\Tools\vsdevcmd.bat"
mkdir a
cd a
wget https://github.com/aseprite/aseprite/releases/download/v%VERSION%/Aseprite-v%VERSION%-Source.zip
unzip Aseprite-v%VERSION%-Source.zip
cd ..
mkdir c
cd c
wget https://github.com/aseprite/skia/releases/download/%SKIAVERSION%/Skia-Windows-Release-x86.zip
unzip Skia-Windows-Release-x86.zip
cd ..
mkdir b
cd b
cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -DLAF_BACKEND=skia -DSKIA_DIR=..\c -DSKIA_LIBRARY_DIR=..\c\out\Release-x86 -DSKIA_LIBRARY=..\c\out\Release-x86\skia.lib -G Ninja ..\a
ninja aseprite
7z a -psalenzo ..\d.7z .
cd ..
