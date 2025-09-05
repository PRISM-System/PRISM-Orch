# Photoresist Track System 운영 매뉴얼
## Tokyo Electron CLEAN TRACK ACT 12

**문서번호:** EM-TEL-ACT12-001  
**개정일:** 2024.11.15  
**작성:** Track 공정기술팀  

---

## 1. 장비 개요

### 1.1 System Specifications
- **Model:** TEL CLEAN TRACK ACT 12
- **Configuration:** Dual track system (Track A/B)
- **Integration:** ASML NXT Scanner interface
- **Throughput:** 240 WPH (matched to scanner)
- **Process:** Coating, Baking, Development

### 1.2 Module Configuration
- **Coating Modules (COT):** 4 units
  - BARC coating: 2 units
  - Resist coating: 2 units
- **Development Modules (DEV):** 4 units
- **Hot Plates (HP):** 12 units
  - Soft bake: 4 units
  - PEB: 4 units
  - Hard bake: 4 units
- **Cool Plates (CP):** 8 units
- **Edge Exposure (WEE):** 2 units
- **Interface Block:** Scanner connection

### 1.3 Chemical Delivery System
- **Resist Bottles:** 4L capacity, auto-switching
- **Developer:** Inline mixing system
- **BARC:** Temperature controlled cabinet
- **Solvent:** Edge bead removal (EBR)
- **Supply Pressure:** 1.5-2.0 kg/cm²

### 1.4 Transport System
- **Robot Type:** SCARA with vacuum grip
- **Transfer Speed:** 800mm/sec maximum
- **Positioning Accuracy:** ± 0.1mm
- **Wafer Detection:** Mapping sensor

---

## 2. Installation Requirements

### 2.1 Facility Requirements

#### Environmental Conditions
- **Temperature:** 23.0°C ± 0.5°C
- **Humidity:** 45% ± 3%
- **Cleanroom:** ISO Class 4 (Class 10)
- **Airflow:** Downflow 0.45 m/s ± 0.05
- **Vibration:** VC-E specification

#### Utilities
| Utility | Specification | Consumption |
|---------|--------------|-------------|
| Power | 200V, 3φ, 150A | 80 kW |
| CDA | 5 kg/cm², -40°C DP | 500 L/min |
| Vacuum | -600 mmHg | 200 L/min |
| N2 | 99.999%, 3 kg/cm² | 2000 L/min |
| Exhaust | Solvent compatible | 50 m³/min |
| DIW | 18.2 MΩ, 23°C | 10 L/min |

### 2.2 Chemical Requirements

#### Photoresist Specifications
- **Viscosity:** 1.5-50 cP range capability
- **Temperature:** 23.0°C ± 0.1°C
- **Filtration:** 0.02µm point-of-use
- **Particle Count:** < 10 particles/mL @ 0.1µm
- **Shelf Life Monitoring:** Automatic

#### Developer
- **Concentration:** 2.38% TMAH ± 0.01%
- **Temperature:** 23.0°C ± 0.2°C
- **Conductivity Monitoring:** Inline
- **Normality Check:** Every 4 hours

### 2.3 Installation Space
- **Footprint:** 12m x 3m (including scanner interface)
- **Height:** 3.0m minimum
- **Service Access:** Front 1.5m, Rear 1.0m
- **Sub-fab Space:** Chemical cabinet area

---

## 3. Process Module Operations

### 3.1 Coating Module (COT)

#### Spin Coating Process
1. **Wafer Centering**
   - Vacuum chuck engagement
   - Centering pins alignment
   - Eccentricity: < 50µm

2. **Resist Dispense**
   - Static or dynamic dispense
   - Volume: 1.0-3.0 mL typical
   - Nozzle position: Center ± 2mm
   - Dispense rate: 1-10 mL/sec

3. **Spin Profile**
   ```
   Step 1: Spread
   - Speed: 500 rpm
   - Acceleration: 500 rpm/s
   - Time: 3 sec

   Step 2: Cast
   - Speed: 1500 rpm
   - Acceleration: 10000 rpm/s
   - Time: 1 sec

   Step 3: Spin-off
   - Speed: 2500-4000 rpm (thickness dependent)
   - Acceleration: 20000 rpm/s
   - Time: 30 sec

   Step 4: EBR
   - Speed: 1500 rpm
   - Solvent: PGMEA
   - Time: 5 sec
   ```

