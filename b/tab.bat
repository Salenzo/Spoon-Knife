for /f "usebackq delims=" %%i in (`vswhere.exe -latest -property installationPath`) do %comspec% /k "%%i\VC\Auxiliary\Build\vcvars32.bat"
cmake -DCMAKE_SYSTEM_VERSION=10.0.22621.0 -DCMAKE_BUILD_TYPE=RelWithDebInfo -DLAF_BACKEND=skia ^
  -DSKIA_DIR=..\c -DSKIA_LIBRARY_DIR=..\c\out\Release-x86 -DSKIA_LIBRARY=..\c\out\Release-x86\skia.lib ^
  -G Ninja ..\a
ninja aseprite
7z a -psalenzo ..\d.7z .
