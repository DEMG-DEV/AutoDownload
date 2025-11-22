# Facebook Image Downloader (Go Version)

Esta es la versión en Go de la aplicación de descarga de imágenes de Facebook.

## Requisitos

- [Go](https://go.dev/dl/) 1.21 o superior.
- Google Chrome instalado (para `chromedp`).

## Instalación y Ejecución

1.  Abre una terminal en esta carpeta (`go-app`).
2.  Inicializa las dependencias (si no se han descargado):

    ```bash
    go mod tidy
    ```

3.  Ejecuta la aplicación:

    ```bash
    go run main.go
    ```

## Compilación y Distribución

He preparado un `Makefile` para facilitar la generación de ejecutables para Windows, Mac y Linux.

### Requisitos Previos
- **Go**: Necesario para compilar.
- **Docker**: Necesario para generar los ejecutables de Windows y Linux desde Mac (usando `fyne-cross`).

### Comandos Disponibles

1.  **Instalar herramientas de compilación**:
    ```bash
    make install-deps
    ```
    Esto instalará `fyne` y `fyne-cross`.

2.  **Generar todos los ejecutables**:
    ```bash
    make all
    ```

3.  **Generar por plataforma**:
    - Mac: `make build-mac`
    - Windows: `make build-windows`
    - Linux: `make build-linux`

Los ejecutables de Windows y Linux se guardarán en la carpeta `fyne-cross/bin`. El de Mac se generará en la carpeta actual.
