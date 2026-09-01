// ============================================================================
//  psu-meter — 1순위 광학 벤치 인쇄 부품  (취미 제작용)
//  같이 볼 것: ../HOBBY_BUILD.md
//
//  ⚠ 이 파일은 OpenSCAD 에서 렌더 검증을 하지 못했습니다. 열어서 F5 로 보고
//    치수를 확인한 뒤 인쇄하십시오. 수치 자체는 src/illum_sim.py 계산값입니다.
//
//  좌표계 : 측정점 M = 원점
//           +X = 프리즘 현(60 mm) 방향
//           +Y = 프리즘 두께 방향.  Y=0 이 입사면 = 클램셸 분할면
//           +Z = 위(시료 쪽).  유리는 Z<0
//
//  ── 설계 근거 (src/illum_sim.py, src/segment_optics.py) ──────────────────
//    팔 각도(현 기준)               15.37 deg     두 팔 사이각 149.26 deg
//    광선이 곡면을 통과하는 자리    x = 22.43, z = -11.02 mm
//    ★ 외부 광선은 측정점을 지나지 않습니다 — 곡면에서 꺾이기 때문입니다.
//      그래서 팔 축은 위 통과점을 지나는 직선으로 정의합니다.
//    팔 250 mm 끝(검출기)           수평 241 mm, 아래 66 mm
//
//  ── 설계 방침 ────────────────────────────────────────────────────────────
//    소켓 대신 **평평한 접착면**을 씁니다. 취미 제작에서 훨씬 관대하고,
//    다이소 재료(우드락 덕트, 전선몰딩, 지관) 무엇이든 붙일 수 있습니다.
//    정밀해야 하는 것은 딱 하나 — **두 팔이 서로 움직이지 않는 것**이고,
//    그래서 허브를 한 몸으로 인쇄합니다.
// ============================================================================

PART = "preview";
//  "hub_a"    허브 반쪽 A  (분할면을 바닥에 놓고 인쇄 — 서포트 불필요)
//  "hub_b"    허브 반쪽 B
//  "clamp"    프리즘 누름쇠 (얹기만 해도 되지만 있으면 안정적)
//  "slit"     슬릿 클램프 아래쪽
//  "slit_lid" 슬릿 클램프 위쪽
//  "led"      LED + 확산판 홀더
//  "sensor"   TSL1401 모듈 받침
//  "baffle"   미광 차단 조리개 (팔마다 2~3개)
//  "preview"  조립 미리보기 (인쇄용 아님)

$fn = 90;

// ── 프리즘 : 사이언스트리 8종 반원렌즈 ──────────────────────────────────
P_CHORD = 60;    // 현
P_SAG   = 20;    // 사지타
P_THICK = 6;     // 두께 — 도착하면 실측해서 고치십시오
FIT     = 0.35;  // 포켓 편측 여유

P_R  = (pow(P_CHORD/2, 2) + pow(P_SAG, 2)) / (2*P_SAG);  // 32.5
P_CZ = P_SAG - P_R;                                       // -12.5

// ── 광학 ────────────────────────────────────────────────────────────────
ARM_DEG = 15.37;            // 팔이 측정면에서 아래로
EXIT_X  = 22.43;            // 광선이 곡면을 지나는 자리
EXIT_Z  = -11.02;
WIN_Z   = 9;                // 광창 높이(부채꼴 방향).  2도 + 여유
PAD_L   = 30;               // 접착 패드 길이
PAD_W   = 26;               // 접착 패드 폭 (Y)

// ── 허브 ────────────────────────────────────────────────────────────────
HUB_TOP = 3;                // 측정면 위로 남기는 살
HUB_X   = 132;              // 전체 X
HUB_Z   = 42;               // 측정면 아래로 파는 깊이
WALL    = 3.5;
HUB_Y   = P_THICK + 2*FIT + 2*WALL;
M3      = 3.4;
PEG_D   = 4;

// ============================================================================
//  기본 형상
// ============================================================================
module prism(f = 0) {
    intersection() {
        translate([0, 0, P_CZ]) rotate([-90, 0, 0])
            cylinder(h = P_THICK + 2*f, r = P_R + f, center = true);
        translate([0, 0, -(P_SAG + f)/2 - 0.5])
            cube([P_CHORD + 2*f + 2, P_THICK + 2*f + 0.02, P_SAG + f + 1], center = true);
    }
}

// 팔 축 위에서 작업. s = +1 오른쪽 / -1 왼쪽,  L = 곡면 통과점에서의 거리
module on_arm(s, L) {
    translate([s*(EXIT_X + L*cos(ARM_DEG)), 0, EXIT_Z - L*sin(ARM_DEG)])
        rotate([0, s*(90 + ARM_DEG), 0])
            children();
}

// 광로 : Y 는 프리즘 두께보다 좁게 유지해 포켓 측벽을 살린다
module beam(s, from, to) {
    on_arm(s, from)
        translate([0, 0, (to - from)/2])
            cube([WIN_Z, P_THICK - 0.5, to - from], center = true);
}

// ============================================================================
//  허브
// ============================================================================
module hub_solid() {
    union() {
        translate([0, 0, HUB_TOP - (HUB_Z + HUB_TOP)/2])
            cube([HUB_X, HUB_Y, HUB_Z + HUB_TOP], center = true);
        // 양쪽 접착 패드 — 팔 축에 수직한 평면
        for (s = [-1, 1])
            on_arm(s, 46) translate([0, 0, -PAD_L/2])
                cube([PAD_W, PAD_W, PAD_L], center = true);
    }
}

