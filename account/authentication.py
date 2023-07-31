from django.contrib.auth.models import User


class EmailAuthBackend:
    def authenticate(
        self, request, username=None, password=None
    ):  # username 과 password 를 이용하여 인증
        try:
            user = User.objects.get(email=username)
            if user.check_password(
                password
            ):  # check_password() 메서드는 비밀번호 해싱을 처리하여 주어진 비밀번호를 데이터베이스에 저장된 비밀번호와 비교
                return user
            return None
        except (user.DoesNotExist, user.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
