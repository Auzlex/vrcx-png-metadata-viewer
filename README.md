# Simple VRCX/PNG Metadata Viewer

This application allows you to view metadata from PNG images, including VRCX application metadata.

**Note:** This viewer may not work with Discord image previews. However, any image uploaded to Discord and opened fully will work when dragged into the application.

**Developer's Note:** Not sure why I made this...

## Usage

1. **Drag and Drop:** Drag and drop a PNG file or URL into the application window.

    ![alt text](image.png)

2. **View Metadata:** The application will display metadata information extracted from the PNG image or URL.

    ![alt text](image-1.png)

3. **VRCX Metadata:** If the metadata contains VRCX application data, it will be displayed in a structured format, including world name, world ID, and player information.

## Dependencies

- Python 3.x
- PyQt5
- PIL (Python Imaging Library)
- requests (for URL image retrieval)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Auzlex/vrcx-png-metadata-viewer
    cd vrcx-png-metadata-viewer
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:

    ```bash
    python execute.py
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
