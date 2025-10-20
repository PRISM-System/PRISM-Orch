# Physical Vapor Deposition 장비 운영 매뉴얼
## Applied Materials Endura HP PVD Platform

**문서번호:** EM-AMAT-ENDURA-001  
**개정일:** 2024.11.15  
**작성:** PVD 공정기술팀  

---

## 1. 장비 개요

### 1.1 System Specifications
- **Model:** Applied Materials Endura HP PVD
- **Configuration:** 2 PVD chambers + 2 Degas chambers + Cool down
- **Process Capability:** Ti/TiN, Al, Cu, Ta/TaN, Co
- **Wafer Size:** 300mm
- **Throughput:** 35-45 WPH (depending on process)

### 1.2 Platform Architecture
- **Transfer Module:** Central vacuum transfer chamber
- **Load Locks:** Dual load locks with 25 wafer capacity each
- **Process Modules:** Up to 6 chambers configurable
- **Robot:** Dual blade vacuum robot
- **Controller:** Centura system controller

### 1.3 Chamber Types and Configuration

#### PVD Chamber Specifications
- **Source Type:** DC Magnetron Sputtering
- **Target Size:** 17 inch diameter
- **Power Supply:** 20kW DC (40kW for Cu)
- **Base Pressure:** < 1.0E-8 Torr
- **Process Pressure:** 1-10 mTorr

#### Degas Chamber
- **Temperature:** Up to 400°C
- **Purpose:** Moisture and outgassing removal
- **Heating:** Resistive heater in pedestal
- **Pump:** Turbo molecular pump

### 1.4 Magnetron System
- **Type:** Rotating magnet array
- **Rotation Speed:** 60-120 RPM
- **Magnetic Field:** 200-400 Gauss at target surface
- **Uniformity Control:** Multi-zone magnet positioning
- **Target Utilization:** > 35%

---

## 2. Installation Requirements

### 2.1 Facility Requirements

#### Power Specifications
- **Main Power:** 480V, 3-phase, 400A
- **Frequency:** 60Hz ± 0.5%
- **Power Distribution:**
  - DC power supplies: 200A
  - RF generators: 100A
  - Pumps and utilities: 100A

#### Cooling Water
- **Temperature:** 20°C ± 1°C
- **Flow Rate:** 150 GPM total
- **Pressure:** 60-80 PSI
- **Quality:** < 1 µS/cm conductivity

#### Process Gases
| Gas | Purity | Flow Range | Pressure |
|-----|---------|------------|----------|
| Ar | 99.9999% | 5-200 sccm | 80 PSI |
| N2 | 99.9999% | 5-100 sccm | 80 PSI |
| H2 | 99.9999% | 0-50 sccm | 60 PSI |
| O2 | 99.999% | 0-20 sccm | 60 PSI |

#### Exhaust System
- **Capacity:** 2000 CFM minimum
- **Foreline Pressure:** < 500 mTorr
- **Scrubber:** Not required for metal deposition

### 2.2 Cleanroom Requirements
- **Classification:** ISO Class 5 (Class 100)
- **Temperature:** 21°C ± 1°C
- **Humidity:** 45% ± 5%
- **Vibration:** VC-D criterion

### 2.3 Equipment Layout
- **Footprint:** 5m x 4m
- **Service Access:** 1.5m all sides
- **Height:** 3.5m minimum
- **Weight:** 8,000 kg

---

## 3. Process Parameters and Control

### 3.1 Deposition Parameters

#### DC Power Control
- **Power Range:** 0-20kW (0-40kW for Cu)
- **Voltage:** 300-600V typical
- **Current:** Up to 40A
- **Power Stability:** ± 0.5%
- **Arc Management:** Auto recovery < 10µs

**💡 Process Tip:** Higher power increases deposition rate but may cause target heating and particle generation

#### Pressure Control
- **Base Pressure Achievement:**
  1. Rough pump to 1 mTorr
  2. Turbo pump engagement
  3. Cryopump for final vacuum
  4. Base pressure < 1E-8 Torr

- **Process Pressure Control:**
  - Throttle valve position: Auto
  - Control range: 1-10 mTorr
  - Stability: ± 2%

