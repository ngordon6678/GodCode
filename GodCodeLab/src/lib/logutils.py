class LogUtils:
    def __init__(self, file_handler):
        self.file_handler = file_handler
        
    def log(self, text):
        """Logs text to output file."""
        self.file_handler.write_output(text + "\n")
        print(text)

