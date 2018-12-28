# might not need these modules at all...
import numpy as np
import os
import pandas as pd
from collections import OrderedDict

# set up a class for people

class InitializePeople:
    """ Make people with attributes needed for conversation"""

    def __init__(self, sex, r_a=0.0,
                    r_b=0.0):
        """
        function to initialize the agent

        Parameters
        ----------
        sex : sex of this agent (0 or 1=male)
        r_a : number of sexist remarks against
        r_b : number of sexist remarks by
        """
        self.sex = sex #no default, sex has to be provided

        self.sexist_remarks_against = r_a
        self.sexist_remarks_by = r_b

    def init_sexism(self):
        """
        function to give agent starting sexism value
        """
        percentage_sexism = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
        prob_sexism = [0.5, 0.1, 0.1, 0.1, 0.1, 0.1]

        self.sexism_init = round(np.random.choice(percentage_sexism,
                                            1, True, prob_sexism),2)
        self.sexism = self.sexism_init

        return self

    def make_objector(self,o_self=True):
        """
        function to decide if agent objects to sexism
        against self

        Parameters
        ----------
        o_self : True or False (default True)
        """
        if o_self:
            self.object_self = True
        else:
            self.object_self = False

    def make_ally(self,o_other=True):
        """
        function to decide if agent objects to sexism
        against other sex

        Parameters
        ----------
        o_other : True or False (default True)
        """
        if o_other:
            self.object_other = True
        else:
            self.object_other = False

    def update_remarks_against(self, remark_made_against=False):
        """
        function to update remarks against

        Parameters
        ----------
        remark_made_against : True or False (default False)
        """
        if remark_made_against:
            self.sexist_remarks_against += 1

    def update_remarks_by(self, remarks_made_by=False):
        """
        function to update remarks made by

        Parameters
        ----------
        remark_made_by : True or False (default False)
        """
        if remarks_made_by:
            self.remarks_made_by += 1

    def update_sexism(self, sexism_increase=0.0):
        """
        function to update sexism

        Parameters
        ----------
        sexism_increase : float amount of sexism increase
        """

        self.sexism += sexism_increase
