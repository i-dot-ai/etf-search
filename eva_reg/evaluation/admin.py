from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.urls import reverse

from . import models


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = models.User
        fields = ("email",)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].help_text = (
            "Raw passwords are not stored, so there is no way to see "
            'this user\'s password. You can <a href="%s"> '
            "change the password using this form</a>."
        ) % reverse("admin:auth_user_password_change", args=[self.instance.id])

    class Meta:
        model = models.User
        fields = (
            "email",
            "password",
            "is_active",
            "is_staff",
            "is_superuser",
        )


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = (
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        "is_external_user",
    )
    list_filter = ("is_active", "is_staff", "is_superuser", "is_external_user")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Permissions",
            {"fields": ("is_active", "is_staff", "is_superuser", "is_external_user")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Evaluation)
admin.site.register(models.Intervention)
admin.site.register(models.OutcomeMeasure)
admin.site.register(models.OtherMeasure)
