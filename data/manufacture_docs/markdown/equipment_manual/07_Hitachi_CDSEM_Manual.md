# Critical Dimension SEM 장비 운영 매뉴얼
## Hitachi CG6300 CD-SEM

**문서번호:** EM-HIT-CG6300-001  
**개정일:** 2024.11.15  
**작성:** 계측장비 기술팀  

---

## 1. 장비 개요

### 1.1 System Specifications
- **Model:** Hitachi CG6300
- **Technology:** Cold Field Emission SEM
- **Resolution:** 0.8nm @ 1kV
- **Magnification:** 100x - 800,000x
- **CD Precision:** 0.3nm (3σ)
- **Throughput:** 35-45 WPH

### 1.2 Electron Optical System
- **Electron Source:** Cold cathode FE gun
- **Acceleration Voltage:** 300V - 2kV
- **Probe Current:** 0.5pA - 100pA
- **Working Distance:** 3.0mm fixed
- **Detectors:** SE, BSE detectors

### 1.3 Stage System
- **Travel Range:** 300mm full wafer
- **Positioning Accuracy:** ± 0.5µm
- **Repeatability:** ± 0.1µm
- **Rotation:** 360° continuous
- **Tilt:** Not available (0°)

### 1.4 Image Processing
- **Digital Resolution:** 1024x1024 pixels
- **Frame Integration:** 8-64 frames
- **CD Algorithm:** Threshold, derivative, model-based
- **Pattern Recognition:** Template matching
- **Data Format:** GDSII overlay capable

---

## 2. Installation Requirements

### 2.1 Environmental Requirements

#### Vibration Isolation
- **Specification:** VC-F or better
- **Active Isolation:** Air suspension
- **Frequency Range:** 1-100 Hz
- **Amplitude:** < 0.5 µm peak-to-peak

#### Magnetic Field
- **AC Field:** < 1 mG peak-to-peak
- **DC Field:** < 5 mG
- **Shielding:** Mu-metal if required
- **Monitor:** Continuous logging

#### Environmental Control
- **Temperature:** 22°C ± 0.5°C
- **Humidity:** 45% ± 5%
- **Cleanroom:** ISO Class 5
- **Acoustic:** < 60 dBC

### 2.2 Utilities

| Utility | Specification | Consumption |
|---------|--------------|-------------|
| Power | 200V, 1φ, 30A | 5 kW |
| Dry N2 | 99.999%, 80 PSI | 20 L/min |
| Compressed Air | Oil-free, 80 PSI | 10 L/min |
| Chilled Water | 20°C ± 1°C | 5 L/min |

### 2.3 Space Requirements
- **Footprint:** 3.5m x 2.5m
- **Service Area:** 1m all sides
- **Height:** 2.8m minimum
- **Weight:** 3,500 kg
- **Floor Loading:** 1,000 kg/m²

---

## 3. Basic Operation

### 3.1 System Start-up

#### Daily Start-up Sequence
1. **Vacuum System Check**
   - Gun vacuum: < 1E-9 Torr
   - Column vacuum: < 1E-7 Torr
   - Chamber vacuum: < 1E-6 Torr

2. **Electron Gun Activation**
   - Flash procedure if needed
   - Emission current: 10 µA
   - Stability check: < 0.5% drift

3. **Alignment Procedure**
   ```
   Gun Alignment:
   - Gun tilt X/Y
   - Gun shift X/Y
   - Anode centering
   
   Column Alignment:
   - Condenser alignment
   - Aperture centering
   - Stigmator adjustment
   - Image shift calibration
   ```

4. **Calibration Verification**
   - Load pitch standard
   - Measure 100nm pitch
   - Verify ± 1% accuracy

### 3.2 Sample Loading

#### Wafer Handling
1. **FOUP Loading**
   - Place on load port
   - Map wafer presence
   - Select wafer

2. **Pre-alignment**
   - Notch detection
   - Center finding
   - Orientation correction

3. **Transfer to Chamber**
   - Robot pick-up
   - Load lock pump-down
   - Chamber transfer
   - Stage loading

