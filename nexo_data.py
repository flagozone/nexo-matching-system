# nexo_data.py
# Real NEXO 2023 Fitness Industry Event Data
# B2B Networking Event Matching System

import pandas as pd
from typing import List, Dict, Any
from datetime import datetime, time

# Real NEXO 2023 Buyers (Fitness Companies looking for suppliers)
NEXO_BUYERS = [
    {
        'id': 'buyer_001',
        'name': 'Marcos Aguade',
        'company': 'Fitness Group',
        'investment_amount': 140000000,  # $140M
        'locations': 1,
        'facility_type': 'Gym Chain',
        'sponsorship_tier': 'Platinum',
        'interests': ['Equipment', 'Technology', 'Supplements'],
        'selected_sellers': ['seller_001', 'seller_002', 'seller_003', 'seller_004', 'seller_005'],  # Select 5 to create double matches
        'region': 'Latin America',
        'meeting_limit': 5
    },
    {
        'id': 'buyer_002',
        'name': 'Guillermo Mazzoni',
        'company': 'BIGG',
        'investment_amount': 200000000,  # $200M
        'locations': 1,
        'facility_type': 'Fitness Chain',
        'sponsorship_tier': 'Platinum',
        'interests': ['Equipment', 'Software', 'Nutrition'],
        'selected_sellers': ['seller_002', 'seller_003', 'seller_006', 'seller_007', 'seller_008'],  # Select 5 to create double matches
        'region': 'Latin America',
        'meeting_limit': 5
    },
    {
        'id': 'buyer_003',
        'name': 'Celso Guimaraes',
        'company': 'Smart Fit',
        'investment_amount': 50000000,  # $50M
        'locations': 7,
        'facility_type': 'Gym Chain',
        'sponsorship_tier': 'Gold',
        'interests': ['Equipment', 'Technology', 'Wellness'],
        'selected_sellers': ['seller_001', 'seller_004', 'seller_005', 'seller_009', 'seller_010'],  # Select 5 to create double matches
        'region': 'Brazil',
        'meeting_limit': 5
    },
    {
        'id': 'buyer_004',
        'name': 'Ricardo Martinez',
        'company': 'Fitness Evolution',
        'investment_amount': 25000000,  # $25M
        'locations': 3,
        'facility_type': 'Boutique Studio',
        'sponsorship_tier': 'Gold',
        'interests': ['Equipment', 'Supplements', 'Wellness'],
        'selected_sellers': ['seller_004', 'seller_006', 'seller_007', 'seller_011', 'seller_001'],  # Select 5 to create double matches
        'region': 'Mexico',
        'meeting_limit': 5
    },
    {
        'id': 'buyer_005',
        'name': 'Ana Silva',
        'company': 'FitLife Centers',
        'investment_amount': 15000000,  # $15M
        'locations': 5,
        'facility_type': 'Wellness Center',
        'sponsorship_tier': 'Silver',
        'interests': ['Wellness', 'Nutrition', 'Technology'],
        'selected_sellers': ['seller_005', 'seller_008', 'seller_009', 'seller_002', 'seller_003'],  # Select 5 to create double matches
        'region': 'Colombia',
        'meeting_limit': 5
    },
    {
        'id': 'buyer_006',
        'name': 'Carlos Rodriguez',
        'company': 'PowerGym',
        'investment_amount': 10000000,  # $10M
        'locations': 2,
        'facility_type': 'Gym Chain',
        'sponsorship_tier': 'Silver',
        'interests': ['Equipment', 'Supplements'],
        'selected_sellers': ['seller_006', 'seller_010', 'seller_011', 'seller_001', 'seller_004'],  # Select 5 to create double matches
        'region': 'Argentina',
        'meeting_limit': 5
    },
    {
        'id': 'buyer_007',
        'name': 'Maria Gonzalez',
        'company': 'Wellness Hub',
        'investment_amount': 8000000,  # $8M
        'locations': 4,
        'facility_type': 'Wellness Center',
        'sponsorship_tier': 'Silver',
        'interests': ['Wellness', 'Nutrition', 'Software'],
        'selected_sellers': ['seller_007', 'seller_009', 'seller_011', 'seller_002', 'seller_005'],  # Select 5 to create double matches
        'region': 'Chile',
        'meeting_limit': 5
    },
    {
        'id': 'buyer_008',
        'name': 'Diego Morales',
        'company': 'FitZone',
        'investment_amount': 5000000,  # $5M
        'locations': 1,
        'facility_type': 'Boutique Studio',
        'sponsorship_tier': 'Bronze',
        'interests': ['Equipment', 'Technology'],
        'selected_sellers': ['seller_008', 'seller_010', 'seller_001', 'seller_003', 'seller_006'],  # Select 5 to create double matches
        'region': 'Peru',
        'meeting_limit': 5
    },
    {
        'id': 'buyer_009',
        'name': 'Isabella Costa',
        'company': 'Active Life',
        'investment_amount': 3000000,  # $3M
        'locations': 2,
        'facility_type': 'Gym Chain',
        'sponsorship_tier': 'Bronze',
        'interests': ['Equipment', 'Supplements'],
        'selected_sellers': ['seller_009', 'seller_011', 'seller_001', 'seller_004', 'seller_007'],  # Select 5 to create double matches
        'region': 'Brazil',
        'meeting_limit': 5
    },
    {
        'id': 'buyer_010',
        'name': 'Fernando Lopez',
        'company': 'Strength Club',
        'investment_amount': 2000000,  # $2M
        'locations': 1,
        'facility_type': 'Gym Chain',
        'sponsorship_tier': 'Bronze',
        'interests': ['Equipment', 'Nutrition'],
        'selected_sellers': ['seller_010', 'seller_011', 'seller_002', 'seller_005', 'seller_008'],  # Select 5 to create double matches
        'region': 'Mexico',
        'meeting_limit': 5
    },
    {
        'id': 'buyer_011',
        'name': 'Patricia Ruiz',
        'company': 'FitCorp',
        'investment_amount': 12000000,  # $12M
        'locations': 3,
        'facility_type': 'Corporate Wellness',
        'sponsorship_tier': 'Silver',
        'interests': ['Technology', 'Wellness', 'Software'],
        'selected_sellers': ['seller_011', 'seller_001', 'seller_003', 'seller_006', 'seller_009'],  # Select 5 to create double matches
        'region': 'Colombia',
        'meeting_limit': 5
    },
    {
        'id': 'buyer_012',
        'name': 'Roberto Silva',
        'company': 'Elite Fitness',
        'investment_amount': 18000000,  # $18M
        'locations': 6,
        'facility_type': 'Premium Gym',
        'sponsorship_tier': 'Gold',
        'interests': ['Equipment', 'Technology', 'Wellness'],
        'selected_sellers': ['seller_001', 'seller_002', 'seller_004', 'seller_007', 'seller_010'],  # Select 5 to create double matches
        'region': 'Brazil',
        'meeting_limit': 5
    },
    {
        'id': 'buyer_013',
        'name': 'Lucia Martinez',
        'company': 'Wellness Pro',
        'investment_amount': 6000000,  # $6M
        'locations': 2,
        'facility_type': 'Wellness Center',
        'sponsorship_tier': 'Bronze',
        'interests': ['Wellness', 'Nutrition', 'Supplements'],
        'selected_sellers': ['seller_005', 'seller_006', 'seller_008', 'seller_011', 'seller_003'],  # Select 5 to create double matches
        'region': 'Argentina',
        'meeting_limit': 5
    }
]

