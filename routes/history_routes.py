from flask import Blueprint, redirect, render_template, request, session, url_for

from database.db_config import koneksi

history_bp = Blueprint('history', __name__)


def execute_user_order_update(order_id, allowed_statuses, next_status):
    user_id = session.get('user_id')

    if not user_id:
        return False

    cursor = koneksi.cursor()
    cursor.execute(
        """
        UPDATE orders
        SET order_status = %s
        WHERE order_id = %s
        AND user_id = %s
        AND order_status IN ({})
        """.format(','.join(['%s'] * len(allowed_statuses))),
        (next_status, order_id, user_id, *allowed_statuses)
    )
    koneksi.commit()
    updated = cursor.rowcount > 0
    cursor.close()

    return updated


@history_bp.route('/history')
def history():
    user_id = session.get('user_id')
    current_user = None
    histories = []

    if user_id:
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

        if current_user:
            cursor.execute(
                """
                SELECT
                    orders.order_id,
                    orders.order_status,
                    orders.order_date,
                    users.name,
                    product.product_name,
                    product.brand,
                    order_items.item_price

                FROM orders

                JOIN users
                ON orders.user_id = users.user_id

                JOIN order_items
                ON orders.order_id = order_items.order_id

                JOIN product
                ON order_items.product_id = product.product_id

                WHERE orders.user_id = %s

                ORDER BY orders.order_date DESC
                """,
                (user_id,)
            )
            histories = cursor.fetchall()
        else:
            session.pop('user_id', None)

        cursor.close()

    return render_template(
        'history.html',
        current_user=current_user,
        histories=histories
    )


@history_bp.route('/history/cancel/<order_id>', methods=['POST'])
def cancel_order(order_id):
    execute_user_order_update(order_id, ['Pending'], 'Canceled')

    return redirect(url_for('history.history'))


@history_bp.route('/history/received/<order_id>', methods=['POST'])
def received_order(order_id):
    execute_user_order_update(order_id, ['Pending'], 'Delivered')

    return redirect(url_for('history.history'))


@history_bp.route('/history/rate/<order_id>', methods=['POST'])
def rate_order(order_id):
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('history.history'))

    try:
        rating = float(request.form.get('rating', '0'))
    except ValueError:
        rating = 0

    rating = max(1, min(rating, 5))

    cursor = koneksi.cursor()
    cursor.execute(
        """
        UPDATE users
        JOIN orders
        ON users.user_id = orders.user_id
        SET
            users.rating = %s,
            orders.order_status = %s
        WHERE orders.order_id = %s
        AND orders.user_id = %s
        AND orders.order_status = %s
        """,
        (rating, 'Rated', order_id, user_id, 'Delivered')
    )
    koneksi.commit()
    cursor.close()

    return redirect(url_for('history.history'))
