def test_create_post(client):
    resp = client.post(
        "/api/posts",
        json={"title": "Первый пост", "content": "Текст поста", "author": "Иван"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Первый пост"
    assert data["content"] == "Текст поста"
    assert data["author"] == "Иван"
    assert "id" in data
    assert "created_at" in data

    get_resp = client.get(f"/api/posts/{data['id']}")
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "Первый пост"


def test_update_post(client):
    create = client.post(
        "/api/posts",
        json={"title": "Пост", "content": "Текст", "author": "Автор"},
    )
    assert create.status_code == 201
    post_id = create.json()["id"]

    resp = client.put(
        f"/api/posts/{post_id}",
        json={"title": "Обновлённый пост", "content": "Новый текст", "author": "Автор"},
    )
    assert resp.status_code == 200
    assert resp.json()["title"] == "Обновлённый пост"
    assert resp.json()["content"] == "Новый текст"


def test_delete_post(client):
    create = client.post(
        "/api/posts",
        json={"title": "Удаляемый пост", "content": "Текст", "author": "Автор"},
    )
    assert create.status_code == 201
    post_id = create.json()["id"]

    resp = client.delete(f"/api/posts/{post_id}")
    assert resp.status_code == 204

    get_resp = client.get(f"/api/posts/{post_id}")
    assert get_resp.status_code == 404


def test_create_comment(client):
    create_post = client.post(
        "/api/posts",
        json={"title": "Пост", "content": "Текст", "author": "Автор"},
    )
    post_id = create_post.json()["id"]

    resp = client.post(
        f"/api/posts/{post_id}/comments",
        json={"author": "Комментатор", "content": "Мой комментарий"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["post_id"] == post_id
    assert data["author"] == "Комментатор"
    assert data["content"] == "Мой комментарий"
    assert "id" in data

    comments = client.get(f"/api/posts/{post_id}/comments").json()
    assert len(comments) == 1
    assert comments[0]["content"] == "Мой комментарий"


def test_update_comment(client):
    create_post = client.post(
        "/api/posts",
        json={"title": "Пост", "content": "Текст", "author": "Автор"},
    )
    post_id = create_post.json()["id"]
    create_com = client.post(
        f"/api/posts/{post_id}/comments",
        json={"author": "Комментатор", "content": "Комментарий"},
    )
    comment_id = create_com.json()["id"]

    resp = client.put(
        f"/api/posts/{post_id}/comments/{comment_id}",
        json={"author": "Комментатор", "content": "Обновлённый комментарий"},
    )
    assert resp.status_code == 200
    assert resp.json()["content"] == "Обновлённый комментарий"


def test_delete_comment(client):
    create_post = client.post(
        "/api/posts",
        json={"title": "Пост", "content": "Текст", "author": "Автор"},
    )
    post_id = create_post.json()["id"]
    create_com = client.post(
        f"/api/posts/{post_id}/comments",
        json={"author": "Комментатор", "content": "Комментарий"},
    )
    comment_id = create_com.json()["id"]

    resp = client.delete(f"/api/posts/{post_id}/comments/{comment_id}")
    assert resp.status_code == 204

    comments = client.get(f"/api/posts/{post_id}/comments").json()
    assert len(comments) == 0
