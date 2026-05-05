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

@app.route("/")
def home():

    fields = [
        "id",
        "name",
        "default_code",
        "list_price",
        "image_1920"
    ]

    products = models.execute_kw(
        db, uid, password,
        "product.template",
        "search_read",
        [[]],
        {"fields": fields, "limit": 20}
    )

    # نحول الصورة إلى رابط سلة تفهمه
    for p in products:
        if p.get("image_1920"):
            p["image_url"] = f"{url}/web/image/product.template/{p['id']}/image_1920"
        else:
            p["image_url"] = ""

    html = """
    <h1>Products</h1>

    {% for p in products %}
        <div style="margin-bottom:20px">
            <h3>{{p.name}}</h3>
            <p>SKU: {{p.default_code}}</p>
            <p>Price: {{p.list_price}}</p>

            {% if p.image_url %}
                <img src="{{p.image_url}}" width="120"/>
            {% endif %}
        </div>
    {% endfor %}
    """

    return render_template_string(html, products=products)


@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)