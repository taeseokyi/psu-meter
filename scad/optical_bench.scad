// ============================================================================
//  psu-meter — 1단계(수동) 측정 헤드 · 인쇄 부품
//  같이 볼 것: ../docs/head.html (도면·3D·이 상수를 뽑아 준다) · ../HOBBY_BUILD.md
//
//  2026-09-02 전면 재작성 — **허브 일체형**.
//  덕트·접착 패드·착탈 칼라·거울이 전부 없어졌습니다. 프리즘 포켓 · 관통 채널 ·
//  인쇄 조리개 · 조명 플러그 소켓 · 칩 포켓이 **본체 한 부품** 안에 있습니다.
//
//  치수는 docs/head.html 의 광선추적 계산값입니다. 실물 제작·측정은 아직 없습니다.
//
//  좌표계 : 측정점 M = 원점
//           +X = 프리즘 현(60 mm) 방향
//           +Y = 프리즘 두께 방향.  Y=0 이 입사면 = 클램셸 분할면
//           +Z = 위(시료 쪽).  유리는 Z<0
//
//  ── 반드시 알고 볼 것 ────────────────────────────────────────────────────
//  ★ 팔 길이는 **곡면 통과점 E** 에서 잽니다. 프리즘 중심이 아닙니다.
//    반원이라 주광선이 곡면을 0°로 지나므로 방향은 M 에서 나온 것과 같지만,
//    기준점은 E(26.93, -13.22) 입니다. 조명팔 40 의 끝은 중심에서 70 mm 입니다.
//
//  ★ 블록 깊이 HUB_Z 는 **프리즘이 아니라 내려가는 팔**이 정합니다.
//    팔이 26.15° 아래로 가므로 팔 끝(칩·플러그)이 프리즘 바닥보다 훨씬 깊습니다.
//    옛 식 ceil(사지타 + 2*벽 + 5) = 42 를 쓰면 검출 채널이 L=59.8 에서 블록
//    바닥을 뚫고 나가고 칩이 바로 L=60 입니다. head.html 의 "블록 깊이 검사" 행이
//    이것을 판정합니다. 형상을 바꾸면 그 표를 다시 보십시오.
//
//  ★ 정밀해야 하는 것은 딱 하나 — **두 팔이 서로 움직이지 않는 것**입니다.
//    그래서 본체를 한 몸으로 인쇄하고, 분할면(Y=0)을 바닥에 놓습니다.
// ============================================================================

/* [부품 선택] */
// OpenSCAD 의 Window > Customizer 를 켜면 아래가 드롭다운으로 나옵니다.
// 고르고 F5(미리보기) / F6(렌더) / F7(STL 내보내기).
PART = "preview"; // [preview:조립 미리보기 (인쇄용 아님), load:★ B 에 부품 얹는 자리 (조립 설명), hub_a:본체 반쪽 A (Y<0) — 분할면을 바닥에, hub_b:본체 반쪽 B (Y>0), base:받침대 — 바닥판+홈턱+힌지기둥+M4 3점, cap:차광 캡, slit_plug:조명측 플러그 (슬릿판), section:분할면 단면 (검증용), fitcheck:간섭 검사 (비어야 정상), thincheck:얇은 살 검사]

/* [Hidden] */

$fn = 180;

// ============================================================================
//  상수 — docs/head.html "SCAD 상수" 블록을 그대로 덮어쓰면 된다
// ============================================================================
// ── 프리즘 ─────────────────────────────────────
P_CHORD = 60;
P_SAG   = 30;
P_THICK = 10;      // 실물 도착하면 실측
FIT     = 0.35;
P_R     = 30.0000;
P_CZ    = 0.0000;

