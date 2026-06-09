from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Category, Product, Review

class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

    def validate_name(self, value):
        if not value.strip():
            raise ValidationError("Название категории не может быть пустым.")
        if Category.objects.filter(name__iexact=value).exists():
            raise ValidationError("Категория с таким названием уже существует.")
        return value


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

   
    def validate_price(self, value):
        if value <= 0:
            raise ValidationError("Цена товара должна быть больше нуля.")
        return value

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise ValidationError("Название товара должно содержать минимум 3 символа.")
        return value

    def validate(self, attrs):
        title = attrs.get('title', '')
        description = attrs.get('description', '')

        if title.lower() in description.lower():
            raise ValidationError({
                "description": "Описание товара не должно содержать в себе его название."
            })
        return attrs


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def validate_text(self, value):
        if len(value.strip()) < 5:
            raise ValidationError("Отзыв слишком короткий. Напишите хотя бы 5 символов.")
        return value

    def validate_stars(self, value):
        if value < 1 or value > 5:
            raise ValidationError("Оценка должна быть в диапазоне от 1 до 5.")
        return value


class ProductReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'rating', 'reviews']

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return 0.0
        total_stars = sum([review.stars for review in reviews])
        return round(total_stars / len(reviews), 2)