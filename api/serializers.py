from rest_framework import serializers

from api.models import Mark, Model


class ModelSerializer(serializers.ModelSerializer):
    mark = serializers.PrimaryKeyRelatedField(queryset=Model.objects.all(), required=False)

    class Meta:
        model = Model
        fields = ['name', 'mark']


class MarkSerializer(serializers.ModelSerializer):
    models = ModelSerializer(many=True)

    class Meta:
        model = Mark
        fields = ['name', 'models']

    def create(self, validated_data):
        mark_name = validated_data.get("name")
        models_data = validated_data.get("models", [])

        mark = Mark.objects.create(name=mark_name)
        models_to_create = []

        for model_data in models_data:
            model_name = model_data.get("name")
            models_to_create.append(Model(name=model_name, mark=mark))

        Model.objects.bulk_create(models_to_create)
        return mark
