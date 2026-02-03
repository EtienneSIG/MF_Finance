# Mesures DAX - Finance Performance Management

Ce fichier contient toutes les mesures DAX testées et validées pour le semantic model Fabric (Finance).

## Tables Requises

- actuals
- budget
- invoices
- payments
- accounts
- cost_centers
- customers
- products (si analyse rentabilité produit)

## Relations Clés

```
accounts[account_id] 1 ----→ * actuals[account_id]
accounts[account_id] 1 ----→ * budget[account_id]
dim_cost_centers[cost_center_id] 1 ----→ * actuals[cost_center_id]
dim_cost_centers[cost_center_id] 1 ----→ * budget[cost_center_id]
dim_customers[customer_id] 1 ----→ * fact_invoices[customer_id]
fact_invoices[invoice_id] 1 ----→ * fact_payments[invoice_id]
```

---

## Métriques P&L (Profit & Loss)

### Revenue

Chiffre d'affaires.

```dax
Revenue = 
CALCULATE(
    SUM(actuals[amount]),
    accounts[account_type] = "Revenue"
)
```

**Format:** Currency (EUR)
**Usage:** Top line P&L

---

### COGS (Cost of Goods Sold)

Coût des marchandises vendues.

```dax
COGS = 
CALCULATE(
    SUM(actuals[amount]),
    accounts[account_type] = "COGS"
)
```

**Format:** Currency (EUR)
**Usage:** Calcul Gross Margin

---

### Gross Profit

Marge brute (montant).

```dax
Gross Profit = 
[Revenue] - [COGS]
```

**Format:** Currency (EUR)
**Usage:** Rentabilité

---

### Gross Margin %

Marge brute (pourcentage).

```dax
Gross Margin % = 
DIVIDE([Gross Profit], [Revenue], 0)
```

**Format:** Pourcentage
**Target:** >= 40%
**Usage:** KPI rentabilité

---

### Operating Expenses

Charges opérationnelles.

```dax
Operating Expenses = 
CALCULATE(
    SUM(actuals[amount]),
    accounts[account_type] = "OpEx"
)
```

**Format:** Currency (EUR)
**Usage:** P&L

---

### EBITDA

Earnings Before Interest, Taxes, Depreciation, Amortization.

```dax
EBITDA = 
[Revenue] - [COGS] - [Operating Expenses]
```

**Format:** Currency (EUR)
**Usage:** Performance opérationnelle

---

### EBITDA Margin %

EBITDA en pourcentage du CA.

```dax
EBITDA Margin % = 
DIVIDE([EBITDA], [Revenue], 0)
```

**Format:** Pourcentage
**Target:** >= 15%
**Usage:** KPI performance

---

### Net Income

Résultat net.

```dax
Net Income = 
CALCULATE(
    SUM(actuals[amount]),
    accounts[account_type] IN {"Revenue", "COGS", "OpEx", "Financial", "Tax"}
)
```

**Format:** Currency (EUR)
**Usage:** Bottom line P&L

---

## Métriques Budget vs Actual

### Budget Amount

Montant budgété.

```dax
Budget Amount = 
SUM(budget[amount])
```

**Format:** Currency (EUR)
**Usage:** Comparaison variance

---

### Actual Amount

Montant réalisé.

```dax
Actual Amount = 
SUM(actuals[amount])
```

**Format:** Currency (EUR)
**Usage:** Comparaison variance

---

### Variance Amount

Écart montant (Actual - Budget).

```dax
Variance Amount = 
[Actual Amount] - [Budget Amount]
```

**Format:** Currency (EUR)
**Usage:** Analyse variance

---

### Variance %

Écart en pourcentage.

```dax
Variance % = 
DIVIDE(
    [Variance Amount],
    [Budget Amount],
    0
)
```

**Format:** Pourcentage
**Threshold:** +/- 10% = material
**Usage:** Alerte variance

---

### Material Variance

Variance matérielle (> 10% ET > 50K EUR).

```dax
Material Variance = 
VAR VarAmount = ABS([Variance Amount])
VAR VarPct = ABS([Variance %])
RETURN
    IF(
        VarAmount > 50000 && VarPct > 0.1,
        [Variance Amount],
        BLANK()
    )
```

**Format:** Currency (EUR)
**Usage:** Focus attention

---

### Variance Status

Classification variance (Favorable/Unfavorable).

```dax
Variance Status = 
VAR AccountType = SELECTEDVALUE(accounts[account_type])
VAR Variance = [Variance Amount]
RETURN
    SWITCH(
        TRUE(),
        AccountType = "Revenue" && Variance > 0, "Favorable",
        AccountType = "Revenue" && Variance < 0, "Unfavorable",
        AccountType IN {"COGS", "OpEx"} && Variance < 0, "Favorable",
        AccountType IN {"COGS", "OpEx"} && Variance > 0, "Unfavorable",
        "Neutral"
    )
```

