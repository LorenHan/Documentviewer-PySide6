# PySide6 代码规范手册

## 1. 文件命名规范

### 1.1 Python 模块文件
- **规范**: 使用全小写字母
- **示例**:
  ```
  main.py
  mainwindow.py
  abstractviewer.py
  imageviewer.py
  recentfiles.py
  ```

### 1.2 UI 相关文件
- **规范**: UI 文件以 `_ui` 结尾，资源文件以 `_rc` 结尾
- **示例**:
  ```
  mainwindow_ui.py
  documentviewer_rc.py
  rc_documentviewer.py
  ```

### 1.3 目录命名
- **规范**: 使用全小写字母，将相关文件组织在同名文件夹中
- **示例**:
  ```
  imageviewer/
  pdfviewer/
  jsonviewer/
  txtviewer/
  ```

## 2. 注释规范

### 2.1 文件头注释
- **规范**: 每个文件必须包含版权信息和许可证声明
- **示例**:
  ```python
  # Copyright (C) 2023 The Qt Company Ltd.
  # SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
  from __future__ import annotations
  ```

### 2.2 模块注释
- **规范**: 在导入语句后添加模块功能描述
- **示例**:
  ```python
  """PySide6 port of the Qt Document Viewer demo from Qt v6.x"""
  ```

### 2.3 行内注释
- **规范**: 注释可以用中文或英文编写，用于解释复杂逻辑或重要操作
- **示例**:
  ```python
  # set AppUserModelID
  try:
      ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('QtExamples.DocumentViewer')
  except Exception as e:
      print(f"Failed to set AppUserModelID: {e}")

  # set application icon
  app.setWindowIcon(QIcon('./images/qt-logo.png'))
  ```

### 2.4 函数和类注释
- **规范**: 重要的函数和类应该有文档字符串
- **示例**:
  ```python
  def msgOpen(name, image):
      """打开文件并返回描述信息"""
      description = image.colorSpace().description() if image.colorSpace().isValid() else "unknown"
      return 'Opened "{0}", {1}x{2}, Depth: {3} ({4})'.format(
          QDir.toNativeSeparators(name),
          image.width(),
          image.height(),
          image.depth(),
          description
      )
  ```

## 3. 代码规范

### 3.1 导入语句
- **规范**: 按照标准库、第三方库、本地库的顺序导入，每种类型之间空一行
- **示例**:
  ```python
  import sys
  import os
  import ctypes
  from argparse import ArgumentParser, RawTextHelpFormatter

  from PySide6.QtWidgets import QApplication
  from PySide6.QtCore import QCoreApplication
  from PySide6.QtGui import QIcon

  from mainwindow import MainWindow
  ```

### 3.2 导入内容
- **规范**: 导入内容时，尽量使用括号包裹，避免使用通配符导入
- **示例**:
  ```python
  from PySide6.QtWidgets import (QDialog, QFileDialog, QMainWindow, QMessageBox)
  from PySide6.QtCore import (QDir, QFile, QFileInfo, QSettings, Slot)
  from PySide6.QtGui import (QPixmap, QImageReader, QIcon, QKeySequence,
                             QGuiApplication, QColorSpace, QPainter, QAction)
  ```

### 3.3 代码格式
- **规范**: 代码缩进使用4个空格，避免使用制表符
- **示例**:
  ```python
  # Correct
  app = QApplication([])
  self._currentDir = QDir()
  self._viewer = None
  count = 10
  result = a + b - c

  # Incorrect
  app=QApplication([])
  self._currentDir=QDir()
  count=10
  result=a+b-c
  ```

### 3.4 类定义
- **规范**: 类名使用驼峰命名法，类成员使用下划线分隔的单词
- **示例**:
  ```python
  from PySide6.QtCore import QObject


  class MainWindow(QMainWindow):

      def __init__(self, parent=None):
          super().__init__(parent)
          self.ui = Ui_MainWindow()

          self._currentDir = QDir()
          self._viewer = None
          self._recentFiles = RecentFiles()

      def closeEvent(self, event):
          self.saveSettings()
  ```

