import flet as ft
from PIL import Image
import base64
import io
from dataclasses import field
import numpy as np
import cv2
import matplotlib.pyplot as plt

def main(page: ft.Page):

    page.title = 'Read Local Image'
    page.window_maximized = True
    page.add(ft.Text('Read Local Image', size=30, color='green'))
    image_holder = ft.Image(visible=False, fit=ft.ImageFit.CONTAIN, width=1400, height=500)
    rotateNumber = 0 
    inScale = False
    staticImageHolder = ""

    def handle_reset_image (*args):
        image_holder = ft.Image(visible=False, fit=ft.ImageFit.CONTAIN, width=1400, height=500)
        image_holder.src_base64 = staticImageHolder
        image_holder.visible = True
        image_holder.rotate = 0
        page.update()

    def handle_loaded_file(e: ft.FilePickerResultEvent):
        if e.files and len(e.files):
            with open(e.files[0].path, 'rb') as r:
                nonlocal staticImageHolder
                a = base64.b64encode(r.read()).decode('utf-8')
                staticImageHolder = a
                image_holder.src_base64 = a
                image_holder.visible = True
                page.update()  



    file_picker = ft.FilePicker(on_result=handle_loaded_file)
    page.overlay.append(file_picker)

    page.add(ft.ElevatedButton(text='Select Image', on_click=lambda _: file_picker.pick_files(allow_multiple=False, allowed_extensions=['jpg','jpeg','png'])))

    page.add(image_holder)

    def convert_to_cv2():
        image = Image.open(io.BytesIO(base64.b64decode(image_holder.src_base64)))
        image_array = np.array(image)
        base64_image = image_holder.src_base64 # Coloque aqui a sua string base64

        image_data = base64.b64decode(base64_image)

        image_array = np.frombuffer(image_data, np.uint8)

        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        return image
        
    def handle_rotate_image(*args):
        nonlocal rotateNumber
        imagem = Image.open(io.BytesIO(base64.b64decode(image_holder.src_base64)))
        imagemy = girar(imagem, 2)
        plt.imshow(imagemy)
        plt.axis('off')
        plt.show()


    def handle_translate_image(*args):
        nonlocal inScale
        imagem = Image.open(io.BytesIO(base64.b64decode(image_holder.src_base64)))
        
        imagem_redimensionada = imagem.resize((790, 150))

        plt.imshow(imagem_redimensionada)
        plt.axis('off')
        plt.show()

    def rgb_to_gray(r, g, b):
        return int(0.2989 * r + 0.5870 * g + 0.1140 * b)

    def handle_convert_to_white_and_black(*args):
            image = Image.open(io.BytesIO(base64.b64decode(image_holder.src_base64)))
            pixels = image.load()

            width, height = image.size

            for y in range(height):
                for x in range(width):
                    if len(pixels[x, y]) == 4:
                        r, g, b, a = pixels[x, y]
                        gray = rgb_to_gray(r, g, b)
                        pixels[x, y] = (gray, gray, gray, a)
                    else:
                        r, g, b = pixels[x, y]
                        gray = rgb_to_gray(r, g, b)
                        pixels[x, y] = (gray, gray, gray)

            plt.imshow(image)
            plt.axis('off')
            plt.show()

    def translate_image(image_array, dx, dy):
        height, width, channels = image_array.shape
        translated_image = np.zeros_like(image_array)
        for y in range(height):
            for x in range(width):
                new_x = x + dx
                new_y = y + dy
                if 0 <= new_x < width and 0 <= new_y < height:
                    translated_image[new_y, new_x] = image_array[y, x]
        return translated_image
    
    def handle_tranlate_image(*args):
        image = Image.open(io.BytesIO(base64.b64decode(image_holder.src_base64)))
        lar = image.size[0]
        alt = image.size[1]
        x_loc = 50
        y_loc = 50
        imagem_original = np.asarray(image.convert('RGB'))
        for x in range(lar):
            for y in range(alt):
                    if x >= x_loc and y >= y_loc:
                        yo = x - x_loc
                        xo = y - y_loc
                        image.putpixel((x,y), (imagem_original[xo,yo][0],imagem_original[xo,yo][1],imagem_original[xo,yo][2]))
                    else:
                        image.putpixel((x,y), (255, 255, 255, 255))
        plt.imshow(image)
        plt.axis('off')
        plt.show()

    def handle_histogram(*args):

        base64_image = image_holder.src_base64  # Coloque aqui a sua string base64

        # Decodificar a string base64 em uma matriz de bytes
        image_data = base64.b64decode(base64_image)

        # Criar um objeto BytesIO para lidar com os dados da imagem
        image_buffer = io.BytesIO(image_data)

        # Abrir a imagem a partir do buffer de bytes
        imagem = Image.open(image_buffer)

        # Converter a imagem para escala de cinza
        imagem_cinza = imagem.convert('L')

        # Obter os valores dos pixels da imagem
        pixels = list(imagem_cinza.getdata())

        # Calcular o histograma
        histograma = [0] * 256  # Inicializa uma lista com 256 elementos para armazenar as contagens de cada valor de pixel
        for pixel in pixels:
            histograma[pixel] += 1

        # Plotar o histograma
        plt.figure(figsize=(10, 5))
        plt.bar(range(256), histograma, color='gray')
        plt.title('Histograma da Imagem em Escala de Cinza')
        plt.xlabel('Valor do Pixel')
        plt.ylabel('Frequência')
        plt.grid(True)
        plt.show()
        
        page.update()

    def handle_cut(*args):
        imagem = Image.open(io.BytesIO(base64.b64decode(image_holder.src_base64)))
        largura = 500
        altura = 500
        # Obtém as dimensões da imagem original
        largura_original, altura_original = imagem.size

        # Corta a imagem - especificamente no centro
        esquerda = (largura_original - largura) / 2
        superior = (altura_original - altura) / 2
        direita = (largura_original + largura) / 2
        inferior = (altura_original + altura) / 2

        imagem_cortada = imagem.crop((esquerda, superior, direita, inferior))

        # Mostra a imagem cortada
        plt.imshow(imagem_cortada)
        plt.axis('off')
        plt.show()

        page.update()

    def handle_balance_color(*args):
        image = Image.open(io.BytesIO(base64.b64decode(image_holder.src_base64)))
        image_np = np.array(image)
        lab_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2LAB)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        lab_image[:, :, 0] = clahe.apply(lab_image[:, :, 0])
        balanced_image_np = cv2.cvtColor(lab_image, cv2.COLOR_LAB2RGB)
        balanced_image = Image.fromarray(balanced_image_np)
        buffered_balanced = io.BytesIO()
        balanced_image.save(buffered_balanced, format="PNG")
        balanced_base64 = base64.b64encode(buffered_balanced.getvalue()).decode('utf-8')
        image_holder.src_base64 = balanced_base64
        image_holder.visible = True
        page.update()

    def handle_red_filter (*args):
        image = Image.open(io.BytesIO(base64.b64decode(image_holder.src_base64)))
        pixels = image.load()

        # Obter dimensões da imagem
        width, height = image.size

        # Aplicar o filtro vermelho
        for y in range(height):
            for x in range(width):
                if len(pixels[x, y]) == 4:
                    r, g, b, a = pixels[x, y]
                    # Aumentar a componente vermelha e diminuir verde e azul
                    red = min(255, int(r * 1.5))  # Ajustar a intensidade do vermelho
                    green = int(g * 0.5)  # Reduzir a intensidade do verde
                    blue = int(b * 0.5)  # Reduzir a intensidade do azul
                    pixels[x, y] = (red, green, blue, a)
                else:
                    r, g, b = pixels[x, y]
                    # Aumentar a componente vermelha e diminuir verde e azul
                    red = min(255, int(r * 1.5))  # Ajustar a intensidade do vermelho
                    green = int(g * 0.5)  # Reduzir a intensidade do verde
                    blue = int(b * 0.5)  # Reduzir a intensidade do azul
                    pixels[x, y] = (red, green, blue)

        # Salvar a imagem resultante
        # Mostrar a imagem resultante
        plt.imshow(image)
        plt.axis('off')  # Ocultar os eixos
        plt.show()


            # função para girar no sentiro anti-horário
    def girar_matriz_sentido_anti_horario(matriz):

        largura, altura = matriz.size

        imagem2 = Image.new("RGB", (altura,largura))

        for i in range(altura):
            for j in range(largura):

                # Pega os pixels da imagem original da esquerda para direita, de cima para baixo
                pixel = matriz.getpixel((j, i))

                # Coloca os pixels da imagem original para a nova orientação que é [i, largura - 1 - j]
                imagem2.putpixel((i, largura - 1 - j), pixel)


        return imagem2


    # função para girar no sentiro horário
    def girar_matriz_sentido_horario(matriz):

        largura, altura = matriz.size

        imagem2 = Image.new("RGB", (altura,largura))

        for i in range(altura):
            for j in range(largura):

                # Pega os pixels da imagem original da esquerda para direita, de cima para baixo
                pixel = matriz.getpixel((j, i))

                # Coloca os pixels da imagem original para a nova orientação que é [altura - 1 - i , j]
                imagem2.putpixel((altura - 1 - i , j), pixel)


        return imagem2

    # Função principal, recebe a imagem e a direção
    # Para girar no sentido anti-horário 1
    # Para girar no sentido horário 2
    def girar(matriz, direcao):
        if direcao == 1:
            imagemy = girar_matriz_sentido_anti_horario(matriz)
        elif direcao == 2:
            imagemy = girar_matriz_sentido_horario(matriz)


        return imagemy

    rrow_button = ft.ResponsiveRow(
        [ft.ElevatedButton(text='Rotaçao', on_click=handle_rotate_image, col={"md": 4}),
         ft.ElevatedButton(text='Translação', on_click=handle_tranlate_image, col={"sm": 4}),
         ft.ElevatedButton(text='Escala', on_click=handle_translate_image, col={"md": 4}),
         ft.ElevatedButton(text='Conversão para preto e branco', on_click=handle_convert_to_white_and_black, col={"md":4}),
         ft.ElevatedButton(text='Histograma', on_click=handle_histogram, col={"sm": 4}),
         ft.ElevatedButton(text='Cortar', on_click=handle_cut, col={"sm": 4}),
         ft.ElevatedButton(text='Filtro vermelho', on_click=handle_red_filter, col={"sm": 4}),
         ]
    )

    page.add(rrow_button)
    
ft.app(target=main)