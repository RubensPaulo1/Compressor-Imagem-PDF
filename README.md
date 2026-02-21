## Compressor de Arquivos (PDF e Imagem)

<img width="1308" height="835" alt="Captura de tela 2026-02-21 131228" src="https://github.com/user-attachments/assets/c41b2225-0bfa-44ea-a249-4f2fe96d7b97" />


Aplicação para **comprimir arquivos PDF e imagens (JPG/PNG)**.  
Ideal para reduzir o tamanho de arquivos antes de enviar por e‑mail ou fazer upload.

### Funcionalidades

- **Comprimir PDF** (Usando Ghostscript) vai gerar arquivo `_comprimido.pdf`.
- **Comprimir Imagens (JPG/PNG)** ( usando Pillow (PIL).

---

### Requisitos

- **Python 3.x**
- **Pillow** para imagens
- **Ghostscript**
- **Node.js**
---

### Como rodar

1. **Backend (API)** na pasta do projeto:
   ```bash
   pip install -r requirements.txt
   python api.py
   ```
   A API sobe em `http://localhost:5000`.

2. **Frontend** em outro terminal:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. Abra **http://localhost:3000** no navegador, escolha PDF ou imagem, ajuste a qualidade (para JPG) e clique em comprimir. O arquivo comprimido será baixado automaticamente. 


