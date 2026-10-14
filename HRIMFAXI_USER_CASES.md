# Hrimfaxi (Car Agent) — User Cases & Scenarios

> **Status:** Working catalog of user scenarios for Heimdall's vehicle domain agent (**Hrimfaxi**).  
> **Reference:** [CAR_AGENT.md](./CAR_AGENT.md), [REQUIREMENTS.md](./REQUIREMENTS.md), [PROGRESS.md](./PROGRESS.md).  
> **Key Principle:** A note or observation never gets lost. Hrimfaxi turns it into a managed work item or reference record and drives it toward a clear, verified outcome under strict Human-in-the-Loop guardrails.

---

## Catalog Overview

| ID | Group | Scenario Title | Primary Trigger | Primary Module Dependencies |
| :--- | :--- | :--- | :--- | :--- |
| **UC-01** | Incidents & Faults | Unstructured Fault Report («Скрипят тормоза») | Voice/Text message | Tasks, Scheduler, Memory |
| **UC-02** | Incidents & Faults | Warning Light / OBD-II Error («Горит Check Engine») | Photo / Error code | Tasks, Knowledge Base |
| **UC-03** | Ingestion & OCR | Service Invoice Ingestion (Заказ-наряд из сервиса) | Photo / PDF Invoice | Documents/OCR, Budget, Tasks |
| **UC-04** | Ingestion & OCR | Fuel / Charging Receipt (Чек с заправки/зарядки) | Photo / App receipt | Budget, Analytics |
| **UC-05** | Ingestion & OCR | Insurance & Technical Inspection (Страховка / TÜV) | PDF Document | Scheduler, Tasks |
| **UC-06** | Maintenance & Deadlines | Proactive Service Interval (Приближение ТО) | Time / Extrapolated Mileage | Scheduler, Tasks, Notifications |
| **UC-07** | Maintenance & Deadlines | Seasonal Tire Swap (Сезонная смена резины) | Calendar / Weather trigger | Scheduler, Tasks |
| **UC-08** | Parts & Purchasing | Part Research & Price Comparison (Подбор колодок) | Text command / Incident | Research, Shopping, Approval |
| **UC-09** | TCO & Lifecycle | Total Cost of Ownership (Реальная стоимость владения) | User query / Monthly cron | Budget, Analytics |
| **UC-10** | TCO & Lifecycle | Digital Service Passport (Сервисная книжка для продажи)| User export request | Documents, MaintenanceLog |

---

## Group 1: Incidents & Fault Management (Observations → Outcomes)

### UC-01: Unstructured Fault Report («Скрипят тормоза») — *MVP Vertical Slice 01*
* **Trigger:** Spontaneous voice or text message: *«Прямо сейчас как раз скрипят тормоза»*.
* **Goal:** Acknowledge the safety concern, link to vehicle context, register a managed task, and follow up until resolved.
* **Agent Behavior:**
  1. **Classify:** Parses intent as `report_vehicle_fault`, extracts `subsystem: brakes`, `symptom: squeak`.
  2. **Enrich:** Fetches active `VehicleProfile` and checks `MaintenanceLog` (e.g., *«Front pads replaced 38,000 km ago»*).
  3. **Respond & Clarify:** Confirms receipt without pseudo-diagnosis, highlights maintenance context, and asks at most one concise question:
     > *«Зафиксировал инцидент по тормозной системе для вашего авто. Создал задачу на диагностику (по истории передние колодки менялись 38 000 км назад — возможен естественный износ).*  
     > *Напомнить вам о записи в сервис через пару дней или сразу подобрать варианты колодок?»*
  4. **State Change:** Inserts record in `incidents` (`status: active_tracking`, `severity: high`) and in `tasks` (`status: pending_action`).
  5. **Proactive Follow-up:** Scheduler registers a reminder for 48 hours later. If the user hasn't booked service, Hrimfaxi sends a gentle ping.
  6. **Closing:** The incident moves to `resolved` only after an invoice is uploaded or the user explicitly confirms the repair.

### UC-02: Warning Light / Diagnostic Code («Загорелся Check Engine»)
* **Trigger:** Photo of the dashboard instrument cluster or typed OBD-II code (e.g., `P0420`).
* **Goal:** Assess immediate urgency (safe to drive or stop engine immediately), explain the indicator, and log a diagnostic work item.
* **Agent Behavior:**
  1. OCR/Vision recognizes the indicator symbol and color (Red = stop safely; Yellow = drive to nearest service).
  2. References the specific vehicle user manual stored in knowledge memory.
  3. Provides an immediate checklist (check oil level, coolant temperature, fuel cap).
  4. Creates an incident ticket linked to recommended service actions.

---

## Group 2: Document & Invoice Ingestion (OCR & Enrichment)

