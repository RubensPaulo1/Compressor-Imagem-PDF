from PIL import Image
import os

def comprimir_imagem(input_path, output_path, qualidade=40):
    imagem = Image.open(input_path)

    # Se for PNG
    if imagem.format == "PNG":
        imagem.save(output_path, optimize=True)

    # Se for JPG/JPEG
    elif imagem.format in ["JPEG", "JPG"]:
        imagem.save(output_path, quality=40, optimize=True)

    else:
        print("Formato não suportado.")
        return

    print(f"Imagem comprimida com sucesso: {output_path}")