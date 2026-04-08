# mediq backend (FastAPI)

Production-ready starter backend for a hospital management platform.

## Tech
- FastAPI + Pydantic
- PostgreSQL
- SQLAlchemy ORM
- Alembic migrations
- JWT auth + role-based access control (patient/receptionist/doctor/admin)
- WebSocket chat (per appointment)

## Quick start (Windows / PowerShell)

1) Create and activate a virtualenv

```powershell
cd d:\kfiles\mediq
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2) Configure env

```powershell
copy .env.example .env
notepad .env
```

3) Create DB (example)

Create a Postgres DB named `mediq`, then set `DATABASE_URL` accordingly.

4) Run migrations

```powershell
alembic upgrade head
```

5) Run API

```powershell
uvicorn app.main:app --reload --port 8000
```

Open docs at `http://localhost:8000/docs`.

## Important endpoints
- `POST /auth/register` patient signup
- `POST /auth/login` get JWT
- `GET /auth/me` current user
- `GET /patients/me/profile` patient profile
- `POST /clinical/appointments` book appointment (auto-assign doctor if available)
- `POST /intake/drafts/from-agent-text` calling-agent transcript → structured intake draft → auto assignment
- `GET /emergency/content` public emergency guidance list
- WebSocket: `/ws/chat/{appointment_id}`

# mediq

Production-ready hospital management platform with a FastAPI backend and a Next.js frontend.

## Components

### 1) Backend (FastAPI)
Located in the root directory. Follow the instructions above to get started.

### 2) Frontend (Next.js)
Located in the `/frontend` directory.

**Features:**
- Premium UI inspired by Apollo Hospitals.
- 4-step Appointment Booking Wizard.
- Responsive design with Dark Mode support.
- Built with Next.js, Tailwind CSS, and Framer Motion.

**Quick Start:**
```powershell
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000` to view the frontend.

 flowchart TD

A[Patient / User Entry] --> B{Authentication}

B -->|New User| C[Register Account]
B -->|Existing User| D[Login]

C --> E[Create Unique Patient ID]
D --> F[Access Dashboard]

E --> F

%% Dashboard Split
F --> G[Patient Services]
F --> H[Hospital Management]
F --> I[Emergency System]

%% Patient Services
G --> G1[View / Update Profile]
G --> G2[Book Appointment]
G --> G3[View Medical Records]
G --> G4[Online Consultation Chat]
G --> G5[View Reports]

G2 --> G21[Select Doctor & Time Slot]
G21 --> G22[Confirm Appointment]
G4 --> G41[Store Chat & Consultation History]

%% Hospital Management
H --> H1[Bed Availability System]
H --> H2[Medicine Inventory]
H --> H3[Doctor Availability]
H --> H4[Ambulance Tracking]
H --> H5[Hospital Referral System]

H1 --> H11[Real-time Bed Status Update]
H2 --> H21[Track Quantity & Expiry]
H2 --> H22[Low Stock Alerts]

H3 --> H31[Assign Doctor for Hospital Visit]
H3 --> H32[Assign Doctor for Home Visit]
H3 --> H33[Assign Doctor for Remote Location]

H4 --> H41[Track Ambulance Availability]
H4 --> H42[Assign Ambulance Request]

H5 --> H51[Suggest Alternative Hospitals]

%% Emergency System
I --> I1[Access Offline Emergency Content]
I1 --> I11[Videos]
I1 --> I12[Text Instructions]
I1 --> I13[First Aid Guidance]

I --> I2[Ambulance Admission Form]

%% Ambulance Form Flow
I2 --> J[Minimal Patient Details Entry]
J --> K[Auto Draft Admission Created]

%% USP Feature
K --> L[Calling Agent Interaction]
L --> M[Speech to Text Conversion]
M --> N[Text Parsing Engine]
N --> O[Extract Patient Details]

O --> P[Structured Admission Draft]

%% Automation
P --> Q[Auto Assign Bed]
P --> R[Auto Assign Doctor]
P --> S{Availability Check}

S -->|Available| T[Confirm Admission]
S -->|Not Available| U[Suggest Referral Hospital]

%% Reports
F --> V[Report Generation System]
V --> V1[Generate PDF Reports]
V --> V2[Store & Retrieve Reports]

T --> W[Patient Admitted Successfully]
U --> W
