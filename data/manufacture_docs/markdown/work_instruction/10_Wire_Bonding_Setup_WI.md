# Wire Bonding Machine Setup 작업 지시서
## K&S IConn ProCu Wire Bonder Recipe Development

**문서번호:** WI-WB-SETUP-011  
**효력발생일:** 2024년 12월 1일  
**개정번호:** Rev 1.3  

---

## 1. 문서 정보

### 1.1 승인 정보
| 구분 | 담당자 | 소속 | 직책 | 서명 |
|------|--------|------|------|------|
| 작성 | 남기훈 | Assembly팀 | 수석 | |
| 검토 | 서은지 | Package개발팀 | 책임 | |
| 승인 | 유상철 | 제조부문 | 부장 | |

### 1.2 적용 범위
- **장비:** K&S IConn ProCu Plus Wire Bonder
- **작업자:** Certified Wire Bond Engineers
- **작업 시기:** New package setup, Recipe optimization
- **소요시간:** 4-6시간 (complexity 따라)

---

## 2. 안전 주의사항 ⚠️

### 2.1 기계적 위험
- **Bond head:** 고속 이동 (충돌 주의)
- **Clamp force:** 최대 500gf (손가락 주의)
- **EFO spark:** 전기 충격 위험

### 2.2 정전기 위험
- **ESD 민감:** Device 손상 가능
- **Wrist strap:** 필수 착용
- **Ionizer:** 상시 작동 확인

---

## 3. Setup 준비

### 3.1 필수 준비물
- [ ] Package drawing
- [ ] Wire specification
- [ ] Sample units (30ea)
- [ ] Capillary (new/cleaned)
- [ ] Wire spool
- [ ] Pull/Shear tester
- [ ] Microscope
- [ ] Bond parameter sheet

### 3.2 Package 정보 확인
```
Package Information:
- Type: __________
- Die size: _____ × _____ mm
- Pad pitch: _____ µm
- Pad size: _____ × _____ µm
- Wire count: _____ wires
- Wire length: _____ mm (max)
```

---

## 4. Machine Setup 절차

### 4.1 Step 1: System 초기화 (15분)

**작업 내용:**
1. Machine 시작
   ```
   Power-on Sequence:
   1) Main power ON
   2) Air pressure: 6 bar
   3) N2 supply: ON (Cu wire용)
   4) System boot: 3분 대기
   5) Home position 실행
   ```

2. System 상태 확인
   ```
   [Main Screen] → [System Status]
   
   확인 항목:
   □ Vision system: OK
   □ XY table: Ready
   □ Bond head: Ready
   □ Wire clamp: Open
   □ No active alarms
   ```

3. 환경 조건
   ```
   요구사항:
   - Temperature: 25 ± 2°C
   - Humidity: 45 ± 10% RH
   - Vibration: < 5µm
   - ESD control: Active
   ```

### 4.2 Step 2: Capillary 설치 (20분)

**작업 내용:**
1. Capillary 선택
   ```
   Selection criteria:
   - Wire diameter: _____ µm
   - Hole size: Wire × 1.3
   - Chamfer diameter: CD
   - Face angle: FA
   - Tip diameter: _____ µm
   
   Model: __________
   ```

2. Capillary 장착
   ```
   설치 절차:
   1) Bond head를 service position
   2) 기존 capillary 제거
   3) 신규 capillary 삽입
   4) Set screw 체결 (가볍게)
   5) Alignment 확인
   6) 최종 체결
   ```

3. Capillary 정렬
   ```
   Vision alignment:
   1) [Setup] → [Capillary Align]
   2) Auto focus 실행
   3) X/Y offset 조정
   4) Rotation 조정
   5) Save position
   
   Tolerance: ± 2µm
   ```

### 4.3 Step 3: Wire Threading (15분)

**작업 내용:**
1. Wire spool 설치
   ```
   Wire 정보:
   - Material: □Au □Cu □Ag
   - Diameter: _____ µm
   - Elongation: _____ %
   - Spool ID: __________
   ```

2. Wire threading
   ```
   Threading 순서:
   1) Spool을 holder에 장착
   2) Wire를 guide를 통해 통과
   3) Air guide 조정
   4) Tensioner 설정: _____ gf
   5) Wire clamp 통과
   6) Capillary 통과 (자동)
   ```

3. Wire tail 형성
   ```
   Tail setup:
   1) Manual tail feed
   2) Length: 150-200µm
   3) EFO fire test
   4) Ball 형성 확인
   ```

### 4.4 Step 4: EFO Parameter Setup (25분)

**작업 내용:**
1. EFO 기본 설정
   ```
   Initial parameters:
   - Current: _____ mA
   - Time: _____ µs
   - Gas type: □N2 □Forming gas
   - Flow rate: _____ L/min
   ```

2. Free Air Ball (FAB) 최적화
   ```
   Ball formation test:
   1) Fire 10 balls
   2) 측정 (vision)
   3) Target: Wire × 2.2
   
   조정:
   - Ball 작음 → Current ↑
   - Ball 큼 → Current ↓
   - 비대칭 → Gas flow 조정
   ```

3. FAB 품질 확인
   ```
   검사 항목:
   □ Diameter: _____ µm (±2µm)
   □ Roundness: > 90%
   □ Centering: Good
   □ No golf ball
   □ Consistent size
   ```

### 4.5 Step 5: Bond Parameter Setup (40분)

**작업 내용:**
1. 1st Bond parameters
   ```
   Ball bond 설정:
   - Search height: _____ µm
   - Impact force: _____ gf
   - Bond force: _____ gf
   - Bond time: _____ ms
   - US power: _____ mW
   - US time: _____ ms
   - Temperature: _____ °C
   ```

