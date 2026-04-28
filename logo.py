from PIL import Image

# Abrir imagem
img = Image.open("imagem.png")

# Converter para RGB (garante compatibilidade)
img = img.convert("RGB")

# Detectar área útil (remove espaços brancos)
bbox = img.getbbox()
img_cropped = img.crop(bbox)

# Redimensionar (ajuste o tamanho aqui)
img_resized = img_cropped.resize((400, 200))

# Salvar nova imagem
img_resized.save("imagem.png")

print("Imagem pronta!")