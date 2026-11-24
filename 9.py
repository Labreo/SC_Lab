import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np

print("=" * 60)
print("EXPERIMENT 9: CNN ON MNIST CHARACTER DATASET")
print("=" * 60)

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

print("\n--- DATASET DETAILS ---")
print("Dataset Name     : MNIST Handwritten Character Dataset")
print("Number of Classes: 10 (Characters '0' through '9')")
print("Training Samples :", x_train.shape[0])
print("Testing Samples  :", x_test.shape[0])
print(f"Sample Dimensions: {x_train.shape[1]}x{x_train.shape[2]} Grayscale")

x_train = x_train / 255.0
x_test = x_test / 255.0

x_train = x_train.reshape(-1, 28, 28, 1)
x_test = x_test.reshape(-1, 28, 28, 1)

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(28, 28, 1)),
    tf.keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu', name='conv2d_layer_1'),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2), name='maxpool_1'),
    tf.keras.layers.Conv2D(64, kernel_size=(3, 3), activation='relu', name='conv2d_layer_2'),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2), name='maxpool_2'),
    tf.keras.layers.Flatten(name='flatten'),
    tf.keras.layers.Dense(128, activation='relu', name='dense_hidden'),
    tf.keras.layers.Dense(10, activation='softmax', name='dense_output')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

print("\n--- MODEL ARCHITECTURE SUMMARY ---")
model.summary()

print("\n--- CONVOLUTION KERNELS CONFIGURED ---")
for layer in model.layers:
    if isinstance(layer, tf.keras.layers.Conv2D):
        print(f"Layer: {layer.name:<16} | Kernel Size: {layer.kernel_size} | Filters: {layer.filters} | Stride: {layer.strides} | Padding: {layer.padding} | Activation: {layer.activation.__name__}")

print("\n--- TRAINING CNN MODEL ---")
history = model.fit(
    x_train,
    y_train,
    epochs=5,
    batch_size=64,
    validation_split=0.1,
    verbose=1
)

print("\n" + "=" * 60)
print("CONVOLUTION KERNELS USED & LEARNED WEIGHT MATRICES")
print("=" * 60)

for layer in model.layers:
    if isinstance(layer, tf.keras.layers.Conv2D):
        weights, biases = layer.get_weights()
        print(f"\n==================================================")
        print(f"Layer Name          : {layer.name}")
        print(f"Kernel Size (H x W) : {layer.kernel_size[0]} x {layer.kernel_size[1]}")
        print(f"Number of Filters   : {layer.filters}")
        print(f"Input Channels      : {weights.shape[2]}")
        print(f"Weight Tensor Shape : {weights.shape}  (H, W, In_Channels, Out_Filters)")
        print(f"Bias Tensor Shape   : {biases.shape}")
        print(f"Activation Function : {layer.activation.__name__}")
        print("--------------------------------------------------")
        
        print("Learned Kernel Matrix (Filter 1, Channel 1):")
        for row in weights[:, :, 0, 0]:
            print("  [" + "  ".join(f"{v:8.4f}" for v in row) + " ]")
        print(f"Filter 1 Bias       : {biases[0]:.4f}")
        
        if weights.shape[3] > 1:
            print("\nLearned Kernel Matrix (Filter 2, Channel 1):")
            for row in weights[:, :, 0, 1]:
                print("  [" + "  ".join(f"{v:8.4f}" for v in row) + " ]")
            print(f"Filter 2 Bias       : {biases[1]:.4f}")

test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)

print("\n" + "=" * 60)
print("FINAL ACCURACY & PERFORMANCE METRICS")
print("=" * 60)
print(f"Final Training Accuracy   : {history.history['accuracy'][-1] * 100:.2f} %")
print(f"Final Validation Accuracy : {history.history['val_accuracy'][-1] * 100:.2f} %")
print(f"Final Test Accuracy       : {test_accuracy * 100:.2f} %")
print(f"Final Test Loss           : {test_loss:.4f}")

plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Training Accuracy', marker='o')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy', marker='s')
plt.title('CNN Model Accuracy vs Epochs')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Training Loss', marker='o', color='red')
plt.plot(history.history['val_loss'], label='Validation Loss', marker='s', color='orange')
plt.title('CNN Model Loss vs Epochs')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

conv1_weights = model.get_layer('conv2d_layer_1').get_weights()[0]
plt.figure(figsize=(8, 8))
for i in range(16):
    plt.subplot(4, 4, i + 1)
    plt.imshow(conv1_weights[:, :, 0, i], cmap='viridis')
    plt.title(f"Kernel {i+1}", fontsize=8)
    plt.axis('off')
plt.suptitle("Layer 1: First 16 Learned Convolution Kernels (3x3 Filters)", fontsize=11)
plt.tight_layout()
plt.show()

print("\n" + "=" * 60)
print("SAMPLE CHARACTER PREDICTION")
print("=" * 60)

class_names = [str(i) for i in range(10)]
sample_indices = [0, 1, 2]

for idx in sample_indices:
    sample_img = x_test[idx:idx+1]
    prediction = model.predict(sample_img, verbose=0)
    pred_class = np.argmax(prediction)
    confidence = prediction[0][pred_class] * 100
    actual_class = y_test[idx]
    
    print(f"\nSample Index        : {idx}")
    print(f"Actual Character    : '{class_names[actual_class]}'")
    print(f"Predicted Character : '{class_names[pred_class]}'")
    print(f"Prediction Confidence: {confidence:.2f} %")

plt.figure(figsize=(9, 3))
for i, idx in enumerate(sample_indices):
    sample_img = x_test[idx:idx+1]
    pred = model.predict(sample_img, verbose=0)
    pred_digit = np.argmax(pred)
    conf = pred[0][pred_digit] * 100
    
    plt.subplot(1, 3, i + 1)
    plt.imshow(x_test[idx].reshape(28, 28), cmap='gray')
    plt.title(f"Actual: '{class_names[y_test[idx]]}'\nPred: '{class_names[pred_digit]}' ({conf:.1f}%)")
    plt.axis('off')

plt.suptitle("MNIST Character Predictions with CNN", fontsize=11)
plt.tight_layout()
plt.show()

