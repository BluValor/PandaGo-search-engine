from django.db import models
import pickle


# python manage.py makemigrations panda_search
# python manage.py sqlmigrate panda_search migration_name
# python manage.py migrate


class ArticleBox(models.Model):

    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200, default='untitled')
    publication = models.CharField(max_length=40, default='unknown source')
    author = models.CharField(max_length=100, default='unknown author')
    date = models.CharField(max_length=40, default='missing date')
    content = models.TextField(default='content not found')

    def __str__(self):
        return 'Title: %s\nAuthor: %s\n%s, %s\n%s' % (self.title, self.author, self.publication, self.date,
                                                      self.content)


class DataBox(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    data = models.BinaryField()

    def set_data(self, input_data):
        self.data = pickle.dumps(input_data)
        self.save()

    @property
    def value(self):
        return pickle.loads(self.data)
