from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from math import exp

import sys

# Data_logging
import logging
logger = logging.getLogger(__name__)


class Contestant(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True)
    name = models.CharField(max_length=30)
    score = models.FloatField(default=50.0)
    phone = models.CharField(max_length=15, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def position(self):
        position = Contestant.objects.all().filter(score__gte=self.score).count()
        return position


class Challenge(models.Model):
    start_date = models.DateTimeField('date started')
    expire_date = models.DateTimeField('deadline')
    attacker = models.ForeignKey(Contestant, related_name='attacks')
    defender = models.ForeignKey(Contestant, related_name='defends')

    WIN = 'WIN'
    LOSE = 'LOSE'
    SPECIAL = 'SPECIAL'
    PENDING = 'PEND'
    CANCEL = 'CANCEL'
    RESULT_CHOICES = ((PENDING, 'Pending'),
                      (WIN, 'Success'),
                      (LOSE, 'Fail'),
                      (SPECIAL, 'SPECIAL'),
                      (CANCEL, 'CANCELLED'),)
    result = models.CharField(max_length=10, choices=RESULT_CHOICES, default=PENDING)
    remark = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return str(self.id)

    def is_active(self):
        return timezone.now() < self.expire_date
    is_active.admin_order_field = 'expire_date'
    is_active.boolean = True
    is_active.short_description = 'Still active?'

    def is_handled(self):
        if self.result == self.PENDING:
            return False
        else:
            return True

    is_handled.admin_order_field = 'expire_date'
    is_handled.boolean = True
    is_handled.short_description = 'Handled yet?'

    def set_results(self, in_result):

        # List that stores the final score change  [0]:attacker change [1]:defender change
        final_score_change = [0.0, 0.0]

        try:
            self.result = in_result
        except ValidationError as err:
            print("Invalid result type: " + str(err))

        if in_result == Challenge.WIN or in_result == Challenge.LOSE:
                # Starts to calculate score
                try:
                    # Check if is Strong attack Weak
                    SvW = False
                    if self.attacker.score > self.defender.score:
                        SvW = True
                    elif self.attacker.score <= self.defender.score:
                        SvW = False

                    # Result 1: Attacker wins
                    if in_result == Challenge.WIN:
                        diff = abs(self.attacker.score - self.defender.score)
                        ref = 0.0

                        if SvW:
                            ref = 18.062 * exp(-0.05 * diff)
                        elif not SvW:
                            ref = 0.3419 * diff + 10.089

                        # attacker + ref ; defender - ref*0.8
                        final_score_change[0] = round(ref, 2)
                        final_score_change[1] = round(ref * 0.8 * -1, 2)

                        self.attacker.score += final_score_change[0]
                        self.defender.score += final_score_change[1]

                    # Result 2: Attacker fails
                    if in_result == Challenge.LOSE:
                        diff = abs(self.attacker.score - self.defender.score)
                        ref = 0.0

                        if SvW:
                            ref = 0.3419 * diff + 10.089
                        elif not SvW:
                            ref = 18.062 * exp(-0.05 * diff)

                        # attacker - ref*0.5*0.8 ; defender + ref*1*0.5
                        final_score_change[0] = round(ref * -1 * 0.4, 2)
                        final_score_change[0] = round(ref * 0.5, 2)

                        self.attacker.score += final_score_change[0]
                        self.defender.score += final_score_change[1]

                except:
                    log_data = ("Error occurred at set_scores" + str(sys.exc_info()) + '\n')
                    logger.info('ERROR: set_results: ' + log_data)

                else:
                    self.attacker.score = round(self.attacker.score, 2)
                    self.defender.score = round(self.defender.score, 2)
                    self.attacker.save()
                    self.defender.save()
                    self.save()
                    # record the use of this function by logging
                    log_data = ('Time: %s, Challenge_id: %s, set_result: %s, score_change: %s\n' %
                                (str(timezone.now()), str(self.id), str(in_result), str(final_score_change)))
                    logger.info('INFO: set_results: ' + log_data)

        else:
            self.result = in_result
            self.save()
            log_data = ('Time: %s, Challenge_id: %s, set_result = %s, score_change: %s\n' %
                        (str(timezone.now()), str(self.id), str(in_result), str(final_score_change)))
            logger.info('INFO: set_results: ' + log_data)
