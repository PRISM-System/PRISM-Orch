# Plasma Etcher 장비 운영 매뉴얼
## LAM Research Flex 45 - Dielectric Etch

**문서번호:** EM-LAM-FX45-001  
**개정일:** 2024.11.15  
**작성:** 장비기술팀  

---

## 1. 장비 개요

### 1.1 Model Specifications
- **Model:** LAM Research Flex 45
- **Process Type:** Dielectric Etching (Oxide, Nitride, Low-k)
- **Wafer Size:** 300mm
- **Throughput:** 60 WPH (Wafers Per Hour)

### 1.2 Chamber Configuration
- **Type:** Dual Frequency Capacitively Coupled Plasma (CCP)
- **Electrode:** Parallel plate design
- **Chamber Material:** Anodized aluminum with Yttria coating
- **Chamber Volume:** 45 Liters

### 1.3 RF Power System
- **Source Frequency:** 13.56 MHz (2kW max)
- **Bias Frequency:** 40 MHz (500W max)
- **Matching Network:** Auto-tune with < 2 sec tuning time
- **Power Delivery:** Solid state amplifiers

### 1.4 Gas Delivery System
- **MFC Channels:** 8 channels
- **Gas Box Configuration:**
  - Channel 1-2: Fluorocarbon (CF4, C4F8)
  - Channel 3-4: CHF3, CH2F2
  - Channel 5: O2
  - Channel 6: Ar
  - Channel 7: N2
  - Channel 8: He (backside cooling)

### 1.5 Endpoint Detection System
- **OES Wavelength Range:** 200-800 nm
- **Sampling Rate:** 10 Hz
- **Algorithm:** Multi-wavelength with derivative analysis

---

## 2. Installation Requirements

### 2.1 Facility Requirements
#### 전력 사양
- **Main Power:** 480V, 3-phase, 200A
- **Frequency:** 60 Hz ± 0.5%
- **Voltage Regulation:** ± 5%
- **Emergency Power Off (EMO):** Required

#### Cooling Water
- **Temperature:** 15°C ± 1°C
- **Flow Rate:** 30 GPM minimum
- **Pressure:** 60-80 PSI
- **Conductivity:** < 1 µS/cm

#### Process Gases
| Gas | Purity | Pressure | Flow Range |
|-----|---------|----------|------------|
| CF4 | 99.999% | 80 PSI | 0-200 sccm |
| CHF3 | 99.999% | 80 PSI | 0-150 sccm |
| O2 | 99.999% | 80 PSI | 0-100 sccm |
| Ar | 99.999% | 80 PSI | 0-500 sccm |
| N2 | 99.999% | 80 PSI | 0-200 sccm |

#### Exhaust System
- **Capacity:** 500 CFM at 0.5" W.C.
- **Scrubber Type:** Wet scrubber for fluorine compounds
- **Pump:** Dry pump with N2 purge capability

### 2.2 Cleanroom Requirements
- **Class:** ISO Class 4 (Class 10)
- **Temperature:** 21°C ± 1°C
- **Humidity:** 45% ± 5%
- **Differential Pressure:** Positive 0.05" W.C.

### 2.3 Footprint and Service Clearance
- **Equipment Footprint:** 2.5m x 2.0m
- **Front Service:** 1.2m minimum
- **Rear Service:** 1.0m minimum
- **Side Clearance:** 0.8m each side
- **Height Clearance:** 3.0m minimum

---

## 3. 운전 조건 설정

### 3.1 Power Setpoint 설정

#### Source Power (13.56 MHz)
- **Range:** 300-2000W
- **Typical Process:** 800-1200W
- **Ramp Rate:** 50W/sec maximum
- **Tuning:** Auto-match < 2 seconds

**💡 Tuning Tip:** Source power 주로 etch rate 제어. 100W 증가 시 약 8-10% rate 상승

#### Bias Power (40 MHz)
- **Range:** 50-500W
- **Typical Process:** 150-300W
- **Ion Energy Control:** Direct correlation
- **Profile Control:** Lower bias = more isotropic

**💡 Tuning Tip:** Bias power는 profile angle 제어. High aspect ratio에서는 250W 이상 권장

### 3.2 Pressure Control
- **Range:** 1-100 mTorr
- **Control Type:** Throttle valve with adaptive PID
- **Stability:** ± 0.5 mTorr
- **Response Time:** < 500 ms

**압력별 특성:**
- **Low Pressure (5-20 mTorr):** High ion directionality, better CD control
- **Medium Pressure (20-50 mTorr):** Balanced etch rate and uniformity
- **High Pressure (50-100 mTorr):** High etch rate, more chemical etching

### 3.3 Gas Flow 설정

