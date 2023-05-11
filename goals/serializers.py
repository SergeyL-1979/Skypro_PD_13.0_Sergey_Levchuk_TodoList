from rest_framework import serializers
from core.serializers import UserSerializer
from goals.models import GoalCategory, GoalComment, Goal


class GoalCreateSerializer(serializers.ModelSerializer):
    """  """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ["id", "created", "updated", "user"]

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("Не разрешено в удаленной категории")

        if value.user != self.context["request"].user:
            raise serializers.ValidationError("Вы не создавали эту категорию")
        return value


class GoalSerializer(serializers.ModelSerializer):
    """  """
    user = UserSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("Не разрешено в удаленной категории")

        if value.user != self.context["request"].user:
            raise serializers.ValidationError("Вы не создавали эту категорию")
        return value


#
class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    """ """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        fields = '__all__'
        read_only_fields = ["id", "created", "updated", "user"]


# 4
class GoalCategorySerializer(serializers.ModelSerializer):
    """  """
    user = UserSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class CommentCreateSerializer(serializers.ModelSerializer):
    """  """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")

    def validate_goal(self, value):
        if value.user != self.context["request"].user:
            raise serializers.ValidationError("Вы не создавали эту заметку")
        return value


class CommentSerializer(serializers.ModelSerializer):
    """  """
    user = UserSerializer(read_only=True)

    class Meta:
        model = GoalComment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", "goal")

    def validate_goal(self, value):
        if value.user != self.context["request"].user:
            raise serializers.ValidationError("Вы не создавали эту заметку")
        return value
