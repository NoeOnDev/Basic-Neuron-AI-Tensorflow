import os
import shutil
import pandas as pd
import numpy as np
import tensorflow as tf
from graficas import plot_evolucion_error, plot_comparacion_y, plot_evolucion_pesos

def recrear_directorios():
    directorios = ['graficas_epocas', 'grafica_evolucion_error', 'grafica_evolucion_pesos']
    for directorio in directorios:
        if os.path.exists(directorio):
            shutil.rmtree(directorio)
        os.makedirs(directorio)

def cargar_datos(ruta_archivo):
    conjunto_datos = pd.read_csv(ruta_archivo)
    x = conjunto_datos[['x1', 'x2', 'x3', 'x4']].values
    y = conjunto_datos['y'].values
    return x, y

def crear_modelo():
    modelo = tf.keras.Sequential([
        tf.keras.layers.Dense(1, input_shape=(4,), activation='linear')
    ])
    return modelo

def entrenar_modelo(modelo, x, y, epocas):
    historial_pesos = []
    
    class PesosCallback(tf.keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs=None):
            pesos, sesgo = modelo.layers[0].get_weights()
            historial_pesos.append(np.append(pesos.flatten(), sesgo))
    
    historial = modelo.fit(x, y, epochs=epocas, callbacks=[PesosCallback()])
    return historial, historial_pesos

def ejecutar_entrenamiento(ruta_archivo, tasa_aprendizaje, epocas):
    recrear_directorios()
    x, y = cargar_datos(ruta_archivo)

    modelo = crear_modelo()
    
    opt = tf.keras.optimizers.Adam(learning_rate=tasa_aprendizaje)
    modelo.compile(optimizer=opt, loss='mean_squared_error')
    
    historial, historial_pesos, predicciones_por_epoca = entrenar_modelo(modelo, x, y, epocas)
    
    historial_costos = historial.history['loss']
    
    plot_evolucion_error(epocas, historial_costos)
    plot_comparacion_y(y, predicciones_por_epoca[0], 0)
    plot_comparacion_y(y, predicciones_por_epoca[epocas // 2], epocas // 2)
    plot_comparacion_y(y, predicciones_por_epoca[-1], epocas - 1)
    plot_evolucion_pesos(epocas, historial_pesos)
    
    pesos = modelo.layers[0].get_weights()[0].flatten()
    sesgo = modelo.layers[0].get_weights()[1].flatten()[0]
    
    return pesos, sesgo, historial_costos[-1]

