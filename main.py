import sys
import subprocess
import os

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QVBoxLayout,
    QMessageBox,
    QTextEdit
)


class OpenModelicaGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OpenModelica Simulation Launcher")
        self.setGeometry(200, 200, 450, 350)

        layout = QVBoxLayout()

        # Executable selection
        self.exe_label = QLabel("Select Application:")
        self.exe_input = QLineEdit()

        self.browse_btn = QPushButton("Browse")
        self.browse_btn.clicked.connect(self.browse_file)

        # Start time
        self.start_label = QLabel("Start Time:")
        self.start_input = QLineEdit()

        # Stop time
        self.stop_label = QLabel("Stop Time:")
        self.stop_input = QLineEdit()

        # Run button
        self.run_btn = QPushButton("Run Simulation")
        self.run_btn.clicked.connect(self.run_simulation)

        # Output box (NEW)
        self.output_label = QLabel("Output:")
        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)

        layout.addWidget(self.exe_label)
        layout.addWidget(self.exe_input)
        layout.addWidget(self.browse_btn)

        layout.addWidget(self.start_label)
        layout.addWidget(self.start_input)

        layout.addWidget(self.stop_label)
        layout.addWidget(self.stop_input)

        layout.addWidget(self.run_btn)

        layout.addWidget(self.output_label)
        layout.addWidget(self.output_box)

        self.setLayout(layout)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName()
        self.exe_input.setText(file_path)

    def run_simulation(self):
        exe = self.exe_input.text()
        start = self.start_input.text()
        stop = self.stop_input.text()

        # Validation
        try:
            start = int(start)
            stop = int(stop)

            if not (0 <= start < stop < 5):
                QMessageBox.warning(
                    self,
                    "Invalid Input",
                    "Ensure: 0 <= start < stop < 5"
                )
                return

        except:
            QMessageBox.warning(
                self,
                "Invalid Input",
                "Start and Stop must be integers"
            )
            return

        exe_name = os.path.basename(exe)

        command = [
            exe,
            "-override",
            f"startTime={start},stopTime={stop}"
        ]

        # Show output info
        self.output_box.append("Running Simulation...")
        self.output_box.append(f"Executable: {exe_name}")
        self.output_box.append(f"Start Time: {start}")
        self.output_box.append(f"Stop Time: {stop}")
        self.output_box.append("----------------------------------")

        try:
            self.run_btn.setEnabled(False)

            subprocess.run(command)

            self.run_btn.setEnabled(True)

            self.output_box.append("Simulation Completed Successfully\n")

            QMessageBox.information(
                self,
                "Success",
                "Simulation completed"
            )

        except Exception as e:
            self.run_btn.setEnabled(True)

            self.output_box.append(f"Error: {str(e)}\n")

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )


app = QApplication(sys.argv)
window = OpenModelicaGUI()
window.show()
sys.exit(app.exec())