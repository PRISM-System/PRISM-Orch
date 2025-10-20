# Rapid Thermal Processing 장비 운영 매뉴얼
## Varian VIISta RTP System

**문서번호:** EM-VAR-VIISTA-001  
**개정일:** 2024.11.15  
**작성:** RTP 공정기술팀  

---

## 1. 장비 개요

### 1.1 System Specifications
- **Model:** Varian VIISta RTP
- **Process Type:** Rapid Thermal Processing
- **Temperature Range:** 200°C - 1200°C
- **Ramp Rate:** Up to 250°C/sec
- **Uniformity:** < ± 2°C at 1000°C
- **Wafer Size:** 300mm
- **Throughput:** 60 WPH

### 1.2 Heating System
- **Heat Source:** Tungsten halogen lamps
- **Configuration:** Top and bottom arrays
- **Lamp Count:** 168 lamps total
- **Power:** 300 kW maximum
- **Zone Control:** 15 independent zones
- **Response Time:** < 1 second

### 1.3 Temperature Measurement
- **Pyrometers:** 5 channels
- **Range:** 300°C - 1400°C
- **Wavelength:** 950nm, 1550nm
- **Sampling Rate:** 100 Hz
- **Accuracy:** ± 1°C
- **Emissivity Compensation:** Automatic

### 1.4 Process Chamber
- **Material:** Quartz chamber
- **Atmosphere:** N2, O2, NH3, H2/N2
- **Pressure:** Atmospheric
- **Gas Flow:** Laminar design
- **Wafer Support:** SiC pins
- **Edge Ring:** SiC coated

---

## 2. Installation Requirements

### 2.1 Facility Requirements

#### Environmental Conditions
- **Temperature:** 21°C ± 1°C
- **Humidity:** 45% ± 5%
- **Cleanroom:** ISO Class 5
- **Vibration:** Standard floor
- **Exhaust:** 1000 CFM

#### Power Requirements
- **Main Power:** 480V, 3-phase, 400A
- **Lamp Power:** 300 kW peak
- **Control Power:** 208V, 30A
- **Frequency:** 60Hz ± 1%
- **Power Quality:** < 3% THD

#### Process Gases
| Gas | Purity | Flow Range | Pressure |
|-----|---------|------------|----------|
| N2 | 99.999% | 100 slm | 60 PSI |
| O2 | 99.999% | 20 slm | 60 PSI |
| NH3 | 99.999% | 5 slm | 30 PSI |
| H2/N2 | 5% H2 | 10 slm | 30 PSI |
| Ar | 99.999% | 50 slm | 60 PSI |

### 2.2 Utilities

#### Cooling System
- **Type:** Closed-loop chiller
- **Temperature:** 20°C ± 1°C
- **Flow Rate:** 40 GPM
- **Pressure:** 60 PSI
- **Heat Load:** 300 kW

#### Exhaust Requirements
- **Flow Rate:** 1000 CFM minimum
- **Temperature Rating:** 200°C
- **Material:** Stainless steel
- **Scrubber:** Required for NH3

### 2.3 Installation Layout
- **Footprint:** 3m x 2.5m
- **Service Access:** 1m rear
- **Height:** 3m minimum
- **Weight:** 2,000 kg
- **Clearance:** Front load

---

## 3. Process Applications

### 3.1 Spike Anneal

#### Ultra-Shallow Junction Activation
```
Process Parameters:
- Peak Temperature: 1050°C
- Ramp Up: 250°C/sec
- Dwell Time: 0 seconds (spike)
- Ramp Down: 80°C/sec
- Ambient: N2
- Flow: 20 slm

Results:
- Junction Depth: < 20nm
- Rs: 500 Ω/□
- Activation: > 40%
- Diffusion: Minimal
```

#### Process Sequence
1. **Load and Purge**
   - Load wafer
   - N2 purge: 30 seconds
   - Stabilize at 400°C

2. **Spike Anneal**
   - Ramp to peak: 3-4 seconds
   - Peak temperature: < 1 second
   - Cool down: 10 seconds

3. **Unload**
   - Cool to 400°C
   - Transfer out

### 3.2 Millisecond Anneal

#### Advanced Junction Formation
```
Flash/Laser Assist Mode:
- Pre-heat: 600°C
- Flash Peak: 1300°C
- Duration: 1-10 ms
- Cool Rate: 1000°C/sec

Applications:
- Sub-10nm junctions
- Minimal diffusion
- High activation
- Low leakage
```

