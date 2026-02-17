import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from compressao import comprimir_pdf
from imagem_compressao import comprimir_imagem


def selecionar_arquivo_pdf():
    caminho = filedialog.askopenfilename(
        title="Selecione um arquivo PDF",
        filetypes=[("Arquivos PDF", "*.pdf")],
    )
    return caminho


def selecionar_arquivo_imagem():
    caminho = filedialog.askopenfilename(
        title="Selecione uma imagem",
        filetypes=[
            ("Imagens", "*.jpg;*.jpeg;*.png"),
            ("JPEG", "*.jpg;*.jpeg"),
            ("PNG", "*.png"),
        ],
    )
    return caminho


def comprimir_pdf_gui(root, status_label, botao):
    caminho_pdf = selecionar_arquivo_pdf()
    if not caminho_pdf:
        return

    base, _ = os.path.splitext(caminho_pdf)
    saida = base + "_comprimido.pdf"

    def tarefa():
        try:
            status_label.config(text="Comprimindo PDF, aguarde...")
            botao.config(state="disabled")
            comprimir_pdf(caminho_pdf, saida)
            messagebox.showinfo(
                "Sucesso",
                f"PDF comprimido com sucesso!\n\nArquivo gerado:\n{saida}",
            )
        except FileNotFoundError as e:
            # Normalmente é Ghostscript não instalado / não encontrado.
            messagebox.showerror(
                "Ghostscript não encontrado",
                f"{e}\n\nDica: após instalar, reabra o terminal/IDE.",
            )
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao comprimir PDF:\n{e}")
        finally:
            status_label.config(text="")
            botao.config(state="normal")

    threading.Thread(target=tarefa, daemon=True).start()


def comprimir_imagem_gui(root, status_label, botao):
    caminho_img = selecionar_arquivo_imagem()
    if not caminho_img:
        return

    base, ext = os.path.splitext(caminho_img)

    if not ext:
        messagebox.showwarning(
            "Extensão inválida",
            "O arquivo precisa ter uma extensão válida (ex: .jpg, .png).",
        )
        return

    saida = base + "_comprimido" + ext

    def tarefa():
        try:
            status_label.config(text="Comprimindo imagem, aguarde...")
            botao.config(state="disabled")
            comprimir_imagem(caminho_img, saida)
            messagebox.showinfo(
                "Sucesso",
                f"Imagem comprimida com sucesso!\n\nArquivo gerado:\n{saida}",
            )
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao comprimir imagem:\n{e}")
        finally:
            status_label.config(text="")
            botao.config(state="normal")

    threading.Thread(target=tarefa, daemon=True).start()


def criar_interface():
    root = tk.Tk()
    root.title("Compressor de Arquivos")

    # Tamanho fixo simples e centralizado
    root.geometry("420x220")
    root.resizable(False, False)

    # Tema "moderno" com ttk
    try:
        root.call("source", "azure.tcl")  # se você tiver um tema externo
        ttk.Style().theme_use("azure")
    except Exception:
        style = ttk.Style()
        if "clam" in style.theme_names():
            style.theme_use("clam")

    style = ttk.Style()
    style.configure("TButton", padding=8, font=("Segoe UI", 10))
    style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"))
    style.configure("Subtitle.TLabel", font=("Segoe UI", 10))

    container = ttk.Frame(root, padding=20)
    container.pack(fill="both", expand=True)

    titulo = ttk.Label(
        container,
        text="Compressor de Arquivos",
        style="Title.TLabel",
    )
    titulo.pack(anchor="center")

    sub = ttk.Label(
        container,
        text="Escolha o tipo de arquivo que você quer comprimir:",
        style="Subtitle.TLabel",
    )
    sub.pack(anchor="center", pady=(5, 15))

    botoes_frame = ttk.Frame(container)
    botoes_frame.pack(pady=5)

    status_label = ttk.Label(
        container,
        text="",
        style="Subtitle.TLabel",
        foreground="#555555",
    )
    status_label.pack(side="bottom", pady=(15, 0))

    botao_pdf = ttk.Button(
        botoes_frame,
        text="Comprimir PDF",
        width=18,
        command=lambda: comprimir_pdf_gui(root, status_label, botao_pdf),
    )
    botao_pdf.grid(row=0, column=0, padx=10)

    botao_img = ttk.Button(
        botoes_frame,
        text="Comprimir Imagem",
        width=18,
        command=lambda: comprimir_imagem_gui(root, status_label, botao_img),
    )
    botao_img.grid(row=0, column=1, padx=10)

    root.mainloop()


if __name__ == "__main__":
    criar_interface()