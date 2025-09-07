from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UniversityChapterSerializer
from django.core.mail import EmailMessage
import json

@api_view(["POST"])
def create_university_chapter_nested(request):
    data = request.data.copy()
    if "data" in data:  # if JSON is sent as a string
        data = json.loads(data["data"])
        files = request.FILES
    else:
        data = request.data
        files = request.FILES

    serializer = UniversityChapterSerializer(data=data)

    if serializer.is_valid():
        chapter = serializer.save()

    
        subject = "New University Chapter Application"
        chapter_data = serializer.data
        university = chapter_data["university"]
        poc = chapter_data["point_of_contact"]["contact"]
        founding_members = chapter_data["founding_members"]
        custom_founding_members = chapter_data["custom_founding_members"]


        body = f"""
        New University Chapter Application Submitted

        🏫 University
        --------------
        Name: {university['name']}
        Address: {university['address']}
        District: {university['district']}
        State: {university['state']}
        Pin Code: {university['pin_code']}
        Website: {university['website']}

        👤 Point of Contact
        -------------------
        Name: {poc['name']}
        Email: {poc['email']}
        Phone: {poc['phone_number']}
        LinkedIn: {poc.get('linkedin', 'N/A')}

        👥 Founding Members
        -------------------
        """

        for i, member in enumerate(founding_members, start=1):
            c = member["contact"]
            body += f"""
        Member {i}:
            Name: {c['name']}
            Email: {c['email']}
            Phone: {c['phone_number']}
            LinkedIn: {c.get('linkedin', 'N/A')}
            Role: {member['role']}
            Level of Study: {member['current_level_of_study']}
            Discipline: {member['discipline']}
        """
        for j, member in enumerate(custom_founding_members, start=1):
            c = member["contact"]
            body += f"""
        Member {i}:
            Name: {c['name']}
            Email: {c['email']}
            Phone: {c['phone_number']}
            LinkedIn: {c.get('linkedin', 'N/A')}
            Role: {member['role']}
            Level of Study: {member['current_level_of_study']}
            Discipline: {member['discipline']}
        """

        email = EmailMessage(
            subject,
            body,
            "smiletesting07@gmail.com",   # from
            ["sid014w@gmail.com"],        # to
        )

        for file_field, file in request.FILES.items():
            email.attach(file.name, file.read(), file.content_type)

        try:
            email.send(fail_silently=False)
        except Exception as e:
            print("Email failed:", e)


        return Response(UniversityChapterSerializer(chapter).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
