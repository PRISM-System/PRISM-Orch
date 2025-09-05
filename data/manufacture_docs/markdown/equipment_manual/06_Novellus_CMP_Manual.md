# Chemical Mechanical Polishing 장비 운영 매뉴얼
## Novellus Systems Vector Express CMP

**문서번호:** EM-NOV-VECTOR-001  
**개정일:** 2024.11.15  
**작성:** CMP 공정기술팀  

---

## 1. 장비 개요

### 1.1 System Specifications
- **Model:** Novellus Vector Express
- **Configuration:** 3-platen system with integrated metrology
- **Process:** Cu, W, Oxide, STI CMP
- **Wafer Size:** 300mm
- **Throughput:** 60 WPH (copper process)

### 1.2 Platen Configuration
- **Platen 1:** Bulk removal (Cu, W)
- **Platen 2:** Barrier removal (Ta/TaN)
- **Platen 3:** Touch-up/Buff (final polish)
- **Diameter:** 30 inches per platen
- **Speed Range:** 20-150 RPM
- **Temperature Control:** 10-60°C

### 1.3 Polishing Head
- **Type:** Titan Contour head
- **Zones:** 5 independent pressure zones
- **Pressure Range:** 0.5-8 PSI per zone
- **Retaining Ring:** Replaceable, PPS material
- **Rotation:** 20-150 RPM independent

### 1.4 Slurry Delivery System
- **Delivery Type:** Point-of-use mixing
- **Flow Control:** Mass flow controllers
- **Temperature:** 22°C ± 1°C
- **Filtration:** 0.45µm at point-of-use
- **Abrasive Types:** Silica, Ceria, Alumina

### 1.5 Endpoint Detection
- **Technology:** Optical endpoint (OEP)
- **Motor Current:** Friction-based endpoint
- **Eddy Current:** Metal film monitoring
- **Integration:** Real-time process control

---

## 2. Installation Requirements

### 2.1 Facility Requirements

#### Environmental Conditions
- **Temperature:** 21°C ± 1°C
- **Humidity:** 45% ± 5%
- **Cleanroom:** ISO Class 5
- **Vibration:** VC-D specification
- **Floor:** Chemical resistant epoxy

#### Power Requirements
- **Main Power:** 480V, 3-phase, 200A
- **Frequency:** 60Hz ± 1%
- **Emergency Stop:** Multiple E-stop locations
- **UPS:** Critical controls only

#### Utilities
| Utility | Specification | Consumption |
|---------|--------------|-------------|
| DIW | 18.2 MΩ·cm, 22°C | 200 L/min |
| CDA | 90 PSI, oil-free | 100 CFM |
| N2 | 99.999%, 60 PSI | 500 L/min |
| Vacuum | -80 kPa | 50 CFM |
| Drain | Chemical waste | 250 L/min |

### 2.2 Chemical Requirements

#### Slurry Specifications
| Type | Abrasive | pH | Particle Size |
|------|----------|-----|---------------|
| Cu | Silica | 4-5 | 50-100nm |
| Barrier | Silica | 10-11 | 30-50nm |
| Oxide | Ceria | 7-8 | 100-200nm |
| W | Alumina | 2-3 | 200nm |

#### Chemical Storage
- **Capacity:** 200L drums
- **Temperature:** 20-25°C
- **Agitation:** Continuous stirring
- **Shelf Life:** Monitor expiration

### 2.3 Equipment Layout
- **Footprint:** 6m x 4m
- **Service Access:** 1.5m all sides
- **Height:** 3.5m minimum
- **Weight:** 12,000 kg
- **Drain Location:** Within 2m

---

## 3. Process Parameters

### 3.1 Copper CMP Process

#### Step 1: Bulk Cu Removal
```
Platen 1 Parameters:
- Pad: IC1010 (K-groove)
- Down Force: 3.0 PSI
- Platen Speed: 93 RPM
- Head Speed: 87 RPM
- Slurry Flow: 200 mL/min
- Removal Rate: 6000 Å/min
- Endpoint: Eddy current signal
```

#### Step 2: Barrier Removal
```
Platen 2 Parameters:
- Pad: Politex
- Down Force: 2.5 PSI
- Platen Speed: 63 RPM
- Head Speed: 57 RPM
- Slurry Flow: 150 mL/min
- Over-polish: 20% of barrier thickness
- Selectivity Cu:Ta > 50:1
```

#### Step 3: Touch-up Polish
```
Platen 3 Parameters:
- Pad: Suba IV
- Down Force: 1.5 PSI
- Platen Speed: 50 RPM
- Head Speed: 47 RPM
- DIW Only: 500 mL/min
- Time: 10 seconds
- Purpose: Defect reduction
```

### 3.2 STI (Shallow Trench Isolation) CMP