#### MFC Calibration
**Monthly Calibration Procedure:**
1. Zero calibration: Pump down to base, close valve, record zero
2. Span calibration: Flow N2 at 100 sccm with calibrated flow meter
3. Linearity check: 25%, 50%, 75%, 100% of full scale
4. Acceptance: ± 1% of setpoint

### 3.4 Temperature Zones

#### Chamber Wall
- **Setpoint:** 60°C ± 2°C
- **Purpose:** Prevent polymer deposition
- **Heater Type:** Resistive heaters in wall

#### ESC (Electrostatic Chuck)
- **Range:** -10°C to 60°C
- **Typical:** 20°C for oxide, 40°C for nitride
- **Coolant:** Galden fluid
- **He Backside:** 10-20 Torr for heat transfer

#### Chamber Lid
- **Setpoint:** 120°C ± 3°C
- **Purpose:** Prevent condensation and particle generation
- **Heating:** Embedded heaters with dual zone control

---

## 4. Process Sequence Programming

### 4.1 Recipe Editor 사용법

#### Recipe Structure
```
Step 1: Stabilization
- Pressure: 10 mTorr
- Gas: Ar 100 sccm
- Time: 5 sec
- No RF

Step 2: Main Etch
- Pressure: 25 mTorr
- Gas: CF4/CHF3/O2 = 50/30/10 sccm
- Source Power: 1000W
- Bias Power: 200W
- Time: Endpoint + 20% OE

Step 3: Over Etch
- Pressure: 40 mTorr
- Gas: CHF3/O2 = 80/5 sccm
- Source Power: 600W
- Bias Power: 150W
- Time: 15 sec

Step 4: Purge
- Pressure: 50 mTorr
- Gas: N2 200 sccm
- Time: 10 sec
```

### 4.2 Step Transition Conditions
- **Time Based:** Fixed duration
- **Endpoint Based:** OES signal detection
- **Pressure Based:** Achieve setpoint before proceeding
- **Temperature Based:** ESC temperature stable ± 0.5°C

### 4.3 Endpoint Algorithm 설정
- **Wavelength Selection:** CO (483nm), CN (388nm) for SiO2
- **Algorithm Type:** Derivative with smoothing
- **Threshold:** 80% drop from baseline
- **Confirmation Time:** 2 seconds continuous signal

### 4.4 Fault Recovery Sequence
**Auto Recovery Conditions:**
- RF reflected power > 50W → Retry match tuning
- Pressure deviation > 10% → Adjust throttle valve
- He leak rate > 5 sccm → Re-clamp wafer

**Manual Intervention Required:**
- Chamber impedance shift > 20%
- Particle count > 50 adds
- Endpoint not detected in 2x expected time

---

## 5. 정기 점검 및 유지보수

### 5.1 Daily Checks

#### Foreline Pressure 확인
- **Location:** Pump display panel
- **Normal Range:** < 100 mTorr
- **Action if High:** Check pump oil level, N2 purge flow

#### Helium Leak Rate Test
- **Procedure:** 
  1. Load dummy wafer
  2. Apply ESC voltage (500V)
  3. Monitor He flow meter
- **Acceptance:** < 2 sccm at 10 Torr backside

#### RF Hour Meter 기록
- **Location:** RF generator display
- **Purpose:** Track consumable life
- **Record:** Daily in logbook

### 5.2 Weekly Maintenance

#### Chamber Seasoning
**After Wet Clean:**
```
Recipe: SEASON_OXIDE
- CF4/O2 = 100/20 sccm
- Power: 1500W/300W
- Time: 30 minutes
- Purpose: Stabilize chamber condition
```

#### Focus Ring 육안 검사
- **Check Points:**
  - Erosion depth < 2mm
  - No chips or cracks
  - Uniform color (no hot spots)

#### Viewport Cleaning
- **Material:** IPA with lint-free wipe
- **Frequency:** Every 500 wafers or weekly
- **Caution:** Do not scratch quartz window

### 5.3 Monthly Maintenance

#### O-ring Inspection
- **Locations:** 
  - Chamber lid seal
  - Viewport seal
  - Gas line connections
- **Check:** No cuts, swelling, or hardening
- **Lubrication:** Krytox grease (thin layer)

#### MFC Calibration
- **Tools Required:** Calibrated flow meter
- **Procedure:** As per Section 3.3
- **Documentation:** Calibration certificate

#### Robot Teaching Verification
- **Test:** Run dummy wafer cycle
- **Check Points:**
  - Centering on ESC ± 0.5mm
  - No wafer sliding
  - Smooth motion (no jerking)

### 5.4 Quarterly Maintenance

