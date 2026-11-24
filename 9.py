import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
print("Training Data:", x_train.shape)
print("Testing Data:", x_test.shape)
x_train = x_train / 255.0
x_test = x_test / 255.0
x_train = x_train.reshape(-1, 28, 28, 1)
x_test = x_test.reshape(-1, 28, 28, 1)
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(28, 28, 1)),
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
model.summary()
history = model.fit(x_train,y_train,epochs=5,batch_size=64,validation_split=0.1
)
print("\n========== CONVOLUTION KERNEL MATRICES ==========")
for layer in model.layers:
    if isinstance(layer, tf.keras.layers.Conv2D):
        weights, biases = layer.get_weights()
        print("\nLayer Name:", layer.name)
        print("Kernel Shape:", weights.shape)
        print("\nFirst Kernel Matrix:")
        print(weights[:, :, 0, 0])
        print("\nFirst Bias:")
        print(biases[0])
test_loss, test_accuracy = model.evaluate(x_test, y_test)
print("\n========== MODEL RESULTS ==========")
print("Test Loss:", test_loss)
print("Test Accuracy:", test_accuracy * 100, "%")
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('CNN Model Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.grid()
plt.show()
prediction = model.predict(x_test[:1])
predicted_digit = np.argmax(prediction)
print("\n========== PREDICTION ==========")
print("Actual Digit:", y_test[0])
print("Predicted Digit:", predicted_digit)
plt.imshow(x_test[0].reshape(28, 28), cmap='gray')
plt.title("Predicted Digit: " + str(predicted_digit))
plt.axis('off')
plt.show()