# Photolithography Scanner 장비 운영 매뉴얼
## ASML TWINSCAN NXT:2050i - ArF Immersion

**문서번호:** EM-ASML-NXT2050-001  
**개정일:** 2024.11.15  
**작성:** Lithography 기술팀  

---

## 1. 장비 개요

### 1.1 System Specifications
- **Model:** ASML TWINSCAN NXT:2050i
- **Light Source:** ArF Excimer Laser (193nm)
- **Technology:** Immersion Lithography
- **Overlay:** ≤ 2.0nm
- **Throughput:** 275 WPH (96 fields @ 26x33mm)
- **CD Uniformity:** < 1.5nm (3σ)

### 1.2 Optical System Configuration
- **Numerical Aperture (NA):** 1.35
- **Reduction Ratio:** 4:1
- **Field Size:** 26mm x 33mm
- **Illumination Modes:** Conventional, Annular, Dipole, Quadrupole, FlexRay
- **Dose Uniformity:** < 0.5%

### 1.3 Stage System
- **Wafer Stage:** Dual stage with measurement and exposure positions
- **Reticle Stage:** 6 DOF with nm-level positioning
- **Stage Accuracy:** ± 1nm positioning, ± 1 nrad leveling
- **Acceleration:** Up to 5 g

### 1.4 Immersion System
- **Immersion Fluid:** Ultra-pure water (UPW)
- **Refractive Index:** 1.44 @ 193nm
- **Flow Rate:** 1.0 L/min
- **Temperature Control:** 22.0°C ± 0.01°C
- **Dissolved Oxygen:** < 1 ppb

### 1.5 Metrology Systems
- **Alignment System:** SMASH (Smart Alignment Sensor Hybrid)
- **Level Sensor:** Air gauge with nm resolution
- **Dose Sensor:** In-situ energy monitor
- **Contamination Control:** Reticle and lens particle detection

---

## 2. Installation Requirements

### 2.1 Facility Requirements

#### Environmental Specifications
- **Temperature:** 22°C ± 0.1°C
- **Humidity:** 45% ± 2%
- **Pressure:** Positive 20 Pa
- **Vibration:** VC-E criterion (< 3 μm/s @ 1-100 Hz)

#### Power Requirements
- **Main Power:** 480V, 3-phase, 300A
- **UPS Backup:** 30 minutes minimum
- **Power Quality:** THD < 3%
- **Grounding:** < 1 ohm resistance

#### Utilities
| Utility | Specification | Consumption |
|---------|--------------|-------------|
| Dry CDA | 6 bar, -70°C dew point | 500 L/min |
| Vacuum | -80 kPa | 100 L/min |
| N2 | 99.999%, 5 bar | 1000 L/min |
| Cooling Water | 20°C ± 0.5°C | 100 L/min |
| Exhaust | Chemical compatible | 1000 m³/hr |

### 2.2 Cleanroom Requirements
- **Classification:** ISO Class 3 (Class 1)
- **Airflow:** Laminar, 0.45 m/s ± 0.05
- **Particle Count:** < 1 particle/ft³ @ 0.1μm
- **AMC Control:** 
  - NH3 < 1 ppb
  - Amines < 1 ppb
  - SO2 < 1 ppb

### 2.3 Installation Footprint
- **Tool Footprint:** 8m x 4m
- **Service Area:** 2m all sides
- **Height Requirement:** 4m minimum
- **Floor Loading:** 2000 kg/m²
- **Access:** Double door, 3m width

---

## 3. 운전 조건 설정

### 3.1 Illumination Settings

#### Source Settings
- **Laser Power:** 40-90W adjustable
- **Pulse Rate:** 6000 Hz
- **Bandwidth:** < 0.3 pm FWHM
- **Pulse Energy Stability:** < 0.3% (3σ)

#### Illumination Modes Configuration
**Conventional:**
- σ = 0.4-0.95
- Best for isolated features

**Annular:**
- σ outer = 0.85
- σ inner = 0.55
- Improved DOF for dense features

**Dipole (X/Y):**
- Opening angle: 30-45°
- σ radius: 0.2
- For 1D patterns (lines/spaces)

**Quadrupole:**
- Opening angle: 30°
- σ radius: 0.2
- For contact holes

**💡 Optimization Tip:** Use source-mask optimization (SMO) for critical layers

### 3.2 Dose Control

#### Dose Calculation
```
Base Dose = Energy / (Pulse Rate × Slit Width × Scan Speed)
```

