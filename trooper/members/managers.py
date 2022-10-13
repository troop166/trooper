from django.contrib.auth.models import UserManager
from django.db.models import Q


class MemberManager(UserManager):
    def get_by_natural_key(self, username):
        return self.get(
            Q(**{f"{self.model.USERNAME_FIELD}__iexact": username})
            | Q(**{f"{self.model.EMAIL_FIELD}__iexact": username})
        )