### 3.3 Recipe Setup

#### CD Measurement Recipe
```
Recipe Parameters:
├── Imaging Conditions
│   ├── Acceleration Voltage: 500V
│   ├── Probe Current: 8pA
│   ├── Magnification: 100kx
│   └── Working Distance: 3.0mm
├── Scan Parameters
│   ├── Scan Speed: TV rate
│   ├── Integration: 32 frames
│   ├── Pixel Size: 0.5nm
│   └── Field of View: 500nm
├── Measurement Settings
│   ├── Algorithm: Model-based
│   ├── Threshold: 50%
│   ├── Filter: Gaussian 3x3
│   └── Edge Detection: Maximum slope
└── Output Configuration
    ├── Parameters: CD, SWA, LER
    ├── Statistics: Mean, 3σ
    └── Images: Save all
```

---

## 4. CD Measurement Techniques

### 4.1 Measurement Algorithms

#### Threshold Method
- **Principle:** Fixed intensity level
- **Application:** High contrast features
- **Setting:** 50% typical
- **Advantage:** Simple, fast
- **Limitation:** Edge effect sensitive

#### Derivative Method
- **Principle:** Maximum slope detection
- **Application:** Sloped sidewalls
- **Processing:** First derivative of profile
- **Advantage:** Less noise sensitive
- **Limitation:** Requires smooth profile

#### Model-Based Method
- **Principle:** Physical model fitting
- **Application:** Complex profiles
- **Parameters:** Material properties
- **Advantage:** Most accurate
- **Limitation:** Computation intensive

### 4.2 Advanced Measurements

#### Line Edge Roughness (LER)
```
Measurement Protocol:
1. High magnification: 200kx
2. Long scan length: 2µm
3. Sampling: 2048 points
4. Analysis:
   - 3σ calculation
   - PSD analysis
   - Correlation length
   - Frequency spectrum
```

#### Sidewall Angle (SWA)
- **Tilt Method:** Not available
- **Model Fitting:** BSE signal analysis
- **Accuracy:** ± 2°
- **Range:** 85-90° typical

#### Contact Hole Measurement
- **Challenge:** Charging, visibility
- **Solution:** Low voltage, fast scan
- **Parameters:**
  - Voltage: 300-500V
  - Current: 2-5pA
  - Integration: 8 frames

### 4.3 Pattern Recognition

#### Auto Focus
1. **Coarse Focus**
   - Range: ± 100µm
   - Step: 5µm
   - Metric: Contrast

2. **Fine Focus**
   - Range: ± 10µm
   - Step: 0.5µm
   - Metric: Sharpness

#### Auto Stigmation
- **Method:** FFT analysis
- **Correction:** X/Y stigmators
- **Criterion:** Circular FFT pattern
- **Iteration:** Maximum 3 cycles

#### Pattern Matching
- **Template:** Design or SEM image
- **Correlation:** > 0.8 required
- **Search Range:** ± 50µm
- **Rotation:** ± 5° tolerance

---

## 5. Maintenance Procedures

### 5.1 Daily Maintenance

#### Operator Checks
1. **Vacuum Levels**
   - Record all gauges
   - Check trends
   - Alert if degradation

2. **Image Quality**
   - Resolution check
   - Astigmatism check
   - Drift monitoring

3. **Measurement Accuracy**
   - Pitch standard
   - Control wafer
   - SPC charts update

### 5.2 Weekly Maintenance

#### Column Cleaning
1. **Aperture Cleaning**
   - Remove aperture strip
   - Plasma clean: 5 minutes
   - Reinstall carefully

2. **Detector Cleaning**
   - SE detector grid
   - BSE detector surface
   - Scintillator check

3. **Gun Maintenance**
   - Flash if needed
   - Emission check
   - Stability verification

### 5.3 Monthly Maintenance

#### Comprehensive PM
1. **Vacuum System**
   - Pump oil check
   - Seal inspection
   - Leak detection

2. **Stage Calibration**
   - Laser interferometer check
   - Repeatability test
   - Orthogonality verification

