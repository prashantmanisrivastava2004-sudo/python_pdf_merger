import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox
from pypdf import PdfWriter

base_dir = Path(__file__).resolve().parent

DEFAULT_PDFS = [base_dir / "gov id.pdf", base_dir / "aktu admit card.pdf"]


def merge_pdfs(pdf_paths, output_path):
    writer = PdfWriter()
    for pdf_path in pdf_paths:
        pdf = Path(pdf_path)
        if not pdf.exists():
            raise FileNotFoundError(f"Input PDF not found: {pdf}")
        writer.append(pdf)
    writer.write(output_path)


class PdfMergerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF Merger")
        self.geometry("520x360")
        self.pdf_paths = []

        self.create_widgets()
        self.load_default_pdfs()

    def create_widgets(self):
        frame = tk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.listbox = tk.Listbox(frame, selectmode=tk.EXTENDED, width=68, height=12)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        button_frame = tk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        add_button = tk.Button(button_frame, text="Add PDFs", command=self.add_pdfs)
        add_button.pack(side=tk.LEFT, padx=(0, 4))

        remove_button = tk.Button(button_frame, text="Remove Selected", command=self.remove_selected)
        remove_button.pack(side=tk.LEFT, padx=(0, 4))

        merge_button = tk.Button(button_frame, text="Merge to merged.pdf", command=self.merge_selected)
        merge_button.pack(side=tk.LEFT, padx=(0, 4))

        saveas_button = tk.Button(button_frame, text="Save As...", command=self.merge_save_as)
        saveas_button.pack(side=tk.LEFT)

    def load_default_pdfs(self):
        for pdf in DEFAULT_PDFS:
            if pdf.exists():
                self.add_path(str(pdf))

    def add_path(self, path):
        if path not in self.pdf_paths:
            self.pdf_paths.append(path)
            self.listbox.insert(tk.END, path)

    def add_pdfs(self):
        files = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF files", "*.pdf")],
            initialdir=base_dir,
        )
        for path in files:
            self.add_path(path)

    def remove_selected(self):
        selected_indexes = list(self.listbox.curselection())
        for index in reversed(selected_indexes):
            self.pdf_paths.pop(index)
            self.listbox.delete(index)

    def merge_selected(self):
        if not self.pdf_paths:
            messagebox.showwarning("No PDFs", "Please add at least one PDF to merge.")
            return

        output_path = base_dir / "merged.pdf"
        try:
            merge_pdfs(self.pdf_paths, output_path)
            messagebox.showinfo("Success", f"Merged {len(self.pdf_paths)} PDFs into '{output_path.name}'.")
        except Exception as exc:
            messagebox.showerror("Merge Failed", str(exc))

    def merge_save_as(self):
        if not self.pdf_paths:
            messagebox.showwarning("No PDFs", "Please add at least one PDF to merge.")
            return

        output_file = filedialog.asksaveasfilename(
            title="Save merged PDF as",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile="merged.pdf",
            initialdir=base_dir,
        )
        if not output_file:
            return

        try:
            merge_pdfs(self.pdf_paths, Path(output_file))
            messagebox.showinfo("Success", f"Merged {len(self.pdf_paths)} PDFs into '{Path(output_file).name}'.")
        except Exception as exc:
            messagebox.showerror("Merge Failed", str(exc))


if __name__ == "__main__":
    app = PdfMergerApp()
    app.mainloop()