#### Gas Flow Control
- **MFC Range:** 0-200 sccm
- **Accuracy:** ± 1% of setpoint
- **Response Time:** < 2 seconds
- **Gas Mixing:** Up to 3 gases simultaneously

### 3.2 Temperature Management

#### Substrate Temperature
- **Pedestal Heating:** -40°C to 500°C
- **Cooling:** Backside He gas cooling
- **Temperature Uniformity:** ± 5°C
- **Ramp Rate:** 10°C/sec maximum

#### Target Cooling
- **Method:** Water cooling through backing plate
- **Temperature:** Maintained < 400°C during deposition
- **Flow Rate:** 5 GPM per target
- **Critical:** Prevents target cracking

### 3.3 Film Property Control

#### Thickness Control
- **Method:** Time-based with rate calibration
- **Uniformity:** < 3% (1σ) across wafer
- **Repeatability:** < 1% run-to-run
- **Monitoring:** Crystal monitor for calibration

#### Film Stress Management
- **Pressure Effect:** Lower pressure → more compressive
- **Power Effect:** Higher power → more tensile
- **Temperature Effect:** Higher temperature → stress relief
- **Bias Application:** -50V to -200V for densification

#### Adhesion Enhancement
- **Pre-clean:** Ar sputter etch
  - RF Power: 200W
  - Time: 10-30 seconds
  - Pressure: 5 mTorr
- **Interface Engineering:** Ti or Ta adhesion layer

---

## 4. Process Recipes

### 4.1 Barrier/Seed Layer Deposition

#### Ti/TiN Barrier Layer
```
Step 1: Degas
- Temperature: 350°C
- Time: 60 seconds
- Pressure: < 1E-7 Torr

Step 2: Pre-clean
- RF Power: 150W
- Ar Flow: 50 sccm
- Time: 15 seconds
- Bias: -150V

Step 3: Ti Deposition
- DC Power: 12kW
- Ar Flow: 40 sccm
- Pressure: 2 mTorr
- Temperature: 250°C
- Thickness: 100Å

Step 4: TiN Deposition
- DC Power: 8kW
- Ar/N2: 40/60 sccm
- Pressure: 4 mTorr
- Temperature: 250°C
- Thickness: 200Å

Step 5: Cool Down
- Temperature: < 50°C
- N2 Purge: 100 sccm
```

### 4.2 Copper Seed Layer

#### Cu Seed for Damascene
```
Step 1: Degas
- Temperature: 250°C
- Time: 45 seconds

Step 2: Ta Barrier
- DC Power: 18kW
- Ar Flow: 85 sccm
- Pressure: 1.5 mTorr
- Thickness: 150Å

Step 3: TaN Barrier
- DC Power: 12kW
- Ar/N2: 85/15 sccm
- Pressure: 2.5 mTorr
- Thickness: 50Å

Step 4: Cu Seed
- DC Power: 30kW (SIP - Self Ionized Plasma)
- Ar Flow: 5 sccm (low flow for ionization)
- Pressure: 0.5 mTorr
- Temperature: -20°C (cooled)
- Thickness: 800Å
- Coverage: > 10% at 10:1 AR
```

### 4.3 Aluminum Metallization

#### Al-Cu Alloy for Backend
```
Step 1: Pre-clean
- RF Power: 200W
- Time: 20 seconds

Step 2: Ti Wetting Layer
- DC Power: 8kW
- Thickness: 50Å

Step 3: Al-0.5%Cu Deposition
- DC Power: 15kW
- Ar Flow: 30 sccm
- Pressure: 2 mTorr
- Temperature: 300°C
- Thickness: 5000Å

Step 4: TiN Cap Layer
- DC Power: 6kW
- Ar/N2: 20/80 sccm
- Thickness: 500Å
```

---

## 5. Maintenance Procedures

### 5.1 Daily Maintenance

#### System Health Check
1. **Base Pressure Verification**
   - Each chamber < 1E-8 Torr
   - Transfer module < 5E-7 Torr
   - Load locks < 1E-6 Torr

2. **Cooling System Check**
   - Target cooling flow: 5 ± 0.5 GPM
   - ESC cooling: Verified
   - Heat exchanger temperature: 20 ± 1°C

3. **Gas System Verification**
   - Supply pressure: Within spec
   - MFC zero check: All channels
   - Leak check if pressure drop > 1 PSI/hr

