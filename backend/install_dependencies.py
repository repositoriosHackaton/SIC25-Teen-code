import subprocess

def install_dependencies():
    # Lista de dependencias
    dependencies = [
        "django",
        "djangorestframework",
        "django-cors-headers",
        "beautifulsoup4",
        "requests",
        "SpeechRecognition"
        "pandas",
        "selenium",
        "scikit-learn",
        "plotly",
        "spacy",
        "pygame",
        "gtts",
        "seaborn",
        "matplotlib",
    ]

    print("Instalando dependencias...")

    for dependency in dependencies:
        try:
            subprocess.check_call(["pip", "install", dependency])
            print(f"Dependencia instalada: {dependency}")
        except subprocess.CalledProcessError as e:
            print(f"Error al instalar {dependency}: {e}")

    print("Instalación de dependencias completada.")

if __name__ == "__main__":
    install_dependencies()
