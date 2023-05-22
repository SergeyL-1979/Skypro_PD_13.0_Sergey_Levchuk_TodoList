from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from core.models import User
from core.serializers import UserSerializer
from goals.models import GoalCategory, GoalComment, Goal, Board, BoardParticipant


class GoalCreateSerializer(serializers.ModelSerializer):
    """ Модель создания объекта `ЦЕЛЬ`. Фильтр, что объект `ЦЕЛЬ` является владельцем. """
    category = serializers.PrimaryKeyRelatedField(queryset=GoalCategory.objects.all())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ["id", "created", "updated", "user"]

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("Не разрешено в удаленной категории")

        if not BoardParticipant.objects.filter(
                board_id=value.board_id,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
                user=self.context["request"].user,
        ).exists():
            raise serializers.ValidationError("Вы не создавали эту категорию")
        return value


class GoalSerializer(serializers.ModelSerializer):
    """ Модель объекта `ЦЕЛЬ`. """
    user = UserSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ("id", "created", "updated", "user")

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("Не разрешено в удаленной категории")

        # if value.user != self.context["request"].user:
        if self.instance.category.board_id != value.board_id:
            raise serializers.ValidationError("Вы не создавали эту категорию")
        return value


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    """ Модель проверки объекта `Категория` является пользователь владельцем или редактором """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        fields = '__all__'
        read_only_fields = ["id", "created", "updated", "user"]

    def validate_board(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("Не разрешено в удаленном объекте")
        allow = BoardParticipant.objects.filter(
            board=value,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
            user=self.context["request"].user,
        ).exists()
        if not allow:
            raise serializers.ValidationError("Вы должны быть владельцем или редактором")
        return value


class GoalCategorySerializer(serializers.ModelSerializer):
    """ Модель вывода объекта """
    user = UserSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = '__all__'
        read_only_fields = ("id", "created", "updated", "user", "board")


class CommentCreateSerializer(serializers.ModelSerializer):
    """ Модель создания объекта `Комментарий` и проверки его на владельца или редактора. """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ("id", "created", "updated", "user")

    def validate_goal(self, value):
        # if value.user != self.context["request"].user:
        if not BoardParticipant.objects.filter(
                board_id=value.category.board_id,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
                user=self.context["request"].user,
        ).exists():
            raise serializers.ValidationError("Вы не являетесь автором этого комментария")
        return value


class CommentSerializer(serializers.ModelSerializer):
    """ Модель вывода объектов `Комментарий` """
    user = UserSerializer(read_only=True)

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ("id", "created", "updated", "user", "goal")


class BoardCreateSerializer(serializers.ModelSerializer):
    """ Модель создания объекта `Доска` """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = ("id", "created", "updated")

    def create(self, validated_data):
        user = validated_data.pop("user")
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(user=user, board=board, role=BoardParticipant.Role.owner)
        return board


class BoardParticipantSerializer(serializers.ModelSerializer):
    """ Модель участников. """
    role = serializers.ChoiceField(required=True, choices=BoardParticipant.editable_choices)
    user = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:
        model = BoardParticipant
        fields = '__all__'
        read_only_fields = ("id", "created", "updated", "board")


class BoardSerializer(serializers.ModelSerializer):
    """ Модель редактирования """
    participants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def update(self, instance, validated_data):
        owner = validated_data.pop("user")
        new_participants = validated_data.pop("participants")
        new_by_id = {part["user"].id: part for part in new_participants}

        old_participants = instance.participants.exclude(user=owner)
        with transaction.atomic():
            for old_participant in old_participants:
                if old_participant.user_id not in new_by_id:
                    old_participant.delete()
                else:
                    if old_participant.role != new_by_id[old_participant.user_id]["role"]:
                        old_participant.role = new_by_id[old_participant.user_id]["role"]
                        old_participant.save()
                    new_by_id.pop(old_participant.user_id)
            for new_part in new_by_id.values():
                BoardParticipant.objects.create(board=instance, user=new_part["user"], role=new_part["role"])

            instance.title = validated_data["title"]
            instance.save()

        return instance

    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = ("id", "created", "updated")


class BoardListSerializer(serializers.ModelSerializer):
    """ Модель выводит все объекты """
    class Meta:
        model = Board
        fields = '__all__'
