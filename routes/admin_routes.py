import os
from uuid import uuid4

from flask import Blueprint, current_app, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename

from database.db_config import koneksi

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


@admin_bp.before_request
def require_admin():
    if request.endpoint in ('admin.login', 'admin.logout'):
        return

    if not session.get('is_admin'):
        return redirect(url_for('admin.login'))


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('is_admin'):
        return redirect(url_for('admin.product_list'))

    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['is_admin'] = True
            return redirect(url_for('admin.product_list'))

        error = 'Username atau password salah.'

    return render_template('admin_login.html', error=error)


@admin_bp.route('/logout')
def logout():
    session.pop('is_admin', None)
    return redirect(url_for('home'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_id(prefix):
    return f'{prefix}-{uuid4().hex[:10].upper()}'


def save_image(image_file):
    if not image_file or image_file.filename == '':
        return None

    if not allowed_file(image_file.filename):
        return None

    filename = secure_filename(image_file.filename)
    extension = filename.rsplit('.', 1)[1].lower()
    new_filename = f'{uuid4().hex}.{extension}'
    save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
    image_file.save(save_path)
    return new_filename


def delete_image(filename):
    if not filename:
        return

    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except OSError:
        pass


def get_sub_categories():
    cursor = koneksi.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT
            sub_category.sub_category_id,
            sub_category.sub_category,
            category.category
        FROM sub_category
        JOIN category ON sub_category.category_id = category.category_id
        ORDER BY category.category, sub_category.sub_category
        """
    )
    sub_categories = cursor.fetchall()
    cursor.close()
    return sub_categories


def get_products():
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
        LEFT JOIN sub_category ON product.sub_category_id = sub_category.sub_category_id
        LEFT JOIN category ON sub_category.category_id = category.category_id
        ORDER BY product.product_name
        """
    )
    products = cursor.fetchall()
    cursor.close()
    return products


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
            product.sub_category_id,
            category.category,
            sub_category.sub_category
        FROM product
        LEFT JOIN sub_category ON product.sub_category_id = sub_category.sub_category_id
        LEFT JOIN category ON sub_category.category_id = category.category_id
        WHERE product.product_id = %s
        """,
        (product_id,)
    )
    product = cursor.fetchone()
    cursor.close()
    return product


@admin_bp.route('/products')
def product_list():
    products = get_products()
    return render_template('admin_products.html', products=products)


@admin_bp.route('/products/new', methods=['GET', 'POST'])
def create_product():
    sub_categories = get_sub_categories()

    if request.method == 'POST':
        product_name = request.form.get('product_name', '').strip()
        brand = request.form.get('brand', '').strip()
        price = request.form.get('price', '').strip()
        sub_category_id = request.form.get('sub_category_id')
        image_file = request.files.get('image')

        if not product_name or not brand or not price or not sub_category_id:
            return render_template(
                'admin_product_form.html',
                product=None,
                sub_categories=sub_categories,
                error='Semua field wajib diisi kecuali gambar.'
            )

        try:
            price_value = float(price)
        except ValueError:
            return render_template(
                'admin_product_form.html',
                product=None,
                sub_categories=sub_categories,
                error='Harga harus berupa angka.'
            )

        image_filename = save_image(image_file)
        product_id = generate_id('PRD')

        cursor = koneksi.cursor()
        cursor.execute(
            """
            INSERT INTO product (
                product_id,
                product_name,
                brand,
                price,
                sub_category_id,
                image_filename
            ) VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (product_id, product_name, brand, price_value, sub_category_id, image_filename)
        )
        koneksi.commit()
        cursor.close()

        return redirect(url_for('admin.product_list'))

    return render_template(
        'admin_product_form.html',
        product=None,
        sub_categories=sub_categories,
        error=None
    )


@admin_bp.route('/products/<product_id>/edit', methods=['GET', 'POST'])
def edit_product(product_id):
    product = get_product(product_id)
    sub_categories = get_sub_categories()

    if not product:
        return redirect(url_for('admin.product_list'))

    if request.method == 'POST':
        product_name = request.form.get('product_name', '').strip()
        brand = request.form.get('brand', '').strip()
        price = request.form.get('price', '').strip()
        sub_category_id = request.form.get('sub_category_id')
        image_file = request.files.get('image')

        if not product_name or not brand or not price or not sub_category_id:
            return render_template(
                'admin_product_form.html',
                product=product,
                sub_categories=sub_categories,
                error='Semua field wajib diisi kecuali gambar.'
            )

        try:
            price_value = float(price)
        except ValueError:
            return render_template(
                'admin_product_form.html',
                product=product,
                sub_categories=sub_categories,
                error='Harga harus berupa angka.'
            )

        image_filename = save_image(image_file)
        if image_filename:
            delete_image(product.get('image_filename'))
        else:
            image_filename = product.get('image_filename')

        cursor = koneksi.cursor()
        cursor.execute(
            """
            UPDATE product
            SET
                product_name = %s,
                brand = %s,
                price = %s,
                sub_category_id = %s,
                image_filename = %s
            WHERE product_id = %s
            """,
            (product_name, brand, price_value, sub_category_id, image_filename, product_id)
        )
        koneksi.commit()
        cursor.close()

        return redirect(url_for('admin.product_list'))

    return render_template(
        'admin_product_form.html',
        product=product,
        sub_categories=sub_categories,
        error=None
    )


@admin_bp.route('/products/<product_id>/delete', methods=['POST'])
def delete_product(product_id):
    product = get_product(product_id)
    if product:
        delete_image(product.get('image_filename'))
        cursor = koneksi.cursor()
        cursor.execute(
            """
            DELETE FROM product
            WHERE product_id = %s
            """,
            (product_id,)
        )
        koneksi.commit()
        cursor.close()

    return redirect(url_for('admin.product_list'))
