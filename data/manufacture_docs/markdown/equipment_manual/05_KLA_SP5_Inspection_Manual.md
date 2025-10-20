# Defect Inspection System 운영 매뉴얼
## KLA-Tencor Surfscan SP5

**문서번호:** EM-KLA-SP5-001  
**개정일:** 2024.11.15  
**작성:** 검사장비 기술팀  

---

## 1. 장비 개요

### 1.1 System Specifications
- **Model:** KLA-Tencor Surfscan SP5
- **Technology:** Unpatterned Wafer Inspection
- **Detection Capability:** 23nm particles on bare Si
- **Throughput:** 100 WPH @ 26nm sensitivity
- **Wafer Size:** 300mm

### 1.2 Optical System
- **Laser Type:** 266nm UV DUV laser
- **Power:** 100mW nominal
- **Scan Type:** Spiral scanning
- **Collection Channels:** 
  - Narrow: High sensitivity
  - Wide: Large particles
  - Normal: Oblique incidence
- **Detection:** PMT (Photomultiplier Tubes)

### 1.3 Signal Processing
- **ADC Resolution:** 16-bit
- **Sampling Rate:** 1 GHz
- **Real-time Processing:** FPGA-based
- **Defect Classification:** AI-powered
- **Data Storage:** 10TB local storage

### 1.4 Wafer Handling
- **Load Ports:** 2 x FOUP
- **Pre-aligner:** Notch/Flat detection
- **Edge Grip:** Minimum contact
- **Throughput:** Continuous operation

---

## 2. Installation Requirements

### 2.1 Facility Requirements

#### Environmental Specifications
- **Temperature:** 21°C ± 1°C
- **Humidity:** 45% ± 5%
- **Cleanroom:** ISO Class 4
- **Vibration:** VC-D specification
- **Acoustic:** < 65 dBC

#### Power Requirements
- **Main Power:** 208V, 3-phase, 30A
- **Frequency:** 50/60 Hz
- **UPS:** Recommended 30 min
- **Grounding:** < 5 ohms

#### Utilities
| Utility | Specification | Usage |
|---------|--------------|-------|
| CDA | 80 PSI, oil-free | 20 CFM |
| Vacuum | -80 kPa | 10 CFM |
| N2 | 99.999% | 50 L/min |
| Exhaust | Particle filtered | 500 CFM |

### 2.2 Space Requirements
- **Footprint:** 2.5m x 2.0m
- **Service Clearance:** 1m all sides
- **Height:** 2.8m minimum
- **Floor Loading:** 1500 kg/m²

---

## 3. Inspection Recipes and Parameters

### 3.1 Recipe Configuration

#### Sensitivity Settings
```
Recipe Parameters:
├── Optical Configuration
│   ├── Laser Power: 20-100%
│   ├── Channel Selection: Narrow/Wide/Both
│   ├── Polarization: P/S/Circular
│   └── Incident Angle: 65-75°
├── Scan Parameters
│   ├── Scan Speed: 10-200 mm/s
│   ├── Spot Size: 10-50 µm
│   ├── Sampling Density: 50-500 kHz
│   └── Edge Exclusion: 1-5 mm
├── Detection Parameters
│   ├── Gain: PMT voltage setting
│   ├── Threshold: S/N ratio
│   ├── Size Binning: 8 bins
│   └── Classification: Enabled/Disabled
└── Output Format
    ├── KLARF file
    ├── Wafer map
    └── Summary statistics
```

### 3.2 Standard Inspection Types

#### Bare Wafer Qualification
- **Purpose:** Incoming wafer quality
- **Sensitivity:** 30nm
- **Threshold:** < 50 particles @ 30nm
- **Scan Mode:** Full wafer spiral

#### Post-CMP Monitoring
- **Purpose:** Scratch and particle detection
- **Sensitivity:** 45nm for particles
- **Special:** Scratch algorithm enabled
- **Focus:** Micro-scratch detection

#### Post-Etch Inspection
- **Purpose:** Particle and residue detection
- **Sensitivity:** 65nm
- **Channels:** Both narrow and wide
- **Classification:** Particle vs. residue

