from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
#import seaborn as sns
#import matplotlib.pyplot as plt
#import pandas as pd



class EndExperiment(QWidget):
	def __init__(self, parent = None):
		QWidget.__init__(self, parent )
 
		#self.setFocusPolicy(Qt.StrongFocus)
		layout = QVBoxLayout(self)
		thanks_lab = QLabel()
		thanks_lab.setText("Fin de l'experience. Merci pour votre participation")		
		layout.addWidget(thanks_lab)


		#######################
		# read csv file
		#######################
		#read your csv file and add the header
		#df = pd.read_csv( ... )
		#print(df)
		#



		##################
		# chart
		##################
		#sns.xxx
		#layout.addWidget( xxx )


