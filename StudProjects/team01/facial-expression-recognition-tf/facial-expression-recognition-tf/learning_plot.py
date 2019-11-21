import numpy as np
import matplotlib.pyplot as plt

file_path = 'models/fer_training_0.1_lr_square_loss/_emotion_training.log'
file = open(file_path, 'r')
lines = file.readlines()

epochs, accuracy, losses, val_accuracy, val_losses = [], [], [], [], []

for line in lines[1:]:
    ep, acc, loss, val_acc, val_loss = line.split(',')
    epochs.append(ep)
    accuracy.append(float(acc))
    losses.append(float(loss))
    val_accuracy.append(float(val_acc))
    val_losses.append(float(val_loss))

plt.plot(epochs, accuracy, label="accuracy")
plt.plot(epochs, losses, label="loss")
plt.plot(epochs, val_accuracy, label="val_accuracy")
plt.plot(epochs, val_losses, label="val_loss")

plt.legend()
plt.show()