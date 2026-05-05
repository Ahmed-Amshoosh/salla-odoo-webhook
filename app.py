from flask import Flask, render_template_string
import xmlrpc.client

app = Flask(__name__)

url = "https://azmparts.odoo.com"
db = "azmparts"
username = "amshoosh2@gmail.com"
password = "772913602"

# Odoo connection
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common", allow_none=True)
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object", allow_none=True)

uid = common.authenticate(db, username, password, {})

@app.route("/")
def home():

    if not uid:
        return "❌ Odoo Login Failed"

    fields = [
        'id',
        'name',
        'list_price',
        'default_code',
        'barcode',
        'description_sale',
        'image_1920',
        'qty_available'
    ]

    products = models.execute_kw(
        db, uid, password,
        'product.template',
        'search_read',
        [[]],
        {'fields': fields, 'limit': 50}
    )

    html = """
    <h1>Odoo Products</h1>
    <ul>
    {% for p in products %}
        <li>
            <b>{{ p.name }}</b> - {{ p.list_price }} SAR
            <br>
            SKU: {{ p.default_code }}
        </li>
    {% endfor %}
    </ul>
    """

    return render_template_string(html, products=products)


@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)