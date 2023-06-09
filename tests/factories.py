import factory
from pytest_factoryboy import register

from django.contrib.auth import get_user_model

from core.models import User
from core.serializers import UserSerializer
from goals.models import GoalCategory, Board, Goal, GoalComment, BoardParticipant
from bot.models import TgUser

USER_MODEL = get_user_model()


@register
class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('user_name')
    password = factory.Faker('password')

    class Meta:
        model = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs) -> User:
        return User.objects.create_user(*args, **kwargs)


class SignUpRequest(factory.django.DjangoModelFactory):
    username = factory.SubFactory(UserFactory)
    password = factory.SubFactory(UserFactory)

    class Meta:
        model = User


# ============================================================
@register
class BoardFactory(factory.django.DjangoModelFactory):
    title = 'New Board'

    class Meta:
        model = Board


class BoardParticipantFactory(factory.django.DjangoModelFactory):
    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = BoardParticipant


class CategoryFactory(factory.django.DjangoModelFactory):
    title = 'New Category'
    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = GoalCategory


class GoalFactory(factory.django.DjangoModelFactory):
    title = 'New Goal'
    description = 'Description of New Goal'
    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)

    class Meta:
        model = Goal


class GoalCommentFactory(factory.django.DjangoModelFactory):
    text = 'test comment'
    goal = factory.SubFactory(GoalFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = GoalComment


class TuserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = TgUser
