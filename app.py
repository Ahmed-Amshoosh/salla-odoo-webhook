from flask import Flask, render_template_string
import xmlrpc.client

app = Flask(__name__)

url = "https://azmparts.odoo.com"
db = "azmparts"
username = "amshoosh2@gmail.com"
password = "772913602"

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common", allow_none=True)
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object", allow_none=True)

uid = common.authenticate(db, username, password, {})

BASE_URL = "https://azmparts.odoo.com"

@app.route("/")
def home():

    fields = [
        "id",
        "name",
        "default_code",
        "list_price",
    ]

    products = models.execute_kw(
        db, uid, password,
        "product.template",
        "search_read",
        [[]],
        {"fields": fields, "limit": 20}
    )

    # نضيف رابط الصورة لكل منتج
    for p in products:
        p["image_url"] = f"{BASE_URL}/web/image/product.template/{p['id']}/image_1920"

    html = """
    <h1>Products with Images</h1>

    {% for p in products %}
        <div style="margin-bottom:20px">
            <img src="{{p.image_url}}" width="120"><br>
            <b>{{p.name}}</b><br>
            SKU: {{p.default_code}}<br>
            Price: {{p.list_price}}
        </div>
    {% endfor %}
    """

    return render_template_string(html, products=products)


@app.route("/webhook", methods=["POST"])
def webhook():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)