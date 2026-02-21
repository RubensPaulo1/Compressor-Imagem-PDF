"""
API Flask para o Compressor de Arquivos.
Expõe endpoints para compressão de PDF e imagens (JPG/PNG).
"""
import io
import os
import tempfile
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

from compressao import comprimir_pdf
from imagem_compressao import comprimir_imagem

app = Flask(__name__)
CORS(app)
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024  # 100 MB

ALLOWED_IMAGE_EXT = {"jpg", "jpeg", "png"}
ALLOWED_PDF_EXT = {"pdf"}


def allowed_file(filename, allowed):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "Compressor API está rodando"})


@app.route("/api/compress/pdf", methods=["POST"])
def compress_pdf():
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Nenhum arquivo selecionado"}), 400
    if not allowed_file(file.filename, ALLOWED_PDF_EXT):
        return jsonify({"error": "Formato inválido. Use apenas .pdf"}), 400

    try:
        with tempfile.TemporaryDirectory() as tmp:
            input_path = os.path.join(tmp, secure_filename(file.filename))
            file.save(input_path)
            base, _ = os.path.splitext(file.filename)
            output_name = f"{base}_comprimido.pdf"
            output_path = os.path.join(tmp, output_name)
            comprimir_pdf(input_path, output_path)
            # Ler para memória antes de sair do TemporaryDirectory
            with open(output_path, "rb") as f:
                data = f.read()
        return send_file(
            io.BytesIO(data),
            as_attachment=True,
            download_name=output_name,
            mimetype="application/pdf",
        )
    except FileNotFoundError as e:
        return (
            jsonify(
                {
                    "error": "Ghostscript não encontrado",
                    "detail": str(e),
                }
            ),
            503,
        )
    except Exception as e:
        return jsonify({"error": "Erro ao comprimir PDF", "detail": str(e)}), 500


@app.route("/api/compress/image", methods=["POST"])
def compress_image():
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Nenhum arquivo selecionado"}), 400
    if not allowed_file(file.filename, ALLOWED_IMAGE_EXT):
        return jsonify({"error": "Formato inválido. Use .jpg, .jpeg ou .png"}), 400

    qualidade = request.form.get("qualidade", type=int)
    if qualidade is None:
        qualidade = 40
    qualidade = max(1, min(100, qualidade))

    try:
        with tempfile.TemporaryDirectory() as tmp:
            input_path = os.path.join(tmp, secure_filename(file.filename))
            file.save(input_path)
            base, ext = os.path.splitext(file.filename)
            output_name = f"{base}_comprimido{ext}"
            output_path = os.path.join(tmp, output_name)
            comprimir_imagem(input_path, output_path, qualidade=qualidade)
            with open(output_path, "rb") as f:
                data = f.read()
        mimetype = "image/jpeg" if ext.lower() in (".jpg", ".jpeg") else "image/png"
        return send_file(
            io.BytesIO(data),
            as_attachment=True,
            download_name=output_name,
            mimetype=mimetype,
        )
    except Exception as e:
        return jsonify({"error": "Erro ao comprimir imagem", "detail": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
