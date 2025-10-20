# CMP Pad 교체 작업 지시서
## Reflexion LK Prime CMP System

**문서번호:** WI-CMP-PAD-004  
**효력발생일:** 2024년 12월 1일  
**개정번호:** Rev 2.1  

---

## 1. 문서 정보

### 1.1 승인 정보
| 구분 | 담당자 | 소속 | 직책 | 서명 |
|------|--------|------|------|------|
| 작성 | 김상호 | CMP 기술팀 | 책임 | |
| 검토 | 이정민 | CMP 생산팀 | 수석 | |
| 승인 | 박철수 | 제조부문 | 부장 | |

### 1.2 적용 범위
- **장비:** Applied Materials Reflexion LK Prime
- **작업자:** CMP Engineers, Senior Operators
- **주기:** 150시간 사용 또는 Performance 저하 시
- **소요시간:** 90분/Platen

---

## 2. 안전 주의사항 ⚠️

### 2.1 물리적 위험
- **Platen:** 회전부 접촉 주의 (Lock-out 필수)
- **무게:** Pad carrier 약 15kg (2인 작업)
- **미끄러짐:** Slurry 잔류물로 인한 미끄러짐 주의

### 2.2 화학물질
- **Slurry 잔류물:** 피부 자극성
- **DI Water:** 대량 사용 시 바닥 미끄러움
- **IPA:** 세척 시 환기 필수

---

## 3. 작업 준비물

### 3.1 필수 도구 및 자재
- [ ] 신규 CMP Pad (IC1010 or Politex)
- [ ] Pad conditioner disk (신품)
- [ ] Torque wrench (15 N·m)
- [ ] Pad template (정렬용)
- [ ] Diamond disk dresser
- [ ] DI water spray bottle
- [ ] IPA wipes
- [ ] 진공 흡입기
- [ ] 작업 체크시트

### 3.2 PPE
- [ ] Cleanroom suit
- [ ] Chemical resistant gloves
- [ ] Safety goggles
- [ ] Face shield (세척 시)

---

## 4. 단계별 작업 절차

### 4.1 Step 1: 시스템 Shutdown (10분)

**작업 내용:**
1. 현재 진행 중인 Lot 완료 확인
2. MES에서 장비 상태 변경
   ```
   [MES] → [Equipment] → [Status]
   → "PM Mode" 선택
   → Reason: "Pad Change"
   ```

3. CMP 시스템 정지
   - All platens → Stop
   - Slurry supply → OFF
   - DI water → Flush mode
   - Conditioner → Park position

4. LOTO (Lock-Out Tag-Out) 실행
   ```
   위치: Main power panel
   Lock 번호: ___________
   Tag 부착 시간: _______
   ```

**💡 Tip:** Platen 온도가 25°C 이하로 냉각 확인

### 4.2 Step 2: 기존 Pad 제거 (20분)

**작업 내용:**
1. Platen 상부 청소
   - Slurry 잔류물 제거
   - DI water로 충분히 rinse
   - 진공 흡입기로 물기 제거

2. Pad 고정 볼트 해제
   ```
   순서: 대각선 방향으로 교차
   1 → 3 → 2 → 4 (시계 반대방향)
   Torque: Loosen gradually
   ```

3. 기존 Pad 제거
   - 2인 1조로 들어올리기
   - Adhesive 잔류물 확인
   - 폐기물 지정 구역에 보관

**Check Point:**
- [ ] Platen 표면 손상 없음
- [ ] Adhesive 완전 제거
- [ ] 표면 평탄도 확인

### 4.3 Step 3: Platen 표면 준비 (15분)

**작업 내용:**
1. 표면 청소
   ```
   청소 순서:
   1) IPA 70%로 1차 세척
   2) DI water로 rinse
   3) Lint-free cloth로 건조
   4) 파티클 검사 (휴대용 라이트)
   ```

2. Adhesive 도포 준비
   - 표면 온도: 23 ± 2°C
   - 습도 확인: < 50% RH
   - Primer 도포 (필요시)

3. 평탄도 측정
   - Dial gauge 사용
   - 허용 범위: < 25µm across platen
   - 기록: _______µm

### 4.4 Step 4: 신규 Pad 설치 (25분)

**작업 내용:**
1. Pad 검수
   - [ ] 모델명 확인: __________
   - [ ] Lot number: __________
   - [ ] 유효기간: __________
   - [ ] 외관 검사 (찢어짐, 변색)

2. Pad 정렬 및 부착
   ```
   정렬 포인트:
   - Center alignment pin 확인
   - Template 사용하여 위치 결정
   - 한 번에 정확히 위치 (재조정 불가)
   ```

