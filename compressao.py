import glob
import os
import shutil
import subprocess
from typing import Optional


def _encontrar_ghostscript() -> Optional[str]:
    """
    Tenta localizar o executável do Ghostscript no Windows.

    Retorna o caminho do executável se encontrado, senão None.
    """
    candidatos = ["gswin64c", "gswin32c", "gs"]

    for nome in candidatos:
        achado = shutil.which(nome)
        if achado:
            return achado

    # Pastas comuns de instalação no Windows
    possiveis = []
    for base in (r"C:\Program Files\gs", r"C:\Program Files (x86)\gs"):
        possiveis.extend(glob.glob(os.path.join(base, r"gs*\bin\gswin64c.exe")))
        possiveis.extend(glob.glob(os.path.join(base, r"gs*\bin\gswin32c.exe")))

    return possiveis[0] if possiveis else None

def comprimir_pdf(input_path, output_path):
    ghostscript_path = _encontrar_ghostscript()
    if not ghostscript_path:
        raise FileNotFoundError(
            "Ghostscript não encontrado.\n\n"
            "Para comprimir PDF, instale o Ghostscript (procure por 'gswin64c') "
            "e garanta que ele esteja no PATH do Windows. "
            "Depois disso, reabra o terminal/IDE e tente novamente."
        )

    comando = [
        ghostscript_path,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",

        #Compressão
        "-dDownsampleColorImages=true",
        "-dColorImageResolution=150",

        "-dDownsampleGrayImages=true",
        "-dGrayImageResolution=150",

        "-dDownsampleMonoImages=true",
        "-dMonoImageResolution=150",

        "-dJPEGQ=50",  #(0–100)

        f"-sOutputFile={output_path}",
        input_path
    ]

    subprocess.run(comando, check=True)
    print("PDF comprimido com sucesso!")