from django import forms
from .models import *
from datetime import date
from info.forms import make_club_choice


def get_current_session():
    now = date.today()
    end = now.replace(day=31, month=3, year=now.year)

    if end > now:
        start_year = now.year - 1
    else:
        start_year = now.year

    return (start_year,str(start_year)+ " - " +str(start_year+1))

def get_next_session():
    c_session = get_current_session()
    start_year = c_session[0]+1
    return (start_year,str(start_year)+ " - " +str(start_year+1))


class NominationForm(forms.Form):
    SESSION_CHOICE= (
        get_current_session(),
        get_next_session(),
    )
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea, help_text="Description supports HTML formatting")
    deadline = forms.DateField(required=True, initial=datetime.now(), help_text="Format YYYY-MM-DD")
    nomi_session = forms.ChoiceField(choices=SESSION_CHOICE, label="Session",
                                     widget=forms.Select(), help_text="Current session " + get_current_session()[1])


class NominationReplicationForm(forms.Form):
    SESSION_CHOICE= (
        get_current_session(),
        get_next_session(),
    )
    title = forms.CharField()
    deadline = forms.DateField(required=True, initial=datetime.now(), help_text="Format YYYY-MM-DD")
    nomi_session = forms.ChoiceField(choices=SESSION_CHOICE, label="Session",
                                     widget=forms.Select(), help_text="Current session " + get_current_session()[1])


class PostForm(forms.Form):
    def __init__(self, parent, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['post_name'] = forms.CharField()

        if parent.perms == 'can ratify the post':
            self.fields['elder_brother'] = forms.ChoiceField(
                choices=[(parent.id,parent)] + [(o.id, o) for o in Post.objects.filter(parent=parent)], widget=forms.Select)
            self.fields['power'] = forms.ChoiceField(
                choices=[("normal", "normal"), ("can approve post and send nominations to users", "can approve and send nominations to users")], widget=forms.Select)

        if parent.club.club_set.all():
            self.fields['club'] = forms.ChoiceField(
                choices=[(o.id, o) for o in Club.objects.filter(club_parent=parent.club)], widget=forms.Select)

        else:
            self.fields['club'] = forms.ChoiceField(choices=[(parent.club.id, parent.club)], widget=forms.Select)

class ChangePostName(forms.Form):
    post_name = forms.CharField()

class PostWithBroForm(forms.Form):
    def __init__(self, parent, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['post_name'] = forms.CharField()


        self.fields['elder_brother'] = forms.ChoiceField(
                choices=[(parent.id,parent)] + [(o.id, o) for o in Post.objects.filter(parent=parent)], widget=forms.Select)

        if parent.club.club_set.all():
            self.fields['club'] = forms.ChoiceField(
                choices=[(o.id, o) for o in Club.objects.filter(club_parent=parent.club)], widget=forms.Select)

        else:
            self.fields['club'] = forms.ChoiceField(choices=[(parent.club.id, parent.club)], widget=forms.Select)



class ClubForm(forms.Form):
    club_name = forms.CharField()

class DeadlineForm(forms.Form):
    deadline = forms.DateField(required=True, initial=datetime.now(), help_text="Format YYYY-MM-DD")


class BlankForm(forms.Form):
    pass


class ConfirmApplication(forms.Form):
    Tick_the_box_for_confirmation = forms.CharField(max_length=100, widget=forms.CheckboxInput())

class RatifyApplication(forms.Form):
    Tick_the_box_for_confirmation = forms.CharField(max_length=100, widget=forms.CheckboxInput())

class SaveConfirm(forms.Form):
    save_or_submit  = forms.ChoiceField(choices=[("only save","only save"),("save and submit","save and submit")] ,widget=forms.RadioSelect)




class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)


class UserId(forms.Form):
    user_roll = forms.CharField(label="IITK Username")


class SelectNomiForm(forms.Form):
    def __init__(self, post, *args, **kwargs):
        super(SelectNomiForm, self).__init__(*args, **kwargs)
        self.fields['group'] = forms.MultipleChoiceField(
            choices=[(o.id, o) for o in Nomination.objects.filter(nomi_approvals=post).filter(group_status = "normal").filter(status='Nomination created')],
            widget=forms.CheckboxSelectMultiple,label="To be grouped ",required=False
        )


class GroupDetail(forms.ModelForm):
    class Meta:
        model = GroupNomination
        labels = {
            "name": "Title *",
            "deadline" : "Common deadline"
        }
        help_texts = {
            'deadline': 'Format:YYYY-MM-DD',
        }

        fields = ('name','description','deadline')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        labels = {
            "name": "Title *",
            "deadline" : "Common deadline"
        }

        fields = ('user_img','hall','room_no','contact')



class ClubFilter(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ClubFilter, self).__init__(*args, **kwargs)
        self.fields["club"] = forms.ChoiceField( choices = make_club_choice(None,-2),widget=forms.Select,required= False)


class PostHolderForm(forms.Form):
    SESSION_CHOICE = (
        get_current_session(),
        get_next_session(),
    )

    email = forms.CharField(label='Username', help_text='Exclude @iitk.ac.in')
    session = forms.ChoiceField(choices=SESSION_CHOICE, widget=forms.Select, label='Session')
