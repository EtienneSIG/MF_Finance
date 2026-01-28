# Schéma de Données - Finance Performance Management

Ce document décrit le schéma complet des **11 tables** de la démo Finance.

---

## 📐 Architecture Relationnelle

```
Finance:
  chart_of_accounts (1) ←─── (N) general_ledger
  cost_centers (1) ←─── (N) general_ledger
  cost_centers (1) ←─── (N) budgets
  cost_centers (1) ←─── (N) forecasts
  chart_of_accounts (1) ←─── (N) budgets
  chart_of_accounts (1) ←─── (N) forecasts

Business:
  customers (1) ←─── (N) invoices (1) ←─── (N) invoice_lines (N) ───→ (1) products
  invoices (1) ←─── (1) payments

Cross-domain:
  general_ledger ←→ invoices (via reference)
  general_ledger ←→ customers (via cost_center region mapping)
```

---

## 📊 Tables Finance (6 tables)

### 1. `chart_of_accounts`

**Description** : Plan comptable (comptes de classe 1 à 7).

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `account_id` | STRING | Identifiant unique compte | PK, format `ACC_XXXX` |
| `account_number` | STRING | Numéro de compte comptable | Unique, ex: "1000", "6010" |
| `account_name` | STRING | Nom du compte | Ex: "Capital social", "Salaires bruts" |
| `account_type` | STRING | Type de compte | Asset, Liability, Equity, Revenue, Expense, Cash |
| `category` | STRING | Catégorie principale | "1 - Actif", "6 - Charges", etc. |
| `sub_category` | STRING | Sous-catégorie | "60 - Achats", "61 - Salaires", etc. |
| `is_active` | BOOLEAN | Compte actif ? | true/false |
| `currency` | STRING | Devise | EUR |

**Volume** : ~150 lignes

**Exemples** :
```
ACC_1000, 1000, Capital social, Equity, 1 - Actif, 10 - Capital, true, EUR
ACC_6010, 6010, Salaires bruts, Expense, 6 - Charges, 61 - Salaires, true, EUR
ACC_7010, 7010, Software Licenses, Revenue, 7 - Produits, 70 - Ventes, true, EUR
```

---

### 2. `general_ledger`

**Description** : Grand livre (journal des écritures comptables).

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `entry_id` | STRING | Identifiant unique écriture | PK, format `GL_XXXXXXXXXX` |
| `entry_date` | DATE | Date de l'écriture | |
| `period_month` | INT | Mois (1-12) | |
| `fiscal_year` | INT | Année fiscale | 2025 |
| `account_id` | STRING | Compte comptable | FK → `chart_of_accounts.account_id` |
| `cost_center_id` | STRING | Centre de coûts | FK → `cost_centers.cost_center_id` |
| `debit_amount_eur` | DECIMAL | Montant débit (EUR) | >= 0 |
| `credit_amount_eur` | DECIMAL | Montant crédit (EUR) | >= 0 |
| `description` | STRING | Description de l'écriture | |
| `reference` | STRING | Référence (facture, budget...) | Ex: INV_00001234, BUD_00000567 |
| `entry_type` | STRING | Type d'écriture | Revenue, Expense, COGS, Asset, Liability |

**Volume** : ~50 000 lignes

**Cardinalité** :
- `general_ledger.account_id` → `chart_of_accounts.account_id` : Many-to-One
- `general_ledger.cost_center_id` → `cost_centers.cost_center_id` : Many-to-One

**Exemples** :
```
GL_0000000001, 2025-01-15, 1, 2025, ACC_7010, CC_001, 0, 15000.00, Revenue from INV_00000123, INV_00000123, Revenue
GL_0000000002, 2025-01-15, 1, 2025, ACC_6000, CC_007, 2250.00, 0, COGS for INV_00000123, INV_00000123, COGS
```

---

### 3. `cost_centers`

