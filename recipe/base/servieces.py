from django.core.exceptions import ValidationError


def path_to_recipe_upload_image(initial, file):
    """
    Построение пути к файлу
    """
    return f'{initial.name}/{file}'