// ── 광학 ───────────────────────────────────────
ARM_DEG = 26.1525;
EXIT_X  = 26.9287;
EXIT_Z  = -13.2228;
WIN_Z   = 4.8;      // 부채꼴 4.5deg x 검출팔 60
ARM_I   = 40;       // 조명팔 — 끝이 슬릿
ARM_D   = 60;       // 검출팔 — 끝이 칩
REACH_I = 61;       // 조명측 부품 적재 총 도달
REACH_D = 72;       // 검출측
STOPS_I = [[30.2,1.37],[21,2.1],[12,2.8]];   // 조명측은 슬릿(L=ARM_I)에서 퍼진다 — 팔 끝에 가까울수록 좁다
STOPS_D = [[9.8,1.37],[19,2.1],[28,2.8]];    // 검출측은 측정점에서 퍼진다

// ── 부품 ───────────────────────────────────────
CHIP_L = 9.4; CHIP_W = 3; CHIP_H = 1.2;   // TSL1401CL CL 패키지
LED_D  = 5.25;
PLUG_W = 10; PLUG_Y = 10; PLUG_L = 20;   // 조명측 플러그

// ── 블록 ───────────────────────────────────────
HUB_TOP = 3;
HUB_L   = 93; HUB_R = 103;
HUB_Z   = 49;      // ★ 프리즘이 아니라 팔 끝이 정한다
WALL    = 3.5;  M3 = 3.4;

// ── 받침대 ─────────────────────────────────────
BASE_W = 220; BASE_D = 70; BASE_T = 6;
BASE_Z = -49;     // 바닥판 윗면 = 블록 바닥 (뜨지 않는다)
RAIL_LEN = 90; RAIL_T = 5; RAIL_H = 19;   // ★ 관통 M3 구멍 위로 살 4.3 mm. 15 면 0.30 mm 였다

// ============================================================================
//  유도값
// ============================================================================
HUB_Y  = P_THICK + 2*FIT + 2*WALL;               // 17.7  블록 두께
XP     = sqrt(pow(P_R + FIT, 2) - pow(P_CZ, 2)); // 30.35 포켓 입구 반폭
XW     = max(6, P_CHORD/2 - 5);                  // 25    측정창 반폭
CH_Y   = P_THICK - 0.5;                          // 9.5   채널 폭(두께 방향)
BAF_T  = 1.2;                                    //       인쇄 조리개 두께
BAF_AY = P_THICK - 2;                            // 8     조리개 개구 폭
SEAM   = 1.0;                                    //       분할면 랩 조인트 단차
PEG_D  = 4;
M4     = 4.4;

// 칩 자리 (설계 좌표) — 배선 슬롯을 여기서 옆으로 뺀다
CHIP_X = EXIT_X + ARM_D*cos(ARM_DEG);
CHIP_Z = EXIT_Z - ARM_D*sin(ARM_DEG);

// 조명측 플러그 캐비티의 바깥 끝 (설계 좌표) — 배선 슬롯을 여기서 옆으로 뺀다
PLUG_X = -(EXIT_X + (REACH_I + 2)*cos(ARM_DEG));
PLUG_Z = EXIT_Z - (REACH_I + 2)*sin(ARM_DEG);

// 조립 볼트 — 포켓도 광로도 피한 네 자리 (head.html g0.bolts 와 같은 식)
// 0.74 였을 때 오른쪽 볼트가 **배선 슬롯을 관통**했다 (단면 확인, 2026-09-02).
// 0.60 으로 올리면 검출측 슬롯 위 5.6 mm · 조명측 캐비티 위 3.4 mm 가 남는다.
BOLTS = [[-(HUB_L-6), -HUB_Z*0.60], [HUB_R-6, -HUB_Z*0.60],
         [-HUB_L*0.32, -(P_SAG+6)], [HUB_R*0.32, -(P_SAG+6)]];
// 아래 두 개는 홈턱까지 관통해 **본체를 받침대에 붙드는 볼트**를 겸한다 (M3 x 35)
RAIL_BOLTS = [BOLTS[2], BOLTS[3]];
XC = (HUB_R - HUB_L)/2;   // 블록 중심 x = 5

// ============================================================================
//  기본 형상
// ============================================================================

