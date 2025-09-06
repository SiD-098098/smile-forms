from django.db import models


class University(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=10)
    website = models.URLField()

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)  # Better for leading zeros & formatting
    linkedin = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.email})"


class PointOfContact(models.Model):
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE, related_name="point_of_contact")

    def __str__(self):
        return f"POC: {self.contact.name}"


class FoundingMember(models.Model):
    ROLE_CHOICES = [
        ("president", "President"),
        ("vice_president", "Vice President"),
        ("director_marketing", "Director, Marketing"),
        ("director_projects", "Director, Projects"),
        ("other", "Other"),
    ]
    LEVEL_CHOICES = [
        ("ug_1", "Undergraduate - First Year"),
        ("ug_2", "Undergraduate - Second Year"),
        ("ug_3", "Undergraduate - Third Year"),
        ("ug_4", "Undergraduate - Fourth Year"),
        ("pg_masters", "Postgraduate - Masters"),
        ("pg_doctoral", "Postgraduate - Doctoral"),
        ("other", "Other"),
    ]

    contact = models.OneToOneField(Contact, on_delete=models.CASCADE, related_name="founding_member")
    role = models.CharField(max_length=100, choices=ROLE_CHOICES)
    current_level_of_study = models.CharField(max_length=100, choices=LEVEL_CHOICES)
    discipline = models.CharField(max_length=100)
    resume = models.FileField(upload_to="resumes/")
    proof_of_association = models.FileField(upload_to="proofs/")

    def __str__(self):
        return f"{self.contact.name} - {self.get_role_display()}"


class CustomFoundingMember(models.Model):
    LEVEL_CHOICES = [
        ("ug_1", "Undergraduate - First Year"),
        ("ug_2", "Undergraduate - Second Year"),
        ("ug_3", "Undergraduate - Third Year"),
        ("ug_4", "Undergraduate - Fourth Year"),
        ("pg_masters", "Postgraduate - Masters"),
        ("pg_doctoral", "Postgraduate - Doctoral"),
        ("other", "Other"),
    ]

    contact = models.OneToOneField(Contact, on_delete=models.CASCADE, related_name="custom_founding_member", blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True)
    current_level_of_study = models.CharField(max_length=100, choices=LEVEL_CHOICES, blank=True, null=True)
    discipline = models.CharField(max_length=100, blank=True, null=True)
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)
    proof_of_association = models.FileField(upload_to="proofs/", blank=True, null=True)

    def __str__(self):
        contact_name = self.contact.name if self.contact else "No Contact"
        role_name = self.role or "No Role"
        return f"{contact_name} - {role_name}"


class UniversityChapter(models.Model):
    university = models.OneToOneField(University, on_delete=models.CASCADE)
    founding_members = models.ManyToManyField(FoundingMember, related_name="university_chapters")
    custom_founding_members = models.ManyToManyField("CustomFoundingMember", related_name="university_chapters", null=True, blank=True)
    point_of_contact = models.OneToOneField(PointOfContact, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.university.name} Chapter"
