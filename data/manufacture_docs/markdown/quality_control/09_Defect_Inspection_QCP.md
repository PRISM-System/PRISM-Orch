# Defect Inspection 품질 관리 계획서
## Quality Control Plan for Inline Defect Detection and Control

**문서번호:** QCP-INSP-DEF-009  
**개정일:** 2024.11.15  
**적용공정:** Fab-wide Defect Inspection  
**기술노드:** 5nm FinFET Manufacturing  

---

## 1. 문서 개요

### 1.1 목적 및 범위
- **목적:** 전 공정 defect 검출 및 제어를 위한 통합 품질 관리 체계 수립
- **범위:** Wafer inspection, Review, Classification, Reduction
- **목표:** Killer defect < 0.01/cm², Yield loss < 1%
- **전략:** Risk-based inspection with intelligent sampling

### 1.2 Inspection Tool Fleet
| Tool Type | Model | Application | Sensitivity |
|-----------|-------|-------------|-------------|
| Brightfield | KLA 2935 | Patterned wafer | 20nm |
| Darkfield | KLA SP5 | Unpatterned | 16nm |
| E-beam | AMAT SEMVision | Voltage contrast | 10nm |
| Macro | KLA 2835 | Macro defects | 5µm |
| Review SEM | AMAT DR5 | Classification | 1nm |

---

## 2. Defect Detection Strategy

### 2.1 Layer-Specific Inspection Plan

```
Critical Layer Inspection Matrix:
Layer          Tool        Sampling    Sensitivity
STI           SP5         100%        30nm
Gate          2935        100%        20nm
Contact       E-beam      25%         15nm
M1            2935        100%        25nm
Via1          E-beam      25%         20nm

Risk Score = Impact × Probability
High Risk (>8): 100% inspection
Medium Risk (4-8): Smart sampling
Low Risk (<4): Skip lot eligible
```

### 2.2 Defect Specifications by Layer

| Layer | Critical Size | D₀ Limit | Adder Limit | Action |
|-------|--------------|----------|-------------|--------|
| Active | >30nm | 0.05/cm² | <20 | Continue |
| Gate | >20nm | 0.02/cm² | <10 | Hold if >0.05 |
| Contact | >25nm | 0.03/cm² | <15 | Review >30 |
| Metal | >40nm | 0.08/cm² | <30 | Monitor |
| Via | >30nm | 0.05/cm² | <20 | Hold if cluster |

### 2.3 Inspection Sensitivity Optimization

```python
def optimize_sensitivity(layer, yield_impact, throughput_limit):
    """
    Dynamic sensitivity adjustment based on:
    - Historical defect density
    - Yield correlation
    - Throughput constraints
    """
    baseline_sensitivity = get_baseline(layer)
    defect_history = get_defect_trend(layer, days=30)
    
    if defect_history.trending_up():
        sensitivity = baseline_sensitivity * 0.8  # More sensitive
    elif yield_impact < threshold:
        sensitivity = baseline_sensitivity * 1.2  # Less sensitive
    
    return min(sensitivity, throughput_limit)
```

---

## 3. Defect Classification System

### 3.1 Automatic Defect Classification (ADC)

```
Classification Hierarchy:
├── Killer Defects (Yield Impact)
│   ├── Bridges (Metal/Poly)
│   ├── Opens (Via/Contact)
│   ├── Missing Pattern
│   └── Extra Pattern
├── Reliability Risks
│   ├── Partial Via
│   ├── Metal Thinning
│   ├── Gate Oxide Defects
│   └── Residue
└── Nuisance/False
    ├── Color Variation
    ├── Previous Layer
    └── Noise

ADC Accuracy Target: >90%
Manual Review: <10% of defects
```

### 3.2 Defect Binning and Coding

| Bin Code | Category | Impact | Review Priority |
|----------|----------|---------|-----------------|
| 01-09 | Pattern defects | Killer | Immediate |
| 10-19 | Particles | High | High |
| 20-29 | Residue | Medium | Medium |
| 30-39 | Scratches | Variable | Sample |
| 40-49 | Process variation | Low | Trend |
| 90-99 | False/Nuisance | None | Skip |

### 3.3 Machine Learning Classification

```python
# Deep Learning Defect Classifier
model_architecture = {
    'input': 'SEM images 512x512',
    'backbone': 'ResNet50',
    'classifier': 'Multi-class (50 categories)',
    'training_data': '1M+ labeled defects',
    'accuracy': '95.5%',
    'inference_time': '<100ms'
}

# Continuous Learning Pipeline
def update_classifier(new_defects, labels):
    if len(new_defects) > 1000:
        retrain_model(incremental=True)
        validate_performance()
        deploy_if_improved()
```

---

## 4. Statistical Process Control

### 4.1 Defect Density Control Charts

