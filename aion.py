# spiral_core/aion.py

import os
import time
import logging
import json
import shutil 
from datetime import datetime
import ast 

# CHANGE START: Changed to absolute import
from spiral_core.daemon_templates import Olympian, BaseDaemon 
# CHANGE END

class Aion(Olympian): 
    """
    Aion Daemon - The Flow Processor.
    Represents the continuous flow of time and the processing of information.
    It takes the raw output from Kairos, processes it into a more refined state,
    performs basic validation, and moves it towards the Mnemo Archive for consolidation by Kronos.
    """
    def __init__(self):
        super().__init__("aion") 
        self.logger.info("Aion Daemon initialized as the flow processor.")

        self.kairos_raw_path = self.params.get('kairos_raw_output_path', 'kairos_raw_output/')
        self.kairos_processed_path = self.params.get('kairos_processed_path', 'kairos_processed_output/') 
        self.aion_output_path = self.params.get('aion_output_path', 'aion_output/')
        self.aion_rejected_path = self.params.get('aion_rejected_output_path', 'aion_rejected_output/') 
        
        os.makedirs(self.kairos_raw_path, exist_ok=True)
        os.makedirs(self.kairos_processed_path, exist_ok=True)
        os.makedirs(self.aion_output_path, exist_ok=True)
        os.makedirs(self.aion_rejected_path, exist_ok=True) 


    def _validate_syntax(self, code_content: str, filename: str) -> bool:
        """
        Performs a basic syntax validation on the Python code content.
        Returns True if syntax is valid, False otherwise.
        """
        try:
            ast.parse(code_content, filename=filename)
            self.logger.debug(f"Aion: Syntax check passed for '{filename}'.")
            return True
        except SyntaxError as e:
            self.logger.warning(f"Aion: Syntax error detected in '{filename}': {e}")
            return False
        except Exception as e:
            self.logger.error(f"Aion: Unexpected error during syntax validation for '{filename}': {e}", exc_info=True)
            return False


    def pulse(self):
        """
        Aion's main pulse function.
        Processes raw code units from Kairos, validates them, and prepares them for Kronos.
        """
        self.logger.info("Aion Pulse: Processing raw code units from Kairos.")

        files_to_process = [f for f in os.listdir(self.kairos_raw_path) if f.endswith('.py')]

        if not files_to_process:
            self.logger.info("Aion: No raw code units found from Kairos to process.")
            return

        processed_count = 0
        rejected_count = 0
        for filename in files_to_process:
            source_filepath = os.path.join(self.kairos_raw_path, filename)
            
            try:
                with open(source_filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if not self._validate_syntax(content, filename):
                    rejected_filepath = os.path.join(self.aion_rejected_path, filename)
                    shutil.move(source_filepath, rejected_filepath)
                    self.logger.warning(f"Aion: Rejected invalid file '{filename}'. Moved to '{self.aion_rejected_path}'")
                    rejected_count += 1
                    continue 
                
                processed_content = f"# Processed by Aion on {datetime.now().isoformat()}\n" \
                                    f"# Original file: {filename}\n" \
                                    f"{content}"
                
                destination_filepath = os.path.join(self.aion_output_path, filename)
                with open(destination_filepath, 'w', encoding='utf-8') as f:
                    f.write(processed_content)
                
                os.remove(source_filepath)
                self.logger.info(f"Aion: Processed and moved '{filename}' to '{self.aion_output_path}'")
                processed_count += 1

            except Exception as e:
                self.logger.error(f"Aion: Error processing file '{filename}': {e}", exc_info=True)
        
        self.logger.info(f"Aion pulse completed. Processed {processed_count} files, Rejected {rejected_count} files.")


if __name__ == '__main__':
    aion_daemon = Aion()
    aion_daemon.run_daemon()

