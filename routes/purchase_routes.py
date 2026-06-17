from uuid import uuid4

from flask import Blueprint, redirect, render_template, request, session, url_for

from database.db_config import koneksi

purchase_bp = Blueprint('purchase', __name__)


def generate_id(prefix):
    return f'{prefix}-{uuid4().hex[:10].upper()}'


def get_product(product_id):
    cursor = koneksi.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT
            product.product_id,
            product.product_name,
            product.brand,
            product.price,
            product.image_filename,
            category.category,
            sub_category.sub_category
        FROM product
        JOIN sub_category
        ON product.sub_category_id = sub_category.sub_category_id
        JOIN category
        ON sub_category.category_id = category.category_id
        WHERE product.product_id = %s
        """,
        (product_id,)
    )
    product = cursor.fetchone()
    cursor.close()
    return product


def get_current_user():
    user_id = session.get('user_id')

    if not user_id:
        return None

    cursor = koneksi.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT user_id, name, gender, rating, interaction_count
        FROM users
        WHERE user_id = %s
        """,
        (user_id,)
    )
    current_user = cursor.fetchone()
    cursor.close()

    if not current_user:
        session.pop('user_id', None)

    return current_user


@purchase_bp.route('/buy/<product_id>', methods=['GET', 'POST'])
def buy(product_id):
    product = get_product(product_id)

    if not product:
        return redirect(url_for('home'))

    current_user = get_current_user()

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        gender = request.form.get('gender', '').strip()

        if not name or not gender:
            return render_template(
                'purchase.html',
                product=product,
                current_user=current_user,
                error='Nama dan gender wajib diisi.'
            )

        user_id = session.get('user_id')

        cursor = koneksi.cursor(dictionary=True)

        if user_id:
            cursor.execute(
                """
                SELECT user_id
                FROM users
                WHERE user_id = %s
                """,
                (user_id,)
            )
            existing_user = cursor.fetchone()
        else:
            existing_user = None

        if existing_user:
            cursor.execute(
                """
                UPDATE users
                SET
                    name = %s,
                    gender = %s,
                    interaction_count = COALESCE(interaction_count, 0) + 1
                WHERE user_id = %s
                """,
                (name, gender, user_id)
            )
        else:
            user_id = generate_id('USR')
            cursor.execute(
                """
                INSERT INTO users (
                    user_id,
                    name,
                    gender,
                    rating,
                    interaction_count
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                (user_id, name, gender, None, 1)
            )
            session['user_id'] = user_id

        order_id = generate_id('ORD')
        order_item_id = generate_id('ITEM')

        cursor.execute(
            """
            INSERT INTO orders (
                order_id,
                user_id,
                order_status,
                order_date
            )
            VALUES (%s, %s, %s, NOW())
            """,
            (order_id, user_id, 'Pending')
        )

        cursor.execute(
            """
            INSERT INTO order_items (
                order_item_id,
                order_id,
                product_id,
                item_price
            )
            VALUES (%s, %s, %s, %s)
            """,
            (order_item_id, order_id, product_id, product['price'])
        )

        koneksi.commit()
        cursor.close()

        return redirect(url_for('history.history'))

    return render_template(
        'purchase.html',
        product=product,
        current_user=current_user,
        error=None
    )