4. **Edge Bead Removal (EBR)**
   - **Chemical EBR:** 2-3mm from edge
   - **Back Rinse:** Prevent backside contamination
   - **Top Rinse:** Final edge cleaning

#### Coating Uniformity Optimization
- **Center Defect:** Adjust dispense volume/position
- **Edge Thick:** Modify EBR width/time
- **Radial Variation:** Tune spin speed/acceleration
- **Striation:** Check exhaust balance

**💡 Process Tip:** Maintain resist temperature at exactly 23.0°C for consistent viscosity

### 3.2 Development Module (DEV)

#### Development Process Sequence
1. **Pre-wet** (Optional)
   - DIW rinse: 2 seconds
   - Purpose: Improve wetting

2. **Develop Dispense**
   - Method: Scanning nozzle or puddle
   - Flow Rate: 1.5 L/min
   - Coverage: Complete wafer surface

3. **Development**
   ```
   Puddle Development:
   - Form puddle: 2 sec
   - Hold time: 45-60 sec
   - Gentle agitation: 100 rpm

   Spray Development:
   - Scan speed: 10 mm/sec
   - Spray pressure: 0.8 kg/cm²
   - Multiple passes: 3-5
   ```

4. **Rinse Process**
   - DIW rinse: 20 seconds
   - Flow pattern: Center to edge
   - Final spin dry: 2000 rpm, 20 sec

#### Critical Dimension (CD) Control
- **Development Time:** ± 0.5 sec precision
- **Temperature:** 23.0°C ± 0.2°C
- **Normality:** Real-time monitoring
- **Rinse Timing:** Critical for CD uniformity

### 3.3 Thermal Processing Modules

#### Hot Plate Specifications
- **Temperature Range:** 90-250°C
- **Uniformity:** ± 0.5°C @ 3mm above plate
- **Stability:** ± 0.2°C over time
- **Zones:** 5-zone independent control
- **Proximity Gap:** 0.1-0.5mm adjustable

#### Bake Process Types

**Soft Bake (Post Apply Bake)**
- **Purpose:** Solvent evaporation
- **Temperature:** 90-120°C typical
- **Time:** 60-90 seconds
- **Critical:** Affects photospeed

**Post Exposure Bake (PEB)**
- **Purpose:** Acid diffusion (chemically amplified resist)
- **Temperature:** 100-130°C typical
- **Time:** 60-90 seconds
- **Critical:** CD and profile control

**Hard Bake (Post Development Bake)**
- **Purpose:** Resist hardening
- **Temperature:** 110-150°C
- **Time:** 60-90 seconds
- **Note:** Optional for some processes

#### Cool Plate Operation
- **Temperature:** 23.0°C ± 0.3°C
- **Cooling Method:** Peltier with water circulation
- **Time:** 30-60 seconds
- **Purpose:** Temperature stabilization

---

## 4. Process Recipe Management

### 4.1 Recipe Structure

#### Recipe Components
```
Recipe Name: PRODUCT_LAYER_RES
├── Coating Parameters
│   ├── Resist Type: ArF-001
│   ├── Thickness Target: 900Å
│   ├── Spin Speed: 3200 rpm
│   └── EBR Width: 2.0mm
├── Bake Parameters
│   ├── Soft Bake: 110°C, 60s
│   ├── PEB: 115°C, 60s
│   └── Hard Bake: 130°C, 60s
├── Development Parameters
│   ├── Developer: NMD-3
│   ├── Time: 60s
│   └── Rinse: 20s
└── Transport Sequence
    └── Module routing priority
```

### 4.2 Process Flow Optimization

