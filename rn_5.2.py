# Actividad 5.2 
from tensorflow.keras import layers, models, optimizers, losses, Input
from d2l import tensorflow as d2l

model = models.Sequential([
    Input(shape=(28, 28)),
    layers.Flatten(),
    layers.Dense(256, activation='relu'),
    layers.Dense(10)
])

model.compile(optimizer=optimizers.SGD(learning_rate=0.1),
              loss=losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

batch_size = 256
train_iter, test_iter = d2l.load_data_fashion_mnist(batch_size)

num_epochs = 10
history = model.fit(train_iter, epochs=num_epochs)

test_loss, test_acc = model.evaluate(test_iter)
print(f'Test accuracy: {test_acc:.3f}')