- **Typical Range:** 20-40 mJ/cm²
- **Dose Mapper:** ± 0.5% correction capability
- **Inter-field Correction:** Available for edge die
- **Intra-field Correction:** 65 zones per field

### 3.3 Focus Control

#### Focus Offset Settings
- **Global Offset:** ± 500nm range
- **Field Curvature:** 3rd order correction
- **Astigmatism:** X/Y independent control
- **Focus Drilling:** Multiple exposure with focus shift

#### Leveling Parameters
- **Tilt Correction:** ± 200 μrad
- **Dynamic Leveling:** Real-time during scan
- **Edge Exclusion:** 2-5mm configurable

### 3.4 Overlay Control

#### Alignment Strategy
- **Mark Type:** ATHENA marks preferred
- **Sampling:** 8-24 marks per wafer
- **Model:** Higher order (up to 3rd)
- **Grid Matching:** Inter/intra field correction

#### Advanced Overlay Correction (AOC)
- **CPE (Correctables Per Exposure):** 10 parameters
- **Thermal Model:** Wafer heating compensation
- **Lens Heating:** Predictive correction
- **Stage Grid:** Regular calibration

---

## 4. Process Recipe Management

### 4.1 Recipe Structure

#### Job Definition
```
JOB: Product_Layer_Version
├── Reticle ID: MASK12345
├── Illumination: Dipole-Y
├── NA/Sigma: 1.35/0.3
├── Dose: 28 mJ/cm²
├── Focus Offset: +20nm
├── Overlay Model: 3rd Order
└── Alignment Recipe: ALN_ATHENA_8PT
```

### 4.2 Reticle Management

#### Reticle Qualification
1. **Pellicle Inspection:** No particles > 1μm
2. **CD Measurement:** ± 2nm from design
3. **Registration:** < 5nm across reticle
4. **Phase (PSM):** 180° ± 2°
5. **Transmission:** ± 0.5% uniformity

#### Reticle Library System
- **Capacity:** 12 reticles in-tool
- **RFID Tracking:** Automatic identification
- **Usage Counter:** Exposure count tracking
- **Cleaning Schedule:** Every 50k exposures

### 4.3 Wafer Flow Sequence

#### Standard Process Flow
1. **Pre-alignment** (5 sec)
   - Notch finding
   - Rough positioning

2. **Loading to Chuck** (3 sec)
   - Vacuum application
   - Flatness check

3. **Global Alignment** (15 sec)
   - Mark detection
   - Model calculation
   - Grid determination

4. **Exposure Sequence** (40 sec)
   - Field-by-field scanning
   - Real-time focus/dose control
   - Immersion fluid management

5. **Unloading** (3 sec)
   - Vacuum release
   - Water removal
   - Transfer to track

### 4.4 Advanced Process Control (APC)

#### Feedback Loops
- **CD Control:** From CD-SEM data
- **Overlay:** From overlay metrology
- **Focus:** From process window monitoring
- **Dose:** From resist thickness measurement

#### Feed-forward Corrections
- **Incoming Overlay:** From previous layer
- **Wafer Shape:** From geometry measurement
- **Reticle Errors:** From reticle qualification

---

## 5. 정기 점검 및 유지보수

### 5.1 Daily Maintenance

#### Optical System Check
- **Laser Power:** Monitor and log
- **Bandwidth:** < 0.35 pm action limit
- **Lens Transmission:** > 95%
- **Contamination:** Check particle counter

#### Immersion System
- **Water Quality:**
  - Resistivity: > 18.2 MΩ·cm
  - TOC: < 1 ppb
  - Particles: < 10 counts/mL @ 50nm
  - Bacteria: < 1 CFU/100mL

#### Stage Performance
- **Repeatability Test:** < 5nm (3σ)
- **Settling Time:** < 20ms
- **Following Error:** < 2nm

### 5.2 Weekly Maintenance

#### Calibrations
**Baseline Establishment:**
1. Lens Aberration Measurement
2. Illumination Pupil Check
3. Stage Grid Calibration
4. Alignment Sensor Verification

#### System Cleaning
- **Reticle Stage:** IPA wipe
- **Wafer Stage:** DI water rinse
- **Sensors:** Lens paper with acetone
- **Frame:** Anti-static cloth

### 5.3 Monthly Maintenance

#### Comprehensive System Check
1. **Optics:**
   - Lens element inspection
   - Mirror alignment verification
   - Pellicle frame inspection

2. **Mechanics:**
   - Stage bearing lubrication
   - Cable carrier inspection
   - Pneumatic system check

