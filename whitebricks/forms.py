from django import forms



class SignupForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))





Cities=[
    ('Trivandrum','Trivandrum'),
    ('Kochi','Kochi'),
    ('Kottayam','Kottayam'),
    ('Kollam','Kollam'),
    ]

Bedrooms= [tuple([x,x]) for x in range(1,10)]

Price=[
    ('1000','Under 1000'),
    ('2000','under 2000'),
    ('5000','under 5000'),
    ('10,000','under 10000'),
    ('20,000','under 20,000')
]

class PGForm(forms.Form):
    info_highlights = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Highlights'}))
    info_description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}))
    info_price = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rent per month'}))
    info_bedroom = forms.IntegerField(widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'No of bedrooms'},choices=Bedrooms))
    info_city = forms.CharField(widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'City'}, choices=Cities))
    info_image = forms.FileField(widget=forms.FileInput(), required=False)
    info_fname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Firstname'}))
    info_lname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lastname'}))
    info_email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    info_phone = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}))
    info_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}))