#### Particle Monitoring
- **Method:** Bare wafer test
- **Acceptance:** < 10 adds @ 0.12µm
- **Action if Fail:** Chamber seasoning or cleaning

### 5.2 Weekly Maintenance

#### Target Inspection
1. **Visual Inspection Through Viewport**
   - Erosion pattern uniformity
   - No flaking or nodule formation
   - Race track depth < 5mm

2. **Target Life Monitoring**
   - kWh consumed recorded
   - Thickness remaining estimated
   - Schedule replacement at 80% consumption

#### Shield Inspection and Cleaning
- **Deposition Shield:**
  - Thickness buildup < 2mm
  - No flaking observed
  - Clean or replace as needed

- **Collimator (if equipped):**
  - Aspect ratio maintained
  - No clogging of holes
  - Clean every 200 wafers

### 5.3 Monthly Maintenance

#### Comprehensive PM Schedule

1. **Chamber Opening and Cleaning**
   - Vent with N2
   - Remove and clean shields
   - Wipe chamber walls with IPA
   - Replace consumables per schedule

2. **O-Ring Replacement**
   - Chamber lid seal
   - Viewport seals
   - Gate valve seals
   - Apply vacuum grease sparingly

3. **Magnetron Service**
   - Motor operation check
   - Bearing inspection
   - Magnet strength verification
   - Balance check

4. **Pumping System Service**
   - Turbo pump vibration check
   - Cryopump regeneration
   - Foreline filter replacement
   - Pump oil level check

### 5.4 Quarterly Maintenance

#### Major Component Service

1. **Target Replacement Procedure**
   - Schedule: Every 300-500 kWh
   - Duration: 8 hours per chamber
   - Includes: Target bonding verification
   - Post-PM: 50 wafer seasoning

2. **Robot Calibration**
   - Teaching point verification
   - Belt tension check
   - Encoder calibration
   - Speed/acceleration optimization

3. **Electrical System Check**
   - DC power supply calibration
   - RF match network cleaning
   - Ground resistance < 1 ohm
   - EMO circuit test

---

## 6. Target Management

### 6.1 Target Specifications

| Material | Purity | Grain Size | Density | Bond |
|----------|---------|------------|---------|------|
| Ti | 99.995% | < 100µm | > 99.5% | In |
| Al | 99.999% | < 500µm | > 99.5% | In |
| Cu | 99.9999% | < 50µm | > 99.8% | In |
| Ta | 99.95% | < 200µm | > 99.5% | In |
| Co | 99.95% | < 100µm | > 99.5% | In |

### 6.2 Target Installation

#### Pre-Installation Checks
1. **Visual Inspection:**
   - No cracks or chips
   - Surface finish Ra < 1µm
   - Flatness < 0.1mm

2. **Bonding Verification:**
   - Ultrasonic scan > 95% bonded area
   - No voids > 5mm diameter
   - Edge seal intact

#### Installation Procedure
1. Clean backing plate with acetone/IPA
2. Apply thermal interface material
3. Mount target with proper torque (50 ft-lb)
4. Connect water cooling
5. Leak check < 1E-9 Torr·L/sec
6. Burn-in procedure (next section)

### 6.3 Target Burn-in and Conditioning

#### New Target Burn-in
```
Phase 1: Low Power (2 hours)
- Power: 1kW stepping to 5kW
- Pressure: 5 mTorr
- Ar Flow: 50 sccm
- Shutter: Closed

Phase 2: Medium Power (2 hours)
- Power: 5kW stepping to 10kW
- Increments: 1kW every 15 min

Phase 3: High Power (1 hour)
- Power: 10kW to max power
- Monitor: Voltage stability
- Check: No arcing

Phase 4: Process Qualification
- Run standard process
- Check uniformity < 3%
- Verify deposition rate
```

### 6.4 Target Life Management

#### Life Tracking Metrics
- **Power Consumption:** kWh counter
- **Thickness Monitoring:** Erosion depth
- **Performance Indicators:**
  - Voltage increase > 20%
  - Uniformity degradation > 5%
  - Particle generation increase

#### End-of-Life Criteria
- **Erosion Depth:** > 8mm at deepest point
- **Minimum Thickness:** < 3mm remaining
- **Catastrophic Failure:** Cracking or burn-through