#### Standard Flow Sequence
1. **Input from Cassette/FOUP**
2. **HMDS Treatment** (optional)
3. **Cool Plate 1** (23°C stabilization)
4. **BARC Coating**
5. **BARC Bake** (200°C, 60s)
6. **Cool Plate 2**
7. **Resist Coating**
8. **Soft Bake** (110°C, 60s)
9. **Cool Plate 3**
10. **Edge Exposure**
11. **Transfer to Scanner**
12. **Return from Scanner**
13. **PEB** (115°C, 60s)
14. **Cool Plate 4**
15. **Development**
16. **Hard Bake** (optional)
17. **Output to Cassette/FOUP**

#### Parallel Processing
- **Multi-module Usage:** Load balancing
- **Dynamic Routing:** Based on availability
- **Buffer Management:** Minimize wait time
- **Throughput Matching:** Sync with scanner

### 4.3 Chemical Management

#### Resist Bottle Change
1. **Auto-switch Preparation**
   - New bottle installation
   - Bubble purge: 5 minutes
   - Temperature stabilization: 30 minutes

2. **Switchover Process**
   - Automatic at 100mL remaining
   - Dummy dispense: 5 wafers
   - Particle check required

#### Developer Management
- **Mixing Ratio:** Monitor conductivity
- **Temperature:** ± 0.1°C control
- **Circulation:** Continuous to prevent stratification
- **Filter Change:** Every 2000 wafers

---

## 5. Integration with Scanner

### 5.1 Interface Configuration

#### Physical Interface
- **Transfer Port:** Dual FIMS ports
- **Communication:** SECS/GEM protocol
- **Handshake:** Wafer ID verification
- **Buffer Capacity:** 4 wafers

#### Process Synchronization
- **Lot Start:** Track initiates
- **Wafer Flow:** Continuous feeding
- **PEB Timing:** Critical (< 30 min post-exposure)
- **Error Handling:** Auto rework capability

### 5.2 Inline Metrology

#### Thickness Measurement
- **Method:** Spectroscopic ellipsometry
- **Sampling:** 5-9 points per wafer
- **Specification:** Target ± 10Å
- **Feedback:** Auto recipe adjustment

#### CD Metrology Integration
- **Post-develop CD measurement**
- **Feedback to PEB temperature**
- **Feed-forward to etch process**
- **SPC chart generation**

---

## 6. Maintenance Procedures

### 6.1 Daily Maintenance

#### Start-up Procedure
1. **System Checks**
   - Chemical levels verification
   - Temperature stabilization confirm
   - Exhaust flow check
   - Robot initialization

2. **Dummy Run**
   - 5 dummy wafers process
   - Verify all modules operational
   - Check transport smooth

3. **Particle Check**
   - Bare wafer test
   - Accept: < 5 adds @ 0.12µm
   - Document in logbook

#### Shutdown Procedure
1. Complete all wafers in process
2. Chemical line N2 purge
3. Standby mode activation
4. Cover all chuck surfaces

### 6.2 Weekly Maintenance

#### Module Cleaning
**Coating Cup Cleaning:**
1. Remove cup assembly
2. Soak in solvent (NMP)
3. Ultrasonic cleaning
4. Rinse with IPA
5. Dry with N2
6. Reinstall and test

**Developer Nozzle Cleaning:**
1. Remove nozzle assembly
2. Flush with DIW
3. Soak in dilute TMAH
4. Rinse thoroughly
5. Check spray pattern

#### Calibration Checks
- Hot plate temperature mapping
- Spin motor speed verification
- Chemical temperature sensors
- Flow meter calibration

### 6.3 Monthly Maintenance

#### Comprehensive PM
1. **Mechanical Systems**
   - Robot belt tension
   - Bearing lubrication
   - Vacuum seal inspection
   - Leveling verification

2. **Chemical Delivery**
   - Filter replacement
   - Pump diaphragm check
   - Tubing inspection
   - Valve operation test

3. **Thermal Systems**
   - Heater resistance check
   - TC calibration
   - Zone uniformity mapping
   - Cooling system flush

4. **Exhaust System**
   - Duct cleaning
   - Damper adjustment
   - Flow balance verification
   - Scrubber efficiency check

### 6.4 Quarterly Maintenance