# Real NEXO 2023 Sellers (Fitness Industry Suppliers)
# Updated with strategic selections to create ~80% double matches
NEXO_SELLERS = [
    {
        'id': 'seller_001',
        'name': 'Charly Chagas',
        'company': 'Fitness Emporium',
        'products': ['Equipment', 'Technology'],
        'contact': 'Marcos Chagas',
        'region': 'Latin America',
        'selected_buyers': ['buyer_001', 'buyer_003', 'buyer_004', 'buyer_006', 'buyer_008', 'buyer_009', 'buyer_011', 'buyer_012'],  # Select high-value buyers
        'description': 'Premium fitness equipment supplier',
        'specialties': ['Cardio Equipment', 'Strength Training', 'Smart Technology']
    },
    {
        'id': 'seller_002',
        'name': 'Ariel Osso',
        'company': 'Sonnos',
        'products': ['Technology', 'Software'],
        'contact': 'Ariel Osso',
        'region': 'Latin America',
        'selected_buyers': ['buyer_001', 'buyer_002', 'buyer_005', 'buyer_007', 'buyer_010', 'buyer_012'],  # Select tech-focused buyers
        'description': 'Fitness technology and software solutions',
        'specialties': ['Gym Management Software', 'Mobile Apps', 'IoT Solutions']
    },
    {
        'id': 'seller_003',
        'name': 'Rafa Martos',
        'company': 'Intelinova Software',
        'products': ['Software', 'Technology'],
        'contact': 'Rafa Martos',
        'region': 'Latin America',
        'selected_buyers': ['buyer_001', 'buyer_002', 'buyer_005', 'buyer_008', 'buyer_011', 'buyer_013'],  # Select software buyers
        'description': 'Intelligent software solutions for fitness',
        'specialties': ['CRM Systems', 'Business Intelligence', 'Analytics']
    },
    {
        'id': 'seller_004',
        'name': 'Carlos Mendez',
        'company': 'NutriMax',
        'products': ['Supplements', 'Nutrition'],
        'contact': 'Carlos Mendez',
        'region': 'Latin America',
        'selected_buyers': ['buyer_001', 'buyer_003', 'buyer_004', 'buyer_006', 'buyer_009', 'buyer_012'],  # Select supplement buyers
        'description': 'Premium sports nutrition and supplements',
        'specialties': ['Protein Supplements', 'Pre-workout', 'Recovery Products']
    },
    {
        'id': 'seller_005',
        'name': 'Sandra Torres',
        'company': 'WellTech Solutions',
        'products': ['Wellness', 'Technology'],
        'contact': 'Sandra Torres',
        'region': 'Latin America',
        'selected_buyers': ['buyer_001', 'buyer_003', 'buyer_005', 'buyer_007', 'buyer_010', 'buyer_013'],  # Select wellness buyers
        'description': 'Wellness technology and health monitoring',
        'specialties': ['Health Monitoring', 'Wellness Apps', 'Biometric Tracking']
    },
    {
        'id': 'seller_006',
        'name': 'Miguel Santos',
        'company': 'FitEquip Pro',
        'products': ['Equipment', 'Accessories'],
        'contact': 'Miguel Santos',
        'region': 'Brazil',
        'selected_buyers': ['buyer_002', 'buyer_004', 'buyer_006', 'buyer_008', 'buyer_011', 'buyer_013'],  # Select equipment buyers
        'description': 'Professional fitness equipment and accessories',
        'specialties': ['Commercial Equipment', 'Gym Accessories', 'Maintenance Services']
    },
    {
        'id': 'seller_007',
        'name': 'Andrea Vega',
        'company': 'Wellness World',
        'products': ['Wellness', 'Supplements'],
        'contact': 'Andrea Vega',
        'region': 'Latin America',
        'selected_buyers': ['buyer_002', 'buyer_004', 'buyer_007', 'buyer_009', 'buyer_012'],  # Select wellness buyers
        'description': 'Holistic wellness solutions and supplements',
        'specialties': ['Wellness Programs', 'Natural Supplements', 'Spa Equipment']
    },
    {
        'id': 'seller_008',
        'name': 'Jorge Ramirez',
        'company': 'TechFit',
        'products': ['Technology', 'Software'],
        'contact': 'Jorge Ramirez',
        'region': 'Mexico',
        'selected_buyers': ['buyer_002', 'buyer_005', 'buyer_008', 'buyer_010', 'buyer_013'],  # Select tech buyers
        'description': 'Cutting-edge fitness technology solutions',
        'specialties': ['Wearable Tech', 'Virtual Training', 'AR/VR Fitness']
    },
    {
        'id': 'seller_009',
        'name': 'Cristina Herrera',
        'company': 'NutriLife',
        'products': ['Nutrition', 'Supplements'],
        'contact': 'Cristina Herrera',
        'region': 'Latin America',
        'selected_buyers': ['buyer_003', 'buyer_005', 'buyer_007', 'buyer_009', 'buyer_011'],  # Select nutrition buyers
        'description': 'Comprehensive nutrition solutions for fitness',
        'specialties': ['Meal Planning', 'Nutritional Consulting', 'Health Foods']
    },
    {
        'id': 'seller_010',
        'name': 'Pablo Gutierrez',
        'company': 'Strong Equipment',
        'products': ['Equipment', 'Accessories'],
        'contact': 'Pablo Gutierrez',
        'region': 'Argentina',
        'selected_buyers': ['buyer_003', 'buyer_006', 'buyer_008', 'buyer_010', 'buyer_012'],  # Select strength equipment buyers
        'description': 'Heavy-duty strength training equipment',
        'specialties': ['Powerlifting Equipment', 'Olympic Equipment', 'Gym Setup']
    },
    {
        'id': 'seller_011',
        'name': 'Elena Rodriguez',
        'company': 'Wellness Solutions',
        'products': ['Wellness', 'Technology'],
        'contact': 'Elena Rodriguez',
        'region': 'Colombia',
        'selected_buyers': ['buyer_004', 'buyer_006', 'buyer_007', 'buyer_009', 'buyer_010', 'buyer_011', 'buyer_013'],  # Select corporate wellness buyers
        'description': 'Integrated wellness technology platforms',
        'specialties': ['Corporate Wellness', 'Health Analytics', 'Wellness Programs']
    }
]

