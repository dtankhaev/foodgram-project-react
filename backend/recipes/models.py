from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

User = get_user_model()


class Recipe(models.Model):
    name = models.CharField(verbose_name='Название',
                            help_text='введите название рецепта',
                            max_length=200
                            )
    author = models.ForeignKey(User,
                               verbose_name='Автор',
                               on_delete=models.CASCADE,
                               related_name='recipes'
                               )
    image = models.ImageField(verbose_name='Изображение',
                              upload_to='recipes/images/',
                              )
    text = models.TextField(verbose_name='Описание',
                            help_text='введите описание рецепта',
                            )
    ingredients = models.ManyToManyField('Ingredient',
                                         through='IngredientAmount',
                                         verbose_name='Ингредиенты',
                                         help_text='введите ингредиенты',
                                         related_name='recipes',
                                         )
    tags = models.ManyToManyField('Tag',
                                  verbose_name='Тег',
                                  help_text='укажите тег рецепта',
                                  related_name='recipes'
                                  )
    cooking_time = models.PositiveSmallIntegerField(
                                verbose_name='Время приготовления в минутах',
                                validators=[MinValueValidator(
                                                1,
                                                message='мин. значение - 1')
                                            ]
                                )

    class Meta:
        ordering = ['name']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(verbose_name='Название',
                            help_text='введите название тега',
                            max_length=200,
                            unique=True
                            )
    color = models.TextField(verbose_name='цветовой HEX-код',
                             help_text='например: #49B64E',
                             max_length=7,
                             unique=True,
                             validators=[RegexValidator(
                                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                                message='не является цветом в формате HEX!'
                                )
                                        ]
                             )
    slug = models.SlugField(verbose_name='slug',
                            help_text='введите уникальный slug',
                            max_length=200,
                            unique=True,
                            )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(verbose_name='Название',
                            help_text='введите название рецепта',
                            max_length=200
                            )
    measurement_unit = models.CharField(verbose_name='единица измерения',
                                        help_text='введите ед. измерения',
                                        max_length=200
                                        )

    class Meta:
        ordering = ['id']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               )
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   )
    amount = models.PositiveIntegerField(verbose_name='количество',
                                         help_text='введите кол-во',
                                         blank=True
                                         )

    class Meta:
        ordering = ['id']
        verbose_name = 'Ингредиенты для рецепта'
        verbose_name_plural = 'Ингредиенты для рецептов'

    def __str__(self):
        return f'{self.ingredient} для {self.recipe}'
