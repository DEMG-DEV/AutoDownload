# Facebook Image Downloader

Una aplicación de escritorio sencilla para descargar imágenes de una URL de Facebook (Página o Perfil) utilizando Selenium y CustomTkinter.

## Requisitos Previos

- Python 3.8 o superior
- Google Chrome instalado

## Instalación

1.  Clona el repositorio o descarga los archivos.
2.  Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

## Ejecución (Modo Script)

Para ejecutar la aplicación directamente desde el código fuente:

```bash
python main.py
```

## Compilación (Crear Ejecutable)

Para crear un ejecutable independiente (.exe en Windows, .app en Mac, binario en Linux), utilizamos `PyInstaller`.

### 1. Instalar PyInstaller

Si no lo has hecho en el paso de instalación:

```bash
pip install pyinstaller
```

### 2. Compilar

Ejecuta el siguiente comando en tu terminal:

```bash
pyinstaller --noconfirm --onefile --windowed --name "FBDownloader" --add-data "venv/lib/python3.x/site-packages/customtkinter;customtkinter/" main.py
```

> **Nota Importante sobre CustomTkinter**: A veces PyInstaller no detecta automáticamente los archivos de datos de CustomTkinter. Si el comando anterior falla o la app no abre, intenta usar este comando más simple y asegúrate de que `customtkinter` esté bien instalado:

```bash
pyinstaller --noconfirm --onefile --windowed --name "FBDownloader" main.py
```

### 3. Ejecutable

El archivo ejecutable se generará en la carpeta `dist/`.

### Nota sobre Compilación Multiplataforma

PyInstaller crea ejecutables **para el sistema operativo en el que se ejecuta**.
- Para crear un `.exe` de Windows, debes compilar en Windows.
- Para crear una `.app` de Mac, debes compilar en macOS.
- Para crear un binario de Linux, debes compilar en Linux.

Si necesitas generar ejecutables para todos los sistemas, deberás usar una máquina virtual o un sistema de CI/CD (como GitHub Actions) que ejecute la compilación en cada sistema operativo.
