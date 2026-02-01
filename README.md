# Quit‑Math Companion

Quit‑Math Companion is a production‑ready, privacy‑respecting mobile and API system that helps people quit disposable vapes and cigarettes by scheduling cognitive and motor tasks instead of nicotine.

The backend implements a continuous‑time craving model \(C(t)\), attentional capacity \(A(t)\), and reward signal \(R(t)\) using ODEs, plus a daily Markov state abstraction and reinforcement‑learning (RL) task scheduler consistent with modern cessation research.[web:1][web:6] The mobile app logs cravings and tasks, delivers adaptive drills, and visualizes abstinent days and eco‑impact from avoided disposable devices.[web:7][web:10]

## Core features

- Continuous craving engine:
  - Implements parameterized ODEs for \(C(t), A(t), R(t)\) with configurable coefficients per user profile.
  - Integrates reward pulses from completed tasks as small, decaying hits that mimic dopamine‑like reinforcement without nicotine.[web:6]
  - Exposes endpoints to simulate trajectories and derive daily averages \(\bar{C}, \bar{A}, \bar{R}\) for Markov and RL layers.[web:1]

- Markov + RL quit controller:
  - Daily states: Smoking (S0), High‑withdrawal abstinent (S1), Stable abstinent (S2), aligned with cessation Markov models.[web:1]
  - RL agent chooses task timing and difficulty to maximize expected time in S2 and reduce relapse episodes into S0.[web:1]
  - Supports both deterministic (threshold‑based) and learned (policy‑gradient) scheduling policies.

- Mobile app (React Native / Expo):
  - Craving diary (0–10 scale), task log, abstinence streak tracker, and in‑app math/motor micro‑tasks.
  - Local‑first UX with background sync to backend and gentle notifications when the controller predicts high craving.
  - Eco‑impact views showing avoided disposable vape hardware mass converted into an EcoNet‑style Karma stream.[web:7][web:10]

- EcoNet‑compatible qpudatashard:
  - Ships a ready‑to‑ingest CSV (Phoenix 2026 pilot) tracking avoided disposables, reduced plastic fraction, PM mass removal from smoke corridors, CPVM clinic incidents, and CO₂e avoided.[web:7][web:10]
  - Schema matches existing EcoNet water and air qpudatashards, including `ecoimpactscore` and `karmaperunit` fields.

## Tech stack

- Backend:
  - Python 3.11, FastAPI, SQLAlchemy, PostgreSQL.
  - RL and ODE integration via NumPy and SciPy.
  - JWT‑based authentication, pydantic schemas, typed services, and pytest test suite.

- Mobile:
  - React Native with Expo and TypeScript.
  - Redux Toolkit for state management, Axios for API, theming via styled components.

## Quick start

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
uvicorn quitmath_backend.main:app --reload
The API will start on http://127.0.0.1:8000, serving OpenAPI docs at /docs.

Mobile app
bash
cd mobile/QuitMathApp
npm install
npm run start
Use the Expo client on your device or an emulator to open the app and configure the API base URL in .env.

qpudatashard
The eco‑impact CSV for the Phoenix 2026 pilot is stored at:

text
qpudatashards/particles/QuitAidAirEcoPhoenix2026v1.csv
It is directly compatible with EcoNet / CEIM ingestion pipelines.

License
MIT License – see LICENSE.
