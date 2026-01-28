# GitHub Copilot Agents Configuration

Ce fichier configure les agents GitHub Copilot spécifiques au scénario Finance Performance Management.

## Agent Finance Controller

**Rôle** : Assistant CFO pour analyses financières

**Compétences** :
- Analyse P&L (Profit & Loss)
- Budget vs Actual analysis
- Variance explanations
- DSO et cash flow analysis
- Cost allocation

**Instructions système** :
Voir [`docs/data_agent_instructions.md`](docs/data_agent_instructions.md)

**Exemples de questions** :
- "Pourquoi la marge brute baisse ce trimestre ?"
- "Quels centres de coûts ont dépassé leur budget ?"
- "Quel est le DSO actuel ?"
- "Affiche le P&L consolidé"

## Configuration Fabric Data Agent

Lors du déploiement dans Microsoft Fabric, configurer le Data Agent avec :
- **Nom** : Finance_Controller
- **Source** : Semantic Model Finance
- **Instructions** : Coller le contenu de `data_agent_instructions.md`
- **Exemples** : Utiliser `data_agent_examples.md` pour tests

## Tests Recommandés

Utiliser les 25 questions de [`docs/data_agent_examples.md`](docs/data_agent_examples.md) pour valider :
- ✅ Calculs de marges corrects
- ✅ Écarts budget/réel expliqués
- ✅ DSO et retards de paiement identifiés
- ✅ Analyses cross-domain (produits × clients × régions)
