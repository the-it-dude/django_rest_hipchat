from django import forms


class InstallationForm(forms.Form):
    oauthId = forms.UUIDField()
    capabilitiesUrl = forms.URLField()
    roomId = forms.IntegerField()
    groupId = forms.IntegerField()
    oauthSecret = forms.CharField()
