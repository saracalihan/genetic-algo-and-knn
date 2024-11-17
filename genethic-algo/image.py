import random

# PGM dosyasını okuma fonksiyonu
def read_pgm(filename):
    with open(filename, 'rb') as f:
        # İlk satırı oku (P5 veya P2 olduğunu doğrula)
        format_code = f.readline().decode().strip()
        assert format_code == 'P5', "Dosya P5 formatında değil!"

        # Yorum satırlarını atla
        line = f.readline().decode().strip()
        while line.startswith('#'):
            line = f.readline().decode().strip()

        # Genişlik ve yükseklik değerlerini al
        width, height = map(int, line.split())
        
        # Maksimum gri değeri oku
        max_val = int(f.readline().decode().strip())
        
        # Piksel verilerini oku
        pixel_data = f.read()
        image = [[pixel_data[i * width + j] for j in range(width)] for i in range(height)]
        
    return image, width, height, max_val

# PGM dosyasını yazma fonksiyonu
def write_pgm(image, width, height, max_val, filename):
    with open(filename, 'w') as f:
        f.write('P2\n')
        f.write(f'{width} {height}\n')
        f.write(f'{max_val}\n')
        for row in image:
            f.write(' '.join(map(str, row)) + '\n')

def write_pgm_from_patches(patches, patch_size, width, height, max_val, filename):
    # Boş bir 2D liste oluştur (tam boyutlu görüntü için)
    image = [[0] * width for _ in range(height)]

    # Dikey olarak ikiye bölündüğü için, önce sol yarıyı sonra sağ yarıyı ekleyeceğiz
    mid_width = width // 2
    patch_idx = 0
    step_size = height // patch_size

    # Sol yarıyı yerleştir
    for i in range(0, height, step_size):
        for k in range(step_size):
            if i + k < height:
                image[i + k][:mid_width] = patches[patch_idx][k]
        patch_idx += 1

    # Sağ yarıyı yerleştir
    for i in range(0, height, step_size):
        for k in range(step_size):
            if i + k < height:
                image[i + k][mid_width:] = patches[patch_idx][k]
        patch_idx += 1

    # PGM dosyasına yazma
    with open(filename, 'w') as f:
        f.write('P2\n')
        f.write(f'{width} {height}\n')
        f.write(f'{max_val}\n')
        for row in image:
            f.write(' '.join(map(str, row)) + '\n')

# Resmi patchlere ayırma fonksiyonu
def split_into_patches(image, patch_size):
    height = len(image)
    width = len(image[0])

    # Dikey olarak iki parçaya böl (her parça yarım genişlik olacak)
    mid_width = width // 2
    patches = []

    # Sol yarıyı patch_size kadar yatay parçalara böl
    step_size = height // patch_size
    for i in range(0, height, step_size):
        patch = [row[:mid_width] for row in image[i:i + step_size]]
        patches.append(patch)

    # Sağ yarıyı patch_size kadar yatay parçalara böl
    for i in range(0, height, step_size):
        patch = [row[mid_width:] for row in image[i:i + step_size]]
        patches.append(patch)


    return patches

def shuffle_patches(patches, patch_size, width, height):
    random.shuffle(patches)
    shuffled_patches = patches
    shuffled_image = []

    step_size = height // patch_size
    # Boş bir 2D liste oluştur
    for i in range(height):
        shuffled_image.append([0] * width)

    # Karıştırılmış patch'leri sırayla shuffled_image içine yerleştir
    mid_width = width // 2
    index = 0
    for i in range(0, height, step_size):
        # Sol yarıya yerleştir
        for k in range(step_size):
            if i + k < height:
                shuffled_image[i + k][:mid_width] = patches[index][k]
        index += 1
        # Sağ yarıya yerleştir
        for k in range(step_size):
            if i + k < height:
                shuffled_image[i + k][mid_width:] = patches[index][k]
        index += 1 
    return shuffled_image, shuffled_patches

