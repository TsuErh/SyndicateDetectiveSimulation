#!/usr/bin/env python
# coding: utf-8

# # Battle the Crymland

# #### Tsu Erh Lin
# ###### Mar 15 2021

# In[1]:


from random import randrange
from random import sample
from random import random
from collections import Counter
import os


# In[2]:


# Read parameters from file

file = open('Parameter.txt','r')

weeks = int((file.readline().split())[2])
n_thieves = int((file.readline().split())[2])
heist_coef = int((file.readline().split())[2])
promotion_wealth = int((file.readline().split())[2])
n_detetectives = int((file.readline().split())[2])
solve_init = float((file.readline().split())[2])
solve_cap = float((file.readline().split())[2])
discover_init = float(((file.readline().split()))[2])
seizes = float(((file.readline().split()))[2])

file.close()


# In[3]:


# Assign several variables

AllThieves = dict()
AllLieus = dict()
ArrestThie = []
ArrestLieus = []
Detective_sei = {1: 0, 2: 0, 3: 0}
WeeklyHeists = []

# Create a weekly report file
file = open('Weekly Report', 'w')
file.close()


# In[4]:


def Collect(week, BribedDet, BiggWealth):
    'A collecter that can write weekly report into a file'
    
    file = open('Weekly Report', 'a')                                  # Open a file which can append text into the file
    weekinfo = ('Week: ' + str(week))                                  # The information of the week
    NumberThie = ('Number of thieves: ' + str(len(AllThieves)))        # The number of the thieves
    NumberLieu = ('Number of lieutenants: ' + str(len(AllThieves)))    # The number of the lieutenants
    ThieJail = ('Number of thieves in jail: ' + str(len(ArrestThie)))  # Number of thieves in jail
    LieuJail = ('Number of lieutenants: ' + str(len(ArrestLieus)))     # Number of lieutenants in jail
    Bigg = ("Mr. Bigg's personal wealth: " + str(BiggWealth))          # Mr.Bigg's wealth
    BribedDet = ("Number of bribed detectives: " + str(BribedDet))     # Number of detectives that has been bribed
    
                                                                       # Write thoes information into file
    file.write(weekinfo + os.linesep)                                  
    file.write(NumberThie + os.linesep)
    file.write(NumberLieu + os.linesep)
    file.write(ThieJail + os.linesep)
    file.write(LieuJail + os.linesep)
    file.write(Bigg + os.linesep)
    file.write(BribedDet + os.linesep)
    file.close()                                                       # Close file
    


# In[5]:


def Syndicate():
    'Main function of Battle of Crymland'
    
    BiggCaught = False                                     # Initiate Mr.Bigg hasn't been caught
    Bigg = Lieutenant(0, 0, 0)                             # Let Mr.Bigg as lieutenant
    Bigg.NewThieves()                                      # Mr.Bigg create a new group of thieves
    Bigg.NewLieu()                                         # Add Mr.Bigg into the Lieutenant's dictionary
    
    BiggWealth = 0                                         # Assign Bigg's Wealth as 0 at first
    LieuID = 0                                             # Let the ID of Lieutenant starts from 0
    week = 1                                               # Let the week starts from 1
    BribedDet = 0                                          # Assign the number of bribed detectives as 0
    
    while (week < weeks) & (BiggCaught == False):          # Run 500 weeks and if Bigg didn't get cought, the loop won't break
        
        WeeklyHeists = []                                  # Assign a list to collect weekly heists
        
        for i in list(AllThieves.keys()):                  # For every thief
            if AllThieves[i] > promotion_wealth:           # If the thief's wealth is bigger than the given promotion wealth
                LieuID += 1                                # Add 1 lieutenant
                Li = Lieutenant(LieuID, AllThieves[i], 0)  # Let it become a lieutenant
                Li.NewThieves()                            # Build it's own thieves group
                Li.NewLieu()                               # Add into the Lieutenant's dictionary
                del AllThieves[i]                          # Delete the thief from the Thieves' dictionary

            else:                                          # If the thief's wealth hasn't reach the promotion wealth
                BiggWeekly = heist()                       # Commit a heist
                WeeklyHeists.append(i)                     # Add a heist into list
                
        
        for i in list(Detective_sei.keys()):               # For every detectives in the dictionary (which was assigned as 3)
            if len(WeeklyHeists) > 1:                      # If there's more than 1 heists in the weekly heists
                Case = sample(WeeklyHeists, 1)             # Randomly select a heist
                WeeklyHeists.remove(Case[0])               # Remove the selected heist from the weekly heists
                det = Detective(solve_init, solve_cap, discover_init, BiggWeekly)   # Let the detective investigate
                det.Experience()                           # Increase the detective's experience
                if det.SolveCase():                        # If the case has been solved
                    ArrestThie.append(Case[0])             # The thief will be arrested and add into the ArresThie list
                    Detective_sei[i] += AllThieves[Case[0]]# Seizes the wealth
                    del AllThieves[Case[0]]                # Delete the thief from the Thieves dictioanry
                else:
                    continue                               # If the case hasn't been solved then continue

                if (Testify(i)) and (Detective_sei[i] > seizes):   # If Testify return true, and the wealth has been seized are over 1000000
                    if det.Bribe():                                # If the detective has been bribed
                        BribedDet += 1                             # Add 1 to BribedDet
                        BiggCaught = False                         # BiggCaught stay False
                        if det.Discover():                         # If the bribed detective been discovered
                            Detective_sei[i+1] = Detective_sei[i]  # Replace its position with new detective
                            del Detective_sei[i]                   # Delete the bribed detective from dictionary
                        else:
                            continue
                    else:                                          # If the detective didn't get bribe
                        BiggCaught = True                          # BiggCaught turn True, loop break
                        print("Mr. Bigg got caught! ")
            else:
                continue
            
            
            BiggWealth += BiggWeekly                               # Let BiggWealth add the wealth weekly
            Collect(week, BribedDet, BiggWealth)                   # Use Collect function create weekly review
            week += 1


# In[6]:


def Testify(Det):
    'Represent the Testification'
    
    Lieu = []                                  # Assign an empty list to Lieu
    for i in ArrestThie:                       # For each thief in ArrestThie
        Lieu.append(i[0])                      # Append its supervisor into the Lieu list
    c = Counter(Lieu)                          # Count the how many thieves are from the same supersivor
    for i in c:                  
        while c[i] >= 3:                       # If there are more than 3 thieves are from the same group
            ArrestLieus.append(i)              # The thieves will testify againt the lieutenant, append the lieutenant to ArrestLieus
            Detective_sei[Det] += AllLieus[i]  # Seize the wealth
            return True                        # Reutrn True


# In[7]:


