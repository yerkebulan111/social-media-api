# SocialMediaAPI

A RESTful social media backend built with **FastAPI**, **SQLModel**, and **PostgreSQL**.

## Features

- **Auth** — Register & Login with JWT Bearer tokens
- **Posts** — Create, read, update, delete (author-only for mutations)
- **Comments** — Per-post comment threads (author-only for mutations)
- **Likes** — Toggle like/unlike on posts
- **Follows** — Follow/unfollow users; view followers & following lists

## Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| ORM / Models | SQLModel (Pydantic v2 + SQLAlchemy) |
| Database | PostgreSQL |
| Auth | JWT via `python-jose`, passwords via `passlib[bcrypt]` |
| Config | `pydantic-settings` |

## Project Structure

```
app/
├── core/
│   ├── __init__.py
│   └── security.py        # JWT + password hashing
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── post.py
│   ├── comment.py
│   ├── like.py
│   └── follow.py
├── repository/            # DB queries (pure data access)
│   ├── __init__.py
│   ├── user.py
│   ├── post.py
│   ├── comment.py
│   ├── like.py
│   └── follow.py
├── services/              # Business logic + HTTP errors
│   ├── __init__.py
│   ├── user.py
│   ├── post.py
│   ├── comment.py
│   ├── like.py
│   └── follow.py
├── routers/               # Route definitions
│   ├── __init__.py
│   ├── user.py
│   ├── post.py
│   ├── comment.py
│   ├── like.py
│   └── follow.py
├── __init__.py
├── config.py
├── database.py
└── main.py
```

## Setup

```bash
# 1. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your PostgreSQL credentials and a strong SECRET_KEY

# 4. Run
uvicorn app.main:app --reload
```

## API Endpoints

### Auth / Users — `/users`
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/users/register` | No   | Register new user |
| POST | `/users/login` | No   | Login, receive JWT token |
| GET | `/users/me` | Yes  | Get your profile |
| PATCH | `/users/me` | Yes  | Update your profile |
| DELETE | `/users/me` | Yes  | Delete your account |
| GET | `/users/{id}` | No   | Get any user profile |

### Posts — `/posts`
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/posts` | No   | List posts (pagination: `?skip=0&limit=20`) |
| GET | `/posts/{id}` | No   | Get single post |
| POST | `/posts` | Yes  | Create post |
| PATCH | `/posts/{id}` | Yes  | Update own post |
| DELETE | `/posts/{id}` | Yes  | Delete own post |

### Comments — `/comments`
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/comments/post/{post_id}` | No   | Get comments for a post |
| POST | `/comments/post/{post_id}` | Yes  | Add comment to a post |
| PATCH | `/comments/{id}` | Yes  | Edit own comment |
| DELETE | `/comments/{id}` | Yes  | Delete own comment |

### Likes — `/likes`
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/likes/post/{post_id}` | Yes  | Toggle like/unlike |

### Follows — `/follows`
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/follows/{user_id}` | Yes  | Toggle follow/unfollow |
| GET | `/follows/{user_id}/following` | No   | Who this user follows |
| GET | `/follows/{user_id}/followers` | No   | Who follows this user |

## Interactive Docs

Visit `http://localhost:8000/docs` for Swagger UI with full API documentation.