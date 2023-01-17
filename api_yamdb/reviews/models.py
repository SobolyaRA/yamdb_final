from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_username, year_validator

TITLE_NAME_LENGTH = 200
TITLE_DESCRIPTION_LENGTH = 225
CATEGORY_NAME_LENGTH = 256
CATEGORY_SLUG_LENGTH = 50
RETURN_STRING_LENGTH = 15


class User(AbstractUser):
    """модель пользователя
    """
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True
    )

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        validators=[
            validate_username
        ],
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=50,
        choices=ROLES,
        default=USER
    )
    bio = models.TextField(
        verbose_name='О себе',
        null=True,
        blank=True
    )

    @property
    def is_moder(self):
        """Возвращает роль пользователя: Модератор
        """
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        """Возвращает роль пользователя: Администратор
        """
        return self.role == self.ADMIN

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Category(models.Model):
    name = models.CharField(max_length=CATEGORY_NAME_LENGTH)
    slug = models.SlugField(max_length=CATEGORY_SLUG_LENGTH, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=CATEGORY_NAME_LENGTH)
    slug = models.SlugField(max_length=CATEGORY_SLUG_LENGTH, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=TITLE_NAME_LENGTH)
    year = models.IntegerField(
        validators=[
            year_validator
        ],
    )
    description = models.TextField(
        max_length=TITLE_DESCRIPTION_LENGTH,
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='categories',
        verbose_name='Категория',
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='genres',
        verbose_name='Жанр',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )


class Review(models.Model):
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    text = models.TextField(
        blank=False,
        null=False,
        verbose_name='Текст отзыва',
    )
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
        verbose_name='Рейтинг отзыва',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации отзыва',
        blank=False,
        null=False,
        db_index=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:RETURN_STRING_LENGTH]


class Comment(models.Model):
    review = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    text = models.TextField(
        blank=False,
        null=False,
        verbose_name='Текст комментария',
    )
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
        blank=False,
        null=False,
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации комментария',
        blank=False,
        null=False,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:RETURN_STRING_LENGTH]
