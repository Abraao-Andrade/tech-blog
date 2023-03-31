import json
from django.shortcuts import reverse
from app.comments.models import Comment


def test_list_comments_by_article(db, client, article, comment):

    response = client.get(
        reverse(
            "comments:comments-article-list",
            kwargs={"version": "v1", "article_id": article.id},
        ),
        content_type="application/json",
    )

    assert response.status_code == 200
    assert response.json().get("count") == 1


def test_create_comment_article(db, client, article):

    payload = json.dumps(
        {
            "name": "test user name",
            "email": "testuser@test.com",
            "text": "test test test text",
            "article_id": article.id,
        }
    )

    response = client.post(
        reverse(
            "comments:comments-create",
            kwargs={"version": "v1"},
        ),
        data=payload,
        content_type="application/json",
    )

    assert response.status_code == 201

    response = client.get(
        reverse(
            "comments:comments-article-list",
            kwargs={"version": "v1", "article_id": article.id},
        ),
        content_type="application/json",
    )

    assert response.status_code == 200
    assert response.json().get("count") == 1


def test_answer_comment(db, client, article, comment):
    payload = json.dumps(
        {
            "name": "test user name",
            "email": "testuser@test.com",
            "text": "test test test text",
            "article_id": article.id,
            "parent_id": comment.id,
        }
    )

    response = client.post(
        reverse(
            "comments:comments-create",
            kwargs={"version": "v1"},
        ),
        data=payload,
        content_type="application/json",
    )

    assert response.status_code == 201

    response = client.get(
        reverse(
            "comments:comments-article-list",
            kwargs={"version": "v1", "article_id": article.id},
        ),
        content_type="application/json",
    )

    assert response.status_code == 200
    assert response.json().get("count") == 2

    assert response.json().get("results")[1].get("parent") == comment.id


def test_interaction_comment(db, client, celery_app, comment):

    assert Comment.objects.get(id=comment.id).like == 0

    payload = json.dumps(
        {
            "like": "true",
        }
    )

    response = client.put(
        reverse(
            "comments:comments-interaction",
            kwargs={"version": "v1", "pk": comment.id},
        ),
        data=payload,
        content_type="application/json",
    )

    assert response.status_code == 200

    assert Comment.objects.get(id=comment.id).like == 1
