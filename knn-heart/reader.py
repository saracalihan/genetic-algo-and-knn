# CSV dosyasını aç ve oku
def read_csv(path):
    with open(path, 'r') as file:
        # İlk satırda başlıklar olabilir
        header = file.readline().strip().split(',')
        data = []
        # Kalan satırları oku ve virgülle ayırarak parçala
        for line in file:
            # Satırdaki boşlukları temizle ve virgülle ayır
            row = line.strip().split(',')
            data.append(row)
    return header, data
