from django.db import models
from django.utils.translation import get_language

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name_en = models.CharField(null=False, blank=False, max_length=255)
    name_de = models.CharField(null=False, blank=False, max_length=255)
    text_en = models.TextField()
    text_de = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)

    def name(self):
        lang = get_language()
        if lang == 'en':
            return self.name_en
        else:
            return self.name_de

    def text(self):
        lang = get_language()
        if lang == 'en':
            text = self.text_en
        else:
            text = self.text_de

        return text.replace('\\', '')

    def text1(self):
        lang = get_language()
        if lang == 'en':
            text = self.text_en
        else:
            text = self.text_de
        return text.partition('\\')[0]

    def text2(self):
        lang = get_language()
        if lang == 'en':
            text = self.text_en
        else:
            text = self.text_de
        return text.partition('\\')[2]

    class Meta:
        ordering = ('-time_created', )

