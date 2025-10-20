# Epitaxy 장비 운영 매뉴얼
## ASM Epsilon 2000 Plus Epitaxial Reactor

**문서번호:** EM-ASM-EPI2000-001  
**개정일:** 2024.11.15  
**작성:** Epitaxy 공정기술팀  

---

## 1. 장비 개요

### 1.1 System Specifications
- **Model:** ASM Epsilon 2000 Plus
- **Process:** Silicon Epitaxy (Si, SiGe, SiC)
- **Wafer Size:** 200mm (upgradeable to 300mm)
- **Capacity:** Single wafer processing
- **Temperature Range:** 550°C - 1200°C
- **Growth Rate:** 0.1 - 10 µm/min

### 1.2 Reactor Configuration
- **Chamber Type:** Cold-wall, horizontal
- **Heating:** Lamp heated susceptor
- **Lamps:** Tungsten halogen, 36 lamps
- **Susceptor:** SiC coated graphite
- **Pyrometer:** Dual wavelength, emissivity corrected
- **Process Pressure:** 10 - 760 Torr

### 1.3 Gas Delivery System
- **Si Sources:** SiH4, SiH2Cl2, SiHCl3
- **Dopants:** B2H6, PH3, AsH3
- **Ge Source:** GeH4
- **Carrier Gas:** H2 (Pd purified)
- **Etchants:** HCl, Cl2
- **MFC Range:** 0.1 sccm - 50 slm

### 1.4 Safety Systems
- **Gas Detection:** H2, toxic, pyrophoric
- **Emergency Shutdown:** Multiple triggers
- **Burn Box:** H2 combustion
- **Scrubber:** Wet scrubbing system
- **N2 Purge:** Automatic on fault

---

## 2. Installation Requirements

### 2.1 Facility Requirements

#### Environmental Control
- **Temperature:** 21°C ± 2°C
- **Humidity:** 40-60% RH
- **Cleanroom:** ISO Class 5
- **Exhaust:** 2000 CFM minimum
- **Vibration:** Standard floor

#### Power Requirements
- **Main Power:** 480V, 3-phase, 200A
- **Lamp Power:** 150kW maximum
- **Frequency:** 60Hz ± 1%
- **UPS:** Control system only
- **Emergency Off:** Multiple locations

#### Process Gases
| Gas | Purity | Pressure | Flow Range |
|-----|---------|----------|------------|
| H2 | 99.99999% | 100 PSI | 100 slm |
| SiH4 | 99.9999% | 50 PSI | 500 sccm |
| HCl | 99.999% | 30 PSI | 5 slm |
| GeH4 | 99.999% | 30 PSI | 50 sccm |
| B2H6/H2 | 100 ppm | 30 PSI | 100 sccm |
| PH3/H2 | 100 ppm | 30 PSI | 100 sccm |

### 2.2 Support Systems

#### Cooling Water
- **Temperature:** 20°C ± 2°C
- **Flow Rate:** 30 GPM
- **Pressure:** 60-80 PSI
- **Quality:** < 1µS/cm

#### Scrubber System
- **Type:** Wet scrubber
- **Capacity:** Match exhaust flow
- **Efficiency:** > 99% for SiH4
- **Monitoring:** pH, ORP

### 2.3 Installation Space
- **Footprint:** 3m x 2.5m
- **Service Access:** 1.5m rear
- **Height:** 3m minimum
- **Weight:** 2,500 kg
- **Sub-fab:** Gas cabinet space

---

## 3. Epitaxial Growth Processes

### 3.1 Silicon Epitaxy

#### Process Sequence
```
1. Load and Pump
   - Load wafer
   - Pump to base pressure
   - N2 purge cycles

2. H2 Bake
   - Ramp to 1150°C
   - H2 flow: 40 slm
   - Time: 60 seconds
   - Pressure: 40 Torr
   - Purpose: Native oxide removal

3. HCl Etch (Optional)
   - Temperature: 1100°C
   - HCl: 500 sccm
   - H2: 40 slm
   - Time: 30 seconds
   - Etch depth: 200Å

4. Epitaxial Growth
   - Temperature: 1050°C
   - SiH2Cl2: 500 sccm
   - H2: 40 slm
   - Pressure: 40 Torr
   - Growth rate: 2 µm/min
   - Thickness: 5 µm

5. Cool Down
   - Ramp down: 50°C/min
   - H2 flow maintained
   - Below 600°C: N2 purge
```