module hub_full() {
    difference() {
        hub_solid();

        // 프리즘 포켓 (위로 열림)
        prism(FIT);
        translate([0, 0, HUB_TOP/2 + 1])
            cube([P_CHORD + 2*FIT, P_THICK + 2*FIT, HUB_TOP + 3], center = true);

        // 측정면 창 — 액적을 올리고 눈으로 보는 자리
        translate([0, 0, HUB_TOP/2 + 1])
            cube([P_CHORD - 10, HUB_Y + 4, HUB_TOP + 3], center = true);

        // 광로 : 곡면 안쪽 2 mm 에서 패드 바깥까지
        for (s = [-1, 1]) beam(s, -2, 62);

        // 조립 M3
        for (x = [-52, -14, 14, 52]) translate([x, 0, -26])
            rotate([90, 0, 0]) cylinder(h = HUB_Y + 4, d = M3, center = true);
    }
}

module hub_half(side) {
    difference() {
        intersection() {
            hub_full();
            translate([0, side*40, 0]) cube([400, 80, 200], center = true);
        }
        if (side < 0)
            for (x = [-33, 33]) translate([x, 0, -14]) rotate([90, 0, 0])
                cylinder(h = 3*PEG_D, d = PEG_D + 0.3, center = true);
    }
    if (side > 0)
        for (x = [-33, 33]) translate([x, 0, PEG_D/2 - 0.01]) rotate([90, 0, 0])
            translate([0, 0, -14]) cylinder(h = PEG_D, d = PEG_D, center = true);
}

// 프리즘 누름쇠 — 측정면을 가리지 않게 양 끝만 누른다
module clamp() {
    difference() {
        cube([P_CHORD + 2*WALL, HUB_Y, 6], center = true);
        cube([P_CHORD - 10, HUB_Y + 2, 8], center = true);
        for (x = [-(P_CHORD/2 + 1.5), P_CHORD/2 + 1.5])
            translate([x, 0, 0]) cylinder(h = 8, d = M3, center = true);
    }
}

// ============================================================================
//  슬릿 클램프 — 커터칼 날 2장 + 종이 심
//    슬릿 폭 = 끼운 복사용지 장수 x 약 0.10 mm  (20장 두께를 재서 보정하십시오)
// ============================================================================
SC_X = 44; SC_Y = 34; SC_T = 6;
BLADE_T = 0.5; BLADE_W = 9;

module slit() {
    difference() {
        cube([SC_X, SC_Y, SC_T], center = true);
        // 날 두 장 자리 (Y 방향으로 마주보게)
        for (s = [-1, 1])
            translate([0, s*(BLADE_W/2 + 1.5), SC_T/2 - BLADE_T/2 + 0.01])
                cube([SC_X + 2, BLADE_W, BLADE_T + 0.04], center = true);
        // 광창
        cube([WIN_Z + 3, 3, SC_T + 2], center = true);
        for (x = [-SC_X/2 + 6, SC_X/2 - 6])
            translate([x, 0, 0]) cylinder(h = SC_T + 2, d = M3, center = true);
    }
}

module slit_lid() {
    difference() {
        cube([SC_X, SC_Y, 3], center = true);
        cube([WIN_Z + 3, 3, 5], center = true);
        for (x = [-SC_X/2 + 6, SC_X/2 - 6])
            translate([x, 0, 0]) cylinder(h = 5, d = M3, center = true);
    }
}

// ============================================================================
//  LED + 확산판 홀더 (팔 끝에 붙임)
// ============================================================================
LED_D = 5.25;
module led() {
    difference() {
        cube([PAD_W, PAD_W, 18], center = true);
        translate([0, 0, -9]) cylinder(h = 10, d = LED_D);   // LED 압입
        translate([0, 0, -10]) cylinder(h = 6, d = 2.8);     // 다리
        translate([0, 0, 2])  cube([PAD_W + 2, PAD_W + 2, 0.7], center = true); // 유산지
        translate([0, 0, 3])  cylinder(h = 14, d = WIN_Z + 2);
    }
}

// ============================================================================
//  TSL1401 받침 — 화소열이 입사면(Y=0) 안에 놓이도록 세워 끼운다
//    PCB 치수는 모듈 도착 후 실측해서 고치십시오
// ============================================================================
PCB_X = 30; PCB_T = 1.7;
module sensor() {
    difference() {
        cube([PCB_X + 14, PAD_W, 12], center = true);
        translate([0, 0, 3]) cube([PCB_X + 0.5, PCB_T + 0.4, 14], center = true);
        cube([14, PAD_W + 2, WIN_Z], center = true);
    }
}

// ── 미광 차단 조리개 : 팔 안에 2~3개. 가장 값싼 성능 향상 ────────────────
module baffle() {
    difference() {
        cube([PAD_W - 1.5, PAD_W - 1.5, 2], center = true);
        cube([WIN_Z, P_THICK, 4], center = true);
    }
}

// ============================================================================
module preview() {
    color("Silver", 0.30) hub_full();
    color("SkyBlue", 0.55) prism(0);
    for (s = [-1, 1]) {
        color("Orange", 0.35) beam(s, -2, 250);
        color("Gray", 0.25) on_arm(s, 46) translate([0, 0, -110])
            cube([PAD_W, PAD_W, 200], center = true);
    }
}

if      (PART == "hub_a")    hub_half(-1);
else if (PART == "hub_b")    hub_half(1);
else if (PART == "clamp")    clamp();
else if (PART == "slit")     slit();
else if (PART == "slit_lid") slit_lid();
else if (PART == "led")      led();
else if (PART == "sensor")   sensor();
else if (PART == "baffle")   baffle();
else                         preview();