### 3.3 Silicidation

#### Nickel Silicide Formation
```
Two-Step Process:

Step 1 - Formation:
- Temperature: 270°C
- Time: 30 seconds
- Ambient: N2
- Purpose: Ni2Si formation

Step 2 - Conversion:
- Temperature: 450°C
- Time: 30 seconds
- Ambient: N2
- Purpose: NiSi formation
- Sheet Resistance: 4-5 Ω/□
```

#### Titanium Silicide
```
RTA Process:
- First RTA: 650°C, 30s, N2
- Selective etch
- Second RTA: 850°C, 30s, N2
- Phase: C54 TiSi2
- Rs: 2-3 Ω/□
```

### 3.4 Oxidation/Nitridation

#### Rapid Thermal Oxidation (RTO)
```
Gate Oxide Growth:
- Temperature: 1000°C
- Time: 60 seconds
- O2 Flow: 10 slm
- Thickness: 20-30Å
- Uniformity: < 2%
```

#### Rapid Thermal Nitridation (RTN)
```
Oxynitride Formation:
- Base oxide: 15Å
- Temperature: 900°C
- NH3 Flow: 5 slm
- Time: 30 seconds
- N incorporation: 2-3%
```

---

## 4. Temperature Control

### 4.1 Pyrometry System

#### Multi-Zone Control
```
Zone Configuration:
- Center: Zones 1-5
- Middle: Zones 6-10
- Edge: Zones 11-15

Control Algorithm:
- PID control per zone
- Cross-talk compensation
- Predictive control
- Real-time adjustment
```

#### Emissivity Compensation
| Material | Emissivity | Temperature |
|----------|------------|-------------|
| Bare Si | 0.65-0.70 | 600-1000°C |
| Oxide | 0.40-0.45 | 600-1000°C |
| Nitride | 0.50-0.55 | 600-1000°C |
| Poly-Si | 0.35-0.40 | 600-1000°C |

### 4.2 Temperature Calibration

#### TC Wafer Calibration
1. **Setup**
   - Instrumented TC wafer
   - 5-9 thermocouples
   - Direct measurement

2. **Calibration Process**
   - Multiple temperature points
   - Pyrometer adjustment
   - Zone balance optimization
   - Store calibration file

3. **Verification**
   - Uniformity mapping
   - Repeatability check
   - Document results

### 4.3 Uniformity Optimization

#### Zone Tuning Procedure
```
Iterative Optimization:
1. Run baseline uniformity
2. Measure temperature map
3. Adjust zone powers:
   - Hot spots: Reduce power
   - Cool spots: Increase power
4. Repeat until < 2°C range
5. Save recipe settings
```

---

## 5. Process Monitoring

### 5.1 Temperature Monitoring

#### Real-time Display
- **Pyrometer Traces:** All channels
- **Set Point vs. Actual:** Deviation plot
- **Zone Powers:** Individual display
- **Ramp Rates:** Calculated real-time
- **Peak Temperature:** Logged

#### Data Logging
```
Parameters Logged:
- Time stamp
- All temperatures
- Zone powers
- Gas flows
- Pressure
- Process events

Storage:
- Local: 30 days
- Server: Permanent
- Format: CSV/Binary
```

### 5.2 Process Control

#### Run-to-Run Control
```
Feedback Parameters:
- Sheet resistance
- Film thickness
- Temperature adjust

Algorithm:
ΔT = k × (Target_Rs - Actual_Rs)
Where k = sensitivity coefficient

Limits:
- Max adjustment: ± 10°C
- Rate of change: 2°C/run
```

#### Statistical Process Control
| Parameter | USL | LSL | Cpk Target |
|-----------|-----|-----|------------|
| Peak Temp | +3°C | -3°C | > 1.67 |
| Rs | +5% | -5% | > 1.33 |
| Uniformity | 3% | 0% | > 1.67 |

### 5.3 Fault Detection

#### Alarm Conditions
- **Temperature Deviation:** > 5°C
- **Ramp Rate Error:** > 10%
- **Zone Imbalance:** > 20%
- **Lamp Failure:** Any lamp
- **Pyrometer Fault:** Signal loss

#### Response Actions
1. **Warning Level**
   - Log event
   - Continue process
   - Alert engineer

