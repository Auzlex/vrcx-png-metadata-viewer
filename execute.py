"""
    A simple image VRCX/Png image metadata viewer

    NOTE: This does not seem to work with discord image previews, 
    however any uploaded image to discord opened fully will work when dragged in.

    Auzlex: Not sure why I made this...
"""
import sys
import json
import requests
from io import BytesIO
from PIL import Image
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem
)

class MetadataExtractor(QMainWindow):
    """
    This class represents the main application window for the PNG Metadata Extractor.
    """

    def __init__(self):
        """
        Initializes the MetadataExtractor window.
        """
        super().__init__()
        self.setWindowTitle("PNG Metadata Extractor")
        self.setGeometry(100, 100, 400, 200)

        # Create a label for displaying instructions and metadata
        self.label = QLabel("Drag and drop a PNG file or URL here")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)  # Enable word wrapping
        self.label.setStyleSheet("QLabel { font-weight: bold; }")  # Set text to bold

        # Enable text copying
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        # Set up the layout for the window
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)

        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        # Allow the window to accept drops of PNG files
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        """
        Event handler for when a drag enters the window.
        Checks if the dragged content is a PNG file OR HTTP/HTTPS URL.
        """

        # detect if we have urls if so handle logic for .png or http/https urls
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.isLocalFile() and url.toString().endswith(".png"):
                    event.acceptProposedAction()
                    return
                elif not url.isLocalFile() and url.scheme() in ["http", "https"]:
                    event.acceptProposedAction()
                    return
        
        # if none of the above ignore it
        event.ignore()

    def dropEvent(self, event):
        """
        Event handler for when a drop occurs in the window.
        Extracts metadata from the dropped PNG file and displays it.
        """

        url = event.mimeData().urls()[0].toString() # grab the event url
        if url.endswith(".png"): # is it a png?
            # cool grab the file
            self.load_from_file(event.mimeData().urls()[0].toLocalFile())
        else:
            self.load_from_url(url) # load from url

    def load_from_url(self, url):
        """
            load_from_url is invoked when we want to load an image from a http/https url
        """
        try:
            # url request the image
            response = requests.get(url)
            if response.status_code == 200: # if its good then we bytes io the content
                image = Image.open(BytesIO(response.content))
                self.process_image(image) # process image as normal
            else:
                self.label.setText(f"Failed to load image from URL.\nStatus code: {response.status_code}")
        except Exception as e:
            self.label.setText(f"Failed to load image from URL.\nError: {str(e)}")

    def load_from_file(self, png_path):
        """
            load_from_file is invoked when we want to load from a .png file
        """

        try: # attempt to open the image and grab the metadata

            image = Image.open(png_path)
            self.process_image(image)

        except Exception as e:

            # set a error message of what happened and why we could not grab the metadata
            self.label.setText(f"\nload_from_file invoked Error: {str(e)}")

    def process_image(self, image):
        """
            process_image handles a PILLOW image object and attempts to grab metadata from the image
        """

        try: # attempt to open the image and grab the metadata

            metadata = image.info # get info

            try: # attempt to grab json data
                self.json_data = json.loads(metadata.get("Description"))

                # Check if metadata contains VRCX application data
                self.display_vrcx_data()
    
            except Exception as e: 
                # if no json data
                print(f"failed to read json dat {e}")
                self.display_regular_metadata(metadata)

        except Exception as e:

            # set a error message of what happened and why we could not grab the metadata
            self.label.setText(f"No metadata found.\nError: {str(e)}")

    def display_regular_metadata(self, metadata):
        """
        Display regular metadata for non-VRCX images.
        """
        formatted_metadata = "\n".join([f"<b>{key}:</b> {value}" for key, value in metadata.items()])
        self.label.setText(f"<center>Metadata:</center>\n{formatted_metadata}")
        self.clear_table() # clear the table

    def display_vrcx_data(self):
        """
        Display VRCX application metadata.
        """
        world_name = self.json_data['world']['name']
        world_id = self.json_data['world']['id']
        players = self.json_data['players']

        self.label.setText(f"<b><font size='5'>'{world_name}'</font></b>\n<b>World ID:</b> '{world_id}' contained {len(players)} players")

        # Create the table only if json_data contains players
        if "players" in self.json_data:
            self.create_table()

    def create_table(self):
        """
            creates a table with the desired header labels for VRCX Metadata
        """
        # clear the table
        self.clear_table()

        # Create a table to display user information
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["User ID", "Display Name"])

        # populate the table information
        self.populate_table(self.table)

        # add to the UI
        self.layout.addWidget(self.table)

    def populate_table(self, table):
        """
            Populates the QTableWidget with data from the players json
        """

        # grab players from json
        players = self.json_data.get("players", [])

        # set table row count
        table.setRowCount(len(players))

        # populate the information
        for i, player in enumerate(players):

            # if user id strip len str is 0 length we replace text with N/A
            user_id_item = QTableWidgetItem("N/A" if len(player.get("id", "").strip()) == 0 else player.get("id", "")) 

            display_name_item = QTableWidgetItem(player.get("displayName", ""))
            table.setItem(i, 0, user_id_item)
            table.setItem(i, 1, display_name_item)

        # Adjust column widths based on content length
        self.table.resizeColumnsToContents()

    def clear_table(self):
        """
        clears the active table if it exists and removes it from the Qt application
        """

        # check if table exists in the qt self app
        if hasattr(self, 'table'):

            # clear the table and remove its widget and delete for later, del from memory
            self.table.clear()
            self.layout.removeWidget(self.table)
            self.table.deleteLater()
            del self.table

if __name__ == "__main__":

    # create an instance of our app pass in our system arguments
    app = QApplication(sys.argv)

    # begin the MetadataExtractor
    window = MetadataExtractor()
    window.show()

    # quit the application
    sys.exit(app.exec_())