def error(true_labels, predict_labels):
    deviation = abs(true_labels - predict_labels) / true_labels
    return deviation.mean()
