# TasteOfShekhawati - Single Store E-commerce website

TasteOfShekhawati is a single-store e-commerce website focused on selling authentic traditional products from the Shekhawati region of Rajasthan — such as Ker Sangri, Papad, Mangodi, snacks, sweets, spices, and more.

<img width="1889" height="910" alt="image" src="https://github.com/user-attachments/assets/71497e22-2f6c-4635-992f-77818ac1b6c7" />

---
## ✅ What the Website Does
- 🛍️ Shows a list of traditional Shekhawati food products
- ➕ Add items to shopping cart
- ✅ Checkout with saved address
- 👤 User signup, login & profile
- 📦 Order history tracking
- ⭐ Product reviews
- 📩 Contact form for inquiries

---

## ✅ Tech Stack
| Component | Technology |
|-----------|------------|
| Backend | Django, REST Framework |
| Database | PostgreSQL |
| Frontend | HTML, CSS, JavaScript |
| Auth | Token / Session (DRF) |
| Media Storage | Django media files |

---

## ✅ Project Structure
<pre>
TasteOfShekhawati/
├── 📁 backend
│   ├── 📁 api
│   │   ├── 🗂 migrations/
│   │   ├── 📄 admin.py
│   │   ├── 📄 models.py
│   │   ├── 📄 serializers.py
│   │   ├── 📄 urls.py
│   │   └── 📄 views.py
│   ├── 📁 Ecom
│   │   ├── 🗂 images/
│   │   ├── 📄 settings.py
│   │   ├── 📄 urls.py
│   │   ├── 📄 views.py
│   │   └── 📄 wsgi.py
│   ├── 📁 media
│   └── 📄 manage.py
│
├── 📁 frontend
│   ├── 🧾 home.html
│   ├── 🧾 product.html
│   ├── 🧾 cart.html
│   ├── 🧾 login.html
│   ├── 🧾 signup.html
│   └── 🧾 orders.html
│
├── 📄 .env
├── 📄 requirements.txt
└── 📄 README.md
</pre>
---

## ✅ API Endpoints Used
| Endpoint | Purpose |
|----------|---------|
| `/Product/` | Get product list, single product details |
| `/Cart/` | Add/remove/update cart items |
| `/Address/` | Save user delivery addresses |
| `/orders/` | View user order history |
| `/Review/` | Product reviews |
| `/ContactForm/` | User messages |
| `/signup/` | Create new account |
| `/login/` | Login user |
| `/profile/` | View profile |

---

## ✅ Installation & Setup

### 1️⃣ Clone Project
    git clone https://github.com/Akshatswami610/TasteOfShekhawati.git
    cd TasteOfShekhawati
### 2️⃣ Create Virtual Environment
    python -m venv env
    source env/bin/activate      # Linux/Mac
    env\Scripts\activate         # Windows
### 3️⃣ Install Dependencies
    pip install -r requirements.txt
### 4️⃣ Setup Environment (.env)
    SECRET_KEY=your_secret_key
    DEBUG=True
    DB_NAME=postgres
    DB_USER=postgres
    DB_PASSWORD=yourpassword
    DB_HOST=localhost
    DB_PORT=5432
### 5️⃣ Apply Migrations
    python backend/manage.py makemigrations
    python backend/manage.py migrate
    python backend/manage.py createsuperuser
### 6️⃣ Run Server
    python backend/manage.py runserver
    
### ✅ Frontend Usage
    
    // Fetch product list from API
    fetch("http://localhost:8000/api/v1/Product/", {
      method: "GET",
      headers: {
        "Content-Type": "application/json"
      }
    })
      .then(response => response.json())
      .then(data => console.log("Products:", data))
      .catch(error => console.error("Error loading products:", error));

---

## ✅ Future Enhancements
- Online payment gateway (Razorpay / UPI)
- Order tracking
- Discount coupons
- Delivery partner integration
- Deploy to AWS / Render / Railway
---

## 🤝 Contributing

Pull requests are welcome! If you have ideas for new features or improvements, feel free to open an issue or submit a PR.

---

## 📄 License

This project is **open-source**. You are free to use, modify, and share it.
