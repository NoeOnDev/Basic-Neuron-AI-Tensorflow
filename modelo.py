import os
import shutil
import pandas as pd
import numpy as np
import tensorflow as tf
from d2l import tensorflow as d2l
from graficas import plot_evolucion_error, plot_comparacion_y, plot_evolucion_pesos

def recrear_directorios():
    directorios = ['graficas_epocas', 'grafica_evolucion_error', 'grafica_evolucion_pesos']
    for directorio in directorios:
        if os.path.exists(directorio):
            shutil.rmtree(directorio)
        os.makedirs(directorio)

def cargar_datos(ruta_archivo):
    conjunto_datos = pd.read_csv(ruta_archivo)
    x1 = conjunto_datos['x1'].values
    x2 = conjunto_datos['x2'].values
    x3 = conjunto_datos['x3'].values
    x4 = conjunto_datos['x4'].values
    yd = conjunto_datos['y'].values

    x = np.column_stack((x1, x2, x3, x4))
    y = yd

    return x, y

class LinearRegression(tf.keras.Model):
    def __init__(self):
        super(LinearRegression, self).__init__()
        self.dense = tf.keras.layers.Dense(1, kernel_initializer=tf.random_normal_initializer())

    def call(self, inputs):
        return self.dense(inputs)

def ejecutar_entrenamiento(ruta_archivo, tasa_aprendizaje, epocas):
    recrear_directorios()
    x, y = cargar_datos(ruta_archivo)
    
    model = LinearRegression()
    optimizer = tf.keras.optimizers.SGD(learning_rate=tasa_aprendizaje)
    loss_object = tf.keras.losses.MeanSquaredError()

    train_dataset = tf.data.Dataset.from_tensor_slices((x, y)).shuffle(len(x)).batch(32)
    
    historial_costos = []
    historial_pesos = []

    for epoch in range(epocas):
        for features, labels in train_dataset:
            with tf.GradientTape() as tape:
                predictions = model(features)
                loss = loss_object(labels, predictions)
            gradients = tape.gradient(loss, model.trainable_variables)
            optimizer.apply_gradients(zip(gradients, model.trainable_variables))

        y_predicho = model(x).numpy().flatten()
        costo = np.mean((y - y_predicho) ** 2)
        
        print(f"Época {epoch} - Costo: {costo}")
        print(f"Pesos: {model.trainable_variables[0].numpy().flatten()}")
        print(f"Sesgo: {model.trainable_variables[1].numpy().flatten()}")

        historial_costos.append(costo)
        historial_pesos.append(np.append(model.trainable_variables[0].numpy().flatten(), model.trainable_variables[1].numpy().flatten()))

        if epoch == 0 or epoch == epocas // 2 or epoch == epocas - 1:
            plot_comparacion_y(y, y_predicho, epoch)

    y_predicho = model(x).numpy().flatten()
    costo_final = np.mean((y - y_predicho) ** 2)

    plot_evolucion_error(epocas, historial_costos)
    plot_evolucion_pesos(epocas, historial_pesos)
    
    return model.trainable_variables[0].numpy().flatten(), model.trainable_variables[1].numpy().flatten(), costo_final
