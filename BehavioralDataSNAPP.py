import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 


class BehavioralData:
    def __init__(self, trial, stringTrial):
        self.stringTrial = stringTrial
        self.keys = scipy.io.loadmat(trial).keys()
        self.timing = scipy.io.loadmat(trial)['timing']
        self.data = scipy.io.loadmat(trial)['data']
        self.timeIncluded = self.timing['MRI'][0][0].dtype
        self.dataIncluded =  self.data.dtype
        self.transitionTime = self.getExitTime() - self.getScannerStart()
        
        
   # time
        
    def getScannerStart(self):
        return self.timing['MRI'][0][0]['scannerStartTime'][0][0][0][0] 
    
    def getBlockStart(self):
        return self.timing['MRI'][0][0]['blockStartTime'][0][0][0][0]
        
    def getExitTime(self):
        return self.timing['MRI'][0][0]['runFinishedExitTime'][0][0][0][0]
    
    def getTrialOnset(self):
        return self.timing['MRI'][0][0]['trialOnset'][0][0][0]
    
    def getStimOnset(self):
        return self.timing['MRI'][0][0]['stimOnset'][0][0][0]
    
    def getStimDuration(self):
        return np.ones(len(self.getStimOnset())) * 0.5
    
    def getTransitionTime(self):
        return self.transitionTime
    
    def setTransitionTime(self, BehavioralDataClass):
        self.transitionTime = self.getExitTime() - self.getScannerStart() + BehavioralDataClass.getTransitionTime()
    
    def printTimes(self):
        print('%s scanner start time: %f' % (self.stringTrial, self.getScannerStart()))
        print('%s block start time: %f' % (self.stringTrial, self.getBlockStart()))
        print('%s exit time: %f'  % (self.stringTrial, self.getExitTime()))
        print()
    
    # conditions
    
    def getCoherence(self):
        return self.data['coherence'][0][0][0]
    
    def getDotDensity(self):
        return self.data['dotDensity'][0][0][0]
    
    def getStimID(self):
        return self.data['stimID'][0][0][0]
    
    def getSubjectResponse(self):
        return self.data['response'][0][0][0]
    
    def getUserConfidenceRating(self):
        return self.data['rating'][0][0][0]
    
    def getCorrectResponseStatus(self):
        return self.data['correct'][0][0][0]
    

def plot_coh_conf(data):
    plt.rcParams['axes.labelsize'] = 18
    plt.figure(figsize=(15, 5))
    sns.regplot(data[data['dotDensity'] == 1]['coherence'],
            data[data['dotDensity'] == 1]['confidence rating (1,2,3,4)'],
           ci = None)
    sns.regplot(data[data['dotDensity'] == 3]['coherence'],
            data[data['dotDensity'] == 3]['confidence rating (1,2,3,4)'],
           ci = None)
    plt.xlim([0.05, 1.05])
    plt.legend(['dotDensity = 1 dot/ deg^2', 'dotDensity = 3 dot/ deg^2'])
    
    plt.figure(figsize=(15, 5))
    plt.subplot(1, 2, 1)
    sns.regplot(data[data['dotDensity'] == 1]['coherence'],
            data[data['dotDensity'] == 1]['confidence rating (1,2,3,4)'],
           ci = None)
    plt.title('dotDensity = 1 dot/ deg^2', fontsize = 18)
    
    plt.subplot(1, 2, 2)
    sns.regplot(data[data['dotDensity'] == 3]['coherence'],
            data[data['dotDensity'] == 3]['confidence rating (1,2,3,4)'],
           ci = None)
    plt.title('dotDensity = 3 dot/ deg^2', fontsize = 18)
    
    plt.show()
    return