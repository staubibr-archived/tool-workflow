set workflow=%1
set input=%2
set output=%3
set params=%4

set OSGEO4W_ROOT=D:\Programs\OSGeo4W64

call "%OSGEO4W_ROOT%\bin\o4w_env.bat"
call "%OSGEO4W_ROOT%\bin\qt5_env.bat"
call "%OSGEO4W_ROOT%\bin\py3_env.bat"

path %OSGEO4W_ROOT%\apps\qgis\bin;%PATH%
set QGIS_PREFIX_PATH=%OSGEO4W_ROOT%\apps\qgis

set GDAL_FILENAME_IS_UTF8=YES

set VSI_CACHE=TRUE
set VSI_CACHE_SIZE=1000000
set QT_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\qgis\qtplugins;%OSGEO4W_ROOT%\apps\qt5\plugins

set PYTHONPATH=%OSGEO4W_ROOT%\apps\qgis\python
set PYTHONHOME=%OSGEO4W_ROOT%\apps\Python37
set PYTHONPATH=%OSGEO4W_ROOT%\apps\Python37\lib\site-packages;%PYTHONPATH%
set PYTHONPATH=%OSGEO4W_ROOT%\apps\qgis\python\plugins;%PYTHONPATH%

set QT_QPA_PLATFORM_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\Qt5\plugins\platforms
set QGIS_PREFIX_PATH=%OSGEO4W_ROOT%\apps\qgis

if "%~4" == "" (
    python D:\Development\devs-web-env\tool-workflow\main.py --workflow %workflow% --input %input% --output %output%
) else (
    python D:\Development\devs-web-env\tool-workflow\main.py --workflow %workflow% --input %input% --output %output% --params %params%
)

exit 0