// 팔 축 위에서 작업.  s = +1 검출(오른쪽) / -1 조명(왼쪽),  L = E 에서의 거리
//   자식 좌표계 : +Z = 팔 진행 방향,  +X = 면내 수직,  +Y = 두께 방향
module on_arm(s, L) {
    translate([s*(EXIT_X + L*cos(ARM_DEG)), 0, EXIT_Z - L*sin(ARM_DEG)])
        rotate([0, s*(90 + ARM_DEG), 0])
            children();
}

// 프리즘 본체 (f = 편측 여유).  P_CZ 는 곡률 중심 — 반원이면 0 = 측정점
module prism(f = 0) {
    intersection() {
        translate([0, 0, P_CZ]) rotate([-90, 0, 0])
            cylinder(h = P_THICK + 2*f, r = P_R + f, center = true);
        translate([0, 0, -(P_SAG + f)/2 - 0.5])
            cube([P_CHORD + 2*f + 2, P_THICK + 2*f + 0.02, P_SAG + f + 1], center = true);
    }
}

// 블록 외형 단면 (XZ).  프리즘 포켓은 두께 방향으로 제한해야 하므로 여기서 빼지 않는다.
//   |x| < XW 의 윗면 홈이 **측정창**(액적 트레이)이고,
//   XW < |x| < XP 에 남는 살이 프리즘을 위에서 물어 준다 — 별도 누름쇠가 필요 없다.
module body_profile() {
    polygon([[-HUB_L, -HUB_Z], [HUB_R, -HUB_Z], [HUB_R, HUB_TOP],
             [XW, HUB_TOP], [XW, 0], [-XW, 0], [-XW, HUB_TOP], [-HUB_L, HUB_TOP]]);
}

module body_solid() {
    rotate([90, 0, 0]) linear_extrude(height = HUB_Y, center = true) body_profile();
}

// 광로 채널 : from ~ to (팔 축 L).  Y 는 프리즘 두께보다 좁게 유지해 측벽을 살린다
module channel(s, from, to) {
    on_arm(s, (from + to)/2)
        cube([WIN_Z, CH_Y, to - from], center = true);
}

// 인쇄 조리개 — 채널을 뚫은 뒤 **다시 채워 넣는** 얇은 판.
//   개구가 국소 빔 폭에 맞춰 커진다. 따로 끼울 부품이 없고 비용도 0.
module baffle(s, L, ap) {
    on_arm(s, L) difference() {
        cube([WIN_Z, CH_Y, BAF_T], center = true);
        cube([ap, BAF_AY, BAF_T + 1], center = true);
    }
}

module baffles() {
    for (t = STOPS_D) baffle( 1, t[0], t[1]);
    for (t = STOPS_I) baffle(-1, t[0], t[1]);
}

// ============================================================================
//  본체 (두 반쪽을 합친 온전한 형상)
// ============================================================================
module body_full() {
    union() {
        difference() {
            body_solid();

            // 프리즘 포켓 — 두께 방향으로 제한된다 (측벽이 남아야 한다)
            prism(FIT);

            // 광로 : 곡면 안쪽 2 mm 에서 팔 끝까지
            channel( 1, -2, ARM_D);
            channel(-1, -2, ARM_I);

            // 조명측 플러그 소켓 — 슬릿판/렌즈판을 갈아끼우는 자리
            on_arm(-1, (ARM_I + REACH_I + 2)/2)
                cube([PLUG_W, PLUG_Y, REACH_I + 2 - ARM_I], center = true);

            // 칩 포켓 — 어레이 8.064 의 길이 방향이 부채꼴 방향(면내)에 오게 눕힌다
            on_arm(1, ARM_D + (CHIP_H + 0.3)/2)
                cube([CHIP_L + 0.4, CHIP_W + 0.4, CHIP_H + 0.3], center = true);

            // 배선 슬롯 — 칩 뒤에서 **오른쪽 끝면으로** 수평으로 뺀다.
            //   축을 따라 뒤로 빼면 블록이 3 mm 더 깊어지고, 바닥으로 빼면 받침대에 눌린다.
            translate([(CHIP_X + HUB_R + 1)/2, 0, CHIP_Z])
                cube([HUB_R + 1 - CHIP_X, 6, 6], center = true);

            // LED 배선 슬롯 — 플러그 캐비티 끝에서 **왼쪽 끝면으로** 수평으로.
            //   캐비티를 축 방향으로 끝면까지 뚫으면 팔이 내려가는 만큼 블록이
            //   5 mm 더 깊어진다. 플러그는 분할면에서 넣으므로 뚫을 필요가 없다.
            translate([(PLUG_X - HUB_L - 1)/2, 0, PLUG_Z])
                cube([PLUG_X + HUB_L + 1, 6, 6], center = true);

            // 조립 M3
            for (p = BOLTS)
                translate([p[0], 0, p[1]]) rotate([90, 0, 0])
                    cylinder(h = HUB_Y + 4, d = M3, center = true);
        }
        baffles();
    }
}

