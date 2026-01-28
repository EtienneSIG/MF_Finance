# Exemples de Questions pour Fabric Data Agent (Finance)

## 🎯 Objectif

Ce document fournit **25 exemples de questions** avec les **réponses attendues** pour tester et valider le Fabric Data Agent dans le contexte Finance Performance Management.

Chaque exemple inclut :
- La question posée
- La réponse attendue (format et contenu)
- Les tables utilisées
- Le type de visualisation suggéré

---

## 📊 Catégorie 1 : P&L Analysis (5 questions)

### 1. Quel est le chiffre d'affaires total de l'année ?

**Réponse attendue** :
> Revenue 2025 : **31.2M€**
> 
> Répartition par trimestre :
> - Q1 : 7.5M€ (24%)
> - Q2 : 8.1M€ (26%)
> - Q3 : 7.8M€ (25%)
> - Q4 : 7.8M€ (25%)
> 
> *Source : `invoice_lines`*

**Tables** : `invoice_lines`  
**Visualisation** : Card + Bar chart trimestriel  
**Complexité** : ⭐ (simple)

---

### 2. Quelle est la marge brute globale ?

**Réponse attendue** :
> Gross Margin 2025 : **71.5%**
> 
> Détail :
> - Revenue : 31.2M€
> - COGS : 8.9M€ (28.5%)
> - Gross Margin : 22.3M€ (71.5%)
> 
> Par catégorie produit :
> - Software Licenses : 85%
> - Maintenance : 70%
> - Training : 50%
> - Professional Services : 40%
> 
> *Source : `invoice_lines`, `products`*

**Tables** : `invoice_lines`, `products`  
**Visualisation** : Card + Donut chart par catégorie  
**Complexité** : ⭐⭐ (calcul + jointure)

---

### 3. Affiche le P&L consolidé annuel

**Réponse attendue** :
> **P&L 2025** :
> 
> | Ligne | Montant | % Revenue |
> |-------|---------|-----------|
> | Revenue | 31.2M€ | 100% |
> | COGS | (8.9M€) | -28.5% |
> | **Gross Margin** | **22.3M€** | **71.5%** |
> | Operating Expenses | (17.8M€) | -57% |
> | **EBITDA** | **4.5M€** | **14.4%** |
> | Net Profit | 2.8M€ | 9.0% |
> 
> *Source : `invoice_lines`, `general_ledger`, `chart_of_accounts`*

**Tables** : `invoice_lines`, `general_ledger`, `chart_of_accounts`  
**Visualisation** : Waterfall chart  
**Complexité** : ⭐⭐⭐ (calculs multiples)

---

### 4. Quel trimestre a la meilleure marge brute ?

**Réponse attendue** :
> **Q4** a la meilleure marge brute : **73%**
> 
> Évolution par trimestre :
> - Q1 : 72%
> - Q2 : 67% (baisse due aux remises)
> - Q3 : 70% (récupération)
> - Q4 : 73% (pic annuel)
> 
> *Source : `invoice_lines` par trimestre*

**Tables** : `invoice_lines`  
**Visualisation** : Line chart  
**Complexité** : ⭐⭐ (agrégation temporelle)

---

### 5. Quelle catégorie de produit génère le plus de revenue ?

**Réponse attendue** :
> **Software Licenses** génère le plus de revenue : **14.5M€** (46.5% du total)
> 
> Répartition par catégorie :
> 1. Software Licenses : 14.5M€ (46.5%)
> 2. Professional Services : 9.2M€ (29.5%)
> 3. Maintenance : 5.1M€ (16.3%)
> 4. Training : 2.4M€ (7.7%)
> 
> *Source : `invoice_lines`, `products`*

**Tables** : `invoice_lines`, `products`  
**Visualisation** : Donut chart  
**Complexité** : ⭐⭐ (jointure + agrégation)

---

## 💰 Catégorie 2 : Budget vs Actual (5 questions)

### 6. Quels centres de coûts ont dépassé leur budget ?

