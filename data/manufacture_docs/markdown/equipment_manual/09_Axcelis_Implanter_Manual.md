# Ion Implantation 장비 운영 매뉴얼
## Axcelis Purion H High Current Ion Implanter

**문서번호:** EM-AXC-PURIONH-001  
**개정일:** 2024.11.15  
**작성:** Ion Implant 기술팀  

---

## 1. 장비 개요

### 1.1 System Specifications
- **Model:** Axcelis Purion H
- **Type:** High current implanter
- **Energy Range:** 0.2 - 80 keV
- **Beam Current:** Up to 45 mA
- **Dose Range:** 1E11 - 1E17 ions/cm²
- **Wafer Size:** 300mm
- **Throughput:** 500 WPH (1E15, 40keV)

### 1.2 Ion Source
- **Type:** Bernas source (hot cathode)
- **Arc Chamber:** Tungsten
- **Gases:** BF3, AsH3, PH3, GeF4, etc.
- **Lifetime:** 100-200 hours typical
- **Beam Extraction:** 0.2-80 kV

### 1.3 Beamline Components
- **Mass Analyzer:** 90° analyzing magnet
- **Resolution:** M/ΔM > 80
- **Acceleration:** Post-acceleration available
- **Scanner:** Electrostatic X-Y scan
- **Beam Current Monitor:** Faraday cups

### 1.4 End Station
- **Wafer Handling:** Vacuum robot
- **Orientation:** 0-60° tilt, 360° rotation
- **Cooling:** Backside gas cooling
- **Charge Control:** Electron flood gun
- **Throughput:** Batch or single wafer

---

## 2. Installation Requirements

### 2.1 Facility Requirements

#### Environmental Specifications
- **Temperature:** 21°C ± 1°C
- **Humidity:** 45% ± 5%
- **Cleanroom:** ISO Class 5
- **Vibration:** Standard floor
- **Magnetic Field:** < 5 Gauss AC

#### Power Requirements
- **Main Power:** 480V, 3-phase, 400A
- **High Voltage:** Up to 200kV internal
- **Frequency:** 60Hz ± 1%
- **Grounding:** < 1 ohm
- **Emergency Off:** Multiple locations

#### Vacuum System
- **Base Pressure:** < 1E-7 Torr
- **Pumps:** Turbo + cryo pumps
- **Foreline:** Dry pumps
- **N2 Purge:** 99.999%
- **Vent Time:** 5 minutes

### 2.2 Gas Supply System

#### Source Gases
| Gas | Purity | Pressure | Hazard |
|-----|---------|----------|--------|
| BF3 | 99.9% | 30 PSI | Toxic |
| AsH3/H2 | 15% | 30 PSI | Toxic |
| PH3/H2 | 15% | 30 PSI | Toxic |
| GeF4 | 99.9% | 30 PSI | Corrosive |
| SiF4 | 99.9% | 30 PSI | Corrosive |

#### Safety Systems
- **Gas Cabinet:** Negative pressure
- **Detection:** ppb level monitors
- **Auto-shutdown:** On leak detection
- **Scrubber:** Wet type
- **Emergency:** N2 purge

### 2.3 Installation Space
- **Footprint:** 8m x 5m
- **Service Access:** 2m all sides
- **Height:** 3.5m minimum
- **Weight:** 15,000 kg
- **Shielding:** Lead walls if needed

---

## 3. Implant Process Control

### 3.1 Beam Setup

#### Source Tuning
```
Optimization Sequence:
1. Gas Flow Setting
   - BF3: 0.5-2.0 sccm
   - Optimal: Maximum beam current
   
2. Arc Current/Voltage
   - Current: 0.5-3.0 A
   - Voltage: 50-150 V
   - Target: Stable plasma
   
3. Extraction Voltage
   - Range: Match implant energy
   - Focus: Optimize transmission
   
4. Source Magnet
   - Field: 100-500 Gauss
   - Purpose: Plasma confinement
```

#### Mass Analysis
```
Mass Resolution Check:
- Target mass: e.g., 11B+
- Adjacent mass rejection: > 100:1
- Peak width: < 1 AMU
- Stability: < 0.1 AMU drift
```

#### Beam Tuning
1. **Extraction Optimization**
   - Maximize current
   - Minimize divergence
   - Stabilize plasma