---

## 7. Process Troubleshooting

### 7.1 Uniformity Issues

#### Problem: Thickness uniformity > 5%
**Diagnostic Approach:**

1. **Magnetron Check**
   - Rotation speed verification
   - Magnet position calibration
   - Motor current draw analysis

2. **Gas Distribution**
   - Flow rate verification each line
   - Gas injection ring inspection
   - Pressure gradient measurement

3. **Target Condition**
   - Erosion profile measurement
   - Race track symmetry check
   - Target age consideration

**Corrective Actions:**
- Adjust magnet spacing
- Optimize Ar flow and pressure
- Implement edge compensation
- Consider target replacement

### 7.2 Particle Issues

#### Problem: Particle adds > 20 @ 0.12µm
**Root Cause Investigation:**

1. **Arcing Detection**
   - Check arc counter history
   - Review voltage traces
   - Inspect target for nodules

2. **Flaking Sources**
   - Shield coating thickness
   - Chamber wall inspection  
   - Shutter mechanism check

3. **Process Conditions**
   - Pressure too high (> 5 mTorr)
   - Power ramping too fast
   - Temperature cycling stress

**Solutions:**
- Reduce power ramp rate
- Lower process pressure
- Increase shield cleaning frequency
- Implement soft-start procedure

### 7.3 Film Property Issues

#### Problem: High resistivity
**Investigation Path:**

1. **Contamination Check**
   - Base pressure degradation
   - Gas purity verification
   - Cross-contamination from previous process

2. **Process Parameters**
   - Power too low → poor crystallinity
   - N2 flow too high (for TiN)
   - Temperature too low

3. **Thickness Verification**
   - Actual vs. target thickness
   - Continuity of ultra-thin films

**Remediation:**
- Increase substrate temperature
- Optimize reactive gas ratio
- Increase deposition power
- Verify film thickness

### 7.4 Adhesion Failures

#### Problem: Film peeling or lifting
**Analysis Protocol:**

1. **Surface Preparation**
   - Pre-clean effectiveness
   - Native oxide removal
   - Surface contamination

2. **Interface Engineering**
   - Adhesion layer thickness
   - Interface mixing (ion bombardment)
   - Thermal mismatch stress

3. **Process Sequence**
   - Vacuum break between layers
   - Queue time violations
   - Temperature ramping rate

**Corrective Measures:**
- Increase pre-clean time/power
- Add or thicken adhesion layer
- Reduce thermal stress
- Minimize air exposure

---

## 8. Advanced Process Control

### 8.1 Run-to-Run Control

#### Controlled Variables
- **Deposition Time:** Adjusted per thickness feedback
- **Power Setpoint:** Compensated for target aging
- **Pressure:** Optimized for uniformity
- **Temperature:** Adjusted for stress control

#### Control Algorithm
```
Next_Setting = Previous_Setting + Gain × (Target - Measured)

Where:
- Gain = 0.3-0.7 (conservative to aggressive)
- Limits: ± 10% of nominal
```

### 8.2 Fault Detection and Classification (FDC)

#### Monitored Parameters
| Parameter | Sampling Rate | Limit |
|-----------|--------------|-------|
| DC Voltage | 10 Hz | ± 5% |
| Reflected Power | 10 Hz | < 50W |
| Pressure | 10 Hz | ± 10% |
| Temperature | 1 Hz | ± 5°C |

#### Fault Response Matrix
- **Warning Level:** Parameter drift 5-10%
  - Action: Alert engineer, continue process
  
- **Alarm Level:** Parameter drift > 10%
  - Action: Complete wafer, hold next lot

- **Abort Level:** Critical parameter failure
  - Action: Immediate process abort

### 8.3 Virtual Metrology

#### Model Inputs
- Power × Time (energy delivered)
- Pressure (affects mean free path)
- Temperature (crystallinity/stress)
- Target age (kWh consumed)

#### Prediction Accuracy
- **Thickness:** ± 2% of actual
- **Uniformity:** ± 1% prediction
- **Sheet Resistance:** ± 5% for metals

---

## 9. Safety and Compliance

### 9.1 Chemical Safety

