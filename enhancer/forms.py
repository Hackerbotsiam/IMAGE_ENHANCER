from django import forms


class ImageUploadForm(forms.Form):
    SCALE_CHOICES = [
        ('2', '2x'),
        ('3', '3x'),
        ('4', '4x'),
    ]
    SHARPEN_CHOICES = [
        ('none', 'Sharpening naa'),
        ('light', 'Halka sharpen'),
        ('strong', 'Strong sharpen'),
    ]

    image = forms.ImageField(label='Chobi select koro')
    scale = forms.ChoiceField(label='Koto guun boro korte chao', choices=SCALE_CHOICES,initial='2')
    sharpen = forms.ChoiceField(label='Sharpening level', choices=SHARPEN_CHOICES, initial='light')