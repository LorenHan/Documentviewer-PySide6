[app]

# 应用程序标题
title = pyside_app_demo

# 项目目录。通常假设 project_dir 是 input_file 的父目录
project_dir = E:\Flex\Python\PySide6\Documentviewer-PySide6\documentviewer

# 源文件路径
input_file = E:\Flex\Python\PySide6\Documentviewer-PySide6\documentviewer\main.py

# 生成可执行文件的输出目录，当前目录下面的Documentviewer文件夹，相对路径
exec_directory = ./Documentviewer

# .pyproject 项目文件路径
project_file = documentviewer.pyproject

# 应用程序图标 ./images/qt-logo.png
icon = ./images/qt-logo.png

[python]

# python 路径
python_path = C:\Python312\python.exe

# 需要安装的 python 包
packages = Nuitka

[qt]

# 使用的 qt 模块，逗号分隔
modules = PdfWidgets,Pdf,Gui,Core,Widgets,PrintSupport

# 应用程序使用的 qt 插件。仅与桌面部署相关。
plugins = xcbglintegrations,platforminputcontexts,iconengines,generic,printsupport,imageformats,egldeviceintegrations,platforms,styles,platforms/darwin,platformthemes,accessiblebridge

[nuitka]

# 使用 nuitka 的模式。接受 standalone 或 onefile。默认为 onefile。
mode = onefile

# (str) 指定任何额外的 nuitka 参数
extra_args = --quiet --noinclude-qt-translations