#### Turbo Pump Service
- **Oil Level Check:** Via sight glass
- **Vibration Check:** < 0.5 mm/s RMS
- **Temperature:** < 60°C at bearing
- **Running Hours:** Record for PM schedule

#### RF Match Network Cleaning
- **Procedure:**
  1. Power off and lockout
  2. Remove match cover
  3. Blow out with dry N2
  4. Check capacitor movement
  5. Verify ground connections

#### Endpoint Window Replacement
- **Frequency:** Every 10,000 wafers or quarterly
- **Parts:** Quartz viewport, O-ring
- **Post-maintenance:** Leak check < 1.0E-9 Torr·L/sec

---

## 6. Parts 수명 관리

### 6.1 Consumable Parts List and Replacement Schedule

| Part Name | Part Number | Life (RF Hours) | Life (Wafers) | Cost |
|-----------|-------------|-----------------|---------------|------|
| Shower Head | SH-045-01 | 3000 | 60,000 | $12,000 |
| Focus Ring | FR-045-QZ | 1500 | 30,000 | $3,500 |
| Chamber Liner | CL-045-Y2O3 | 5000 | 100,000 | $8,000 |
| ESC | ESC-045-01 | 8000 | 160,000 | $25,000 |
| Edge Ring | ER-045-01 | 1000 | 20,000 | $1,500 |
| Bellows | BL-045-SS | 10000 | 200,000 | $2,000 |

### 6.2 교체 절차 Step-by-Step

#### Focus Ring Replacement
1. **Preparation (30 min)**
   - Vent chamber with N2
   - Cool down to < 30°C
   - Open chamber

2. **Removal (15 min)**
   - Remove 6x screws (torque: 15 in-lb)
   - Lift old focus ring carefully
   - Inspect ESC surface for damage

3. **Installation (20 min)**
   - Clean mating surface with IPA
   - Place new focus ring
   - Torque screws in star pattern
   - Verify flatness < 0.05mm

4. **Qualification (2 hours)**
   - Pump down and leak check
   - Run seasoning recipe (30 min)
   - Process monitor wafer
   - Measure CD and uniformity

### 6.3 Post-Maintenance Qualification

#### Particle Qualification
- **Test:** 25 dummy wafers
- **Pass Criteria:** < 5 adds @ 0.13μm
- **If Fail:** Extended seasoning + repeat

#### Process Qualification
- **Etch Rate:** ± 5% of baseline
- **Uniformity:** < 3% (3σ)
- **CD Bias:** ± 2nm from target
- **Profile Angle:** 88° ± 2°

---

## 7. Troubleshooting Guide

### 7.1 Etch Rate Drift

#### 현상: Etch rate 10% 이상 변화

#### Check Points and Solutions:

**Check 1: Endpoint Window 오염도**
- **확인:** Visual inspection through viewport
- **정상:** Clear, transparent
- **이상:** Cloudy, coated
- **조치:** IPA cleaning or replacement

**Check 2: Chamber Temperature Stability**
- **확인:** Temperature log trend (last 24 hours)
- **정상:** ± 1°C variation
- **이상:** Cycling or drift
- **조치:** 
  - Check heater resistance
  - Verify TCU operation
  - Calibrate temperature sensors

**Check 3: MFC Actual vs. Setpoint**
- **확인:** MFC diagnostic screen
- **정상:** Actual = Setpoint ± 1%
- **이상:** Deviation > 2%
- **조치:**
  - Zero/span calibration
  - Check gas supply pressure
  - Replace MFC if persistent

**Check 4: RF Power Delivery**
- **확인:** Forward/Reflected power
- **정상:** Reflected < 2% of forward
- **이상:** High reflected power
- **조치:**
  - Clean RF contacts
  - Check match network tuning
  - Measure chamber impedance

### 7.2 Uniformity Degradation

#### 현상: Within-wafer uniformity > 5%

**Root Cause Analysis:**
1. **Gas Distribution:**
   - Check shower head holes for clogging
   - Verify gas flow ratio stability
   
2. **Temperature Distribution:**
   - ESC temperature mapping
   - He backside pressure uniformity
   
3. **Plasma Density:**
   - Check magnetic field configuration
   - RF power coupling efficiency

### 7.3 Particle Excursions

#### 현상: Particle adds > 20 @ 0.13μm

**Immediate Actions:**
1. Stop processing
2. Run particle monitor wafer
3. Inspect chamber visually

**Systematic Investigation:**
- Chamber pressure stability
- Wafer clamping/de-clamping sequence
- Polymer flaking from chamber walls
- Focus ring condition

---

## 8. Safety Interlock System

### 8.1 EMO Circuit
- **Activation:** Red button at tool frame
- **Result:** 
  - RF power off immediately
  - Gas flow stopped
  - Chamber isolated
  - Pumps continue running

