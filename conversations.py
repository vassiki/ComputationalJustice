import numpy as np
import os
import pandas as pd
from collections import OrderedDict
import people

# change conv_agents to conv_agent_indices to make life easier
# need to set is_sexist_convo, anti_f_sexism, anti_m_sexism
# to zero every time a new conversation starts

# what needs to be refreshed each time we start a new convo?
# 1. who is in the group
# 2. is the conversation sexist
# 3. against whom is it sexist
class Group():

    """ Create a group of agents for one conversation """

    def __init__(self,num_agents, percent_self,
                    max_sexist_allies, anti_f_sexism=0,
                    anti_m_sexism=0,is_sexist_convo=0):
        self.percent_object_self = percent_self
        self.max_sexist_allies = max_sexist_allies
        sex_proportion = [0.2, 0.8]
        sex_index = [0,1]
        agent_sex = np.random.choice(sex_index,replace=True,
                                        size=num_agents,
                                        p=sex_proportion)
        keys = ["person{0}".format(i) for i in range(num_agents)]
        self.agent_name = keys
        self.agents = OrderedDict({keys[i] :
                            people.InitializePeople(agent_sex[i])
                            for i in range(num_agents)})
        self.anti_f_sexism = anti_f_sexism
        self.anti_m_sexism = anti_m_sexism
        self.is_sexist_convo = is_sexist_convo

    def make_sexist(self):

        """ Give all agents a starting sexism value """

        {self.agents[i].init_sexism() for i in self.agent_name}

    def choose_people(self,conversation_size=8):

        """ Choose agents for the conversation_size

        Parameters
        ----------
        conversation_size : number of agents in the
                            conversation

        Returns
        -------
        agents : unique people in this conversation

        """
        self.conversation_size = conversation_size
        keys = self.agent_name
        agent_keys = np.random.choice(keys,conversation_size,
                                    False)

        self.conv_agent_indices = [k for k in agent_keys]

    def get_sex_distribution(self):
        """ Helper function to check # of females in convo"""
        count = 0
        female_tally = [count+1 for k in self.conv_agent_indices
                                if 0 == self.agents[k].sex]
        females = sum(female_tally)
        males = len(self.conv_agent_indices)-females

        return (females,males)

    def get_sex_indices(self):
        """ Helper function to get indices of females in convo """
        females = [k for k in self.conv_agent_indices
                        if 0 == self.agents[k].sex]
        males = [k_remain for k_remain in self.conv_agent_indices
                        if k_remain not in females]

        (f,m) = self.get_sex_distribution()

        assert len(females) == f

        return (females,males)

    def sexism_against(self):
        """ Check if sexism is possible againts men or women """
        (females,males) = self.get_sex_distribution()

        if females == males:
            (f_idx,m_idx) = self.get_sex_indices()
            f_sexism = [self.agents[f].sexism for f in f_idx]
            m_sexism = [self.agents[m].sexism for m in m_idx]
            if sum(f_sexism) > sum(m_sexism):
                self.anti_m_sexism = 1
            elif sum(f_sexism) < sum(m_sexism):
                self.anti_f_sexism = 1
        elif females < males:
            self.anti_f_sexism = 1
        else:
            self.anti_m_sexism = 1

    def check_sexism_convo(self):
        """ Decide if convo was sexist or not, given the sexism of
            agents in convo """
        coin_flips = [np.random.uniform(0) for i in
                        range(self.conversation_size)]
        sexism_level = [self.agents[k].sexism
                            for k in self.conv_agent_indices]
        assert len(coin_flips) == len(sexism_level)

        sexist_remarks = [coin_flips[i] <= sexism_level[i]
                            for i in range(len(coin_flips))]

        if 1 in sexist_remarks:
            self.is_sexist_convo = 1

    #def spread_sexism_effects(self):

        # if conversation is sexist against women,
        # we make all the men increase and









    def objectors_and_allies(self,percent_self=70,
                                max_sexist_allies=70):

        # this is wrong. 70% of ALL women in the group need
        # to object for self, and they do it with prob 0.2 in
        # a convo
        # function to make some people object for self, some object
        # for other
        prob_obj_self = [0.8,0.2]
        prob_obj_other = [0.9,0.1]

        (f_idx,m_idx) = self.get_sex_indices()
        # if sexism is against women, self is women
        if self.anti_f_sexism:
            # randomly select some people who
            # object for self
            self_indices = f_idx
            other_indices = m_idx

            num_obj_agents_to_chose = percent_self*0.01*len(f_idx)
            # these women object for women
            objector_indices = np.random.choice(
                                f_idx, num_obj_agents_to_chose,
                                False)














        # percent_self to decide how many people object
        # for self

        # take all people of opposite sex

        # anyone who is less sexist than max_sexist_allies
        # is an ally, who objects with probability prob_obj_other





# function to determine if sexism happened
# whether it was against men or women
# --new computation
# --against sex

# function to determine if objection happened, against
# which sex

# function to spread contagion to relevant group

# workflow

#x = conversation.Group(num_agents,percent_self,max_sexist_allies)
#x.make_sexist()
#x.choose_people(conversation_size)
#x.sexism_against()
#x.check_sexism_convo()