2. **Transmission Tuning**
   - Lens voltages
   - Steering adjustments
   - Aperture alignment

3. **Scan Calibration**
   - Uniformity mapping
   - Scan amplitude
   - Frequency optimization

### 3.2 Dose and Energy Control

#### Dose Calculation
```
Dose (ions/cm²) = (I × t) / (q × A × e)

Where:
- I: Beam current (A)
- t: Implant time (s)
- q: Charge state
- A: Implant area (cm²)
- e: Elementary charge

Example:
- 10 mA beam
- 20 seconds
- Single charge
- 300mm wafer
→ Dose = 1.77E15 ions/cm²
```

#### Energy Settings
| Application | Ion | Energy | Dose |
|-------------|-----|--------|------|
| Source/Drain | As+ | 30 keV | 3E15 |
| Halo | B+ | 8 keV | 8E13 |
| Well | P+ | 200 keV | 1E13 |
| Threshold | BF2+ | 35 keV | 2E12 |

#### Angle Control
- **Tilt:** 0-60° from normal
- **Rotation:** 0-360°
- **Quad Mode:** 0°, 90°, 180°, 270°
- **Purpose:** Channeling control

### 3.3 Uniformity Control

#### Scan System
```
2D Scanning:
- X-scan: Electrostatic, 500 Hz
- Y-scan: Mechanical, 1-10 Hz
- Pattern: Raster scan
- Overlap: > 50%
```

#### Uniformity Optimization
1. **Scan Calibration**
   - Bare wafer implant
   - Thermawave mapping
   - Adjust scan parameters

2. **Beam Shape**
   - Gaussian profile typical
   - Width measurement
   - Symmetry check

3. **Dose Compensation**
   - Edge enhancement
   - Center adjustment
   - Pattern-dependent correction

---

## 4. Process Recipes

### 4.1 Standard Implants

#### NMOS Source/Drain
```
Recipe: NSD_As_3E15
- Species: As+
- Energy: 40 keV
- Dose: 3E15 ions/cm²
- Tilt: 0°
- Rotation: 0°
- Temperature: 25°C
- Beam Current: 20 mA
- Time: ~9 seconds
```

#### PMOS Source/Drain Extension
```
Recipe: PSDE_B_8E14
- Species: B+
- Energy: 2 keV
- Dose: 8E14 ions/cm²
- Tilt: 0°
- Rotation: Quad (4x22.5°)
- Temperature: -50°C (cooled)
- Beam Current: 2 mA
```

#### Deep Well
```
Recipe: NWELL_P_180keV
- Species: P+
- Energy: 180 keV
- Dose: 2E13 ions/cm²
- Tilt: 7°
- Rotation: 22°
- Chain Energy: 60keV x3
- Screen Oxide: 100Å
```

### 4.2 Advanced Techniques

#### Damage Engineering
```
Pre-amorphization (PAI):
- Species: Ge+ or Si+
- Energy: 30 keV
- Dose: 5E14 ions/cm²
- Purpose: Reduce channeling
- Benefit: Shallow junction
```

#### Co-implantation
```
Carbon Co-implant:
- With: Boron implant
- Purpose: Reduce TED
- Energy: Matched to B
- Dose: 0.5-1x B dose
- Sequence: C first, then B
```

#### Plasma Doping (PLAD)
```
BF3 Plasma:
- Energy: 0.2-2 keV
- Dose: 1E15-1E16
- Advantage: Ultra-shallow
- Challenge: Uniformity
```

---

## 5. Maintenance Procedures

### 5.1 Daily Maintenance

#### Pre-Production Checks
1. **Vacuum Status**
   - Source: < 5E-7 Torr
   - Beamline: < 1E-7 Torr
   - End station: < 5E-7 Torr

2. **Beam Setup Verify**
   - Reference beam check
   - Transmission: > 80%
   - Stability: < 2% variation

3. **Safety Systems**
   - Radiation monitor
   - Gas detection
   - Interlock test

#### Production Monitoring
- Beam current stability
- Dose controller accuracy
- Uniformity tracking
- Particle monitoring

### 5.2 Weekly Maintenance