// ── 분할 ─────────────────────────────────────────────────────────────────
//  ★ 분할면은 광로 한가운데를 196 mm 내내 지나간다. 평평한 면끼리 맞대면
//    그 이음매가 검출기까지 직통하는 **빛 새는 틈**이 된다.
//    그래서 채널 둘레에서만 분할면을 한 단(SEAM) 옮겨 랩 조인트를 만든다.
module seam_claim(clr = 0) {
    for (s = [-1, 1])
        let (reach = (s > 0) ? REACH_D : REACH_I)
            on_arm(s, (reach - 2)/2)
                translate([0, -SEAM/2, 0])
                    cube([WIN_Z + 8 + 2*clr, SEAM + 2*clr, reach + 2 + 2*clr], center = true);
}

// B(Y>0) 가 가져가는 영역
module claim_b(clr = 0) {
    union() {
        translate([0, 200, 0]) cube([600, 400, 400], center = true);
        seam_claim(clr);
    }
}

PEGS = [[-60, -44], [70, -44]];

module hub_half(side) {
    difference() {
        if (side > 0) intersection() { body_full(); claim_b(0); }
        else          difference()   { body_full(); claim_b(0.2); }

        // A 쪽에 페그 구멍
        if (side < 0)
            for (p = PEGS) translate([p[0], -PEG_D/2, p[1]])
                rotate([90, 0, 0]) cylinder(h = PEG_D + 0.4, d = PEG_D + 0.3, center = true);
    }
    // B 쪽에 페그 — 분할면에서 A 쪽(Y<0)으로 튀어나간다
    if (side > 0)
        for (p = PEGS) translate([p[0], -PEG_D/2 + 0.01, p[1]])
            rotate([90, 0, 0]) cylinder(h = PEG_D, d = PEG_D, center = true);
}

// ============================================================================
//  받침대 — 바닥판 + 홈턱 + 힌지 기둥 + M4 수평조절 3점
//    ★ 블록 바닥이 바닥판 윗면에 **닿는다**. 옛 배치는 1 mm 떠 있어서 수직
//      기준면이 없었다 — 홈턱 옆면만으로는 뚜껑 닫는 힘에 흔들린다.
//    ★ 홈턱은 블록의 **두께 방향**으로 벌어진다. 가운데 M3 두 개가 홈턱-블록-홈턱을
//      관통해 본체를 붙든다 (M3 x 35). 새 나사가 늘지 않는다.
// ============================================================================
FEET = [[-88.2, BASE_D*0.34], [XC, -BASE_D*0.34], [96.6, BASE_D*0.34]];