#### Growth Rate Control
```
Growth Rate = k × P(SiH2Cl2) × exp(-Ea/RT)

Where:
- k: Rate constant
- P: Partial pressure
- Ea: Activation energy
- R: Gas constant
- T: Temperature

Typical rates:
- 900°C: 0.5 µm/min
- 1000°C: 1.5 µm/min
- 1100°C: 3.0 µm/min
```

### 3.2 SiGe Epitaxy

#### Selective SiGe for Source/Drain
```
Process Parameters:
- Temperature: 650-750°C
- Si source: SiH4 or Si2H6
- Ge source: GeH4
- HCl: For selectivity
- Pressure: 10-50 Torr

Typical Recipe:
- SiH4: 50 sccm
- GeH4: 30 sccm (for 30% Ge)
- HCl: 200 sccm
- H2: 20 slm
- Temperature: 700°C
- Pressure: 20 Torr
- Growth rate: 20 nm/min
- Selectivity: > 1000:1
```

#### Ge Content Control
- **Linear Relationship:** GeH4/(SiH4+GeH4)
- **Range:** 0-50% Ge achievable
- **Uniformity:** < 2% variation
- **Stability:** Monitored by pyrometry

### 3.3 In-situ Doping

#### Boron Doping (p-type)
```
Doping Level Control:
- B2H6 flow: 1-100 sccm
- Concentration: 1E15 - 1E20 /cm³
- Uniformity: < 3% across wafer

Incorporation:
C(B) = K × [B2H6]/[Si-source] × f(T)
```

#### Phosphorus Doping (n-type)
```
Process Considerations:
- PH3 flow: 1-50 sccm
- Concentration: 1E15 - 1E19 /cm³
- Auto-doping prevention
- Memory effect management
```

#### Arsenic Doping
```
Special Requirements:
- AsH3 handling precautions
- Lower incorporation efficiency
- Surface segregation control
- Growth rate impact
```

---

## 4. Process Control

### 4.1 Temperature Control

#### Pyrometry System
- **Type:** Dual wavelength
- **Range:** 500-1300°C
- **Accuracy:** ± 2°C
- **Response:** < 1 second
- **Emissivity:** Auto-corrected

#### Temperature Calibration
1. **Thermocouple Wafer**
   - Direct measurement
   - 9-point mapping
   - Quarterly calibration

2. **Melting Point Standards**
   - Al: 660°C
   - Au-Si: 363°C
   - Verification points

3. **Uniformity Mapping**
   - < 2°C variation target
   - Zone adjustment
   - Lamp balance optimization

### 4.2 Thickness Monitoring

#### In-situ Monitoring
- **Pyrometry Interference:** For transparent films
- **Range:** 0.1-10 µm
- **Real-time:** Growth rate feedback
- **Accuracy:** ± 2%

#### Ex-situ Measurement
- **Ellipsometry:** Standard method
- **FTIR:** For thick films
- **Profilometry:** Step height
- **Cross-section SEM:** Verification

### 4.3 Film Quality Control

#### Defect Density
- **Specification:** < 0.1 defects/cm²
- **Size:** > 0.12 µm
- **Inspection:** KLA tool
- **Frequency:** Every run

#### Resistivity Control
```
Target Uniformity:
- Within wafer: < 3%
- Run-to-run: < 2%
- Measurement: 4-point probe
- Mapping: 49 points
```

---

## 5. Maintenance Procedures

### 5.1 Daily Maintenance

#### Pre-run Checklist
1. **Gas Supply Check**
   - Cylinder pressures
   - MFC zero check
   - Leak check display

2. **Cooling System**
   - Water flow/temperature
   - Lamp cooling verification

3. **Safety Systems**
   - Gas monitor status
   - EMO verification
   - Exhaust flow check

#### Post-run Procedures
1. Susceptor inspection
2. Viewport cleaning
3. Process log update
4. Particle count record

### 5.2 Weekly Maintenance

#### Chamber Cleaning
```
Cleaning Recipe:
1. Heat to 1150°C
2. Flow HCl: 2 slm
3. H2: 40 slm
4. Time: 15 minutes
5. Purpose: Remove Si deposits
```

#### System Checks
- Lamp intensity verification
- Pyrometer window cleaning
- Gas line purge
- MFC calibration check

### 5.3 Monthly Maintenance

