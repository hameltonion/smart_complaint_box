# Smart Complaint Box 📨  
*A machine learning powered complaint management system for smart routing and tracking*  

![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)  
![Flask](https://img.shields.io/badge/flask-2.x-lightgrey.svg)  
![SQLite](https://img.shields.io/badge/database-SQLite-green.svg)  
![License](https://img.shields.io/badge/license-MIT-orange.svg)  

---

## 🚀 Features  
- 📝 Submit complaints via a simple text form  
- 🤖 **ML-powered classification** (Category, Subcategory, Urgency)  
- 📧 Automatic routing to departments with escalation support  
- 🔍 Track complaints by unique ID  
- 📊 **Admin dashboard** with key-based access  
- 🗄 Database-backed complaint history & status logs  
- 🧩 Modular architecture (Backend, Frontend, ML Models, Configs)  

---

## 📸 Screenshots  

### User Interface  
![Submit Complaint](docs/preview/index.jpg)  
![Track Complaint](docs/preview/track.jpg)  

### Admin Dashboard  
![Admin Panel](docs/preview/admin.jpg)  

---

## 🏗 Architecture Diagram  

![System Architecture](docs/preview/architecture.png)  

---

## 📂 Project Structure 
```
smart_complaint_box/
│
├── backend/ # Backend logic
│ ├── blueprints/ # Flask Blueprints
│ │ ├── admin.py # Admin routes (dashboard, keys)
│ │ └── user.py # User routes (submit, track)
│ ├── classifier.py # Loads ML models, runs predictions
│ ├── email_sender.py # Sends complaint emails
│ ├── router.py # Complaint → department mapping
│ └── storage.py # Database interactions (CRUD)
│
├── config/ # Config files
│ └── routing.json # Category + Subcategory → Department mapping
│
├── database/ # Database integration
│ ├── models.py # SQLAlchemy models (Complaint, StatusLog)
│ ├── schema.sql # DB schema (tables + fields)
│ └── smart_complaint_box.db # Local SQLite DB (ignored in Git)
│
├── docs/ # Documentation
│ ├── project_tree.txt # Project structure reference
│ └── preview/ # Screenshots & diagrams for README
│ ├── index.jpg
│ ├── track.jpg
│ ├── admin.jpg
│ └── architecture.png
│
├── frontend/ # User & Admin UI
│ ├── index.html # Complaint submission form
│ ├── track.html # Complaint tracking page
│ └── admin.html # Admin dashboard
│
├── ml_models/ # ML training + models
│ ├── dataset/complaints.csv # Training dataset
│ ├── trained_data/ # Saved models
│ │ ├── category_model.pkl
│ │ ├── urgency_model.pkl
│ │ └── subcategory_models/ # Per-category models
│ │ ├── subcategory_water.pkl
│ │ ├── subcategory_electricity.pkl
│ │ ├── subcategory_sanitation.pkl
│ │ └── subcategory_road.pkl
│ └── trainall.py # Script to train/retrain models
│
├── main.py # Application entrypoint
├── paths.py # Centralized path configs
├── requirements.txt # Python dependencies
└── README.md # Project documentation
```


---

## 🗄 Database Schema  

### `Complaint`  
| Field        | Type      | Description                                      |
|--------------|-----------|--------------------------------------------------|
| complaint_id | String    | Unique ID for each complaint                     |
| user_input   | Text      | Original complaint text                          |
| category     | String    | Predicted category (Water, Road, etc.)           |
| subcategory  | String    | Predicted subcategory (Leakage, Potholes, etc.)  |
| urgency      | String    | Predicted urgency (High, Medium, Low)            |
| status       | String    | Complaint status (Pending/Resolved)              |
| assigned_to  | String    | Department email assigned                        |
| created_at   | DateTime  | Timestamp when complaint was created             |
| updated_at   | DateTime  | Last update timestamp                            |

### `StatusLog`  
| Field        | Type      | Description                        |
|--------------|-----------|------------------------------------|
| id           | Integer   | Auto-increment primary key         |
| complaint_id | String    | Complaint ID (foreign key)         |
| status       | String    | Status at that moment              |
| assigned_to  | String    | Handler or department email        |
| timestamp    | DateTime  | When the change was logged         |

---

## ⚙️ Setup & Installation  

1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/smart_complaint_box.git
   cd smart_complaint_box

2. **Create a virtual environment & install dependencies**
  ```bash
    python -m venv venv
    source venv/bin/activate   # Linux/Mac
    venv\Scripts\activate      # Windows

    pip install -r requirements.txt
  ```

3. **Configure environment variables**
  ```bash
    cp .env.example .env
    # Fill in required values (e.g., email credentials, DB settings)
```
4. **Run the application**

```bash
    python main.py
```
---

## 🔮 Future Improvements
- 🔑 User authentication with role-based access (User/Admin)
- 🎨 Centralized CSS/JS styling for frontend
- 📜 Enhanced logging & monitoring
- 🐳 Deployment support (Docker)
- 📲 Push notifications (SMS/WhatsApp/Email updates)
- 🌍 Automatic geolocation tagging (fetch location with user permission for map-based tracking)
- 🕵️ Anonymous complaints (allow users to submit issues without revealing identity)

---