**Description** : Centres de coûts / centres de profit.

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `cost_center_id` | STRING | Identifiant unique CC | PK, format `CC_XXX` |
| `cost_center_name` | STRING | Nom du centre de coûts | Ex: "Sales France", "Marketing" |
| `cost_center_type` | STRING | Type de CC | Revenue, Support, R&D, Delivery, Admin |
| `region` | STRING | Région | France, EMEA, Americas, Global |
| `manager` | STRING | Responsable | Ex: "Manager 1" |
| `budget_allocation_pct` | DECIMAL | % d'allocation budget | 0-1 (ex: 0.15 = 15%) |
| `is_active` | BOOLEAN | CC actif ? | true/false |

**Volume** : 13 lignes

**Exemples** :
```
CC_001, Sales France, Revenue, France, Manager 1, 0.15, true
CC_004, Marketing, Support, Global, Manager 4, 0.08, true
CC_005, Product Development, R&D, Global, Manager 5, 0.20, true
```

---

### 4. `budgets`

**Description** : Budgets mensuels par centre de coûts et compte.

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `budget_id` | STRING | Identifiant unique budget | PK, format `BUD_XXXXXXXX` |
| `fiscal_year` | INT | Année fiscale | 2025 |
| `period_month` | INT | Mois (1-12) | |
| `period_date` | DATE | Date du mois (1er du mois) | |
| `cost_center_id` | STRING | Centre de coûts | FK → `cost_centers.cost_center_id` |
| `account_id` | STRING | Compte comptable | FK → `chart_of_accounts.account_id` |
| `budget_amount_eur` | DECIMAL | Montant budgeté (EUR) | |
| `budget_type` | STRING | Type de budget | Operating, Capital |
| `version` | STRING | Version du budget | V1_Approved, V2_Revised, etc. |

**Volume** : ~2 000 lignes

**Cardinalité** :
- `budgets.cost_center_id` → `cost_centers.cost_center_id` : Many-to-One
- `budgets.account_id` → `chart_of_accounts.account_id` : Many-to-One

---

### 5. `forecasts`

**Description** : Reforecasts trimestriels (Q2, Q3, Q4).

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `forecast_id` | STRING | Identifiant unique forecast | PK, format `FCS_XXXXXXXX` |
| `fiscal_year` | INT | Année fiscale | 2025 |
| `period_month` | INT | Mois (1-12) | |
| `period_date` | DATE | Date du mois (1er du mois) | |
| `cost_center_id` | STRING | Centre de coûts | FK → `cost_centers.cost_center_id` |
| `account_id` | STRING | Compte comptable | FK → `chart_of_accounts.account_id` |
| `forecast_amount_eur` | DECIMAL | Montant forecasté (EUR) | |
| `forecast_type` | STRING | Type de forecast | Rolling, Committed |
| `version` | STRING | Version du forecast | Q2_Reforecast, Q3_Reforecast, Q4_Reforecast |
| `created_date` | DATE | Date de création du forecast | |

**Volume** : ~6 000 lignes

---

### 6. `allocations`

**Description** : Allocations de coûts indirects (overhead).

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `allocation_id` | STRING | Identifiant unique allocation | PK, format `ALLOC_XXXXXX` |
| `fiscal_year` | INT | Année fiscale | 2025 |
| `from_cost_center` | STRING | CC source (overhead pool) | Ex: "IT Infrastructure", "HR Services" |
| `to_cost_center_id` | STRING | CC destination | FK → `cost_centers.cost_center_id` |
| `allocation_driver` | STRING | Driver d'allocation | headcount, revenue, square_footage, transactions |
| `driver_units` | DECIMAL | Nombre d'unités du driver | Ex: 15.5 (headcount) |
| `allocated_amount_eur` | DECIMAL | Montant alloué (EUR) | |
| `allocation_month` | INT | Mois d'allocation | Généralement 12 (fin d'année) |

**Volume** : ~65 lignes

---

## 📊 Tables Business (5 tables)

### 7. `customers`

