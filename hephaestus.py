# spiral_core/hephaestus.py

import os
import json
import time
import random
import logging
from datetime import datetime
import sys
import io
import traceback

# CHANGE START: Changed to absolute import
from spiral_core.daemon_templates import Olympian, BaseDaemon
# CHANGE END

class Hephaestus(Olympian): # Hephaestus inherits from Olympian
    """
    Hephaestus Daemon - The Forge.
    Manages a sandbox environment for executing and testing generated code units.
    """
    def __init__(self):
        super().__init__("hephaestus") # Pass daemon name to BaseDaemon constructor
        self.logger.info("Hephaestus Daemon initialized as the forge.")
        
        # Ensure necessary directories exist on startup, using paths from params
        self.hephaestus_forge_path = self.params.get('hephaestus_forge_path', 'hephaestus_forge/')
        self.hephaestus_experiment_results_path = self.params.get('hephaestus_experiment_results_path', 'hephaestus_experiment_results/')
        self.mnemo_archive_path = self.params.get('mnemo_archive_path', 'mnemo_archive/')

        # Create all necessary directories
        os.makedirs(self.hephaestus_forge_path, exist_ok=True)
        os.makedirs(self.hephaestus_experiment_results_path, exist_ok=True)
        os.makedirs(self.mnemo_archive_path, exist_ok=True)


    def execute_code_in_sandbox(self, code_content, experiment_id, sandbox_path):
        """
        Executes Python code in a simulated sandbox environment.
        Captures stdout, stderr, and returns execution status.
        """
        self.logger.info(f"Hephaestus: Executing code for experiment {experiment_id} in sandbox: {sandbox_path}")
        
        # Create a fresh, isolated environment for execution
        exec_globals = {
            '__builtins__': __builtins__, # Provide standard builtins
            'os': os, # Basic OS functions like creating dirs, for generated code
            'sys': sys,
            'random': random,
            'time': time,
            'json': json,
            # Potentially other safe modules the generated code might need
        }
        exec_locals = {} # Local namespace for the executed code

        # Redirect stdout and stderr to capture output
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        redirected_output = io.StringIO()
        redirected_error = io.StringIO()
        sys.stdout = redirected_output
        sys.stderr = redirected_error

        execution_result = "unknown"
        error_message = ""
        captured_stdout = ""
        captured_stderr = ""

        try:
            # Change current working directory to the sandbox for the execution duration
            original_cwd = os.getcwd()
            os.chdir(sandbox_path)
            
            exec(code_content, exec_globals, exec_locals)
            execution_result = "success"
        except SyntaxError as e:
            execution_result = "syntax_error"
            error_message = f"Syntax Error: {e}"
            self.logger.error(f"Hephaestus: Syntax Error in experiment {experiment_id}: {e}")
        except Exception as e:
            execution_result = "runtime_error"
            error_message = f"Runtime Error: {traceback.format_exc()}" # Get full traceback
            self.logger.error(f"Hephaestus: Runtime Error in experiment {experiment_id}: {e}")
        finally:
            # Restore stdout and stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            captured_stdout = redirected_output.getvalue()
            captured_stderr = redirected_error.getvalue()
            
            # Change back to original working directory
            os.chdir(original_cwd)

        return {
            "status": execution_result,
            "stdout": captured_stdout,
            "stderr": captured_stderr,
            "error_message": error_message
        }

    def pulse(self):
        """
        Hephaestus's main pulse function.
        Identifies a code unit, runs it, and logs results.
        """
        self.logger.info("Hephaestus: Forge pulse initiated.")

        # Find a Python file to experiment with from Mnemo's archive
        candidate_files = [f for f in os.listdir(self.mnemo_archive_path) if f.endswith('.py')]
        
        if not candidate_files:
            self.logger.info("Hephaestus: No Python files found in Mnemo archive to experiment with.")
            return

        # Pick a random file for now, or implement a selection strategy later
        file_to_test = os.path.join(self.mnemo_archive_path, random.choice(candidate_files))
        
        experiment_id = os.urandom(4).hex()
        self.logger.info(f"Hephaestus: Preparing experiment {experiment_id} with file: {os.path.basename(file_to_test)}")

        # Create a dedicated sandbox directory for this experiment
        current_forge_sandbox = os.path.join(self.hephaestus_forge_path, f"experiment_{experiment_id}")
        os.makedirs(current_forge_sandbox, exist_ok=True)

        try:
            with open(file_to_test, 'r', encoding='utf-8') as f:
                code_content = f.read()

            # Execute the code
            execution_report = self.execute_code_in_sandbox(code_content, experiment_id, current_forge_sandbox)
            
            # Save experiment results for Apollo
            result_filename = f"experiment_{experiment_id}_result.json"
            result_file_path = os.path.join(self.hephaestus_experiment_results_path, result_filename)
            
            # Add metadata to the report
            execution_report['timestamp'] = datetime.now().isoformat()
            execution_report['tested_file'] = os.path.basename(file_to_test)
            execution_report['sandbox_path'] = current_forge_sandbox

            with open(result_file_path, 'w', encoding='utf-8') as f:
                json.dump(execution_report, f, indent=4)
            
            self.logger.info(f"Hephaestus: Experiment {experiment_id} finished. Status: {execution_report['status']}. Results saved to {result_file_path}")

        except Exception as e:
            self.logger.error(f"Hephaestus: Error during experiment {experiment_id} for file {os.path.basename(file_to_test)}: {e}", exc_info=True)
            # Log a basic error report if something went wrong before execution
            error_report = {
                "status": "hephaestus_internal_error",
                "tested_file": os.path.basename(file_to_test),
                "error_message": str(e),
                "timestamp": datetime.now().isoformat()
            }
            result_filename = f"experiment_{experiment_id}_error.json"
            result_file_path = os.path.join(self.hephaestus_experiment_results_path, result_filename)
            with open(result_file_path, 'w', encoding='utf-8') as f:
                json.dump(error_report, f, indent=4)

        finally:
            # Clean up the sandbox directory (optional, or Apollo can do it)
            # For now, we'll leave it for inspection if needed.
            pass

        self.logger.info("Hephaestus: Forge pulse completed.")

if __name__ == '__main__':
    hephaestus_daemon = Hephaestus()
    hephaestus_daemon.run_daemon()

