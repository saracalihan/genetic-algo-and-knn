
def euclidean_distance(point1, point2):
    distance = 0
    for i in range(len(point1)):
        distance += (point1[i] - point2[i]) ** 2
    return distance ** 0.5

def knn_predict(X_train, y_train, X_test, k):
    predictions = []
    for test_point in X_test:
        # Compute distances from the test point to all training points
        distances = [(euclidean_distance(test_point, x), label) for x, label in zip(X_train, y_train)]
        # Sort by distance and get k nearest labels
        nearest_labels = [label for _, label in sorted(distances)[:k]]
        # Predict the majority class
        prediction = max(set(nearest_labels), key=nearest_labels.count)
        predictions.append(prediction)
    return predictions

def evaluate_model(y_true, y_pred):
    tp = fp = fn = tn = 0
    for true, pred in zip(y_true, y_pred):
        if true == "1" and pred == "1":
            tp += 1  # True Positive
        elif true == "1" and pred == "0":
            fn += 1  # False Negative
        elif true == "0" and pred == "1":
            fp += 1  # False Positive
        elif true == "0" and pred == "0":
            tn += 1  # True Negative

    accuracy = (tp + tn) / (tp + tn + fp + fn) #başaro oranı
    precision = tp / (tp + fp) if (tp + fp) != 0 else 0 #doğruluk
    recall = tp / (tp + fn) if (tp + fn) != 0 else 0 #hassaslık
    confusion_matrix = [[tp, fp], [fn, tn]]
    return accuracy, precision, recall, confusion_matrix
