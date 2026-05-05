from flask import Flask, render_template_string
import xmlrpc.client
import base64

app = Flask(__name__)

url = "https://azmparts.odoo.com"
db = "azmparts"
username = "amshoosh2@gmail.com"
password = "772913602"

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common", allow_none=True)
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object", allow_none=True)

uid = common.authenticate(db, username, password, {})

@app.route("/")
def home():

    fields = [
        "id",
        "name",
        "default_code",
        "barcode",
        "list_price",
        "description_sale",
        "image_1920",
        "categ_id"
    ]

    products = models.execute_kw(
        db, uid, password,
        "product.template",
        "search_read",
        [[]],
        {"fields": fields, "limit": 20}
    )

    html = """
    <h1>Products from Odoo</h1>
    <ul>
    {% for p in products %}
        <li>
            <b>{{p.name}}</b><br>
            SKU: {{p.default_code}}<br>
            Price: {{p.list_price}}
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