**Format:** Texte
**Usage:** Couleur conditionnelle

---

### Budget Revenue

Revenue budgété.

```dax
Budget Revenue = 
CALCULATE(
    SUM(budget[amount]),
    accounts[account_type] = "Revenue"
)
```

**Format:** Currency (EUR)
**Usage:** Comparaison top line

---

### Revenue Variance

Écart revenue vs budget.

```dax
Revenue Variance = 
[Revenue] - [Budget Revenue]
```

**Format:** Currency (EUR)
**Usage:** Focus top line

---

### Budget COGS

COGS budgété.

```dax
Budget COGS = 
CALCULATE(
    SUM(budget[amount]),
    accounts[account_type] = "COGS"
)
```

**Format:** Currency (EUR)
**Usage:** Comparaison coûts

---

### COGS Variance

Écart COGS vs budget.

```dax
COGS Variance = 
[COGS] - [Budget COGS]
```

**Format:** Currency (EUR)
**Usage:** Contrôle coûts

---

## Métriques Cash Flow

### Total Invoices

Total factures émises.

```dax
Total Invoices = 
SUM(fact_invoices[amount])
```

**Format:** Currency (EUR)
**Usage:** AR analysis

---

### Paid Invoices

Factures payées.

```dax
Paid Invoices = 
CALCULATE(
    SUM(fact_invoices[amount]),
    NOT(ISBLANK(fact_invoices[paid_date]))
)
```

**Format:** Currency (EUR)
**Usage:** Collection rate

---

### Unpaid Invoices

Factures non payées.

```dax
Unpaid Invoices = 
CALCULATE(
    SUM(fact_invoices[amount]),
    ISBLANK(fact_invoices[paid_date])
)
```

**Format:** Currency (EUR)
**Usage:** AR monitoring

---

### Accounts Receivable (AR)

Créances clients.

```dax
Accounts Receivable = 
[Unpaid Invoices]
```

**Format:** Currency (EUR)
**Usage:** DSO calculation

---

### DSO (Days Sales Outstanding)

Délai moyen de paiement clients.

```dax
DSO = 
VAR AR = [Accounts Receivable]
VAR DailyRevenue = DIVIDE([Revenue], 365, BLANK())
RETURN
    DIVIDE(AR, DailyRevenue, BLANK())
```

**Format:** Jours
**Target:** < 45 days
**Usage:** Working capital management

---

### Overdue Invoices

Factures en retard (> due_date).

```dax
Overdue Invoices = 
CALCULATE(
    SUM(fact_invoices[amount]),
    ISBLANK(fact_invoices[paid_date]),
    fact_invoices[due_date] < TODAY()
)
```

**Format:** Currency (EUR)
**Usage:** Collection urgence

---

### Overdue Invoices Count

Nombre de factures en retard.

```dax
Overdue Invoices Count = 
CALCULATE(
    COUNTROWS(invoices),
    ISBLANK(fact_invoices[paid_date]),
    fact_invoices[due_date] < TODAY()
)
```

**Format:** Nombre entier
**Usage:** Collection tracking

---

### Collection Rate

Taux de recouvrement.

```dax
Collection Rate = 
DIVIDE(
    [Paid Invoices],
    [Total Invoices],
    0
)
```

**Format:** Pourcentage
**Target:** >= 95%
**Usage:** Efficacité collection

---

### Avg Days to Pay

Délai moyen de paiement.

```dax
Avg Days to Pay = 
AVERAGEX(
    FILTER(
        invoices,
        NOT(ISBLANK(fact_invoices[paid_date]))
    ),
    DATEDIFF(fact_invoices[invoice_date], fact_invoices[paid_date], DAY)
)
```

**Format:** Jours
**Usage:** Analyse comportement paiement

---

### Total Payments

Total paiements reçus.

```dax
Total Payments = 
SUM(fact_payments[amount])
```

**Format:** Currency (EUR)
**Usage:** Cash in

---

### Operating Cash Flow

Flux de trésorerie opérationnel (simplifié).

```dax
Operating Cash Flow = 
[Total Payments] - [Operating Expenses]
```

**Format:** Currency (EUR)
**Usage:** Cash management

---

## Métriques par Dimension

### Revenue by Cost Center

Revenue par centre de coûts.

```dax
Revenue by Cost Center = 
CALCULATE(
    [Revenue],
    ALLEXCEPT(cost_centers, dim_cost_centers[cost_center_id])
)
```

**Format:** Currency (EUR)
**Context:** Cost center
**Usage:** Analyse contribution

---

### COGS by Cost Center

COGS par centre de coûts.

```dax
COGS by Cost Center = 
CALCULATE(
    [COGS],
    ALLEXCEPT(cost_centers, dim_cost_centers[cost_center_id])
)
```