3. **Metrology:**
   - Interferometer calibration
   - Encoder scale cleaning
   - Sensor linearization

### 5.4 Quarterly Maintenance

#### Major Preventive Maintenance
**Duration:** 24-48 hours

**Tasks:**
1. Complete optical alignment
2. Stage base frame leveling
3. Immersion hood replacement
4. Major component replacement per schedule
5. Full system qualification

#### Component Life Tracking
| Component | Life Expectancy | Current Usage |
|-----------|----------------|---------------|
| Laser Tube | 30 billion pulses | 18 billion |
| Projection Lens | 5 years | 3.2 years |
| Immersion Hood | 1 million wafers | 620k wafers |
| Stage Motor | 10 million km | 6.5 million km |

---

## 6. Advanced Imaging Optimization

### 6.1 Resolution Enhancement Techniques (RET)

#### Optical Proximity Correction (OPC)
- **Model Based:** Full chip simulation
- **Rule Based:** For non-critical layers
- **Iteration:** 3-5 cycles typical
- **Verification:** Process window check

#### Sub-Resolution Assist Features (SRAF)
- **Placement Rules:** 
  - Distance from main: 150-200nm
  - Width: 40-60nm (sub-resolution)
- **Purpose:** Improve pattern fidelity

#### Source Mask Optimization (SMO)
- **Computation:** 24-48 hours for full chip
- **Benefit:** 20-30% process window improvement
- **Application:** Critical layers only

### 6.2 Process Window Optimization

#### Focus-Exposure Matrix (FEM)
**Standard Conditions:**
- Focus: ± 100nm, 20nm steps
- Dose: ± 10%, 2% steps
- Metrics: CD, Sidewall angle, Resist loss

#### Process Window Determination
```
Overlapping Process Window:
- CD Tolerance: ± 10% of target
- Sidewall Angle: > 85°
- Resist Loss: < 10%
- DOF: > 200nm
- EL (Exposure Latitude): > 10%
```

### 6.3 Immersion Specific Optimization

#### Defectivity Control
- **Watermark Prevention:**
  - Post-exposure rinse: 5 sec
  - Spin dry: 3000 rpm
  - N2 blow: 10 L/min

- **Bubble Elimination:**
  - Degas water to < 1 ppm DO
  - Meniscus speed optimization
  - Contact angle > 70°

#### Top Coat Process
- **Purpose:** Prevent leaching
- **Thickness:** 90nm ± 5nm
- **Removal:** Developer soluble
- **Impact:** -2% throughput

---

## 7. Troubleshooting Guide

### 7.1 Overlay Issues

#### Problem: Overlay > 3nm
**Diagnostic Flow:**
1. **Check Alignment Marks**
   - Signal strength > 0.7
   - Symmetry > 0.8
   - No damage/contamination

2. **Verify Model**
   - Residuals < 10nm
   - No systematic patterns
   - Sufficient sampling

3. **Stage Grid Check**
   - Run grid calibration
   - Check environmental conditions
   - Verify stage following error

4. **Lens Heating**
   - Check dose history
   - Apply thermal model
   - Consider dose scheduling

### 7.2 CD Variation

#### Problem: CD Range > 3nm across wafer
**Root Cause Analysis:**
1. **Dose Uniformity**
   - Scan uniformity test
   - Slit uniformity check
   - Dose mapper calibration

2. **Focus Variation**
   - Leveling sensor check
   - Wafer flatness measurement
   - Chuck vacuum verification

3. **Resist Process**
   - PEB plate uniformity
   - Developer uniformity
   - Resist thickness variation

### 7.3 Defectivity Issues

#### Problem: Defect Count > 20/wafer
**Investigation Steps:**
1. **Defect Classification**
   - Particles: Check immersion water
   - Watermarks: Verify drying process
   - Micro-bridges: Review OPC/SRAF

2. **Source Identification**
   - Reticle inspection
   - Environmental monitoring
   - Process chemicals check

3. **Corrective Actions**
   - Reticle cleaning
   - Water system flush
   - Hood replacement if needed

---

## 8. Performance Monitoring

### 8.1 Key Performance Indicators (KPI)

#### Productivity Metrics
- **Availability:** > 95%
- **Utilization:** > 85%
- **Yield:** > 99.5%
- **OEE:** > 80%

#### Technical Metrics
- **Overlay Mean + 3σ:** < 2.5nm
- **CD Uniformity:** < 1.5nm
- **Focus Uniformity:** < 30nm
- **Defect Density:** < 0.01/cm²