2. Loop parameters
   ```
   Loop profile:
   - Loop height: _____ µm
   - Kink height: _____ µm
   - Rev distance: _____ µm
   - Rev height: _____ µm
   - Trajectory points: _____
   ```

3. 2nd Bond parameters
   ```
   Stitch bond 설정:
   - Search height: _____ µm
   - Bond force: _____ gf
   - Bond time: _____ ms
   - US power: _____ mW
   - US time: _____ ms
   - Tail length: _____ µm
   ```

### 4.6 Step 6: Pattern Recognition Setup (30분)

**작업 내용:**
1. Die PR (Pattern Recognition)
   ```
   Die reference 설정:
   1) Sample die load
   2) Move to die center
   3) [Vision] → [Teach Die PR]
   4) Select unique pattern
   5) Adjust brightness/contrast
   6) Save template
   
   Score: > 85 required
   ```

2. Lead PR setup
   ```
   Lead reference:
   1) Move to lead finger
   2) [Vision] → [Teach Lead PR]
   3) Define search area
   4) Pattern learning
   5) Test recognition (10 times)
   
   Success rate: > 95%
   ```

3. Reference system
   ```
   Coordinate 설정:
   - Die reference: (0, 0)
   - Matrix teaching
   - Offset calculation
   - Bond sequence define
   ```

### 4.7 Step 7: Bond Program Creation (45분)

**작업 내용:**
1. Wire sequence
   ```
   Programming:
   1) [Program] → [New]
   2) Device name: __________
   3) Wire count: _____
   
   각 wire 정의:
   - Start pad (X, Y)
   - End pad (X, Y)
   - Loop type
   - Special parameters
   ```

2. Bond 순서 최적화
   ```
   Sequence 원칙:
   - Short → Long wires
   - Inside → Outside
   - Minimize table movement
   - Avoid wire crossing
   ```

3. Program verification
   ```
   Dry run:
   1) Capillary up position
   2) Run without bonding
   3) Path 확인
   4) Interference check
   5) Cycle time: _____ sec
   ```

---

## 5. Process 검증

### 5.1 Test Bonding (30분)

**작업 내용:**
1. Sample bonding
   ```
   Initial run:
   - Units: 5 ea
   - Speed: 50%
   - 실시간 monitoring
   - Parameter 미세조정
   ```

2. Bond 품질 검사
   ```
   Visual inspection:
   □ Ball size/shape
   □ Ball placement
   □ Loop profile
   □ Stitch shape
   □ No short/sweep
   ```

### 5.2 Bond Strength Test (20분)

**작업 내용:**
1. Pull test
   ```
   Test 조건:
   - Sample: 10 wires
   - Pull angle: 90°
   - Speed: 100µm/s
   
   Results:
   Average: _____ gf
   Min: _____ gf
   Cpk: _____
   
   Spec: > 6gf (Au), > 8gf (Cu)
   ```

2. Ball shear test
   ```
   Test 조건:
   - Sample: 10 balls
   - Shear height: 5µm
   - Speed: 100µm/s
   
   Results:
   Average: _____ gf
   Min: _____ gf
   
   Spec: > 25gf
   ```

---

## 6. Recipe 최적화

### 6.1 Fine Tuning

| Parameter | Issue | Adjustment |
|-----------|-------|------------|
| Non-stick | Low temp/force | Increase force +5gf |
| Ball lift | Over US | Reduce power -10mW |
| Neck break | Impact high | Reduce impact -10gf |
| Poor loop | Speed fast | Reduce speed 20% |
| Stitch lift | Low force | Increase +10gf |

### 6.2 Process Window

```
DOE (Design of Experiment):
- Force: ±20% from nominal
- Power: ±20% from nominal
- Time: ±20% from nominal
- Find optimum window
- Document limits
```

---

## 7. 문서화

### 7.1 Recipe Card 작성

```
Recipe Documentation
=====================
Recipe Name: __________
Date: ____/__/__
Engineer: __________

Machine Parameters:
[1st Bond]
Force: _____ gf
Power: _____ mW
Time: _____ ms
Temp: _____ °C

[Loop]
Height: _____ µm
Type: __________

[2nd Bond]
Force: _____ gf
Power: _____ mW
Time: _____ ms

Performance:
Pull: _____ gf
Shear: _____ gf
UPH: _____ units
Yield: _____ %

Approved: __________
```

### 7.2 System 저장

```
[Recipe] → [Save As]
- Name: [Package]_[Wire]_[Rev]
- Lock recipe: Yes
- Backup: Server
- Access level: Production
```

---

## 8. Production 전환

### 8.1 Operator Training
- Recipe 설명
- Key parameter
- 주의사항
- Troubleshooting

### 8.2 Production Release
```
Release checklist:
□ Recipe locked
□ Document complete
□ Quality approved
□ MES updated
□ Training done
```

---

## 9. 이상 상황 대응

### 9.1 Bond 불량

| 불량 유형 | 원인 | 대책 |
|----------|------|------|
| NSOP | Contamination | Plasma clean |
| Cratering | Over-bonding | Reduce parameter |
| Wire sag | Long loop | Modify trajectory |
| Short | Wire sweep | Reduce loop |

### 9.2 Machine Alarm

| Alarm | Description | Action |
|-------|-------------|--------|
| PR_FAIL | Pattern not found | Re-teach |
| WIRE_BREAK | Wire 끊김 | Re-thread |
| CLAMP_ERR | Clamp 불량 | Clean/Replace |
| EFO_FAIL | No ball | Check gap |

---

**교육 이수 서명란:**

| 이름 | 사번 | 교육일 | 서명 |
|------|------|--------|------|
| | | | |
| | | | |

**문서 관리:** Assembly팀
**다음 개정:** 2025년 3월