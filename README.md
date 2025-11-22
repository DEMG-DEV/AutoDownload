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

## Compilación

Para crear un ejecutable independiente:

```bash
go build -o FBDownloader main.go
```

(En Windows se generará `FBDownloader.exe`).
