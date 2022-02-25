import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Introduction import *
from InterTrial import *
from Canvas import *
from EndExperiment import *
import numpy as np
from time import time

class MainWindow(QMainWindow):

    def __init__(self, parent = None ):
        QMainWindow.__init__(self, parent )
        self.resize(600, 500)
        self.index = 0

        ###############################
        #         MAIN VARIABLES      #
        ###############################
        self.experiment_design_file_name = "./experiment2.csv"
        self.experiment_name = ""
        self.participant_id  =-1
        self.block_id        = 0
        self.trial_id        = 0
        self.condition       = ""
        self.mat_size        = 0

        self.experiment_name_col  = 0
        self.participant_col = 1
        self.trial_col       = 2
        self.block_col       = 3
        self.condition_col   = 4
        self.grid_size_col   = 5

        self.content = "participant_id,trial_id,block_id,condition,size,target,click,time\n"
        self.start = None

        ###############################
        ###############################

        self.introduction = Introduction()
        self.introduction.start_button.clicked.connect(self.start_experiment)

        self.canvas = Canvas(self)
        self.canvas.stopTrial.connect(self.stop_trial)

        self.interTrial = InterTrial(self)
        self.interTrial.startTrial.connect(self.start_trial)

        self.endExperiment = EndExperiment(self)

        self.stack = QStackedWidget()
        self.stack.addWidget(self.introduction)
        self.stack.addWidget(self.interTrial)
        self.stack.addWidget(self.canvas)
        self.stack.addWidget(self.endExperiment)


        self.setCentralWidget(self.stack)

        self.load_experiment_plan()



    def start_experiment(self):
        self.participant_id = self.introduction.participant_id
        print("start epxeriment with participant", self.participant_id)
        found = False
        while not found:
            self.index = self.index+1
            found = self.update_trial_values()
        self.setup_trial()


    def update_trial_values(self):
            same_participant = True
            if self.index >= len(self.plan):     #end of the file
                return False
            trial_str = self.plan[self.index]
            trial_str = trial_str.replace('\r\n', '')
            trial_str = trial_str.replace('\n', '')

            trial = trial_str.split(',')
            # print( trial )
            id = int( trial[ self.participant_col ])

            if id == self.participant_id:
                #self.practice = True if trial[1] == 'true' else False
                self.practice = False
                self.experiment_name = trial[ self.experiment_name_col]
                self.block_id = trial[ self.block_col ]
                self.trial_id = trial[ self.trial_col ]
                self.condition = trial[ self.condition_col ]
                self.mat_size = int(trial[5])
                print(id, self.trial_id, self.mat_size )
                same_participant = True
            else:
                same_participant = False
            return same_participant


    def setup_trial(self):
        list = self.generate_stimulus()
        self.canvas.set_stimulus(list)
        self.canvas.setState(0)
        self.interTrial.set_block_trial(self.block_id, self.trial_id)
        self.interTrial.set_practice(self.practice)
        self.stack.setCurrentWidget(self.interTrial)


    def generate_stimulus(self):
        n = self.mat_size
        list = []
        if self.condition == 'Taille': # TODO
            cond = ['Big','Small']
            distractor =  np.random.choice(cond, 1, p=[0.5,0.5])
            distractor = distractor[0]
            target = cond[1] if distractor == cond[0] else cond[0]
            self.pos_target = np.random.randint(n)
            for i in range(0,n):
                list.append(distractor)
            list[self.pos_target] = target

        elif self.condition == 'Courbure': # TODO
            cond = ['Concavity_Big','Convexity_Big']
            distractor =  np.random.choice(cond, 1, p=[0.5,0.5])
            distractor = distractor[0]
            target = cond[1] if distractor == cond[0] else cond[0]
            self.pos_target = np.random.randint(n)
            for i in range(0,n):
                list.append(distractor)
            list[self.pos_target] = target

        elif self.condition == 'CourbureTaille': # TODO
            cond = ['Concavity_Big', 'Concavity_Small', 'Convexity_Big', 'Convexity_Small']
            target =  np.random.choice(cond, 1, p=[0.25,0.25, 0.25, 0.25])
            target = target[0]
            self.pos_target = np.random.randint(n)
            cond.remove(target)
            valid_trial = False
            while not valid_trial:
                list  = []
                for i in range(0,n):
                    distractor = np.random.choice(cond, 1, p=[0.333,0.333, 0.334])
                    list.append(distractor[0])
                    # dict[ distractor[0] ] += 1
                list[self.pos_target] = target
                valid_trial = self.is_valid_trial( list, cond )


        else:
            print(' ======= ERROR =====')
            print('condition is: ', self.condition)
            print('condition should be \'Taille\', \'Courbure\' or \'CourbureTaille\' ' )
            exit( 0 )
        return list


    def is_valid_trial( self, my_list, cond ):
        valid = True
        for elem in cond:
            if np.count_nonzero( np.array(my_list) == elem ) < 2:
                valid = False
            print(elem, "count", np.count_nonzero( np.array(my_list) == elem ) )
        return valid


    def start_trial(self):
        self.stack.setCurrentWidget(self.canvas)
        #print("start_trial -> target: ", self.pos_target)
        self.start = time()

        ####################
        # TODO
        ####################


    def stop_trial(self):
        selected_target = self.canvas.selected_target
        print("target vs. selected target: "+ str(self.pos_target) +  " vs. " + str(selected_target) )
        self.content += str(self.participant_id) + "," + str(self.trial_id) + "," + \
                        str(self.block_id) + "," + str(self.condition) + "," +\
                        str(self.mat_size) + "," + str(self.pos_target) + ","  +\
                        str(selected_target) + "," + str(time()-self.start) + "\n"
        self.start = None

        ####################
        # TODO
        ####################

        self.index = self.index + 1
        if self.update_trial_values():
            self.setup_trial()
        else:
            print("End of the experiment. Thanks")
            self.stack.setCurrentWidget(self.endExperiment)

            ####################
            # TODO
            ####################
            title = "participant_" + str(self.participant_id)
            self.save_user_data(title, self.content)



    ####################
    def keyReleaseEvent(self, e):
        if e.key() == Qt.Key_Space:
            if self.interTrial.isVisible():
                self.start_trial()
            elif self.canvas.isVisible():
                self.canvas.setState(1)


    ##############
    def load_experiment_plan(self):
        file = open(self.experiment_design_file_name, 'r') # TODO
        self.plan = file.readlines()
        file.close()

    ##############
    def save_user_data(self, title, content):
        with open('./logs/'+title + '.csv', 'w') as fileSave:
            fileSave.write(content)
            fileSave.close()

if __name__=="__main__":

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec_()