**Description** : Clients (B2B).

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `customer_id` | STRING | Identifiant unique client | PK, format `CUST_XXXXXX` |
| `company_name` | STRING | Nom de l'entreprise | |
| `segment` | STRING | Segment client | enterprise, mid_market, smb |
| `industry` | STRING | Secteur d'activité | Technology, Retail, Finance, etc. |
| `country` | STRING | Pays | France, Germany, UK, USA, Spain, Italy |
| `payment_terms_days` | INT | Conditions de paiement (jours) | 30, 45, 60 |
| `credit_limit_eur` | DECIMAL | Limite de crédit (EUR) | |
| `account_manager` | STRING | Account Manager | Ex: AM_01 |
| `created_date` | DATE | Date de création client | |
| `is_active` | BOOLEAN | Client actif ? | true/false |

**Volume** : 500 lignes

**Distribution segments** :
- Enterprise : 10% (50 clients)
- Mid-market : 30% (150 clients)
- SMB : 60% (300 clients)

---

### 8. `products`

**Description** : Catalogue produits.

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `product_id` | STRING | Identifiant unique produit | PK, format `PROD_XXXXX` |
| `product_name` | STRING | Nom du produit | |
| `category` | STRING | Catégorie | software_licenses, professional_services, maintenance, training |
| `unit_price_eur` | DECIMAL | Prix unitaire (EUR) | |
| `cogs_eur` | DECIMAL | Coût de revient (EUR) | |
| `gross_margin_pct` | DECIMAL | Marge brute (%) | |
| `is_active` | BOOLEAN | Produit actif ? | true/false |

**Volume** : 50 lignes

**Distribution catégories** :
- Software Licenses : 15 produits (marge 85%)
- Professional Services : 10 produits (marge 40%)
- Maintenance : 15 produits (marge 70%)
- Training : 10 produits (marge 50%)

---

### 9. `invoices`

**Description** : Factures clients.

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `invoice_id` | STRING | Identifiant unique facture | PK, format `INV_XXXXXXXX` |
| `invoice_number` | STRING | Numéro de facture | Format FYYYYNNNNNN |
| `customer_id` | STRING | Client | FK → `customers.customer_id` |
| `invoice_date` | DATE | Date de facturation | |
| `due_date` | DATE | Date d'échéance | |
| `total_amount_eur` | DECIMAL | Montant total TTC (EUR) | |
| `status` | STRING | Statut | Issued, Paid, Overdue |
| `payment_terms_days` | INT | Conditions de paiement (jours) | |

**Volume** : 8 000 lignes

**Cardinalité** :
- `invoices.customer_id` → `customers.customer_id` : Many-to-One

---

### 10. `invoice_lines`

**Description** : Lignes de factures (détail produits).

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `line_id` | STRING | Identifiant unique ligne | PK, format `LINE_XXXXXXXX_XX` |
| `invoice_id` | STRING | Facture | FK → `invoices.invoice_id` |
| `product_id` | STRING | Produit | FK → `products.product_id` |
| `quantity` | INT | Quantité | >= 1 |
| `unit_price_eur` | DECIMAL | Prix unitaire (EUR) | |
| `discount_pct` | DECIMAL | Remise (%) | 0-0.15 |
| `line_total_eur` | DECIMAL | Total ligne (EUR) | quantity × unit_price × (1 - discount) |
| `cogs_eur` | DECIMAL | Coût de revient total (EUR) | |

**Volume** : ~20 000 lignes

**Cardinalité** :
- `invoice_lines.invoice_id` → `invoices.invoice_id` : Many-to-One
- `invoice_lines.product_id` → `products.product_id` : Many-to-One

---

### 11. `payments`

**Description** : Paiements reçus.

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `payment_id` | STRING | Identifiant unique paiement | PK, format `PAY_XXXXXXXX` |
| `invoice_id` | STRING | Facture payée | FK → `invoices.invoice_id` |
| `payment_date` | DATE | Date de paiement | |
| `payment_amount_eur` | DECIMAL | Montant payé (EUR) | |
| `payment_method` | STRING | Moyen de paiement | Wire Transfer, Check, Credit Card |
| `days_overdue` | INT | Jours de retard | >= 0 |

**Volume** : ~7 000 lignes

**Cardinalité** :
- `payments.invoice_id` → `invoices.invoice_id` : Many-to-One (ou One-to-One)

---

## 🔗 Relations Clés

