## Compressor de Arquivos (PDF e Imagem)

Aplicação simples com interface gráfica em Python para **comprimir arquivos PDF e imagens (JPG/PNG)**.  
Ideal para evitar compartilhar documentos sensíveis e reduzir o tamanho de arquivos antes de enviar por e‑mail ou fazer upload.

### Funcionalidades

- **Comprimir PDF**
  - Usa Ghostscript para reduzir o tamanho do arquivo.
  - Gera um novo arquivo com o sufixo `_comprimido.pdf`.
- **Comprimir Imagens (JPG/PNG)**
  - Usa Pillow (`PIL`) para otimizar PNG e reduzir qualidade de JPG/JPEG.
  - Gera um novo arquivo com o sufixo `_comprimido.ext`.

---

### Requisitos

- **Python 3.x**
- **Pillow (PIL)** para manipulação de imagens
- **Ghostscript** 


