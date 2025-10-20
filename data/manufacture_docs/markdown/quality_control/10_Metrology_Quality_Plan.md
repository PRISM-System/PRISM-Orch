# Metrology 품질 관리 계획서
## Quality Control Plan for Dimensional and Material Metrology

**문서번호:** QCP-METRO-DIM-010  
**개정일:** 2024.11.15  
**적용범위:** Fab-wide Metrology Systems  
**기술노드:** 5nm/3nm Advanced Technology  

---

## 1. 문서 개요

### 1.1 목적 및 범위
- **목적:** 반도체 제조 전 공정의 측정 시스템 품질 관리 체계 확립
- **범위:** CD, Overlay, Film thickness, Composition, Stress 측정
- **목표:** Measurement uncertainty < 3% of tolerance
- **전략:** Total Measurement Uncertainty (TMU) management

### 1.2 Metrology Equipment Portfolio
| Category | Tool | Application | Precision (3σ) |
|----------|------|-------------|---------------|
| CD Metrology | CD-SEM | Critical dimensions | 0.3nm |
| Scatterometry | OCD | Profile/CD | 0.2nm |
| Overlay | Imaging overlay | Registration | 0.5nm |
| Film Thickness | Ellipsometer | Transparent films | 0.5Å |
| Stress | Wafer bow | Film stress | 10MPa |
| Composition | XPS/XRF | Material analysis | 1at% |

---

## 2. Measurement System Analysis (MSA)

### 2.1 Gage R&R Requirements

```
Acceptance Criteria:
%GRR = (σ_measurement/σ_total) × 100

Excellent: %GRR < 10%
Acceptable: %GRR < 30%
Unacceptable: %GRR > 30%

Components:
- Repeatability: Same operator, same part
- Reproducibility: Different operators
- Part variation: Actual process variation
```

### 2.2 Measurement Capability Study

| Parameter | Tool | %GRR | Cp | Cpk | P/T Ratio |
|-----------|------|------|-----|-----|-----------|
| Gate CD | CD-SEM | 8.5% | 2.15 | 1.98 | 0.08 |
| Overlay | Archer | 6.2% | 2.35 | 2.21 | 0.06 |
| Thickness | Ellipsometer | 4.8% | 2.85 | 2.72 | 0.05 |
| Line Profile | AFM | 9.8% | 1.92 | 1.78 | 0.10 |
| Sheet Rs | 4-point probe | 7.5% | 2.05 | 1.91 | 0.08 |

### 2.3 Total Measurement Uncertainty

```python
def calculate_TMU(components):
    """
    TMU = √(u_repeatability² + u_reproducibility² + 
           u_calibration² + u_sampling² + u_environment²)
    """
    tmu_squared = sum([u**2 for u in components])
    tmu = math.sqrt(tmu_squared)
    
    # Expanded uncertainty (k=2, 95% confidence)
    U = 2 * tmu
    
    return {
        'standard_uncertainty': tmu,
        'expanded_uncertainty': U,
        'confidence': 95
    }
```

---

## 3. CD Metrology Control

### 3.1 CD-SEM Measurement Protocol

```
Standard Operating Conditions:
- Acceleration Voltage: 500V (±10V)
- Probe Current: 8pA (±0.5pA)
- Magnification: 100,000× (calibrated)
- Frame Integration: 32 frames
- Measurement Algorithm: Threshold 50%

Site Selection:
- 17 sites per wafer (standard)
- 49 sites for uniformity
- 5 sites for monitor
- Edge exclusion: 3mm
```

### 3.2 Scatterometry (OCD) Control

| Profile Parameter | Specification | Tolerance | Correlation |
|------------------|---------------|-----------|-------------|
| CD Top | Design ±10% | ±0.5nm | R² > 0.95 |
| CD Bottom | Design ±10% | ±0.8nm | R² > 0.93 |
| Sidewall Angle | 88° | ±1° | R² > 0.90 |
| Height | Target ±5% | ±1nm | R² > 0.97 |

### 3.3 Reference Material Program

```
Reference Standards Hierarchy:
NIST Traceable → Master Standard → Working Standard
                        ↓                ↓
                  Quarterly Cal      Daily Check

CD Standards:
- 100nm pitch grating (NIST certified)
- 45nm isolated line (master)
- Process monitor wafer (working)

Calibration Frequency:
- Daily: Working standard
- Weekly: Tool matching
- Monthly: Master standard
- Quarterly: NIST traceable
```

---

## 4. Overlay Metrology Management

### 4.1 Overlay Measurement Strategy

```
Measurement Modes:
1. Image-Based Overlay (IBO)
   - Box-in-box targets
   - Accuracy: ±0.5nm
   - Speed: Fast

2. Diffraction-Based Overlay (DBO)
   - Grating targets
   - Accuracy: ±0.3nm
   - Speed: Medium

3. In-Device Overlay
   - Actual device features
   - Accuracy: ±1.0nm
   - Correlation: Direct
```

### 4.2 Overlay Control Limits