#### Target Material Hazards
| Material | Hazard | PPE Required |
|----------|--------|--------------|
| Be | Toxic | Full suit, respirator |
| Cr | Carcinogenic | Gloves, mask |
| Ni | Allergenic | Gloves, safety glasses |
| In | Toxic | Standard PPE |

#### Handling Procedures
1. Used target disposal as hazardous waste
2. Vacuum cleaning only (no compressed air)
3. Wet wiping for particle control
4. Proper labeling and documentation

### 9.2 Electrical Safety

#### High Voltage Hazards
- **DC Power:** Up to 1000V present
- **RF Systems:** 13.56 MHz radiation
- **Lockout/Tagout:** Required for all service
- **Discharge Time:** Wait 5 minutes after power off

#### Safety Interlocks
- Chamber door → Disables HV
- EMO buttons → Complete shutdown
- Light curtains → Robot stop
- Gas detection → Auto isolation

### 9.3 Vacuum Safety

#### Implosion Risk
- Never strike viewports
- Use proper viewport covers
- Regular inspection for cracks
- Gradual venting procedure

#### Pump Safety
- Proper lifting for pump service
- Hot surface warnings
- Rotation hazard labels
- Foreline isolation during service

---

## 10. Performance Metrics and KPIs

### 10.1 Productivity Metrics

#### Overall Equipment Effectiveness (OEE)
```
OEE = Availability × Performance × Quality

Target: > 85%
Current Typical: 82-88%
```

Components:
- **Availability:** > 92% (Uptime)
- **Performance:** > 95% (Speed)
- **Quality:** > 98% (Yield)

### 10.2 Process Capability

#### Critical Parameters Cpk
| Parameter | Spec | Cpk Target | Current |
|-----------|------|------------|---------|
| Thickness | ± 5% | > 1.67 | 1.8 |
| Uniformity | < 3% | > 1.67 | 2.1 |
| Resistivity | ± 10% | > 1.33 | 1.5 |
| Stress | ± 100 MPa | > 1.33 | 1.4 |

### 10.3 Cost of Ownership (CoO)

#### Cost Breakdown (per wafer)
- **Consumables:** $8.50
  - Targets: $6.00
  - Shields: $1.50
  - Parts: $1.00
- **Utilities:** $2.50
- **Maintenance:** $3.00
- **Total:** $14.00/wafer

#### Cost Reduction Initiatives
1. Target utilization improvement (35% → 40%)
2. Shield cleaning vs. replacement
3. Preventive maintenance optimization
4. Process time reduction

---

## Appendix A: Quick Reference Tables

### Process Recipe Matrix
| Film | Power | Pressure | Ar Flow | Dep Rate |
|------|-------|----------|---------|----------|
| Ti | 12kW | 2 mT | 40 sccm | 1000 Å/min |
| TiN | 8kW | 4 mT | 40/60 | 300 Å/min |
| Al | 15kW | 2 mT | 30 sccm | 5000 Å/min |
| Cu | 30kW | 0.5 mT | 5 sccm | 2000 Å/min |
| Ta | 18kW | 1.5 mT | 85 sccm | 600 Å/min |

### Troubleshooting Quick Guide
| Symptom | Likely Cause | First Action |
|---------|--------------|--------------|
| High particles | Arcing | Check target |
| Poor uniformity | Magnetron | Check rotation |
| High resistivity | Contamination | Check base pressure |
| Peeling | Poor adhesion | Increase pre-clean |
| Slow rate | Target aging | Check power/voltage |

---

## Appendix B: Vendor Support

### Applied Materials Support
- **24/7 Hotline:** 1-800-882-0200
- **Local Office:** +82-31-000-0000
- **Online Support:** AGS Connect portal
- **Response Time:** 4 hours on-site

### Consumables Suppliers
| Item | Vendor | Lead Time |
|------|--------|-----------|
| Targets | Honeywell | 8-12 weeks |
| Shields | Local Machine Shop | 2 weeks |
| O-rings | Marco Rubber | 1 week |
| Spare Parts | AMAT | 2-8 weeks |

---

**문서 관리:**
- 작성자: PVD 공정팀 이승준 수석
- 검토자: 장비기술팀 박찬호 책임
- 승인자: 제조기술부문 김태영 이사
- 차기 개정: 2025년 2월 (새 Ta/TaN 프로세스 추가)