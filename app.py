# app.py
# NEXO Event Matching System - Main Streamlit Application
# B2B Networking Event Scheduler for Fitness Industry

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Any
import copy
from datetime import datetime

# Import our custom modules
from nexo_data import (
    NEXO_BUYERS, NEXO_SELLERS, TIME_SLOTS,
    get_buyers_df, get_sellers_df, get_event_summary, get_sponsorship_limits
)
from matching_algorithm import NEXOEventMatcher, Match

# Page configuration
st.set_page_config(
    page_title="NEXO Event Matching System",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c5aa0;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 1px solid #e9ecef;
    }
    .priority-1 {
        background: #d4edda;
        border-left: 4px solid #28a745;
    }
    .priority-2 {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
    }
    .priority-3 {
        background: #f8d7da;
        border-left: 4px solid #dc3545;
    }
    .match-card {
        background: #e8f4f8;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #17a2b8;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">🤝 NEXO Event Matching System</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.1rem; color: #666; margin-bottom: 2rem;">B2B Networking Event Scheduler for Fitness Industry - September 25-30, 2025</p>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.header("🔧 Navigation")
    page = st.sidebar.selectbox("Choose a page", [
        "🏠 Dashboard", 
        "👥 Participants", 
        "🎯 Generate Matches", 
        "📅 Create Schedule", 
        "📊 Match Results",
        "📈 Analytics"
    ])
    
    # Process page selection
    page_key = page.split(' ', 1)[1] if ' ' in page else page
    
    if page_key == "Dashboard":
        show_dashboard()
    elif page_key == "Participants":
        show_participants()
    elif page_key == "Generate Matches":
        show_generate_matches()
    elif page_key == "Create Schedule":
        show_create_schedule()
    elif page_key == "Match Results":
        show_match_results()
    elif page_key == "Analytics":
        show_analytics()

def show_dashboard():
    """Display main dashboard"""
    st.markdown('<h2 class="sub-header">📊 Event Dashboard</h2>', unsafe_allow_html=True)
    
    # Event summary metrics
    event_summary = get_event_summary()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="👥 Total Buyers",
            value=event_summary['total_buyers'],
            help="Fitness companies looking for suppliers"
        )
    
    with col2:
        st.metric(
            label="🏪 Total Sellers", 
            value=event_summary['total_sellers'],
            help="Fitness industry suppliers and service providers"
        )
    
    with col3:
        st.metric(
            label="💰 Total Investment",
            value=f"${event_summary['total_investment']:,.0f}",
            help="Combined investment capacity of all buyers"
        )
    
    with col4:
        st.metric(
            label="📍 Total Locations",
            value=f"{event_summary['total_locations']}",
            help="Combined number of buyer locations"
        )
    
    # Quick overview
    st.markdown("---")
    st.subheader("📋 Quick Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **🎯 3-Tier Priority System**
        1. **Double Match** - Both parties selected each other
        2. **Seller Choice** - Seller selected buyer (hosted buyer obligation)
        3. **AI Suggestion** - High compatibility matches (>70%)
        """)
    
    with col2:
        st.info("""
        **📅 Event Details**
        - **Dates**: May 18-19, 2023
        - **Duration**: 15-minute meetings
        - **Time Slots**: 20 available slots
        - **Meeting Limits**: Based on sponsorship tier
        """)
    
    # Sponsorship tier breakdown
    st.subheader("🏆 Sponsorship Tier Breakdown")
    
    buyers_df = get_buyers_df()
    if not buyers_df.empty:
        tier_counts = buyers_df['sponsorship_tier'].value_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Create pie chart for sponsorship tiers
            fig_tier = px.pie(
                values=tier_counts.values,
                names=tier_counts.index,
                title="Buyers by Sponsorship Tier",
                color_discrete_map={
                    'Platinum': '#FFD700',
                    'Gold': '#C0C0C0',
                    'Silver': '#CD7F32',
                    'Bronze': '#A0522D'
                }
            )
            st.plotly_chart(fig_tier, use_container_width=True)
        
        with col2:
            # Meeting limits by tier
            limits_df = pd.DataFrame([
                {'Tier': 'Platinum', 'Meeting Limit': 20, 'Count': tier_counts.get('Platinum', 0)},
                {'Tier': 'Gold', 'Meeting Limit': 20, 'Count': tier_counts.get('Gold', 0)},
                {'Tier': 'Silver', 'Meeting Limit': 15, 'Count': tier_counts.get('Silver', 0)},
                {'Tier': 'Bronze', 'Meeting Limit': 10, 'Count': tier_counts.get('Bronze', 0)}
            ])
            
            fig_limits = px.bar(
                limits_df,
                x='Tier',
                y='Count',
                title="Buyer Count by Sponsorship Tier",
                color='Tier',
                color_discrete_map={
                    'Platinum': '#FFD700',
                    'Gold': '#C0C0C0',
                    'Silver': '#CD7F32',
                    'Bronze': '#A0522D'
                }
            )
            st.plotly_chart(fig_limits, use_container_width=True)

def show_participants():
    """Display participant information"""
    st.markdown('<h2 class="sub-header">👥 Event Participants</h2>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🏢 Buyers", "🏪 Sellers"])
    
    with tab1:
        st.subheader("🏢 Buyer Portfolio")
        buyers_df = get_buyers_df()
        
        if not buyers_df.empty:
            # Buyer filters
            col1, col2, col3 = st.columns(3)
            
            with col1:
                regions = buyers_df['region'].unique()
                selected_regions = st.multiselect("Filter by Region", regions, default=list(regions))
            
            with col2:
                tiers = buyers_df['sponsorship_tier'].unique()
                selected_tiers = st.multiselect("Filter by Sponsorship", tiers, default=list(tiers))
            
            with col3:
                facilities = buyers_df['facility_type'].unique()
                selected_facilities = st.multiselect("Filter by Facility Type", facilities, default=list(facilities))
            
            # Apply filters
            filtered_buyers = buyers_df[
                (buyers_df['region'].isin(selected_regions)) &
                (buyers_df['sponsorship_tier'].isin(selected_tiers)) &
                (buyers_df['facility_type'].isin(selected_facilities))
            ]
            
            # Display filtered buyers
            st.dataframe(
                filtered_buyers[['name', 'company', 'investment_amount', 'locations', 'facility_type', 'sponsorship_tier', 'region']],
                use_container_width=True
            )
            
            # Analytics
            if len(filtered_buyers) > 0:
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_investment = px.bar(
                        filtered_buyers,
                        x='name',
                        y='investment_amount',
                        title="Investment Amount by Buyer",
                        labels={'investment_amount': 'Investment ($)', 'name': 'Buyer'}
                    )
                    fig_investment.update_xaxes(tickangle=45)
                    st.plotly_chart(fig_investment, use_container_width=True)
                
                with col2:
                    fig_locations = px.scatter(
                        filtered_buyers,
                        x='locations',
                        y='investment_amount',
                        size='investment_amount',
                        color='sponsorship_tier',
                        title="Investment vs Locations",
                        labels={'investment_amount': 'Investment ($)', 'locations': 'Number of Locations'}
                    )
                    st.plotly_chart(fig_locations, use_container_width=True)
    
    with tab2:
        st.subheader("🏪 Seller Portfolio")
        sellers_df = get_sellers_df()
        
        if not sellers_df.empty:
            # Seller filters
            col1, col2 = st.columns(2)
            
            with col1:
                regions = sellers_df['region'].unique()
                selected_regions = st.multiselect("Filter by Region", regions, default=list(regions), key="seller_regions")
            
            with col2:
                # Extract unique products
                all_products = []
                for products in sellers_df['products']:
                    all_products.extend(products)
                unique_products = list(set(all_products))
                selected_products = st.multiselect("Filter by Products", unique_products, default=unique_products)
            
            # Apply filters
            filtered_sellers = sellers_df[
                (sellers_df['region'].isin(selected_regions))
            ]
            
            # Additional product filter
            if selected_products:
                filtered_sellers = filtered_sellers[
                    filtered_sellers['products'].apply(lambda x: any(p in selected_products for p in x))
                ]
            
            # Display filtered sellers
            st.dataframe(
                filtered_sellers[['name', 'company', 'products', 'region', 'description']],
                use_container_width=True
            )
            
            # Analytics
            if len(filtered_sellers) > 0:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Product distribution
                    product_counts = {}
                    for products in filtered_sellers['products']:
                        for product in products:
                            product_counts[product] = product_counts.get(product, 0) + 1
                    
                    fig_products = px.bar(
                        x=list(product_counts.keys()),
                        y=list(product_counts.values()),
                        title="Product/Service Distribution",
                        labels={'x': 'Product/Service', 'y': 'Number of Sellers'}
                    )
                    st.plotly_chart(fig_products, use_container_width=True)
                
                with col2:
                    # Regional distribution
                    region_counts = filtered_sellers['region'].value_counts()
                    fig_regions = px.pie(
                        values=region_counts.values,
                        names=region_counts.index,
                        title="Sellers by Region"
                    )
                    st.plotly_chart(fig_regions, use_container_width=True)

def show_generate_matches():
    """Display matching interface"""
    st.markdown('<h2 class="sub-header">🎯 Generate Matches</h2>', unsafe_allow_html=True)
    
    st.info("Configure and run the NEXO matching algorithm to find optimal buyer-seller matches using the 3-tier priority system.")
    
    # Algorithm configuration
    st.subheader("⚙️ Algorithm Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Compatibility Scoring Weights**")
        interest_weight = st.slider("Interest/Product Alignment", 0.0, 1.0, 0.40, 0.05, help="Weight for product/service alignment")
        investment_weight = st.slider("Investment Factor", 0.0, 1.0, 0.25, 0.05, help="Weight for investment amount")
        company_size_weight = st.slider("Company Size", 0.0, 1.0, 0.20, 0.05, help="Weight for number of locations")
    
    with col2:
        st.markdown("**Additional Factors**")
        facility_weight = st.slider("Facility Type", 0.0, 1.0, 0.10, 0.05, help="Weight for facility type compatibility")
        relationship_weight = st.slider("Existing Relationship", 0.0, 1.0, 0.05, 0.05, help="Weight for existing relationships")
        ai_threshold = st.slider("AI Suggestion Threshold", 50, 90, 70, 5, help="Minimum compatibility for AI suggestions (%)")
    
    # Display current configuration
    st.subheader("📊 Current Configuration")
    
    # Normalize weights
    total_weight = interest_weight + investment_weight + company_size_weight + facility_weight + relationship_weight
    if total_weight > 0:
        weights = {
            'Interest Alignment': interest_weight / total_weight,
            'Investment Factor': investment_weight / total_weight,
            'Company Size': company_size_weight / total_weight,
            'Facility Type': facility_weight / total_weight,
            'Existing Relationship': relationship_weight / total_weight
        }
        
        fig_weights = px.bar(
            x=list(weights.keys()),
            y=list(weights.values()),
            title="Normalized Matching Criteria Weights",
            labels={'x': 'Criteria', 'y': 'Weight'}
        )
        st.plotly_chart(fig_weights, use_container_width=True)
    
    # Run matching
    st.subheader("🚀 Run Matching Algorithm")
    
    if st.button("🎯 Generate Matches", type="primary", use_container_width=True):
        with st.spinner("Running NEXO matching algorithm..."):
            # Initialize matching engine
            matcher = NEXOEventMatcher()
            
            # Update compatibility weights
            if total_weight > 0:
                matcher.compatibility_weights = {
                    'interest_alignment': interest_weight / total_weight,
                    'investment_factor': investment_weight / total_weight,
                    'company_size': company_size_weight / total_weight,
                    'facility_type': facility_weight / total_weight,
                    'existing_client': relationship_weight / total_weight
                }
            
            # Get data (make copies to avoid modifying original)
            buyers_copy = copy.deepcopy(NEXO_BUYERS)
            sellers_copy = copy.deepcopy(NEXO_SELLERS)
            
            # Run matching
            matches = matcher.find_matches(buyers_copy, sellers_copy)
            
            # Store results in session state
            st.session_state.matches = matches
            st.session_state.matcher = matcher
            
            st.success(f"✅ Matching completed! Found {len(matches)} potential matches.")
            
            # Display quick summary
            if matches:
                # Calculate statistics
                match_types = {}
                for match in matches:
                    match_types[match.match_type] = match_types.get(match.match_type, 0) + 1
                
                avg_compatibility = sum(match.compatibility_score for match in matches) / len(matches)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Matches", len(matches))
                
                with col2:
                    st.metric("Avg Compatibility", f"{avg_compatibility:.1f}%")
                
                with col3:
                    st.metric("Double Matches", match_types.get('double_match', 0))
                
                # Match type breakdown
                st.subheader("📋 Match Type Breakdown")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    match_type_df = pd.DataFrame([
                        {'Type': 'Double Match', 'Count': match_types.get('double_match', 0), 'Priority': 1},
                        {'Type': 'Seller Choice', 'Count': match_types.get('seller_choice', 0), 'Priority': 2},
                        {'Type': 'AI Suggestion', 'Count': match_types.get('ai_suggestion', 0), 'Priority': 3}
                    ])
                    
                    fig_types = px.bar(
                        match_type_df,
                        x='Type',
                        y='Count',
                        color='Priority',
                        title="Matches by Type and Priority",
                        color_continuous_scale='RdYlGn_r'
                    )
                    st.plotly_chart(fig_types, use_container_width=True)
                
                with col2:
                    # Top matches preview
                    st.markdown("**🏆 Top Matches Preview**")
                    top_matches = sorted(matches, key=lambda x: (x.priority, -x.compatibility_score))[:5]
                    
                    for i, match in enumerate(top_matches):
                        buyer_name = next((b['name'] for b in NEXO_BUYERS if b['id'] == match.buyer_id), 'Unknown')
                        seller_name = next((s['name'] for s in NEXO_SELLERS if s['id'] == match.seller_id), 'Unknown')
                        
                        st.markdown(f"""
                        **{i+1}.** {buyer_name} ↔ {seller_name}  
                        *{match.match_type.replace('_', ' ').title()} - {match.compatibility_score:.1f}% compatibility*
                        """)

def show_create_schedule():
    """Display schedule creation interface"""
    st.markdown('<h2 class="sub-header">📅 Create Schedule</h2>', unsafe_allow_html=True)
    
    if 'matches' not in st.session_state or not st.session_state.matches:
        st.warning("⚠️ No matches available. Please generate matches first.")
        return
    
    matches = st.session_state.matches
    matcher = st.session_state.matcher
    
    st.info(f"📋 Ready to schedule {len(matches)} matches across {len(TIME_SLOTS)} available time slots.")
    
    # Show available time slots
    st.subheader("🕐 Available Time Slots")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**May 18, 2023**")
        may_18_slots = [slot for slot in TIME_SLOTS if slot['date'] == '2023-05-18']
        for slot in may_18_slots:
            st.text(f"• {slot['time']} ({slot['duration']} min)")
    
    with col2:
        st.markdown("**May 19, 2023**")
        may_19_slots = [slot for slot in TIME_SLOTS if slot['date'] == '2023-05-19']
        for slot in may_19_slots:
            st.text(f"• {slot['time']} ({slot['duration']} min)")
    
    # Create schedule
    st.subheader("🗓️ Generate Schedule")
    
    if st.button("📅 Create Conflict-Free Schedule", type="primary", use_container_width=True):
        with st.spinner("Creating optimal schedule..."):
            # Create schedule
            scheduled_meetings = matcher.create_schedule(matches, NEXO_BUYERS, NEXO_SELLERS, TIME_SLOTS)
            
            # Store in session state
            st.session_state.scheduled_meetings = scheduled_meetings
            st.session_state.schedule_statistics = matcher.get_matching_statistics(matches, scheduled_meetings)
            
            st.success(f"✅ Schedule created! {len(scheduled_meetings)} meetings scheduled.")
            
            # Display quick stats
            if scheduled_meetings:
                col1, col2, col3, col4 = st.columns(4)
                
                stats = st.session_state.schedule_statistics
                
                with col1:
                    st.metric("Scheduled Meetings", stats['scheduled_meetings'])
                
                with col2:
                    st.metric("Scheduling Efficiency", f"{stats['scheduling_efficiency']:.1f}%")
                
                with col3:
                    st.metric("Unique Buyers", stats['unique_buyers_matched'])
                
                with col4:
                    st.metric("Unique Sellers", stats['unique_sellers_matched'])
                
                # Show schedule preview
                st.subheader("📋 Schedule Preview")
                
                # Create schedule DataFrame
                schedule_data = []
                for meeting in scheduled_meetings[:10]:  # Show first 10
                    buyer_name = next((b['name'] for b in NEXO_BUYERS if b['id'] == meeting['buyer_id']), 'Unknown')
                    seller_name = next((s['name'] for s in NEXO_SELLERS if s['id'] == meeting['seller_id']), 'Unknown')
                    
                    schedule_data.append({
                        'Date': meeting['date'],
                        'Time': meeting['time'],
                        'Buyer': buyer_name,
                        'Seller': seller_name,
                        'Type': meeting['match_type'].replace('_', ' ').title(),
                        'Compatibility': f"{meeting['compatibility_score']:.1f}%"
                    })
                
                schedule_df = pd.DataFrame(schedule_data)
                st.dataframe(schedule_df, use_container_width=True)
                
                if len(scheduled_meetings) > 10:
                    st.info(f"Showing first 10 meetings. Total: {len(scheduled_meetings)} meetings scheduled.")

def show_match_results():
    """Display detailed match results"""
    st.markdown('<h2 class="sub-header">📊 Match Results</h2>', unsafe_allow_html=True)
    
    if 'matches' not in st.session_state or not st.session_state.matches:
        st.warning("⚠️ No match results available. Please generate matches first.")
        return
    
    matches = st.session_state.matches
    
    # Check if we have scheduled meetings
    has_schedule = 'scheduled_meetings' in st.session_state and st.session_state.scheduled_meetings
    
    if has_schedule:
        scheduled_meetings = st.session_state.scheduled_meetings
        stats = st.session_state.schedule_statistics
        
        # Display comprehensive statistics
        st.subheader("📈 Overall Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Matches", stats['total_matches'])
        
        with col2:
            st.metric("Scheduled Meetings", stats['scheduled_meetings'])
        
        with col3:
            st.metric("Scheduling Efficiency", f"{stats['scheduling_efficiency']:.1f}%")
        
        with col4:
            st.metric("Avg Compatibility", f"{stats['average_compatibility']:.1f}%")
        
        # Match type and priority distribution
        st.subheader("📊 Match Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Match type distribution
            match_types = stats['match_type_distribution']
            fig_types = px.pie(
                values=list(match_types.values()),
                names=[name.replace('_', ' ').title() for name in match_types.keys()],
                title="Match Type Distribution"
            )
            st.plotly_chart(fig_types, use_container_width=True)
        
        with col2:
            # Priority distribution
            priority_dist = stats['priority_distribution']
            fig_priority = px.bar(
                x=list(priority_dist.keys()),
                y=list(priority_dist.values()),
                title="Priority Distribution",
                labels={'x': 'Priority Level', 'y': 'Count'}
            )
            st.plotly_chart(fig_priority, use_container_width=True)
        
        # Detailed schedule table
        st.subheader("📅 Complete Schedule")
        
        # Create detailed schedule DataFrame
        schedule_data = []
        for meeting in scheduled_meetings:
            buyer_info = next((b for b in NEXO_BUYERS if b['id'] == meeting['buyer_id']), {})
            seller_info = next((s for s in NEXO_SELLERS if s['id'] == meeting['seller_id']), {})
            
            schedule_data.append({
                'Date': meeting['date'],
                'Time': meeting['time'],
                'Buyer': buyer_info.get('name', 'Unknown'),
                'Buyer Company': buyer_info.get('company', 'Unknown'),
                'Seller': seller_info.get('name', 'Unknown'),
                'Seller Company': seller_info.get('company', 'Unknown'),
                'Match Type': meeting['match_type'].replace('_', ' ').title(),
                'Compatibility': f"{meeting['compatibility_score']:.1f}%",
                'Priority': meeting['priority']
            })
        
        schedule_df = pd.DataFrame(schedule_data)
        st.dataframe(schedule_df, use_container_width=True)
        
        # Export functionality
        st.subheader("📥 Export Schedule")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 Export as CSV", use_container_width=True):
                matcher = st.session_state.matcher
                csv_data = matcher.export_schedule_csv(scheduled_meetings, NEXO_BUYERS, NEXO_SELLERS)
                st.download_button(
                    label="💾 Download CSV",
                    data=csv_data,
                    file_name=f"nexo_schedule_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        
        with col2:
            if st.button("📊 Export Statistics", use_container_width=True):
                stats_text = f"""NEXO Event Matching Statistics
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Total Matches: {stats['total_matches']}
Scheduled Meetings: {stats['scheduled_meetings']}
Scheduling Efficiency: {stats['scheduling_efficiency']:.1f}%
Average Compatibility: {stats['average_compatibility']:.1f}%

Match Type Distribution:
{chr(10).join([f"- {k.replace('_', ' ').title()}: {v}" for k, v in stats['match_type_distribution'].items()])}

Priority Distribution:
{chr(10).join([f"- {k}: {v}" for k, v in stats['priority_distribution'].items()])}
"""
                st.download_button(
                    label="💾 Download Statistics",
                    data=stats_text,
                    file_name=f"nexo_statistics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
    
    else:
        # Show matches without schedule
        st.info("📋 Showing match results. Create a schedule to see detailed scheduling information.")
        
        # Match summary
        match_types = {}
        for match in matches:
            match_types[match.match_type] = match_types.get(match.match_type, 0) + 1
        
        avg_compatibility = sum(match.compatibility_score for match in matches) / len(matches)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Matches", len(matches))
        
        with col2:
            st.metric("Avg Compatibility", f"{avg_compatibility:.1f}%")
        
        with col3:
            st.metric("Double Matches", match_types.get('double_match', 0))
        
        # Detailed match table
        st.subheader("📋 All Matches")
        
        match_data = []
        for match in matches:
            buyer_info = next((b for b in NEXO_BUYERS if b['id'] == match.buyer_id), {})
            seller_info = next((s for s in NEXO_SELLERS if s['id'] == match.seller_id), {})
            
            match_data.append({
                'Buyer': buyer_info.get('name', 'Unknown'),
                'Buyer Company': buyer_info.get('company', 'Unknown'),
                'Seller': seller_info.get('name', 'Unknown'),
                'Seller Company': seller_info.get('company', 'Unknown'),
                'Match Type': match.match_type.replace('_', ' ').title(),
                'Compatibility': f"{match.compatibility_score:.1f}%",
                'Priority': match.priority
            })
        
        match_df = pd.DataFrame(match_data)
        st.dataframe(match_df, use_container_width=True)

def show_analytics():
    """Display advanced analytics"""
    st.markdown('<h2 class="sub-header">📈 Advanced Analytics</h2>', unsafe_allow_html=True)
    
    # Market analysis
    st.subheader("🏪 Market Analysis")
    
    buyers_df = get_buyers_df()
    sellers_df = get_sellers_df()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Investment distribution
        fig_investment = px.histogram(
            buyers_df,
            x='investment_amount',
            nbins=10,
            title="Investment Amount Distribution",
            labels={'investment_amount': 'Investment Amount ($)', 'count': 'Number of Buyers'}
        )
        st.plotly_chart(fig_investment, use_container_width=True)
    
    with col2:
        # Regional distribution
        region_counts = buyers_df['region'].value_counts()
        fig_regions = px.pie(
            values=region_counts.values,
            names=region_counts.index,
            title="Buyer Distribution by Region"
        )
        st.plotly_chart(fig_regions, use_container_width=True)
    
    # Matching potential analysis
    if 'matches' in st.session_state and st.session_state.matches:
        st.subheader("🎯 Matching Potential Analysis")
        
        matches = st.session_state.matches
        
        # Compatibility score distribution
        compatibility_scores = [match.compatibility_score for match in matches]
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_compatibility = px.histogram(
                x=compatibility_scores,
                nbins=20,
                title="Compatibility Score Distribution",
                labels={'x': 'Compatibility Score (%)', 'count': 'Number of Matches'}
            )
            st.plotly_chart(fig_compatibility, use_container_width=True)
        
        with col2:
            # Top buyer-seller pairs
            top_matches = sorted(matches, key=lambda x: -x.compatibility_score)[:10]
            
            top_match_data = []
            for match in top_matches:
                buyer_name = next((b['name'] for b in NEXO_BUYERS if b['id'] == match.buyer_id), 'Unknown')
                seller_name = next((s['name'] for s in NEXO_SELLERS if s['id'] == match.seller_id), 'Unknown')
                
                top_match_data.append({
                    'Pair': f"{buyer_name} - {seller_name}",
                    'Compatibility': match.compatibility_score
                })
            
            top_df = pd.DataFrame(top_match_data)
            
            fig_top = px.bar(
                top_df,
                x='Compatibility',
                y='Pair',
                orientation='h',
                title="Top 10 Compatibility Matches",
                labels={'Compatibility': 'Compatibility Score (%)'}
            )
            st.plotly_chart(fig_top, use_container_width=True)
    
    # Event efficiency metrics
    if 'scheduled_meetings' in st.session_state:
        st.subheader("⚡ Event Efficiency Metrics")
        
        stats = st.session_state.schedule_statistics
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Utilization Rate",
                f"{(stats['scheduled_meetings'] / len(TIME_SLOTS) * 100):.1f}%",
                help="Percentage of time slots utilized"
            )
        
        with col2:
            st.metric(
                "Buyer Participation",
                f"{(stats['unique_buyers_matched'] / len(NEXO_BUYERS) * 100):.1f}%",
                help="Percentage of buyers with at least one meeting"
            )
        
        with col3:
            st.metric(
                "Seller Participation",
                f"{(stats['unique_sellers_matched'] / len(NEXO_SELLERS) * 100):.1f}%",
                help="Percentage of sellers with at least one meeting"
            )

if __name__ == "__main__":
    main() 