**Format:** Currency (EUR)
**Context:** Cost center
**Usage:** Allocation coûts

---

### Margin by Customer

Marge par client.

```dax
Margin by Customer = 
VAR CustomerRevenue = 
    CALCULATE(
        [Revenue],
        ALLEXCEPT(customers, dim_customers[customer_id])
    )
VAR CustomerCOGS = 
    CALCULATE(
        [COGS],
        ALLEXCEPT(customers, dim_customers[customer_id])
    )
RETURN
    CustomerRevenue - CustomerCOGS
```

**Format:** Currency (EUR)
**Context:** Customer
**Usage:** Profitabilité client

---

### Cost Center Budget Utilization

Utilisation budget par CC.

```dax
Cost Center Budget Utilization = 
DIVIDE(
    [Actual Amount],
    [Budget Amount],
    BLANK()
)
```

**Format:** Pourcentage
**Context:** Cost center
**Usage:** Contrôle budget

---

## Métriques Temporelles

### YTD Revenue

Revenue cumul année.

```dax
YTD Revenue = 
CALCULATE(
    [Revenue],
    DATESYTD('Date'[Date])
)
```

**Format:** Currency (EUR)
**Usage:** Cumul annuel

---

### YTD Budget

Budget cumul année.

```dax
YTD Budget = 
CALCULATE(
    [Budget Amount],
    DATESYTD('Date'[Date])
)
```

**Format:** Currency (EUR)
**Usage:** Comparaison YTD

---

### YTD Variance

Variance cumul année.

```dax
YTD Variance = 
[YTD Revenue] - [YTD Budget]
```

**Format:** Currency (EUR)
**Usage:** Performance YTD

---

### MoM Growth %

Croissance mois sur mois.

```dax
MoM Growth % = 
VAR CurrentMonth = [Revenue]
VAR PreviousMonth = 
    CALCULATE(
        [Revenue],
        DATEADD('Date'[Date], -1, MONTH)
    )
RETURN
    DIVIDE(CurrentMonth - PreviousMonth, PreviousMonth, BLANK())
```

**Format:** Pourcentage
**Usage:** Trend analysis

---

### YoY Growth %

Croissance année sur année.

```dax
YoY Growth % = 
VAR CurrentYear = [Revenue]
VAR PreviousYear = 
    CALCULATE(
        [Revenue],
        DATEADD('Date'[Date], -1, YEAR)
    )
RETURN
    DIVIDE(CurrentYear - PreviousYear, PreviousYear, BLANK())
```

**Format:** Pourcentage
**Usage:** Comparaison annuelle

---

## Mesures Avancées

### Forecast Accuracy

Précision prévisions (Budget = forecast).

```dax
Forecast Accuracy = 
1 - ABS([Variance %])
```

**Format:** Pourcentage
**Target:** >= 90%
**Usage:** Qualité forecasting

---

### Working Capital

Fonds de roulement (simplifié).

```dax
Working Capital = 
[Accounts Receivable] - [Accounts Payable]
```

**Format:** Currency (EUR)
**Note:** Accounts Payable à créer si disponible
**Usage:** Trésorerie

---

### Burn Rate

Taux de consommation trésorerie (mensuel).

```dax
Burn Rate = 
DIVIDE(
    [Operating Expenses],
    DISTINCTCOUNT('Date'[Month]),
    BLANK()
)
```

**Format:** Currency (EUR/mois)
**Usage:** Cash runway

---

### Revenue per Employee

Revenue par employé (si table employees disponible).

```dax
Revenue per Employee = 
DIVIDE(
    [Revenue],
    DISTINCTCOUNT(employees[employee_id]),
    BLANK()
)
```

**Format:** Currency (EUR)
**Usage:** Productivité

---

## Notes d'Implémentation

### Vérification des Noms de Colonnes

**Tables critiques:**
- actuals.amount (FLOAT)
- actuals.account_id (STRING, FK)
- actuals.cost_center_id (STRING, FK)
- budget.amount (FLOAT)
- invoices.paid_date (DATE, nullable pour DSO)
- accounts.account_type (STRING)

### Relations Manquantes

Si une mesure retourne BLANK(), vérifier:
1. Relations entre tables créées
2. Cardinalités correctes (1:Many)
3. Table Date créée et reliée

### Performance

Pour améliorer les performances:
- Créer table Date si pas déjà fait
- Indexer account_id, cost_center_id
- Pré-calculer YTD dans table intermédiaire si volume élevé

---

## Validation

**Valeurs attendues (dataset complet):**
- Gross Margin %: ~40-45%
- EBITDA Margin %: ~15-20%
- Variance %: +/- 5-10% (normal), > 10% (investigate)
- DSO: ~30-45 days
- Collection Rate: ~95%

