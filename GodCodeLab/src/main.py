from unittests.test_runner import TestRunner
import sys
from lib.des import Des
from lib.filehandler import FileHandler
from lib.logutils import LogUtils
from datetime import datetime

class Main:
    def __init__(self):
        pass
        
    def process_line(self, line, config):
        """Processes a single chat line, returning the prog_sum and a progressive sum string."""
        query = config.get("session", {}).get("query", "")
        des_to_get = config.get("session", {}).get("des", "")
        line = query + line
        des = Des.get_instance(des_to_get,
            line)
        des_str = str(des)
        return des_str
        
    @staticmethod
    def format_table(headers, rows):
        """Creates a simple ASCII table from headers and rows."""
        col_widths = [max(len(str(item)) for item in col) for col in zip(headers, *rows)]
        sep_line = '+' + '+'.join('-' * (w + 2) for w in col_widths) + '+'
        header_row = '|' + '|'.join(f' {h.ljust(w)} ' for h, w in zip(headers, col_widths)) + '|'
        row_lines = []
        for row in rows:
            row_line = '|' + '|'.join(f' {str(item).ljust(w)} ' for item, w in zip(row, col_widths)) + '|'
            row_lines.append(row_line)
        table = '\n'.join([sep_line, header_row, sep_line] + row_lines + [sep_line])
        return table

    def format_nested_table(self, params):
        """Formats the nested parameters into a structured table."""
        rows = []
        for section, details in params.items():
            if isinstance(details, dict):
                rows.append([section, ""])
                for key, value in details.items():
                    rows.append([f"|{key}|", value if value is not None else ""])
            else:
                rows.append([section, details])
        return self.format_table(["Parameter", "Value"], rows)

    ########################################################################
    #                               Start                                  #
    ########################################################################
    def start(self):
        ver_major, ver_minor = "11_05", "001.001"
        ver = f"{ver_major}_{ver_minor}"
        input_file = "config.yaml"
        output_file = "output/output.md"

        file_handler = FileHandler(input_file, output_file)
        self.logutils = LogUtils(file_handler)
        config = file_handler.read_input()

        now = datetime.now()
        formatted_now = now.strftime("%Y/%m/%d-%H:%M:%S.%f")[:-3] + f" {now.strftime('%A')}"
        info_headers = ["Program", "Version", "Timestamp"]
        info_rows = [["God Chat API", ver, formatted_now]]
        info_table = self.format_table(info_headers, info_rows)
        self.logutils.log(info_table)

        # Log all supplied parameters in a nested format
        params_data = {
            "godcode": config.get("godcode", {}),
            "application": config.get("application", {}),
            "session": config.get("session", {}),
        }
        params_table = self.format_nested_table(params_data)
        self.logutils.log("Supplied Parameters:\n" + params_table)

        chat_lines_config = config.get("chat_lines", [])
        if isinstance(chat_lines_config, dict) and "source_file" in chat_lines_config:
            source_file = chat_lines_config["source_file"]
            try:
                with open(source_file, "r") as f:
                    chat_lines = [line.strip() for line in f if line.strip()]
            except Exception as e:
                self.logutils.log(f"Error reading source file '{source_file}': {e}")
                chat_lines = []
        elif isinstance(chat_lines_config, list):
            chat_lines = chat_lines_config
        else:
            chat_lines = []

        ########################################################################
        #                          Process Lines                               #
        ########################################################################
        qr_rows = []
        for line in chat_lines:
            des_str = self.process_line(line,config)
            qr_rows.append([line, des_str])

        if qr_rows:
            qr_table = self.format_table(["Query", "Reply"], qr_rows)
            self.logutils.log("Query/Reply Log:\n" + qr_table)
        else:
            self.logutils.log("No chat lines to process.")

        self.logutils.log("Completed.")


########################################################################
#                          Main Runner                                 #
########################################################################
if __name__ == "__main__":
    # Run unit tests first
    test_result = TestRunner().run_all_tests()
    if not test_result.wasSuccessful():
        sys.exit("Unit tests failed. Aborting execution.")
    
    # Then run the main program
    Main().start()