| Layer Pair | Spec (nm) | Mean+3σ | Cpk Target | Current |
|------------|-----------|---------|------------|---------|
| Gate-Active | 3.0 | 2.5 | >1.67 | 1.82 |
| Contact-Gate | 4.0 | 3.2 | >1.67 | 1.75 |
| M1-Contact | 4.0 | 3.5 | >1.67 | 1.71 |
| Via1-M1 | 4.0 | 3.3 | >1.67 | 1.78 |

### 4.3 Overlay Sampling Plans

```
Standard Sampling (Production):
- 13 sites per wafer
- 3 wafers per lot (F/M/L)
- Both X and Y directions
- 4 targets per site

Enhanced Sampling (Development):
- 41 sites per wafer
- All wafers
- Multiple target types
- Correlation to device
```

---

## 5. Film Metrology Control

### 5.1 Thickness Measurement Control

| Film Type | Tool | Range | Accuracy | Precision |
|-----------|------|-------|----------|-----------|
| Oxide | Ellipsometer | 10-5000Å | ±1% | ±0.5% |
| Nitride | Ellipsometer | 50-3000Å | ±1% | ±0.5% |
| Poly-Si | Ellipsometer | 500-5000Å | ±1.5% | ±0.8% |
| Metal | XRF | 100-10000Å | ±2% | ±1% |
| Thin films | XRR | 5-500Å | ±2% | ±1% |

### 5.2 Optical Constants Monitoring

```
Critical Films n&k Control:
Film     λ(nm)  n_target  k_target  Tolerance
SiO₂     633    1.46      0         ±0.01
Si₃N₄    633    2.00      0         ±0.02
Poly-Si  633    3.88      0.02      ±0.05
TiN      633    1.20      2.50      ±0.10

Verification Method:
- Spectroscopic ellipsometry
- Multi-angle measurement
- Cauchy/Tauc-Lorentz fitting
```

### 5.3 Film Property Measurements

| Property | Method | Specification | Frequency |
|----------|--------|---------------|-----------|
| Stress | Wafer bow | <500MPa | Every lot |
| Density | XRR | >95% bulk | Daily |
| Composition | XPS | ±2at% | Weekly |
| Roughness | AFM | <5Å RMS | Daily |
| Uniformity | 49-point | <2% (1σ) | Every wafer |

---

## 6. Calibration and Standards

### 6.1 Calibration Hierarchy

```
Calibration Traceability Chain:
International Standard (SI units)
         ↓
National Standard (NIST/PTB)
         ↓
Primary Reference Material
         ↓
Working Standard
         ↓
Production Measurement
```

### 6.2 Calibration Schedule

| Equipment | Daily | Weekly | Monthly | Annual |
|-----------|-------|--------|---------|--------|
| CD-SEM | Mag check | Full cal | Drift check | Certification |
| Ellipsometer | Verification | Calibration | Model update | Service |
| Overlay tool | TIS check | Calibration | Lens check | Certification |
| AFM | Scanner cal | Tip check | Full cal | Certification |
| XRF | Energy cal | Intensity | Matrix cal | Certification |

### 6.3 Standard Reference Materials

```
SRM Inventory Management:
Material         Stock  Expiry   Usage/month
Si thickness     5      2025-06  2
Line width       3      2025-12  1
Overlay          4      2026-03  1
Particle         10     2025-09  3
Roughness        2      2026-01  0.5

Acceptance Criteria:
- Certificate of calibration
- Uncertainty statement
- Traceability documentation
- Stability verification
```

---

## 7. Statistical Process Control for Metrology

### 7.1 Measurement System SPC

```
Control Charts for Metrology:
- Tool Matching: X̄-R chart
- Repeatability: Moving Range
- Drift: CUSUM
- Calibration: Individual

Control Limits:
UCL = μ + 3σ
LCL = μ - 3σ
Warning = μ ± 2σ
```

### 7.2 Tool-to-Tool Matching

| Tool Pair | Parameter | Offset | Correlation | Action |
|-----------|-----------|--------|-------------|--------|
| CDSEM 1-2 | Gate CD | 0.3nm | 0.98 | Monitor |
| Ellip 1-2 | Thickness | 2Å | 0.99 | OK |
| OVL 1-2 | Overlay X | 0.2nm | 0.97 | Monitor |
| AFM 1-2 | Roughness | 0.5Å | 0.95 | Investigate |

### 7.3 Measurement Trending

```python
def detect_measurement_drift(data, window=20):
    """
    Detect systematic drift in measurement system
    """
    # Calculate moving average
    ma = data.rolling(window=window).mean()
    
    # Calculate drift rate
    drift = np.polyfit(range(len(ma)), ma, 1)[0]
    
    # Alert if significant drift
    if abs(drift) > DRIFT_THRESHOLD:
        alert = f"Measurement drift detected: {drift:.3f} nm/day"
        trigger_calibration()
        
    return drift
```

---

## 8. Advanced Metrology Techniques

### 8.1 Hybrid Metrology