class Detective():
    'A class that represent a detective'
    
    def __init__(self, solve_init, solve_cap, discover_init, BiggWeekly):
        self.Solve_init = solve_init
        self.Solve_cap = solve_cap
        self.Solved = 0
        self.DetID = 1
        self.Bribed = False
        self.BiggWeekly = BiggWeekly
        self.DisInit = discover_init
        self.SeWealth = 0
    
    def Experience(self):
        "Return the experience"
        self.Solved = self.Solve_init + DetExp()   # Use the helper function DetExp() to add the exeprience
        if self.Solved < self.Solve_cap:           # If the possibility to solve case are smaller than Solve_cap than return self.Solved
            return self.Solved
        return self.Solve_cap                      # If the possibility to solve the case are bigger than Solve_cap, return Solve_cap
    

    def SolveCase(self):
        "Return if the detective solved tha case"
        SolveProb = random()                                    # For each case, the porbability that the case to be sovled
        if self.Bribed == False and SolveProb <= self.Solved:   # If its smaller than the experience, return True (Case been solved)
            return True
        return False
    
    def Bribe(self):
        "Return if the detective has been bribed"
        BribProb = random()                                                  # Create a probability the detective be bribed
        if (self.BiggWeekly/10 < 10000) and (BribProb > 0.05):               # If the bribe < 10000, and the BribProb is bigger than 0.05, return True(been bribed)
            return True
        elif (10000< self.BiggWeekly/10 < 100000) and (BribProb > 0.1):      # If the bribe < 100000, and the BribProb is bigger than 0.1, return True(been bribed)
            return True
        elif (100000 < self.BiggWeekly/10 < 1000000) and (BribProb > 0.25):  # If the bribe < 1000000, and the BribProb is bigger than 0.25, return True(been bribed)
            return True
        elif (self.BiggWeekly/10 > 1000000) and (BribProb > 0.5):            # If the bribe > 1000000, and the BribProb is bigger than 0.5, return True(been bribed)
            return True
        return False                                                         # Or return Fasle(not be bribed)
    
    def Discover(self):
        "Return if the bribed detective will be discover"
        self.DisProb = self.DisInit + DiscoverPro()                          # Add the possibability of the bribed detective to be disvoered each week
        self.Discovered = random()                                           # Create the possibility of the bribed detective to be discovered
        if self.DisProb > self.Discovered:                                   # If bigger than the possibability, return True(Been discovered)
            return True


# In[8]:


def heist():
    'Represent a heist'
    
    BiggWeekly = 0                        # Assign 0 to Mr.Bigg's weekly wealth
    for i in AllThieves:                  # For every thief
        value = HeistValue()              # Use helper function HeistValue to calculate the value of heist
        wealth = value/2                  # Calculate the value the thief earned each heist
        AllThieves[i] += wealth           # Add value to its wealth
        if i[0] == 0:                     # If the thief's supervisor is Mr.Bigg
            BiggWeekly += wealth          # Mr.Bigg earned same value
        elif i[0] in AllLieus.keys():     # If the thief's supervisor isn't Mr.Bigg
            AllLieus[i[0]] += wealth/2    # It's supervior earns half of value
            BiggWeekly += wealth/2        # Mr.Bigg earns half of the value 
    return BiggWeekly


# In[9]:


class Thief():
    'A class that represent the thief'
    
    def __init__(self, LieuID):
        self.LieuID = LieuID
        self.ThieID = 0
        
    def NewThie(self):
        "Add new thief"
        self.ThieID += 1
        return self.ThieID


# In[10]:


class Lieutenant(Thief):
    'A class that represent the lieutenant'
    
    def __init__(self, LieuID, Wealth, ThieID):
        self.LieuID = LieuID                     # Initialize the ID of lieutenant by given LieuID
        self.ThieID = ThieID                     # Initialize the ID if thief by given ThieID
        self.LieWealth = Wealth                  # Initialize the lieutenant's wealth by given wealth
        
    def NewThieves(self):
        "Build new group of thieves"
        for i in range(n_thieves):               # Create the group of thieves by the given number
            AllThieves[self.LieuID, i] = 0
        return AllThieves
    
    def NewLieu(self):
        "Add new Lieutenant"
        AllLieus[self.LieuID] = self.LieWealth   # Add new lieutanent to the dictionary
        return AllLieus
    


# In[11]:


def HeistValue():
    'Return the value of each hiest'
    
    d = dice(20)         # Use helper function dice
    v = heist_coef * d   # Create the value of heist
    return v


# In[12]:


def DetExp():
    "Return the experience of solving the case"
    
    d = dice(10)         # Use helper function dice
    ex = d/100           # Calculate the experience
    return ex


# In[13]:


def DiscoverPro():
    "Return the probability if the detective is discovered"
    
    d = dice(20)         # Use helper function dice
    dis = d/100          # Calculate the probability of discover
    return dis


# In[14]:


def dice(n):
    'Return the value of dice'
    
    num = randrange(n)
    return num


# In[15]:


Syndicate()


# In[ ]:





# In[ ]:




