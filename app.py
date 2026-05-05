from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    if data.get("event") == "product.created":

        product = data["data"]

        print("📦 New Product Received")
        print("Name:", product["name"])
        print("SKU:", product["sku"])
        print("Price:", product["price"]["amount"])

        # هنا لاحقًا نرسله إلى Odoo
        # send_to_odoo(product)

    return jsonify({"status": "ok"})

@app.route('/')
def home():
    return "Salla-Odoo Server Running 🚀"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)