```
Control Chart Configuration:
- Type: C-chart for count data
- Subgroup: Per wafer or lot
- Limits: Based on Poisson distribution
- UCL = λ + 3√λ
- LCL = max(0, λ - 3√λ)

Trend Detection Rules:
1. Single point > UCL
2. 2 of 3 points > 2σ
3. 4 of 5 points > 1σ
4. 8 consecutive points same side
5. 6 points trending
```

### 4.2 Spatial Signature Analysis

```
Signature Recognition Algorithms:
- Radial patterns: Process uniformity
- Repeating defects: Reticle/Scanner
- Clusters: Local events
- Scratches: Handling damage
- Edge effects: Process margin

Signature Library:
1. Center-high: Chuck contamination
2. Edge ring: EBR issue
3. Scan direction: Scanner problem
4. Repeating 26x33: Reticle defect
5. Random: Particles
```

### 4.3 Process Capability Metrics

| Metric | Current | Target | Best Practice |
|--------|---------|--------|---------------|
| D₀ (defects/cm²) | 0.025 | <0.020 | <0.010 |
| Capture Rate | 92% | >95% | >98% |
| False Rate | 8% | <5% | <2% |
| Review Rate | 15% | <10% | <5% |
| ADC Accuracy | 88% | >90% | >95% |

---

## 5. Sampling Strategies

### 5.1 Intelligent Sampling

```
Risk-Based Sampling Algorithm:
Sample_Rate = Base_Rate × Risk_Factor × History_Factor

Where:
- Base_Rate: Default sampling (20%)
- Risk_Factor: Layer criticality (0.5-2.0)
- History_Factor: Recent performance (0.5-1.5)

Dynamic Adjustment:
if defect_density > UCL:
    increase_sampling(2x)
elif consecutive_good > 10:
    reduce_sampling(0.5x)
```

### 5.2 Lot Sampling Plans

| Lot Type | Inspection Coverage | Review Strategy |
|----------|-------------------|-----------------|
| Development | 100% all wafers | 100% killer defects |
| Qualification | 50% wafers | 50% all defects |
| Production | 20% or 3 wafers | Smart review |
| Monitor | 100% | Trend analysis |
| Rework | 100% | Focus on issue |

### 5.3 Skip Lot Qualification

```
Skip Lot Criteria:
- 20 consecutive lots pass
- D₀ stable (Cpk > 1.67)
- No excursions
- No process changes

Skip Rate Limits:
- Maximum: 80% skip
- Minimum inspection: 1 wafer/lot
- Random audit: 10%
- Full inspection triggers
```

---

## 6. Defect Review and Dispositioning

### 6.1 Review Sampling Strategy

```python
def smart_review_selection(defects):
    """
    Intelligent selection of defects for SEM review
    """
    review_list = []
    
    # Always review killer defects
    review_list.extend(defects[defects.class == 'killer'])
    
    # Sample by size and location diversity
    for bin in defect_bins:
        samples = stratified_sample(
            defects[defects.bin == bin],
            by=['size', 'location'],
            n=min(5, len(defects)*0.1)
        )
        review_list.extend(samples)
    
    return review_list[:MAX_REVIEW_COUNT]
```

### 6.2 Disposition Criteria

| Defect Density | Action | Authority | Customer Notice |
|---------------|---------|-----------|-----------------|
| < Baseline | Release | Operator | No |
| Baseline-UCL | Monitor | Engineer | No |
| > UCL | Hold | Engineer | If requested |
| > 2×UCL | Hold + Review | Manager | Yes |
| Cluster/Systematic | Hold | Manager | Yes |

### 6.3 Excursion Response

```
Excursion Response Timeline:
T+0: Defect excursion detected
T+30min: Initial assessment
T+2hr: Root cause investigation
T+4hr: Containment action
T+8hr: Corrective action plan
T+24hr: Implementation
T+48hr: Effectiveness verification
```

---

## 7. Yield Impact Analysis

### 7.1 Defect to Yield Correlation

```
Yield Model:
Y = Y₀ × ∏(1 - Dᵢ × Aᵢ × Kᵢ)

Where:
Y₀ = Baseline yield
Dᵢ = Defect density for type i
Aᵢ = Die area
Kᵢ = Kill ratio for defect type i

Kill Ratios (empirical):
- Bridge: 0.95
- Open: 0.90
- Particle: 0.30
- Residue: 0.20
- Cosmetic: 0.05
```

### 7.2 Critical Area Analysis

| Layer | Feature | Critical Area | Weight |
|-------|---------|---------------|--------|
| Poly | Gate | 0.15 | 1.0 |
| Contact | Hole | 0.08 | 0.9 |
| M1 | Line | 0.25 | 0.8 |
| Via1 | Via | 0.10 | 0.9 |
| M2 | Line | 0.30 | 0.7 |

