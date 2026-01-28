# Demo Story - La Performance Financière sous Contrôle

## 🎬 Scénario : "Le CFO face aux Défis 2025"

### Contexte

**TechCorp** est une entreprise SaaS B2B avec 24M€ de revenue annuel. Le CFO, **Marie Durand**, utilise Microsoft Fabric et le Data Agent pour piloter la performance financière en 2025.

**Enjeux** :
- Maintenir une marge brute >70%
- Respecter le budget (tolérance ±10%)
- Améliorer le cash flow (DSO cible : 45 jours)
- Identifier les leviers de croissance rentable

---

## Acte 1 : Q1 - Lancement d'Année Prometteur

### Situation (Janvier-Mars 2025)

Marie démarre l'année avec optimisme :
- Budget approuvé : 24M€ de dépenses
- Revenue target : 30M€ (+25% vs 2024)
- Marge brute cible : 72%

**Questions au Data Agent** :
> *"Affiche le P&L consolidé de Q1"*

**Réponse** :
```
Q1 2025 P&L:
- Revenue: 7.5M€
- COGS: 2.1M€ (28%)
- Gross Margin: 5.4M€ (72%) ✅
- Operating Expenses: 4.2M€
- EBITDA: 1.2M€ (16%)

✅ Q1 dans les clous : marge brute = target
```

Marie est satisfaite. Q1 performe selon le plan.

---

## Acte 2 : Q2 - Alerte Marge !

### Situation (Avril-Juin 2025)

En avril, Marie remarque une baisse de la marge brute lors de sa revue mensuelle.

**Question au Data Agent** :
> *"Pourquoi la marge brute baisse en Q2 ?"*

**Réponse** :
```
⚠️ Marge brute Q2: 67% (vs 72% en Q1) → -5 points

Causes identifiées:
1. Remises agressives: +8% de discount moyen (vs 5% en Q1)
2. Mix produit: hausse des Professional Services (marge 40%) 
   au détriment des Software Licenses (marge 85%)
3. Prix moyen: -12% sur les licences (guerre des prix)

Impact revenue: +2.1M€ (bon)
Impact marge: -450K€ (mauvais)

🎯 Recommandation: Revoir la stratégie pricing, réduire les discounts
```

### Actions

Marie organise une réunion avec les Sales :
- **Décision 1** : Limiter les remises à 10% max (sauf deals stratégiques)
- **Décision 2** : Inciter les ventes de licences (commission ajustée)
- **Décision 3** : Augmenter les prix de 5% sur la gamme premium

**Résultat** : En juin, la marge remonte à 70%.

---

## Acte 3 : Q3 - Dépassement Budget Marketing

### Situation (Juillet-Septembre 2025)

En août, lors de la revue budgétaire, une alerte apparaît.

**Question au Data Agent** :
> *"Quels centres de coûts ont dépassé leur budget en Q3 ?"*

**Réponse** :
```
⚠️ Dépassements budgétaires Q3:

1. Marketing: +25% vs budget
   - Budget Q3: 600K€
   - Réel Q3: 750K€
   - Écart: +150K€
   
   Causes:
   - Campagne lancement produit non budgetée: +100K€
   - Events & conférences: +30K€
   - Agence créative: +20K€

2. R&D: +8% vs budget (acceptable)
3. Autres CCs: conformes

🎯 Impact annuel: Si maintenu, dépassement total = +600K€
```

### Actions

Marie convoque le CMO :
- **Analyse** : La campagne de lancement a généré 500 leads qualifiés
- **ROI projeté** : 1.2M€ de pipeline (ROI +240%)
- **Décision** : Approuver le dépassement MAIS compenser par réduction Q4

**Question de suivi** :
> *"Quel est le ROI de la campagne lancement produit ?"*

**Réponse** :
```
Campagne "New Product Launch" (Juillet-Août):
- Investissement: 100K€
- Leads générés: 500
- Conversions à date: 35 deals
- Revenue généré: 280K€
- Pipeline qualifié: 1.2M€ (taux conversion attendu: 30%)

ROI actuel: +180% (280K€ / 100K€)
ROI projeté: +360% (360K€ / 100K€)

✅ Campagne performante, investissement justifié
```

Marie valide le reforecast Q3-Q4 avec ajustement budget Marketing.

---

## Acte 4 : Q4 - Crise du Cash Flow

### Situation (Novembre-Décembre 2025)

En novembre, Marie reçoit une alerte de la trésorière : le cash est tendu.

**Question au Data Agent** :
> *"Quel est le DSO actuel et pourquoi a-t-il augmenté ?"*

**Réponse** :
```
⚠️ DSO actuel: 62 jours (vs cible 45 jours)

Évolution DSO:
- Q1: 42 jours ✅
- Q2: 46 jours ⚠️
- Q3: 53 jours ⚠️
- Q4: 62 jours ❌ (+17 jours vs cible)

Causes:
1. Clients Enterprise en retard:
   - Company 0042 SA: 850K€ à 90 jours (normalement 60 jours)
   - Company 0078 GmbH: 620K€ à 75 jours
   - Company 0125 Ltd: 480K€ à 68 jours
   
2. Augmentation des ventes à crédit (60 jours) vs 30 jours

Impact cash: -1.8M€ de manque à gagner (AR retardées)
```

