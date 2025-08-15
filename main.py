# main.py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import json
from pathlib import Path
import sys
import os

from Dir2CSV import FileScanner  # translated class name

# -----------------------------------------------------------------------------
# main
# Purpose: Launch the configuration UI, persist user inputs if desired,
#          and run the directory scan -> CSV export workflow.
# -----------------------------------------------------------------------------
def main():
    config_file = "scanner_config.json"

    # -------------------------------------------------------------------------
    # load_saved_values
    # Purpose: Load previously saved folder/CSV values from a JSON config file.
    #          Supports old German keys for backward compatibility.
    # -------------------------------------------------------------------------
    def load_saved_values():
        if Path(config_file).exists():
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Backward compatibility: accept old keys if present
                    folder = data.get("folder", data.get("ordner", ""))
                    csv_path = data.get("csv", data.get("csv_datei", ""))
                    return {"folder": folder, "csv": csv_path}
            except Exception:
                return {}
        return {}

    # -------------------------------------------------------------------------
    # save_values
    # Purpose: Store current folder/CSV values to the JSON config file.
    # -------------------------------------------------------------------------
    def save_values(folder, csv_path):
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump({"folder": folder, "csv": csv_path}, f)

    # -------------------------------------------------------------------------
    # start_scan
    # Purpose: Trigger the scan using FileScanner and write results to CSV.
    #          Show user feedback dialogs for success and errors.
    # -------------------------------------------------------------------------
    def start_scan(folder, csv_file):
        scanner = FileScanner()
        try:
            found = scanner.scan_folder(folder)
            scanner.create_csv(found, csv_file)
            messagebox.showinfo("Done!", f"Scan finished.\nFile saved to:\n{csv_file}")
        except PermissionError:
            messagebox.showerror("Error", f"No write access to:\n{csv_file}")
            show_ui()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during scanning:\n{e}")
            show_ui()

    # -------------------------------------------------------------------------
    # show_ui
    # Purpose: Build and display the main Tkinter window to configure inputs.
    # -------------------------------------------------------------------------
    def show_ui():
        saved = load_saved_values()

        # ---------------------------------------------------------------------
        # on_ok
        # Purpose: Validate inputs, optionally persist them, and start the scan.
        # ---------------------------------------------------------------------
        def on_ok():
            folder = entry_folder.get().strip()
            csv_path = entry_csv.get().strip()
            if not folder or not csv_path:
                messagebox.showwarning("Missing input", "Please fill in all fields.")
                return
            window.destroy()
            if var_save.get():
                save_values(folder, csv_path)
            start_scan(folder, csv_path)

        # ---------------------------------------------------------------------
        # on_exit
        # Purpose: Close the configuration window without running a scan.
        # ---------------------------------------------------------------------
        def on_exit():
            window.destroy()

        # ---------------------------------------------------------------------
        # choose_folder
        # Purpose: Let the user pick the folder to scan.
        # ---------------------------------------------------------------------
        def choose_folder():
            path = filedialog.askdirectory()
            if path:
                entry_folder.delete(0, tk.END)
                entry_folder.insert(0, path)

        # ---------------------------------------------------------------------
        # choose_file
        # Purpose: Let the user choose where to save the CSV file.
        # ---------------------------------------------------------------------
        def choose_file():
            path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if path:
                entry_csv.delete(0, tk.END)
                entry_csv.insert(0, path)

        window = tk.Tk()
        window.title("Configure File Scanner")
        window.configure(bg="#8E44AD")  # Purple background
        # window.iconbitmap("app.ico")
        # Note: keep the original icon resolution path logic for compatibility.
        ico_path = os.path.join(getattr(sys, '_MEIPASS', os.path.dirname(__file__)), "favicon.ico\\favicon.ico")
        try:
            window.iconbitmap(ico_path)
        except Exception:
            # Fail silently if icon not found or invalid on the platform
            pass

        # Modern styling
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", background="#A569BD", foreground="white", font=("Segoe UI", 10), padding=6)
        style.map("TButton", background=[("active", "#BA55D3")])
        style.configure("TLabel", background="#8E44AD", foreground="white", font=("Segoe UI", 10, "bold"))
        style.configure("TCheckbutton", background="#8E44AD", foreground="white", font=("Segoe UI", 10))
        style.map("TCheckbutton", background=[("active", "#8E44AD")])

        padding = {"padx": 10, "pady": 8}

        ttk.Label(window, text="Folder to scan:").grid(row=0, column=0, sticky="w", **padding)
        entry_folder = ttk.Entry(window, width=60)
        entry_folder.grid(row=0, column=1, **padding)
        ttk.Button(window, text="Browse", command=choose_folder).grid(row=0, column=2, **padding)

        ttk.Label(window, text="CSV output file:").grid(row=1, column=0, sticky="w", **padding)
        entry_csv = ttk.Entry(window, width=60)
        entry_csv.grid(row=1, column=1, **padding)
        ttk.Button(window, text="Browse", command=choose_file).grid(row=1, column=2, **padding)

        var_save = tk.BooleanVar(value=True)
        ttk.Checkbutton(window, text="Save inputs", variable=var_save).grid(row=2, column=1, **padding)

        ttk.Button(window, text="OK", command=on_ok).grid(row=3, column=1, sticky="e", **padding)
        ttk.Button(window, text="Exit", command=on_exit).grid(row=3, column=2, sticky="w", **padding)

        # Pre-fill with saved values (supports old keys via load_saved_values)
        entry_folder.insert(0, saved.get("folder", ""))
        entry_csv.insert(0, saved.get("csv", ""))

        window.mainloop()

    show_ui()


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
