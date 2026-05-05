import xmlrpc.client

url = "https://azmparts.odoo.com/odoo"
db = "azmparts"
username = "amshoosh2@gmail.com"
password = "772913602"

# login
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})

models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

# جلب المنتجات
products = models.execute_kw(
    db, uid, password,
    'product.template',
    'search_read',
    [[['sale_ok', '=', True]]],
    {'fields': ['id', 'name', 'list_price'], 'limit': 10}
)

print(products)