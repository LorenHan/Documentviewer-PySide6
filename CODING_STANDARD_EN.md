# PySide6 Document Viewer Coding Standard

> Version: v2.1 (Updated: 2025-09-27)  
> References: Qt C++ Coding Style (`cppqt_coding_standard.md`), PEP 8, and the PySide6 code that already exists under `documentviewer`.

## Table of Contents
1. [General Principles](#1-general-principles)  
2. [Project Layout & Structure](#2-project-layout--structure)  
3. [File Naming Rules](#3-file-naming-rules)  
4. [Naming Conventions](#4-naming-conventions)  
5. [Formatting & Layout](#5-formatting--layout)  
6. [Statements & Control Flow](#6-statements--control-flow)  
7. [Classes & Function Organization](#7-classes--function-organization)  
8. [Qt / PySide6 Specific Rules](#8-qt--pyside6-specific-rules)  
9. [Resources & UI](#9-resources--ui)  
10. [Localization & Translation](#10-localization--translation)  
11. [Comments, Docs & Strings](#11-comments-docs--strings)  
12. [Error Handling & Logging](#12-error-handling--logging)  
13. [Testing & Verification](#13-testing--verification)  
14. [Version Control & Reviews](#14-version-control--reviews)  
15. [Maintenance & References](#15-maintenance--references)

---

## 1. General Principles
- Use the Qt C++ coding style as the baseline and blend in PEP 8 guidance so that new code matches what already ships in the `documentviewer` package.
- Any exception must be justified during review and recorded here; by default, follow the dominant pattern that the current code base uses.
- Examples come from existing sources such as `documentviewer/mainwindow.py` and `documentviewer/imageviewer/imageviewer.py`; align new code with those patterns.
- Keep the modular architecture: viewers act as plug-ins managed by `ViewerFactory`, while the main window coordinates application flow and shared UI.

## 2. Project Layout & Structure
- Recommended layout (2025). Legacy layout remains accepted until migrated:
  ```text
  project-root/
    documentviewer/                 # App package (importable)
      __init__.py
      main.py                       # Entry (or keep at repo root as needed)
      mainwindow.py
      viewerfactory.py
      abstractviewer.py
      viewers/                      # Pluggable viewers
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
      ui/                           # Designer forms + generated wrappers
        mainwindow.ui
        mainwindow_ui.py            # generated (do not edit)
      resources/                    # QRC + assets
        documentviewer.qrc
        documentviewer_rc.py        # generated (do not edit)
        images/
          qt-logo.png
          ...
      i18n/                         # Translations (.ts/.qm)
        documentviewer_zh_CN.ts
        ...
    tests/                          # Unit tests (pytest/unittest)
      test_recentfiles.py
      test_jsonmodel.py
    examples/                       # Sample files for manual testing
      sample.json
      sample.pdf
    scripts/                        # Dev helpers
      regenerate_ui.bat
      regenerate_rc.bat
    tools/                          # Optional CLI/tools
    docs/                           # Project docs
      README.md
      CODING_STANDARD_EN.md
      CODING_STANDARD_CN.md
    packaging/
      pysidedeploy.spec
  ```
  Notes:
  - Never hand-edit generated `*_ui.py` and `*_rc.py`.
  - Viewers live under `documentviewer/viewers/<name>/` and register via `ViewerFactory`.
- Top-level layout:
  - `documentviewer/` — core application package;  
  - `<viewer_name>/` — per-viewer subpackages (`jsonviewer/`, `imageviewer/`, etc.);  
  - `images/` — shared assets;  
  - `tools/`, `scripts/` — optional helper utilities.
- Store generated files beside their sources and never hand-edit `_ui.py` or `_rc.py` modules.
- Recommended layout:
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

## 3. File Naming Rules
| Type | Rule | Example |
| --- | --- | --- |
| Python modules / packages | `lower_snake_case` | `recentfiles.py`, `viewerfactory.py` |
| Viewer subpackages | Lowercase concatenated words | `pdfviewer`, `jsonviewer` |
| Qt Designer forms | `ComponentName.ui` | `mainwindow.ui` |
| Generated UI modules | `ComponentName_ui.py` | `mainwindow_ui.py` |
| Resource collections | `<name>.qrc` / `<name>_rc.py` | `documentviewer.qrc` |
| Images & icons | Lowercase + hyphen/underscore | `zoom-in.png` |
| Docs | Topic + `.md` | `README.md`, `CODING_STANDARD_EN.md` |

## 4. Naming Conventions
### 4.1 Modules, Classes, Enums
- Classes use PascalCase, e.g. `MainWindow`, `ImageViewer`; abstract bases highlight their role, such as `AbstractViewer`.
- Avoid cryptic abbreviations. Keep acronyms camel-cased in Qt style, for example `QKeySequence`, `QImageReader`.
- Enums use PascalCase types with capitalized members that describe intent:
  ```python
  class RemoveReason(Enum):
      Other = auto()
      Duplicate = auto()
  ```
- Declare or assign variables close to where they are first needed to keep scope tight.

### 4.2 Functions, Methods, Slots
- Public APIs adopt Qt-styled camelCase names: `openFile`, `saveSettings`, `printDocument`.
- Slot names follow `on<Widget><Signal>` and carry an explicit `@Slot` decorator:
  ```python
  @Slot(int)
  def onActionOpenTriggered(self):
      ...
  ```
- Internal helpers may use `_lower_snake_case` to distinguish them from public Qt-facing methods (see `_recentFilesCountChanged` in `mainwindow.py`).
  In general, prefer `_snake_case` for internal helpers and camelCase only where interacting with Qt conventions.

### 4.3 Variables, Attributes, Constants
- Local variables use `lower_snake_case` and meaningful names; single letters are reserved for simple counters or short-lived temporaries.
- Protected/private attributes start with a single underscore, e.g. `self._viewer`, `self._recentFiles`.
- Constants are `UPPER_SNAKE_CASE`, such as `ABOUT_TEXT`, `MENU_NAME`.

Example constants used in this project:
```python
ABOUT_TEXT = (
    "A Widgets application to display and print JSON, "
    "text and PDF files."
)

MENU_NAME = "qtFileMenu"
```
- Keep one assignment per line; prefer explicit unpacking instead of chained assignments unless setting obvious constants.

## 5. Formatting & Layout
### 5.1 Indentation & Structure
- Four spaces per level; do not mix tabs. Follow the “attached brace” mindset from the Qt guide by placing the colon at the end of the statement and indenting the block on the next line.
- Group related statements inside functions and favor early returns to limit nesting depth.

### 5.2 Line Length
- Limit code lines to 100 characters. When wrapping strings, use implicit concatenation via parentheses or helper utilities such as `textwrap.dedent`.
- Keep comments and docstrings under 80 characters where practical.

### 5.3 Line Breaks & Continuations
- Wrap long expressions with parentheses, brackets, or braces; avoid backslash continuations.
- When breaking logical or arithmetic expressions, place the operator at the start of the new line, mirroring the Qt C++ rule:
  ```python
  while (dialog.exec() == QDialog.DialogCode.Accepted
         and not self.openFile(dialog.selectedFiles()[0])):
      pass

  total = (value
           + extra
           + adjustment)
  ```
- Align chained calls with either a four-space indent or parameter indentation, matching the patterns already present in viewer code.

### 5.4 Blank Lines & Grouping
- Use a single blank line to separate logical sections, properties, or helper blocks. Avoid multiple consecutive blank lines.
- Keep two blank lines between top-level declarations and one blank line between methods inside a class, matching current files.

### 5.5 Spacing Rules
- Surround binary operators with a single space: `width = size.width() / device_pixel_ratio`.
- Keep a space between control-flow keywords and conditions: `if condition:`, `for path in paths:`.
- Add spaces after commas; follow `name: Type = value` for annotations and defaults.
- Do not add stray spaces before colons, inside parentheses, or at the end of lines.

### 5.6 Statement Granularity
- Keep one statement per line; avoid compact forms such as `if foo: bar()`.
- After a jump statement (`return`, `break`, `continue`), omit a trailing `else` unless symmetry improves readability. This mirrors the Qt guideline on jump statements.

## 6. Statements & Control Flow
- Maintain symmetry in branch blocks: if one branch spreads across multiple lines, expand the matching branch as well.
- Break complex conditions into named booleans or helper functions to reduce nesting depth.
- When using Python `match`/`case`, align each `case` with `match`, handle every path explicitly, and avoid implicit fallthrough by delegating to helper functions instead.
- When conditions span multiple lines inside loops, prefer temporary variables or parentheses so the intent stays clear before `continue`, `break`, or `return`.

## 7. Classes & Function Organization
- Recommended order: class constants → signals → `__init__` → public methods → protected helpers → private utilities/slots.
- Keep constructors lightweight; move IO or heavy initialization into helper methods such as `ImageViewer.openFile`.
- Functions with more than five parameters should be refactored or accept keyword/data objects to preserve readability and testability.
- Public methods need docstrings that summarize behavior, side effects, and emitted signals; describe user interaction steps for UI-heavy methods.
- Abstract bases should be explicit: use `abc.ABC` with `@abstractmethod` for required viewer methods (`viewerName`, `supportedMimeTypes`, `init`, `hasContent`, `printDocument`).
- Avoid cleanup work in `__del__`; rely on Qt parent-child ownership and explicit `cleanup()` when replacing viewers.

## 8. Qt / PySide6 Specific Rules
- Startup flow: create `QApplication` → set application identity and load resources → construct and show the main window → call `exec()`.
- Signals & slots:
  - Declare signatures with `Signal(...)`; decorate slots with `@Slot(...)`.
  - Group connection statements for readability, as in `MainWindow.__init__` where multiple `triggered.connect` calls appear together.
  - Avoid lambdas as slot targets. They are anonymous (hard to disconnect), bypass any name-based checks, and hide parameter mismatches until runtime. Prefer named slots with `@Slot(...)` and use `functools.partial` to bind extra arguments when needed. Never use legacy string-based `SIGNAL/SLOT` connections.
- Viewer registration: custom viewers must implement `viewerName`, `supportedMimeTypes`, `hasContent`, `init`, etc., and register in `ViewerFactory`.
- `QSettings`: define key constants centrally, pass defaults when reading, and call `settings.sync()` after writes.
- Platform hooks (e.g., Windows AppUserModelID) need `try/except` guards; report failures through the status bar or logging.

### 8.1 QSettings conventions
- Define keys as `UPPER_SNAKE_CASE` constants in one place; group with `beginGroup`/`endGroup` for viewer state.
  ```python
  SETTINGS_DIR = "WorkingDir"
  SETTINGS_MAIN_WINDOW = "MainWindow"
  SETTINGS_VIEWERS = "Viewers"
  SETTINGS_FILES = "RecentFiles"
  ```
- Provide default types/values on reads (e.g., `settings.value(key, default, type)`), and call `settings.sync()` after writes.

### 8.2 Model/View implementation rules
- `QAbstractItemModel` overrides return `QModelIndex()` for invalid indices, not `None`.
- Use `createIndex` consistently; the parent of top-level items is `QModelIndex()`.
- If editability is intended, implement `flags`/`setData` and restrict edits to specific columns.

### 8.3 Porting pitfalls (C++ → Python)
- Replace `list.isEmpty()` with `if not list_obj:`; avoid `list.find(x)` on Python lists; use `x in list_obj`/`list_obj.index(x)` carefully.
- Avoid `.toString()`, `.toInt()`, `.toReal()`; prefer native Python types (`str(value)`, `int(value)`, `float(value)`).
- Return explicit booleans from predicates (e.g., `hasContent()` returns `True/False`), do not rely on object truthiness.
- Extract magic numbers (timeouts like `8000`) into module-level constants, for example `STATUS_TIMEOUT_MS = 8000`.

## 9. Resources & UI
- Maintain `.ui` files with Qt Designer and regenerate Python wrappers after edits:
  ```bash
  pyside6-uic mainwindow.ui -o mainwindow_ui.py
  ```
- Rebuild resource modules whenever `.qrc` files change:
  ```bash
  pyside6-rcc documentviewer.qrc -o documentviewer_rc.py
  ```
- Use Qt resource prefixes (`:/prefix/path`) consistently and keep aliases updated in the `.qrc` file.
- Wrap localizable strings with `self.tr("...")` and provide the English source text when adding translations.

### 9.1 Icons and resource usage
- Prefer QRC resource paths for application and action icons. Use theme icons with explicit QRC fallbacks:
  ```python
  icon = QIcon.fromTheme(QIcon.ThemeIcon.ZoomIn,
                         QIcon(":/demos/documentviewer/images/zoom-in.png"))
  app.setWindowIcon(QIcon(":/demos/documentviewer/images/qt-logo.png"))
  ```
- Keep resource aliases stable when refactoring; update `.qrc` accordingly.
- When packaging (PySide deploy), ensure QRC resources are included (see `documentviewer/pysidedeploy.spec`).

### 9.2 Language & translation policy
See Section 10 for full localization guidance (source language, TS/QM workflow, and translator notes).

## 10. Localization & Translation
- Source language is English. All strings passed to `tr()` are written in English.
- Store translation sources under `documentviewer/i18n/` with `.ts` files; compiled `.qm` under the same or a `dist` subfolder.
- Run lupdate/lrelease tooling as part of the workflow:
  ```bash
  pyside6-lupdate documentviewer -ts documentviewer/i18n/documentviewer_zh_CN.ts
  pyside6-lrelease documentviewer/i18n/documentviewer_zh_CN.ts
  ```
- Provide translator comments for non-obvious strings using `/*: ... */` in `.ui` or `QtCore.QCoreApplication.translate` contexts.
- Prefer stable contexts: class names or `QObject`-based contexts to keep TS entries stable across refactors.
- Avoid string concatenation in translatable messages; use placeholders and `arg`-style formatting.

## 11. Comments, Docs & Strings
- Module docstrings explain the module’s purpose and background (see `main.py`).
- Class/method docstrings describe responsibilities, emitted signals, key workflows, and any threading assumptions.
- Inline comments only cover non-obvious logic. Place them directly above the relevant code with a single leading `#`:
  ```python
  # Ensure the toolbar button opens the recent file menu directly
  if button:
      self.ui.actionRecent.triggered.connect(button.showMenu)
  ```
- TODO/FIXME comments follow `# TODO(name, YYYY-MM-DD): description` and should link to an issue.

## 12. Error Handling & Logging
- User-facing errors go through `QMessageBox`, the status bar, or purpose-built widgets. Avoid `print`.
- Use the standard `logging` module for diagnostics:
  ```python
  import logging
  LOGGER = logging.getLogger(__name__)
  LOGGER.debug("Loading file %s", file_name)
  ```
- Include context such as file paths or MIME types where helpful, but do not leak sensitive data.
- Catch specific exceptions and provide actionable feedback; restore UI state when necessary (e.g., reset cursors).

### Logging conventions
- Do not use `print` for diagnostics; use `logging` with module-level loggers (e.g., `LOGGER = logging.getLogger(__name__)`).
- Initialize logging in the entry point if needed; keep logs terse for UI flows.
- Wrap platform-specific initialization and log failures instead of printing:
  ```python
  if sys.platform == "win32":
      try:
          ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('QtExamples.DocumentViewer')
      except Exception as exc:
          LOGGER.warning("Failed to set AppUserModelID: %s", exc)
  ```

## 13. Testing & Verification
- Unit tests cover core logic (`RecentFiles`, `JsonItemModel`, etc.) with pytest or unittest. GUI flows can use Qt Test or scripted manual checks.
- Smoke checklist:
  1. Launch the application.  
  2. Open sample JSON/PDF/TXT/image files and confirm rendering.  
  3. Verify the recent files menu and print action states.  
  4. Restart the app and ensure window state and recent files persist.  
- Update tests and sample assets when adding viewers or features.

### Linting & type checking
- Enforce linting (ruff/flake8) in CI: no `print`, import hygiene, line length, and common PySide idioms.
- Type-check with mypy where feasible; relax strictness around Qt types or add selective `# type: ignore` for bindings.

### Suggested tests for this repo
- `RecentFiles`: add/remove, duplicate suppression, max size, settings roundtrip.
- `JsonItemModel`: `index`/`parent` invariants, header content, editability limits.

## 14. Version Control & Reviews
- Keep commits atomic and prefer `type(scope): summary` messages such as `feat(viewer): add csv support`.
- Do not commit generated artefacts, caches, or personal configs (`__pycache__/`, `.pyside6/`, etc.).
- Reference issues in merge requests and include evidence (logs, screenshots) for UI-facing changes.
- Review checklist: consistent naming, balanced signal/slot connections, registered resources, updated docs/tests.

## 15. Maintenance & References
- Review this guide quarterly. Update both language versions together and record the date, author, and summary of changes.
- References:
  - [Qt Coding Style](https://wiki.qt.io/Qt_Coding_Style)  
  - [PEP 8 -- Style Guide for Python Code](https://peps.python.org/pep-0008/)  
  - [Qt for Python Documentation](https://doc.qt.io/qtforpython/)

---

> If practice diverges from this guide, open an issue first, agree on the change, and then update the document.
