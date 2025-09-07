from rest_framework import serializers
from .models import (
    University, Contact, PointOfContact,
    FoundingMember, UniversityChapter, CustomFoundingMember
)

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = "__all__"

class PointOfContactSerializer(serializers.ModelSerializer):
    contact = ContactSerializer()

    class Meta:
        model = PointOfContact
        fields = ["contact"]


class FoundingMemberSerializer(serializers.ModelSerializer):
    contact = ContactSerializer()

    class Meta:
        model = FoundingMember
        fields = ["contact", "role", "current_level_of_study", "discipline", "resume", "proof_of_association"]

class CustomFoundingMemberSerializer(serializers.ModelSerializer):
    contact = ContactSerializer(required=False, allow_null=True)  # optional

    class Meta:
        model = CustomFoundingMember
        fields = [
            "contact", "role", "current_level_of_study",
            "discipline", "resume", "proof_of_association"
        ]

class UniversityChapterSerializer(serializers.ModelSerializer):
    university = UniversitySerializer()
    point_of_contact = PointOfContactSerializer()
    founding_members = FoundingMemberSerializer(many=True)
    custom_founding_members = CustomFoundingMemberSerializer(many=True, required=False)

    class Meta:
        model = UniversityChapter
        fields = [
            "university", "point_of_contact",
            "founding_members", "custom_founding_members"
        ]

    def validate(self, attrs):
        founding_members = attrs.get("founding_members", [])
        if len(founding_members) != 4:
            raise serializers.ValidationError(
                {"founding_members": "Exactly 4 founding members are required."}
            )
        return attrs

    def create(self, validated_data):
        # Extract nested data
        university_data = validated_data.pop("university")
        poc_data = validated_data.pop("point_of_contact")
        founding_members_data = validated_data.pop("founding_members")
        custom_founding_members_data = validated_data.pop("custom_founding_members", [])

        # Create University
        university = University.objects.create(**university_data)

        # Create PointOfContact and its Contact
        poc_contact_data = poc_data.pop("contact")
        poc_contact = Contact.objects.create(**poc_contact_data)
        point_of_contact = PointOfContact.objects.create(contact=poc_contact)

        # Create FoundingMembers
        founding_members = []
        for member_data in founding_members_data:
            contact_data = member_data.pop("contact")
            contact = Contact.objects.create(**contact_data)
            member = FoundingMember.objects.create(contact=contact, **member_data)
            founding_members.append(member)

        # Create CustomFoundingMembers
        custom_founding_members = []
        for member_data in custom_founding_members_data:
            contact_data = member_data.pop("contact")
            contact = Contact.objects.create(**contact_data)
            member = CustomFoundingMember.objects.create(contact=contact, **member_data)
            custom_founding_members.append(member)

        # Create UniversityChapter and link everything
        chapter = UniversityChapter.objects.create(
            university=university,
            point_of_contact=point_of_contact
        )
        chapter.founding_members.set(founding_members)
        chapter.custom_founding_members.set(custom_founding_members)

        return chapter
