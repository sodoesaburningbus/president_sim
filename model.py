### This module contains the class that handles the simulations
### of the Presidential Election
### Christopher Phillips

### Import required variables
import numpy as np
import numpy.random as nr

### Simulator Class
class simulator():
    
    # Object creation function
    def __init__(self, input_file='input.csv', nameR='Republican', nameD='Democrat'):

        # Attach variables for later use
        self.nameR = nameR
        self.nameD = nameD

        # Load the data into a dictionary
        self.inputs = {'states': [], 'probs': [], 'votes': []}
        fn = open(input_file)
        for line in fn:
            dummy = line.split(',')
            self.inputs['states'].append(dummy[0])
            self.inputs['probs'].append(dummy[1])
            self.inputs['votes'].append(dummy[2])
        fn.close()

        # Array things
        self.inputs['probs'] = np.array(self.inputs['probs'], dtype='float')
        self.inputs['votes'] = np.array(self.inputs['votes'], dtype='int')

        return
    
    # Function to run the simulation
    def run_sim(self, runs=10000):

        # Create dictionary to hold the runs
        self.data = {'#Runs': runs, 'President': [], 'CountR': [], 'CountD': [], 'Map': []}

        # Run the simulations
        rng = nr.default_rng()
        for i in range(runs):

            # Perform the sim
            results = rng.random(size=len(self.inputs['states']))
            winners = []
            mask = (results < self.inputs['probs'])
            for m in mask:
                if m:
                    winners.append(self.nameR)
                else:
                    winners.append(self.nameD)

            countR = np.sum(self.inputs['votes'][mask])
            countD = np.sum(self.inputs['votes'][~mask])
            if (countR >= 270):
                president = self.nameR
            elif (countD >= 270):
                president = self.nameD
            else:
                president = 'tie'

            # Create dictionary with the state-by-state results
            resultMap = {}
            for state, winner in zip(self.inputs['states'], winners):
                resultMap[state] = winner

            # Store the outputs
            self.data['President'].append(president)
            self.data['CountR'].append(countR)
            self.data['CountD'].append(countD)
            self.data['Map'].append(resultMap)

        # Get the overall winner
        finalR = np.sum(np.array(self.data['President']) == self.nameR)
        finalD = np.sum(np.array(self.data['President']) == self.nameD)
        if (finalR > finalD):
            self.data['Overall'] = self.nameR
        elif (finalR < finalD):
            self.data['Overall'] = self.nameD
        else:
            self.data['Overall'] = 'tie'

        return
