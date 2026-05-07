import pymongo
uri = "mongodb+srv://raresnica85_db_user:mbDWJ1KXhAkWnzA5@cluster0.iemrgjk.mongodb.net/?appName=Cluster0"

try:
    client = pymongo.MongoClient(uri)

    client.admin.command('ping')
    print("Conectare reușită la MongoDB Atlas!\n")
except Exception as e:
    print("Eroare la conectare:", e)
    exit()

baza_date_noua = client["baza_de_date_din_cod"]

colectia_1 = baza_date_noua["telefoane"]
colectia_2 = baza_date_noua["accesorii"]

intrari_noi = [
    {"marca": "Samsung", "model": "Galaxy S23", "stoc": 15, "pret": 3500},
    {"marca": "Apple", "model": "iPhone 15", "stoc": 10, "pret": 4500},
    {"marca": "Google", "model": "Pixel 8", "stoc": 5, "pret": 3000}
]

rezultat = colectia_1.insert_many(intrari_noi)
print(f"Au fost adăugate {len(rezultat.inserted_ids)} intrări în colecția 'telefoane'.")

colectia_2.insert_one({"tip": "Incarcator", "putere": "20W", "pret": 100})

print("\n--- Conținutul colecției din Interfața Grafică (GUI) ---")

baza_date_gui = client["magazin"] 
colectie_gui = baza_date_gui["produse"]

documente_gui = colectie_gui.find()
for doc in documente_gui:
    print(doc)

client.close()