### 8.2 Gas Detection System
- **Toxic Gas Monitor:** SiH4, NH3
- **Location:** Gas box exhaust
- **Alarm Level 1:** 10 ppm → Visual/audio alarm
- **Alarm Level 2:** 25 ppm → Auto gas shutdown

### 8.3 RF Power Interlock
- **Door Open:** RF disabled
- **Reflected Power > 100W:** Auto shutdown
- **Arc Detection:** < 100μs response

### 8.4 Chamber Access Control
- **Interlock:** Cannot open if pressure > 100 Torr
- **Vent Sequence:** Auto N2 purge before opening
- **Light Curtain:** Stops robot if breached

---

## 9. Spare Parts Inventory

### 9.1 Critical Spares List

| Category | Part | Min Stock | Current | Lead Time |
|----------|------|-----------|---------|-----------|
| **Critical** | ESC | 1 | 1 | 12 weeks |
| **Critical** | Shower Head | 1 | 2 | 8 weeks |
| **Critical** | RF Match Board | 1 | 1 | 6 weeks |
| **Essential** | Focus Ring | 3 | 4 | 4 weeks |
| **Essential** | Chamber Liner | 2 | 2 | 6 weeks |
| **Essential** | MFC | 2 | 3 | 3 weeks |
| **Routine** | O-rings Set | 5 | 8 | 1 week |
| **Routine** | Viewport | 2 | 3 | 2 weeks |

### 9.2 Vendor Information
- **OEM Parts:** LAM Research Korea
  - Contact: +82-31-000-0000
  - Lead time: 4-12 weeks
  - Emergency: 24hr hotline

- **Refurbished Parts:** Semicore Solutions
  - Contact: +82-31-111-1111
  - Lead time: 2-6 weeks
  - Cost: 40-60% of OEM

### 9.3 Compatible Parts Cross-Reference
| OEM Part # | Compatible | Vendor | Notes |
|------------|------------|--------|-------|
| SH-045-01 | SH-045-RF | Semicore | Refurbished, 80% life |
| FR-045-QZ | FR-045-SI | Local | Silicon version, similar performance |

---

## 10. Performance Metrics

### 10.1 Reliability Metrics
- **MTBF Target:** > 200 hours
- **Current MTBF:** 218 hours (3-month average)
- **MTTR Target:** < 4 hours
- **Current MTTR:** 3.5 hours

### 10.2 Process Performance
- **Particle Performance:** < 5 adds @ 0.13μm
- **Current:** 3.2 adds average
- **Uniformity:** < 3% (3σ)
- **Current:** 2.4%

### 10.3 Throughput Metrics
- **Mechanical Time:** 45 sec/wafer
- **Process Time:** 90 sec/wafer (typical)
- **Overall Equipment Efficiency (OEE):** > 85%
- **Current OEE:** 87.3%

### 10.4 Cost Metrics
- **Cost per Wafer:** $12.50
  - Consumables: $8.00
  - Utilities: $2.50
  - Maintenance: $2.00
- **Yearly Parts Cost:** $180,000

---

## Appendix A: Alarm Codes and First Response

| Alarm Code | Description | First Action | Engineer Call |
|------------|-------------|--------------|---------------|
| AL-001 | RF Reflected High | Check match tuning | If persists > 3 attempts |
| AL-002 | Pressure Unstable | Check throttle valve | Immediately |
| AL-003 | He Leak High | Re-clamp wafer | If > 5 sccm |
| AL-004 | Temperature Error | Check TCU status | If ± 5°C deviation |
| AL-005 | MFC Deviation | Check gas pressure | If > 5% deviation |

## Appendix B: Process Recipes Library

### Standard Oxide Etch
- **Target:** 5000Å SiO2
- **Rate:** 5500Å/min
- **Selectivity to Si:** > 30:1
- **Profile:** 89° ± 1°

### Low-k Dielectric Etch
- **Material:** SiOCH (k=2.7)
- **Chemistry:** Reduced O2 to prevent damage
- **Critical:** Minimize k-value shift

### Contact Etch (High Aspect Ratio)
- **Aspect Ratio:** Up to 20:1
- **Key:** High bias power, low pressure
- **Challenge:** Bottom CD control

---

**문서 관리:**
- 작성자: 장비기술팀 김상훈 수석
- 검토자: 공정기술팀 박지원 책임
- 승인자: 제조부문 이준호 이사
- 차기 개정: 2025년 2월 (Quarterly PM 결과 반영)

**교육 이수 기록:**

| 이름 | 소속 | 교육일 | 서명 |
|------|------|--------|------|
| | | | |
| | | | |