### 7.3 Yield Learning Curves

```
Defect Reduction Roadmap:
Month 1-3: Baseline (D₀ = 0.10)
Month 4-6: Tool optimization (D₀ = 0.05)
Month 7-9: Process improvement (D₀ = 0.03)
Month 10-12: Mature (D₀ = 0.02)
Target: D₀ < 0.01 for HVM
```

---

## 8. Advanced Detection Technologies

### 8.1 E-beam Inspection

```
Voltage Contrast Applications:
- Contact/Via opens
- Electrical shorts
- Leakage paths
- Gate oxide integrity

Operating Conditions:
- Beam Energy: 500-1000eV
- Current: 100-500nA
- Pixel Size: 10-20nm
- Throughput: 2-5 wph
```

### 8.2 Multi-Modal Inspection

| Mode | Application | Advantage | Limitation |
|------|-------------|-----------|------------|
| Brightfield | Pattern defects | High resolution | Slow |
| Darkfield | Particles | Fast | Lower resolution |
| Phase Shift | Transparent films | Height sensitive | Complex |
| Fluorescence | Organic residue | Specific | Limited materials |

### 8.3 Machine Learning Enhancement

```python
# Predictive Defect Detection
class DefectPredictor:
    def __init__(self):
        self.model = load_model('lstm_defect_predictor')
        
    def predict_excursion(self, process_data):
        features = extract_features(process_data)
        risk_score = self.model.predict(features)
        
        if risk_score > 0.8:
            trigger_inspection(priority='high')
            alert_engineer()
        
        return risk_score
```

---

## 9. Defect Reduction Programs

### 9.1 Systematic Defect Reduction

```
PDCA Approach:
Plan:
- Pareto analysis
- Root cause hypothesis
- DOE planning

Do:
- Implement changes
- Controlled experiment
- Data collection

Check:
- Statistical analysis
- Yield correlation
- Cost-benefit

Act:
- Standardize improvements
- Update procedures
- Monitor sustainability
```

### 9.2 Defect Reduction Targets

| Quarter | Particle | Pattern | Residue | Overall D₀ |
|---------|---------|---------|---------|------------|
| Q1 2024 | 0.015 | 0.008 | 0.005 | 0.028 |
| Q2 2024 | 0.012 | 0.006 | 0.004 | 0.022 |
| Q3 2024 | 0.010 | 0.005 | 0.003 | 0.018 |
| Q4 2024 | 0.008 | 0.004 | 0.002 | 0.014 |

### 9.3 Best Known Methods

```
Particle Reduction:
1. HEPA filter upgrade
2. Wafer handling optimization
3. Chemical filtration
4. Equipment PM optimization
5. Cleanroom protocol

Pattern Defect Reduction:
1. Process window centering
2. OPC optimization
3. Scanner maintenance
4. Resist/Developer optimization
5. CD uniformity improvement
```

---

## 10. Documentation and Reporting

### 10.1 Defect Database Management

```
Data Structure:
Lot_ID → Wafer_ID → Inspection_ID → Defect_ID
    ↓
Attributes:
- Coordinates (x, y)
- Size (area, height)
- Classification
- Image (reference)
- Review results
- Disposition

Retention Policy:
- Summary data: 5 years
- Images: 1 year
- Detailed data: 90 days
```

### 10.2 Reporting Requirements

| Report | Frequency | Audience | Content |
|--------|-----------|----------|---------|
| Daily Defect | Daily | Operations | Excursions, trends |
| Weekly Summary | Weekly | Management | Pareto, actions |
| Monthly Review | Monthly | All stakeholders | Full analysis |
| Customer Report | Per request | Customer | Specific data |

### 10.3 Key Metrics Dashboard

```
Real-time Dashboard Elements:
- Current D₀ by layer
- Trend charts (24hr, 7day, 30day)
- Excursion alerts
- Pareto by defect type
- Yield correlation
- Tool availability
- Review queue status
- Action item tracker
```

---

## Appendix A: Defect Size Standards

| Technology Node | Critical Size | Inspection Capability |
|-----------------|---------------|----------------------|
| 7nm | 20nm | 15nm |
| 5nm | 15nm | 12nm |
| 3nm | 10nm | 8nm |
| 2nm | 8nm | 6nm |

---

## Appendix B: Statistical Methods

### Poisson Distribution for Defects
```
P(x) = (λˣ × e⁻λ) / x!
Where λ = average defect count
Used for random defect modeling
```

### Cluster Analysis
```
Nearest Neighbor Distance:
If distance < critical_distance:
    Mark as cluster
    Investigate systematic cause
```

---

**Document Approval:**
- Defect Engineering: ___________
- Quality Manager: ___________
- Operations Manager: ___________
- Customer Quality: ___________

**Review Date:** 2025-02-15