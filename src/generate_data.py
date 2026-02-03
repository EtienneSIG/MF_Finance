#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur de données Finance Performance Management pour Microsoft Fabric
Génère des données fictives pour démonstration Fabric Data Agent
"""

import csv
import random
import yaml
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any
import sys

# Configuration des chemins
SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / "config.yaml"
DATA_DIR = SCRIPT_DIR.parent / "data" / "raw"
FINANCE_DIR = DATA_DIR / "finance"
BUSINESS_DIR = DATA_DIR / "business"


def load_config() -> Dict[str, Any]:
    """Charge la configuration depuis config.yaml"""
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def generate_chart_of_accounts(config: Dict) -> List[Dict]:
    """Génère le plan comptable"""
    print("📊 Génération du plan comptable...")
    
    accounts = []
    account_id = 1000
    
    # Structure du plan comptable (norme française simplifiée)
    account_structure = {
        "1 - Actif": {
            "10 - Capital": ["Capital social", "Réserves", "Report à nouveau"],
            "11 - Immobilisations": ["Logiciels", "Matériel", "Mobilier", "Véhicules"],
            "12 - Stocks": ["Marchandises", "Produits finis"],
        },
        "2 - Passif": {
            "20 - Dettes fournisseurs": ["Fournisseurs"],
            "21 - Dettes fiscales": ["TVA à payer", "Charges sociales"],
            "22 - Emprunts": ["Emprunts bancaires"],
        },
        "4 - Trésorerie": {
            "40 - Banques": ["Compte courant", "Compte épargne"],
            "41 - Clients": ["Clients France", "Clients Export"],
            "42 - Fournisseurs": ["Fournisseurs"],
        },
        "6 - Charges": {
            "60 - Achats": ["Achats matières", "Sous-traitance"],
            "61 - Salaires": ["Salaires bruts", "Charges sociales", "Bonus"],
            "62 - Autres charges externes": ["Loyers", "Marketing", "Déplacements", "Cloud & IT", "Conseil"],
            "63 - Impôts et taxes": ["CFE", "Formation"],
            "64 - Charges financières": ["Intérêts emprunts"],
        },
        "7 - Produits": {
            "70 - Ventes": ["Software Licenses", "Professional Services", "Maintenance", "Training"],
            "71 - Production stockée": ["Production stockée"],
            "76 - Produits financiers": ["Intérêts perçus"],
        },
    }
    
    for main_category, sub_categories in account_structure.items():
        for sub_category, account_names in sub_categories.items():
            for account_name in account_names:
                account_type = "Asset" if main_category.startswith("1") else \
                              "Liability" if main_category.startswith("2") else \
                              "Equity" if main_category.startswith("1") else \
                              "Cash" if main_category.startswith("4") else \
                              "Expense" if main_category.startswith("6") else \
                              "Revenue"
                
                accounts.append({
                    'account_id': f'ACC_{account_id}',
                    'account_number': str(account_id),
                    'account_name': account_name,
                    'account_type': account_type,
                    'category': main_category,
                    'sub_category': sub_category,
                    'is_active': 'true',
                    'currency': config['output']['currency']
                })
                account_id += 1
    
    print(f"  ✓ {len(accounts)} comptes créés")
    return accounts


def generate_cost_centers(config: Dict) -> List[Dict]:
    """Génère les centres de coûts"""
    print("🏢 Génération des centres de coûts...")
    
    cost_centers_data = [
        {"name": "Sales France", "type": "Revenue", "region": "France", "budget_pct": 0.15},
        {"name": "Sales EMEA", "type": "Revenue", "region": "EMEA", "budget_pct": 0.12},
        {"name": "Sales AMER", "type": "Revenue", "region": "Americas", "budget_pct": 0.10},
        {"name": "Marketing", "type": "Support", "region": "Global", "budget_pct": 0.08},
        {"name": "Product Development", "type": "R&D", "region": "Global", "budget_pct": 0.20},
        {"name": "Customer Success", "type": "Support", "region": "Global", "budget_pct": 0.07},
        {"name": "Professional Services", "type": "Delivery", "region": "Global", "budget_pct": 0.10},
        {"name": "IT Infrastructure", "type": "Support", "region": "Global", "budget_pct": 0.05},
        {"name": "HR", "type": "Admin", "region": "Global", "budget_pct": 0.03},
        {"name": "Finance", "type": "Admin", "region": "Global", "budget_pct": 0.02},
        {"name": "Legal", "type": "Admin", "region": "Global", "budget_pct": 0.02},
        {"name": "Facilities", "type": "Admin", "region": "Global", "budget_pct": 0.02},
        {"name": "Executive", "type": "Admin", "region": "Global", "budget_pct": 0.04},
    ]
    
    cost_centers = []
    for idx, cc in enumerate(cost_centers_data, start=1):
        cost_centers.append({
            'cost_center_id': f'CC_{idx:03d}',
            'cost_center_name': cc['name'],
            'cost_center_type': cc['type'],
            'region': cc['region'],
            'manager': f'Manager {idx}',
            'budget_allocation_pct': cc['budget_pct'],
            'is_active': 'true'
        })
    
    print(f"  ✓ {len(cost_centers)} centres de coûts créés")
    return cost_centers


def generate_customers(config: Dict) -> List[Dict]:
    """Génère les clients"""
    print("👥 Génération des clients...")
    
    customers = []
    customer_count = config['customers']['count']
    segments = config['customers']['segments']
    
    company_suffixes = ["SAS", "SA", "SARL", "GmbH", "Ltd", "Inc", "Corp", "AG"]
    industries = ["Technology", "Retail", "Finance", "Healthcare", "Manufacturing", "Education", "Energy", "Telecom"]
    
    for i in range(1, customer_count + 1):
        # Déterminer le segment
        rand = random.random()
        cumulative = 0
        segment_data = None
        for seg in segments:
            cumulative += seg['pct']
            if rand <= cumulative:
                segment_data = seg
                break
        
        segment_name = segment_data['name']
        payment_terms = segment_data['payment_terms_days']
        
        # Générer nom de société
        company_name = f"Company {i:04d} {random.choice(company_suffixes)}"
        
        customers.append({
            'customer_id': f'CUST_{i:06d}',
            'company_name': company_name,
            'segment': segment_name,
            'industry': random.choice(industries),
            'country': random.choice(['France', 'Germany', 'UK', 'USA', 'Spain', 'Italy']),
            'payment_terms_days': payment_terms,
            'credit_limit_eur': segment_data['avg_revenue'] * 2,
            'account_manager': f'AM_{random.randint(1, 15):02d}',
            'created_date': (datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1800))).strftime('%Y-%m-%d'),
            'is_active': 'true'
        })
    
    print(f"  ✓ {customer_count} clients créés")
    return customers


def generate_products(config: Dict) -> List[Dict]:
    """Génère les produits"""
    print("📦 Génération des produits...")
    
    products = []
    product_id = 1
    
    for category in config['products']['categories']:
        for i in range(category['count']):
            price_min, price_max = category['price_range']
            price = random.uniform(price_min, price_max)
            cogs = price * category['cogs_pct']
            
            products.append({
                'product_id': f'PROD_{product_id:05d}',
                'product_name': f"{category['name'].replace('_', ' ').title()} {i+1}",
                'category': category['name'],
                'unit_price_eur': round(price, 2),
                'cogs_eur': round(cogs, 2),
                'gross_margin_pct': round((1 - category['cogs_pct']) * 100, 1),
                'is_active': 'true'
            })
            product_id += 1
    
    print(f"  ✓ {len(products)} produits créés")
    return products


def generate_budgets(config: Dict, cost_centers: List[Dict], accounts: List[Dict]) -> List[Dict]:
    """Génère les budgets mensuels"""
    print("💰 Génération des budgets...")
    
    budgets = []
    start_date = datetime.strptime(config['start_date'], '%Y-%m-%d')
    end_date = datetime.strptime(config['end_date'], '%Y-%m-%d')
    
    # Budget annuel total (en millions)
    total_annual_budget = 24_000_000  # 24M€
    
    # Répartition mensuelle avec saisonnalité
    monthly_weights = {
        1: 0.07, 2: 0.07, 3: 0.09,  # Q1: 23%
        4: 0.08, 5: 0.08, 6: 0.09,  # Q2: 25%
        7: 0.08, 8: 0.07, 9: 0.09,  # Q3: 24%
        10: 0.09, 11: 0.09, 12: 0.10 # Q4: 28% (saison forte)
    }
    
    # Comptes de charges (classe 6)
    expense_accounts = [acc for acc in accounts if acc['account_type'] == 'Expense']
    
    current_date = start_date
    budget_id = 1
    
    while current_date <= end_date:
        month = current_date.month
        year = current_date.year
        monthly_budget = total_annual_budget * monthly_weights[month]
        
        for cc in cost_centers:
            cc_budget = monthly_budget * cc['budget_allocation_pct']
            
            # Répartir le budget du CC sur plusieurs comptes de charges
            num_accounts = random.randint(3, 6)
            selected_accounts = random.sample(expense_accounts, num_accounts)
            
            for acc in selected_accounts:
                account_budget = cc_budget / num_accounts * random.uniform(0.7, 1.3)
                
                budgets.append({
                    'budget_id': f'BUD_{budget_id:08d}',
                    'fiscal_year': year,
                    'period_month': month,
                    'period_date': current_date.strftime('%Y-%m-%d'),
                    'cost_center_id': cc['cost_center_id'],
                    'account_id': acc['account_id'],
                    'budget_amount_eur': round(account_budget, 2),
                    'budget_type': 'Operating',
                    'version': 'V1_Approved'
                })
                budget_id += 1
        
        # Mois suivant
        if month == 12:
            current_date = datetime(year + 1, 1, 1)
        else:
            current_date = datetime(year, month + 1, 1)
    
    print(f"  ✓ {len(budgets)} lignes budgétaires créées")
    return budgets


def generate_invoices_and_lines(config: Dict, customers: List[Dict], products: List[Dict]) -> tuple:
    """Génère les factures et lignes de factures"""
    print("📄 Génération des factures...")
    
    invoices = []
    invoice_lines = []
    
    start_date = datetime.strptime(config['start_date'], '%Y-%m-%d')
    end_date = datetime.strptime(config['end_date'], '%Y-%m-%d')
    total_days = (end_date - start_date).days
    
    invoice_count = config['invoices']['count']
    avg_lines = config['invoices']['avg_lines_per_invoice']
    
    for i in range(1, invoice_count + 1):
        # Date de facture aléatoire
        invoice_date = start_date + timedelta(days=random.randint(0, total_days))
        
        # Client aléatoire
        customer = random.choice(customers)
        payment_terms = customer['payment_terms_days']
        due_date = invoice_date + timedelta(days=payment_terms)
        
        # Nombre de lignes
        num_lines = max(1, int(random.gauss(avg_lines, 1)))
        
        # Générer les lignes
        total_amount = 0
        line_id = 1
        for _ in range(num_lines):
            product = random.choice(products)
            quantity = random.randint(1, 10)
            unit_price = product['unit_price_eur']
            discount = random.choice([0, 0, 0, 0.05, 0.10, 0.15])  # 60% sans remise
            line_total = quantity * unit_price * (1 - discount)
            total_amount += line_total
            
            invoice_lines.append({
                'line_id': f'LINE_{i:08d}_{line_id:02d}',
                'invoice_id': f'INV_{i:08d}',
                'product_id': product['product_id'],
                'quantity': quantity,
                'unit_price_eur': unit_price,
                'discount_pct': discount,
                'line_total_eur': round(line_total, 2),
                'cogs_eur': round(quantity * product['cogs_eur'], 2)
            })
            line_id += 1
        
        invoices.append({
            'invoice_id': f'INV_{i:08d}',
            'invoice_number': f'F{invoice_date.year}{i:06d}',
            'customer_id': customer['customer_id'],
            'invoice_date': invoice_date.strftime('%Y-%m-%d'),
            'due_date': due_date.strftime('%Y-%m-%d'),
            'total_amount_eur': round(total_amount, 2),
            'status': 'Issued',
            'payment_terms_days': payment_terms
        })
    
    print(f"  ✓ {len(invoices)} factures créées")
    print(f"  ✓ {len(invoice_lines)} lignes de factures créées")
    return invoices, invoice_lines


def generate_payments(config: Dict, invoices: List[Dict]) -> List[Dict]:
    """Génère les paiements avec délais réalistes"""
    print("💳 Génération des paiements...")
    
    payments = []
    payment_config = config['payments']
    
    # Scénario Q4: augmentation des retards
    q4_dso_spike = config['scenarios']['q4_dso_spike']
    
    for invoice in invoices:
        invoice_date = datetime.strptime(invoice['invoice_date'], '%Y-%m-%d')
        due_date = datetime.strptime(invoice['due_date'], '%Y-%m-%d')
        amount = invoice['total_amount_eur']
        
        # Appliquer le scénario Q4 si activé
        is_q4 = invoice_date.month >= q4_dso_spike['trigger_month'] if q4_dso_spike['enabled'] else False
        
        # Déterminer le délai de paiement
        rand = random.random()
        if rand < payment_config['on_time_pct']:
            # Paiement à temps (ou légèrement en avance)
            payment_delay = random.randint(-5, 2)
        elif rand < payment_config['on_time_pct'] + payment_config['late_7_days_pct']:
            # Retard 7 jours
            payment_delay = random.randint(3, 10)
        elif rand < payment_config['on_time_pct'] + payment_config['late_7_days_pct'] + payment_config['late_30_days_pct']:
            # Retard 30 jours
            payment_delay = random.randint(15, 40)
        else:
            # Retard 60+ jours
            payment_delay = random.randint(45, 90)
        
        # Augmenter les retards en Q4
        if is_q4 and payment_delay > 0:
            payment_delay += q4_dso_spike['dso_increase_days']
        
        payment_date = due_date + timedelta(days=payment_delay)
        
        # Ne générer que les paiements déjà effectués (pas dans le futur)
        if payment_date <= datetime.now():
            payments.append({
                'payment_id': f'PAY_{invoice["invoice_id"].replace("INV_", "")}',
                'invoice_id': invoice['invoice_id'],
                'payment_date': payment_date.strftime('%Y-%m-%d'),
                'payment_amount_eur': amount,
                'payment_method': random.choice(['Wire Transfer', 'Check', 'Credit Card']),
                'days_overdue': max(0, payment_delay)
            })
    
    print(f"  ✓ {len(payments)} paiements créés")
    return payments


def generate_general_ledger(config: Dict, invoices: List[Dict], invoice_lines: List[Dict],
                            budgets: List[Dict], accounts: List[Dict], cost_centers: List[Dict]) -> List[Dict]:
    """Génère le grand livre (journal des écritures)"""
    print("📚 Génération du grand livre...")
    
    gl_entries = []
    entry_id = 1
    
    start_date = datetime.strptime(config['start_date'], '%Y-%m-%d')
    end_date = datetime.strptime(config['end_date'], '%Y-%m-%d')
    
    # Scénarios
    q2_margin_drop = config['scenarios']['q2_margin_drop']
    q3_cost_overrun = config['scenarios']['q3_cost_overrun']
    
    # 1. Générer les écritures de ventes (revenus)
    revenue_accounts = [acc for acc in accounts if acc['account_type'] == 'Revenue']
    
    for invoice in invoices:
        invoice_date = datetime.strptime(invoice['invoice_date'], '%Y-%m-%d')
        total = invoice['total_amount_eur']
        
        # Répartir sur les comptes de revenus selon les lignes de facture
        for line in [l for l in invoice_lines if l['invoice_id'] == invoice['invoice_id']]:
            # Trouver le compte de revenu selon le produit
            product_category = next((p['category'] for p in products if p['product_id'] == line['product_id']), 'software_licenses')
            
            # Mapper catégorie → compte de revenu
            revenue_mapping = {
                'software_licenses': 'Software Licenses',
                'professional_services': 'Professional Services',
                'maintenance': 'Maintenance',
                'training': 'Training'
            }
            revenue_account_name = revenue_mapping.get(product_category, 'Software Licenses')
            revenue_account = next((acc for acc in revenue_accounts if acc['account_name'] == revenue_account_name), revenue_accounts[0])
            
            # Écriture de revenu (crédit)
            gl_entries.append({
                'entry_id': f'GL_{entry_id:010d}',
                'entry_date': invoice_date.strftime('%Y-%m-%d'),
                'period_month': invoice_date.month,
                'fiscal_year': invoice_date.year,
                'account_id': revenue_account['account_id'],
                'cost_center_id': random.choice([cc['cost_center_id'] for cc in cost_centers if cc['cost_center_type'] == 'Revenue']),
                'debit_amount_eur': 0,
                'credit_amount_eur': line['line_total_eur'],
                'description': f"Revenue from {invoice['invoice_id']}",
                'reference': invoice['invoice_id'],
                'entry_type': 'Revenue'
            })
            entry_id += 1
            
            # Écriture COGS (débit)
            cogs_account = next((acc for acc in accounts if acc['account_name'] == 'Achats matières'), accounts[0])
            gl_entries.append({
                'entry_id': f'GL_{entry_id:010d}',
                'entry_date': invoice_date.strftime('%Y-%m-%d'),
                'period_month': invoice_date.month,
                'fiscal_year': invoice_date.year,
                'account_id': cogs_account['account_id'],
                'cost_center_id': random.choice([cc['cost_center_id'] for cc in cost_centers if cc['cost_center_type'] == 'Delivery']),
                'debit_amount_eur': line['cogs_eur'],
                'credit_amount_eur': 0,
                'description': f"COGS for {invoice['invoice_id']}",
                'reference': invoice['invoice_id'],
                'entry_type': 'COGS'
            })
            entry_id += 1
    
    # 2. Générer les écritures de charges (expenses) basées sur le budget
    expense_accounts = [acc for acc in accounts if acc['account_type'] == 'Expense']
    
    current_date = start_date
    while current_date <= end_date:
        month = current_date.month
        year = current_date.year
        
        # Récupérer les budgets de ce mois
        monthly_budgets = [b for b in budgets if b['period_month'] == month and b['fiscal_year'] == year]
        
        for budget in monthly_budgets:
            budget_amount = budget['budget_amount_eur']
            
            # Appliquer variance (réel vs budget)
            variance = random.uniform(-config['general_ledger']['variance_pct'],
                                    config['general_ledger']['variance_pct'])
            
            # Scénario Q2: baisse de marge (augmentation COGS)
            if q2_margin_drop['enabled'] and month >= q2_margin_drop['trigger_month'] and month < 7:
                if 'Achats' in budget['account_id']:  # Si c'est un compte d'achats
                    variance += q2_margin_drop['impact_pct']
            
            # Scénario Q3: dépassement budget marketing
            if q3_cost_overrun['enabled'] and month >= q3_cost_overrun['trigger_month'] and month < 10:
                cc = next((c for c in cost_centers if c['cost_center_id'] == budget['cost_center_id']), None)
                if cc and 'Marketing' in cc['cost_center_name']:
                    variance += q3_cost_overrun['budget_overrun_pct']
            
            actual_amount = budget_amount * (1 + variance)
            
            # Générer plusieurs écritures pour répartir dans le mois
            num_entries = random.randint(2, 5)
            for i in range(num_entries):
                entry_amount = actual_amount / num_entries
                entry_date = current_date + timedelta(days=random.randint(1, 28))
                
                gl_entries.append({
                    'entry_id': f'GL_{entry_id:010d}',
                    'entry_date': entry_date.strftime('%Y-%m-%d'),
                    'period_month': month,
                    'fiscal_year': year,
                    'account_id': budget['account_id'],
                    'cost_center_id': budget['cost_center_id'],
                    'debit_amount_eur': round(entry_amount, 2),
                    'credit_amount_eur': 0,
                    'description': f"Expense for {budget['cost_center_id']}",
                    'reference': budget['budget_id'],
                    'entry_type': 'Expense'
                })
                entry_id += 1
        
        # Mois suivant
        if month == 12:
            current_date = datetime(year + 1, 1, 1)
        else:
            current_date = datetime(year, month + 1, 1)
    
    print(f"  ✓ {len(gl_entries)} écritures générées")
    return gl_entries


def generate_forecasts(config: Dict, budgets: List[Dict]) -> List[Dict]:
    """Génère les forecasts (reforecasts trimestriels)"""
    print("🔮 Génération des forecasts...")
    
    forecasts = []
    forecast_id = 1
    
    # Générer des forecasts pour Q2, Q3, Q4 (reforecasts)
    quarters = {
        'Q2': {'month_start': 4, 'version': 'Q2_Reforecast'},
        'Q3': {'month_start': 7, 'version': 'Q3_Reforecast'},
        'Q4': {'month_start': 10, 'version': 'Q4_Reforecast'}
    }
    
    for quarter, qinfo in quarters.items():
        # Prendre les budgets du trimestre
        quarter_budgets = [b for b in budgets if b['period_month'] >= qinfo['month_start'] and b['period_month'] < qinfo['month_start'] + 3]
        
        for budget in quarter_budgets:
            # Forecast = Budget ajusté selon la précision (s'améliore au fil de l'année)
            accuracy_factor = 1 + random.uniform(-0.10, 0.10)  # +/- 10%
            
            forecasts.append({
                'forecast_id': f'FCS_{forecast_id:08d}',
                'fiscal_year': budget['fiscal_year'],
                'period_month': budget['period_month'],
                'period_date': budget['period_date'],
                'cost_center_id': budget['cost_center_id'],
                'account_id': budget['account_id'],
                'forecast_amount_eur': round(budget['budget_amount_eur'] * accuracy_factor, 2),
                'forecast_type': 'Rolling',
                'version': qinfo['version'],
                'created_date': f"{budget['fiscal_year']}-{qinfo['month_start']:02d}-01"
            })
            forecast_id += 1
    
    print(f"  ✓ {len(forecasts)} forecasts créés")
    return forecasts


def generate_allocations(config: Dict, cost_centers: List[Dict], accounts: List[Dict]) -> List[Dict]:
    """Génère les allocations de coûts indirects"""
    print("🔄 Génération des allocations...")
    
    allocations = []
    allocation_id = 1
    
    # Pools de coûts indirects
    overhead_pools = [
        {'name': 'IT Infrastructure', 'driver': 'headcount', 'total_amount': 500000},
        {'name': 'HR Services', 'driver': 'headcount', 'total_amount': 300000},
        {'name': 'Facilities', 'driver': 'square_footage', 'total_amount': 400000},
        {'name': 'Finance & Admin', 'driver': 'revenue', 'total_amount': 250000},
        {'name': 'Legal', 'driver': 'transactions', 'total_amount': 150000}
    ]
    
    # Centres de coûts bénéficiaires (hors admin)
    target_cost_centers = [cc for cc in cost_centers if cc['cost_center_type'] not in ['Admin', 'Support']]
    
    for pool in overhead_pools:
        # Répartir le pool sur les centres de coûts
        total_driver = sum([random.uniform(1, 10) for _ in target_cost_centers])  # Unités du driver
        
        for cc in target_cost_centers:
            driver_units = random.uniform(1, 10)
            allocated_amount = (driver_units / total_driver) * pool['total_amount']
            
            allocations.append({
                'allocation_id': f'ALLOC_{allocation_id:06d}',
                'fiscal_year': 2025,
                'from_cost_center': pool['name'],
                'to_cost_center_id': cc['cost_center_id'],
                'allocation_driver': pool['driver'],
                'driver_units': round(driver_units, 2),
                'allocated_amount_eur': round(allocated_amount, 2),
                'allocation_month': 12  # Allocation en fin d'année
            })
            allocation_id += 1
    
    print(f"  ✓ {len(allocations)} allocations créées")
    return allocations


def save_to_csv(data: List[Dict], filename: str, directory: Path):
    """Sauvegarde les données en CSV"""
    if not data:
        print(f"  ⚠ Aucune donnée à sauvegarder pour {filename}")
        return
    
    filepath = directory / filename
    directory.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    
    print(f"  ✓ Sauvegardé: {filepath} ({len(data)} lignes)")


def main():
    """Fonction principale"""
    print("=" * 80)
    print("🚀 Générateur de données Finance Performance Management")
    print("=" * 80)
    print()
    
    # Charger la configuration
    config = load_config()
    print(f"📋 Configuration chargée depuis {CONFIG_FILE}")
    print()
    
    # Générer les données Finance
    chart_of_accounts = generate_chart_of_accounts(config)
    cost_centers = generate_cost_centers(config)
    budgets = generate_budgets(config, cost_centers, chart_of_accounts)
    forecasts = generate_forecasts(config, budgets)
    allocations = generate_allocations(config, cost_centers, chart_of_accounts)
    
    # Générer les données Business
    customers = generate_customers(config)
    global products  # Nécessaire pour generate_general_ledger
    products = generate_products(config)
    invoices, invoice_lines = generate_invoices_and_lines(config, customers, products)
    payments = generate_payments(config, invoices)
    
    # Générer le grand livre (dépend de toutes les autres tables)
    general_ledger = generate_general_ledger(config, invoices, invoice_lines, budgets, chart_of_accounts, cost_centers)
    
    print()
    print("💾 Sauvegarde des fichiers CSV...")
    print()
    
    # Sauvegarder Finance
    save_to_csv(chart_of_accounts, 'dim_chart_of_accounts.csv', FINANCE_DIR)
    save_to_csv(cost_centers, 'dim_cost_centers.csv', FINANCE_DIR)
    save_to_csv(budgets, 'fact_budgets.csv', FINANCE_DIR)
    save_to_csv(forecasts, 'fact_forecasts.csv', FINANCE_DIR)
    save_to_csv(allocations, 'fact_allocations.csv', FINANCE_DIR)
    save_to_csv(general_ledger, 'fact_general_ledger.csv', FINANCE_DIR)
    
    # Sauvegarder Business
    save_to_csv(customers, 'dim_customers.csv', BUSINESS_DIR)
    save_to_csv(products, 'dim_products.csv', BUSINESS_DIR)
    save_to_csv(invoices, 'fact_invoices.csv', BUSINESS_DIR)
    save_to_csv(invoice_lines, 'fact_invoice_lines.csv', BUSINESS_DIR)
    save_to_csv(payments, 'fact_payments.csv', BUSINESS_DIR)
    
    print()
    print("=" * 80)
    print("✅ Génération terminée avec succès!")
    print("=" * 80)
    print()
    print(f"📊 Statistiques:")
    print(f"  - Comptes comptables: {len(chart_of_accounts)}")
    print(f"  - Centres de coûts: {len(cost_centers)}")
    print(f"  - Lignes budgétaires: {len(budgets)}")
    print(f"  - Forecasts: {len(forecasts)}")
    print(f"  - Allocations: {len(allocations)}")
    print(f"  - Écritures GL: {len(general_ledger)}")
    print(f"  - Clients: {len(customers)}")
    print(f"  - Produits: {len(products)}")
    print(f"  - Factures: {len(invoices)}")
    print(f"  - Lignes de factures: {len(invoice_lines)}")
    print(f"  - Paiements: {len(payments)}")
    print()
    print(f"📁 Fichiers générés dans:")
    print(f"  - Finance: {FINANCE_DIR}")
    print(f"  - Business: {BUSINESS_DIR}")
    print()


if __name__ == "__main__":
    main()
