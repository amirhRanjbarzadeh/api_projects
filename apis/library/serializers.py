from rest_framework import serializers
from .models import Author, Genre, Book


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "bio"]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    genres = GenreSerializer(many=True)

    class Meta:
        model = Book
        fields = ["id", "title", "description", "publication_date", "authors", "genres"]

    def create(self, validated_data):
        authors_data = validated_data.pop("authors")
        genres_data = validated_data.pop("genres")
        book = Book.objects.create(**validated_data)

        for author_data in authors_data:
            author, created = Author.objects.get_or_create(**author_data)
            book.authors.add(author)

        for genre_data in genres_data:
            genre, created = Genre.objects.get_or_create(**genre_data)
            book.genres.add(genre)

        return book

    def update(self, instance, validated_data):
        authors_data = validated_data.pop('authors', None)
        genres_data = validated_data.pop('genres', None)

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.publication_date = validated_data.get('publication_date', instance.publication_date)
        instance.save()

        if authors_data is not None:
            instance.authors.clear()
            for author_data in authors_data:
                author, created = Author.objects.get_or_create(**author_data)
                instance.authors.add(author)

        if genres_data is not None:
            instance.genres.clear()
            for genre_data in genres_data:
                genre, created = Genre.objects.get_or_create(**genre_data)
                instance.genres.add(genre)

        return instance