### Actions

**Question de suivi** :
> *"Quels clients ont plus de 500K€ en retard de paiement ?"*

**Réponse** :
```
Top 5 clients en retard (>500K€):

1. Company 0042 SA
   - Montant dû: 850K€
   - Retard moyen: 30 jours
   - Segment: Enterprise
   - Action: Appel CFO-to-CFO, plan de paiement

2. Company 0078 GmbH
   - Montant dû: 620K€
   - Retard moyen: 15 jours
   - Segment: Enterprise
   - Action: Relance Account Manager

3. Company 0125 Ltd
   - Montant dû: 480K€
   - Retard moyen: 8 jours
   - Segment: Mid-Market
   - Action: Email de relance automatique

Total AR >60 jours: 2.1M€
```

Marie lance un plan d'action :
- **Action 1** : Relances personnalisées CFO-to-CFO (top 3 clients)
- **Action 2** : Négociation plan de paiement échelonné
- **Action 3** : Policy future : pas de crédit >45 jours pour nouveaux clients

**Résultat** : En décembre, 1.2M€ encaissés, DSO redescend à 55 jours.

---

## Acte 5 : Clôture Annuelle - Bilan 2025

### Situation (Fin Décembre 2025)

Marie prépare le board meeting de clôture annuelle.

**Question au Data Agent** :
> *"Affiche le P&L annuel 2025 et compare au budget"*

**Réponse** :
```
P&L 2025 - Actuel vs Budget:

Revenue:
- Actual: 31.2M€
- Budget: 30.0M€
- Variance: +1.2M€ (+4%) ✅

COGS:
- Actual: 8.9M€ (28.5%)
- Budget: 8.4M€ (28%)
- Variance: +500K€ (+6%) ⚠️ (prix discount Q2)

Gross Margin:
- Actual: 22.3M€ (71.5%)
- Budget: 21.6M€ (72%)
- Variance: +700K€ ✅ mais marge % légèrement en-dessous

Operating Expenses:
- Actual: 17.8M€
- Budget: 17.0M€
- Variance: +800K€ (+5%) ⚠️ (Marketing +600K€)

EBITDA:
- Actual: 4.5M€ (14.4%)
- Budget: 4.6M€ (15.3%)
- Variance: -100K€ (-2%) ⚠️

Net Profit:
- Actual: 2.8M€ (9.0%)
- Budget: 3.0M€ (10%)
- Variance: -200K€ (-7%) ⚠️

🎯 Analyse:
✅ Revenue: objectif dépassé
⚠️ Marge: légèrement dégradée (guerre des prix Q2)
⚠️ Opex: dépassement Marketing compensé par valeur pipeline
⚠️ Bottom line: -200K€ vs plan mais croissance +25% vs 2024
```

### Présentation au Board

Marie présente 3 slides :

**Slide 1 : Réussites**
- ✅ Revenue +4% vs budget (+25% vs 2024)
- ✅ Marge brute maintenue à 71.5%
- ✅ Investissement Marketing ROI +240%

**Slide 2 : Défis surmontés**
- ⚠️ Baisse marge Q2 → corrigée en Q3
- ⚠️ Dépassement budget Marketing → ROI validé
- ⚠️ DSO dégradé Q4 → actions en cours

**Slide 3 : Plan 2026**
- Objectif revenue : 38M€ (+22%)
- Objectif marge brute : 73%
- DSO cible : 42 jours
- Budget R&D : +30% (innovation produit)

Le board approuve le plan 2026.

---

## 🎯 Leçons Apprises

### 1. Data-Driven Decision Making
Marie a utilisé le Data Agent pour :
- Identifier la cause de la baisse de marge (remises)
- Valider le ROI du dépassement Marketing
- Prioriser les relances clients (AR management)

**Impact** : Décisions prises en quelques minutes (vs plusieurs jours d'analyse manuelle).

### 2. Proactivité vs Réactivité
Les alertes automatiques ont permis de détecter :
- La dégradation de marge dès avril (pas septembre)
- Le dépassement Marketing dès juillet (pas décembre)
- L'augmentation DSO dès octobre (pas après clôture)

**Impact** : Actions correctives immédiates, pas de surprise en fin d'année.

### 3. Collaboration Finance-Métier
Le Data Agent a facilité :
- Les discussions CFO ↔ CMO (données objectives)
- Les alignements CFO ↔ Sales (pricing)
- Les relances CFO ↔ Clients (AR management)

**Impact** : Finance devient un business partner (pas juste un contrôleur).

---

## 📊 Métriques Clés de la Démo

| Métrique | Q1 | Q2 | Q3 | Q4 | Année |
|----------|----|----|----|----|-------|
| Revenue (M€) | 7.5 | 8.1 | 7.8 | 7.8 | 31.2 |
| Gross Margin % | 72% | 67% | 70% | 73% | 71.5% |
| EBITDA % | 16% | 12% | 14% | 15% | 14.4% |
| DSO (jours) | 42 | 46 | 53 | 62 | 55 |
| Budget Variance % | +2% | -5% | +8% | +3% | +5% |

---

**Cette story démontre comment un Data Agent transforme le pilotage financier : de la donnée à l'action en quelques secondes.** 🚀
