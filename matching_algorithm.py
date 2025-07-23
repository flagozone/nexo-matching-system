# matching_algorithm.py
# NEXO Event Matching Algorithm for B2B Networking
# Business Logic: Sellers choose buyers (mandatory), Double matches, Buyers get 5 meetings

import pandas as pd
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
import logging
from datetime import datetime

@dataclass
class Match:
    """Represents a match between buyer and seller"""
    buyer_id: str
    seller_id: str
    match_type: str  # 'double_match', 'seller_choice', 'ai_suggestion'
    compatibility_score: float
    meeting_scheduled: bool = False
    time_slot: Optional[str] = None
    priority: int = 1  # 1=highest, 3=lowest

class NEXOEventMatcher:
    """
    NEXO Event Matching Engine for B2B Networking
    Business Logic: 
    - Sellers choose buyers → Buyers MUST accept (sponsored obligation)
    - Double matches when both select each other (highest priority)
    - Buyers must accept exactly 5 meetings
    - Remaining slots filled with AI compatibility matches
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.matches = []
        self.scheduled_meetings = []
        self.compatibility_weights = {
            'interest_alignment': 0.40,    # 40% - Product/service alignment
            'investment_factor': 0.25,     # 25% - Investment amount factor
            'company_size': 0.20,          # 20% - Number of locations
            'facility_type': 0.10,         # 10% - Facility type compatibility
            'existing_client': 0.05        # 5% - Existing relationship bonus
        }
    
    def calculate_compatibility_score(self, buyer: Dict, seller: Dict) -> float:
        """Calculate compatibility score between buyer and seller (0-100%)"""
        score = 0.0
        
        # Interest/Product alignment (40%)
        buyer_interests = set(buyer.get('interests', []))
        seller_products = set(seller.get('products', []))
        interest_overlap = len(buyer_interests.intersection(seller_products))
        max_interests = max(len(buyer_interests), len(seller_products), 1)
        interest_score = interest_overlap / max_interests
        score += interest_score * self.compatibility_weights['interest_alignment']
        
        # Investment amount factor (25%)
        investment = buyer.get('investment_amount', 0)
        if investment >= 100000000:  # $100M+
            investment_score = 1.0
        elif investment >= 50000000:  # $50M+
            investment_score = 0.8
        elif investment >= 10000000:  # $10M+
            investment_score = 0.6
        elif investment >= 1000000:   # $1M+
            investment_score = 0.4
        else:
            investment_score = 0.2
        score += investment_score * self.compatibility_weights['investment_factor']
        
        # Company size (number of locations) (20%)
        locations = buyer.get('locations', 1)
        if locations >= 5:
            size_score = 1.0
        elif locations >= 3:
            size_score = 0.8
        elif locations >= 2:
            size_score = 0.6
        else:
            size_score = 0.4
        score += size_score * self.compatibility_weights['company_size']
        
        # Facility type compatibility (10%)
        facility_score = 0.5  # Base compatibility
        if buyer.get('facility_type') in ['Gym Chain', 'Premium Gym']:
            if 'Equipment' in seller.get('products', []):
                facility_score = 1.0
        elif buyer.get('facility_type') in ['Wellness Center', 'Corporate Wellness']:
            if 'Wellness' in seller.get('products', []):
                facility_score = 1.0
        elif buyer.get('facility_type') == 'Boutique Studio':
            if 'Technology' in seller.get('products', []):
                facility_score = 1.0
        score += facility_score * self.compatibility_weights['facility_type']
        
        # Existing client relationship bonus (5%)
        score += 0.5 * self.compatibility_weights['existing_client']
        
        return min(score * 100, 100)  # Convert to percentage and cap at 100%
    
    def find_matches(self, buyers: List[Dict], sellers: List[Dict]) -> List[Match]:
        """
        Find matches using NEXO business logic:
        1. Double matches (both selected each other) - highest priority
        2. Seller choices (buyers must accept - sponsored obligation)
        3. Fill remaining buyer slots with AI compatibility matches
        4. Each buyer gets exactly 5 meetings
        """
        all_matches = []
        buyer_meetings = {buyer['id']: [] for buyer in buyers}  # Track meetings per buyer
        
        # Step 1: Process Double Matches (highest priority)
        print("🤝 Processing Double Matches...")
        for buyer in buyers:
            buyer_selections = set(buyer.get('selected_sellers', []))
            for seller in sellers:
                seller_selections = set(seller.get('selected_buyers', []))
                
                # Check if both selected each other
                if buyer['id'] in seller_selections and seller['id'] in buyer_selections:
                    compatibility = self.calculate_compatibility_score(buyer, seller)
                    match = Match(
                        buyer_id=buyer['id'],
                        seller_id=seller['id'],
                        match_type='double_match',
                        compatibility_score=compatibility,
                        priority=1
                    )
                    all_matches.append(match)
                    buyer_meetings[buyer['id']].append(match)
                    print(f"   Double Match: {buyer['name']} ↔ {seller['name']} ({compatibility:.1f}%)")
        
        # Step 2: Process Seller Choices (buyers must accept - sponsored obligation)
        print("\n🏷️ Processing Seller Choices (Sponsored Obligations)...")
        for seller in sellers:
            seller_selections = set(seller.get('selected_buyers', []))
            for buyer_id in seller_selections:
                buyer = next((b for b in buyers if b['id'] == buyer_id), None)
                if not buyer:
                    continue
                
                # Skip if already matched in double match
                existing_match = any(m.buyer_id == buyer_id and m.seller_id == seller['id'] 
                                   for m in buyer_meetings[buyer_id])
                if existing_match:
                    continue
                
                # Check if buyer has room for more meetings
                if len(buyer_meetings[buyer_id]) < 5:
                    compatibility = self.calculate_compatibility_score(buyer, seller)
                    match = Match(
                        buyer_id=buyer_id,
                        seller_id=seller['id'],
                        match_type='seller_choice',
                        compatibility_score=compatibility,
                        priority=2
                    )
                    all_matches.append(match)
                    buyer_meetings[buyer_id].append(match)
                    print(f"   Seller Choice: {buyer['name']} ← {seller['name']} (MUST ACCEPT)")
        
        # Step 3: Fill remaining buyer slots with AI compatibility matches
        print("\n🤖 Processing AI Compatibility Assignments...")
        for buyer in buyers:
            buyer_id = buyer['id']
            current_meetings = len(buyer_meetings[buyer_id])
            
            if current_meetings < 5:
                needed_meetings = 5 - current_meetings
                print(f"   {buyer['name']} needs {needed_meetings} more meetings...")
                
                # Get sellers not already matched with this buyer
                matched_seller_ids = {m.seller_id for m in buyer_meetings[buyer_id]}
                available_sellers = [s for s in sellers if s['id'] not in matched_seller_ids]
                
                # Calculate compatibility with available sellers
                compatibility_scores = []
                for seller in available_sellers:
                    compatibility = self.calculate_compatibility_score(buyer, seller)
                    compatibility_scores.append((seller, compatibility))
                
                # Sort by compatibility and take top matches
                compatibility_scores.sort(key=lambda x: x[1], reverse=True)
                
                for seller, compatibility in compatibility_scores[:needed_meetings]:
                    match = Match(
                        buyer_id=buyer_id,
                        seller_id=seller['id'],
                        match_type='ai_suggestion',
                        compatibility_score=compatibility,
                        priority=3
                    )
                    all_matches.append(match)
                    buyer_meetings[buyer_id].append(match)
                    print(f"     AI Match: {buyer['name']} ↔ {seller['name']} ({compatibility:.1f}%)")
        
        # Print summary
        print(f"\n📊 MATCHING SUMMARY:")
        double_matches = len([m for m in all_matches if m.match_type == 'double_match'])
        seller_choices = len([m for m in all_matches if m.match_type == 'seller_choice'])
        ai_suggestions = len([m for m in all_matches if m.match_type == 'ai_suggestion'])
        total = len(all_matches)
        
        print(f"   🤝 Double Matches: {double_matches} ({double_matches/total*100:.1f}%)")
        print(f"   🏷️ Seller Choices: {seller_choices} ({seller_choices/total*100:.1f}%)")
        print(f"   🤖 AI Suggestions: {ai_suggestions} ({ai_suggestions/total*100:.1f}%)")
        print(f"   📋 Total Meetings: {total}")
        
        # Verify each buyer has exactly 5 meetings
        for buyer in buyers:
            meeting_count = len(buyer_meetings[buyer['id']])
            print(f"   {buyer['name']}: {meeting_count} meetings")
        
        return all_matches
    
    def create_schedule(self, matches: List[Match], buyers: List[Dict], sellers: List[Dict], 
                       time_slots: List[Dict]) -> List[Dict]:
        """Create conflict-free meeting schedule with business priority"""
        scheduled_meetings = []
        buyer_schedule = {}  # buyer_id -> [time_slots]
        seller_schedule = {}  # seller_id -> [time_slots]
        
        # Sort matches by priority (double matches first, then seller choices, then AI)
        sorted_matches = sorted(matches, key=lambda x: (x.priority, -x.compatibility_score))
        
        print(f"\n📅 SCHEDULING {len(sorted_matches)} MEETINGS...")
        
        for match in sorted_matches:
            buyer_id = match.buyer_id
            seller_id = match.seller_id
            
            # Find available time slot
            for time_slot in time_slots:
                slot_id = time_slot['id']
                
                # Check if both buyer and seller are available
                buyer_available = slot_id not in buyer_schedule.get(buyer_id, [])
                seller_available = slot_id not in seller_schedule.get(seller_id, [])
                
                if buyer_available and seller_available:
                    # Schedule the meeting
                    meeting = {
                        'buyer_id': buyer_id,
                        'seller_id': seller_id,
                        'time_slot': slot_id,
                        'date': time_slot['date'],
                        'time': time_slot['time'],
                        'duration': time_slot['duration'],
                        'match_type': match.match_type,
                        'compatibility_score': match.compatibility_score,
                        'priority': match.priority
                    }
                    
                    scheduled_meetings.append(meeting)
                    
                    # Update schedules
                    if buyer_id not in buyer_schedule:
                        buyer_schedule[buyer_id] = []
                    if seller_id not in seller_schedule:
                        seller_schedule[seller_id] = []
                    
                    buyer_schedule[buyer_id].append(slot_id)
                    seller_schedule[seller_id].append(slot_id)
                    
                    # Mark match as scheduled
                    match.meeting_scheduled = True
                    match.time_slot = slot_id
                    
                    # Get names for logging
                    buyer_name = next((b['name'] for b in buyers if b['id'] == buyer_id), 'Unknown')
                    seller_name = next((s['name'] for s in sellers if s['id'] == seller_id), 'Unknown')
                    match_icon = {'double_match': '🤝', 'seller_choice': '🏷️', 'ai_suggestion': '🤖'}[match.match_type]
                    
                    print(f"   {match_icon} {time_slot['date']} {time_slot['time']}: {buyer_name} ← → {seller_name}")
                    
                    break  # Move to next match
        
        print(f"\n✅ SCHEDULED {len(scheduled_meetings)} meetings successfully!")
        return scheduled_meetings
    
    def get_matching_statistics(self, matches: List[Match], scheduled_meetings: List[Dict]) -> Dict[str, Any]:
        """Generate comprehensive matching statistics"""
        if not matches:
            return {'error': 'No matches found'}
        
        # Match type distribution
        match_types = {}
        for match in matches:
            match_types[match.match_type] = match_types.get(match.match_type, 0) + 1
        
        # Compatibility statistics
        compatibility_scores = [match.compatibility_score for match in matches]
        avg_compatibility = sum(compatibility_scores) / len(compatibility_scores)
        
        # Scheduling statistics
        scheduled_count = len(scheduled_meetings)
        total_matches = len(matches)
        scheduling_efficiency = (scheduled_count / total_matches) * 100 if total_matches > 0 else 0
        
        # Priority distribution
        priority_dist = {}
        for match in matches:
            priority_dist[f'Priority {match.priority}'] = priority_dist.get(f'Priority {match.priority}', 0) + 1
        
        return {
            'total_matches': total_matches,
            'scheduled_meetings': scheduled_count,
            'unscheduled_matches': total_matches - scheduled_count,
            'scheduling_efficiency': round(scheduling_efficiency, 2),
            'average_compatibility': round(avg_compatibility, 2),
            'match_type_distribution': match_types,
            'priority_distribution': priority_dist,
            'unique_buyers_matched': len(set(match.buyer_id for match in matches)),
            'unique_sellers_matched': len(set(match.seller_id for match in matches))
        }
    
    def export_schedule_csv(self, scheduled_meetings: List[Dict], buyers: List[Dict], sellers: List[Dict]) -> str:
        """Export schedule to CSV format"""
        if not scheduled_meetings:
            return "No meetings scheduled"
        
        # Create buyer and seller lookup dictionaries
        buyer_dict = {buyer['id']: buyer for buyer in buyers}
        seller_dict = {seller['id']: seller for seller in sellers}
        
        csv_data = []
        csv_data.append("Date,Time,Buyer,Buyer Company,Seller,Seller Company,Match Type,Compatibility Score,Priority")
        
        for meeting in scheduled_meetings:
            buyer = buyer_dict.get(meeting['buyer_id'], {})
            seller = seller_dict.get(meeting['seller_id'], {})
            
            row = [
                meeting['date'],
                meeting['time'],
                buyer.get('name', 'Unknown'),
                buyer.get('company', 'Unknown'),
                seller.get('name', 'Unknown'),
                seller.get('company', 'Unknown'),
                meeting['match_type'].replace('_', ' ').title(),
                str(round(meeting['compatibility_score'], 1)),
                str(meeting['priority'])
            ]
            csv_data.append(','.join(row))
        
        return '\n'.join(csv_data) 