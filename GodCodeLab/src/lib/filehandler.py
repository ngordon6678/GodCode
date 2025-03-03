import yaml

class FileHandler:
    """Handles input and output file operations."""
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def read_input(self):
        """Parses YAML input file."""
        with open(self.input_file, "r") as file:
            return yaml.safe_load(file)

    def write_output(self, text):
        """Writes text to output file."""
        with open(self.output_file, "a") as file:
            file.write(text)

