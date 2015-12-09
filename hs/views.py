from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required, user_passes_test
from hs.models import Contestant, Challenge
from hs.forms import NewAttackForm, SetChallengeResultForm
# Data_logging
import logging

logger = logging.getLogger(__name__)


def is_hs_contestant_check(user):
    if hasattr(user, 'contestant'):
        return True
    else:
        return False

def is_hs_staff_check(user):
    # TODO: finish the staff check
    return False


def error_not_hs_member(request):
    return render(request, 'hs/auth/error_not_hs_member.html')


def redirect_to_hs(request):
    return HttpResponseRedirect(reverse('hs:index'))


def index(request):
    return render(request, 'hs/index.html')

@user_passes_test(is_hs_staff_check, 'hs:error_not_hs_member')
def rank(request):
    '''
    /hs/rank.html
    !!!Access control needed!!!
    Only staff can view this page!
    :param request:
    :return:
    '''
    latest_contestant_list = Contestant.objects.filter(is_active=True).order_by('-score')
    context = {'latest_contestant_list': latest_contestant_list}
    return render(request, 'hs/rank.html', context)


@login_required
@user_passes_test(is_hs_contestant_check, 'hs:error_not_hs_member')
def contestant_detail(request, contestant_id):
    contestant = get_object_or_404(Contestant, id=contestant_id)
    return render(request, 'hs/contestant_detail.html', {'contestant': contestant})


@login_required
@user_passes_test(is_hs_contestant_check, 'hs:error_not_hs_member')
def challenge_detail(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)
    return render(request, 'hs/challenge_detail.html', {'challenge': challenge})


@login_required
@user_passes_test(is_hs_contestant_check, 'hs:error_not_hs_member')
def contestant_my_index(request):
    if request.user.is_staff:
        # temporary: not finished admin page
        return HttpResponseRedirect(reverse('hs:error_not_hs_member'))

    attack_list = Challenge.objects.filter(attacker=request.user.contestant, result='PEND')
    defend_list = Challenge.objects.filter(defender=request.user.contestant, result='PEND')

    history_attack_list = Challenge.objects.filter(attacker=request.user.contestant).exclude(result='PEND').order_by(
        '-expire_date')[0:3]
    history_defend_list = Challenge.objects.filter(defender=request.user.contestant).exclude(result='PEND').order_by(
        '-expire_date')[0:3]

    current_contestant = request.user.contestant
    contestant_score = current_contestant.score
    contestant_list = Contestant.objects.filter(is_active=True)

    # for the ahead contestant's score
    ahead_contestant_score = contestant_score
    if current_contestant.position != 1:
        ahead_contestant_score = contestant_list.filter(score__gt=contestant_score).order_by('score').first().score

    # for the follow contestant's score
    try:
        follow_contestant_score = contestant_list.filter(score__lt=contestant_score).order_by('-score').first().score
    except AttributeError:
        follow_contestant_score = contestant_score


    context = {'attack_list': attack_list, 'defend_list': defend_list, 'history_attack_list': history_attack_list,
               'history_defend_list': history_defend_list, 'ahead_contestant_score': ahead_contestant_score, 'follow_contestant_score': follow_contestant_score}
    return render(request, 'hs/contestant_my_index.html', context)


@login_required
@user_passes_test(is_hs_contestant_check, 'hs:error_not_hs_member')
def new_attack(request):
    if request.user.is_staff:
        # temporary: not finished admin page
        return HttpResponseRedirect(reverse('hs:error_not_hs_member'))

    if request.method == 'POST':
        form = NewAttackForm(request.POST)
        form.fields['attacker'].initial = request.user.contestant.id
        if form.is_valid():
            # process
            attacker = form.cleaned_data['attacker']
            defender = form.cleaned_data['defender']
            new_challenge = Challenge(start_date=timezone.now(),
                                      expire_date=timezone.now() + timedelta(days=1),
                                      attacker=attacker, defender=defender)
            new_challenge.save()
            return HttpResponseRedirect(reverse('hs:challenge_detail', args=(new_challenge.id,)))
    else:
        form = NewAttackForm()
        form.fields['attacker'].initial = request.user.contestant.id

    return render(request, 'hs/new_attack.html', {'form': form})


@login_required
@user_passes_test(is_hs_contestant_check, 'hs:error_not_hs_member')
def set_challenge_result(request):
    if request.user.is_staff:
        # temporary: not finished admin page
        return HttpResponseRedirect(reverse('hs:error_not_hs_member'))
    if request.method == 'POST':
        form = SetChallengeResultForm(request.POST)
        # if request.POST['in_challenge_id'] exists, go to ELSE part to render a new form
        # if that is not exist, it means that the forms is filled and process data instead.
        # Alternative method: if 'in_challenge_id' not in request.POST: statement
        try:
            request.POST['in_challenge_id']
        except:
            challenge = Challenge.objects.get(pk=request.POST['challenge'])
            form.fields['applicant'].initial = request.user.contestant.id
            if form.is_valid():
                # process
                result = form.cleaned_data['result']
                if result == Challenge.WIN or result == Challenge.LOSE or result == Challenge.CANCEL:
                    Challenge.set_results(challenge, result)

                log_data = str(timezone.now()) + ' [SET RESULT]: Applicant:%s , Challenge:%s, Set_Result:%s' % \
                                                 (str(request.user.contestant.id), str(challenge.id), str(result))
                logger.info(log_data)
                return HttpResponseRedirect(reverse('hs:challenge_detail', args=(challenge.id,)))
            return render(request, 'hs/set_challenge_result.html', {'form': form})
        else:
            form = SetChallengeResultForm()
            form.fields['challenge'].initial = request.POST['in_challenge_id']
            form.fields['applicant'].initial = request.user.contestant.id
            return render(request, 'hs/set_challenge_result.html', {'form': form})
    else:
        return render(request, 'hs/auth/error_not_hs_member.html')
