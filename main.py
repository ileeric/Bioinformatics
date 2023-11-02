import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QListWidget, QListWidgetItem, QGroupBox, QFormLayout, QMessageBox, QProgressBar
import ncbi
from PyQt6.QtCore import QThread, pyqtSignal

possibleGenId = 0
class Worker(QThread):
    requestFinished = pyqtSignal(bool, list)
    sequenceRetrieved = pyqtSignal(bool, object)

    def __init__(self, gene_name):
        super().__init__()
        self.gene_name = gene_name

    def run(self):
        global possibleGenId

        requestRes, possibleGenId = ncbi.nameToId(self.gene_name, type="nucleotide")
        self.requestFinished.emit(requestRes, possibleGenId)
        if requestRes:
            for id in possibleGenId:
                res, sequence = ncbi.geneSequence(id, type="nucleotide")
                self.sequenceRetrieved.emit(res, sequence)


class GeneSequenceUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Gene Sequence Viewer')
        self.setWindowIcon(QIcon('assets/icon.png'))
        self.setGeometry(100, 100, 500, 500)
        self.layout = QVBoxLayout()
        self.input_layout = QHBoxLayout()
        self.output_layout = QVBoxLayout()
        self.input_label = QLabel('Enter Gene Name:')
        self.input_text = QLineEdit()
        self.request_button = QPushButton('Request')
        self.request_button.clicked.connect(self.make_request)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)  # Set the range to be between 0 and 100 percent
        self.layout.addWidget(self.progress_bar)
        self.output_label = QLabel('Gene Sequences:')
        self.output_list = QListWidget()
        self.output_list.itemClicked.connect(self.show_sequence_properties)
        self.details_group_box = QGroupBox('Gene Details')
        self.details_layout = QFormLayout()
        self.details_group_box.setLayout(self.details_layout)
        self.input_layout.addWidget(self.input_label)
        self.input_layout.addWidget(self.input_text)
        self.input_layout.addWidget(self.request_button)
        self.output_layout.addWidget(self.output_label)
        self.output_layout.addWidget(self.output_list)
        self.layout.addLayout(self.input_layout)
        self.layout.addLayout(self.output_layout)
        self.layout.addWidget(self.details_group_box)
        self.setLayout(self.layout)
        self.geneInfo = dict()
        self.sequences = []

    def clearLayout(self, myLayout):
        while myLayout.count():
            child = myLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def make_request(self):
        self.request_button.setEnabled(False)
        self.progress_bar.setValue(0)
        gene_name = self.input_text.text()

        self.geneInfo = dict()
        self.sequences = []

        self.clearLayout(self.output_layout)

        self.worker = Worker(gene_name)
        self.worker.requestFinished.connect(self.handle_request_finished)
        self.worker.sequenceRetrieved.connect(self.handle_sequence_retrieved)
        self.worker.start()

    def handle_request_finished(self, requestRes):
        if not requestRes:
            self.output_list.clear()
            self.output_list.addItem('Network Error.')
        # Re-enable the request button after the worker thread finishes
        self.request_button.setEnabled(True)
        self.progress_bar.setValue(100)

    def handle_sequence_retrieved(self, res, sequence):
        if res:
            self.sequences.append(sequence)
            self.geneInfo[sequence.fullname] = {'Code': sequence.code,
                                                'Full Name': sequence.fullname,
                                                'NCBI ID': str(sequence.ncbiId),
                                                'Sequence': sequence.sequence,
                                                'Base pairs': str(sequence.basepair) + 'bp'}
            item = QListWidgetItem(sequence.fullname)
            item.setData(1, {'GeneName': sequence.fullname})
            self.output_list.addItem(item)
            progress_percentage = int((len(self.sequences) / len(possibleGenId)) * 100)
            self.progress_bar.setValue(progress_percentage)


    def show_sequence_properties(self, item):
        properties = item.data(1)
        sequence = properties['GeneName']
        self.output_list.clearSelection()
        self.output_list.setCurrentItem(item)
        self.output_list.scrollToItem(item)
        self.show_gene_details(sequence)

    def show_gene_details(self, sequence):
        print(self.geneInfo)
        try:
            self.clearLayout(self.details_layout)
            for category, value in self.geneInfo[sequence].items():
                label = QLabel(category)
                field = QLabel(value)
                self.details_layout.addRow(label, field)
        except:
            self.clearLayout(self.details_layout)
            self.details_layout.addRow(QLabel('Error'), QLabel('Could not retrieve gene details.'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gene_sequence_ui = GeneSequenceUI()
    gene_sequence_ui.show()
    sys.exit(app.exec())