2. **Alarm Level**
   - Complete current wafer
   - Hold next lot
   - Require inspection

3. **Abort Level**
   - Immediate stop
   - Safety shutdown
   - Evacuation if needed

---

## 6. Maintenance Procedures

### 6.1 Daily Maintenance

#### Start-up Checks
1. **Lamp Inspection**
   - Visual through viewport
   - All lamps lit?
   - Uniform brightness?

2. **Pyrometer Check**
   - Signal strength OK?
   - Window clean?
   - Calibration valid?

3. **Gas System**
   - Supply pressures
   - Flow verification
   - Leak check

#### Shift Tasks
- Process log review
- Particle count check
- Temperature verification
- Consumables check

### 6.2 Weekly Maintenance

#### Chamber Cleaning
1. **Quartz Clean**
   - Cool chamber
   - Wipe with IPA
   - Check for deposits
   - Inspect for cracks

2. **Lamp Module**
   - Reflector cleaning
   - Lamp inspection
   - Connection check
   - Power balance test

#### System Checks
- Pyrometer windows
- Gas line purge
- Exhaust flow verify
- Safety interlock test

### 6.3 Monthly Maintenance

#### Comprehensive PM
1. **Lamp Replacement**
   - Criteria: 1000 hours or failure
   - Replace in groups
   - Power calibration after
   - Uniformity verification

2. **Pyrometer Service**
   - Window replacement
   - Fiber optic check
   - Electronics calibration
   - Noise level check

3. **Gas System**
   - MFC calibration
   - Filter replacement
   - Valve operation
   - Leak detection

### 6.4 Quarterly Maintenance

#### Major Service
1. **Chamber Overhaul**
   - Complete disassembly
   - Deep cleaning
   - Seal replacement
   - Reassembly and test

2. **Control System**
   - Software backup
   - Hardware diagnostics
   - Sensor calibration
   - Communication test

3. **Performance Qualification**
   - Temperature uniformity
   - Repeatability study
   - Process verification
   - Documentation

---

## 7. Troubleshooting

### 7.1 Temperature Issues

#### Problem: Non-uniformity > 5°C
**Diagnosis:**
1. **Lamp Check**
   - Individual lamp test
   - Power distribution
   - Age matching

2. **Pyrometer Issues**
   - Window contamination
   - Alignment drift
   - Calibration shift

3. **Wafer Placement**
   - Centering accuracy
   - Pin height uniform
   - Edge ring position

**Solutions:**
- Replace weak lamps
- Clean pyrometer windows
- Recalibrate system
- Adjust zone powers

### 7.2 Process Issues

#### Problem: Rs Out of Specification
**Investigation:**
1. **Temperature Accuracy**
   - Verify with TC wafer
   - Check pyrometer
   - Review temperature log

2. **Ambient Control**
   - Gas flow rates
   - Gas purity
   - Chamber leaks

3. **Time Control**
   - Ramp rates actual
   - Dwell time accuracy
   - Cool down rate

**Corrective Actions:**
- Temperature adjustment
- Gas system check
- Recipe optimization
- Hardware calibration

### 7.3 Reliability Issues

#### Problem: Lamp Failures
**Root Causes:**
1. **Power Cycling**
   - Excessive on/off
   - Rapid temperature changes
   - Power surges

2. **Contamination**
   - Fingerprints
   - Chemical deposits
   - Particulates

3. **Age Related**
   - Normal wear
   - Tungsten evaporation
   - Envelope degradation

**Prevention:**
- Proper handling
- Regular cleaning
- Grouped replacement
- Power conditioning

---

## 8. Safety Considerations

### 8.1 Thermal Hazards

#### High Temperature Safety
- **Chamber:** Up to 1200°C
- **Cool Down:** 30 minutes minimum
- **Indicators:** Warning lights
- **PPE:** Heat resistant gloves
- **Burns:** First aid available

#### Lamp Module Safety
- **UV Radiation:** Eye protection
- **High Voltage:** Lockout required
- **Hot Surfaces:** Clearly marked
- **Handling:** Two-person lift

### 8.2 Gas Safety

#### Toxic Gases
| Gas | Hazard | TLV | Response |
|-----|--------|-----|----------|
| NH3 | Corrosive | 25 ppm | Evacuate |
| SiH4 | Pyrophoric | 5 ppm | Shutdown |
| AsH3 | Toxic | 0.05 ppm | Emergency |