#### Source Maintenance
1. **Source Inspection**
   - Arc chamber condition
   - Insulator cleanliness
   - Extraction gap check

2. **Gas System**
   - Leak check
   - Flow verification
   - Bottle pressure

3. **Beam Quality**
   - Mass spectrum scan
   - Emittance measurement
   - Contamination check

### 5.3 Monthly Maintenance

#### Comprehensive PM
1. **Source Service**
   - Arc chamber cleaning
   - Filament inspection
   - Insulator replacement

2. **Beamline Service**
   - Faraday cup calibration
   - Aperture cleaning
   - Lens alignment

3. **End Station**
   - Wafer handler teaching
   - Platen inspection
   - Cooling system check

### 5.4 Periodic Maintenance

#### Quarterly Service
1. **Source Rebuild**
   - Complete disassembly
   - Parts replacement
   - Reassembly and test
   - Lifetime: 500-1000 hours

2. **System Calibration**
   - Energy calibration
   - Dose calibration
   - Angle calibration
   - Mass calibration

3. **Safety Certification**
   - Radiation survey
   - Interlock test
   - Gas system check
   - Documentation

---

## 6. Contamination Control

### 6.1 Cross-Contamination

#### Species Segregation
| Category | Species | Cleaning |
|----------|---------|----------|
| Group I | B, BF2 | Standard |
| Group II | P, As | Standard |
| Group III | Sb, In | Deep clean |
| Group IV | Metals | Dedicated |

#### Cleaning Protocols
```
Species Change Procedure:
1. Run cleaning beam (Ar+)
2. Time: 30 minutes
3. Verify with SIMS
4. Release for production
```

### 6.2 Metallic Contamination

#### Sources and Prevention
- **Source Materials:** High purity
- **Beam Path:** Regular cleaning
- **Wafer Handling:** Clean gloves
- **Monitoring:** TXRF analysis

#### Detection Methods
- **SIMS:** Depth profiling
- **TXRF:** Surface metals
- **Lifetime:** Minority carrier
- **Electrical:** Junction leakage

### 6.3 Particle Control

#### Generation Sources
1. **Source Flaking**
   - Deposits on walls
   - Regular cleaning needed

2. **Beam Strike**
   - Aperture sputtering
   - Proper alignment critical

3. **Wafer Handling**
   - Robot cleanliness
   - Static charge control

#### Reduction Strategies
- Optimized source conditions
- Regular PM schedule
- Proper beam tuning
- Charge neutralization

---

## 7. Process Monitoring

### 7.1 Dose Monitoring

#### Thermawave Measurement
- **Principle:** Sheet resistance change
- **Sampling:** 49 points
- **Calculation:** Dose from Rs
- **Accuracy:** ± 2%

#### SIMS Verification
- **Frequency:** Weekly
- **Depth Profile:** Full
- **Peak Concentration:** Check
- **Integrated Dose:** Verify

### 7.2 Uniformity Monitoring

#### Mapping Techniques
```
Uniformity (%) = (σ/mean) × 100

Target: < 1% for critical implants

Measurement:
- 49-point Rs map
- Edge exclusion: 3mm
- Statistical analysis
```

### 7.3 Contamination Monitoring

#### Regular Checks
| Test | Frequency | Limit |
|------|-----------|-------|
| Particles | Per lot | < 5 adds |
| Metals | Weekly | < 1E10 /cm² |
| Lifetime | Daily | > 100 µs |
| SIMS | Monthly | Profile check |

---

## 8. Troubleshooting

### 8.1 Beam Current Issues

#### Problem: Low Beam Current
**Diagnosis:**
1. **Source Condition**
   - Filament worn?
   - Arc chamber dirty?
   - Gas flow adequate?

2. **Extraction System**
   - Voltage correct?
   - Gap spacing?
   - Alignment OK?

3. **Transmission**
   - Lens voltages?
   - Beam centered?
   - Apertures clear?

**Solutions:**
- Replace filament
- Clean source
- Optimize extraction
- Retune beam line

### 8.2 Dose Uniformity Issues

#### Problem: Non-uniformity > 2%
**Investigation:**
1. **Scan System**
   - Calibration current?
   - Waveform distortion?
   - Mechanical issues?

2. **Beam Shape**
   - Symmetrical?
   - Proper focus?
   - Stable position?