### 8.2 Statistical Process Control (SPC)

#### Control Charts
**Daily Monitoring:**
- Overlay X/Y by field position
- CD by radius
- Focus offset trend
- Dose trend

**Control Limits:**
- UCL/LCL: ± 3σ from mean
- Warning Limits: ± 2σ
- Run Rules: Western Electric rules

### 8.3 Predictive Maintenance

#### Condition Monitoring
- **Vibration Analysis:** Stage bearings
- **Thermal Imaging:** Electronic modules
- **Particle Trending:** Gradual increase detection
- **Performance Degradation:** Throughput analysis

#### Maintenance Scheduling
- **Algorithm:** Weibull distribution
- **Confidence Level:** 95%
- **Cost Optimization:** Minimize CoO
- **Part Ordering:** JIT with safety stock

---

## 9. Safety Systems

### 9.1 Laser Safety
- **Classification:** Class 4 laser product
- **Interlocks:** Multiple door sensors
- **Beam Path:** Fully enclosed
- **Emergency Stop:** < 100ms response
- **PPE Required:** Laser safety glasses (OD > 7 @ 193nm)

### 9.2 Chemical Safety
- **Immersion Water:** No hazard
- **Purge Gases:** Asphyxiation hazard
- **Cleaning Solvents:** Proper ventilation required
- **MSDS Location:** Tool computer and lab

### 9.3 Ergonomic Safety
- **Reticle Weight:** Max 1.5 kg
- **Lifting Aids:** For heavy components
- **Service Position:** Platforms provided
- **Repetitive Motion:** Rotation of tasks

### 9.4 Emergency Procedures
1. **Chemical Spill:** Use spill kit, evacuate if large
2. **Gas Leak:** Evacuate, call facility
3. **Fire:** CO2 extinguisher, evacuate
4. **Injury:** First aid, call medical

---

## 10. System Qualification

### 10.1 Installation Qualification (IQ)
- **Mechanical:** Leveling, utilities connection
- **Electrical:** Power quality, grounding
- **Environmental:** Temperature, humidity, vibration
- **Safety:** Interlock verification

### 10.2 Operational Qualification (OQ)
- **Baseline Performance:** All specifications met
- **Repeatability:** 20 wafer marathon test
- **Stability:** 24-hour continuous run
- **Cross-Check:** With reference tool

### 10.3 Process Qualification (PQ)
- **Product Wafers:** 3 lots minimum
- **Yield Criteria:** > 99%
- **Overlay Matching:** < 1nm offset to reference
- **CD Matching:** < 1nm offset

### 10.4 Periodic Requalification
- **Frequency:** After major PM or upgrade
- **Scope:** Abbreviated OQ/PQ
- **Duration:** 4-8 hours
- **Sign-off:** Process owner required

---

## Appendix A: Common Recipes

### 7nm Logic Gate Layer
- **Illumination:** Dipole-Y, 30° opening
- **NA/σ:** 1.35/0.25
- **Dose:** 32 mJ/cm²
- **Focus Offset:** +15nm
- **OPC:** Model-based with SRAF
- **Target CD:** 28nm
- **Pitch:** 54nm

### 5nm Metal Layer
- **Illumination:** SMO optimized
- **NA/σ:** 1.35/custom
- **Dose:** 35 mJ/cm²
- **Multiple Patterning:** SADP
- **Overlay Requirement:** < 2nm

### Contact Layer
- **Illumination:** Quadrupole
- **NA/σ:** 1.35/0.2
- **Dose:** 38 mJ/cm²
- **Focus Drilling:** 3 exposures
- **Assist Features:** Aggressive SRAF

---

## Appendix B: Vendor Contacts

### ASML Support
- **24/7 Hotline:** +31-40-268-4444
- **Local Office:** +82-31-000-0000
- **Remote Support:** e-Diagnostics enabled
- **Response Time:** 2 hours for critical

### Critical Suppliers
| Component | Vendor | Contact | Lead Time |
|-----------|---------|---------|-----------|
| Laser Tube | Cymer | +1-858-000-0000 | 12 weeks |
| Immersion Hood | ASML | Direct | 8 weeks |
| Encoders | Heidenhain | +49-8669-000 | 6 weeks |
| Optics | Zeiss | +49-7364-000 | 20 weeks |

---

**문서 관리:**
- 작성자: Photo 기술팀 정현수 수석
- 검토자: 공정통합팀 김미래 책임  
- 승인자: 기술본부 박정호 상무
- 차기 개정: 2025년 5월 (NXT:2100i 도입 시)