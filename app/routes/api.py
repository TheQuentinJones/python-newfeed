from flask import Blueprint, request, jsonify, session
from app.models import User, Post, Comment, Vote
from app.db import get_db
import sys

bp = Blueprint('api', __name__, url_prefix='/api')

# Signup

@bp.route('/users', methods=['POST'])
def signup():
  data = request.get_json()
  db = get_db()

  try:
    # attempt creating a new user
    newUser = User(
      username = data['username'],
      email = data['email'],
      password = data['password']
    )

    db.add(newUser)
    db.commit()
  except:
    # insert failed, so send error to front end
    print(sys.exc_info()[0])
    # insert failed, so rollback and send error to front end
    db.rollback()
    return jsonify(message = 'Signup failed'), 500

  session.clear()
  session['user_id'] = newUser.id
  session['loggedIn'] = True

  return jsonify(id = newUser.id)

@bp.route('/users/logout', methods=['POST'])
def logout():
  # remove session variables
  session.clear()
  return '', 204

# Login

@bp.route('/users/login', methods=['POST'])
def login():
  data = request.get_json()
  db = get_db()

  try:
    user = db.query(User).filter(User.email == data['email']).one()
  except:
    print(sys.exc_info()[0])

    return jsonify(message = 'Incorrect credentials'), 400

  if user.verify_password(data['password']) == False:
    return jsonify(message = 'Incorrect credentials'), 400

  session.clear()
  session['user_id'] = user.id
  session['loggedIn'] = True

  return jsonify(id = user.id)

# Comments

@bp.route('/comments', methods=['POST'])
def comment():
  data = request.get_json()
  db = get_db()

  try:
  # create a new comment
    newComment = Comment(
      comment_text = data['comment_text'],
      post_id = data['post_id'],
      user_id = session.get('user_id')
    )

    db.add(newComment)
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Comment failed'), 500
  
  return jsonify(id = newComment.id)

# Votes

@bp.route('/posts/upvote', methods=['PUT'])
def upvote():
  data = request.get_json()
  db = get_db()

  try:
    # create a new vote with incoming id and session id
    newVote = Vote(
      post_id = data['post_id'],
      user_id = session.get('user_id')
    )

    db.add(newVote)
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Upvote failed'), 500

  return '', 204

# Creating Posts

@bp.route('/posts', methods=['POST'])
def create():
  data = request.get_json()
  db = get_db()

  try:
    # create a new post
    newPost = Post(
      title = data['title'],
      post_url = data['post_url'],
      user_id = session.get('user_id')
    )

    db.add(newPost)
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Post failed'), 500

  return jsonify(id = newPost.id)

# Update Posts

@bp.route('/posts/<id>', methods=['PUT'])
def update(id):
  data = request.get_json()
  db = get_db()

  try:
    # retrieve post and update title property
    post = db.query(Post).filter(Post.id == id).one()
    post.title = data['title']
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Post not found'), 404

  return '', 204

# Delete Posts

@bp.route('/posts/<id>', methods=['DELETE'])
def delete(id):
  db = get_db()

  try:
    # delete post from db
    db.delete(db.query(Post).filter(Post.id == id).one())
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Post not found'), 404

  return '', 204