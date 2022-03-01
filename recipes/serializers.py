from rest_framework import  serializers
from .models import Recipe, Image, Ingredient, Instruction, Vedio

#make all class serializers for Image , Ingredient , Instruction , Vedio , Recipe
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('url',)

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('details',)

class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruction
        fields = ('details',)


class VedioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vedio
        fields = ('url',)


class RecipeSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    instructions = InstructionSerializer(many=True, read_only=True)
    vedios = VedioSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ('name', 'slug', 'rating', 'time', 'images', 'ingredients', 'instructions', 'vedios')
