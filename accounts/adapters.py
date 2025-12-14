from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom adapter for django-allauth.
    You can extend this later for:
    - email verification logic
    - domain restrictions
    - auto profile setup
    """

    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)

        if user.email:
            user.email = user.email.lower()

        if commit:
            user.save()
        return user
