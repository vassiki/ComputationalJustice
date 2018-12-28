import numpy as np
import os
import pandas as pd
from collections import OrderedDict
import people

class Conversations:
    """ This is the class to generate coversations
    one simulation at a time """

    def make_people(self):
        num_people = 50
        prob_sex = [0.2,0.8]
        sex = [0,1] #0 is female

        sex_distribution = np.random.choice(sex,
                                            num_people,True,
                                            prob_sex)

        agents = OrderedDict()
        agents = {'p{0}'.format(str(i).zfill(2)):
                 people.InitializePeople(sex_distribution[i])
                 for i in range(num_people)}


        # now apply all the functions required to
        # give properties to these people
        objectors = [0,1]
        prob_objectors = [0.8,0.2] #nicole's data

        objector_distribution = np.random.choice(objectors,
                                                 num_people,True,
                                                 prob_objectors)

        allies = [0,1]
        prob_allies = [0.9,0.1] # guessing

        ally_distribution = np.random.choice(allies,
                                             num_people,True,
                                             prob_allies)
        for idx,key in enumerate(agents):
            #initialize sexism
            agents[key].init_sexism()
            # make objectors
            agents[key].make_objector(objector_distribution[idx])
            # make allies
            agents[key].make_ally(ally_distribution[idx])

        return agents


    agents = make_people()

    def __init__(self,size,agents):
        self.convo_size = size
        self.agents_idx_in_convo = np.random.choice(agents.keys(),
                                       size, False)
        self.agents_in_convo = {key: agents[key] for key in
                                                    self.agents_idx_in_convo}

    def thresh_objectors(self,agents,n_objectors):
        # see how many objectors for self we have
        n_agent_obj_now = sum([self.agents_in_convo[i].object_self
                              for i in self.agents_in_convo])
        # see how many would be left when we use threshold
        # from the simulation
        n_agent_obj_update = round(n_objectors * n_agent_obj_now)
        # find who the objectors are
        now_objectors_idx = [i for i in self.agents_idx_in_convo if
                            self.agents_in_convo[i].object_self == True]
        # randomly pick who to get rid of
        who_to_change = np.random.choice(now_objectors_idx,
                                        int(n_agent_obj_now-n_agent_obj_update),
                                        False)

        for k in self.agents_in_convo:
            if k in who_to_change:
                self.agents_in_convo[k].make_objector(False)