#### Film Deposition Monitor
- **Purpose:** Particle adders check
- **Method:** Pre/post comparison
- **Sensitivity:** 40nm
- **Acceptance:** < 10 adders

### 3.3 Advanced Detection Algorithms

#### Haze Detection
- **Purpose:** Surface roughness monitoring
- **Method:** Scattered light integration
- **Metric:** Haze units (ppm)
- **Specification:** < 0.1 ppm

#### Slip Line Detection
- **Technology:** Pattern recognition
- **Sensitivity:** 0.5µm width
- **Application:** Thermal process monitoring

#### Edge Inspection
- **Coverage:** 1-5mm from edge
- **Purpose:** Edge chip, contamination
- **Algorithm:** Edge-specific filters

---

## 4. Calibration and Standards

### 4.1 PSL Sphere Calibration

#### Standard Sphere Sizes
| Size (nm) | Purpose | Frequency |
|-----------|---------|-----------|
| 30 | Sensitivity baseline | Daily |
| 47 | Mid-range calibration | Weekly |
| 81 | Large particle | Weekly |
| 120 | Size correlation | Monthly |

#### Calibration Procedure
1. **Load PSL Standard Wafer**
2. **Run Calibration Recipe**
3. **Verify Detection:**
   - Capture efficiency > 95%
   - Size accuracy ± 10%
   - Position accuracy ± 1mm
4. **Update Calibration File**
5. **Document in Log**

### 4.2 System Calibration

#### Laser Power Calibration
- **Tool:** Power meter
- **Position:** At wafer plane
- **Specification:** ± 5% of setpoint
- **Frequency:** Monthly

#### Scanner Calibration
- **Method:** Grid pattern wafer
- **Accuracy:** ± 0.5mm positioning
- **Repeatability:** < 0.1mm
- **Frequency:** Quarterly

#### PMT Calibration
- **Dark Current:** < 1nA
- **Gain Uniformity:** ± 5%
- **Linearity:** R² > 0.999
- **Frequency:** Monthly

---

## 5. Daily Operations

### 5.1 Start-up Procedure

#### Morning Checklist
1. **System Health Check**
   - Laser warm-up: 30 minutes
   - Vacuum system: OK
   - Temperature stable: ± 0.5°C

2. **Calibration Verification**
   - Run 30nm PSL standard
   - Confirm > 95% capture
   - Check false count < 5

3. **Background Check**
   - Run particle-free wafer
   - Verify < 2 counts
   - Document baseline

4. **Communication Check**
   - MES connection active
   - Database accessible
   - Network throughput OK

### 5.2 Production Operation

#### Lot Processing Flow
1. **Recipe Selection**
   - Auto-select from MES
   - Verify parameters
   - Load correct calibration

2. **Wafer Inspection**
   - FOUP load
   - Auto-start sequence
   - Real-time monitoring

3. **Data Review**
   - Auto-classification
   - Outlier detection
   - SPC update

4. **Result Disposition**
   - Pass/Fail determination
   - Hold for review if needed
   - Data upload to MES

### 5.3 End-of-Day Procedure

1. **Complete Running Lots**
2. **Data Backup**
   - Local backup
   - Network archive
   - Clear old files
3. **Maintenance Mode**
   - Laser standby
   - Cover optics
   - Log shutdown

---

## 6. Maintenance Schedule

### 6.1 Daily Maintenance

#### Operator Level
- Visual inspection of optics
- Check laser power indicator
- Verify vacuum levels
- Clean wafer handling area
- Review error log

### 6.2 Weekly Maintenance

#### Technician Level
1. **Optical Cleaning**
   - Collection optics: Lens tissue
   - Windows: IPA wipe
   - Mirrors: Air blow only

2. **Calibration Check**
   - All PSL sizes
   - Update drift chart
   - Adjust if needed

3. **Mechanical Check**
   - Stage smoothness
   - Chuck vacuum
   - Robot alignment

### 6.3 Monthly Maintenance

#### Preventive Maintenance
1. **Deep Cleaning**
   - Disassemble collection optics
   - Clean all optical surfaces
   - Replace filters

2. **System Calibration**
   - Full optical alignment
   - PMT gain optimization
   - Laser power calibration

3. **Performance Verification**
   - Sensitivity test all channels
   - Repeatability study
   - Correlation with other tools

### 6.4 Quarterly Maintenance

#### Major Service
1. **Laser Service**
   - Cavity inspection
   - Mirror alignment
   - Power supply check
   - Cooling system service

2. **Stage Service**
   - Bearing inspection
   - Encoder cleaning
   - Motion profile verification
   - Vibration analysis

3. **Computer System**
   - OS updates
   - Database optimization
   - Storage cleanup
   - Security patches

---

## 7. Troubleshooting Guide

### 7.1 High False Count

#### Problem: False counts > 10
**Diagnostic Steps:**
1. **Check Background**
   - Run clean wafer
   - Verify chamber cleanliness
   - Check for light leaks

2. **Optical System**
   - Inspect for contamination
   - Verify laser stability
   - Check PMT noise

3. **Vibration Check**
   - Monitor during scan
   - Check floor vibration
   - Verify isolation system

**Solutions:**
- Clean optics thoroughly
- Adjust threshold settings
- Replace PMT if noisy
- Address vibration sources

### 7.2 Low Sensitivity

#### Problem: Missing known particles
**Investigation:**
1. **Calibration Status**
   - Run PSL standards
   - Check capture rate
   - Verify size accuracy

2. **Laser Power**
   - Measure actual power
   - Check beam quality
   - Verify alignment

3. **Detection Chain**
   - PMT gain setting
   - Signal processing
   - Threshold optimization

**Corrective Actions:**
- Recalibrate system
- Increase laser power
- Optimize PMT gain
- Lower threshold carefully

### 7.3 Classification Errors

#### Problem: Misclassification > 20%
**Analysis:**
1. **Training Set Review**
   - Sufficient samples?
   - Representative defects?
   - Recent updates?

2. **Feature Extraction**
   - Signal quality
   - All channels working?
   - Proper normalization?

3. **Classification Model**
   - Model version current?
   - Parameters optimized?
   - Confidence thresholds?

**Resolution:**
- Retrain classifier
- Update defect library
- Adjust confidence levels
- Manual review subset

---

## 8. Data Management

### 8.1 File Formats

#### KLARF (KLA Results File)
- **Content:** Defect coordinates, size, class
- **Format:** ASCII text
- **Size:** 1-10 MB typical
- **Retention:** 90 days local

#### Wafer Maps
- **Format:** Binary or image
- **Resolution:** 100 pixels/inch
- **Color Coding:** By size/class
- **Usage:** Visual review

#### Summary Reports
- **Format:** CSV, XML
- **Content:** Statistics, trends
- **Frequency:** Per lot/wafer
- **Distribution:** Auto email

### 8.2 Database Integration

#### MES Integration
- **Protocol:** SECS/GEM
- **Data Points:** 50+ parameters
- **Update Rate:** Real-time
- **Error Handling:** Auto retry

#### Yield Management System
- **Upload:** Automatic
- **Parameters:** All defect data
- **Correlation:** With yield data
- **Analysis:** Trend charts

### 8.3 Data Analysis

#### Statistical Process Control
- **Charts:** P-chart, C-chart
- **Limits:** ± 3σ
- **Rules:** Western Electric
- **Actions:** Auto-alert

#### Spatial Signature Analysis
- **Purpose:** Systematic defects
- **Method:** Wafer map stacking
- **Detection:** Pattern recognition
- **Output:** Signature library

---

## 9. Advanced Applications

### 9.1 Process Monitor Wafers

#### Types and Usage
| Type | Purpose | Frequency | Spec |
|------|---------|-----------|------|
| Bare Si | Baseline | Daily | < 10 @ 30nm |
| Post-CVD | Particle adders | Per lot | < 5 adders |
| Post-CMP | Scratches | Per lot | 0 scratches |
| Post-Etch | Residue | Sample | < 20 @ 65nm |

### 9.2 Excursion Detection

#### Real-time Monitoring
- **Threshold:** 3σ from baseline
- **Response:** Auto-hold lot
- **Notification:** Email/SMS
- **Escalation:** 15 min timeline

#### Root Cause Analysis
1. **Defect Gallery Review**
2. **Spatial Analysis**
3. **Time Correlation**
4. **Tool Commonality**
5. **Material Trace**

### 9.3 Predictive Maintenance

#### Tool Health Monitoring
- **Laser Power Trend:** Degradation rate
- **PMT Gain Drift:** Aging indicator
- **Stage Repeatability:** Wear detection
- **False Count Trend:** Contamination

#### Predictive Models
- **Algorithm:** Machine learning
- **Inputs:** 100+ parameters
- **Output:** Failure probability
- **Accuracy:** > 85%

---

## 10. Performance Metrics

### 10.1 Key Performance Indicators

#### Sensitivity Metrics
| Particle Size | Capture Rate | False Count |
|--------------|--------------|-------------|
| 30nm | > 95% | < 5 |
| 45nm | > 98% | < 3 |
| 65nm | > 99% | < 2 |

#### Throughput Metrics
- **Mechanical Time:** 30 sec/wafer
- **Inspection Time:** 25 sec @ 45nm
- **Total Time:** < 60 sec/wafer
- **Availability:** > 95%

### 10.2 Correlation Studies

#### Tool-to-Tool Matching
- **Method:** Split lot study
- **Requirement:** R² > 0.95
- **Parameters:** Count, size, location
- **Frequency:** Monthly

#### SEM Verification
- **Sample Size:** 20 defects
- **Accuracy:** ± 15% size
- **Real vs. False:** > 90% correct
- **Documentation:** Required

### 10.3 Cost of Ownership

#### Operating Costs
| Item | Cost/Month | Notes |
|------|------------|-------|
| PSL Standards | $500 | Consumable |
| Laser Maintenance | $2,000 | Contract |
| Utilities | $800 | Power, gases |
| Total | $3,300 | ~$0.05/wafer |

#### ROI Calculation
- **Yield Improvement:** 0.5%
- **Wafer Value:** $5,000
- **Detection Rate:** 95%
- **Payback Period:** < 6 months

---

## Appendix A: Recipe Library

### Standard Recipes
| Recipe Name | Application | Sensitivity | Throughput |
|-------------|-------------|-------------|------------|
| BARE_30 | Incoming | 30nm | 80 WPH |
| CMP_45 | Post-CMP | 45nm | 100 WPH |
| CVD_40 | Post-depo | 40nm | 90 WPH |
| ETCH_65 | Post-etch | 65nm | 120 WPH |

### Special Recipes
| Recipe Name | Purpose | Special Features |
|-------------|---------|------------------|
| HAZE_01 | Haze measurement | Integration mode |
| SLIP_01 | Slip detection | Pattern recognition |
| EDGE_01 | Edge inspection | 1mm exclusion |
| BACKSIDE | Backside check | Flip handling |

---

## Appendix B: Defect Classification

### Defect Categories
| Class | Description | Size Range | Action |
|-------|-------------|------------|--------|
| 1 | Particles | > 30nm | Monitor |
| 2 | Scratches | Width > 0.5µm | Review |
| 3 | Pits | Depth > 10nm | Investigate |
| 4 | Residue | Various | Reclean |
| 5 | Haze | Area > 1mm² | Hold |

### Auto-Classification Rules
1. **Size-based:** Initial binning
2. **Shape-based:** Aspect ratio
3. **Intensity-based:** Scattering profile
4. **Location-based:** Edge vs. center
5. **Cluster-based:** Isolated vs. clustered

---

**문서 관리:**
- 작성자: 검사장비팀 박성준 수석
- 검토자: 품질관리팀 김혜진 책임
- 승인자: 장비기술부문 최인호 이사
- 차기 개정: 2025년 4월 (AI 분류기 업그레이드)