### Relations Finance
```sql
general_ledger.account_id → chart_of_accounts.account_id
general_ledger.cost_center_id → cost_centers.cost_center_id
budgets.account_id → chart_of_accounts.account_id
budgets.cost_center_id → cost_centers.cost_center_id
forecasts.account_id → chart_of_accounts.account_id
forecasts.cost_center_id → cost_centers.cost_center_id
allocations.to_cost_center_id → cost_centers.cost_center_id
```

### Relations Business
```sql
invoices.customer_id → customers.customer_id
invoice_lines.invoice_id → invoices.invoice_id
invoice_lines.product_id → products.product_id
payments.invoice_id → invoices.invoice_id
```

### Relations Cross-Domain
```sql
general_ledger.reference → invoices.invoice_id (soft link via reference field)
```

---

## 📊 Métriques Calculées

### Revenue Metrics
- **Total Revenue** : SUM(invoice_lines.line_total_eur)
- **Revenue by Category** : GROUP BY products.category

### Profitability Metrics
- **Total COGS** : SUM(invoice_lines.cogs_eur)
- **Gross Margin** : (Revenue - COGS) / Revenue
- **Operating Expenses** : SUM(general_ledger.debit_amount_eur WHERE account_type='Expense')
- **EBITDA** : Revenue - COGS - Operating Expenses

### Budget Metrics
- **Budget vs Actual** : 
  - Budget : SUM(budgets.budget_amount_eur)
  - Actual : SUM(general_ledger.debit_amount_eur WHERE account_id = budget.account_id)
  - Variance : (Actual - Budget) / Budget × 100

### Cash Metrics
- **DSO** : (Accounts Receivable / Revenue) × 365
  - AR : SUM(invoices.total_amount_eur WHERE status != 'Paid')
- **Overdue Amount** : SUM(invoices.total_amount_eur WHERE due_date < TODAY() AND status != 'Paid')

---

## 🎯 Cas d'Usage d'Analyse

### 1. P&L Analysis
```sql
SELECT 
    DATE_TRUNC('month', gl.entry_date) AS month,
    SUM(CASE WHEN coa.account_type = 'Revenue' THEN gl.credit_amount_eur ELSE 0 END) AS revenue,
    SUM(CASE WHEN coa.account_name = 'Achats matières' THEN gl.debit_amount_eur ELSE 0 END) AS cogs,
    SUM(CASE WHEN coa.account_type = 'Expense' AND coa.account_name != 'Achats matières' THEN gl.debit_amount_eur ELSE 0 END) AS opex
FROM general_ledger gl
JOIN chart_of_accounts coa ON gl.account_id = coa.account_id
GROUP BY month
ORDER BY month;
```

### 2. Budget Variance by Cost Center
```sql
SELECT 
    cc.cost_center_name,
    SUM(b.budget_amount_eur) AS budget,
    SUM(gl.debit_amount_eur) AS actual,
    (SUM(gl.debit_amount_eur) - SUM(b.budget_amount_eur)) / SUM(b.budget_amount_eur) * 100 AS variance_pct
FROM budgets b
JOIN cost_centers cc ON b.cost_center_id = cc.cost_center_id
LEFT JOIN general_ledger gl ON b.account_id = gl.account_id 
    AND b.cost_center_id = gl.cost_center_id 
    AND b.period_month = gl.period_month
WHERE b.fiscal_year = 2025
GROUP BY cc.cost_center_name
ORDER BY variance_pct DESC;
```

### 3. DSO and Aging Analysis
```sql
SELECT 
    c.segment,
    COUNT(i.invoice_id) AS invoice_count,
    SUM(i.total_amount_eur) AS total_ar,
    AVG(DATEDIFF(COALESCE(p.payment_date, CURRENT_DATE), i.due_date)) AS avg_days_overdue
FROM invoices i
JOIN customers c ON i.customer_id = c.customer_id
LEFT JOIN payments p ON i.invoice_id = p.invoice_id
WHERE i.status != 'Paid'
GROUP BY c.segment
ORDER BY avg_days_overdue DESC;
```

---

*Ce schéma permet de répondre à toutes les questions CFO/Finance via le Data Agent.*
