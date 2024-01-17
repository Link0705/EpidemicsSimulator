from functools import partial
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, Qt
from src.epidemics_simulator.gui.ui_widget_creator import UiWidgetCreator
from src.epidemics_simulator.gui.templates import templates

class UiStartup(QtWidgets.QDialog):
    def __init__(self, parent):
        super(UiStartup, self).__init__()
        self.setWindowTitle('Network tool')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setStyleSheet(parent.styleSheet())
        self.parent = parent
        self.resize(200, 400)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.default_alignment = self.layout().alignment()
        self.back_icon = QIcon('assets/back.png')
        
                
    def launch_startup(self):
        self.add_startup_buttons()
        self.show()
        
    def add_startup_buttons(self):
        self.parent.unload_items_from_layout(self.layout())
        self.layout().setAlignment(self.default_alignment)
        new_button: QtWidgets.QPushButton = UiWidgetCreator.create_qpush_button('New', 'new_network_button')
        new_from_template_button: QtWidgets.QPushButton = UiWidgetCreator.create_qpush_button('New from template', 'new_template_button')
        open_button: QtWidgets.QPushButton = UiWidgetCreator.create_qpush_button('Open', 'open_network_button')
        
        new_button.clicked.connect(lambda: self.new_network())
        new_from_template_button.clicked.connect(lambda: self.new_from_template())
        open_button.clicked.connect(lambda: self.open_network())
        
        self.layout().addWidget(new_button)
        self.layout().addWidget(new_from_template_button)
        self.layout().addWidget(open_button)
        
    def new_from_template(self):
        self.parent.unload_items_from_layout(self.layout())
        self.layout().setAlignment(Qt.AlignTop)
        for i in range(0, len(templates)):
            template = templates[i]
            template = UiWidgetCreator.create_qpush_button(template.name, 'new_network')
            template.clicked.connect(partial(self.new_template_network, i))
            self.layout().addWidget(template)
        back = UiWidgetCreator.create_qpush_button(None, 'back_button')
        back.setIcon(self.back_icon)
        back.clicked.connect(lambda: self.add_startup_buttons())
        self.layout().addWidget(back)
        
    def new_network(self):
        if not self.parent.new_network(self):
            return
        self.close_startup()
        
    def new_template_network(self, template_id):
        if not self.parent.new_network(self, template_id):
            return
        self.close_startup()
        
    def open_network(self):
        if not self.parent.open_network(self):
            return
        self.close_startup()
        
            
    def close_startup(self):
        self.parent.show()
        self.close()