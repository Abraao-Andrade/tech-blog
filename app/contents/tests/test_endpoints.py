import freezegun
from django.utils import timezone
from django.shortcuts import reverse


def test_list_categories(db, client, category, category_1, category_inative):

    response = client.get(
        reverse(
            "contents:categories-list",
            kwargs={"version": "v1"},
        ),
        content_type="application/json",
    )

    assert response.status_code == 200
    assert response.json().get("count") == 2


def test_list_categories_contents(
    db, client, category, category_1, article, article_future
):

    response = client.get(
        reverse(
            "contents:category-contents-list",
            kwargs={"version": "v1", "slug": category.slug},
        ),
        content_type="application/json",
    )

    assert response.status_code == 200
    assert response.json().get("count") == 1

    response = client.get(
        reverse(
            "contents:category-contents-list",
            kwargs={"version": "v1", "slug": category_1.slug},
        ),
        content_type="application/json",
    )

    assert response.status_code == 200
    assert response.json().get("count") == 0


def test_list_articles(db, client, article, article_future):

    response = client.get(
        reverse(
            "contents:articles-list",
            kwargs={"version": "v1"},
        ),
        content_type="application/json",
    )

    assert response.status_code == 200
    assert response.json().get("count") == 1

    with freezegun.freeze_time(timezone.now() + timezone.timedelta(days=1)):
        response = client.get(
            reverse(
                "contents:articles-list",
                kwargs={"version": "v1"},
            ),
            content_type="application/json",
        )

        assert response.status_code == 200
        assert response.json().get("count") == 2


def test_retrieve_articles(db, client, article):

    response = client.get(
        reverse(
            "contents:article-retrieve",
            kwargs={"version": "v1", "slug": article.slug},
        ),
        content_type="application/json",
    )

    assert response.status_code == 200
    assert response.json().get("slug") == article.slug

    response = client.get(
        reverse(
            "contents:article-retrieve",
            kwargs={"version": "v1", "slug": "slug-test"},
        ),
        content_type="application/json",
    )

    assert response.status_code == 404


def test_most_read_articles(db, client, celery_app, article, article_future):

    response = client.get(
        reverse(
            "contents:articles-most-read-list",
            kwargs={"version": "v1"},
        ),
        content_type="application/json",
    )

    assert response.status_code == 200
    assert response.json().get("count") == 0

    response = client.get(
        reverse(
            "contents:article-retrieve",
            kwargs={"version": "v1", "slug": article.slug},
        ),
        content_type="application/json",
    )

    assert response.status_code == 200

    with freezegun.freeze_time(timezone.now() + timezone.timedelta(days=1)):
        response = client.get(
            reverse(
                "contents:article-retrieve",
                kwargs={"version": "v1", "slug": article.slug},
            ),
            content_type="application/json",
        )

        assert response.status_code == 200

        response = client.get(
            reverse(
                "contents:article-retrieve",
                kwargs={"version": "v1", "slug": article_future.slug},
            ),
            content_type="application/json",
        )

        assert response.status_code == 200

        response = client.get(
            reverse(
                "contents:articles-most-read-list",
                kwargs={"version": "v1"},
            ),
            content_type="application/json",
        )

        assert response.status_code == 200
        assert response.json().get("count") == 2

        assert response.json().get("results")[0].get("slug") == article.slug
        assert response.json().get("results")[1].get("slug") == article_future.slug


def test_list_videos(db, client, video, video_future):

    response = client.get(
        reverse(
            "contents:videos-list",
            kwargs={"version": "v1"},
        ),
        content_type="application/json",
    )

    assert response.status_code == 200
    assert response.json().get("count") == 1

    with freezegun.freeze_time(timezone.now() + timezone.timedelta(days=1)):
        response = client.get(
            reverse(
                "contents:videos-list",
                kwargs={"version": "v1"},
            ),
            content_type="application/json",
        )

        assert response.status_code == 200
        assert response.json().get("count") == 2


def test_retrieve_videos(db, client, video):

    response = client.get(
        reverse(
            "contents:video-retrieve",
            kwargs={"version": "v1", "slug": video.slug},
        ),
        content_type="application/json",
    )

    assert response.status_code == 200
    assert response.json().get("slug") == video.slug

    response = client.get(
        reverse(
            "contents:video-retrieve",
            kwargs={"version": "v1", "slug": "slug-test"},
        ),
        content_type="application/json",
    )

    assert response.status_code == 404


def test_list_banners(db, client, article, article_future):

    response = client.get(
        reverse(
            "contents:banners-list",
            kwargs={"version": "v1"},
        ),
        content_type="application/json",
    )

    assert response.status_code == 200
    assert response.json().get("count") == 1