**Réponse attendue** :
> **2 centres de coûts** en dépassement :
> 
> 1. **Marketing** : +25% (Unfavorable)
>    - Budget : 2.4M€
>    - Actual : 3.0M€
>    - Écart : +600K€
> 
> 2. **R&D** : +8% (Unfavorable)
>    - Budget : 4.8M€
>    - Actual : 5.2M€
>    - Écart : +400K€
> 
> Tous autres CCs : conformes (±5%)
> 
> *Source : `budgets`, `general_ledger`, `cost_centers`*

**Tables** : `budgets`, `general_ledger`, `cost_centers`  
**Visualisation** : Bar chart variance  
**Complexité** : ⭐⭐⭐ (jointures + calcul variance)

---

### 7. Quel est l'écart global budget vs réel ?

**Réponse attendue** :
> Écart global 2025 : **+5%** (Unfavorable)
> 
> - Budget total : 17.0M€
> - Actual total : 17.8M€
> - Variance : +800K€ (+5%)
> 
> Décomposition :
> - Marketing : +600K€
> - R&D : +400K€
> - Autres CCs : -200K€ (économies)
> 
> *Source : `budgets`, `general_ledger`*

**Tables** : `budgets`, `general_ledger`  
**Visualisation** : Card + Waterfall chart  
**Complexité** : ⭐⭐ (sommes + calcul)

---

### 8. Pourquoi le Marketing a dépassé son budget en Q3 ?

**Réponse attendue** :
> ⚠️ Marketing Q3 : **+25% vs budget**
> 
> Budget Q3 : 600K€  
> Actual Q3 : 750K€  
> Écart : +150K€ (Unfavorable)
> 
> Causes identifiées :
> 1. Campagne lancement produit (non budgetée) : +100K€
> 2. Events & conférences : +30K€
> 3. Agence créative : +20K€
> 
> *Impact annuel : +600K€ si maintenu*
> 
> *Source : `budgets`, `general_ledger` filtre Q3 + Marketing*

**Tables** : `budgets`, `general_ledger`, `cost_centers`  
**Visualisation** : Variance analysis table  
**Complexité** : ⭐⭐⭐⭐ (filtre période + drill-down)

---

### 9. Affiche les variances par mois pour Sales France

**Réponse attendue** :
> Variances Budget vs Actual - Sales France (2025) :
> 
> | Mois | Budget | Actual | Variance % | Status |
> |------|--------|--------|------------|--------|
> | Jan | 180K€ | 175K€ | -2.8% | ✅ Favorable |
> | Fev | 180K€ | 185K€ | +2.8% | ⚠️ Unfavorable |
> | Mar | 200K€ | 195K€ | -2.5% | ✅ Favorable |
> | ... | ... | ... | ... | ... |
> | Dec | 220K€ | 230K€ | +4.5% | ⚠️ Unfavorable |
> 
> *Source : `budgets`, `general_ledger` filtre CC_001 (Sales France)*

**Tables** : `budgets`, `general_ledger`, `cost_centers`  
**Visualisation** : Line chart mensuel  
**Complexité** : ⭐⭐⭐ (filtre CC + temporalité)

---

### 10. Compare le budget vs forecast vs réel pour Q4

**Réponse attendue** :
> **Comparaison Q4 2025** :
> 
> | Métrique | Budget | Forecast Q3 | Actual | Variance Budget | Variance Forecast |
> |----------|--------|-------------|--------|-----------------|-------------------|
> | Total | 4.2M€ | 4.5M€ | 4.6M€ | +9.5% | +2.2% |
> 
> Analyse :
> - Budget sous-estimé de 400K€
> - Forecast Q3 plus précis (écart +100K€)
> - Accuracy du forecast : 97.8%
> 
> *Source : `budgets`, `forecasts`, `general_ledger`*

**Tables** : `budgets`, `forecasts`, `general_ledger`  
**Visualisation** : Comparison bar chart  
**Complexité** : ⭐⭐⭐⭐ (3 sources + calculs)

---

## 💳 Catégorie 3 : Cash Flow & DSO (5 questions)

### 11. Quel est le DSO actuel ?

