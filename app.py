from flask import Flask, render_template_string
import xmlrpc.client

app = Flask(__name__)

url = "https://azmparts.odoo.com"
db = "azmparts"
username = "amshoosh2@gmail.com"
password = "YOUR_API_KEY"

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common", allow_none=True)
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

uid = common.authenticate(db, username, password, {})

@app.route("/")
def home():

    products = models.execute_kw(
        db, uid, password,
        "product.template",
        "search_read",
        [[["sale_ok", "=", True]]],
        {"fields": ["id", "name", "list_price"], "limit": 20}
    )

    html = """
    <h1>Odoo Products</h1>
    <ul>
    {% for p in products %}
        <li>{{p.name}} - {{p.list_price}}</li>
    {% endfor %}
    </ul>
    """

    return render_template_string(html, products=products)


@app.route("/webhook", methods=["POST"])
def webhook():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)