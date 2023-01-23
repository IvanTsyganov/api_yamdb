import datetime
from rest_framework import serializers

from reviews.models import Category, Title, Genre, Review, Comment


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'



        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        class TitleSerializer(serializers.ModelSerializer):
    def validate_year(self,value):
        year_now = datetime.date.today().year
        if not (value <= year_now):
            raise serializers.ValidationError('Проверьте год выпуска')
        return value
    
    def validate_genre(self,value):
        if not Genre.objects.filter(name = f'{value}').exists():
            raise serializers.ValidationError('Выберите жанр из ранее созданных')
        return value
    
    def validate_category(self,value):
        if not Category.objects.filter(name = f'{value}').exists():
            raise serializers.ValidationError('Выберите категорию из ранее созданных')
        return value

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
