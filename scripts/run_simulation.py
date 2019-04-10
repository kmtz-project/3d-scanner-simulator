from src import variables
from src.scanner_simulator import ScannerSimulatorApp

scanner_simulator = ScannerSimulatorApp(variables.left_captures_path, variables.right_captures_path)
scanner_simulator.run()