#### Safety Systems
- Gas detection monitors
- Automatic shutdown
- Exhaust ventilation
- Emergency scrubber
- PPE requirements

### 8.3 Electrical Safety

#### High Voltage
- **Lamp Power:** 480V, 400A
- **Lockout Points:** Identified
- **Discharge Time:** 5 minutes
- **Test Equipment:** Rated for voltage
- **Training:** Required

---

## 9. Advanced Applications

### 9.1 Stress Engineering

#### Tensile Stress (NMOS)
```
SMT Process:
- Stress Memorization Technique
- Pre-amorphization implant
- Tensile nitride deposition
- RTA: 1050°C spike
- Stress: +1.5 GPa
- Mobility gain: 15%
```

#### Compressive Stress (PMOS)
```
Embedded SiGe:
- Post-epi anneal
- Temperature: 1000°C
- Time: 5 seconds
- Stress: -2 GPa
- Mobility gain: 35%
```

### 9.2 Advanced Anneals

#### Laser Spike Anneal (LSA)
```
Hybrid Process:
- RTP preheat: 600°C
- Laser pulse: 1350°C peak
- Duration: < 1ms
- Applications:
  - USJ activation
  - Contact resistance
  - Defect anneal
```

#### Dynamic Surface Anneal (DSA)
```
Parameters:
- Peak: 1300°C
- Dwell: 1-5ms
- Ambient: N2
- Benefits:
  - High activation
  - Low diffusion
  - Low defects
```

### 9.3 Novel Materials

#### High-k Gate Stack
```
Post-Deposition Anneal:
- Material: HfO2
- Temperature: 900°C
- Time: 30 seconds
- Ambient: N2
- Purpose: Crystallization
```

#### III-V Integration
```
InGaAs Activation:
- Temperature: 600°C
- Time: 30 seconds
- Ambient: N2/H2
- Challenge: Low thermal budget
```

---

## 10. Performance Metrics

### 10.1 Process Capability

#### Key Metrics
| Parameter | Specification | Cpk | Status |
|-----------|--------------|-----|--------|
| Temperature | ± 3°C | 1.8 | Good |
| Uniformity | < 2% | 1.7 | Good |
| Rs | ± 5% | 1.5 | Good |
| Throughput | 60 WPH | N/A | Met |

### 10.2 Equipment Performance

#### Reliability Metrics
- **MTBF:** > 300 hours
- **MTTR:** < 2 hours
- **Availability:** > 95%
- **Lamp Life:** 1000 hours
- **PM Interval:** 4 weeks

### 10.3 Cost Analysis

#### Operating Costs
```
Cost per Wafer:
- Lamps: $1.50
- Gases: $0.30
- Energy: $0.50
- Maintenance: $0.70
Total: $3.00/wafer

Annual Budget:
- Lamps: $150k
- Service: $100k
- Gases: $30k
- Total: $280k
```

---

## Appendix A: Recipe Database

### Standard Recipes
| Process | Temp | Time | Gas | Application |
|---------|------|------|-----|-------------|
| Spike_1050 | 1050°C | 0s | N2 | Junction |
| RTO_1000 | 1000°C | 60s | O2 | Gate ox |
| Ni_Silicide | 450°C | 30s | N2 | Contact |
| Densify_900 | 900°C | 30s | N2 | ILD |

### Development Recipes
| Process | Status | Owner | Notes |
|---------|--------|-------|-------|
| MSA_1300 | Qual | R&D | Millisecond |
| SiGe_Anneal | Dev | Integration | Stress |
| Low_T_Spike | Test | Advanced | 500°C max |

---

## Appendix B: Troubleshooting Matrix

### Quick Reference
| Symptom | Probable Cause | Action |
|---------|---------------|--------|
| Poor uniformity | Lamp failure | Replace lamps |
| Temperature error | Pyrometer dirty | Clean windows |
| High Rs | Low temperature | Calibrate |
| Slow ramp | Power limit | Check lamps |
| Gas alarm | Leak detected | Find and fix |

---

**문서 관리:**
- 작성자: RTP 공정팀 권상우 수석
- 검토자: 열처리팀 나현정 책임
- 승인자: 공정기술부문 송민재 이사
- 차기 개정: 2025년 4월 (MSA 공정 추가)