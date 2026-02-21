const API = '/api';

async function loadPosts() {
  const res = await fetch(API + '/posts');
  if (!res.ok) throw new Error('Не удалось загрузить посты');
  return res.json();
}

async function createPost(title, content, author) {
  const res = await fetch(API + '/posts', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, content, author }),
  });
  if (!res.ok) throw new Error('Ошибка создания поста');
  return res.json();
}

async function updatePost(id, data) {
  const res = await fetch(API + '/posts/' + id, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Ошибка обновления поста');
  return res.json();
}

async function deletePost(id) {
  const res = await fetch(API + '/posts/' + id, { method: 'DELETE' });
  if (!res.ok) throw new Error('Ошибка удаления поста');
}

async function getComments(postId) {
  const res = await fetch(API + '/posts/' + postId + '/comments');
  if (!res.ok) throw new Error('Не удалось загрузить комментарии');
  return res.json();
}

async function addComment(postId, author, content) {
  const res = await fetch(API + '/posts/' + postId + '/comments', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ author, content }),
  });
  if (!res.ok) throw new Error('Ошибка добавления комментария');
  return res.json();
}

async function updateComment(postId, commentId, data) {
  const res = await fetch(API + '/posts/' + postId + '/comments/' + commentId, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Ошибка обновления комментария');
  return res.json();
}

async function deleteComment(postId, commentId) {
  const res = await fetch(API + '/posts/' + postId + '/comments/' + commentId, { method: 'DELETE' });
  if (!res.ok) throw new Error('Ошибка удаления комментария');
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

function formatDate(iso) {
  if (!iso) return '';
  const d = new Date(iso);
  return d.toLocaleString('ru-RU', { dateStyle: 'short', timeStyle: 'short' });
}

function renderPost(p, comments) {
  const card = document.createElement('div');
  card.className = 'card card-post mb-4';
  card.dataset.postId = p.id;
  card.innerHTML = `
    <div class="card-body">
      <div class="d-flex justify-content-between align-items-start gap-2 flex-wrap">
        <h5 class="card-title">${escapeHtml(p.title)}</h5>
        <div class="d-flex gap-1">
          <button type="button" class="btn btn-outline-primary btn-action btn-edit" data-action="edit-post"><i class="bi bi-pencil me-1"></i>Изменить</button>
          <button type="button" class="btn btn-outline-danger btn-action btn-del" data-action="delete-post"><i class="bi bi-trash me-1"></i>Удалить</button>
        </div>
      </div>
      <p class="post-meta mb-2"><i class="bi bi-person"></i>${escapeHtml(p.author)} <span class="ms-2"><i class="bi bi-clock"></i>${formatDate(p.created_at)}</span></p>
      <p class="card-text post-content">${escapeHtml(p.content)}</p>

      <div class="comments-section comments-block" data-post-id="${p.id}">
        <div class="section-title"><i class="bi bi-chat-left-text me-1"></i>Комментарии</div>
        <div class="comments-list mb-3"></div>
        <form class="form-new-comment mb-0 form-inline" data-post-id="${p.id}">
          <div class="row g-2">
            <div class="col-md-4"><input type="text" class="form-control form-control-sm" placeholder="Ваше имя" name="author" required></div>
            <div class="col-md"><input type="text" class="form-control form-control-sm" placeholder="Написать комментарий..." name="content" required></div>
            <div class="col-md-auto"><button class="btn btn-primary btn-sm w-100" type="submit"><i class="bi bi-plus-lg me-1"></i>Добавить</button></div>
          </div>
        </form>
      </div>
    </div>
  `;

  const commentsList = card.querySelector('.comments-list');
  (comments || []).forEach(c => {
    commentsList.appendChild(renderComment(p.id, c));
  });

  card.querySelector('[data-action="edit-post"]').addEventListener('click', () => startEditPost(card, p));
  card.querySelector('[data-action="delete-post"]').addEventListener('click', () => confirmDeletePost(p.id));
  card.querySelector('.form-new-comment').addEventListener('submit', (e) => {
    e.preventDefault();
    const form = e.target;
    addComment(p.id, form.author.value.trim(), form.content.value.trim())
      .then(() => { form.reset(); refreshPosts(); })
      .catch(err => alert(err.message));
  });

  return card;
}

function renderComment(postId, c) {
  const div = document.createElement('div');
  div.className = 'comment-item d-flex justify-content-between align-items-start gap-2';
  div.dataset.commentId = c.id;
  div.innerHTML = `
    <div class="flex-grow-1 min-w-0">
      <span class="comment-author">${escapeHtml(c.author)}</span>
      <span class="comment-date ms-1">${formatDate(c.created_at)}</span>
      <p class="comment-text mb-0">${escapeHtml(c.content)}</p>
    </div>
    <div class="d-flex gap-1 flex-shrink-0">
      <button type="button" class="btn btn-link btn-sm p-0 text-primary btn-edit-comment" title="Изменить"><i class="bi bi-pencil"></i></button>
      <button type="button" class="btn btn-link btn-sm p-0 text-danger btn-del-comment" title="Удалить"><i class="bi bi-trash"></i></button>
    </div>
  `;
  div.querySelector('.btn-edit-comment').addEventListener('click', () => editComment(postId, c, div));
  div.querySelector('.btn-del-comment').addEventListener('click', () => confirmDeleteComment(postId, c.id));
  return div;
}

function startEditPost(card, p) {
  const body = card.querySelector('.card-body');
  const titleEl = body.querySelector('.card-title');
  const contentEl = body.querySelector('.post-content');
  if (!contentEl) return;
  const btnEdit = body.querySelector('[data-action="edit-post"]');
  if (card.dataset.editing === '1') return;
  card.dataset.editing = '1';
  titleEl.innerHTML = `<input type="text" class="form-control form-control-sm" value="${escapeHtml(p.title)}" id="edit-title">`;
  contentEl.outerHTML = `<textarea class="form-control form-control-sm" rows="3" id="edit-content">${escapeHtml(p.content)}</textarea>`;
  btnEdit.innerHTML = '<i class="bi bi-check2 me-1"></i>Сохранить';
  btnEdit.dataset.action = 'save-post';
  body.querySelector('[data-action="save-post"]').addEventListener('click', () => {
    const title = document.getElementById('edit-title').value.trim();
    const content = document.getElementById('edit-content').value.trim();
    updatePost(p.id, { title, content, author: p.author })
      .then(() => refreshPosts())
      .catch(err => alert(err.message));
  });
}

function editComment(postId, c, div) {
  const block = div.querySelector('.flex-grow-1');
  if (!block) return;
  block.innerHTML = `
    <div class="row g-2 align-items-center">
      <div class="col-auto"><input type="text" class="form-control form-control-sm" value="${escapeHtml(c.author)}" id="edit-com-author" placeholder="Имя"></div>
      <div class="col"><input type="text" class="form-control form-control-sm" value="${escapeHtml(c.content)}" id="edit-com-content" placeholder="Текст"></div>
      <div class="col-auto"><button type="button" class="btn btn-sm btn-primary" id="save-com-btn"><i class="bi bi-check2 me-1"></i>Сохранить</button></div>
    </div>
  `;
  document.getElementById('save-com-btn').addEventListener('click', () => {
    const author = document.getElementById('edit-com-author').value.trim();
    const content = document.getElementById('edit-com-content').value.trim();
    updateComment(postId, c.id, { author, content })
      .then(() => refreshPosts())
      .catch(err => alert(err.message));
  });
}

function confirmDeletePost(id) {
  if (!confirm('Удалить пост?')) return;
  deletePost(id).then(() => refreshPosts()).catch(err => alert(err.message));
}

function confirmDeleteComment(postId, commentId) {
  if (!confirm('Удалить комментарий?')) return;
  deleteComment(postId, commentId).then(() => refreshPosts()).catch(err => alert(err.message));
}

async function refreshPosts() {
  const list = document.getElementById('posts-list');
  list.innerHTML = '<div class="text-center py-4"><span class="loading-spinner me-2"></span>Загрузка...</div>';
  try {
    const posts = await loadPosts();
    list.innerHTML = '';
    if (posts.length === 0) {
      list.innerHTML = '<div class="empty-state"><i class="bi bi-journal-plus display-4 d-block mb-2"></i>Пока нет постов. Создайте первый выше.</div>';
      return;
    }
    for (const p of posts) {
      let comments = [];
      try {
        comments = await getComments(p.id);
      } catch (_) {}
      list.appendChild(renderPost(p, comments));
    }
  } catch (err) {
    list.innerHTML = '<div class="alert alert-danger d-flex align-items-center"><i class="bi bi-exclamation-triangle me-2"></i>' + escapeHtml(err.message) + '</div>';
  }
}

document.getElementById('form-new-post').addEventListener('submit', (e) => {
  e.preventDefault();
  const title = document.getElementById('new-post-title').value.trim();
  const content = document.getElementById('new-post-content').value.trim();
  const author = document.getElementById('new-post-author').value.trim();
  createPost(title, content, author)
    .then(() => {
      document.getElementById('form-new-post').reset();
      refreshPosts();
    })
    .catch(err => alert(err.message));
});

refreshPosts();