## 4. 命名规范

### 4.1 类名
- **规范**: 使用驼峰命名法
- **示例**:
  ```python
  class MainWindow(QMainWindow):
      pass

  class AbstractViewer(QObject):
      pass

  class RecentFiles(QObject):
      pass
  ```

### 4.2 函数名
- **规范**: 使用小写字母，单词之间用下划线分隔
- **示例**:
  ```python
  def onActionOpenTriggered(self):
      pass

  def onActionAboutTriggered(self):
      pass

  def saveSettings(self):
      pass
  ```

### 4.3 变量名
- **规范**: 使用小写字母，单词之间用下划线分隔
- **示例**:
  ```python
  def __init__(self):
      self._currentDir = QDir()
      self._viewer = None
      self._recentFiles = RecentFiles()
      self._file = None
      self._widget = None
  ```

### 4.4 常量
- **规范**: 使用大写字母，单词之间用下划线分隔
- **示例**:
  ```python
  DESCRIPTION = "A viewer for JSON, PDF and text files"
  DEFAULT_MAX_FILES = 10
  MENU_NAME = "qtFileMenu"

  ABOUT_TEXT = """A Widgets application to display and print JSON,
  text and PDF files. Demonstrates various features to use
  in widget applications: Using QSettings, query and save
  user preferences, manage file histories and control cursor
  behavior when hovering over widgets.
  """
  ```

### 4.5 设置键
- **规范**: 使用小写字母，单词之间用下划线分隔
- **示例**:
  ```python
  settingsDir = "WorkingDir"
  settingsMainWindow = "MainWindow"
  settingsViewers = "Viewers"
  settingsFiles = "RecentFiles"
  ```

## 5. UI 规范

### 5.1 UI 文件
- **规范**: UI 文件生成的部件应该直接连接信号和槽
- **示例**:
  ```python
  # UI file-generated widgets
  self.ui.actionOpen.triggered.connect(self.onActionOpenTriggered)
  self.ui.actionAbout.triggered.connect(self.onActionAboutTriggered)
  self.ui.scrollArea.setWidget(self._viewer.widget())

  # Code-created widgets
  self.image_label = QLabel(parent)
  self.image_label.setFrameShape(QLabel.Box)
  self.image_label.setAlignment(Qt.AlignCenter)
  ```

### 5.2 工具栏和菜单
- **规范**: 工具栏和菜单的 `objectName` 应该与标题一致
- **示例**:
  ```python
  def addToolBar(self, title):
      bar = self.mainWindow().addToolBar(title)
      name = title.replace(' ', '')
      bar.setObjectName(name)
      self._toolBars.append(bar)
      return bar

  def addMenu(self, title):
      menu = QMenu(title, self.menuBar())
      menu.setObjectName(title)
      self.menuBar().insertMenu(self._uiAssets_help, menu)
      self._menus.append(menu)
      return menu
  ```

## 6. 信号和槽规范

### 6.1 信号和槽定义
- **规范**: 使用 `@Slot()` 装饰器定义槽函数
- **示例**:
  ```python
  @Slot(int)
  def _recentFilesCountChanged(self, count):
      self.ui.actionRecent.setText(f"{count} recent files")

  @Slot()
  def onActionOpenTriggered(self):
      fileDialog = QFileDialog(self, "Open Document",
                               self._currentDir.absolutePath())

  @Slot(str)
  def openFile(self, fileName):
      file = QFile(fileName)
      # Handle file opening logic
  ```

### 6.2 信号和槽命名
- **规范**: 信号和槽的命名应该清晰且具有描述性
- **示例**:
  ```python
  # Event handler slots
  def onActionOpenTriggered(self):
      pass

  def onActionAboutTriggered(self):
      pass

  # Private slots
  @Slot(int)
  def _recentFilesCountChanged(self, count):
      pass

  # Public slots
  @Slot()
  def print_(self):
      pass
  ```

## 7. 初始化规范

