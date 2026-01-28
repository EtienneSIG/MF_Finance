# Guide de Déploiement - Microsoft Fabric (Scénario Finance)

## 🎯 Objectif

Ce guide décrit **étape par étape** comment déployer la démo Finance Performance Management dans Microsoft Fabric.

**Prérequis** :
- Un compte Microsoft Fabric (trial ou licence)
- Les données générées localement (voir README.md)
- Un workspace Fabric créé

**Durée estimée** : 30-40 minutes

---

## 📋 Vue d'Ensemble du Déploiement

```
Étape 1: Créer un Lakehouse
Étape 2: Uploader les données vers OneLake
Étape 3: Créer des OneLake Shortcuts (optionnel)
Étape 4: Charger les CSV en tables Delta
Étape 5: Créer un Semantic Model
Étape 6: Configurer le Fabric Data Agent
Étape 7: Tester et valider
```

---

## Étape 1 : Créer un Lakehouse

### 1.1 Accéder au Workspace

1. Ouvrir [Microsoft Fabric](https://app.fabric.microsoft.com/)
2. Sélectionner ou créer un workspace (ex: `Demo-Finance`)
3. Vérifier que vous êtes dans l'expérience **Data Engineering**

### 1.2 Créer le Lakehouse

1. Cliquer sur **+ New** → **Lakehouse**
2. Nom : `Finance_Lakehouse`
3. Cliquer sur **Create**

✅ **Résultat attendu** : Un Lakehouse vide avec deux sections : **Tables** et **Files**.

---

## Étape 2 : Uploader les Données vers OneLake

### 2.1 Préparer les Données Locales

Sur votre machine locale, les données générées sont dans :
```
data/
├── raw/
│   ├── finance/
│   │   ├── chart_of_accounts.csv
│   │   ├── general_ledger.csv
│   │   ├── cost_centers.csv
│   │   ├── budgets.csv
│   │   ├── forecasts.csv
│   │   └── allocations.csv
│   └── business/
│       ├── customers.csv
│       ├── products.csv
│       ├── invoices.csv
│       ├── invoice_lines.csv
│       └── payments.csv
```

### 2.2 Upload via l'Interface Fabric

**Option A : Upload direct**

1. Dans le Lakehouse, aller dans **Files**
2. Créer une structure de dossiers :
   - Cliquer sur **Upload** → **Upload folder**
   - Sélectionner `data/raw/finance`
   - Répéter pour `data/raw/business`

**Option B : Upload via OneLake File Explorer (recommandé)**

1. Installer [OneLake File Explorer](https://www.microsoft.com/en-us/download/details.aspx?id=105222)
2. Ouvrir OneLake File Explorer
3. Naviguer vers votre workspace → `Finance_Lakehouse` → **Files**
4. Copier-coller les dossiers `finance/` et `business/` depuis votre explorateur Windows

✅ **Résultat attendu** : Structure de dossiers visible dans **Files** du Lakehouse.

---

## Étape 3 : Créer des OneLake Shortcuts (optionnel)

### 3.1 Principe des Shortcuts

Les **OneLake Shortcuts** créent des liens symboliques sans duplication de données.

**Pour cette démo** : Optionnel si les fichiers sont déjà dans le Lakehouse.

### 3.2 Créer un Shortcut (Exemple : CSV Finance)

1. Dans le Lakehouse, section **Files**
2. Clic droit sur la racine → **New shortcut**
3. Choisir **OneLake**
4. Sélectionner :
   - **Workspace** : Demo-Finance
   - **Item** : Finance_Lakehouse
   - **Path** : `Files/raw/finance`
5. Nommer le shortcut : `finance_data`
6. Cliquer sur **Create**

✅ **Résultat attendu** : Icône de shortcut visible dans Files.

---

## Étape 4 : Charger les CSV en Tables Delta

### 4.1 Créer des Tables depuis les CSV

**Méthode A : Via l'interface**

1. Dans **Files**, naviguer vers `raw/finance/chart_of_accounts.csv`
2. Clic droit → **Load to new table**
3. Configurer :
   - **Table name** : `chart_of_accounts`
   - **Delimiter** : Comma
   - **First row has headers** : ✅ Yes
   - **Infer schema** : ✅ Yes
4. Cliquer sur **Load**

Répéter pour toutes les tables :

**Tables Finance (6)** :
- `chart_of_accounts`
- `general_ledger`
- `cost_centers`
- `budgets`
- `forecasts`
- `allocations`

**Tables Business (5)** :
- `customers`
- `products`
- `invoices`
- `invoice_lines`
- `payments`

**Méthode B : Via Notebook (pour automatisation)**

```python
# Notebook: Load CSV to Delta Tables

from pyspark.sql import SparkSession

# Chemins des fichiers Finance
finance_files = {
    "chart_of_accounts": "Files/raw/finance/chart_of_accounts.csv",
    "general_ledger": "Files/raw/finance/general_ledger.csv",
    "cost_centers": "Files/raw/finance/cost_centers.csv",
    "budgets": "Files/raw/finance/budgets.csv",
    "forecasts": "Files/raw/finance/forecasts.csv",
    "allocations": "Files/raw/finance/allocations.csv"
}

# Chemins des fichiers Business
business_files = {
    "customers": "Files/raw/business/customers.csv",
    "products": "Files/raw/business/products.csv",
    "invoices": "Files/raw/business/invoices.csv",
    "invoice_lines": "Files/raw/business/invoice_lines.csv",
    "payments": "Files/raw/business/payments.csv"
}

# Fusionner
all_files = {**finance_files, **business_files}

# Charger chaque CSV en table Delta
for table_name, file_path in all_files.items():
    df = spark.read.csv(file_path, header=True, inferSchema=True)
    df.write.format("delta").mode("overwrite").saveAsTable(table_name)
    print(f"✅ Table {table_name} créée avec {df.count()} lignes")
```

✅ **Résultat attendu** : 11 tables Delta au total dans **Tables**.

### 4.2 Vérifier les Types de Données

```sql
-- Vérifier les dates
DESCRIBE general_ledger;
-- Attendu: entry_date DATE

DESCRIBE invoices;
-- Attendu: invoice_date DATE, due_date DATE

-- Vérifier les montants
DESCRIBE budgets;
-- Attendu: budget_amount_eur DECIMAL
```

Si les types sont incorrects :

```python
from pyspark.sql.functions import to_date, col

# Corriger les dates du general_ledger
df = spark.table("general_ledger")
df = df.withColumn("entry_date", to_date(col("entry_date"), "yyyy-MM-dd"))
df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("general_ledger")
```

---

## Étape 5 : Créer un Semantic Model

### 5.1 Créer le Semantic Model

1. Dans le Lakehouse, cliquer sur **New semantic model**
2. Nom : `Finance_Model`
3. Sélectionner les tables à inclure :
   - ✅ **Finance** : chart_of_accounts, general_ledger, cost_centers, budgets, forecasts, allocations
   - ✅ **Business** : customers, products, invoices, invoice_lines, payments
4. Cliquer sur **Confirm**

### 5.2 Définir les Relations

Créer les relations suivantes :

**Relations Finance**

| Table From | Colonne From | Table To | Colonne To | Cardinalité |
|------------|--------------|----------|------------|-------------|
| `general_ledger` | `account_id` | `chart_of_accounts` | `account_id` | Many-to-One |
| `general_ledger` | `cost_center_id` | `cost_centers` | `cost_center_id` | Many-to-One |
| `budgets` | `account_id` | `chart_of_accounts` | `account_id` | Many-to-One |
| `budgets` | `cost_center_id` | `cost_centers` | `cost_center_id` | Many-to-One |
| `forecasts` | `account_id` | `chart_of_accounts` | `account_id` | Many-to-One |
| `forecasts` | `cost_center_id` | `cost_centers` | `cost_center_id` | Many-to-One |
| `allocations` | `to_cost_center_id` | `cost_centers` | `cost_center_id` | Many-to-One |

**Relations Business**

| Table From | Colonne From | Table To | Colonne To | Cardinalité |
|------------|--------------|----------|------------|-------------|
| `invoices` | `customer_id` | `customers` | `customer_id` | Many-to-One |
| `invoice_lines` | `invoice_id` | `invoices` | `invoice_id` | Many-to-One |
| `invoice_lines` | `product_id` | `products` | `product_id` | Many-to-One |
| `payments` | `invoice_id` | `invoices` | `invoice_id` | Many-to-One |

### 5.3 Créer des Mesures DAX

```dax
// ============================================
// Mesures Revenue
// ============================================

Total Revenue = 
SUMX(
    invoice_lines,
    invoice_lines[quantity] * invoice_lines[unit_price_eur] * (1 - invoice_lines[discount_pct])
)

Revenue from GL = 
CALCULATE(
    SUM(general_ledger[credit_amount_eur]),
    chart_of_accounts[account_type] = "Revenue"
)

// ============================================
// Mesures COGS & Gross Margin
// ============================================

Total COGS = SUM(invoice_lines[cogs_eur])

COGS from GL = 
CALCULATE(
    SUM(general_ledger[debit_amount_eur]),
    chart_of_accounts[account_name] = "Achats matières"
)

Gross Margin EUR = [Total Revenue] - [Total COGS]

Gross Margin % = 
DIVIDE(
    [Gross Margin EUR],
    [Total Revenue],
    0
) * 100

// ============================================
// Mesures Operating Expenses
// ============================================

Total Opex = 
CALCULATE(
    SUM(general_ledger[debit_amount_eur]),
    chart_of_accounts[account_type] = "Expense",
    chart_of_accounts[account_name] <> "Achats matières"
)

// ============================================
// Mesures Profitability
// ============================================

EBITDA = [Gross Margin EUR] - [Total Opex]

EBITDA % = 
DIVIDE(
    [EBITDA],
    [Total Revenue],
    0
) * 100

Net Profit = [EBITDA]  // Simplifié (sans intérêts, taxes, etc.)

Net Profit % = 
DIVIDE(
    [Net Profit],
    [Total Revenue],
    0
) * 100

// ============================================
// Mesures Budget
// ============================================

Total Budget = SUM(budgets[budget_amount_eur])

Actual Expenses = 
CALCULATE(
    SUM(general_ledger[debit_amount_eur]),
    chart_of_accounts[account_type] = "Expense"
)

Budget Variance EUR = [Actual Expenses] - [Total Budget]

Budget Variance % = 
DIVIDE(
    [Budget Variance EUR],
    [Total Budget],
    0
) * 100

// ============================================
// Mesures Forecast
// ============================================

Total Forecast = SUM(forecasts[forecast_amount_eur])

Forecast Accuracy % = 
DIVIDE(
    [Actual Expenses],
    [Total Forecast],
    0
) * 100

// ============================================
// Mesures Cash & DSO
// ============================================

Accounts Receivable = 
CALCULATE(
    SUM(invoices[total_amount_eur]),
    invoices[status] <> "Paid"
)

DSO = 
DIVIDE(
    [Accounts Receivable],
    [Total Revenue] / 365,
    0
)

Overdue Amount = 
CALCULATE(
    SUM(invoices[total_amount_eur]),
    invoices[due_date] < TODAY(),
    invoices[status] <> "Paid"
)

Avg Days Overdue = AVERAGE(payments[days_overdue])

// ============================================
// Mesures Counts
// ============================================

Total Invoices = COUNTROWS(invoices)

Total Customers = COUNTROWS(customers)

Total Products = COUNTROWS(products)
```

### 5.4 Publier le Semantic Model

1. Cliquer sur **File** → **Save**
2. Le modèle est automatiquement publié dans le workspace

✅ **Résultat attendu** : Semantic Model disponible, prêt pour Power BI et Data Agent.

---

## Étape 6 : Configurer le Fabric Data Agent

### 6.1 Activer la Preview Data Agent

1. Aller dans **Settings** (⚙️) → **Tenant settings**
2. Rechercher **Fabric Data Agent**
3. Activer la preview pour le workspace

### 6.2 Créer le Data Agent

1. Dans le workspace, cliquer sur **+ New** → **Data Agent**
2. Nom : `Finance_Controller`
3. Sélectionner la source :
   - **Type** : Semantic Model
   - **Source** : `Finance_Model`
4. Cliquer sur **Create**

### 6.3 Configurer les Instructions (System Prompt)

1. Ouvrir le Data Agent
2. Aller dans **Settings** → **Instructions**
3. Coller le contenu de [`data_agent_instructions.md`](data_agent_instructions.md)
4. Sauvegarder

### 6.4 Tester le Data Agent

Poser une première question :
```
Quel est le chiffre d'affaires total ?
```

Réponse attendue : `~31M€`

Si la réponse est correcte ✅, passer à l'étape 7.

---

## Étape 7 : Tester et Valider

### 7.1 Questions de Validation

Poser les questions de [`questions_demo.md`](questions_demo.md) :

1. ✅ Quel est le chiffre d'affaires total de l'année ?
2. ✅ Quelle est la marge brute globale ?
3. ✅ Quels centres de coûts ont dépassé leur budget ?
4. ✅ Quel est le DSO actuel ?
5. ✅ Pourquoi la marge brute baisse en Q2 ?

**Critère de succès** : Au moins 16/20 questions fonctionnent correctement.

### 7.2 Créer un Dashboard Power BI

1. Dans le workspace, cliquer sur **+ New** → **Report**
2. Sélectionner `Finance_Model` comme source
3. Créer quelques visuels :

**Page 1 : P&L**
   - Card : Total Revenue, Gross Margin %, EBITDA, Net Profit
   - Waterfall Chart : P&L Breakdown
   - Line Chart : Revenue & EBITDA by Month

**Page 2 : Budget Analysis**
   - Card : Total Budget, Actual, Variance %
   - Bar Chart : Budget Variance by Cost Center
   - Table : Top 10 Overrun Accounts

**Page 3 : Cash & DSO**
   - Card : DSO, Overdue Amount
   - Line Chart : DSO Trend
   - Table : Top Overdue Customers

4. Sauvegarder le rapport : `Finance_Dashboard`

### 7.3 Vérifier les Permissions

Si la démo doit être partagée :
1. Aller dans **Workspace settings** → **Access**
2. Ajouter les viewers/contributors
3. Vérifier que le Semantic Model est partagé

---

## 🎉 Déploiement Terminé

Vous avez maintenant :
- ✅ Un Lakehouse avec 11 tables Delta
- ✅ Des OneLake Shortcuts (optionnel)
- ✅ Un Semantic Model complet avec relations et mesures
- ✅ Un Data Agent fonctionnel
- ✅ Un dashboard Power BI Finance

**Prochaines étapes** :
- Tester les 20 questions de la démo
- Personnaliser le dashboard
- Préparer le pitch ([demo_story.md](demo_story.md))

---

## 🔧 Troubleshooting

### Problème : Le Data Agent ne répond pas correctement

**Solutions** :
1. Vérifier que le Semantic Model est publié
2. Vérifier les relations entre tables (11 relations au total)
3. Vérifier que toutes les mesures DAX sont bien calculées
4. Simplifier la question (utiliser termes exacts)

### Problème : Erreurs de type de données

**Solutions** :
```python
from pyspark.sql.functions import to_date, col

# Corriger les dates
df = spark.table("general_ledger")
df = df.withColumn("entry_date", to_date(col("entry_date"), "yyyy-MM-dd"))
df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("general_ledger")
```

### Problème : Les montants ne matchent pas

**Solutions** :
- Vérifier que les mesures DAX utilisent les bonnes tables
- Revenue : utiliser `invoice_lines` (source de vérité)
- Budget : utiliser `budgets`
- Actual : utiliser `general_ledger`

---

## ✅ Checklist de Déploiement

- [ ] Lakehouse créé
- [ ] Données uploadées (11 CSV)
- [ ] OneLake Shortcuts créés (optionnel)
- [ ] 11 tables Delta créées et vérifiées
- [ ] Semantic Model créé
- [ ] Relations Finance définies (7 relations)
- [ ] Relations Business définies (4 relations)
- [ ] Mesures DAX ajoutées (Revenue, Margin, Budget, DSO...)
- [ ] Data Agent configuré
- [ ] Instructions du Data Agent ajoutées
- [ ] Questions de test validées (≥16/20)
- [ ] Dashboard Power BI créé
- [ ] Permissions partagées (si nécessaire)

**Si toutes les cases sont cochées, la démo est prête ! 🚀**