#### High Selectivity Slurry Process
```
Process Flow:
1. Oxide Polish
   - Pad: IC1010
   - Pressure: 4.0 PSI
   - Ce-based slurry
   - Rate: 3000 Å/min
   - Selectivity Ox:SiN > 30:1

2. Endpoint Detection
   - Motor current monitoring
   - Pattern density compensation
   - Real-time rate adjustment

3. Over-polish
   - Time: 10-15% of main polish
   - Reduced pressure: 2.0 PSI
   - Purpose: Clearing residuals
```

### 3.3 Tungsten CMP

#### Contact/Via Plug Process
```
W Polish Parameters:
- Pad: IC1010 perforated
- Pressure Profile:
  - Center: 3.5 PSI
  - Middle: 3.0 PSI  
  - Edge: 4.0 PSI
- Slurry: Acidic alumina
- pH: 2.5 ± 0.2
- Temperature: 35°C
- Endpoint: Optical reflectance
```

---

## 4. Pad Management

### 4.1 Pad Conditioning

#### In-situ Conditioning
- **Disk Type:** 3M A165 diamond disk
- **Grit Size:** 100-180 µm diamonds
- **Down Force:** 7-9 lbs
- **Sweep Pattern:** Full pad coverage
- **Frequency:** During each wafer polish

#### Ex-situ Conditioning
- **Purpose:** Pad break-in and regeneration
- **Duration:** 30 minutes for new pad
- **Parameters:**
  - High down force: 12 lbs
  - Aggressive sweep
  - Slurry application

### 4.2 Pad Life Management

#### Monitoring Parameters
- **Thickness:** Measure weekly
- **Groove Depth:** > 15 mils minimum
- **Surface Roughness:** Ra monitoring
- **Removal Rate:** Track degradation

#### Replacement Criteria
- **Thickness:** < 50% of original
- **Groove Depth:** < 10 mils
- **Rate Drop:** > 20% from baseline
- **Defects:** Excessive scratches

### 4.3 Pad Installation

#### Installation Procedure
1. **Surface Preparation**
   - Clean platen with IPA
   - Check platen flatness
   - Remove old adhesive

2. **Pad Mounting**
   - Apply adhesive evenly
   - Position pad carefully
   - Remove air bubbles
   - Apply uniform pressure

3. **Break-in Process**
   - Initial conditioning: 30 min
   - Dummy wafers: 25 wafers
   - Rate qualification
   - Defect qualification

---

## 5. Endpoint Detection Systems

### 5.1 Optical Endpoint (OEP)

#### Principle of Operation
- **Light Source:** Broad spectrum LED
- **Detection:** Reflectance change
- **Wavelength:** 400-700nm
- **Sampling Rate:** 10 Hz

#### Setup and Calibration
1. **Spectrum Acquisition**
   - Pre-polish reference
   - Film stack modeling
   - Wavelength selection

2. **Algorithm Selection**
   - Peak detection
   - Derivative analysis
   - Pattern matching

3. **Threshold Setting**
   - Signal-to-noise > 3:1
   - Confidence level: 95%
   - Time window: 5 seconds

### 5.2 Eddy Current Monitoring

#### Metal Film Detection
- **Frequency:** 2-8 MHz
- **Sensitivity:** 100Å Cu remaining
- **Calibration:** Known thickness wafers
- **Application:** Cu clearing

#### Real-time Control
```python
if eddy_current_signal < threshold:
    transition_to_barrier_removal()
    adjust_removal_rate()
    log_endpoint_time()
```

### 5.3 Motor Current Endpoint

#### Friction-based Detection
- **Principle:** Torque change at interface
- **Sensitivity:** Material dependent
- **Filter:** Low-pass 1 Hz
- **Trigger:** Derivative threshold

---

## 6. Metrology Integration

### 6.1 Integrated Thickness Measurement

#### Pre-CMP Measurement
- **Technology:** Eddy current/Optical
- **Points:** 49-point map
- **Purpose:** Incoming thickness
- **Feed-forward:** Polish time calculation

#### Post-CMP Measurement
- **Technology:** Same as pre
- **Points:** 49-point map
- **Metrics:** Remaining, removal, uniformity
- **Feedback:** Recipe adjustment

### 6.2 Process Control

#### Run-to-Run Control
```
Algorithm:
1. Measure post-CMP thickness
2. Calculate removal amount
3. Compare to target
4. Adjust polish time:
   New_time = Old_time × (Target/Actual)
5. Apply EWMA filter (λ=0.3)
6. Update recipe database
```

#### Within-Wafer Uniformity Control
- **Zone Pressure Adjustment:**
  - Center fast: Reduce center pressure
  - Edge fast: Increase edge pressure
  - Donut pattern: Adjust middle zones

### 6.3 Defect Inspection

