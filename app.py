from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    
    # لو GET (فتح من المتصفح)
    if request.method == 'GET':
        return "Webhook is working ✅ (Send POST from Salla)", 200

    # لو POST (هذا المهم من سلة)
    data = request.get_json(silent=True)

    if not data:
        data = request.form.to_dict()

    print("🔥 RAW WEBHOOK DATA:")
    print(data)

    event = data.get("event")

    # 🔑 أهم حدث بالبداية (عشان تاخذ access_token)
    if event == "app.store.authorize":
        token = data.get("data", {}).get("access_token")
        print("🔐 ACCESS TOKEN:", token)

    # 📦 عند إنشاء منتج
    elif event == "product.created":
        product = data.get("data", {})

        print("📦 New Product Received")
        print("Name:", product.get("name"))
        print("SKU:", product.get("sku"))

        price = product.get("price", {})
        if isinstance(price, dict):
            print("Price:", price.get("amount"))
        else:
            print("Price:", price)

    else:
        print("⚠️ Event not handled:", event)

    return jsonify({"status": "ok"}), 200


@app.route('/')
def home():
    return "Salla-Odoo Server Running 🚀"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)