3. **Electron Optics**
   - Lens alignment
   - Deflector calibration
   - Detector gain adjustment

### 5.4 Quarterly Maintenance

#### Major Service
1. **Gun Replacement**
   - Schedule: 6-12 months
   - Duration: 8 hours
   - Includes: Full alignment

2. **Stage Service**
   - Bearing inspection
   - Encoder cleaning
   - Motor check

3. **System Calibration**
   - Magnification calibration
   - All measurement algorithms
   - Pattern recognition update

---

## 6. Troubleshooting

### 6.1 Image Quality Issues

#### Problem: Poor Resolution
**Diagnosis:**
1. **Check Alignment**
   - Gun alignment
   - Stigmator setting
   - Aperture centering

2. **Verify Vacuum**
   - Gun vacuum < 1E-9
   - Column contamination
   - Sample outgassing

3. **Electron Source**
   - Emission current
   - Tip condition
   - Extraction voltage

**Solutions:**
- Realignment procedure
- Gun flash/replacement
- Bake-out column
- Reduce probe current

#### Problem: Image Drift
**Investigation:**
1. **Charging Effects**
   - Voltage too high
   - Poor grounding
   - Insulating sample

2. **Thermal Drift**
   - Stage temperature
   - Room temperature
   - Air flow

3. **Mechanical Issues**
   - Stage settling
   - Vibration
   - Acoustic noise

**Corrective Actions:**
- Reduce voltage
- Increase scan speed
- Wait for thermal equilibrium
- Check vibration isolation

### 6.2 Measurement Issues

#### Problem: CD Variation > 1nm
**Root Cause Analysis:**
1. **Focus Variation**
   - Auto-focus failure
   - Sample height variation
   - Stage tilt

2. **Algorithm Issues**
   - Threshold setting
   - Noise level
   - Edge detection

3. **Sample Issues**
   - Resist shrinkage
   - Contamination
   - Charging

**Resolution:**
- Manual focus optimization
- Algorithm parameter tuning
- Lower acceleration voltage
- Fresh calibration

#### Problem: Pattern Recognition Failure
**Troubleshooting Steps:**
1. **Template Quality**
   - Update template
   - Increase search range
   - Reduce correlation threshold

2. **Stage Accuracy**
   - Calibration check
   - Repeatability test
   - Coordinate system verify

3. **Image Quality**
   - Improve S/N ratio
   - Optimize imaging conditions
   - Check contamination

---

## 7. Advanced Applications

### 7.1 3D Profile Reconstruction

#### Stereo Imaging
- **Method:** Dual detector imaging
- **Detectors:** SE + BSE simultaneous
- **Processing:** Shape from shading
- **Output:** Height map
- **Accuracy:** ± 5nm vertical

### 7.2 Automated Recipe Generation

#### Design-Based Metrology
```
Workflow:
1. Import GDS file
2. Select measurement sites
3. Auto-generate coordinates
4. Create measurement recipe
5. Optimize imaging conditions
6. Validate on test wafer
```

### 7.3 Machine Learning Integration

#### CD Prediction Model
- **Inputs:** Image features
- **Algorithm:** CNN
- **Training:** 10,000+ images
- **Accuracy:** ± 0.5nm
- **Speed:** 10x faster

#### Defect Classification
- **Categories:** Bridging, breaks, roughness
- **Detection:** Anomaly detection
- **Confidence:** > 95%
- **Action:** Auto-alert

---

## 8. Calibration Standards

### 8.1 Magnification Calibration

#### Pitch Standards
| Pitch | Material | Uncertainty | Frequency |
|-------|----------|-------------|-----------|
| 100nm | Si grating | ± 0.5nm | Daily |
| 200nm | Si grating | ± 1.0nm | Weekly |
| 700nm | Au on Si | ± 2.0nm | Monthly |

#### Calibration Procedure
1. Load standard
2. Locate pattern
3. Measure 10 locations
4. Calculate correction
5. Update calibration file
6. Verify with second standard

### 8.2 CD Standards