#### Inline Defect Monitoring
- **Inspection Tool:** KLA SP3/SP5
- **Sampling:** 100% for development, 10% production
- **Defect Types:**
  - Scratches
  - Particles
  - Residues
  - Corrosion

---

## 7. Maintenance Procedures

### 7.1 Daily Maintenance

#### Start-of-Day Checklist
1. **Slurry System**
   - Check drum levels
   - Verify flow rates
   - Check filter pressure
   - Inspect delivery lines

2. **Pad Inspection**
   - Visual check for damage
   - Groove depth spot check
   - Conditioning disk inspection

3. **Consumables Check**
   - Retaining rings
   - Membrane condition
   - Backing films

#### Shift Pass-down
- Process issues
- Maintenance performed
- Consumable changes
- Quality excursions

### 7.2 Weekly Maintenance

#### Comprehensive Cleaning
1. **Platen Cleaning**
   - Remove pad debris
   - Clean platen surface
   - Check temperature sensors

2. **Head Maintenance**
   - Membrane inspection
   - Zone pressure test
   - Gimbal check

3. **Slurry System**
   - Line flush
   - Filter replacement
   - Flow rate calibration

### 7.3 Monthly Maintenance

#### Preventive Maintenance Schedule
1. **Mechanical Systems**
   - Belt tension check
   - Bearing lubrication
   - Motor current baseline
   - Encoder verification

2. **Pneumatic Systems**
   - Regulator calibration
   - Leak detection
   - Valve operation test
   - Actuator speed check

3. **Conditioning System**
   - Disk replacement
   - Arm calibration
   - Sweep verification
   - Down force calibration

### 7.4 Quarterly Maintenance

#### Major Overhaul
1. **Complete System PM**
   - Duration: 24 hours
   - All wear parts replacement
   - Full calibration
   - Performance qualification

2. **Specific Tasks**
   - Spindle bearing service
   - Load cup overhaul
   - Robot teaching
   - Software backup

---

## 8. Process Troubleshooting

### 8.1 Dishing and Erosion

#### Problem: Excessive Cu dishing > 500Å
**Root Cause Analysis:**
1. **Over-polish Time**
   - Review endpoint trace
   - Check over-polish percentage

2. **Down Force**
   - Verify pressure settings
   - Check membrane integrity

3. **Slurry Chemistry**
   - pH verification
   - Oxidizer concentration
   - Inhibitor level

**Solutions:**
- Reduce over-polish time
- Optimize pressure profile
- Adjust slurry chemistry
- Implement selective slurry

### 8.2 Within-Die Non-uniformity

#### Problem: Center-to-edge > 5%
**Investigation:**
1. **Pattern Density Effect**
   - Review layout
   - Calculate pattern factor

2. **Pressure Distribution**
   - Zone pressure mapping
   - Retaining ring wear

3. **Slurry Distribution**
   - Flow rate verification
   - Dispense arm position

**Corrective Actions:**
- Adjust zone pressures
- Modify slurry flow
- Replace retaining ring
- Optimize conditioning

### 8.3 Scratch Defects

#### Problem: Scratches > 10 per wafer
**Systematic Check:**
1. **Particle Source**
   - Slurry contamination
   - Dried slurry on pad
   - Conditioning debris

2. **Mechanical Issues**
   - Pad damage
   - Head membrane torn
   - Transport contact

3. **Process Parameters**
   - Excessive down force
   - Insufficient slurry
   - Poor pad conditioning

**Resolution Steps:**
- Filter replacement
- Pad inspection/replacement
- Reduce down force
- Increase slurry flow
- Optimize conditioning

### 8.4 Corrosion Issues

#### Problem: Cu corrosion spots
**Critical Factors:**
1. **Post-CMP Clean**
   - Rinse time insufficient
   - pH not neutralized
   - Drying incomplete

2. **Queue Time**
   - Exposure to ambient
   - Humidity effect
   - Temperature variation

3. **Chemical Interaction**
   - Slurry residue
   - Galvanic corrosion
   - BTA concentration

**Prevention:**
- Immediate rinse
- pH adjustment
- Anti-corrosion agent
- Reduce queue time

---

## 9. Advanced Process Control

### 9.1 Virtual Metrology

#### Model Development
```
Inputs:
- Incoming thickness (nm)
- Polish time (sec)
- Down force (PSI)
- Pad life (wafers)
- Slurry age (hours)

Model:
- Neural network
- 3 hidden layers
- Training set: 1000 wafers

Output:
- Predicted thickness
- Confidence interval
- Anomaly detection
```

### 9.2 Fault Detection

#### Real-time Monitoring
| Parameter | Sampling | Limits | Action |
|-----------|----------|--------|--------|
| Motor current | 10 Hz | ± 10% | Alarm |
| Slurry flow | 1 Hz | ± 5% | Adjust |
| Temperature | 1 Hz | ± 2°C | Hold |
| Vibration | 100 Hz | < 2g | Stop |

