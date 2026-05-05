from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(silent=True)

    # fallback لو JSON فشل
    if not data:
        data = request.form.to_dict()

    print("🔥 RAW WEBHOOK DATA:")
    print(data)

    event = data.get("event")

    if event == "product.created":
        product = data.get("data", {})

        print("📦 New Product Received")
        print("Name:", product.get("name"))
        print("SKU:", product.get("sku"))
        
        price = product.get("price", {})
        if isinstance(price, dict):
            print("Price:", price.get("amount"))
        else:
            print("Price:", price)

    return jsonify({"status": "ok"}), 200


@app.route('/')
def home():
    return "Salla-Odoo Server Running 🚀"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)