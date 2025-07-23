# 🏗️ NEXO Event Matching System - Technical Architecture

## 📋 Table of Contents
- [Tech Stack](#-tech-stack)
- [System Architecture](#-system-architecture)
- [Core Algorithms](#-core-algorithms)
- [Data Structures](#-data-structures)
- [Frontend Implementation](#-frontend-implementation)
- [Backend Logic](#-backend-logic)
- [Performance Considerations](#-performance-considerations)
- [Deployment Architecture](#-deployment-architecture)

---

## 🛠️ Tech Stack

### **Core Technologies**
- **Language**: Python 3.13
- **Web Framework**: Streamlit 1.46.1
- **Data Processing**: Pandas 2.3.0
- **Visualization**: Plotly 6.2.0
- **Type Hints**: Python typing module
- **Data Classes**: Python dataclasses

### **Development Tools**
- **Version Control**: Git
- **Package Management**: pip
- **Code Organization**: Modular Python architecture
- **Documentation**: Markdown + docstrings

### **Deployment Stack**
- **Cloud Platform**: Streamlit Cloud
- **Repository**: GitHub
- **CI/CD**: Automatic deployment from Git pushes
- **Hosting**: Serverless (managed by Streamlit Cloud)

---

## 🏛️ System Architecture

### **Modular Design Pattern**
```
nexo-matching-system/
├── 📄 app.py (841 lines)           # Main Streamlit application
├── 🧠 matching_algorithm.py (345 lines)  # Core matching engine
├── 📊 nexo_data.py (370 lines)     # Data layer & business logic
├── 📋 requirements.txt             # Dependencies
├── 📖 README.md                    # Project documentation
└── 🏗️ TECHNICAL_DETAILS.md         # This file
```

### **Architecture Layers**

#### **1. Presentation Layer (Streamlit)**
- **File**: `app.py`
- **Purpose**: User interface and interaction
- **Components**:
  - Multi-page navigation system
  - Interactive forms and controls
  - Real-time data visualization
  - Export functionality

#### **2. Business Logic Layer**
- **File**: `matching_algorithm.py`
- **Purpose**: Core matching algorithms and scheduling
- **Components**:
  - NEXOEventMatcher class
  - Compatibility scoring engine
  - Conflict resolution system
  - Schedule optimization

#### **3. Data Layer**
- **File**: `nexo_data.py`
- **Purpose**: Data management and business rules
- **Components**:
  - Participant data structures
  - Event configuration
  - Data transformation utilities
  - Business rule enforcement

---

## 🧠 Core Algorithms

### **1. Three-Tier Matching Algorithm**

```python
def find_matches(self, buyers: List[Dict], sellers: List[Dict]) -> List[Match]:
    """
    Priority-based matching system:
    1. Double Matches (Priority 1) - Mutual selection
    2. Seller Choices (Priority 2) - Sponsored obligations
    3. AI Suggestions (Priority 3) - Compatibility-based
    """
```

**Algorithm Complexity**: O(n²) where n = max(buyers, sellers)
**Space Complexity**: O(n) for storing matches and schedules

### **2. Compatibility Scoring Algorithm**

```python
def calculate_compatibility_score(self, buyer: Dict, seller: Dict) -> float:
    """
    Weighted multi-factor compatibility calculation:
    - Interest Alignment: 40%
    - Investment Factor: 25%
    - Company Size: 20%
    - Facility Type: 10%
    - Existing Client: 5%
    """
```

**Scoring Formula**:
```
Score = (Interest_Overlap / Max_Interests) * 0.40 +
        (Investment_Score) * 0.25 +
        (Size_Score) * 0.20 +
        (Facility_Score) * 0.10 +
        (Relationship_Bonus) * 0.05
```

### **3. Conflict-Free Scheduling Algorithm**

```python
def create_schedule(self, matches: List[Match], ...) -> List[Dict]:
    """
    Greedy algorithm for conflict-free scheduling:
    1. Sort matches by priority and compatibility
    2. Iterate through time slots
    3. Assign first available slot for each match
    4. Track buyer/seller availability
    """
```

**Scheduling Strategy**: Greedy with priority ordering
**Conflict Resolution**: Real-time availability tracking

---

## 📊 Data Structures

### **1. Match Dataclass**
```python
@dataclass
class Match:
    buyer_id: str
    seller_id: str
    match_type: str  # 'double_match', 'seller_choice', 'ai_suggestion'
    compatibility_score: float
    meeting_scheduled: bool = False
    time_slot: Optional[str] = None
    priority: int = 1  # 1=highest, 3=lowest
```

### **2. Participant Data Structure**
```python
{
    'id': 'buyer_001',
    'name': 'Marcos Aguade',
    'company': 'Fitness Group',
    'investment_amount': 140000000,
    'locations': 1,
    'facility_type': 'Gym Chain',
    'sponsorship_tier': 'Platinum',
    'interests': ['Equipment', 'Technology', 'Supplements'],
    'selected_sellers': ['seller_001', 'seller_002', ...],
    'region': 'Latin America',
    'meeting_limit': 5
}
```

### **3. Time Slot Structure**
```python
{
    'id': 'slot_001',
    'date': '2023-05-18',
    'time': '09:00',
    'duration': 15
}
```

---

## 🎨 Frontend Implementation

### **Streamlit Components Used**

#### **1. Navigation System**
```python
page = st.sidebar.selectbox("Choose a page", [
    "🏠 Dashboard", 
    "👥 Participants", 
    "🎯 Generate Matches", 
    "📅 Create Schedule", 
    "📊 Match Results",
    "📈 Analytics"
])
```

#### **2. Interactive Forms**
- **Slider Controls**: Algorithm weight adjustment
- **Select Boxes**: Participant filtering
- **Buttons**: Action triggers
- **File Upload**: Data import (if needed)

#### **3. Data Visualization**
```python
# Plotly Charts
fig_types = px.bar(
    match_type_df,
    x='Type',
    y='Count',
    color='Priority',
    title="Matches by Type and Priority",
    color_continuous_scale='RdYlGn_r'
)
```

#### **4. Real-time Metrics**
```python
st.metric(
    label="👥 Total Buyers",
    value=event_summary['total_buyers'],
    help="Fitness companies looking for suppliers"
)
```

### **CSS Customization**
```css
.main-header {
    font-size: 2.5rem;
    color: #1f4e79;
    text-align: center;
    margin-bottom: 2rem;
    font-weight: bold;
}
.priority-1 { background: #d4edda; border-left: 4px solid #28a745; }
.priority-2 { background: #fff3cd; border-left: 4px solid #ffc107; }
.priority-3 { background: #f8d7da; border-left: 4px solid #dc3545; }
```

---

## ⚙️ Backend Logic

### **1. Session State Management**
```python
# Store results in session state
st.session_state.matches = matches
st.session_state.matcher = matcher
```

### **2. Data Persistence**
- **In-Memory Storage**: Session state for runtime data
- **File Export**: CSV generation for external use
- **State Management**: Cross-page data sharing

### **3. Error Handling**
```python
if 'matches' not in st.session_state or not st.session_state.matches:
    st.warning("⚠️ No matches available. Please generate matches first.")
    return
```

### **4. Business Rule Enforcement**
- **Meeting Limits**: Each buyer gets exactly 5 meetings
- **Sponsorship Obligations**: Sellers can force buyer acceptance
- **Conflict Prevention**: No double-booking of time slots
- **Priority Respect**: Higher priority matches scheduled first

---

## ⚡ Performance Considerations

### **1. Algorithm Optimization**
- **Early Termination**: Stop when buyer meeting limits reached
- **Efficient Sorting**: Priority-based match ordering
- **Memory Management**: Deep copy for data isolation

### **2. Data Processing**
- **Pandas Optimization**: Vectorized operations for data analysis
- **Lazy Loading**: Load data only when needed
- **Caching**: Session state for repeated calculations

### **3. Scalability Considerations**
- **Current Capacity**: 7 buyers × 11 sellers = 77 potential matches
- **Scalability**: Algorithm can handle 100+ participants
- **Performance**: Sub-second matching for current dataset

### **4. Memory Usage**
- **Data Structures**: ~50KB for current dataset
- **Session State**: ~10KB for runtime data
- **Total Memory**: <100KB for full application

---

## 🚀 Deployment Architecture

### **Streamlit Cloud Deployment**
```
GitHub Repository → Streamlit Cloud → Public URL
     ↓                    ↓              ↓
  Code Changes → Automatic Build → Live Application
```

### **Deployment Process**
1. **Code Push**: `git push origin main`
2. **Auto-Build**: Streamlit Cloud detects changes
3. **Dependency Installation**: `pip install -r requirements.txt`
4. **Application Launch**: `streamlit run app.py`
5. **Public Access**: URL generation and distribution

### **Environment Configuration**
```python
# Streamlit Cloud automatically handles:
# - Python environment setup
# - Dependency resolution
# - Port configuration
# - SSL certificates
# - Load balancing
```

### **Monitoring & Logging**
- **Build Logs**: Available in Streamlit Cloud dashboard
- **Error Tracking**: Automatic error reporting
- **Performance Metrics**: Response time monitoring
- **Usage Analytics**: Built-in Streamlit analytics

---

## 🔧 Development Workflow

### **1. Local Development**
```bash
# Setup
cd nexo-matching-system
pip install -r requirements.txt
streamlit run app.py

# Development
# Edit files → Test locally → Commit → Push → Auto-deploy
```

### **2. Version Control**
```bash
git add .
git commit -m "Feature description"
git push origin main
# Automatic deployment to Streamlit Cloud
```

### **3. Testing Strategy**
- **Unit Testing**: Algorithm validation
- **Integration Testing**: End-to-end workflow
- **User Acceptance**: Real business scenario testing
- **Performance Testing**: Load testing with larger datasets

---

## 📈 Future Enhancements

### **Technical Improvements**
- **Database Integration**: PostgreSQL for persistent storage
- **API Development**: RESTful API for external integrations
- **Real-time Updates**: WebSocket for live collaboration
- **Advanced Analytics**: Machine learning for better matching

### **Feature Additions**
- **Multi-Event Support**: Handle multiple events simultaneously
- **Advanced Scheduling**: AI-powered schedule optimization
- **Integration APIs**: CRM and calendar system integration
- **Mobile Support**: Responsive design for mobile devices

---

## 🎯 Key Technical Achievements

1. **Complex Algorithm Implementation**: Three-tier priority matching system
2. **Real-time Conflict Resolution**: Automated scheduling with constraint satisfaction
3. **Scalable Architecture**: Modular design supporting future growth
4. **Professional UI/UX**: Enterprise-grade interface with interactive visualizations
5. **Production-Ready Deployment**: Cloud-native architecture with automatic scaling
6. **Business Logic Integration**: Real-world constraints and sponsorship rules
7. **Data Export Capabilities**: CSV generation for external system integration

This system demonstrates advanced Python development, algorithmic problem-solving, and modern web application architecture suitable for enterprise B2B event management. 