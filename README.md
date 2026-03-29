# MTIT_Group_290

# 🏥 Hospital Management Microservices System

## 📌 Overview

This project implements a **Hospital Management System** using **Microservices Architecture**.

Each service is independent and connected through an **API Gateway (Nginx)**.

---

## 🏗️ Services

* Patient Service → Manage patients
* Doctor Service → Manage doctors
* Appointment Service → Manage appointments
* Billing Service → Manage billing

---

## 📂 Project Structure

```
MTIT_Group_290/
│
├── patient-service/
├── doctor-service/
├── appointment-service/
├── billing-service/
├── nginx/
│   └── nginx.conf
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 👥 Team Workflow

Each member must:

1. Clone the repository
2. Create a branch for their service
3. Work only on your service
4. Push changes and create a Pull Request

---

## 🔁 Git Workflow

### Clone repo

```
git clone <repo-url>
cd MTIT_Group_290
```

### Create your branch

```
git checkout -b feature/<service-name>
```

Example:

* feature/patient-service
* feature/doctor-service
* feature/appointment-service
* feature/billing-service

---

### Push your branch

```
git add .
git commit -m "Implemented <service-name>"
git push origin feature/<service-name>
```

Then create a Pull Request to `main`.

---

## ⚙️ Setup Instructions

### 1. Create virtual environment

```
python -m venv .venv
```

Activate (Windows):

```
.venv\Scripts\activate
```

---

### 2. Install dependencies

```
pip install -r requirements.txt
```

---

### 3. Create `.env` file (inside each service)

```
MONGO_URL=mongodb+srv://<username>:<password>@cluster.mongodb.net/hospital_db
```



## ▶️ Run Services

Open **4 terminals**

### Patient Service

```
cd patient-service
uvicorn app.main:app --reload --port 8001
```

### Doctor Service

```
cd doctor-service
uvicorn app.main:app --reload --port 8002
```

### Appointment Service

```
cd appointment-service
uvicorn app.main:app --reload --port 8003
```

### Billing Service

```
cd billing-service
uvicorn app.main:app --reload --port 8004
```

---

## 🌐 API Gateway (Nginx)

### 1. Download Nginx

Download from:
👉 https://nginx.org/en/download.html

---

### 2. Setup Nginx

* Extract Nginx
* Go to `conf/nginx.conf`
* Replace with the provided file in:

```
nginx/nginx.conf
```

---

### 3. Run Nginx

```
cd C:\nginx
start nginx
```

---

## 🔗 Access APIs

Use ONLY:

```
http://localhost:8080
```

Swagger endpoints:

* http://localhost:8080/patients/docs
* http://localhost:8080/doctors/docs
* http://localhost:8080/appointments/docs
* http://localhost:8080/bills/docs

---

## 🧪 Testing Order

1. Create Patients
2. Create Doctors
3. Create Appointments
4. Create Bills