#### Reference Materials
- **NIST traceable:** 100nm ± 2nm
- **Cross-section:** Available
- **Material:** Poly-Si on SiO2
- **Certification:** Annual

#### Transfer Standards
- **In-house:** Monitor wafers
- **Correlation:** To NIST standard
- **Frequency:** Daily use
- **Control:** SPC tracking

---

## 9. Data Management

### 9.1 Data Collection

#### Measurement Data
```
Data Structure:
├── Wafer Information
│   ├── Lot ID
│   ├── Wafer ID
│   ├── Recipe name
│   └── Timestamp
├── Site Data
│   ├── Coordinates
│   ├── CD values
│   ├── Statistics
│   └── Images
├── Summary Statistics
│   ├── Mean
│   ├── 3σ
│   ├── Range
│   └── Cpk
└── Quality Flags
    ├── Focus quality
    ├── Pattern match score
    └── Measurement confidence
```

### 9.2 Database Integration

#### MES Connection
- **Protocol:** SECS/GEM
- **Data Points:** 100+ per site
- **Upload:** Real-time
- **Format:** XML/CSV

#### Analysis Tools
- **SPC Charts:** Real-time
- **Correlation:** Multi-tool
- **Trending:** Historical
- **Reporting:** Automated

### 9.3 Image Archive

#### Storage Requirements
- **Image Size:** 1-4 MB each
- **Retention:** 90 days minimum
- **Compression:** Lossless
- **Backup:** Daily incremental

---

## 10. Performance Metrics

### 10.1 Measurement Capability

#### Precision (Repeatability)
| Feature | Static (3σ) | Dynamic (3σ) |
|---------|------------|---------------|
| Line CD | 0.3nm | 0.5nm |
| Contact | 0.5nm | 0.8nm |
| LER | 0.2nm | 0.3nm |
| SWA | 1.0° | 1.5° |

#### Accuracy
- **Calibration:** NIST traceable
- **Uncertainty:** ± 2nm total
- **Verification:** Cross-section
- **Audit:** Annual

### 10.2 Throughput Analysis

#### Time Breakdown (per site)
```
Load/Unload: 15 sec
Move time: 3 sec
Auto-focus: 5 sec
Measurement: 10 sec
Total: 33 sec/site

Sites/wafer: 50
Total time: 27.5 min/wafer
Throughput: ~40 WPH
```

### 10.3 Tool Matching

#### Fleet Management
- **Matching Criteria:** ± 0.5nm offset
- **Method:** Golden wafer
- **Frequency:** Weekly
- **Documentation:** Required

#### Correlation Studies
- **Reference:** Cross-section SEM
- **Sites:** 20 minimum
- **R² Target:** > 0.98
- **Slope:** 1.00 ± 0.02

---

## Appendix A: Recipe Parameters

### Logic Gate CD
```
Voltage: 500V
Current: 8pA
Mag: 100kx
Integration: 32
Algorithm: Model-based
Sites: 45
```

### Contact Holes
```
Voltage: 300V
Current: 5pA
Mag: 150kx
Integration: 16
Algorithm: Ellipse fit
Sites: 65
```

### Metal Lines
```
Voltage: 800V
Current: 10pA
Mag: 80kx
Integration: 24
Algorithm: Threshold
Sites: 35
```

---

## Appendix B: Error Codes

### Critical Errors
| Code | Description | Action |
|------|-------------|--------|
| E101 | Gun vacuum fail | Check gun, pumps |
| E102 | Stage error | Initialize stage |
| E103 | Detector fail | Check connections |
| E104 | Focus fail | Manual focus |

### Warnings
| Code | Description | Action |
|------|-------------|--------|
| W201 | Emission low | Schedule flash |
| W202 | Vibration detected | Check environment |
| W203 | Calibration due | Run calibration |
| W204 | PM due | Schedule PM |

---

**문서 관리:**
- 작성자: 계측장비팀 강민수 수석
- 검토자: 품질팀 한지영 책임
- 승인자: 기술지원부문 조현철 이사
- 차기 개정: 2025년 6월 (AI 측정 기능 추가)