### 7.1 初始化函数
- **规范**: `__init__` 函数应该包含所有初始化逻辑
- **示例**:
  ```python
  def __init__(self, parent=None):
      super().__init__(parent)
      self.ui = Ui_MainWindow()

      # UI initialization
      self.ui.setupUi(self)

      # Signal-slot connections
      # 注意不要使用lambda连接，编译时候lambda连接不会报错，但是运行时候有问题
      self.ui.actionOpen.triggered.connect(self.onActionOpenTriggered) 
      self.ui.actionAbout.triggered.connect(self.onActionAboutTriggered)
      self.ui.actionAboutQt.triggered.connect(self.onActionAboutQtTriggered)
  ```

### 7.2 初始化逻辑
- **规范**: 初始化逻辑应该清晰且易于理解
- **示例**:
  ```python
  if self._viewer:
      self._viewer.printingEnabledChanged.connect(self.ui.actionPrint.setEnabled)
      self.ui.actionPrint.triggered.connect(self._viewer.print_)
      self._viewer.showMessage.connect(self.statusBar().showMessage)

  button = self.ui.mainToolBar.widgetForAction(self.ui.actionRecent)
  if button:
      self.ui.actionRecent.triggered.connect(button.showMenu)
  ```

### 7.3 信号定义
- **规范**: 信号定义应该清晰且易于理解
- **示例**:
  ```python
  # Signal definitions
  countChanged = Signal(int)
  printingEnabledChanged = Signal(bool)
  showMessage = Signal(str, int)

  # Signal connections
  self._recentFiles.countChanged.connect(self._recentFilesCountChanged)
  menu.fileOpened.connect(self.openFile)
  self.uiInitialized.connect(self.setupImageUi)
  ```

## 8. 清理规范

### 8.1 try-except 语句
- **规范**: 使用 try-except 语句处理可能的异常
- **示例**:
  ```python
  try:
      ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('QtExamples.DocumentViewer')
  except Exception as e:
      print(f"Failed to set AppUserModelID: {e}")
  ```

### 8.2 析构函数
- **规范**: 使用 `__del__` 函数进行资源清理
- **示例**:
  ```python
  def __del__(self):
      self.cleanup()

  def cleanup(self):
      if self._file:
          self._file = None
      self._menus.clear()
      self._toolBars.clear()
  ```

## 9. 字符串格式化规范

### 9.1 f-string
- **规范**: 使用 f-string 进行字符串格式化
- **示例**:
  ```python
  self.ui.actionRecent.setText(f"{count} recent files")
  self.statusBar().showMessage(f'Available viewers: {viewers}')
  print(f"Failed to set AppUserModelID: {e}")
  ```

### 9.2 format
- **规范**: 使用 `format` 方法进行字符串格式化
- **示例**:
  ```python
  return 'Opened "{0}", {1}x{2}, Depth: {3} ({4})'.format(
      QDir.toNativeSeparators(name),
      image.width(),
      image.height(),
      image.depth(),
      description
  )
  ```

## 10. 类型注解规范

### 10.1 Future Annotations
- **规范**: 使用 `from __future__ import annotations`
- **示例**:
  ```python
  from __future__ import annotations
  ```

### 10.2 类型注解
- **规范**: 使用类型注解提高代码可读性和可维护性
- **示例**:
  ```python
  def supportedMimeTypes() -> list:
      return []

  def isEmpty(self) -> bool:
      return not self.hasContent()
  ```

## 参考
- [PEP 8 -- Style Guide for Python Code](https://peps.python.org/pep-0008/) - Python官方代码风格指南。
- [Qt C++ Coding Style](https://wiki.qt.io/Qt_Coding_Style) - Qt官方C++编码规范，PySide6作为Qt的Python绑定，其API设计和最佳实践深受其影响。
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) - 广泛使用的Python风格指南，提供了许多实用的建议。
- [The Zen of Python (PEP 20)](https://peps.python.org/pep-0020/) - Python之禅，理解Python设计哲学的基础。
