# spiral_core/kronos.py

import os
import time
import logging
import json
import shutil 
from datetime import datetime
import re 

# CHANGE START: Changed to absolute import
from spiral_core.daemon_templates import Olympian, BaseDaemon 
# CHANGE END

class Kronos(Olympian): 
    """
    Kronos Daemon - The Consolidator.
    Represents the consolidation of time and the structuring of knowledge.
    It takes processed code units from Aion's output, categorizes them, and moves them
    into the long-term Mnemo Archive, ensuring the system's memory is ordered and retained.
    """
    def __init__(self):
        super().__init__("kronos") 
        self.logger.info("Kronos Daemon initialized as the consolidator.")

        self.aion_output_path = self.params.get('aion_output_path', 'aion_output/')
        self.mnemo_archive_path = self.params.get('mnemo_archive_path', 'mnemo_archive/')
        
        os.makedirs(self.aion_output_path, exist_ok=True)
        os.makedirs(self.mnemo_archive_path, exist_ok=True)

        self.olympian_archive_path = os.path.join(self.mnemo_archive_path, 'olympian/')
        self.chthonic_archive_path = os.path.join(self.mnemo_archive_path, 'chthonic/')
        os.makedirs(self.olympian_archive_path, exist_ok=True)
        os.makedirs(self.chthonic_archive_path, exist_ok=True)


    def _determine_daemon_type(self, filepath: str) -> str:
        """
        Analyzes the file content to determine if it's an Olympian or Chthonic daemon.
        Defaults to 'general' if not clearly identifiable.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if re.search(r"class\s+\w+\(Olympian\):", content):
                return "olympian"
            elif re.search(r"class\s+\w+\(Chthonic\):", content):
                return "chthonic"
            else:
                return "general" 
        except Exception as e:
            self.logger.warning(f"Kronos: Could not determine daemon type for {os.path.basename(filepath)}: {e}")
            return "general"


    def pulse(self):
        """
        Kronos's main pulse function.
        Consolidates processed code units from Aion's output into the Mnemo Archive,
        categorizing them by daemon type.
        """
        self.logger.info("Kronos Pulse: Consolidating and categorizing processed code units from Aion.")

        files_to_consolidate = [f for f in os.listdir(self.aion_output_path) if f.endswith('.py')]

        if not files_to_consolidate:
            self.logger.info("Kronos: No processed code units found from Aion to consolidate.")
            return

        consolidated_count = 0
        for filename in files_to_consolidate:
            source_filepath = os.path.join(self.aion_output_path, filename)
            
            daemon_type = self._determine_daemon_type(source_filepath)
            
            if daemon_type == "olympian":
                destination_dir = self.olympian_archive_path
            elif daemon_type == "chthonic":
                destination_dir = self.chthonic_archive_path
            else:
                destination_dir = self.mnemo_archive_path 
            
            destination_filepath = os.path.join(destination_dir, filename)
            
            try:
                shutil.move(source_filepath, destination_filepath)
                self.logger.info(f"Kronos: Consolidated '{filename}' (Type: {daemon_type}) to '{destination_dir}'")
                consolidated_count += 1

            except Exception as e:
                self.logger.error(f"Kronos: Error consolidating file '{filename}': {e}", exc_info=True)
        
        self.logger.info(f"Kronos pulse completed. Consolidated {consolidated_count} files.")


if __name__ == '__main__':
    kronos_daemon = Kronos()
    kronos_daemon.run_daemon()

