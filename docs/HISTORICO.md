# Histórico exigido no enunciado

- Commit inicial: projeto Django e modelo `Post`.
- `CRUD v1`: funções sem Django Form e sem validação de campos, com confirmação de exclusão.
- `CRUD v2`: funções e `PostForm` (ModelForm).
- `CRUD v3`: ListView, DetailView, CreateView, UpdateView, DeleteView.
- Branch `comments` a partir da `main`: `Comment`, ForeignKey para AUTH_USER_MODEL, criação e ordenação; merge na main.
- Branch `categories` criada após o merge de comments: `Category`, ManyToMany, listagens, links; merge na main.

Os conteúdos exatos das versões de views podem ser extraídos com:

```bash
git log --oneline --graph --all
git show b8e94ae:posts/views.py
git show 0d4ac5e:posts/views.py
git show cf23978:posts/views.py
```

Para conferir branches: `git branch -a`.
