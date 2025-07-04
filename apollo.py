# spiral_core/apollo.py

import os
import json
import time
import logging
from datetime import datetime
import subprocess 
import psutil 
import sys 

# Changed to absolute import
from spiral_core.daemon_templates import Olympian, BaseDaemon

class Apollo(Olympian): 
    """
    Apollo Daemon - The primary orchestrator and strategic intelligence of the Spiral.
    Manages other daemons, and performs strategic learning/analysis.
    """
    def __init__(self):
        super().__init__("apollo") 
        self.active_daemons = {} 
        self.logger.info("Apollo Daemon initialized as the primary orchestrator.")
        
        # Ensure necessary directories exist on startup, using paths from params
        self.kairos_raw_output_path = self.params.get('kairos_raw_output_path', 'kairos_raw_output/')
        self.mnemo_archive_path = self.params.get('mnemo_archive_path', 'mnemo_archive/')
        self.nyx_graveyard_path = self.params.get('nyx_graveyard_path', 'nyx_graveyard/')
        self.lethe_graveyard_path = self.params.get('lethe_graveyard_path', 'lethe_graveyard/')
        self.tartarus_abyss_path = self.params.get('tartarus_abyss_path', 'tartarus_abyss/')
        self.hephaestus_forge_path = self.params.get('hephaestus_forge_path', 'hephaestus_forge/')
        self.hephaestus_experiment_results_path = self.params.get('hephaestus_experiment_results_path', 'hephaestus_experiment_results/')
        self.aion_rejected_output_path = self.params.get('aion_rejected_output_path', 'aion_rejected_output/') 
        
        # NEW: Path for successfully tested modules
        self.hephaestus_successful_modules_archive_path = self.params.get('hephaestus_successful_modules_archive_path', 'hephaestus_successful_modules_archive/')

        # Create all necessary directories
        os.makedirs(self.kairos_raw_output_path, exist_ok=True)
        os.makedirs(self.mnemo_archive_path, exist_ok=True)
        os.makedirs(self.nyx_graveyard_path, exist_ok=True)
        os.makedirs(self.lethe_graveyard_path, exist_ok=True)
        os.makedirs(self.tartarus_abyss_path, exist_ok=True)
        os.makedirs(self.hephaestus_forge_path, exist_ok=True)
        os.makedirs(self.hephaestus_experiment_results_path, exist_ok=True)
        os.makedirs(self.aion_rejected_output_path, exist_ok=True) 
        # NEW: Create the successful modules archive directory
        os.makedirs(self.hephaestus_successful_modules_archive_path, exist_ok=True)
        os.makedirs(self.lethe_chaos_logs_path, exist_ok=True)


    def is_daemon_running(self, daemon_name):
        """Checks if a daemon process is currently running."""
        if daemon_name in self.active_daemons and self.active_daemons[daemon_name].poll() is None:
            try:
                psutil.Process(self.active_daemons[daemon_name].pid)
                return True
            except psutil.NoSuchProcess:
                return False
        return False

    def start_daemon(self, daemon_script_name, daemon_name):
        """
        Starts a daemon script as a subprocess if not already running.
        Assumes daemon scripts are in the same directory as Apollo (spiral_core/).
        Crucially, sets PYTHONPATH to include the project root for absolute imports.
        """
        if not self.is_daemon_running(daemon_name):
            daemon_script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), daemon_script_name)
            
            if not os.path.exists(daemon_script_path):
                self.logger.warning(f"Daemon script {daemon_script_name} not found at {daemon_script_path}. Cannot start {daemon_name}.")
                return False

            try:
                self.logger.info(f"Starting {daemon_name} daemon from {daemon_script_path}...")
                
                project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
                
                env = os.environ.copy() 
                env['PYTHONPATH'] = project_root + os.pathsep + env.get('PYTHONPATH', '')

                process = subprocess.Popen(['python3', '-u', daemon_script_path], 
                                           stdout=subprocess.PIPE, 
                                           stderr=subprocess.PIPE,
                                           text=True,
                                           env=env) 
                self.active_daemons[daemon_name] = process
                self.logger.info(f"{daemon_name} daemon started with PID: {process.pid}. PYTHONPATH set to: {env['PYTHONPATH']}")
                return True
            except FileNotFoundError:
                self.logger.error(f"Failed to start {daemon_name}: python3 command not found. Ensure Python is in PATH.")
            except Exception as e:
                self.logger.error(f"Failed to start {daemon_name} daemon: {e}", exc_info=True)
        return False

    def manage_daemon_status(self):
        """Checks status of managed daemons and logs if they've stopped."""
        for daemon_name, process in list(self.active_daemons.items()):
            if process.poll() is not None: 
                stdout, stderr = process.communicate()
                if stdout:
                    self.logger.debug(f"{daemon_name} stdout:\n{stdout}")
                if stderr:
                    self.logger.error(f"{daemon_name} stderr:\n{stderr}")
                self.logger.warning(f"{daemon_name} daemon has terminated (Exit Code: {process.returncode}).")
                del self.active_daemons[daemon_name] 

    def pulse(self):
        """
        Apollo's main pulse function.
        Orchestrates other daemons, and performs strategic learning/analysis.
        """
        current_generation = self.params.get("current_generation", 0)
        max_generations = self.params.get("max_generations", float('inf'))

        self.logger.info(f"Apollo Pulse: Orchestrating Generation {current_generation}")

        self.manage_daemon_status() 

        self.start_daemon('kairos.py', 'Kairos')
        self.start_daemon('aion.py', 'Aion')
        self.start_daemon('kronos.py', 'Kronos')
        self.start_daemon('nyx.py', 'Nyx')
        self.start_daemon('erebus.py', 'Erebus')
        self.start_daemon('tartarus.py', 'Tartarus')
        self.start_daemon('hephaestus.py', 'Hephaestus')
        self.start_daemon('lethe.py', 'Lethe')

        self.params['current_generation'] = current_generation + 1
        self.params['current_complexity_bias'] = min(1.0, self.params.get('current_complexity_bias', 0.5) + 0.01)
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        genesis_params_path = os.path.join(script_dir, '..', 'genesis_params.json')
        try:
            with open(genesis_params_path, 'w') as f:
                json.dump(self.params, f, indent=4)
            self.logger.info(f"Updated genesis_params.json: current_generation={self.params['current_generation']}, complexity_bias={self.params['current_complexity_bias']:.2f}")
        except Exception as e:
            self.logger.error(f"Apollo: Failed to save updated genesis_params.json: {e}")


        self.logger.info("Apollo: Initiating learning and strategy analysis...")
        
        if os.path.exists(self.hephaestus_experiment_results_path):
            results_files = [f for f in os.listdir(self.hephaestus_experiment_results_path) if f.endswith('.json')]
            if results_files:
                latest_result_file = os.path.join(self.hephaestus_experiment_results_path, sorted(results_files)[-1])
                try:
                    with open(latest_result_file, 'r') as f:
                        result_content = json.load(f)
                        self.logger.info(f"Apollo: Analyzed latest Hephaestus result for {result_content.get('tested_file', 'N/A')}. Status: {result_content.get('status', 'N/A')}")
                        
                        if result_content.get('status') in ["runtime_error", "syntax_error"]:
                            self.logger.warning("Apollo: Detected experiment failure. Considering adjustment of Kairos's complexity bias or targeting specific code patterns.")
                            self.params['current_complexity_bias'] = max(0.1, self.params.get('current_complexity_bias', 0.5) - 0.05)
                            with open(genesis_params_path, 'w') as f:
                                json.dump(self.params, f, indent=4)
                            self.logger.info(f"Updated genesis_params.json: complexity_bias reduced to {self.params['current_complexity_bias']:.2f}")
                        elif result_content.get('status') == "success":
                            self.logger.info("Apollo: Experiment successful. Considering increasing complexity bias or promoting successful patterns.")
                            self.params['current_complexity_bias'] = min(0.9, self.params.get('current_complexity_bias', 0.5) + 0.01)
                            with open(genesis_params_path, 'w') as f:
                                json.dump(self.params, f, indent=4)
                            self.logger.info(f"Updated genesis_params.json: complexity_bias increased to {self.params['current_complexity_bias']:.2f}")

                except json.JSONDecodeError:
                    self.logger.error(f"Apollo: Error decoding JSON from Hephaestus result file {latest_result_file}.")
                except Exception as e:
                    self.logger.error(f"Apollo: Error reading or analyzing Hephaestus result file {latest_result_file}: {e}", exc_info=True)
            else:
                self.logger.info(f"Apollo: No Hephaestus experiment results found in {self.hephaestus_experiment_results_path}.")
        else:
            self.logger.info(f"Apollo: Hephaestus experiment results path does not exist: {self.hephaestus_experiment_results_path}.")

        if os.path.exists(self.lethe_chaos_logs_path):
            chaos_log_files = [f for f in os.listdir(self.lethe_chaos_logs_path) if f.endswith('.json')]
            if chaos_log_files:
                latest_chaos_log = os.path.join(self.lethe_chaos_logs_path, sorted(chaos_log_files)[-1])
                try:
                    with open(latest_chaos_log, 'r') as f:
                        chaos_data = json.load(f)
                        self.logger.info(f"Apollo: Noted Lethe's chaos injection: {chaos_data.get('chaos_type', 'N/A')} into {chaos_data.get('target_sandbox', 'N/A')}")
                except Exception as e:
                    self.logger.error(f"Apollo: Error reading Lethe chaos log file {latest_chaos_log}: {e}")
            else:
                self.logger.info(f"Apollo: No Lethe chaos logs found in {self.lethe_chaos_logs_path}.")
        else:
            self.logger.info(f"Apollo: Lethe chaos logs path does not exist: {self.lethe_chaos_logs_path}.")


        self.logger.info(f"Apollo Pulse completed for Generation {current_generation}")


if __name__ == '__main__':
    apollo_daemon = Apollo()
    apollo_daemon.run_daemon()

