from django.db import transaction
from django.db import IntegrityError
from django.utils import timezone
from app.contents.models import Category, Author, Article, Video


def test_create_category(db):
    Category.objects.create(
        name="category test",
        description="desc test",
    )
    try:
        with transaction.atomic():
            Category.objects.create(
                name="category test",
                description="desc test",
            )
    except IntegrityError:
        pass

    assert Category.objects.count() == 1


def test_create_author(db):
    Author.objects.create(
        name="category test",
        profession="profession test",
        description="desc test",
    )

    assert Author.objects.count() == 1


def test_create_article(db, author, category):
    article = Article.objects.create(
        title="article test",
        subtitle="subtitle test",
        text="text test",
        author=author,
        show_in_start=True,
        published_at=timezone.now(),
    )
    article.categories.add(category)

    try:
        with transaction.atomic():
            Article.objects.create(
                title="article test",
                subtitle="subtitle test",
                text="text test",
                author=author,
                show_in_start=True,
                published_at=timezone.now(),
            )
    except IntegrityError:
        pass

    assert Article.objects.count() == 1


def test_create_video(db):
    Video.objects.create(
        url="https://www.youtube.com/",
        title="title test",
        description="desc test",
        published_at=timezone.now(),
    )
    assert Video.objects.count() == 1