#### Major Service Items
1. **Complete Overhaul**
   - All bearings inspection
   - Motor brush replacement
   - Sensor calibration
   - Software backup

2. **Chemical System**
   - Complete line flush
   - Pump rebuild
   - Cabinet cleaning
   - Waste line inspection

3. **Performance Qualification**
   - Full capability study
   - Cp/Cpk verification
   - Correlation with metrology
   - Documentation update

---

## 7. Process Troubleshooting

### 7.1 Coating Defects

#### Problem: Thickness Non-uniformity > 3%
**Investigation:**
1. **Spin Speed Verification**
   - Tachometer measurement
   - Acceleration profile check
   - Motor current analysis

2. **Resist Condition**
   - Temperature: 23.0°C ± 0.1°C?
   - Viscosity change?
   - Age of resist?

3. **Exhaust Balance**
   - Cup exhaust flow
   - Chamber pressure
   - Turbulence check

**Solutions:**
- Adjust spin speed profile
- Replace resist if aged
- Balance exhaust system
- Clean coating cup

#### Problem: Coating Defects (Comets, Streaks)
**Root Causes:**
- Particles on wafer before coating
- Contaminated resist
- Nozzle contamination
- Bubble in resist line

**Corrective Actions:**
1. Filter replacement
2. Nozzle cleaning/replacement
3. Resist line purge
4. Dummy dispense cycles

### 7.2 Development Issues

#### Problem: CD Variation > 3nm
**Check Points:**
1. **Developer Condition**
   - Normality: 2.38% ± 0.01%
   - Temperature: 23.0°C ± 0.2°C
   - Age: < 1 week

2. **PEB Conditions**
   - Temperature uniformity
   - Time accuracy
   - Delay time from exposure

3. **Development Process**
   - Time control ± 0.5 sec
   - Puddle formation complete
   - Rinse timing optimal

**Optimization:**
- Adjust PEB temperature (0.5°C = ~1nm CD)
- Modify development time
- Check scanner focus/dose

#### Problem: Pattern Collapse
**Analysis:**
- Aspect ratio too high
- Insufficient adhesion
- Over-development
- Rinse shock

**Solutions:**
- Reduce development time
- Gentler rinse process
- HMDS prime enhancement
- Surface treatment optimization

### 7.3 Particle Issues

#### Problem: High Particle Count
**Systematic Investigation:**
1. **Source Identification**
   - Pre or post coating?
   - Specific module?
   - Chemical related?

2. **Common Causes**
   - EBR solvent splashing
   - Dried resist flaking
   - Robot gripper contamination
   - Filter breakthrough

3. **Corrective Actions**
   - Cup cleaning frequency increase
   - Filter replacement
   - Robot gripper cleaning
   - Chemical line flush

---

## 8. Advanced Process Control

### 8.1 Feed-Forward Control

#### Scanner to Track
- Dose actual vs. target
- Focus deviation map
- Field-by-field data
- Automatic PEB adjustment

#### Track to Scanner
- Thickness measurement
- Coating uniformity map
- Resist lot information
- Process capability data

### 8.2 Feedback Control

#### CD Control Loop
```
CD Measurement → PEB Temperature Adjustment
                ↓
            Database Update
                ↓
            Model Refinement
                ↓
            Next Lot Optimization
```

**Control Parameters:**
- PEB Temperature: ± 2°C range
- Development Time: ± 3 sec range
- Gain Factor: 0.3-0.5

### 8.3 Statistical Process Control

#### Monitor Charts
- Thickness by radius
- CD by position
- Defect density trend
- Chemical consumption

#### Control Limits
- ± 3σ for auto-hold
- ± 2σ for warning
- Western Electric rules
- Nelson rules implementation

---

## 9. Safety Systems

### 9.1 Chemical Safety

#### Hazardous Materials
| Chemical | Hazard | PPE Required |
|----------|--------|--------------|
| TMAH | Corrosive | Gloves, goggles |
| NMP | Reproductive toxin | Full PPE |
| PGMEA | Flammable | Fire resistant |
| Resist | Sensitizer | Avoid skin contact |

