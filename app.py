from flask import Flask, render_template_string
import xmlrpc.client

app = Flask(__name__)

# Odoo connection
url = "https://azmparts.odoo.com/odoo"
db = "azmparts"
username = "amshoosh2@gmail.com"
password = "772913602"

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, None)

models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")


@app.route('/')
def home():

    # جلب المنتجات
    products = models.execute_kw(
        db, uid, password,
        'product.template',
        'search_read',
        [[['sale_ok', '=', True]]],
        {'fields': ['id', 'name', 'list_price'], 'limit': 20}
    )

    # HTML بسيط لعرض البيانات
    html = """
    <h1>📦 Odoo Products</h1>
    <table border="1" cellpadding="10">
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Price</th>
        </tr>
    """

    for p in products:
        html += f"""
        <tr>
            <td>{p['id']}</td>
            <td>{p['name']}</td>
            <td>{p['list_price']}</td>
        </tr>
        """

    html += "</table>"

    return render_template_string(html)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)