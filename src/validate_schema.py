"""
Script de Validation des Noms de Colonnes - Finance Performance Management Demo

Vérifie que tous les noms de colonnes correspondent au schéma attendu
et que les données sont cohérentes pour les DAX queries.

Usage:
    cd src
    python validate_schema.py
"""

import pandas as pd
import sys
from pathlib import Path

class SchemaValidator:
    def __init__(self, data_root='../data/raw'):
        self.data_root = Path(data_root)
        self.errors = []
        self.warnings = []
        
    def validate_all(self):
        """Exécute toutes les validations"""
        print("=" * 80)
        print("VALIDATION DES SCHEMAS - Finance Performance Management Demo")
        print("=" * 80)
        print()
        
        # Validation des tables Finance
        self.validate_finance_tables()
        
        # Validation des tables Dimensions
        self.validate_dimension_tables()
        
        # Validation des relations
        self.validate_relationships()
        
        # Afficher le résumé
        self.print_summary()
        
        return len(self.errors) == 0
    
    def validate_finance_tables(self):
        """Valide les tables Finance"""
        print("--- Validation Finance Tables ---")
        
        # actuals (CRITIQUE pour P&L)
        actuals = self.load_csv('finance/actuals.csv')
        if actuals is not None:
            self.check_columns(actuals, 'actuals', [
                'transaction_id', 'account_id', 'cost_center_id', 'period_date',
                'amount', 'currency'
            ])
            
            # Vérifier amount (pas de NULL)
            if 'amount' in actuals.columns:
                null_amounts = actuals['amount'].isna().sum()
                if null_amounts > 0:
                    self.errors.append(
                        f"actuals.amount contient {null_amounts} valeurs NULL"
                    )
        
        # budget (CRITIQUE pour Variance Analysis)
        budget = self.load_csv('finance/budget.csv')
        if budget is not None:
            self.check_columns(budget, 'budget', [
                'budget_id', 'account_id', 'cost_center_id', 'period_date',
                'amount', 'version'
            ])
        
        # invoices (CRITIQUE pour DSO)
        invoices = self.load_csv('finance/invoices.csv')
        if invoices is not None:
            self.check_columns(invoices, 'invoices', [
                'invoice_id', 'customer_id', 'invoice_date', 'due_date',
                'amount', 'paid_date', 'status'
            ])
            
            # Vérifier paid_date nullable (CRITIQUE pour DSO)
            if 'paid_date' in invoices.columns:
                null_pct = invoices['paid_date'].isna().sum() / len(invoices)
                print(f"  ℹ️  Invoices non payées: {null_pct*100:.1f}% (paid_date NULL)")
                
                if null_pct == 0:
                    self.warnings.append(
                        "invoices.paid_date: aucune valeur NULL trouvée. "
                        "Vérifier si toutes les invoices sont payées."
                    )
        
        # payments
        payments = self.load_csv('finance/payments.csv')
        if payments is not None:
            self.check_columns(payments, 'payments', [
                'payment_id', 'invoice_id', 'payment_date', 'amount', 'method'
            ])
        
        print()
    
    def validate_dimension_tables(self):
        """Valide les tables de dimensions"""
        print("--- Validation Dimension Tables ---")
        
        # accounts (Chart of Accounts)
        accounts = self.load_csv('finance/accounts.csv')
        if accounts is not None:
            self.check_columns(accounts, 'accounts', [
                'account_id', 'account_name', 'account_type', 'category'
            ])
            
            # Vérifier account_type values
            if 'account_type' in accounts.columns:
                account_types = accounts['account_type'].unique()
                print(f"  ℹ️  Account types: {list(account_types)}")
        
        # cost_centers
        cost_centers = self.load_csv('finance/cost_centers.csv')
        if cost_centers is not None:
            self.check_columns(cost_centers, 'cost_centers', [
                'cost_center_id', 'cost_center_name', 'department', 'manager'
            ])
        
        # customers
        customers = self.load_csv('finance/customers.csv')
        if customers is not None:
            self.check_columns(customers, 'customers', [
                'customer_id', 'customer_name', 'country', 'segment'
            ])
        
        print()
    
    def validate_relationships(self):
        """Valide les relations entre tables (foreign keys)"""
        print("--- Validation Relations (Foreign Keys) ---")
        
        # Charger les tables principales
        actuals = self.load_csv('finance/actuals.csv')
        budget = self.load_csv('finance/budget.csv')
        accounts = self.load_csv('finance/accounts.csv')
        cost_centers = self.load_csv('finance/cost_centers.csv')
        
        if actuals is None or accounts is None or cost_centers is None:
            self.errors.append("Impossible de valider les relations: tables manquantes")
            return
        
        # Vérifier actuals.account_id → accounts.account_id
        invalid_accounts = ~actuals['account_id'].isin(accounts['account_id'])
        if invalid_accounts.any():
            self.errors.append(
                f"{invalid_accounts.sum()} actuals avec account_id invalide"
            )
        else:
            print(f"  ✅ actuals.account_id → accounts.account_id (100% valide)")
        
        # Vérifier actuals.cost_center_id → cost_centers.cost_center_id
        invalid_cc = ~actuals['cost_center_id'].isin(cost_centers['cost_center_id'])
        if invalid_cc.any():
            self.errors.append(
                f"{invalid_cc.sum()} actuals avec cost_center_id invalide"
            )
        else:
            print(f"  ✅ actuals.cost_center_id → cost_centers.cost_center_id (100% valide)")
        
        # Vérifier budget.account_id → accounts.account_id
        if budget is not None:
            invalid_budget_accounts = ~budget['account_id'].isin(accounts['account_id'])
            if invalid_budget_accounts.any():
                self.errors.append(
                    f"{invalid_budget_accounts.sum()} budget avec account_id invalide"
                )
            else:
                print(f"  ✅ budget.account_id → accounts.account_id (100% valide)")
        
        print()
    
    def check_columns(self, df, table_name, expected_columns):
        """Vérifie que les colonnes attendues sont présentes"""
        missing = set(expected_columns) - set(df.columns)
        extra = set(df.columns) - set(expected_columns)
        
        if missing:
            self.errors.append(f"{table_name}: colonnes manquantes: {missing}")
        
        if extra:
            self.warnings.append(f"{table_name}: colonnes inattendues: {extra}")
        
        if not missing and not extra:
            print(f"  ✅ {table_name}: {len(expected_columns)} colonnes valides")
    
    def load_csv(self, relative_path):
        """Charge un CSV et gère les erreurs"""
        filepath = self.data_root / relative_path
        
        if not filepath.exists():
            self.errors.append(f"Fichier manquant: {filepath}")
            return None
        
        try:
            return pd.read_csv(filepath, encoding='utf-8')
        except Exception as e:
            self.errors.append(f"Erreur lecture {filepath}: {e}")
            return None
    
    def print_summary(self):
        """Affiche le résumé des validations"""
        print("=" * 80)
        print("RÉSUMÉ DE VALIDATION")
        print("=" * 80)
        
        if self.warnings:
            print(f"\n⚠️  {len(self.warnings)} AVERTISSEMENT(S):")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        if self.errors:
            print(f"\n❌ {len(self.errors)} ERREUR(S):")
            for error in self.errors:
                print(f"  - {error}")
            print("\n🔧 ACTIONS REQUISES:")
            print("  1. Corriger les erreurs listées ci-dessus")
            print("  2. Régénérer les données avec generate_data.py")
            print("  3. Relancer ce script de validation")
            print("\n❌ VALIDATION ÉCHOUÉE")
        else:
            print("\n✅ VALIDATION RÉUSSIE - Tous les schémas sont corrects !")
            print("\n✅ Les DAX queries devraient fonctionner correctement.")
        
        print("=" * 80)


def main():
    """Point d'entrée principal"""
    validator = SchemaValidator()
    success = validator.validate_all()
    
    # Exit code pour CI/CD
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
