-- Q1: Todos os posts, do mais recente ao mais antigo.
SELECT *
FROM posts_post
ORDER BY published_at DESC;

-- Q2: Todos os comentarios de um post que possui comentarios (post 1).
SELECT *
FROM posts_comment
WHERE post_id = 1
ORDER BY created_at DESC;

-- Q3: Colunas de comentario (exceto post_id), titulo e data do post (post_date).
SELECT c.id, c.author_id, c.text, c.created_at,
       p.title AS post_title, p.published_at AS post_date
FROM posts_comment AS c
INNER JOIN posts_post AS p ON p.id = c.post_id
WHERE p.id = 1
ORDER BY c.created_at DESC;

-- Q4: Todas as colunas da categoria e dos posts associados (categoria 1).
SELECT cat.*, p.*
FROM posts_category AS cat
INNER JOIN posts_post_categories AS pc ON pc.category_id = cat.id
INNER JOIN posts_post AS p ON p.id = pc.post_id
WHERE cat.id = 1
ORDER BY p.published_at DESC;

-- Q5: Categorias que possuem dois ou mais posts.
SELECT cat.id, cat.name, cat.description, COUNT(DISTINCT pc.post_id) AS total_posts
FROM posts_category AS cat
INNER JOIN posts_post_categories AS pc ON pc.category_id = cat.id
GROUP BY cat.id, cat.name, cat.description
HAVING COUNT(DISTINCT pc.post_id) >= 2
ORDER BY total_posts DESC, cat.name ASC;