module base() {
    difference() {
        union() {
            // 바닥판 — 충진을 아끼지 말 것. 무게가 곧 안정성이다.
            translate([XC, 0, BASE_Z - BASE_T/2])
                cube([BASE_W, BASE_D, BASE_T], center = true);
            // 홈턱 2줄
            for (sd = [-1, 1])
                translate([XC, sd*(HUB_Y/2 + RAIL_T/2 + 0.3), BASE_Z + RAIL_H/2])
                    cube([RAIL_LEN, RAIL_T, RAIL_H], center = true);
        }
        // 홈턱 관통 M3 (본체 고정 겸용)
        for (p = RAIL_BOLTS)
            translate([p[0], 0, p[1]]) rotate([90, 0, 0])
                cylinder(h = BASE_D + 4, d = M3, center = true);
        // M4 수평조절 3점 — 삼각 지지라 덜컹거리지 않는다
        for (f = FEET)
            translate([f[0], f[1], BASE_Z - BASE_T/2])
                cylinder(h = BASE_T + 2, d = M4, center = true);
    }
}

// ============================================================================
//  차광 캡 — **상부 전체를 덮는 슈라우드**.  힌지 없음. 들어서 벗기고 덮는다.
//
//  2026-09-02 : 힌지 달린 작은 뚜껑에서 이것으로 바꿨다. 이유가 두 개다.
//   (1) 차광 — 배선 슬롯이 블록의 **양 끝면에 열려** 있고, 검출측 슬롯은 칩 포켓에
//       바로 이어진다. 위만 덮으면 그 구멍으로 외광이 곧장 검출기에 든다.
//       시료 쪽 외광은 검출기의 어두운 쪽만 비대칭으로 채워 경계를 밀어낸다(§5-1).
//   (2) 하중 — 네 벽이 **바닥판에 직접 내려앉아** 블록을 아예 건드리지 않는다.
//       힌지도, 61 mm 기둥도 없다. 프리즘-칩 사이를 휘게 할 경로 자체가 없어졌다.
//       (검출팔 60 mm 에서 칩이 1 µm 미끄러지면 0.061 PSU)
//
//  ★ 내면은 무광 검정으로. 이것이 이 장치의 차광 본체다.
//  ★ 인쇄는 열린 면을 위로(천장을 바닥에) 놓는다 — 서포트가 필요 없다.
// ============================================================================
COV_T   = 2;                  // 벽 두께
COV_CLR = 2;                  // 블록과의 편측 여유 (X)
COV_HY  = 19;                 // 안쪽 반폭. 홈턱(14.15)과 가운데 M3 머리(약 16.7)를 넘겨야 한다
COV_TOP = HUB_TOP + 3;        // 안쪽 천장 z = 6
COV_NW  = 10;                 // 배선 노치 폭
COV_NZ  = -36;                // 배선 노치 윗변 — 슬롯(-44~-36.7)보다 위
//  ★ 노치를 y=0 에 두면 안 된다. 블록의 배선 슬롯이 y=0 을 중심으로 +-3 이라
//    노치와 **일직선으로 뚫려** 외광이 곧장 칩까지 든다. 옆으로 비켜 놓으면
//    선은 구부러져 나가고 빛은 직선으로 못 들어온다.
COV_NY  = 12;                 // 노치 중심 y (슬롯의 +-3 과 겹치지 않는다)

module cap() {
    xi0 = -(HUB_L + COV_CLR);          // 안쪽 x 범위
    xi1 =   HUB_R + COV_CLR;
    xc  = (xi0 + xi1)/2;
    xw  = xi1 - xi0;
    difference() {
        translate([xc, 0, (BASE_Z + COV_TOP + COV_T)/2])
            cube([xw + 2*COV_T, 2*(COV_HY + COV_T), COV_TOP + COV_T - BASE_Z], center = true);
        // 속 — 아래로 열린다
        translate([xc, 0, (BASE_Z - 1 + COV_TOP)/2])
            cube([xw, 2*COV_HY, COV_TOP - BASE_Z + 1], center = true);
        // 배선 노치 — 양 끝벽에 아래로 열린 슬롯. 다리를 밖으로 뺀다.
        //   ★ y=0 에서 비켜 놓아 블록의 배선 슬롯과 **직선으로 통하지 않게** 한다.
        for (x = [xi0, xi1])
            translate([x, COV_NY, (BASE_Z - 1 + COV_NZ)/2])
                cube([2*COV_T + 2, COV_NW, COV_NZ - BASE_Z + 1], center = true);
    }
}

