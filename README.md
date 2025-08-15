# Dir2CSV

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-blue)](#)
[![Downloads](https://img.shields.io/github/downloads/kikki/Dir2CSV/total.svg)](https://github.com/kikki/Dir2CSV/releases)
[![Last Commit](https://img.shields.io/github/last-commit/kikki/Dir2CSV)](https://github.com/kikki/Dir2CSV/commits/main)

**Dir2CSV** is a lightweight tool that **recursively scans all files in a folder** and exports the results into a **CSV file** — **no administrator rights required**.

---

## Why use Dir2CSV?

You can use it to:  
- **Create a snapshot of a project’s current state**  
  → Example: Export the structure and content of your `my-app/` folder into `project_snapshot.csv` before a big refactor.  
- **Package code and data for Large Language Models (LLMs)**  
  → Example: Send the exported CSV to ChatGPT so it can “see” your entire project and help debug or refactor it.  
- **Quickly list all files with metadata**  
  → Example: Generate a CSV of all `.py` and `.txt` files with their relative paths and contents for documentation or code review.  

---

## ✨ Features

- 🔍 Recursively scans directories  
- 🧾 Exports CSV with path, filename, extension, and (optional) file content  
- 🗂️ Handles binary files gracefully (adds placeholder text)  
- 🎯 Optional filters for file extensions and folders  
- 📂 Supports **most common text-based formats** (see list below)  
- 🚫 Allows excluding specific folders (customizable)  
- 🛡️ Robust against write-protection and access errors (shows clear messages)  
- 🪟 Portable **.exe** version — **runs without admin rights or installation**  
- 🖥 Windows-only (Linux/macOS planned)

---

## 📄 Supported File Formats (Content Reading)

By default, Dir2CSV will attempt to read the contents of **text-based files**, including:  

- **Code files**: `.py`, `.js`, `.ts`, `.java`, `.c`, `.cpp`, `.h`, `.cs`, `.php`, `.rb`  
- **Markup / text**: `.html`, `.css`, `.xml`, `.json`, `.yaml`, `.yml`, `.md`, `.txt`  
- **Data files**: `.csv`, `.tsv`  
- **Config files**: `.ini`, `.env`, `.cfg`  

### How binary or large files are handled  
Binary or large files (e.g., `.exe`, `.dll`, `.ico`, `.png`, `.jpg`, `.zip`) are **not read**.  
Instead, the CSV will contain this placeholder in the `content` column:  

```
[Binary file – content not readable]
```

This avoids huge CSV sizes, encoding errors, and keeps the file usable in Excel or analysis tools.

You can change which file types get this treatment via CLI or GUI filters.

---

## 🚫 Default & Custom Excluded Folders

By default, these folders are skipped during scanning:  

- `.git`  
- `__pycache__`  
- `node_modules`  
- `.idea`  
- `.vscode`  
- `dist`  
- `build`  

You can **add or remove** excluded folders:

**GUI**  
- Open the *Exclude folders* settings and enter folder names separated by commas  
- Example:  
  ```
  .git,__pycache__,node_modules,logs,temp
  ```

**CLI**  
```bash
python -m dir2csv   --input "C:\Projects\my-project"   --output "C:\Exports\project_snapshot.csv"   --exclude-folders ".git,__pycache__,node_modules,logs,temp"
```

📌 Tip: Folder exclusion is case-insensitive on Windows but case-sensitive on Linux/macOS.

---

## 📊 CSV Schema

| Column           | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| `relativer_pfad` | Relative path starting from the chosen root folder                          |
| `datei_name`     | File name                                                                    |
| `datei_endung`   | File extension (e.g., `.py`, `.txt`, `.ico`)                                 |
| `inhalt`         | File content, or placeholder for binary files                               |

**Example row (shortened):**
```csv
"scanner\file_scanner_class.py";"file_scanner_class.py";".py";"import os\nimport csv\nfrom pathlib import Path\n..."
```

---

## 🛠 Installation

### Option A: Python (Development)
```bash
# 1) Clone the repository
git clone https://github.com/<your-org>/Dir2CSV.git
cd Dir2CSV

# 2) Set up virtual environment
python -m venv .venv
. .venv/Scripts/activate  # Windows
pip install -r requirements.txt
```

### Option B: Portable .exe (Usage)
- Download the prebuilt **Dir2CSV.exe** from the Releases section  
- Run it via double-click — **no admin rights, no installation required**

---

## 🚀 Usage

### GUI
1. Select **source folder**  
2. Select **target CSV**  
3. (Optional) Set filters for extensions/folders  
4. **Start** – progress will be displayed, and you’ll get a completion message

### CLI
```bash
python -m dir2csv   --input "C:\Projects\my-project"   --output "C:\Exports\project_snapshot.csv"   --include-ext ".py,.txt,.md"   --exclude-folders ".git,__pycache__,node_modules"   --no-content-for ".*\.(ico|png|jpg|exe|dll|zip)$"
```

**Key Options:**
- `--input` (path): Source folder  
- `--output` (file): Target CSV file  
- `--include-ext` / `--exclude-ext`: Filter by extension  
- `--exclude-folders`: Skip specific folders  
- `--no-content-for`: Regex to skip reading content of specific file types

---

## 📤 Output & Compatibility

- CSV is **UTF-8**, `;` separated, and **fully quoted** → safe for commas/line breaks in content  
- Directly usable in Excel, Power BI, or Python

---

## ⚠ Error Handling

- Write-protected/locked files: Skipped with clear message  
- Large files: Optional *metadata-only* mode  
- Binary files: Replaced with `[Binary file – content not readable]`

---

## 💡 Use Cases

- Project snapshots for reviews & audits  
- Providing project context to LLMs (code + structure)  
- Code inventory/license checks (metadata level)  
- Change tracking over time (CSV diff)

---

## 🛣 Roadmap

- [ ] Add file hash column (e.g., SHA-256)  
- [ ] Config file (JSON) for reusable scan profiles  
- [ ] Multi-language GUI (automatic locale detection)  
- [ ] Performance mode for huge repositories

---

## 🔧 Development & Build (PyInstaller)

Example:
```bash
pyinstaller --onefile --noconsole --icon favicon.ico Dir2CSV.py
```
The `.spec` file in the repo contains adjusted settings (icon, resources, etc.).

---

## 📜 License

Choose a suitable open-source license (e.g., MIT) and include it as `LICENSE`.

---

**GitHub short description:**  
> Recursively scan any folder and export file paths, metadata, and contents to CSV — no admin rights required.
