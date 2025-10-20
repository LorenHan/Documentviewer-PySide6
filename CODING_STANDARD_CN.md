# PySide6 Document Viewer 编码规范（中文）

> 版本：v2.1（更新日期：2025-09-27）  
> 参考：Qt C++ Coding Style（cppqt_coding_standard.md）、PEP 8，以及 `documentviewer` 包中的现有 PySide6 代码。

## 目录
1. [总则](#1-总则)  
2. [目录与工程结构](#2-目录与工程结构)  
3. [文件命名](#3-文件命名)  
4. [命名约定](#4-命名约定)  
5. [格式与排版](#5-格式与排版)  
6. [语句与控制流](#6-语句与控制流)  
7. [类与函数组织](#7-类与函数组织)  
8. [Qt / PySide6 特定规则](#8-qt--pyside6-特定规则)  
9. [资源、UI 与本地化](#9-资源ui-与本地化)  
10. [注释、文档与字符串](#10-注释文档与字符串)  
11. [错误处理与日志](#11-错误处理与日志)  
12. [测试与验证](#12-测试与验证)  
13. [版本控制与评审](#13-版本控制与评审)  
14. [维护与参考资料](#14-维护与参考资料)

---

## 1. 总则
- 以 Qt C++ 编码规范为基础，结合 Python 的 PEP 8 要求，保持 `documentviewer` 包中现有风格的一致性。
- 任何偏离约定的写法必须在代码评审中说明原因，并在此文档记录；默认遵循项目中当前最常见的写法。
- 示例均来自仓库现有代码（如 `documentviewer/mainwindow.py`、`documentviewer/imageviewer/imageviewer.py`），新代码应与之保持对齐。
- 采用模块化设计：各 Viewer 作为插件由 `ViewerFactory` 管理，主窗口负责应用流转和公共 UI。
  ```python
  self._factory = ViewerFactory(self.ui.viewArea, self)
  self._viewer = self._factory.viewer(file)
  ```

## 2. 目录与工程结构
- 根目录划分：
  - `documentviewer/` —— 核心应用包；  
  - `<viewer_name>/` —— 各 Viewer 子包（例如 `jsonviewer/`、`imageviewer/`）；  
  - `images/` —— 公共资源；  
  - `tools/`、`scripts/` —— 辅助脚本（可选）。
- UI 与资源文件与其生成物放在同级目录，禁止手动修改 `_ui.py`、`_rc.py`。
- 目录示例：
  ```text
  documentviewer/
    main.py
    mainwindow.py
    mainwindow.ui
    mainwindow_ui.py
    documentviewer.qrc
    documentviewer_rc.py
    viewerfactory.py
    abstractviewer.py
    jsonviewer/
      jsonviewer.py
    imageviewer/
      imageviewer.py
    images/
      qt-logo.png
  scripts/
    regenerate_ui.bat
  ```

### 2.1 推荐目录结构（2025）
```text
project-root/
  documentviewer/                 # 应用包（可导入）
    __init__.py
    main.py                       # 入口（也可放仓库根目录）
    mainwindow.py
    viewerfactory.py
    abstractviewer.py
    viewers/                      # 可插拔 Viewers
      jsonviewer/
        __init__.py
        jsonviewer.py
      pdfviewer/
        __init__.py
        pdfviewer.py
        zoomselector.py
      imageviewer/
        __init__.py
        imageviewer.py
      txtviewer/
        __init__.py
        txtviewer.py
    ui/                           # Designer 表单 + 生成包装
      mainwindow.ui
      mainwindow_ui.py            # 生成文件（禁止手改）
    resources/                    # QRC + 资源
      documentviewer.qrc
      documentviewer_rc.py        # 生成文件（禁止手改）
      images/
        qt-logo.png
        ...
    i18n/                         # 翻译（.ts/.qm）
      documentviewer_zh_CN.ts
      ...
  tests/                          # 单元测试
    test_recentfiles.py
    test_jsonmodel.py
  examples/                       # 示例文件（便于手测）
    sample.json
    sample.pdf
  scripts/                        # 开发辅助脚本
    regenerate_ui.bat
    regenerate_rc.bat
  tools/                          # 可选工具
  docs/                           # 项目文档
    README.md
    CODING_STANDARD_EN.md
    CODING_STANDARD_CN.md
  packaging/
    pysidedeploy.spec
```
说明：
- 生成文件（`*_ui.py`、`*_rc.py`）禁止手工修改；统一放在 `ui/`、`resources/` 或与源码同层，需保持一致性。
- Viewer 放于 `documentviewer/viewers/<name>/`，由 `ViewerFactory` 统一注册与创建。

## 3. 文件命名
| 类型 | 规则 | 示例 |
| --- | --- | --- |
| Python 模块 / 包 | `lower_snake_case` | `recentfiles.py`, `viewerfactory.py` |
| Viewer 子包 | 小写拼合单词 | `pdfviewer`, `jsonviewer` |
| Qt Designer 表单 | `ComponentName.ui` | `mainwindow.ui` |
| 生成的 UI 模块 | `ComponentName_ui.py` | `mainwindow_ui.py` |
| 资源集合 | `<name>.qrc` / `<name>_rc.py` | `documentviewer.qrc` |
| 图片与图标 | 小写 + 连字符/下划线 | `zoom-in.png` |
| 文档 | 主题 + `.md` | `README.md`, `CODING_STANDARD_CN.md` |

## 4. 命名约定
### 4.1 模块、类、枚举
- 类使用大驼峰（PascalCase）命名，例如 `MainWindow`、`ImageViewer`。抽象基类需要突出职责，例如 `AbstractViewer`。
  ```python
  from PySide6.QtWidgets import QMainWindow

  class MainWindow(QMainWindow):
      def __init__(self, parent=None):
          super().__init__(parent)
          self.ui = Ui_MainWindow()
  ```
- Qt 风格的缩写保持大驼峰写法（首字母缩写同样按首字母大写拼写），如 `QKeySequence`、`QImageReader`。
  ```python
  from PySide6.QtGui import QIcon, QKeySequence

  icon = QIcon.fromTheme(
      QIcon.ThemeIcon.ZoomIn,
      QIcon(":/demos/documentviewer/images/zoom-in.png"),
  )
  self.zoom_in_act.setShortcut(QKeySequence.StandardKey.ZoomIn)
  ```
- 枚举类型名称仍使用大驼峰（PascalCase），成员根据语义采用首字母大写或全大写方式，与现有代码保持一致：
  ```python
  class RemoveReason(Enum):
      Other = auto()
      Duplicate = auto()
  ```

  ```python
  class ViewerState(Enum):
      Loading = auto()
      Ready = auto()
      Error = auto()
  ```
- 变量在需要时再声明或赋值，避免提前占位造成作用域混乱：
  ```python
  self._viewer = self._factory.viewer(file)
  if not self._viewer:
      nf = QDir.toNativeSeparators(fileName)
      self.statusBar().showMessage(f"File {nf} can't be opened.")
      return False
  ```

### 4.2 函数、方法、槽函数
- 公共方法遵循小驼峰（camelCase）命名，例如 `openFile`、`saveSettings`、`printDocument`。
  ```python
  def openFile(self, fileName):
      file = QFile(fileName)
      if not file.exists():
          nf = QDir.toNativeSeparators(fileName)
          self.statusBar().showMessage(f"File {nf} could not be opened")
          return False

      fileInfo = QFileInfo(file)
      self._currentDir = fileInfo.dir()
      self._recentFiles.addFile(fileInfo.absoluteFilePath())
      return True
  ```
- 槽函数命名采用 `on<对象><信号>`，并使用 `@Slot` 装饰器声明参数类型：
  ```python
  @Slot(int)
  def onActionOpenTriggered(self):
      file_dialog = QFileDialog(self, self.tr("打开文档"),
                                self._currentDir.absolutePath())
      while (file_dialog.exec() == QDialog.DialogCode.Accepted
             and not self.openFile(file_dialog.selectedFiles()[0])):
          pass
  ```
- 内部辅助函数推荐使用 `_lower_snake_case` 与公开 API 区分；历史代码中 `_recentFilesCountChanged` 等沿用 Qt 命名，新逻辑可逐步迁移：
  ```python
  def _normalize_file_path(self, file_path: str) -> str:
      return QDir.toNativeSeparators(file_path)
  ```

  ```python
  def _recent_files_count_changed(self, count: int) -> None:
      self.ui.actionRecent.setText(f"{count} recent files")
  ```
- 典型的类结构示例：
  ```python
  class RecentFiles(QObject):
      countChanged = Signal(int)

      def addFile(self, file_path: str) -> None:
          if file_path in self._items:
              return
          self._items.append(file_path)
          self.countChanged.emit(len(self._items))

      @Slot()
      def clear(self) -> None:
          self._items.clear()
          self.countChanged.emit(0)
  ```

### 4.3 变量、属性、常量
- 局部变量使用 `lower_snake_case` 并保持语义清晰，单字母仅用于循环计数或短暂临时值：
  ```python
  target_size = self.image_label.parentWidget().size()
  initial_scale = min(
      target_size.width() / self.image_size.width(),
      target_size.height() / self.image_size.height(),
  )
  ```
- 受保护/私有属性使用单下划线前缀，如 `self._viewer`、`self._recentFiles`：
  ```python
  self._currentDir = QDir()
  self._viewer = None
  self._recentFiles = RecentFiles(self.ui.actionRecent)
  ```
- 常量使用 `UPPER_SNAKE_CASE` 表达，并集中在模块顶部声明：
  ```python
  ABOUT_TEXT = (
      "A Widgets application to display and print JSON, "
      "text and PDF files."
  )

  MENU_NAME = "qtFileMenu"
  ```
- 一行仅写一个赋值语句，避免 `a = b = 0` 这类链式赋值影响可读性：
  ```python
  def __init__(self, parent=None):
      super().__init__(parent)
      self._maxFiles = DEFAULT_MAX_FILES
      self._files = []
  ```

### 4.4 Qt 接口与内部命名
- 面向 Qt 的公共 API、Slot 使用 camelCase：如 `openFile`、`saveSettings`、`onActionOpenTriggered`。
- 纯 Python 内部辅助函数使用 `_snake_case`，用于与 Qt 接口区分：如 `_normalize_path`、`_recent_files_count_changed`。
- 命名尽量语义化，避免难懂缩写；缩写按 Qt 风格处理（如 `QImageReader`、`QKeySequence`）。

## 5. 格式与排版
### 5.1 缩进与结构
- 统一使用 4 个空格缩进，不使用 Tab；嵌套块按层次排布：
  ```python
  def resetViewer(self):
      if not self._viewer:
          return
      self.saveViewerSettings()
      self._viewer.cleanup()
  ```
- 在类和函数内部按逻辑分组，使用空行隔开初始化、信号连接等语句：
  ```python
  self.ui.actionOpen.triggered.connect(self.onActionOpenTriggered)
  self.ui.actionAbout.triggered.connect(self.onActionAboutTriggered)

  self._recentFiles = RecentFiles(self.ui.actionRecent)
  self._recentFiles.countChanged.connect(self._recent_files_count_changed)
  ```

### 5.2 行宽
- 代码行长度控制在 100 列以内，必要时对长字符串进行拆分：
  ```python
  ABOUT_TEXT = (
      "A Widgets application to display and print JSON, "
      "text and PDF files. Demonstrates various features "
      "to use in widget applications."
  )
  ```
- 注释与文档字符串尽量控制在 80 列左右：
  ```python
  """PySide6 port of the Qt Document Viewer demo from Qt v6.x"""
  ```

### 5.3 换行与续行
- 使用括号或方括号包裹多行表达式，避免反斜杠续行：
  ```python
  while (dialog.exec() == QDialog.DialogCode.Accepted
         and not self.openFile(dialog.selectedFiles()[0])):
      pass
  ```
- 拆分逻辑或算术表达式时，将运算符放在新行开头以突出结构：
  ```python
  total = (
      value
      + extra
      + adjustment
  )
  ```
- 链式调用或函数参数换行时，保持四空格缩进，与 `imageviewer.py` 中的写法一致：
  ```python
  icon = QIcon.fromTheme(
      QIcon.ThemeIcon.ZoomIn,
      QIcon(":/demos/documentviewer/images/zoom-in.png"),
  )
  ```

### 5.4 空行与分组
- 使用单个空行分隔不同的逻辑块，保持结构清晰：
  ```python
  self.ui.actionRecent.setMenu(menu)
  menu.fileOpened.connect(self.openFile)

  button = self.ui.mainToolBar.widgetForAction(self.ui.actionRecent)
  if button:
      self.ui.actionRecent.triggered.connect(button.showMenu)
  ```
- 顶层函数或类之间保持两个空行，类内方法之间保持一个空行：
  ```python
  class ImageViewer(AbstractViewer):

      def init(self, file, parent, mainWindow):
          ...

      def setupImageUi(self):
          ...
  ```

### 5.5 空格规则
- 为二元运算符两侧添加单个空格：
  ```python
  width = size.width() / device_pixel_ratio
  ```
- 控制语句与条件之间保留空格：
  ```python
  if self._viewer:
      self._viewer.printingEnabledChanged.connect(self.ui.actionPrint.setEnabled)
  ```
- 参数默认值和类型注解遵循 `name: Type = value` 的间隔方式：
  ```python
  def viewer(self, file: QFile) -> AbstractViewer | None:
      ...
  ```
- 不在括号内侧或行尾添加多余空格：
  ```python
  self.statusBar().showMessage(f"{count} recent files")
  ```

### 5.6 语句粒度
- 每行只写一条语句，避免 `if foo: bar()` 这样的紧凑写法：
  ```python
  if not file.exists():
      nf = QDir.toNativeSeparators(fileName)
      self.statusBar().showMessage(f"File {nf} could not be opened")
      return False
  ```
- 使用提前返回等跳转语句后，不再编写多余的 `else` 块，除非为了对称性：
  ```python
  if not self._viewer:
      nf = QDir.toNativeSeparators(fileName)
      self.statusBar().showMessage(f"File {nf} can't be opened.")
      return False

  self.ui.actionPrint.setEnabled(self._viewer.hasContent())
  ```

## 6. 语句与控制流
- 条件分支保持对称，当某分支包含多行逻辑时同时使用代码块包裹：
  ```python
  if dlg.exec() == QDialog.DialogCode.Accepted:
      self.printDocument(printer)
  else:
      self.statusMessage("Printing canceled!", type)
      return
  ```
- 将复杂条件拆分为具名变量，减少嵌套深度：
  ```python
  needs_downscale = (
      self.image_size.width() > target_size.width()
      or self.image_size.height() > target_size.height()
  )
  if needs_downscale:
      self.doSetScaleFactor(initial_scale)
  ```
- 使用 `match` / `case` 时为每个分支提供显式处理，必要时调用辅助函数：
  ```python
  match remove_reason:
      case RemoveReason.Duplicate:
          return
      case RemoveReason.Other:
          self._files.remove(file_name)
      case _:
          self._files.clear()
  ```
- 在循环中使用跳转语句前，尽量抽出布尔变量保持主体清晰：
  ```python
  while i < len(self._files):
      file_name = self._files[i]
      file_missing = not testFileAccess(file_name)
      if file_missing:
          self._removeFile(file_name, RemoveReason.Other)
          continue
      i += 1
  ```

## 7. 类与函数组织
- 推荐顺序：类常量 → 信号 → `__init__` → 公共方法 → 受保护方法 → 私有/槽函数：
  ```python
  class ImageViewer(AbstractViewer):
      def __init__(self):
          super().__init__()
          self.formats = imageFormats()
          self.uiInitialized.connect(self.setupImageUi)

      def init(self, file, parent, mainWindow):
          ...
  ```
- 构造函数保持轻量，将重型逻辑拆分到辅助方法：
  ```python
  def init(self, file, parent, mainWindow):
      self.image_label = QLabel(parent)
      self.image_label.setScaledContents(True)
      super().init(file, self.image_label, mainWindow)
  ```
- 参数过多时考虑拆分为数据对象或使用关键字参数：
  ```python
  def initViewer(self, back, forward, help_action, tabs):
      tabs.clear()
      tabs.setVisible(self.supportsOverview())
  ```
- 公共方法提供 docstring，描述副作用与信号：
  ```python
  def saveSettings(self):
      """Persist window state and recent files to QSettings."""
      settings = QSettings()
      settings.setValue(settingsDir, self._currentDir.absolutePath())
  ```

- 抽象基类应显式声明：推荐使用 `abc.ABC` 与 `@abstractmethod` 约束 Viewer 必须实现的方法（`viewerName`、`supportedMimeTypes`、`init`、`hasContent`、`printDocument`）。
- 避免在 `__del__` 中做清理工作；依赖 Qt 父子关系和显式 `cleanup()`，在替换 Viewer 前进行释放与保存。

## 8. Qt / PySide6 特定规则
- 应用启动顺序：创建 `QApplication` → 设置元数据与资源 → 构造并显示主窗口 → 调用 `exec()`：
  ```python
  app = QApplication([])
  app.setWindowIcon(QIcon("./images/qt-logo.png"))

  window = MainWindow()
  window.show()
  sys.exit(app.exec())
  ```
- 信号与槽：声明 `Signal` 签名并在初始化时集中连接：
  ```python
  class AbstractViewer(QObject):
      uiInitialized = Signal()
      printingEnabledChanged = Signal(bool)

  self.ui.actionOpen.triggered.connect(self.onActionOpenTriggered)
  self._recentFiles.countChanged.connect(self._recent_files_count_changed)
  ```
- Viewer 注册：在 `ViewerFactory` 构造函数中添加并初始化插件：
  ```python
  for viewer in [PdfViewer(), JsonViewer(), TxtViewer(), ImageViewer()]:
      self._viewers[viewer.viewerName()] = viewer
      if viewer.isDefaultViewer():
          self._defaultViewer = viewer
  ```
- `QSettings` 访问集中定义键名，读写后调用 `sync()`：
  ```python
  settings = QSettings()
  settings.setValue(settingsDir, self._currentDir.absolutePath())
  settings.setValue(settingsMainWindow, self.saveState())
  settings.sync()
  ```
- 平台差异调用使用 `try/except` 捕获错误，并提供用户可见反馈：
  ```python
  try:
      ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
          "QtExamples.DocumentViewer"
      )
  except Exception as exc:
      print(f"Failed to set AppUserModelID: {exc}")
  ```

### 8.1 信号与槽连接方式
- 使用 `对象.信号.connect(槽函数)` 的直接绑定写法，保持在初始化阶段集中管理，便于审查：
  ```python
  self.ui.actionOpen.triggered.connect(self.onActionOpenTriggered)
  self.ui.actionAbout.triggered.connect(self.onActionAboutTriggered)
  self._recentFiles.countChanged.connect(self._recent_files_count_changed)
  ```
- 优先传递槽函数引用，确需额外参数时使用 `functools.partial` 或轻量级 lambda，并保持语句可读：
  ```python
  from functools import partial

  for action, viewer_name in self._viewerActions.items():
      action.triggered.connect(partial(self._switch_viewer, viewer_name))
  ```
- 跨对象连接时注意断开旧连接，避免悬挂槽函数：
  ```python
  if self._viewer:
      self._viewer.printingEnabledChanged.disconnect(self.ui.actionPrint.setEnabled)
  ```
- Viewer 内部信号建议在 `init()` 或 `initViewer()` 中完成注册，与 `MainWindow` 的公共信号保持一致风格：
  ```python
  self.uiInitialized.connect(self.setupImageUi)
  self.printingEnabledChanged.connect(self.ui.actionPrint.setEnabled)
  ```

- 避免使用 lambda 直接作为槽函数：
  - lambda 是匿名函数，无法通过名称做静态检查；参数签名错误、内部引用的成员改名等问题只会在运行时暴露；
  - 难以精确断开：`disconnect()` 需要同一个可调用对象，临时 lambda 无法复用；
  - 可读性与可测试性较差，调用栈也不直观。
- 推荐做法：
  - 使用具名槽函数/方法，并用 `@Slot(...)` 标注参数类型；
  - 需要额外实参时，优先使用 `functools.partial` 绑定，或在槽内使用 `self.sender()` 判别来源；
  - 严禁旧式字符串 `SIGNAL/SLOT` 连接方式。

### 8.2 QSettings 规范
- 所有 key 使用全大写下划线命名并集中定义，必要时使用 `beginGroup`/`endGroup` 管理分组：
  ```python
  SETTINGS_DIR = "WorkingDir"
  SETTINGS_MAIN_WINDOW = "MainWindow"
  SETTINGS_VIEWERS = "Viewers"
  SETTINGS_FILES = "RecentFiles"
  ```
- 读取时总是提供默认值与类型（如 `settings.value(key, default, type)`），写入后调用 `settings.sync()`。

### 8.3 模型/视图实现规范
- `QAbstractItemModel` 的覆写方法针对无效索引返回 `QModelIndex()`，不要返回 `None`。
- 统一使用 `createIndex` 创建索引；顶层元素的父索引应为 `QModelIndex()`。
- 若模型可编辑，请实现 `flags`/`setData` 并限制可编辑的列。

### 8.4 C++ → Python 移植注意事项
- 不要把 C++ 的 API 直接调用在 Python 对象上：用 `if not files:` 代替 `files.isEmpty()`；避免 `list.find(x)`，改用 `x in list_` 或谨慎使用 `list_.index(x)`。
- 避免 `.toString()`、`.toInt()`、`.toReal()` 等调用；改用 Python 内置类型转换（`str(...)`、`int(...)`、`float(...)`）。
- 断言型方法必须返回显式布尔值：例如 `hasContent()` 返回 `True/False`，不要返回“对象或 False”的表达式。
- 将魔法数字（如状态栏消息超时 `8000`）提取为模块级常量，例如 `STATUS_TIMEOUT_MS = 8000`。

## 9. 资源、UI 与本地化
- 使用 Qt Designer 维护 `.ui` 文件，修改后执行：
  ```bash
  pyside6-uic mainwindow.ui -o mainwindow_ui.py
  ```
- 更新 `.qrc` 后同步生成资源模块：
  ```bash
  pyside6-rcc documentviewer.qrc -o documentviewer_rc.py
  ```
- 资源路径统一使用 `:/前缀/路径` 形式，并在 `.qrc` 中维护别名。
- 可本地化字符串通过 `self.tr("...")` 包装；新增字符串需同步英文原文，便于翻译。

### 9.1 图标与资源使用
- 应用图标与动作图标优先使用 QRC 路径；使用主题图标时必须提供 QRC 回退：
  ```python
  icon = QIcon.fromTheme(QIcon.ThemeIcon.ZoomIn,
                         QIcon(":/demos/documentviewer/images/zoom-in.png"))
  app.setWindowIcon(QIcon(":/demos/documentviewer/images/qt-logo.png"))
  ```
- 重构资源时保持 alias 稳定，并更新 `.qrc`；打包（PySide deploy）时确保打入 QRC（参见 `documentviewer/pysidedeploy.spec`）。

### 9.2 语言与翻译策略
完整的本地化与翻译规范请见第 10 章（源语言、TS/QM 流程与翻译注释）。

## 10. 本地化与翻译
- 源语言统一为英文。所有传入 `tr()` 的字符串均使用英文编写。
- 翻译源文件放在 `documentviewer/i18n/` 下（.ts），编译产物（.qm）可放在同目录或 `dist/` 子目录。
- 建议在工作流中加入 lupdate/lrelease：
  ```bash
  pyside6-lupdate documentviewer -ts documentviewer/i18n/documentviewer_zh_CN.ts
  pyside6-lrelease documentviewer/i18n/documentviewer_zh_CN.ts
  ```
- 对不直观的文案，使用翻译注释（.ui 中 `/*: ... */` 或 `QCoreApplication.translate` 上下文中添加备注）。
- 保持上下文稳定（类名/对象名），减少重构导致的 TS 项变动。
- 避免在可翻译字符串中拼接，优先使用占位符与格式化。

## 11. 注释、文档与字符串
- 模块 docstring 说明用途与背景，例如：
  ```python
  """PySide6 port of the Qt Document Viewer demo from Qt v6.x"""
  ```
- 类/方法 docstring 描述职责、关键信号及副作用：
  ```python
  class RecentFileMenu(QMenu):
      """Menu that exposes the shared RecentFiles helper."""
  ```
- 行内注释只在逻辑不直观时使用，写在相关代码上方，并以 `#` + 空格开头：
  ```python
  # 确保工具栏按钮直接弹出最近文件菜单
  if button:
      self.ui.actionRecent.triggered.connect(button.showMenu)
  ```
- TODO/FIXME 采用 `# TODO(name, YYYY-MM-DD): 描述` 格式，并关联 Issue：
  ```python
  # TODO(alice, 2025-09-27): Support exporting viewer state as JSON
  ```

## 12. 错误处理与日志
- 面向用户的错误信息使用 `QMessageBox`、状态栏或其他 UI 反馈，而非 `print`：
  ```python
  QMessageBox.about(self, "About Document Viewer Demo", text)
  self.statusBar().showMessage(f"File {nf} could not be opened")
  ```
- 使用标准库 `logging` 输出调试信息：
  ```python
  import logging
  LOGGER = logging.getLogger(__name__)
  LOGGER.debug("Loading file %s", file_name)
  ```
- 错误消息包含路径或 MIME 等关键信息，同时避免泄露敏感数据：
  ```python
  nf = QDir.toNativeSeparators(fileName)
  self.statusBar().showMessage(f"File {nf} could not be opened")
  ```
- 捕获异常后恢复 UI 状态（如光标）或写入日志，保持应用可用性：
  ```python
  if orig_image.isNull():
      self.statusMessage(
          f"Cannot read file {name}:
{reader.errorString()}", "open"
      )
      self.disablePrinting()
      QGuiApplication.restoreOverrideCursor()
      return
  ```

### 日志规范
- 禁止使用 `print` 输出调试/错误信息，统一使用 `logging` 并在模块级创建记录器（例如 `LOGGER = logging.getLogger(__name__)`）。
- 入口（main）按需初始化日志；UI 相关路径保持简洁日志。
- 平台特定初始化（如 Windows AppUserModelID）需捕获并记录失败：
  ```python
  if sys.platform == "win32":
      try:
          ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('QtExamples.DocumentViewer')
      except Exception as exc:
          LOGGER.warning("Failed to set AppUserModelID: %s", exc)
  ```

## 13. 测试与验证
- 单元测试覆盖核心逻辑（`RecentFiles`、`JsonItemModel` 等），可使用 pytest 或 unittest：
  ```python
  def test_recent_files_add(tmp_path):
      sample = tmp_path / "demo.json"
      sample.write_text("{}")
      recent = RecentFiles()
      recent.addFile(str(sample))
      assert not recent.isEmpty()
  ```
- 手工冒烟检查：
  1. 启动应用；
  2. 打开 JSON/PDF/TXT/图片文件并验证渲染；
  3. 检查最近文件菜单、打印按钮状态；
  4. 重启应用确认窗口状态与最近文件持久化。
- 新增 Viewer 或功能时同步更新测试与示例资源。

### Lint 与类型检查
- 在 CI 中启用 linter（ruff/flake8）：禁止 `print`，检查导入、行宽与常见 PySide6 习惯用法。
- 结合 mypy 进行类型检查；针对 Qt 绑定类型可适当放宽或使用局部 `# type: ignore`。

### 本仓库的建议测试
- `RecentFiles`：添加/去重/容量限制、QSettings 读写往返。
- `JsonItemModel`：`index`/`parent` 关系、不合法索引返回、表头内容、可编辑列限制。

## 14. 版本控制与评审
- 保持原子提交，推荐 `type(scope): summary` 样式：
  ```text
  feat(viewer): add csv support
  ```
- 不提交生成物、缓存或个人配置（例如 `__pycache__/`、`.pyside6/`）。
- Merge Request/PR 中引用相关 Issue，提供测试证明或 UI 截图。
- 评审检查点：命名一致性、信号槽成对、资源注册、文档/测试更新。

## 15. 维护与参考资料
- 本指南每季度回顾，更新时同步中文与英文版并记录日期、作者、主要变更。
- 参考资料：
  - [Qt Coding Style](https://wiki.qt.io/Qt_Coding_Style)
  - [PEP 8 -- Style Guide for Python Code](https://peps.python.org/pep-0008/)
  - [Qt for Python 文档](https://doc.qt.io/qtforpython/)

---

> 若项目实践与本规范不一致，请先创建 Issue 讨论并在调整后更新本文件。