```
Data Fusion Approach:
CD-SEM + Scatterometry + AFM → Unified Profile

Benefits:
- Reduced uncertainty
- Complete profile
- Better correlation
- Throughput optimization

Implementation:
1. Measure subset with all tools
2. Build correlation model
3. Use fast tool for production
4. Periodic verification
```

### 8.2 Machine Learning in Metrology

```python
class VirtualMetrology:
    def __init__(self):
        self.model = self.build_model()
        
    def predict_cd(self, process_params):
        """
        Predict CD from process parameters
        """
        features = [
            process_params['dose'],
            process_params['focus'],
            process_params['peb_temp'],
            process_params['develop_time']
        ]
        
        cd_prediction = self.model.predict(features)
        confidence = self.calculate_confidence(features)
        
        return cd_prediction, confidence
```

### 8.3 In-line vs Off-line Correlation

| Measurement | In-line Tool | Off-line Tool | Correlation |
|-------------|--------------|---------------|-------------|
| CD | CD-SEM | Cross-section | R² = 0.96 |
| Overlay | Optical | CD-SEM | R² = 0.94 |
| Thickness | Ellipsometer | TEM | R² = 0.98 |
| Composition | XRF | SIMS | R² = 0.92 |
| Stress | Wafer bow | XRD | R² = 0.89 |

---

## 9. Metrology Sampling Optimization

### 9.1 Risk-Based Sampling

```
Sampling Decision Matrix:
             Low Process Risk    High Process Risk
Low Value    Minimal (5%)        Standard (20%)
High Value   Standard (20%)      Enhanced (50%)

Factors:
- Process capability (Cpk)
- Layer criticality
- Historical performance
- Customer requirements
```

### 9.2 Adaptive Sampling

```python
def adaptive_sampling_rate(cpk_history, defect_history):
    """
    Dynamically adjust sampling based on performance
    """
    base_rate = 0.20  # 20% baseline
    
    # Adjust for capability
    if cpk_history[-10:].mean() > 2.0:
        rate_multiplier = 0.5
    elif cpk_history[-10:].mean() < 1.33:
        rate_multiplier = 2.0
    else:
        rate_multiplier = 1.0
    
    # Adjust for defects
    if defect_history[-5:].max() > UCL:
        rate_multiplier *= 1.5
        
    return min(base_rate * rate_multiplier, 1.0)
```

### 9.3 Skip Lot Metrology

```
Skip Lot Qualification:
- 30 consecutive lots pass
- All Cpk > 1.67
- No tool changes
- No process changes

Skip Rate:
- Maximum: 90%
- Minimum sampling: 1 wafer/lot
- Critical parameters: No skip
- Audit: 5% random
```

---

## 10. Quality Metrics and Reporting

### 10.1 Metrology KPIs

| KPI | Target | Current | Trend |
|-----|--------|---------|-------|
| Measurement GRR | <10% | 8.2% | ↓ |
| Tool Availability | >95% | 94.5% | ↔ |
| Calibration Compliance | 100% | 100% | → |
| Tool Matching | R²>0.95 | 0.96 | ↑ |
| False Alarm Rate | <5% | 6.2% | ↑ |

### 10.2 Metrology Dashboard

```
Real-time Monitoring Elements:
┌─────────────────────────────┐
│ Tool Status    │ Cal Status │
├────────────────┼────────────┤
│ Measurement    │ Trending   │
│ Capability     │ Charts     │
├────────────────┼────────────┤
│ Tool Matching  │ Alerts     │
└────────────────┴────────────┘

Update Frequency: Every measurement
Alert Threshold: Customizable
Data Retention: 90 days online
```

### 10.3 Customer Reporting

```
Monthly Metrology Report Contents:
1. Executive Summary
   - Key metrics status
   - Major issues/improvements

2. Measurement Capability
   - GRR studies
   - Cpk analysis
   - Tool matching

3. Calibration Status
   - Compliance percentage
   - Upcoming calibrations
   - Issues resolved

4. Improvement Actions
   - Completed projects
   - Ongoing initiatives
   - Future plans
```

---

## Appendix A: Uncertainty Budget Template

| Component | Type | Distribution | Value | u(x) |
|-----------|------|--------------|-------|------|
| Repeatability | A | Normal | σ = 0.2nm | 0.2nm |
| Reproducibility | A | Normal | σ = 0.15nm | 0.15nm |
| Calibration | B | Rectangular | ±0.3nm | 0.17nm |
| Resolution | B | Rectangular | ±0.1nm | 0.06nm |
| **Combined** | - | - | - | **0.31nm** |
| **Expanded (k=2)** | - | - | - | **0.62nm** |

---

## Appendix B: Metrology Best Practices

### CD-SEM Best Practices
1. Daily magnification calibration
2. Consistent measurement algorithm
3. Regular contamination check
4. Automated recipe execution
5. Image quality monitoring

### Ellipsometer Best Practices
1. Model validation with TEM
2. Multi-angle measurement
3. Spot size verification
4. Regular lamp replacement
5. Temperature stabilization

---

**Document Approval:**
- Metrology Manager: ___________
- Quality Engineering: ___________
- Process Integration: ___________
- Customer Quality: ___________

**Next Review:** 2025-02-15