**Réponse attendue** :
> **DSO actuel : 62 jours** (vs cible 45 jours)
> 
> Calcul :
> - Accounts Receivable : 5.3M€
> - Revenue annualisé : 31.2M€
> - DSO : (5.3 / 31.2) × 365 = 62 jours
> 
> Aging AR :
> - 0-30 jours : 2.1M€ (40%)
> - 31-60 jours : 1.8M€ (34%)
> - 61-90 jours : 1.1M€ (21%)
> - >90 jours : 300K€ (5%)
> 
> *Source : `invoices`, `payments`*

**Tables** : `invoices`, `payments`  
**Visualisation** : Gauge + Aging bar chart  
**Complexité** : ⭐⭐⭐⭐ (calcul DSO + aging)

---

### 12. Quels clients ont plus de 500K€ en retard de paiement ?

**Réponse attendue** :
> **3 clients** > 500K€ en retard :
> 
> 1. **Company 0042 SA**
>    - Montant dû : 850K€
>    - Retard moyen : 30 jours
>    - Segment : Enterprise
> 
> 2. **Company 0078 GmbH**
>    - Montant dû : 620K€
>    - Retard moyen : 15 jours
>    - Segment : Enterprise
> 
> 3. **Company 0125 Ltd**
>    - Montant dû : 480K€
>    - Retard moyen : 8 jours
>    - Segment : Mid-Market
> 
> Total AR >500K€ : 1.95M€
> 
> *Source : `invoices`, `payments`, `customers`*

**Tables** : `invoices`, `payments`, `customers`  
**Visualisation** : Table avec highlight  
**Complexité** : ⭐⭐⭐⭐ (jointures + filtres)

---

### 13. Pourquoi le DSO a augmenté en Q4 ?

**Réponse attendue** :
> ⚠️ **DSO Q4 : 62 jours** (vs 42 jours en Q1) → **+20 jours**
> 
> Causes identifiées :
> 1. **Clients Enterprise en retard** : 60-90 jours au lieu de 60 jours
>    - Impact : +12 jours de DSO
> 
> 2. **Augmentation du crédit 60 jours** : +30% des ventes
>    - Impact : +5 jours de DSO
> 
> 3. **Mix client** : Plus d'Enterprise (payment terms 60j) vs SMB (30j)
>    - Impact : +3 jours de DSO
> 
> *Impact cash : -1.8M€ de manque à gagner*
> 
> *Source : `invoices`, `payments`, `customers`*

**Tables** : `invoices`, `payments`, `customers`  
**Visualisation** : Waterfall chart impact  
**Complexité** : ⭐⭐⭐⭐⭐ (analyse multi-facteurs)

---

### 14. Quel est le montant total des créances en retard (>60 jours) ?

