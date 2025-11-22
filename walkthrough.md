# Facebook Image Downloader Walkthrough

I have created a desktop application that allows you to download images from a Facebook URL.

## Prerequisities
Ensure you have Google Chrome installed, as the application uses it to scrape images.

## How to Run
1.  Open your terminal.
2.  Navigate to the project directory:
    ```bash
    cd /Users/devco/CourtBetSD/AutoDownload
    ```
3.  Run the application:
    ```bash
    python main.py
    ```

## How to Use
1.  **Enter URL**: Paste the URL of a Facebook Page or Profile in the input field (e.g., `https://www.facebook.com/natgeo`).
2.  **Select Folder**: Click "Browse" to choose where you want to save the images.
3.  **Image Count**: Enter the number of images you want to download (default is 5).
4.  **Download**: Click "Download Images".
    - A Chrome window will open. **Do not close it**.
    - The script will scroll and look for images.
    - Once finished, it will show a success message and the images will be in your selected folder.

## Troubleshooting
-   **Login Popup**: If Facebook asks for login and blocks the view, the script might fail to find images. You can try logging in manually in the opened Chrome window if you trust the session, or try a public page that doesn't require login.
-   **No Images Found**: Some pages are heavily protected or use different layouts. The script looks for standard `img` tags with `scontent` in the URL.
