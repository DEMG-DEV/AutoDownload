import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Facebook Image Downloader")
        self.geometry("600x400")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=1)

        # Title
        self.title_label = ctk.CTkLabel(self, text="Facebook Image Downloader", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # URL Input
        self.url_entry = ctk.CTkEntry(self, placeholder_text="Enter Facebook Page/Profile URL")
        self.url_entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # Destination Folder
        self.folder_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.folder_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.folder_frame.grid_columnconfigure(0, weight=1)
        self.folder_frame.grid_columnconfigure(1, weight=0)

        self.folder_path = ctk.StringVar()
        self.folder_entry = ctk.CTkEntry(self.folder_frame, textvariable=self.folder_path, placeholder_text="Select Download Folder", state="readonly")
        self.folder_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        self.browse_button = ctk.CTkButton(self.folder_frame, text="Browse", command=self.browse_folder, width=100)
        self.browse_button.grid(row=0, column=1)

        # Image Count Input
        self.count_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.count_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        self.count_label = ctk.CTkLabel(self.count_frame, text="Number of Images:", width=120)
        self.count_label.pack(side="left", padx=(0, 10))
        
        self.count_entry = ctk.CTkEntry(self.count_frame, width=60)
        self.count_entry.pack(side="left")
        self.count_entry.insert(0, "5") # Default value

        # Download Button
        self.download_button = ctk.CTkButton(self, text="Download Images", command=self.start_download_thread)
        self.download_button.grid(row=4, column=0, padx=20, pady=20)

        # Status/Log
        self.status_label = ctk.CTkLabel(self, text="Ready", text_color="gray")
        self.status_label.grid(row=5, column=0, padx=20, pady=10)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def start_download_thread(self):
        url = self.url_entry.get()
        folder = self.folder_path.get()
        try:
            max_images = int(self.count_entry.get())
            if max_images <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of images")
            return

        if not url:
            messagebox.showerror("Error", "Please enter a Facebook URL")
            return
        if not folder:
            messagebox.showerror("Error", "Please select a download folder")
            return

        self.download_button.configure(state="disabled", text="Downloading...")
        self.status_label.configure(text=f"Starting download process for {max_images} images...", text_color="blue")
        
        thread = threading.Thread(target=self.download_images, args=(url, folder, max_images))
        thread.start()

    def download_images(self, url, folder, max_images):
        driver = None
        try:
            options = Options()
            # options.add_argument("--headless") # Headless might be detected more easily, keep visible for now or debug
            options.add_argument("--disable-notifications")
            options.add_argument("--start-maximized")
            
            self.update_status("Initializing Browser...")
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

            self.update_status(f"Navigating to {url}...")
            driver.get(url)
            time.sleep(5) # Wait for initial load

            self.update_status(f"Scrolling to find {max_images} images...")
            
            image_urls = set()
            scroll_attempts = 0
            max_scrolls = max_images * 2 # Allow more scrolls for more images
            
            while len(image_urls) < max_images and scroll_attempts < max_scrolls:
                # Find images
                images = driver.find_elements(By.TAG_NAME, "img")
                for img in images:
                    src = img.get_attribute("src")
                    if src and "scontent" in src: # Facebook images usually contain 'scontent'
                        # Filter out small icons/emojis if possible by checking size (requires more complex logic or just assumption)
                        # For now, just collect unique URLs
                        width = img.get_attribute("width")
                        height = img.get_attribute("height")
                        
                        # Basic filter: skip very small images if dimensions are available
                        if width and int(width) < 100: continue
                        if height and int(height) < 100: continue
                        
                        image_urls.add(src)
                        if len(image_urls) >= max_images:
                            break
                
                if len(image_urls) < max_images:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(3)
                    scroll_attempts += 1
            
            if not image_urls:
                self.update_status("No suitable images found. You might need to login manually in the browser window if prompted.")
                # Give user a chance to login if they see the window
                time.sleep(5) 
                # Try one more time
                images = driver.find_elements(By.TAG_NAME, "img")
                for img in images:
                    src = img.get_attribute("src")
                    if src and "scontent" in src:
                        image_urls.add(src)
                        if len(image_urls) >= max_images: break

            self.update_status(f"Found {len(image_urls)} images. Downloading...")
            
            count = 0
            for i, img_url in enumerate(list(image_urls)[:max_images]):
                try:
                    response = requests.get(img_url, stream=True)
                    if response.status_code == 200:
                        file_path = os.path.join(folder, f"fb_image_{i+1}.jpg")
                        with open(file_path, 'wb') as f:
                            for chunk in response.iter_content(1024):
                                f.write(chunk)
                        count += 1
                except Exception as e:
                    print(f"Error downloading {img_url}: {e}")

            self.update_status(f"Successfully downloaded {count} images!", color="green")
            messagebox.showinfo("Success", f"Downloaded {count} images to {folder}")

        except Exception as e:
            self.update_status(f"Error: {str(e)}", color="red")
            messagebox.showerror("Error", str(e))
        finally:
            if driver:
                driver.quit()
            self.download_button.configure(state="normal", text="Download Images")

    def update_status(self, text, color="black"):
        self.status_label.configure(text=text, text_color=color)

if __name__ == "__main__":
    app = App()
    app.mainloop()