### UC-03: Service Invoice Ingestion (Заказ-наряд из сервиса)
* **Trigger:** Photo or PDF scan of a garage invoice/work order.
* **Goal:** Extract facts, update vehicle mileage and history, log costs, and turn mechanic recommendations into future tasks.
* **Agent Behavior:**
  1. Submits document to `Documents/OCR` module.
  2. Extracts: Date, current mileage, garage name, itemized parts, labor items, VAT, and total sum.
  3. Matches VIN or license plate on invoice with `VehicleProfile`.
  4. Presents a structured draft for user confirmation.
  5. On approval:
     - Updates `VehicleProfile.current_mileage`.
     - Inserts entry into `MaintenanceLog`.
     - Emits `VehicleExpenseCreated` to `Budget`.
     - Scans text for recommendations (e.g., *«Рекомендация: остаток задних колодок 20%»*) $\rightarrow$ automatically proposes a future reminder.

### UC-04: Fuel & Charging Receipts (Чеки заправки / зарядки)
* **Trigger:** Photo of gas station receipt or EV charging session screenshot.
* **Goal:** Log fuel/energy costs and refine average mileage and consumption calculations.
* **Agent Behavior:**
  1. Extracts amount, volume (liters/kWh), price per unit, and fuel grade.
  2. If accompanied by odometer photo/text, computes consumption since last full tank ($L/100\text{km}$ or $kWh/100\text{km}$).
  3. Records expense in vehicle budget under `fuel_or_charging`.

### UC-05: Insurance & Technical Inspection (Страховка и ТО/TÜV)
* **Trigger:** PDF of OSAGO/KASKO policy or inspection report (TÜV / MOT).
* **Goal:** Keep emergency helpline numbers accessible and guarantee timely renewal reminders.
* **Agent Behavior:**
  1. Extracts policy number, validity dates, road assistance phone numbers.
  2. Registers calendar deadlines: 30 days and 7 days prior to expiration.
  3. Provides quick emergency lookup: *«Hrimfaxi, номер эвакуатора по страховке»* $\rightarrow$ returns phone and policy number instantly.

---

## Group 3: Proactive Maintenance & Recurring Deadlines

### UC-06: Approaching Scheduled Service (Плановое ТО)
* **Trigger:** Scheduler cron triggers based on elapsed time (e.g., 11 months since last service) or extrapolated mileage (e.g., reached 14,000 km of 15,000 km interval).
* **Goal:** Prevent missed services without requiring manual odometer tracking.
* **Agent Behavior:**
  1. Computes estimated mileage using historical daily average.
  2. Sends notification: *«Подходит срок планового ТО (ориентировочно осталось ~1 000 км или 3 недели)»*.
  3. Prepares a service checklist based on manufacturer schedule (oil, oil filter, cabin filter, air filter, spark plugs if applicable).
  4. Keeps track of service appointment until invoice is uploaded.

### UC-07: Seasonal Tire Swap (Сезонная смена резины)
* **Trigger:** Calendar season shift or local weather forecast integration (e.g., temperatures consistently drop below +7°C).
* **Goal:** Timely tire change planning with storage location tracking.
* **Agent Behavior:**
  1. Reminds user about tire swap.
  2. Recalls tire profile data: where the winter/summer set is stored (home garage vs tire hotel contract), last measured tread depth.
  3. Offers to schedule tire swap appointment.

---

## Group 4: Parts Research & Human-in-the-Loop Purchasing

### UC-08: Compatible Part Research & Comparison («Подобрать колодки»)
* **Trigger:** Explicit user request (*«Найди передние колодки на мою машину»*) or output of an active fault incident.
* **Goal:** Find correct compatible parts, compare price tiers, and prepare a purchase link without unauthorized buying.
* **Agent Behavior:**
  1. Queries vehicle specs and exact VIN to identify OEM part numbers.
  2. Finds verified aftermarket cross-references (e.g., Brembo, ATE, TRW).
  3. Compares prices across connected suppliers/marketplaces.
  4. Presents a 3-tier card:
     * **OEM Original:** maximum compatibility guarantee.
     * **Premium Aftermarket:** best price/performance ratio.
     * **Budget:** lowest price verified fit.
  5. **Guardrail:** Prepares direct purchase links or pre-filled cart; does not execute payments autonomously.

---

## Group 5: Total Cost of Ownership (TCO) & Digital Passport

### UC-09: Total Cost of Ownership Analytics («Сколько мне обходится машина?»)
* **Trigger:** User analytics query or end-of-year summary.
* **Goal:** Transparency into full automotive financial footprint.
* **Agent Behavior:**
  1. Aggregates all vehicle expenses: fuel/charging, repairs, maintenance, insurance, taxes, parking, washes.
  2. Computes metrics: Cost per month, cost per kilometer/mile, maintenance vs fuel ratio.
  3. Visualizes trend changes (e.g., increasing maintenance cost on aging vehicle).

### UC-10: Digital Service Passport for Resale («Сервисная книжка для продажи»)
* **Trigger:** User command: *«Сформируй отчет по обслуживанию для продажи авто»*.
* **Goal:** Generate a clean, verifiable PDF service history to maximize vehicle resale value.
* **Agent Behavior:**
  1. Compiles all verified `MaintenanceLog` entries in chronological order.
  2. Attaches proof references (service invoices, inspection certificates).
  3. Exports a clean, tamper-evident document summary for prospective buyers.