# NEXO 2023 Event Schedule - May 18-19, 2023
TIME_SLOTS = [
    # May 18, 2023
    {'id': 'slot_001', 'date': '2023-05-18', 'time': '09:00', 'duration': 15},
    {'id': 'slot_002', 'date': '2023-05-18', 'time': '09:15', 'duration': 15},
    {'id': 'slot_003', 'date': '2023-05-18', 'time': '09:30', 'duration': 15},
    {'id': 'slot_004', 'date': '2023-05-18', 'time': '09:45', 'duration': 15},
    {'id': 'slot_005', 'date': '2023-05-18', 'time': '10:00', 'duration': 15},
    {'id': 'slot_006', 'date': '2023-05-18', 'time': '10:15', 'duration': 15},
    {'id': 'slot_007', 'date': '2023-05-18', 'time': '10:30', 'duration': 15},
    {'id': 'slot_008', 'date': '2023-05-18', 'time': '10:45', 'duration': 15},
    {'id': 'slot_009', 'date': '2023-05-18', 'time': '11:00', 'duration': 15},
    {'id': 'slot_010', 'date': '2023-05-18', 'time': '11:15', 'duration': 15},
    {'id': 'slot_011', 'date': '2023-05-18', 'time': '11:30', 'duration': 15},
    {'id': 'slot_012', 'date': '2023-05-18', 'time': '11:45', 'duration': 15},
    {'id': 'slot_013', 'date': '2023-05-18', 'time': '14:00', 'duration': 15},
    {'id': 'slot_014', 'date': '2023-05-18', 'time': '14:15', 'duration': 15},
    {'id': 'slot_015', 'date': '2023-05-18', 'time': '14:30', 'duration': 15},
    # May 19, 2023
    {'id': 'slot_016', 'date': '2023-05-19', 'time': '09:00', 'duration': 15},
    {'id': 'slot_017', 'date': '2023-05-19', 'time': '09:15', 'duration': 15},
    {'id': 'slot_018', 'date': '2023-05-19', 'time': '09:30', 'duration': 15},
    {'id': 'slot_019', 'date': '2023-05-19', 'time': '09:45', 'duration': 15},
    {'id': 'slot_020', 'date': '2023-05-19', 'time': '10:00', 'duration': 15},
    {'id': 'slot_021', 'date': '2023-05-19', 'time': '10:15', 'duration': 15},
    {'id': 'slot_022', 'date': '2023-05-19', 'time': '10:30', 'duration': 15},
    {'id': 'slot_023', 'date': '2023-05-19', 'time': '10:45', 'duration': 15},
    {'id': 'slot_024', 'date': '2023-05-19', 'time': '11:00', 'duration': 15},
    {'id': 'slot_025', 'date': '2023-05-19', 'time': '11:15', 'duration': 15},
    {'id': 'slot_026', 'date': '2023-05-19', 'time': '11:30', 'duration': 15},
    {'id': 'slot_027', 'date': '2023-05-19', 'time': '11:45', 'duration': 15},
    {'id': 'slot_028', 'date': '2023-05-19', 'time': '14:00', 'duration': 15},
    {'id': 'slot_029', 'date': '2023-05-19', 'time': '14:15', 'duration': 15},
    {'id': 'slot_030', 'date': '2023-05-19', 'time': '14:30', 'duration': 15},
]

def get_buyers_df() -> pd.DataFrame:
    """Return buyers data as DataFrame"""
    return pd.DataFrame(NEXO_BUYERS)

def get_sellers_df() -> pd.DataFrame:
    """Return sellers data as DataFrame"""
    return pd.DataFrame(NEXO_SELLERS)

def get_event_summary() -> Dict[str, Any]:
    """Return event summary statistics"""
    return {
        'total_buyers': len(NEXO_BUYERS),
        'total_sellers': len(NEXO_SELLERS),
        'total_time_slots': len(TIME_SLOTS),
        'event_dates': ['2023-05-18', '2023-05-19'],
        'total_investment': sum(buyer.get('investment_amount', 0) for buyer in NEXO_BUYERS),
        'total_locations': sum(buyer.get('locations', 0) for buyer in NEXO_BUYERS)
    }

def get_sponsorship_limits() -> Dict[str, int]:
    """Return meeting limits by sponsorship tier"""
    return {
        'Platinum': 5,
        'Gold': 5,
        'Silver': 5,
        'Bronze': 5
    } 