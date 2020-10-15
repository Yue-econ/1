import math
import random

from django.db import models


from decimal import *

from otree.api import (
    models, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range, widgets)

from otree_tools.models.fields import MultipleChoiceModelField


class Constants (BaseConstants):
    name_in_url = 'project_OT1_25'
    players_per_group = None
    players_per_round = 25
    patients_per_round = 24
    num_rounds = 6
    instructions_template = 'project_OT1_25/instruction.html'
    endowment_patient = 653
    painThreshold_increment = 0.01
    painThreshold_choices = [x/100 for x in range(0, 400)]
    per_visit_fee = c(103)
    price = c(15)
    price2 = c(550)
    weight_factor_health = 1.1
    id_in_group = (1, 2, 3, 4, 5, 6, 7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25)
    id_in_group_patient = (1, 2, 3, 4, 5, 6, 7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24)
    showupfee = 10
    segement1 = 0.94
    segement2 = 1.4
    segement3 = 1.7
    segement4 = 2.5


class Subsession (BaseSubsession):
    def creating_session(self):
        self.group_randomly ()
        if self.round_number == 1:
            paying_round = random.randint(5, Constants.num_rounds)
            self.session.vars['paying_round'] = paying_round
            self.session.vars['lossaversionchosen'] = random.randint (1, 6)

        for p in self.get_players():
            p.lossaversionchosen = self.session.vars['lossaversionchosen']


class Group (BaseGroup):
    threshold_sick_level = models.StringField (
        choices=['sick', 'sick*', 'sick**', 'sick***','more severe than sick***'])
    decision_threshold_sick_level = models.StringField (
        choices=['sick', 'sick*', 'sick**', 'sick***', 'more severe than sick***'])
 #   painThreshold = models.FloatField(min=0.00, max=4.00)

    visit_or_not = models.BooleanField ()
    # prescribed = models.BooleanField()
    total_visit_fee = models.CurrencyField ()
    thresholdExceedCount = models.IntegerField ()
    thresholdExceedCount2 = models.IntegerField ()
    visit_count = models.IntegerField ()

    total_health_patients = models.FloatField ()
    total_payoff_physician = models.FloatField ()
    id_in_group = Constants.id_in_group
    # pain_eligible = models.FloatField(min=painThreshold, max=400)
    id_visit = models.IntegerField ()

    def painThreshold(self):
        if self.decision_threshold_sick_level == 'sick':
            return float(0.9)
        elif self.decision_threshold_sick_level == 'sick*':
            return 1.39
        elif self.decision_threshold_sick_level == 'sick**':
            return 1.69
        elif self.decision_threshold_sick_level == 'sick***':
            return 2.49
        elif self.decision_threshold_sick_level == 'more severe than sick***':
            return 3

    def set_payoffs(self):
        players = self.get_players ()
        physician = self.get_player_by_role ('physician')
  #      patient = self.get_player_by_role ('patient {}')
        patient1 = self.get_player_by_role ('patient 1')
        patient2 = self.get_player_by_role ('patient 2')
        patient3 = self.get_player_by_role ('patient 3')
        patient4 = self.get_player_by_role ('patient 4')

#        health_impact = 684.72 * math.log1p (0.66 * self.player.pain() + 0.012 - 1)
#        prescribedPatients = [p for p in players if self.p.pain >= self.group.painThreshold]
        print (patient1.decision)
        print (patient2.decision)
        print (patient3.decision)
        print (patient4.decision)

        if patient1.decision:
            if patient1.pain() >= self.painThreshold():
                patient1.is_prescribed = True
            else:
                patient1.is_prescribed = False
        else:
            patient1.is_prescribed = False

        if patient2.decision:
            if patient2.pain() >= self.painThreshold():
                patient2.is_prescribed = True
            else:
                patient2.is_prescribed = False
        else:
            patient2.is_prescribed = False

        if patient3.decision:
            if patient3.pain() >= self.painThreshold():
                patient3.is_prescribed = True
            else:
                patient3.is_prescribed = False
        else:
            patient3.is_prescribed = False

        if patient4.decision:
            if patient4.pain() >= self.painThreshold():
                patient4.is_prescribed = True
            else:
                patient4.is_prescribed = False

    def painThreshold_history(self):
        return [g.painThreshold for g in self.in_previous_rounds ()]

    def visit_id(self):
        if self.get_player_by_role == {'physician'}:
            if self.group.visit_or_not:
                return {self.player.id_in_group}