#### Comprehensive PM
1. **Chamber Opening**
   - Full vent procedure
   - Susceptor removal
   - Chamber wall cleaning
   - Quartz parts inspection

2. **Lamp Module Service**
   - Individual lamp check
   - Reflector cleaning
   - Power balance test
   - Replace weak lamps

3. **Gas System**
   - Filter replacement
   - Valve operation check
   - Mass flow calibration
   - Leak detection

### 5.4 Quarterly Maintenance

#### Major Service Items
1. **Susceptor Replacement**
   - SiC coating inspection
   - Flatness verification
   - New susceptor conditioning

2. **Pump Service**
   - Oil change
   - Seal inspection
   - Pumping speed test

3. **Pyrometer Calibration**
   - Full range calibration
   - Optical path cleaning
   - Electronics check

---

## 6. Safety Protocols

### 6.1 Gas Safety

#### Toxic Gas Handling
| Gas | TLV | IDLH | Response |
|-----|-----|------|----------|
| AsH3 | 0.05 ppm | 3 ppm | Evacuate |
| PH3 | 0.3 ppm | 50 ppm | Evacuate |
| B2H6 | 0.1 ppm | 15 ppm | Evacuate |
| GeH4 | 0.2 ppm | Unknown | Evacuate |

#### Pyrophoric Gas Procedures
1. **SiH4 Handling**
   - Always purge lines
   - No air exposure
   - Controlled burn-off
   - Double containment

2. **Emergency Response**
   - Auto shutdown
   - N2 purge activation
   - Evacuation if needed
   - Fire suppression ready

### 6.2 High Temperature Safety

#### Burn Hazards
- **Hot Surfaces:** Marked clearly
- **Susceptor:** 1200°C maximum
- **Cool-down:** 2 hours minimum
- **PPE:** Heat resistant gloves

#### Lamp Module Safety
- **UV Exposure:** Eye protection
- **High Voltage:** 480V present
- **Replacement:** Cool lamps only
- **Disposal:** Mercury content

### 6.3 Emergency Procedures

#### Power Failure
1. Auto-shutdown sequence
2. N2 purge activation
3. Lamp power off
4. Process gases isolated
5. Manual vent if needed

#### Gas Leak
1. Alarm activation
2. Auto gas shutdown
3. Area evacuation
4. Emergency response team
5. Leak identification/repair

---

## 7. Process Troubleshooting

### 7.1 Growth Rate Issues

#### Problem: Low Growth Rate
**Investigation:**
1. **Temperature Verification**
   - Pyrometer reading
   - TC wafer check
   - Lamp power output

2. **Gas Flow Check**
   - MFC actual vs. setpoint
   - Supply pressure adequate
   - Line restrictions

3. **Chemistry Issues**
   - Gas purity verification
   - Moisture contamination
   - Decomposition efficiency

**Solutions:**
- Recalibrate pyrometer
- Replace process gases
- Increase temperature
- Check susceptor condition

### 7.2 Uniformity Problems

#### Problem: Thickness Non-uniformity > 3%
**Root Causes:**
1. **Temperature Gradient**
   - Lamp balance off
   - Susceptor warped
   - Pyrometer drift

2. **Gas Flow Issues**
   - Asymmetric flow pattern
   - Injector clogging
   - Pressure variations

**Corrective Actions:**
- Lamp zone adjustment
- Susceptor replacement
- Flow pattern optimization
- Chamber cleaning

### 7.3 Defect Issues

#### Problem: High Particle Count
**Analysis:**
1. **Source Identification**
   - Pre-epi particles?
   - Gas phase nucleation?
   - Chamber flaking?

2. **Process Conditions**
   - Temperature too low
   - Growth rate too high
   - HCl etch insufficient

**Resolution:**
- Optimize H2 bake
- Reduce growth rate
- Increase HCl etch time
- Chamber clean frequency

### 7.4 Doping Control

#### Problem: Resistivity Out of Spec
**Troubleshooting:**
1. **Dopant Flow**
   - MFC calibration
   - Gas concentration verify
   - Memory effect check

2. **Incorporation Efficiency**
   - Temperature dependence
   - Growth rate effect
   - Surface segregation

**Optimization:**
- Recalibrate MFCs
- Adjust temperature
- Modify growth rate
- Dopant gas change

---

## 8. Advanced Processes

### 8.1 Selective Epitaxy

