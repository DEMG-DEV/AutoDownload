package main

import (
	"context"
	"errors"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"time"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/dialog"
	"fyne.io/fyne/v2/widget"
	"github.com/chromedp/chromedp"
)

func main() {
	a := app.New()
	w := a.NewWindow("Facebook Image Downloader")
	w.Resize(fyne.NewSize(600, 400))

	// UI Components
	titleLabel := widget.NewLabelWithStyle("Facebook Image Downloader", fyne.TextAlignCenter, fyne.TextStyle{Bold: true})

	urlEntry := widget.NewEntry()
	urlEntry.SetPlaceHolder("Enter Facebook Page/Profile URL")

	folderEntry := widget.NewEntry()
	folderEntry.SetPlaceHolder("Select Download Folder")
	folderEntry.Disable() // Read-only, set by button

	var folderPath string

	browseButton := widget.NewButton("Browse", func() {
		dialog.ShowFolderOpen(func(uri fyne.ListableURI, err error) {
			if err == nil && uri != nil {
				folderPath = uri.Path()
				folderEntry.SetText(folderPath)
			}
		}, w)
	})

	countEntry := widget.NewEntry()
	countEntry.SetText("5")
	countLabel := widget.NewLabel("Number of Images:")

	statusLabel := widget.NewLabel("Ready")
	statusLabel.Alignment = fyne.TextAlignCenter

	var downloadBtn *widget.Button
	downloadBtn = widget.NewButton("Download Images", func() {
		url := urlEntry.Text
		countStr := countEntry.Text
		maxImages, err := strconv.Atoi(countStr)

		if err != nil || maxImages <= 0 {
			dialog.ShowError(errors.New("Please enter a valid number of images"), w)
			return
		}
		if url == "" {
			dialog.ShowError(errors.New("Please enter a Facebook URL"), w)
			return
		}
		if folderPath == "" {
			dialog.ShowError(errors.New("Please select a download folder"), w)
			return
		}

		downloadBtn.Disable()
		downloadBtn.SetText("Downloading...")
		statusLabel.SetText(fmt.Sprintf("Starting download process for %d images...", maxImages))

		go func() {
			defer func() {
				downloadBtn.Enable()
				downloadBtn.SetText("Download Images")
			}()

			err := downloadImages(url, folderPath, maxImages, func(status string) {
				statusLabel.SetText(status)
			})

			if err != nil {
				statusLabel.SetText("Error: " + err.Error())
				dialog.ShowError(err, w)
			} else {
				statusLabel.SetText(fmt.Sprintf("Successfully downloaded images to %s", folderPath))
				dialog.ShowInformation("Success", "Download complete!", w)
			}
		}()
	})

	// Layout
	content := container.NewVBox(
		titleLabel,
		widget.NewLabel(""), // Spacer
		urlEntry,
		widget.NewLabel(""), // Spacer
		container.NewBorder(nil, nil, nil, browseButton, folderEntry),
		widget.NewLabel(""), // Spacer
		container.NewHBox(countLabel, countEntry),
		widget.NewLabel(""), // Spacer
		downloadBtn,
		widget.NewLabel(""), // Spacer
		statusLabel,
	)

	w.SetContent(container.NewPadded(content))
	w.ShowAndRun()
}

func downloadImages(url, folder string, maxImages int, updateStatus func(string)) error {
	// Create context
	opts := append(chromedp.DefaultExecAllocatorOptions[:],
		chromedp.DisableGPU,
		chromedp.Flag("disable-notifications", true),
		// chromedp.Flag("headless", false), // Uncomment to see the browser
	)
	allocCtx, cancel := chromedp.NewExecAllocator(context.Background(), opts...)
	defer cancel()

	ctx, cancel := chromedp.NewContext(allocCtx)
	defer cancel()

	// Set timeout for the whole operation (optional, e.g., 5 minutes)
	ctx, cancel = context.WithTimeout(ctx, 5*time.Minute)
	defer cancel()

	updateStatus("Initializing Browser...")

	var imageURLs []string

	err := chromedp.Run(ctx,
		chromedp.Navigate(url),
		chromedp.ActionFunc(func(ctx context.Context) error {
			updateStatus(fmt.Sprintf("Navigating to %s...", url))
			// Wait for initial load - simple sleep or wait for body
			time.Sleep(5 * time.Second)
			return nil
		}),
		chromedp.ActionFunc(func(ctx context.Context) error {
			updateStatus(fmt.Sprintf("Scrolling to find %d images...", maxImages))
			
			// Simple scrolling logic
			// In a real scenario, we might need more robust waiting/scrolling
			uniqueURLs := make(map[string]bool)
			
			for len(uniqueURLs) < maxImages {
				var srcs []string
				// Execute JS to get all image srcs
				err := chromedp.Evaluate(`Array.from(document.querySelectorAll('img')).map(i => i.src)`, &srcs).Do(ctx)
				if err != nil {
					return err
				}

				for _, src := range srcs {
					if strings.Contains(src, "scontent") {
						uniqueURLs[src] = true
						if len(uniqueURLs) >= maxImages {
							break
						}
					}
				}

				if len(uniqueURLs) >= maxImages {
					break
				}

				// Scroll down
				err = chromedp.Evaluate(`window.scrollTo(0, document.body.scrollHeight);`, nil).Do(ctx)
				if err != nil {
					return err
				}
				time.Sleep(2 * time.Second)
			}

			for u := range uniqueURLs {
				imageURLs = append(imageURLs, u)
			}
			return nil
		}),
	)

	if err != nil {
		return err
	}

	if len(imageURLs) == 0 {
		return errors.New("no images found")
	}

	updateStatus(fmt.Sprintf("Found %d images. Downloading...", len(imageURLs)))

	count := 0
	for i, imgURL := range imageURLs {
		if i >= maxImages {
			break
		}

		err := downloadFile(imgURL, filepath.Join(folder, fmt.Sprintf("fb_image_%d.jpg", i+1)))
		if err != nil {
			fmt.Printf("Failed to download %s: %v\n", imgURL, err)
			continue
		}
		count++
	}

	if count == 0 {
		return errors.New("failed to download any images")
	}

	return nil
}

func downloadFile(url, filepath string) error {
	resp, err := http.Get(url)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		return fmt.Errorf("received non-200 response code: %d", resp.StatusCode)
	}

	out, err := os.Create(filepath)
	if err != nil {
		return err
	}
	defer out.Close()

	_, err = io.Copy(out, resp.Body)
	return err
}