class Player (BasePlayer):
    sick = models.StringField (choices=['sick***', 'sick**', 'sick*', 'sick'])
    enjoy = models.StringField (choices=['enjoy***', 'enjoy**', 'enjoy*', 'enjoy'])
    health_patient = models.FloatField()
#    pain = models.FloatField()

    #   pain = models.FloatField(min=0, max=400, choices=[x/100 for x in range(0, 400)])
    # id = models.StringField
    #    thresholdDecision_physician = models.FloatField(min=0.00, max=4.00)
    thresholdExceed = models.IntegerField ()
    #     doc="Likert Scale: how likely do you think you can get the prescription (0-7))"
    # )
    # total_health_impact = models.FloatField()
    # result_physician = models.CurrencyField()
    # result_patient = models.CurrencyField()
    is_prescribed = models.BooleanField (
        doc="if threshold amount is exceeded (direct response method)"
    )
    decision = models.BooleanField (initial=False)  # patient's decision: visit or not
    lossaversionchosen = models.IntegerField()

    LTchoice1 = models.StringField(
        choices=['Accept', 'Reject'],
        label='Lottery 1: if the coin turns up head, then you loss $1; if the coin turns up tails, you win $3.',
        widget=widgets.RadioSelectHorizontal)

    LTchoice2 = models.StringField(
        choices=['Accept', 'Reject'],
        label='Lottery 2: if the coin turns up head, then you loss $1.5; if the coin turns up tails, you win $3.',
        widget=widgets.RadioSelectHorizontal)

    LTchoice3 = models.StringField(
        choices=['Accept', 'Reject'],
        label='Lottery 3: if the coin turns up head, then you loss $2; if the coin turns up tails, you win $3.',
        widget=widgets.RadioSelectHorizontal)

    LTchoice4 = models.StringField(
        choices=['Accept', 'Reject'],
        label='Lottery 4: if the coin turns up head, then you loss $2.5; if the coin turns up tails, you win $3.',
        widget=widgets.RadioSelectHorizontal)

    LTchoice5 = models.StringField(
        choices=['Accept', 'Reject'],
        label='Lottery 5: if the coin turns up head, then you loss $3; if the coin turns up tails, you win $3.',
        widget=widgets.RadioSelectHorizontal)

    LTchoice6 = models.StringField(
        choices=['Accept', 'Reject'],
        label='Lottery 6: if the coin turns up head, then you loss $3.5; if the coin turns up tails, you win $3.',
        widget=widgets.RadioSelectHorizontal)

    age = models.IntegerField (label='1. What is your age (in years)?', min=18, max=125)

    gender = models.StringField (
        choices=['Male', 'Female', 'Other'],
        label='2. What is your gender?',
        widget=widgets.RadioSelect)

    marriage = models.StringField (
        choices=['Single, Never Married', 'Married, Civil Union, Domestic Partner', 'Separated', 'Divorced', 'Widowed'],
        label='3. What is your marital status?',
        widget=widgets.RadioSelect)

    student = models.StringField (
        choices=['Full-time Student', 'Part-time Student', 'Not a Student'],
        label='4. Are you a full time or part time student?',
        widget=widgets.RadioSelect)

    year = models.StringField (
        choices=['Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate Student', 'Not a Student'],
        label='5. What is your current student classification?',
        widget=widgets.RadioSelect)

    home_country = models.StringField (
        choices=['United States', 'Another Country'],
        label='6. Where were you born?',
        widget=widgets.RadioSelect)

    language = models.StringField (
        choices=['Yes', 'No'],
        label='7. Do you speak a language other than English at home?',
        widget=widgets.RadioSelect)

    employment = models.StringField (
        choices=['Not Working', 'Temporary Job', 'Permanent Job less than 30 hours per week',
                 'Permanent Job more than 30 hours per week'],
        label='8. What is your employment status?',
        widget=widgets.RadioSelect)

    income = models.StringField (
        choices=['Less than $14,000', '$14,000 - $27,999', '$28,000 - $43,999', '$44,000 - $65,999',
                 '$66,000 - $89,999',
                 '$90,000 or above', 'Not Applicable'],
        label='9. What is your own yearly income?',
        widget=widgets.RadioSelect)

    experiment_experience = models.StringField (
        choices=['Yes', 'No', 'Do not remember'],
        label='10. Have you ever participated in any similar trading experiment before?',
        widget=widgets.RadioSelect)

    ethnicity = MultipleChoiceModelField (
        choices=['American Indian or Native Alaskan', 'Black or African American',
                 'East Asian (Chinese, Japanese, Korean, etc.)',
                 'Hispanic or Latino', 'Middle Eastern', 'Pacific Islander or Hawaiian',
                 'South Asian (India, Pakistan, Bangladesh, etc.)', 'White', 'Other'],
        label='11. What is your ethnicity? Please check ALL categories that apply')
    decision01 = models.TextField (initial=None, verbose_name="How you made your decisions in Part 1? "
                                                              "Please describe your decision making process as a physician and a patient if you have played both roles in the past 30 rounds. ")
    comments = models.TextField (blank=True, initial=None,
                                 verbose_name="Do you have any comment, questions, or complains about today's experiment?")

    def physician_player(self):
        return self.get_others_in_group ()[25]

    def get_visitor(self):
        if self.player.role == {'physician'}:
            return self.group.visit_or_not.get_others_in_group ()

    def role(self):
        if self.id_in_group == 25:
            return 'physician'
        if self.id_in_group in (1, 2,3,4,5,6,7,8):
            return 'patient 1'
        if self.id_in_group in (9,10,11,12):
            return 'patient 2'
        if self.id_in_group in (13,14,15,16):
            return 'patient 3'
        else:
            return 'patient 4'


    def action(self):
        if self.decision == True:
            return 'visit'
        else:
            return 'not visit'

    def pain(self):
        if self.id_in_group in (1, 2,3,4,5,6,7,8):
            return 0.94
        if self.id_in_group in (9,10,11,12):
            return 1.40
        if self.id_in_group in (13,14,15,16):
            return 1.70
        if self.id_in_group in (17,18,19,20,21,22,23,24):
            return 2.50
        else:
            return 0

    def sick1(self):
        if self.id_in_group in (1,2,3,4,5,6,7,8):
            return 'sick'
        if self.id_in_group in (9,10,11,12):
            return 'sick*'
        if self.id_in_group in (13,14,15,16):
            return 'sick**'
        if self.id_in_group in (17,18,19,20,21,22,23,24):
            return 'sick***'
        else:
            return 0

    def taste(self):
        if self.id_in_group in (1, 2,3,4,5,6,7,8):
            return 1000
        elif self.id_in_group in (9,10,11,12):
            return 165

        elif self.id_in_group in (13,14,15,16):
            return 50

        elif self.id_in_group in (17,18,19,20,21,22,23,24):
            return 250
        else:
            return 'None'

    def taste1(self):
        if self.id_in_group in (1, 2,3,4,5,6,7,8):
            return 'enjoy***'
        if self.id_in_group in (9,10,11,12):
            return 'enjoy*'
        if self.id_in_group in (13,14,15,16):
            return 'enjoy'
        if self.id_in_group in (17,18,19,20,21,22,23,24):
            return 'enjoy**'
        else:
            return 0

    @property
    def patient(self):
        pain = models.FloatField ()
        taste = models.FloatField ()
        id_pain_dic = {self.id_in_group: pain}
        id_taste_dic = {self.id_in_group: taste}

        if self.id_in_group in [1, 2,3,4,5,6,7,8]:
            id_pain_dic[self.id_in_group] = 0.94
            id_taste_dic[self.id_in_group] = 1000
            print ("I am patient self.id_in_group, my pain level k = 0.94, and my taste for opioid is 1000")
            return 'patient with pain level 0.94', 'patient with taste level 1000'
        if self.id_in_group in [9,10,11,12]:
            id_pain_dic[self.id_in_group] = 1.4
            id_taste_dic[self.id_in_group] = 165
            print ("I am patient self.id_in_group, my pain level k = 1.4, and my taste for opioid is 165")
            return 'patient with pain level 1.4', 'patient with taste level 165'
        if self.id_in_group in [13,14,15,16]:
            id_pain_dic[self.id_in_group] = 1.7
            id_taste_dic[self.id_in_group] = 50
            print ("I am patient self.id_in_group, my pain level k = 1.7, and my taste for opioid is 50")
            return 'patient with pain level 1.7', 'patient with taste level 50'
        if self.id_in_group in [17,18,19,20,21,22,23,24]:
            id_pain_dic[self.id_in_group] = 2.5
            id_taste_dic[self.id_in_group] = 50
            print ("I am patient self.id_in_group, my pain level k = 2.5, and my taste for opioid is 250")
            return 'patient with pain level 2.5', 'patient with taste level 250'

    def pain_threshold(self):
        if self.id_in_group == 25:
            print ("You are a physician with 24 patients and your patient pain level is " +
                   str (Constants.id_pain_dic[self.id_in_group_patient]))
            # return float(input('given the pain level of your patients, enter a threshold pain level:'))

    def result_patient(self):
        if self.id_in_group in (1,2,3,4,5,6,7,8):
            if self.decision:  #visit
                if self.is_prescribed == False:
                    return round(653 - 103,2)
                else: # get the prescription from the physician
                    return round(653 + 1000 - 15 - 103 - 314,2)
            else:
                return round(653,2)

        if self.id_in_group in (9,10,11,12):
            if self.decision:
                if self.is_prescribed == False:
                    return round (653 - 103, 2)
                else:   # get it from the physician, consume
                    return round(653 + 165 - 45 - 15 - 103,2)
            else:
                return round(653,2)

        if self.id_in_group in (13,14,15,16):
            if self.decision:
                if self.is_prescribed == False:
                    return round (653 - 103, 2)
                else:  # get the prescription from the physician

                    return round(653 + 86 + 50 - 15 - 103,2)
            else:
                return round(653,2)

        if self.id_in_group in (17,18,19,20,21,22,23,24):
            if self.decision:
                if self.is_prescribed == False:
                    return round(653 - 103,2)
                else:  # get the prescription from the physician
                    return round(653 + 348 + 250 - 15 - 103,2)
            else:
                return 653

    def result_patient2(self):
        if self.id_in_group in (1, 2, 3, 4, 5, 6, 7, 8):
            if self.decision:  # visit
                if self.is_prescribed == False:
                    return round ((653 - 103)/100, 2)
                else:  # get the prescription from the physician
                    return round ((653 + 1000 - 15 - 103 - 314)/100, 2)
            else:
                return round ((653/100), 2)

        if self.id_in_group in (9, 10, 11, 12):
            if self.decision:
                if self.is_prescribed == False:
                    return round ((653 - 103)/100, 2)
                else:  # get it from the physician, consume
                    return round ((653 + 165 - 45 - 15 - 103)/100, 2)
            else:
                return round ((653/100), 2)

        if self.id_in_group in (13, 14, 15, 16):
            if self.decision:
                if self.is_prescribed == False:
                    return round ((653 - 103)/100, 2)
                else:  # get the prescription from the physician

                    return round ((653 + 86 + 50 - 15 - 103)/100, 2)
            else:
                return round ((653/100), 2)

        if self.id_in_group in (17, 18, 19, 20, 21, 22, 23, 24):
            if self.decision:
                if self.is_prescribed == False:
                    return round ((653 - 103)/100, 2)
                else:  # get the prescription from the physician
                    return round ((653 + 348 + 250 - 15 - 103)/100, 2)
            else:
                return round((653/100),2)



    def result_physician(self):
        if self.group.painThreshold() <= 0.94:
            return self.group.total_health_patients + Constants.per_visit_fee * self.group.thresholdExceedCount2

        elif self.group.painThreshold() <= 1.40:
            return self.group.total_health_patients + Constants.per_visit_fee * self.group.thresholdExceedCount2

        elif self.group.painThreshold() <= 1.70:
            return self.group.total_health_patients + Constants.per_visit_fee * self.group.thresholdExceedCount2
        elif self.group.painThreshold() <= 2.50:
            return self.group.total_health_patients + Constants.per_visit_fee * self.group.thresholdExceedCount2

        else:
            return c(0)

    def result_physician2(self):

        if self.group.painThreshold() <= 0.94:
            return round((self.group.total_health_patients + Constants.per_visit_fee * self.group.thresholdExceedCount2) / 100, 1)

        elif self.group.painThreshold() <= 1.40:
            return round ((self.group.total_health_patients + Constants.per_visit_fee * self.group.thresholdExceedCount2) / 100,
                          1)

        elif self.group.painThreshold() <= 1.70:
            return round ((self.group.total_health_patients + Constants.per_visit_fee * self.group.thresholdExceedCount2) / 100,1)
        elif self.group.painThreshold() <= 2.50:
            return round ((self.group.total_health_patients + Constants.per_visit_fee * self.group.thresholdExceedCount2) / 100, 1)

        else:
            return round (c (0) / 100, 1)


def health_function(k_i):
    return 684.72 * math.log1p (0.66 * k_i + 0.012 - 1)


def sum(health_impact):
    z = 0
    for k_i in models.group.pain_eligible:
        z = z + 684.72 * math.log1p (0.66 * k_i + 0.012 - 1)
        return z