#### Multivariate Analysis
- **Method:** PCA (Principal Component Analysis)
- **Variables:** 50+ process parameters
- **Detection:** Hotelling T² statistic
- **Response:** Automated classification

### 9.3 Process Optimization

#### Design of Experiments (DOE)
```
Factorial Design:
Factors:
- Pressure: 2, 3, 4 PSI
- Speed: 60, 75, 90 RPM
- Slurry flow: 150, 200, 250 mL/min

Responses:
- Removal rate
- Uniformity
- Defects
- Dishing

Analysis:
- Main effects
- Interactions
- Response surface
- Optimization
```

---

## 10. Safety and Environmental

### 10.1 Chemical Safety

#### Hazardous Materials
| Chemical | Hazard | PPE Required | Spill Response |
|----------|--------|--------------|----------------|
| H2O2 | Oxidizer | Gloves, goggles | Dilute with water |
| KOH | Caustic | Full suit | Neutralize with acid |
| BTA | Toxic | Respirator | Contain and absorb |
| NH4OH | Corrosive | Face shield | Ventilate area |

#### Emergency Procedures
1. **Chemical Spill**
   - Alert personnel
   - Contain spill
   - Use appropriate neutralizer
   - Dispose properly

2. **Exposure Protocol**
   - Eye wash: 15 minutes
   - Shower: Remove clothing
   - Medical attention
   - Document incident

### 10.2 Waste Management

#### Waste Streams
- **Copper Waste:** Separate collection
- **Slurry Waste:** pH adjustment required
- **Pad Waste:** Solid waste disposal
- **Rinse Water:** Treatment system

#### Environmental Compliance
- **Discharge Limits:**
  - Cu: < 2 ppm
  - pH: 6-9
  - TSS: < 30 mg/L
- **Monitoring:** Daily sampling
- **Reporting:** Monthly to authorities

### 10.3 Ergonomics

#### Manual Handling
- **Slurry Drums:** Use drum dolly
- **Pad Changes:** Two-person lift
- **Head Service:** Use lifting fixture
- **Repetitive Tasks:** Rotate personnel

---

## 11. Performance Metrics

### 11.1 Process Capability

#### Key Metrics
| Metric | Specification | Cpk | Current |
|--------|--------------|-----|---------|
| Removal Rate | ± 10% | > 1.33 | 1.45 |
| Uniformity | < 3% | > 1.67 | 1.82 |
| Dishing | < 300Å | > 1.33 | 1.41 |
| Erosion | < 200Å | > 1.33 | 1.38 |

### 11.2 Equipment Performance

#### Productivity Metrics
- **Throughput:** 58 WPH actual
- **Availability:** 94%
- **MTBF:** 168 hours
- **MTTR:** 2.5 hours
- **OEE:** 87%

### 11.3 Cost Analysis

#### Cost per Wafer
```
Consumables:
- Slurry: $4.50
- Pad: $1.20
- Disk: $0.30
- Other: $0.50
Subtotal: $6.50

Maintenance: $2.00
Utilities: $1.50
Total: $10.00/wafer
```

#### Cost Reduction Projects
1. Slurry reduction (200→150 mL/min)
2. Pad life extension (2000→2500 wafers)
3. Reduced over-polish (20%→15%)
4. Chemical recycling evaluation

---

## Appendix A: Process Recipe Library

### Production Recipes
| Recipe | Application | Removal (Å) | Time (sec) |
|--------|-------------|-------------|------------|
| CU_BULK_01 | 12k Cu | 12000 | 120 |
| BARRIER_01 | 250Å Ta/TaN | 300 | 45 |
| OXIDE_ILD | 5k oxide | 5000 | 100 |
| W_PLUG | 8k W | 8000 | 160 |
| STI_01 | 7k STI | 7000 | 140 |

### Development Recipes
| Recipe | Purpose | Status |
|--------|---------|--------|
| LOW_K_01 | k=2.5 dielectric | Qual |
| CO_BARRIER | Cobalt barrier | Dev |
| RU_LINER | Ruthenium | Research |

---

## Appendix B: Troubleshooting Matrix

### Quick Reference
| Symptom | Probable Cause | Check | Action |
|---------|---------------|-------|--------|
| Low rate | Pad glazed | Groove depth | Condition aggressive |
| High defects | Contamination | Slurry/pad | Replace/clean |
| Poor uniformity | Pressure | Zone settings | Adjust profile |
| Dishing | Over-polish | Endpoint | Reduce time |
| Corrosion | Rinse issue | pH, time | Improve clean |

---

**문서 관리:**
- 작성자: CMP 공정팀 정우진 수석
- 검토자: 통합공정팀 이서연 책임
- 승인자: 제조기술부문 김동현 이사
- 차기 개정: 2025년 3월 (Cobalt CMP 추가)