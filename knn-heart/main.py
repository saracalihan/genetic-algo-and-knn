from knn import knn_predict, evaluate_model
from reader import read_csv
import config

# CSV dosyasını oku
header, data = read_csv("data.csv")

# Veriyi yüzde 75 oranında eğitim ve yüzde 25 oranında test olarak ayır
train_size = int(len(data) * config.train_test_rate)

# Eğitim verisi
X_train = [list(map(float, row[:-1])) for row in data[:train_size]]  # Özellikler
y_train = [row[-1] for row in data[:train_size]]  # Etiketler

# Test verisi
X_test = [list(map(float, row[:-1])) for row in data[train_size:]]

# KNN tahminini yap
y_pred = knn_predict(X_train, y_train, X_test, config.k)
total_predictions = len(y_pred)
y_true = [row[-1] for row in data[-total_predictions:]]

accuracy, precision, recall, confusion_matrix = evaluate_model(y_true, y_pred)

print(f"Data: {header}")
print(f"Configs:\n\tK: {config.k}\n\tTrain Test Split: {config.train_test_rate*100} - {100 - config.train_test_rate*100} \n\tTrain Data Count:{train_size}/{len(data)}\n\tTest Data Count: {len(X_test)}/{len(data)}")
print(f"Accuracy:  {accuracy:.4f}", )
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"Confusion Matrix: {confusion_matrix}")
