import csv

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)

TABLES_2_FILES_DICT = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
    GenreTitle: 'genre_title.csv'
}
FOREIGN_KEYS = ('category', 'author')


def csv_handler(csv_data, model):
    objs = []
    for row in csv_data:
        for field in FOREIGN_KEYS:
            if field in row:
                row[f'{field}_id'] = row[field]
                del row[field]
        objs.append(model(**row))
    model.objects.bulk_create(objs)


class Command(BaseCommand):
    help = 'Import data from CSV files in static folder'

    def handle(self, *args, **options):
        for model, file in TABLES_2_FILES_DICT.items():
            with open(
                    f'{settings.BASE_DIR}/static/data/{file}',
                    'r', encoding='utf-8'
            ) as csv_file:
                try:
                    csv_handler(csv.DictReader(csv_file), model)
                except Exception as err:
                    self.stderr.write(f'Error in importing data: {err}')
                    CommandError(err)
        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
