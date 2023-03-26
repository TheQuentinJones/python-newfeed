from flask import Blueprint, render_template, session
from app.models import Post
from app.db import get_db

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/')
def dash():

  db = get_db()
  posts = (
  db.query(Post)
  .filter(Post.user_id == session.get('user_id'))
  .order_by(Post.created_at.desc())
  .all()
  )

  return render_template(
  'dashboard.html',
  posts=posts,
  loggedIn=session.get('loggedIn')
  )

@bp.route('/edit/<id>')
def edit(id):
  # get single post by id
  db = get_db()
  post = db.query(Post).filter(Post.id == id).one()

  # render edit page
  return render_template(
    'edit-post.html',
    post=post,
    loggedIn=session.get('loggedIn')
  )