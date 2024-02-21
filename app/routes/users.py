from flask import Blueprint, render_template, request, jsonify
from app import db
from app.models import User
from app.validation.roles import admin_required

users = Blueprint('users', __name__)


@users.route('/users')
@admin_required
def users_list():
    page = request.args.get('page', 1, type=int)
    all_users = User.query.paginate(page=page, per_page=10, error_out=False)
    return render_template('users.html', users=all_users.items, pagination=all_users)

@users.route('/add-user', methods=['POST'])
@admin_required
def add_user():
    username = request.form['username']
    email = request.form['email']
    role_id = request.form['role_id']
    password_hash = request.form['password_hash']
    new_user = User(username=username, email=email, password_hash=password_hash, role_id=role_id)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"success": True, "message": "User added successfully"})


@users.route('/delete-user/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    found_user = User.query.get(user_id)
    if found_user:
        db.session.delete(found_user)
        db.session.commit()
        return jsonify({'success': True, 'message': 'User has been deleted.'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404


@users.route('/update-user/<int:user_id>', methods=['POST'])
@admin_required
def update_user(user_id):
    found_user = User.query.get(user_id)
    if found_user:
        found_user.username = request.form['username']
        found_user.email = request.form['email']
        found_user.role_id = request.form['role_id']

        db.session.commit()
        return jsonify({'success': True, 'message': 'User has been updated.'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404
