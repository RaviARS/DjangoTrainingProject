from rest_framework import serializers
from datetime import date
from .models import Customer


class CustomerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'mobile', 'email', 'date_of_birth']

    name = serializers.CharField(max_length=100)
    mobile = serializers.IntegerField()
    email = serializers.EmailField()
    date_of_birth = serializers.DateField()

    def validate_name(self, name):
        "Allows only Alphabet character"

        if not name.isalpha():
            raise serializers.ValidationError("Invalid Name ( Allows only Alphabet character ) ")
        return name

    def validate_mobile(self, mobile):
        "Allows only 10 digit Mobile Number"

        if not (10 == len(str(mobile))):
            raise serializers.ValidationError("Invalid mobile number ( Allows only 10 digit Mobile Number ) ")
        return mobile

    def validate_date_of_birth(self, dob):
        "Allows only age between 18 to 60 "

        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if not (18 <= age <= 60):
            raise serializers.ValidationError("You are not eligible to Register ( Allows only age between 18 to 60 ) ")
        return dob