**Corrective Actions:**
- Recalibrate scan
- Adjust beam optics
- Check parallelism
- Verify setup beam

### 8.3 Contamination Issues

#### Problem: Metal Contamination
**Root Cause:**
1. **Source Materials**
   - Gas purity?
   - Source parts?

2. **Sputtering**
   - Beam strike?
   - Component wear?

3. **Handling**
   - Clean protocols?
   - Cross-contamination?

**Resolution:**
- Change gas supply
- Replace worn parts
- Review procedures
- Deep cleaning cycle

---

## 9. Advanced Applications

### 9.1 Precision Doping

#### Ultra-Shallow Junctions
```
Requirements:
- Junction depth: < 10nm
- Abruptness: < 2nm/decade
- Activation: > 50%

Techniques:
- Low energy implant
- Molecular ions (BF2, B18H22)
- Cooled substrate
- Spike anneal
```

### 9.2 3D Device Implants

#### FinFET Doping
```
Conformal Doping:
- Tilt: 30-45°
- Rotation: 8 angles
- Energy: Multiple
- Dose matching critical
```

#### Vertical Devices
- High tilt angles
- Aspect ratio challenges
- Shadowing effects
- Process optimization needed

### 9.3 Material Modification

#### Strain Engineering
```
Ge Implant for Strain:
- Into S/D regions
- Dose: 1E15-1E16
- Creates tensile strain
- Mobility enhancement
```

#### Smart Cut Process
```
H2 Implant for Layer Transfer:
- Energy: 30-100 keV
- Dose: 5E16
- Splitting temperature: 400-600°C
- Application: SOI wafers
```

---

## 10. Performance Metrics

### 10.1 Process Capability

#### Key Parameters
| Metric | Specification | Cpk |
|--------|--------------|-----|
| Dose | ± 2% | > 2.0 |
| Uniformity | < 1% | > 1.67 |
| Energy | ± 0.5% | > 2.0 |
| Angle | ± 0.5° | > 1.67 |

### 10.2 Productivity

#### Throughput Analysis
```
Mechanical Time:
- Load/unload: 6 sec
- Pump/vent: 10 sec
- Move/align: 4 sec
Total: 20 sec

Implant Time:
- Depends on dose/current
- Example: 1E15 @ 20mA = 9 sec

Total: ~30 sec/wafer = 120 WPH
```

### 10.3 Cost of Ownership

#### Operating Costs
```
Per Wafer Costs:
- Source gas: $0.50
- Parts: $2.00
- Energy: $0.30
- Maintenance: $1.20
Total: $4.00/wafer

Annual Costs:
- Gas: $100k
- Parts: $400k
- Service: $200k
- Total: $700k
```

---

## Appendix A: Implant Tables

### Common Recipes
| Application | Species | Energy | Dose | Angle |
|-------------|---------|--------|------|-------|
| NLDD | As | 5 keV | 3E14 | 0° |
| PLDD | BF2 | 3 keV | 2E14 | 0° |
| NSD | As | 40 keV | 3E15 | 0° |
| PSD | B | 3 keV | 2E15 | 0° |
| N-Well | P | 380 keV | 2E13 | 7° |
| P-Well | B | 160 keV | 3E13 | 7° |

### Range Data (Silicon)
| Ion | Energy | Rp | ΔRp |
|-----|--------|-----|-----|
| B | 1 keV | 34Å | 21Å |
| B | 10 keV | 325Å | 114Å |
| P | 50 keV | 625Å | 245Å |
| As | 40 keV | 268Å | 89Å |

---

## Appendix B: Safety Information

### Emergency Response
| Situation | Action |
|-----------|--------|
| Gas leak | Evacuate, call emergency |
| Radiation alarm | Leave area immediately |
| Power failure | Safe shutdown initiated |
| Fire | CO2 extinguisher, evacuate |

### PPE Requirements
- Safety glasses
- Cleanroom suit
- Chemical gloves for source work
- Radiation badge
- Safety shoes

---

**문서 관리:**
- 작성자: Implant 공정팀 신동욱 수석
- 검토자: 공정통합팀 류현진 책임
- 승인자: 제조기술부문 오승환 이사
- 차기 개정: 2025년 5월 (Plasma doping 추가)