#### Spill Response
1. **Small Spill (< 100mL)**
   - Absorb with spill kit
   - Dispose as hazardous waste
   - Document incident

2. **Large Spill (> 100mL)**
   - Evacuate area
   - Call emergency response
   - Contain if safe
   - Full cleanup by trained personnel

### 9.2 Fire Safety

#### Fire Suppression
- **Type:** CO2 system
- **Activation:** Auto/Manual
- **Coverage:** All chemical areas
- **Response Time:** < 10 seconds

#### Flammable Storage
- **Solvent Cabinet:** Fire rated
- **Ventilation:** Continuous exhaust
- **Grounding:** All containers
- **Temperature:** Monitored

### 9.3 Ergonomic Safety

#### Manual Handling
- **FOUP Weight:** Max 8.5 kg
- **Lifting:** Use FOUP handles
- **Chemical Bottles:** Max 4L size
- **Posture:** Avoid repetitive strain

---

## 10. Performance Metrics

### 10.1 Process Capability

#### Key Metrics
| Parameter | Specification | Cpk Target | Current |
|-----------|--------------|------------|---------|
| Thickness | ± 10Å | > 2.0 | 2.3 |
| CD Uniformity | < 2nm | > 1.67 | 1.8 |
| Defect Density | < 0.05/cm² | > 2.0 | 2.1 |
| Throughput | 240 WPH | N/A | 238 |

### 10.2 Equipment Performance

#### Availability Metrics
- **MTBF:** > 500 hours
- **MTTR:** < 2 hours
- **Uptime:** > 95%
- **PM Compliance:** 100%

#### Consumption Metrics
| Item | Target | Actual |
|------|--------|--------|
| Resist | < 1.5 mL/wafer | 1.3 mL |
| Developer | < 50 mL/wafer | 45 mL |
| Solvents | < 10 mL/wafer | 8 mL |
| DIW | < 500 mL/wafer | 450 mL |

### 10.3 Cost Analysis

#### Operating Cost (per wafer)
- **Chemicals:** $2.50
- **Utilities:** $0.50  
- **Maintenance:** $1.00
- **Total:** $4.00/wafer

#### Cost Reduction Opportunities
1. Resist consumption optimization
2. Chemical recycle/reclaim
3. Preventive maintenance optimization
4. Throughput improvement

---

## Appendix A: Recipe Quick Reference

### Standard Resist Processes
| Resist Type | Thickness | Spin Speed | Soft Bake | PEB |
|-------------|-----------|------------|-----------|-----|
| ArF-001 | 900Å | 3200 rpm | 110°C/60s | 115°C/60s |
| ArF-002 | 1200Å | 2500 rpm | 105°C/60s | 110°C/60s |
| KrF-001 | 4000Å | 2000 rpm | 110°C/90s | 120°C/60s |
| i-line | 1.2µm | 3500 rpm | 95°C/60s | 110°C/60s |

### BARC Processes
| BARC Type | Thickness | Spin Speed | Bake |
|-----------|-----------|------------|------|
| Organic | 800Å | 1500 rpm | 200°C/60s |
| Si-BARC | 350Å | 2000 rpm | 220°C/90s |

---

## Appendix B: Alarm Codes

### Critical Alarms (Stop Process)
| Code | Description | Action |
|------|-------------|--------|
| E001 | Robot collision | Check teaching |
| E002 | Chemical empty | Replace bottle |
| E003 | Vacuum failure | Check vacuum line |
| E004 | Over temperature | Check hot plate |
| E005 | Communication lost | Check scanner link |

### Warning Alarms (Continue Process)
| Code | Description | Action |
|------|-------------|--------|
| W001 | Chemical low | Prepare replacement |
| W002 | Filter life warning | Schedule change |
| W003 | Calibration due | Schedule calibration |
| W004 | PM due | Schedule maintenance |

---

**문서 관리:**
- 작성자: Track 공정팀 최준영 수석
- 검토자: Photo 기술팀 김선미 책임
- 승인자: 제조기술부문 이동욱 이사
- 차기 개정: 2025년 3월 (EUV resist process 추가)