from rest_framework import serializers
from ..models import Book
import re

class BookSerialzer(serializers.ModelSerializer):
    published_date_formatter = serializers.DateField(source = 'published_date', format="%Y-%m-%d ",read_only=True)

    class Meta:
        model=Book
        fields = ('id', 'title', 'author', 'isbn', 'published_date', 
            'published_date_formatter', 'genre', 'available', 
            'created_at', 'updated_at', )
        read_only_fields=('id','created_at','updated_at')

class BookCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model=Book
        fields=('title', 'author', 'isbn', 'published_date', 'genre', 'available')

    def validate_isbn(self,value):
        if not re.match(r'^\d{10,13}',value):
            raise serializers.ValidationError("isbn must contain 10 to 13 digits only numbers")
        return value 

    def validate(self, data):
        if len(data.get("title","")) < 5:
            raise serializers.ValidationError("title must contain at least 5 characters")
        if len(data.get("author",'')) < 3:
            raise serializers.ValidationError("author name must contain at least 3 characters")
        
        return data
    
class BookUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields= ('title', 'author', 'isbn', 'published_date', 'genre', 'available')
        read_only_fields=("isbn",)
        extra_kwargs={
            'title': {'required': False},
            'author': {'required': False},
            'published_date': {'required': False},
            'genre': {'required': False},
            'available': {'required': False},
        }

    def validate(self, data):
        if len(data.get("title","")) < 5:
            raise serializers.ValidationError("title must contain at least 5 characters")
        if len(data.get("author",'')) < 3:
            raise serializers.ValidationError("author name must contain at least 3 characters")
        
        return data