3. Pad 고정
   - 중앙부터 바깥쪽으로 기포 제거
   - 볼트 체결 (대각선 순서)
   - Torque: 15 N·m (단계적 체결)
   ```
   1차: 5 N·m
   2차: 10 N·m
   3차: 15 N·m (최종)
   ```

**💡 Tip:** Pad groove 방향이 slurry flow와 일치하는지 확인

### 4.5 Step 5: Conditioning 준비 (10분)

**작업 내용:**
1. Conditioner disk 교체
   - 기존 disk 제거
   - 신규 disk 장착 (Diamond grid 확인)
   - Pressure: 5 lbs 설정

2. Conditioning arm 정렬
   - Sweep 범위 설정
   - Oscillation 속도: 10 sweeps/min
   - Down force calibration

### 4.6 Step 6: Break-in Process (20분)

**작업 내용:**
1. Initial conditioning
   ```
   Recipe: PAD_BREAK_IN_01
   Duration: 10 minutes
   Pressure: 7 lbs
   Platen RPM: 30
   Oscillation: ON
   DI Flow: 500 ml/min
   ```

2. Slurry break-in
   ```
   Recipe: PAD_BREAK_IN_02
   Duration: 10 minutes
   Dummy wafers: 5 EA
   Slurry flow: 200 ml/min
   Process pressure: 4 psi
   ```

3. 표면 상태 확인
   - Visual inspection
   - Groove depth 측정
   - Uniformity check

---

## 5. 품질 확인

### 5.1 설치 후 검증

| 검사 항목 | 규격 | 측정값 | 판정 |
|----------|------|--------|------|
| Pad 평탄도 | < 50µm | ___µm | □ Pass □ Fail |
| Groove depth | 500 ± 50µm | ___µm | □ Pass □ Fail |
| 중심 정렬 | ± 1mm | ___mm | □ Pass □ Fail |
| 표면 결함 | 0 | ___ | □ Pass □ Fail |

### 5.2 Performance 확인

**Monitor wafer run (5매):**
- Removal rate: _______ Å/min (Target: 6000 ± 300)
- Non-uniformity: _______ % (Spec: < 3%)
- Defect adder: _______ ea (Spec: < 20 @ 0.16µm)

---

## 6. 시스템 재가동

### 6.1 재가동 체크리스트

- [ ] 모든 볼트 체결 확인
- [ ] Tool 제거 확인
- [ ] LOTO 해제
- [ ] Slurry line 연결
- [ ] DI water line 정상
- [ ] Conditioning program 설정
- [ ] Alarm 없음

### 6.2 MES 등록

```
[MES] → [PM Record] → [Pad Change]
입력 사항:
- Old pad run time: _______hrs
- New pad lot: _______
- Break-in completion: _______
- Qualification result: Pass/Fail
```

---

## 7. 이상 상황 대응

### 7.1 주요 이상 상황

| 상황 | 원인 | 조치 |
|------|------|------|
| Pad 들뜸 | 부적절한 부착 | 재설치 |
| 과도한 groove 마모 | Conditioning 과다 | Parameter 조정 |
| 불균일한 제거율 | 정렬 불량 | Pad 위치 재조정 |
| Scratch 발생 | Contamination | Pad 표면 청소 |

### 7.2 긴급 연락처

- CMP 엔지니어: 내선 7234
- 시설안전: 내선 7911
- Vendor 지원: 010-1234-5678

---

## 8. 폐기물 처리

### 8.1 폐Pad 처리
- 분류: 산업폐기물
- 보관: 지정 컨테이너 (B동 1층)
- 처리: 주 1회 외부 처리업체

### 8.2 Chemical 폐기물
- Slurry 잔류물: Chemical drain
- IPA wipes: 지정 폐기물통
- 폐 conditioner disk: 금속 재활용

---

## 9. 작업 완료 보고

### 9.1 Check Sheet 작성

```
작업일: ____/__/__ 시작: __:__ 종료: __:__
작업자: __________ 확인자: __________

주요 측정값:
□ Pad 두께: _____mils
□ Groove depth: _____µm
□ Removal rate: _____Å/min
□ Uniformity: _____%

특이사항:
_________________________________________

서명: _____________ 일시: ______________
```

---

**교육 이수 서명란:**

| 이름 | 사번 | 교육일 | 서명 |
|------|------|--------|------|
| | | | |
| | | | |

**문서 관리:** CMP 기술팀
**다음 개정:** 2025년 3월