#### Process Development
```
Selectivity Requirements:
- No poly on oxide/nitride
- Pattern loading effect < 5%
- Faceting control

Key Parameters:
- Temperature: 650-850°C
- HCl/SiH4 ratio: > 3
- Pressure: Low (10-40 Torr)
- Growth rate: Reduced
```

#### Applications
- Raised source/drain
- Embedded SiGe stressor
- SiC source/drain
- Selective Si capping

### 8.2 Graded Layers

#### SiGe Grading
```
Profile Types:
1. Linear Grade
   - Ge: 0 → 30% over 100nm
   - Stress management
   
2. Step Grade
   - Discrete Ge steps
   - Interface control
   
3. Box Profile
   - Constant Ge content
   - Sharp interfaces
```

#### Implementation
- Recipe stepping
- Flow ramping
- Real-time control
- Profile verification

### 8.3 Multi-layer Stacks

#### Superlattice Structures
```
Si/SiGe Stack:
- Layer 1: Si, 10nm
- Layer 2: Si0.7Ge0.3, 20nm
- Repeat: 10 cycles
- Interface: < 1nm transition
- Application: Strain engineering
```

---

## 9. Process Qualification

### 9.1 Film Characterization

#### Required Measurements
| Parameter | Method | Specification |
|-----------|--------|---------------|
| Thickness | Ellipsometry | Target ± 2% |
| Resistivity | 4-point probe | Target ± 5% |
| Ge content | XRD | Target ± 1% |
| Defects | Light scattering | < 0.1/cm² |
| Stress | Wafer bow | < 100 MPa |

### 9.2 Electrical Testing

#### Device Parameters
- **Contact Resistance:** < 1E-8 Ω·cm²
- **Junction Leakage:** < 1 nA/cm²
- **Mobility:** Meet target
- **Breakdown:** > Design voltage

### 9.3 Reliability Testing

#### Stress Tests
1. **Thermal Cycling**
   - Range: -40 to 125°C
   - Cycles: 1000
   - Check: Adhesion, stress

2. **Current Stress**
   - Current density: 1E6 A/cm²
   - Duration: 168 hours
   - Monitor: Resistance change

---

## 10. Performance Metrics

### 10.1 Process Capability

#### Key Metrics
| Parameter | Cpk Target | Current |
|-----------|------------|---------|
| Thickness | > 2.0 | 2.3 |
| Uniformity | > 1.67 | 1.9 |
| Resistivity | > 1.67 | 1.8 |
| Particles | > 2.0 | 2.2 |

### 10.2 Equipment Performance

#### Availability and Utilization
- **MTBF:** > 200 hours
- **MTTR:** < 4 hours
- **Availability:** > 90%
- **PM Compliance:** 100%

### 10.3 Cost Analysis

#### Operating Cost per Wafer
```
Consumables:
- Gases: $15.00
- Susceptor: $5.00
- Parts: $3.00

Utilities: $4.00
Maintenance: $5.00

Total: $32.00/wafer
```

---

## Appendix A: Standard Recipes

### Blanket Si Epitaxy
```
Thickness: 5µm
Temperature: 1050°C
SiH2Cl2: 500 sccm
H2: 40 slm
Pressure: 40 Torr
Time: 2.5 minutes
```

### Selective SiGe
```
Thickness: 50nm
Temperature: 700°C
SiH4: 50 sccm
GeH4: 30 sccm
HCl: 200 sccm
H2: 20 slm
Pressure: 20 Torr
```

### Heavily Doped Si
```
Dopant: Boron
Level: 1E20 /cm³
B2H6: 100 sccm
SiH4: 200 sccm
Temperature: 850°C
```

---

## Appendix B: Troubleshooting Guide

### Quick Reference
| Problem | Check | Solution |
|---------|-------|----------|
| Low rate | Temperature, MFC | Increase T, calibrate |
| Poor uniformity | Lamp balance | Adjust zones |
| High defects | Pre-clean, temp | Optimize bake |
| Wrong resistivity | Dopant flow | Calibrate MFC |
| No selectivity | HCl ratio, temp | Increase HCl |

---

**문서 관리:**
- 작성자: Epi 공정팀 윤성호 수석
- 검토자: 공정개발팀 백승현 책임
- 승인자: 기술개발부문 황정민 이사
- 차기 개정: 2025년 4월 (SiC epitaxy 추가)