**Réponse attendue** :
> **Créances >60 jours : 2.1M€** (40% de l'AR total)
> 
> Détail par tranche :
> - 61-90 jours : 1.1M€ (52%)
> - 91-120 jours : 750K€ (36%)
> - >120 jours : 250K€ (12%)
> 
> Top 5 clients concernés :
> 1. Company 0042 SA : 850K€
> 2. Company 0078 GmbH : 620K€
> 3. Company 0125 Ltd : 280K€
> 4. Company 0156 Inc : 190K€
> 5. Company 0089 Corp : 160K€
> 
> *Source : `invoices`, `payments`*

**Tables** : `invoices`, `payments`, `customers`  
**Visualisation** : Donut chart aging + Table  
**Complexité** : ⭐⭐⭐ (filtre date + agrégation)

---

### 15. Affiche l'évolution du DSO par trimestre

**Réponse attendue** :
> **Évolution DSO 2025** :
> 
> | Trimestre | DSO | Variation | Status |
> |-----------|-----|-----------|--------|
> | Q1 | 42 jours | - | ✅ Cible atteinte |
> | Q2 | 46 jours | +4 | ⚠️ Dégradation |
> | Q3 | 53 jours | +7 | ⚠️ Alerte |
> | Q4 | 62 jours | +9 | ❌ Hors cible |
> 
> Tendance : Dégradation progressive (+20 jours sur l'année)
> 
> *Source : `invoices`, `payments` par trimestre*

**Tables** : `invoices`, `payments`  
**Visualisation** : Line chart avec seuil cible  
**Complexité** : ⭐⭐⭐ (temporalité + calcul DSO)

---

## 📈 Catégorie 4 : Analyse de Marge (5 questions)

### 16. Pourquoi la marge brute baisse en Q2 ?

**Réponse attendue** :
> ⚠️ **Marge brute Q2 : 67%** (vs 72% en Q1) → **-5 points**
> 
> Causes identifiées :
> 1. **Remises agressives** : +8% de discount moyen (vs 5% en Q1)
>    - Impact : -2.5 points de marge
> 
> 2. **Mix produit** : Hausse Professional Services (marge 40%) au détriment Software Licenses (marge 85%)
>    - Impact : -1.5 points de marge
> 
> 3. **Prix moyen** : -12% sur Software Licenses (guerre des prix)
>    - Impact : -1 point de marge
> 
> **Impact revenue** : +2.1M€ (bon)  
> **Impact marge** : -450K€ (mauvais)
> 
> *Source : `invoice_lines`, `products`*

**Tables** : `invoice_lines`, `products`  
**Visualisation** : Variance analysis waterfall  
**Complexité** : ⭐⭐⭐⭐⭐ (analyse multi-facteurs)

---

### 17. Quelle catégorie de produit a la meilleure marge ?

**Réponse attendue** :
> **Software Licenses** a la meilleure marge : **85%**
> 
> Classement par marge :
> 1. Software Licenses : 85%
> 2. Maintenance : 70%
> 3. Training : 50%
> 4. Professional Services : 40%
> 
> Contribution au Gross Margin total :
> - Software Licenses : 12.3M€ (55%)
> - Maintenance : 3.6M€ (16%)
> - Training : 1.2M€ (5%)
> - Professional Services : 3.7M€ (17%)
> - Autres : 1.5M€ (7%)
> 
> *Source : `invoice_lines`, `products`*

**Tables** : `invoice_lines`, `products`  
**Visualisation** : Bar chart marge % + Donut contribution  
**Complexité** : ⭐⭐ (jointure + calcul marge)

---

### 18. Quel client génère le plus de marge brute ?

**Réponse attendue** :
> Top 5 clients par Gross Margin :
> 
> 1. **Company 0042 SA** : 1.2M€ (marge 78%)
>    - Revenue : 1.54M€
>    - Segment : Enterprise
> 
> 2. **Company 0078 GmbH** : 890K€ (marge 75%)
>    - Revenue : 1.19M€
>    - Segment : Enterprise
> 
> 3. **Company 0125 Ltd** : 720K€ (marge 72%)
>    - Revenue : 1.0M€
>    - Segment : Mid-Market
> 
> 4. **Company 0156 Inc** : 680K€ (marge 74%)
>    - Revenue : 920K€
>    - Segment : Enterprise
> 
> 5. **Company 0089 Corp** : 620K€ (marge 70%)
>    - Revenue : 886K€
>    - Segment : Mid-Market
> 
> *Source : `invoice_lines`, `invoices`, `customers`, `products`*

**Tables** : `invoice_lines`, `invoices`, `customers`, `products`  
**Visualisation** : Table avec highlight  
**Complexité** : ⭐⭐⭐⭐ (jointures multiples + calculs)

---

### 19. Compare la marge brute par segment client

**Réponse attendue** :
> **Marge brute par segment** :
> 
> | Segment | Revenue | Gross Margin | Margin % | Clients |
> |---------|---------|--------------|----------|---------|
> | Enterprise | 15.6M€ | 11.8M€ | 75.6% | 50 |
> | Mid-Market | 10.4M€ | 7.3M€ | 70.2% | 150 |
> | SMB | 5.2M€ | 3.2M€ | 61.5% | 300 |
> 
> **Analyse** :
> - Enterprise : Meilleure marge (achètent plus de licences)
> - SMB : Marge plus faible (demandent plus de services)
> 
> *Source : `invoice_lines`, `invoices`, `customers`, `products`*

**Tables** : `invoice_lines`, `invoices`, `customers`, `products`  
**Visualisation** : Comparison bar chart  
**Complexité** : ⭐⭐⭐⭐ (jointures + groupby)

---

### 20. Affiche la rentabilité par centre de coûts

**Réponse attendue** :
> **Rentabilité par centre de coûts (2025)** :
> 
> **Revenue Centers** :
> | CC | Revenue | Costs | Profit | Margin % |
> |----|---------|-------|--------|----------|
> | Sales France | 12.5M€ | 1.8M€ | 10.7M€ | 85.6% |
> | Sales EMEA | 10.2M€ | 1.5M€ | 8.7M€ | 85.3% |
> | Sales AMER | 8.5M€ | 1.3M€ | 7.2M€ | 84.7% |
> 
> **Cost Centers** :
> | CC | Costs | Budget | Variance |
> |----|-------|--------|----------|
> | Marketing | 3.0M€ | 2.4M€ | +25% |
> | R&D | 5.2M€ | 4.8M€ | +8% |
> | Customer Success | 1.8M€ | 1.7M€ | +6% |
> 
> *Source : `general_ledger`, `cost_centers`, `invoice_lines`*

**Tables** : `general_ledger`, `cost_centers`, `invoice_lines`  
**Visualisation** : Table multi-sections  
**Complexité** : ⭐⭐⭐⭐⭐ (segmentation revenue vs cost)

---

## 🔗 Catégorie 5 : Questions Cross-Domain (5 questions avancées)

### 21. Quels produits génèrent le plus d'Operating Expenses ?

**Réponse attendue** :
> Top 3 produits par Opex alloué :
> 
> 1. **Professional Services** : 4.2M€
>    - R&D : 1.8M€
>    - Delivery : 2.0M€
>    - Support : 400K€
> 
> 2. **Software Licenses** : 3.8M€
>    - R&D : 2.5M€
>    - Sales : 900K€
>    - Marketing : 400K€
> 
> 3. **Maintenance** : 2.1M€
>    - Support : 1.2M€
>    - IT : 600K€
>    - Admin : 300K€
> 
> *Source : `allocations`, `general_ledger`, `products`*

**Tables** : `allocations`, `general_ledger`, `products`, `cost_centers`  
**Visualisation** : Stacked bar chart  
**Complexité** : ⭐⭐⭐⭐⭐ (allocations indirectes)

---

### 22. Affiche le P&L par segment client

**Réponse attendue** :
> **P&L par segment (2025)** :
> 
> | Métrique | Enterprise | Mid-Market | SMB |
> |----------|------------|------------|-----|
> | Revenue | 15.6M€ (50%) | 10.4M€ (33%) | 5.2M€ (17%) |
> | COGS | (3.8M€) | (3.1M€) | (2.0M€) |
> | Gross Margin | 11.8M€ (76%) | 7.3M€ (70%) | 3.2M€ (62%) |
> | Opex Allocated | (7.8M€) | (6.2M€) | (3.8M€) |
> | EBITDA | 4.0M€ (26%) | 1.1M€ (11%) | -600K€ (-12%) |
> 
> **Insight** : SMB non rentable (coût d'acquisition élevé)
> 
> *Source : Toutes tables*

**Tables** : Toutes (cross-domain complet)  
**Visualisation** : Table comparative multi-colonnes  
**Complexité** : ⭐⭐⭐⭐⭐ (P&L complet segmenté)

---

### 23. Quels clients Enterprise ont une marge <60% ?

**Réponse attendue** :
> **5 clients Enterprise** avec marge <60% :
> 
> 1. Company 0203 SA : 58% (beaucoup de services)
> 2. Company 0187 GmbH : 56% (remises agressives)
> 3. Company 0245 Ltd : 54% (mix produit défavorable)
> 4. Company 0112 Inc : 52% (prix réduits)
> 5. Company 0298 Corp : 50% (100% services)
> 
> **Action recommandée** : Revoir pricing ou mix produit
> 
> *Source : `invoice_lines`, `invoices`, `customers`, `products`*

**Tables** : `invoice_lines`, `invoices`, `customers`, `products`  
**Visualisation** : Table avec alerte  
**Complexité** : ⭐⭐⭐⭐ (filtres multiples)

---

### 24. Compare Budget vs Actual vs Forecast pour l'année

**Réponse attendue** :
> **Comparaison annuelle 2025** :
> 
> | Métrique | Budget | Forecast Q3 | Actual | Var Budget | Var Forecast |
> |----------|--------|-------------|--------|------------|--------------|
> | Revenue | 30.0M€ | 31.0M€ | 31.2M€ | +4.0% | +0.6% |
> | Opex | 17.0M€ | 17.5M€ | 17.8M€ | +4.7% | +1.7% |
> | EBITDA | 4.6M€ | 4.7M€ | 4.5M€ | -2.2% | -4.3% |
> 
> **Analyse** :
> - Revenue : Forecast plus précis que Budget
> - Opex : Dépassements non anticipés au forecast
> - EBITDA : Légèrement en-dessous des 2 références
> 
> *Source : `budgets`, `forecasts`, `general_ledger`, `invoice_lines`*

**Tables** : `budgets`, `forecasts`, `general_ledger`, `invoice_lines`  
**Visualisation** : Comparison chart 3 colonnes  
**Complexité** : ⭐⭐⭐⭐⭐ (3 sources + calculs)

---

### 25. Quel est le ROI de la campagne Marketing lancée en Q3 ?

**Réponse attendue** :
> **ROI Campagne Lancement Produit (Q3)** :
> 
> Investissement : 100K€ (dépassement budget)
> 
> Résultats :
> - Leads générés : 500
> - Conversions à date : 35 deals
> - Revenue généré : 280K€
> - Pipeline qualifié : 1.2M€ (taux conversion 30%)
> 
> **ROI actuel** : +180% (280K€ / 100K€)  
> **ROI projeté** : +360% (360K€ / 100K€)
> 
> ✅ **Conclusion** : Campagne performante, investissement justifié
> 
> *Source : `general_ledger` (Marketing Q3) + `invoice_lines` (revenue tracking)*

**Tables** : `general_ledger`, `cost_centers`, `invoice_lines`, `invoices`  
**Visualisation** : ROI card + Funnel chart  
**Complexité** : ⭐⭐⭐⭐⭐ (attribution marketing complexe)

---

## 📋 Guide d'Utilisation

### Comment Tester ces Questions

1. **Ordre recommandé** : Commencer par les questions simples (catégorie 1), puis augmenter la complexité
2. **Validation** : Vérifier que la réponse est cohérente (chiffres, calculs corrects)
3. **Flexibilité** : Reformuler si la première tentative échoue

### Critères de Succès

| Niveau | Questions réussies | Commentaire |
|--------|-------------------|-------------|
| ⭐ Basic | 15+/25 | Fonctionnel pour démo |
| ⭐⭐ Good | 20+/25 | Très bon niveau |
| ⭐⭐⭐ Excellent | 23+/25 | Production-ready |

### Troubleshooting

| Problème | Solution |
|----------|----------|
| Réponse incorrecte | Vérifier les relations et mesures DAX |
| Timeout | Filtrer sur période plus courte |
| "Je ne peux pas répondre" | Reformuler avec termes Finance exacts |
| Montants incohérents | Vérifier source de données (GL vs invoices) |

---

## 🎯 Scénarios de Démo Recommandés

### Scénario 1 : "CFO Monthly Review"
Questions à enchaîner : 1 → 2 → 3 → 6  
**Pitch** : Revue mensuelle CFO complète en 5 minutes

### Scénario 2 : "Budget Crisis Management"
Questions à enchaîner : 6 → 7 → 8 → 10  
**Pitch** : Identifier et expliquer les dépassements budgétaires

### Scénario 3 : "Cash Flow Alert"
Questions à enchaîner : 11 → 12 → 13 → 14  
**Pitch** : Analyser la dégradation du DSO et agir

### Scénario 4 : "Margin Investigation"
Questions à enchaîner : 16 → 17 → 18 → 19  
**Pitch** : Comprendre pourquoi la marge baisse et où

---

*Ces 25 exemples couvrent l'ensemble des cas d'usage Finance pour un Data Agent CFO-ready.*