// ============================================================================
//  조명측 플러그 — 슬릿판.  **분할면에서 떨어뜨려 넣는다** (축으로 밀어 넣지 않는다)
//    축으로 밀어 넣으려면 캐비티를 끝면까지 뚫어야 하는데, 팔이 26° 내려가므로
//    그러면 블록이 5 mm 더 깊어진다. 클램셸이라 그럴 필요가 없다.
//
//    슬릿 폭 = 끼운 복사용지 장수 x 약 0.10 mm.  권장 0.19 mm (1~2장)
//    ★ 집광형 LED 는 경계 자체를 만들지 못한다. 돔을 사포로 갈아 평평하게 + 유산지 확산판.
//    렌즈 안(배치 A)으로 판정이 나면 **이 부품만 새로 뽑는다** — 본체는 그대로.
//
//    인쇄 : 9.7 x 9.7 끝면을 바닥에 놓고 세워서. 날·확산판 슬롯은 0.5~0.7 mm 다리이고
//           LED 구멍은 수직이 되어 서포트가 필요 없다.
// ============================================================================
BLADE_T = 0.5; BLADE_W = 9;
PLUG_CLR = 0.3;                       // 캐비티 대비 편측 여유
PLUG_LEN = REACH_I + 2 - ARM_I - 0.4; // 22.6

module slit_plug() {
    difference() {
        translate([0, 0, PLUG_LEN/2])
            cube([PLUG_W - PLUG_CLR, PLUG_Y - PLUG_CLR, PLUG_LEN], center = true);

        // 슬릿 광창 — 안쪽 끝면에서 날 자리까지만. 이것이 광원의 실제 개구다.
        translate([0, 0, 0.5]) cube([WIN_Z, CH_Y, 2.2], center = true);

        // 커터칼 날 2장 자리 — 양쪽에서 밀어 넣어 마주보게. 심으로 폭을 맞춘다.
        translate([0, 0, 1.6 + BLADE_T/2])
            cube([PLUG_W + 2, BLADE_W, BLADE_T + 0.05], center = true);

        // 유산지 확산판 슬롯
        translate([0, 0, 3.4]) cube([PLUG_W + 2, PLUG_Y + 2, 0.7], center = true);

        // 확산판과 LED 사이 공동
        translate([0, 0, (3.75 + 12.6)/2]) cube([7, 7, 12.6 - 3.75], center = true);

        // LED 압입 (바깥 끝에서 넣는다) + 다리 관통
        translate([0, 0, PLUG_LEN + 0.1]) rotate([180, 0, 0]) cylinder(h = 10.2, d = LED_D);
        translate([0, 0, PLUG_LEN + 0.1]) rotate([180, 0, 0]) cylinder(h = 12,   d = 2.8);
    }
}

// ============================================================================
//  조립 설명 — **반쪽 B 가 부품을 싣는 쪽**이다.
//    분할면의 랩 조인트(SEAM)가 채널 둘레에서 B 쪽으로 1 mm 넘어와 있으므로
//    B 의 홈이 더 깊다 : 플러그 6 mm (A 는 4) · 칩 2.7 mm (A 는 0.7).
//    그래서 B 를 분할면이 위로 오게 눕혀 놓고 **떨어뜨려 얹은 뒤** A 를 덮는다.
//    밀어 넣는 것이 아니다 — 어느 쪽으로도 뚫려 있지 않다.
// ============================================================================
CHIP_ARR = 8.064;   // 어레이 길이. 데이터시트 Figure 10

