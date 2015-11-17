from django import forms
from hs.models import Contestant, Challenge


class NewAttackForm(forms.Form):
    attacker_set = Contestant.objects.all().filter(is_active=True)
    attacker = forms.ModelChoiceField(queryset=attacker_set, widget=forms.HiddenInput, label='Who are you?')
    defender = forms.ModelChoiceField(queryset=attacker_set, label='Who do you want to attack?')

    def clean(self):
        cleaned_data = super(NewAttackForm, self).clean()
        attacker = cleaned_data.get("attacker")
        defender = cleaned_data.get("defender")

        if attacker == defender:
            raise forms.ValidationError("You can't attack yourself!")


class SetChallengeResultForm(forms.Form):
    challenge_set = Challenge.objects.all().filter(result=Challenge.PENDING)
    applicant_set = Contestant.objects.all().filter(is_active=True)
    result_choice = (
        ('', "----------"),
        (Challenge.WIN, 'Yes. Challenge succeeded'),
        (Challenge.LOSE, 'No. Challenge Failed'),
        (Challenge.CANCEL, 'Cancelled. Challenge is canceled by the attacker')
    )
    applicant = forms.ModelChoiceField(queryset=applicant_set, widget=forms.HiddenInput, label='Who are you?')
    challenge = forms.ModelChoiceField(queryset=challenge_set, widget=forms.HiddenInput, label='Which Challenge?')
    result = forms.ChoiceField(result_choice, label='Does the challenge succeed?')
