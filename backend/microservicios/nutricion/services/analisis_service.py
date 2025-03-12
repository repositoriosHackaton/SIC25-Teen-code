from ..utils.data_utils import cargar_datos, filtrar_datos
from ..utils.graficos_utils import configurar_estilo, formato_tiempo, render_grafico
import seaborn as sns
import matplotlib.pyplot as plt

class AnalisisService:
    @staticmethod
    def dificultad_vs_valoracion(dificultad, tipo):
        clasificacion, df = cargar_datos()
        df = filtrar_datos(clasificacion, df, dificultad, tipo)
        configurar_estilo()

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=df, x='Dificultad', y='Valoracion', ax=ax)
        ax.set_facecolor('black')
        plt.title("Dificultad vs Valoración", fontsize=16, color='white')
        plt.xlabel("Dificultad", fontsize=14, color='white')
        plt.ylabel("Valoración (%)", fontsize=14, color='white')

        return render_grafico(fig)

    @staticmethod
    def duracion_vs_dificultad(dificultad, tipo):
        clasificacion, df = cargar_datos()
        df = filtrar_datos(clasificacion, df, dificultad, tipo)
        configurar_estilo()

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=df, x='Duracion', y='Dificultad', ax=ax)
        formato_tiempo(ax)
        ax.set_facecolor('black')
        plt.title("Duración vs Dificultad", fontsize=16, color='white')
        plt.xlabel("Duración", fontsize=14, color='white')
        plt.ylabel("Dificultad", fontsize=14, color='white')
        ax.invert_yaxis()

        return render_grafico(fig)

    @staticmethod
    def barras_dificultad(dificultad, tipo):
        clasificacion, df = cargar_datos()
        df = filtrar_datos(clasificacion, df, dificultad, tipo)
        configurar_estilo()

        fig, ax = plt.subplots(figsize=(10, 6))
        nivel_counts = df["Dificultad"].value_counts(sort=False)
        sns.barplot(x=nivel_counts.index, y=nivel_counts.values, ax=ax)
        ax.set_facecolor('black')
        plt.title("Comparación de Niveles de Dificultad", fontsize=16, color='white')
        plt.xlabel("Nivel de Dificultad", fontsize=14, color='white')
        plt.ylabel("Cantidad de Recetas", fontsize=14, color='white')

        return render_grafico(fig)