// TSL1401CL 이 놓이는 자세 — 어레이 길이 방향이 **부채꼴 방향(면내)**
module chip() {
    on_arm(1, ARM_D + CHIP_H/2 + 0.15) {
        color("#14181C") cube([CHIP_L, CHIP_W, CHIP_H], center = true);
        // 수광창 : 프리즘을 바라보는 면에 있다
        color("#6FC8F0") translate([0, 0, -CHIP_H/2 - 0.06])
            cube([CHIP_ARR, 0.8, 0.12], center = true);
    }
}

module loaded_b() {
    color("Silver", 0.55) hub_half(1);
    color("Tomato", 0.85) on_arm(-1, ARM_I) slit_plug();
    chip();
    color("SkyBlue", 0.35) prism(0);
}

// ============================================================================
//  얇은 살 검사 — 단면에서 **THIN*2 보다 얇은 살**만 남겨 보여 준다.
//    열림(줄였다 늘리기)은 얇은 것을 지운다. 원본에서 그걸 빼면 얇은 데만 남는다.
//    이 프로젝트에서 같은 실수가 세 번 났다 (전부 이 검사에 걸렸을 것들이다) :
//      · 검출 채널이 블록 바닥을 0.07 mm 뚫음
//      · 힌지 기둥 꼭대기가 핀 구멍과 같은 높이 (구멍이 아니라 홈)
//      · 홈턱 관통 M3 구멍 위 살 0.30 mm
//
//    ⚠ **볼록한 모서리는 원래 걸린다** (열림이 모서리를 둥글리기 때문). 개수가 아니라
//      **면적**으로 판단할 것. 지금 남는 것은 전부 의도한 것이다 :
//        · 12.7 mm² x=±27 z=+1.5  — 측정창 턱(프리즘을 무는 살). 두께 HUB_TOP=3
//        · 1.0~2.0 mm² x6 쌍      — 인쇄 조리개의 어깨. 설계상 1.0~1.7 mm
//        · 2.3 / 1.0 mm² x=-83~-86 — 플러그 캐비티와 LED 배선 슬롯이 만나는 쐐기, 1.8 mm
//      **이 목록에 없는 것이 나오면 그것이 버그다.**
// ============================================================================
THIN = 1.5;   // 반경. 2*THIN = 3 mm 미만이 잡힌다

module thin_of() {
    difference() {
        children();
        offset(r = THIN) offset(r = -THIN) children();
    }
}

module thincheck() {
    // 본체 — 분할면 단면
    thin_of() projection(cut = true) rotate([-90, 0, 0]) body_full();
    // 받침대 — 홈턱을 지나는 단면
    thin_of() projection(cut = true) rotate([-90, 0, 0])
        translate([0, HUB_Y/2 + RAIL_T/2 + 0.3, 0]) base();
}

// ============================================================================
module preview() {
    color("Silver",  0.35) body_full();
    color("SkyBlue", 0.55) prism(0);
    color("Gray",    0.60) base();
    color("Tan",     0.45) cap();
    color("Tomato",  0.70) on_arm(-1, ARM_I) slit_plug();
}

if      (PART == "hub_a")     hub_half(-1);
else if (PART == "hub_b")     hub_half(1);
else if (PART == "base")      base();
else if (PART == "cap")       cap();
else if (PART == "slit_plug") slit_plug();
// 검증용 : 분할면(Y=0) 단면. docs/head.html "도면 2" 와 대조한다.
//   openscad --backend=manifold -o section.dxf -D "PART=\"section\"" optical_bench.scad
else if (PART == "section")   projection(cut = true) rotate([-90, 0, 0]) body_full();
else if (PART == "load")      loaded_b();
// 검증용 : 닫힌 자세에서 받침대와 캡이 서로 파고드는지. **비어 있어야 한다.**
//   openscad -o fit.stl -D "PART=\"fitcheck\"" optical_bench.scad
//   -> "Current top level object is empty" 가 나오면 간섭 없음.
else if (PART == "fitcheck")  intersection() { cap(); union() { base(); body_full(); } }
else if (PART == "thincheck") thincheck();
else                          preview();
