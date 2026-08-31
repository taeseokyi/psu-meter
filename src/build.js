const pptxgen = require('pptxgenjs');
const fs = require('fs');

const P = { deep:'065A82', teal:'1C7293', mid:'21295C', amb:'E8901F',
            ink:'1A2430', grey:'78899A', card:'F2F7FA', line:'D8E3EA',
            white:'FFFFFF', red:'B4453C', violet:'7B4FA8' };
const F = 'Arial';
const W = 13.3, H = 7.5;

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';
pres.author = 'KISTI RDC';
pres.title  = '해수 수조 광학식 염도 측정 시스템';

// ---------- helpers ----------
function titleSlide(s, kicker, title, sub) {
  s.background = { color: P.mid };
  s.addText(kicker, { x:0.9, y:1.75, w:11.5, h:0.35, fontSize:14, color:'8FB8CE',
    fontFace:F, charSpacing:2, isTextBox:true, margin:0 });
  s.addText(title, { x:0.9, y:2.2, w:11.5, h:1.5, fontSize:40, bold:true, color:P.white,
    fontFace:F, lineSpacing:46, isTextBox:true, margin:0 });
  s.addText(sub, { x:0.9, y:3.85, w:11.0, h:1.4, fontSize:15, color:'B9D3E2',
    fontFace:F, lineSpacing:26, isTextBox:true, margin:0 });
}
function head(s, t, sub) {
  s.addText(t, { x:0.62, y:0.38, w:12.1, h:0.55, fontSize:28, bold:true, color:P.mid,
    fontFace:F, isTextBox:true, margin:0 });
  if (sub) s.addText(sub, { x:0.62, y:0.97, w:12.1, h:0.42, fontSize:12.5, color:P.grey,
    fontFace:F, isTextBox:true, margin:0 });
}
function card(s, x, y, w, h, fill) {
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h, fill:{ color: fill || P.card },
    line:{ color:P.line, width:1 }, rectRadius:0.06 });
}
function statCard(s, x, y, w, h, value, label, note, col) {
  card(s, x, y, w, h);
  s.addText(value, { x:x+0.22, y:y+0.20, w:w-0.44, h:0.66, fontSize:30, bold:true,
    color: col || P.deep, fontFace:F, isTextBox:true, margin:0 });
  s.addText(label, { x:x+0.22, y:y+0.88, w:w-0.44, h:0.34, fontSize:12.5, bold:true,
    color:P.ink, fontFace:F, isTextBox:true, margin:0 });
  if (note) s.addText(note, { x:x+0.22, y:y+1.24, w:w-0.44, h:h-1.42, fontSize:10.5,
    color:P.grey, fontFace:F, lineSpacing:16, isTextBox:true, margin:0 });
}
function numRow(s, x, y, w, n, title, body, col) {
  s.addShape(pres.ShapeType.ellipse, { x, y:y+0.03, w:0.34, h:0.34,
    fill:{ color: col || P.amb }, line:{ color: col || P.amb, width:0 } });
  s.addText(String(n), { x, y:y+0.03, w:0.34, h:0.34, fontSize:12, bold:true,
    color:P.white, align:'center', valign:'middle', fontFace:F, isTextBox:true, margin:0 });
  s.addText(title, { x:x+0.5, y:y, w:w-0.5, h:0.32, fontSize:13.5, bold:true, color:P.ink,
    fontFace:F, isTextBox:true, margin:0 });
  s.addText(body, { x:x+0.5, y:y+0.33, w:w-0.5, h:0.9, fontSize:11.5, color:P.grey,
    fontFace:F, lineSpacing:17, isTextBox:true, margin:0 });
}
function tbl(s, x, y, w, rows, colW, opts) {
  const o = opts || {};
  s.addTable(rows, { x, y, w, colW, fontFace:F, fontSize: o.fs || 11.5,
    color:P.ink, border:{ type:'solid', color:P.line, pt:0.75 },
    fill:{ color:P.white }, valign:'middle', rowH: o.rowH || 0.34,
    margin: o.margin === undefined ? 0.07 : o.margin });
}
const th = (t) => ({ text:t, options:{ bold:true, color:P.white, fill:{ color:P.deep }, fontSize:11.5 } });
const mono = (t) => ({ text:t, options:{ fontFace:'Courier New', fontSize:10.5 } });

// ============================================================ 1 title
{
  const s = pres.addSlide();
  titleSlide(s, '설계 문서   ·   2026',
    '해수 수조 광학식 염도 측정 시스템',
    '임계각 굴절계 방식  ·  34 PSU 자동 모니터링  ·  하루 2회 무인 측정\nBK7 반원통 렌즈 + 단색 LED + TSL1401 리니어 어레이 + 매 사이클 2점 자가보정');
  s.addShape(pres.ShapeType.ellipse, { x:0.9, y:5.55, w:0.13, h:0.13, fill:{ color:P.amb }, line:{ width:0 } });
  s.addText('취미용 부품으로 만드는 실험실급 구조', { x:1.18, y:5.42, w:8, h:0.38,
    fontSize:13, color:P.amb, bold:true, fontFace:F, isTextBox:true, margin:0 });
  s.addNotes('전체 설계의 핵심은 매 측정 사이클마다 RO-DI와 표준액 두 점으로 자가보정을 수행해, 온도·LED 파장·광량·기구 드리프트를 모두 상쇄시키는 것입니다.');
}

// ============================================================ 2 목표와 요구 정밀도
{
  const s = pres.addSlide();
  head(s, '목표와 요구 정밀도', '염도는 굴절률로 환산해 측정합니다. 먼저 얼마나 정밀해야 하는지부터 확인합니다.');
  statCard(s, 0.62, 1.62, 2.92, 2.05, '1.81×10⁻⁴', '염도 1 PSU 당 굴절률 변화',
    '해수 굴절률 경험식(OSU)에서\n26 °C, 590 nm 기준으로 계산', P.deep);
  statCard(s, 3.72, 1.62, 2.92, 2.05, '1 / 14,800', '±0.5 PSU 를 위한 분해능',
    'Δn ≈ 9.1×10⁻⁵ 을 읽어야 함.\n굴절률의 1만 5천분의 1 수준', P.teal);
  statCard(s, 6.82, 1.62, 2.92, 2.05, '0.667', '온도 1 °C 당 PSU 오차',
    '절대 측정 시. 온도가 정밀도를\n좌우하는 가장 큰 변수', P.red);
  statCard(s, 9.92, 1.62, 2.76, 2.05, '0.19', '파장 1 nm 당 PSU 오차',
    '분산(dispersion) 때문.\n광원 선택이 설계를 결정', P.amb);

  card(s, 0.62, 3.95, 12.06, 2.62, P.mid);
  s.addText('이 세 숫자가 설계 전체를 결정합니다', { x:0.92, y:4.16, w:11.4, h:0.4,
    fontSize:16, bold:true, color:P.white, fontFace:F, isTextBox:true, margin:0 });
  const rows = [
    ['광학 방식', '임계각(critical angle) 방식만이 요구 감도를 만족 — 상용 디지털 굴절계와 동일 원리'],
    ['광원', '백색 LED는 그림자 경계가 28 PSU 폭으로 뭉개져 사용 불가 → 단색 LED 필수'],
    ['온도', '절대 측정으로는 불가능. 표준액과 시료를 같은 온도에서 재고 차분 → 0.0015 PSU/°C 로 감소'],
  ];
  let yy = 4.72;
  rows.forEach(([k, v]) => {
    s.addText(k, { x:0.92, y:yy, w:1.6, h:0.34, fontSize:12.5, bold:true, color:P.amb,
      fontFace:F, isTextBox:true, margin:0 });
    s.addText(v, { x:2.6, y:yy, w:9.75, h:0.44, fontSize:12, color:'D5E4EE',
      fontFace:F, lineSpacing:16, isTextBox:true, margin:0 });
    yy += 0.6;
  });
  s.addNotes('요구 분해능 자체보다 온도와 광원 파장이 더 큰 문제라는 점이 이 설계의 출발점입니다.');
}

// ============================================================ 3 임계각 원리
{
  const s = pres.addSlide();
  head(s, '구조와 원리 —  임계각 굴절계', '프리즘·시료 경계에서 전반사가 시작되는 각도를 읽어 굴절률을 구합니다.');
  s.addImage({ path:'fig_optics.png', x:0.62, y:1.48, w:12.06, h:4.98 });
  s.addNotes('LED는 부채꼴 광선속으로 측정면 한 점에 모여야 합니다. 단일 평행광이면 각도 분포가 없어 경계선 자체가 생기지 않습니다.');
}

// ============================================================ 4 광학 부품 선택
{
  const s = pres.addSlide();
  head(s, '왜 BK7 인가,  왜 단색 LED 인가', '두 가지 선택이 감도와 측정 범위를 결정합니다.');

  s.addText('프리즘 —  굴절률이 낮을수록 민감', { x:0.62, y:1.5, w:5.9, h:0.35,
    fontSize:15, bold:true, color:P.deep, fontFace:F, isTextBox:true, margin:0 });
  tbl(s, 0.62, 1.95, 5.9, [
    [th('유리'), th('임계각'), th('감도'), th('평가')],
    ['BK7  n=1.5168', '61.93°', '253 µrad/PSU', { text:'채택', options:{ bold:true, color:P.deep } }],
    ['SF계  n=1.72', '51.09°', '167 µrad/PSU', { text:'−34 %', options:{ color:P.grey } }],
  ], [1.85, 1.1, 1.55, 1.4], { rowH:0.42 });
  s.addText('임계각이 클수록 cos θc 가 작아져 각도 변화가 증폭됩니다.\n비싼 고굴절 유리가 오히려 불리하다는 반가운 결과입니다.\n형상은 반원통(hemicylinder) — 곡면으로 들어온 빛이 중심을\n향하면 굴절 없이 통과해 광로 계산이 단순해집니다.',
    { x:0.62, y:3.28, w:5.9, h:1.1, fontSize:11.5, color:P.ink, fontFace:F,
      lineSpacing:18, isTextBox:true, margin:0 });

  s.addText('광원 —  스펙트럼 폭이 곧 경계 번짐', { x:6.78, y:1.5, w:5.9, h:0.35,
    fontSize:15, bold:true, color:P.amb, fontFace:F, isTextBox:true, margin:0 });
  tbl(s, 6.78, 1.95, 5.9, [
    [th('광원'), th('스펙트럼 폭'), th('경계 번짐'), th('평가')],
    ['백색 LED', '≈ 150 nm', '≈ 28 PSU', { text:'사용 불가', options:{ bold:true, color:P.red } }],
    ['단색 LED', '≈ 20 nm', '≈ 3.8 PSU', { text:'채택', options:{ bold:true, color:P.deep } }],
    ['레이저 다이오드', '< 1 nm', '≈ 0.2 PSU', { text:'스페클 노이즈', options:{ color:P.grey } }],
  ], [1.85, 1.25, 1.35, 1.45], { rowH:0.42 });
  s.addText('백색 LED는 경계선이 측정 범위 전체를 덮어버려 아무것도 읽을 수\n없습니다. 레이저는 경계가 날카롭지만 스페클이 위치 검출에\n랜덤 노이즈로 들어와 오히려 불리합니다.',
    { x:6.78, y:3.72, w:5.9, h:0.9, fontSize:11.5, color:P.ink, fontFace:F,
      lineSpacing:18, isTextBox:true, margin:0 });

  card(s, 0.62, 4.72, 12.06, 1.62, '#FDF4E8');
  s.addText('덤으로 얻는 것', { x:0.92, y:4.9, w:3, h:0.32, fontSize:13, bold:true,
    color:'8A5A15', fontFace:F, isTextBox:true, margin:0 });
  s.addText('20 nm LED 의 자연스러운 경계 번짐 폭 3.8 PSU 는, 34 PSU 를 중심으로 ±2 PSU 를 덮습니다. 리프 수조가 실제로 머무는 범위와 정확히 일치합니다.\n즉 광원 선택이 측정 범위까지 알아서 맞춰준 셈입니다. (2분할 포토다이오드 방식을 쓸 경우 이 폭이 그대로 선형 구간이 됩니다.)',
    { x:0.92, y:5.26, w:11.5, h:0.92, fontSize:12, color:P.ink, fontFace:F,
      lineSpacing:18, isTextBox:true, margin:0 });
}

// ============================================================ 5 검출기 + 검량선
{
  const s = pres.addSlide();
  head(s, '검출기 —  TSL1401CL 리니어 어레이', '128 픽셀 × 63.5 µm.  250 mm 검출팔에서 1 픽셀이 곧 1 PSU가 됩니다.');
  s.addImage({ path:'fig_cal.png', x:0.62, y:1.42, w:8.35, h:4.35 });

  const items = [
    ['왜 어레이인가', '2분할 포토다이오드는 34 PSU 밖의 RO-DI 를 볼 수 없어 1점 보정만 가능합니다.'],
    ['왜 TSL1401 인가', 'TCD1304 는 1~4 MHz ADC 가 필요해 아두이노로는 불가. TSL1401 은 클럭이 느려 나노로도 충분합니다.'],
    ['정렬이 쉬워짐', '8 mm 어레이 어디에 맺혀도 소프트웨어가 경계를 찾습니다. 0.1 mm 기구 정밀도가 불필요합니다.'],
  ];
  let yy = 1.62;
  items.forEach(([t, b], i) => { numRow(s, 9.28, yy, 3.55, i+1, t, b); yy += 1.5; });
  s.addNotes('서브픽셀 에지 피팅으로 1/20 픽셀까지 읽으면 0.05 PSU 분해능이 나옵니다.');
}

// ============================================================ 6 자가보정 (핵심)
{
  const s = pres.addSlide();
  s.background = { color: P.mid };
  s.addText('핵심 구조', { x:0.62, y:0.42, w:5, h:0.32, fontSize:13, color:P.amb,
    bold:true, charSpacing:2, fontFace:F, isTextBox:true, margin:0 });
  s.addText('오차가 통째로 상쇄됩니다', { x:0.62, y:0.8, w:12.1, h:0.6, fontSize:30,
    bold:true, color:P.white, fontFace:F, isTextBox:true, margin:0 });
  s.addText('표준액과 시료를 같은 셀에서, 같은 온도로, 몇 초 간격으로 재고 그 차이만 씁니다. 그러면 느리게 변하는 오차원은 두 측정에 똑같이 실려 차분에서 지워집니다.',
    { x:0.62, y:1.44, w:12.1, h:0.5, fontSize:13, color:'B9D3E2', fontFace:F,
      lineSpacing:19, isTextBox:true, margin:0 });

  const rows = [
    [{ text:'오차원', options:{ bold:true, color:P.white, fill:{ color:'2E3A6B' } } },
     { text:'절대 측정 시', options:{ bold:true, color:P.white, fill:{ color:'2E3A6B' } } },
     { text:'차분 측정 시', options:{ bold:true, color:P.white, fill:{ color:'2E3A6B' } } },
     { text:'개선', options:{ bold:true, color:P.white, fill:{ color:'2E3A6B' } } }],
    ['온도', '0.667 PSU / °C', { text:'0.0015 PSU / °C', options:{ bold:true, color:'7FD4A8' } }, '450 배'],
    ['LED 파장 드리프트', '0.19 PSU / nm', { text:'거의 0', options:{ bold:true, color:'7FD4A8' } }, '수 초 간격이면 무시'],
    ['LED 광량 · 검출기 게인', '직접 영향', { text:'0', options:{ bold:true, color:'7FD4A8' } }, '비율 연산으로 제거'],
    ['기구 열팽창 (250 mm Al)', '0.091 PSU / °C', { text:'거의 0', options:{ bold:true, color:'7FD4A8' } }, '차분으로 상쇄'],
  ];
  s.addTable(rows, { x:0.62, y:2.14, w:12.06, colW:[3.4, 3.0, 3.16, 2.5], fontFace:F,
    fontSize:12, color:'E4EEF5', fill:{ color:'2A3560' },
    border:{ type:'solid', color:'46528C', pt:0.75 }, valign:'middle', rowH:0.46, margin:0.09 });

  card(s, 0.62, 5.06, 5.86, 1.5, '2A3560');
  s.addText('전제 조건', { x:0.86, y:5.24, w:5.4, h:0.3, fontSize:13, bold:true,
    color:P.amb, fontFace:F, isTextBox:true, margin:0 });
  s.addText('표준액과 시료가 정말로 같은 온도여야 합니다. 그래서 온도 센서를 좋은 것으로 쓰는 것보다 플로우셀을 섬프에 담가 열적으로 물리는 쪽이 훨씬 중요합니다.',
    { x:0.86, y:5.58, w:5.4, h:0.86, fontSize:11.5, color:'C3D6E4', fontFace:F,
      lineSpacing:17, isTextBox:true, margin:0 });
  card(s, 6.82, 5.06, 5.86, 1.5, '2A3560');
  s.addText('그래서 남는 것', { x:7.06, y:5.24, w:5.4, h:0.3, fontSize:13, bold:true,
    color:P.amb, fontFace:F, isTextBox:true, margin:0 });
  s.addText('부품의 안정성이 아니라 표준액의 정확도가 전체 정확도를 결정합니다. 계측기 설계에서 도달하고 싶은 지점이 바로 이것입니다.',
    { x:7.06, y:5.58, w:5.4, h:0.86, fontSize:11.5, color:'C3D6E4', fontFace:F,
      lineSpacing:17, isTextBox:true, margin:0 });
}

// ============================================================ 7 오차 예산
{
  const s = pres.addSlide();
  head(s, '측정 오차와 정밀도 이해', '자가보정 이후 남는 오차 항목들. 합계는 제곱합제곱근(RSS) 기준입니다.');
  s.addChart(pres.ChartType.bar, [{
    name:'기여 오차 (PSU)',
    labels:['표준액 정확도','에지 검출 노이즈','기포 · 재현성','캐리오버(10× 플러시)','기구 열팽창 잔차','잔류 온도차'],
    values:[0.100, 0.050, 0.030, 0.010, 0.010, 0.003],
  }], {
    x:0.62, y:1.5, w:7.5, h:4.2, barDir:'bar',
    showTitle:true, title:'항목별 기여 오차', titleFontSize:13, titleColor:P.mid, titleFontFace:F,
    chartColors:[P.deep], showValue:true, dataLabelPosition:'outEnd',
    dataLabelFontSize:10.5, dataLabelColor:P.ink, dataLabelFontFace:F,
    dataLabelFormatCode:'0.000',
    catAxisLabelColor:P.ink, catAxisLabelFontSize:11, catAxisLabelFontFace:F,
    valAxisLabelColor:P.grey, valAxisLabelFontSize:10, valAxisLabelFontFace:F,
    valAxisMaxVal:0.12, valGridLine:{ color:'E6EDF2', size:1 },
    catGridLine:{ style:'none' }, showLegend:false,
    valAxisTitle:'PSU', showValAxisTitle:true, valAxisTitleFontSize:10.5,
    valAxisTitleColor:P.grey, valAxisTitleFontFace:F,
  });

  statCard(s, 8.38, 1.5, 4.3, 1.62, '± 0.12 PSU', '종합 정밀도 (RSS)',
    '일반 취미용 굴절계가 ±1 PSU 수준인 것과 비교하면 한 자릿수 앞선 값입니다.', P.deep);
  card(s, 8.38, 3.3, 4.3, 2.4);
  s.addText('읽는 법', { x:8.6, y:3.48, w:3.9, h:0.3, fontSize:13, bold:true,
    color:P.ink, fontFace:F, isTextBox:true, margin:0 });
  s.addText('표준액 정확도가 전체를 지배합니다. 즉 더 좋은 부품을 사는 것보다 표준액을 밀폐 보관하고 사용 기한을 지키는 쪽이 정밀도에 훨씬 크게 기여합니다.\n\n에지 검출 노이즈는 프레임 평균 횟수를 늘리면 더 줄일 수 있습니다.',
    { x:8.6, y:3.84, w:3.9, h:1.74, fontSize:11.5, color:P.grey, fontFace:F,
      lineSpacing:17, isTextBox:true, margin:0 });
  card(s, 0.62, 5.96, 12.06, 1.06, '#FDF4E8');
  s.addText('부품 드리프트를 다 지우고 나면 남는 것', { x:0.88, y:6.12, w:4.2, h:0.3,
    fontSize:12.5, bold:true, color:'8A5A15', fontFace:F, isTextBox:true, margin:0 });
  s.addText('기포 — 측정면의 미세 기포 하나가 n=1.0 이 되어 경계를 망가뜨립니다   ·   표준액의 정확도 — 밀폐 보관과 사용 기한 관리가 곧 정밀도   ·   측정면의 얇은 막 — 상당 부분 상쇄되지만 완전하지 않아 UVC 와 구연산 세정이 여전히 필요',
    { x:0.88, y:6.44, w:11.6, h:0.42, fontSize:11, color:P.ink, fontFace:F,
      lineSpacing:16, isTextBox:true, margin:0 });
  s.addNotes('RSS = sqrt(0.1^2 + 0.05^2 + 0.03^2 + 0.01^2 + 0.01^2 + 0.003^2) = 0.117 PSU');
}

// ============================================================ 8 플로우셀
{
  const s = pres.addSlide();
  head(s, '플로우셀 설계', '상시 침지가 아니라 필요할 때만 물을 받아 재는 구조. 생물오손 문제를 구조적으로 회피합니다.');
  s.addImage({ path:'fig_cell.png', x:2.14, y:1.44, w:9.01, h:4.70 });
  s.addText('측정 사이에는 셀을 비워 말리지 않고 35.0 PSU 표준액으로 채워둡니다. 마르면 측정면에 염 결정이 남아 그대로 오차가 되기 때문입니다.',
    { x:0.62, y:6.32, w:12.06, h:0.4, fontSize:11.5, color:P.grey, fontFace:F, align:'center',
      isTextBox:true, margin:0 });
}

// ============================================================ 9 유체 회로
{
  const s = pres.addSlide();
  head(s, '유체 회로', '페리스탈틱 펌프 4개로 밸브 없이 구성. 각 펌프가 MOSFET 하나로 제어됩니다.');
  s.addImage({ path:'fig_fluidics.png', x:1.20, y:1.50, w:10.90, h:5.40 });
}

// ============================================================ 10 보관액 선택
{
  const s = pres.addSlide();
  head(s, '보관액은 왜 35.0 PSU 표준액인가', '잔류액의 굴절률 차이가 그대로 측정 오차가 됩니다. 오차는 대략  잔류율 × (보관액 염도 − 34).');
  tbl(s, 0.62, 1.6, 6.1, [
    [th('보관액'), th('1 % 잔류 시 오차'), th('수조 유입 시')],
    ['RO-DI  (0 PSU)', { text:'0.34 PSU', options:{ bold:true, color:P.red } }, '무해'],
    ['35.0 PSU 표준액', { text:'0.01 PSU', options:{ bold:true, color:P.deep } }, '완전 무해 (그냥 해수)'],
    ['차아염소산 (표백제)', '—', { text:'생물 폐사 — 자동 루프 금지', options:{ color:P.red } }],
  ], [2.1, 2.0, 2.0], { rowH:0.44 });
  s.addText('34 배 차이입니다. 이 한 줄이 보관액 선택을 결정합니다.',
    { x:0.62, y:3.5, w:6.1, h:0.32, fontSize:12.5, bold:true, color:P.deep,
      fontFace:F, isTextBox:true, margin:0 });

  const items = [
    ['잔류 오차가 사라짐', '보관액과 시료의 염도 차이가 1 PSU 뿐이라\n캐리오버에 거의 둔감해집니다.'],
    ['수조에 완전 무해', '복귀 라인으로 넘어가도 그냥 해수입니다.\n화학 약품 유입 위험이 원천적으로 없습니다.'],
    ['공짜 보정점', '유휴 상태의 셀이 항상 알려진 표준액으로\n채워져 있어, 매 사이클 직전 보정점이 생깁니다.'],
  ];
  let yy = 1.66;
  items.forEach(([t, b], i) => { numRow(s, 7.05, yy, 5.6, i+1, t, b); yy += 1.3; });

  card(s, 0.62, 4.06, 6.1, 2.32, '#F3EEF8');
  s.addText('오손 방지는 화학약품 대신 UVC LED 로', { x:0.86, y:4.26, w:5.6, h:0.34,
    fontSize:13.5, bold:true, color:'6B3F97', fontFace:F, isTextBox:true, margin:0 });
  s.addText('유휴 시간 동안 셀 내부에 265 nm UVC LED 를 간헐 점등합니다. 해양 광학 센서의 방오 대책으로 검증된 방법이고, 소모품이 없으며 수조 유입 위험이 없습니다.\n\n주의 : UVC 는 실리콘 튜브 · PMMA · 접착제를 열화시킵니다. UVC 근처는 PTFE 나 유리를 쓰고, 프리즘 접착에 UV 경화 접착제는 피하십시오.',
    { x:0.86, y:4.66, w:5.6, h:1.6, fontSize:11.5, color:P.ink, fontFace:F,
      lineSpacing:17, isTextBox:true, margin:0 });

  card(s, 7.05, 5.44, 5.63, 0.94, '#FDF4E8');
  s.addText('스케일 대책', { x:7.28, y:5.6, w:5.2, h:0.28, fontSize:12.5, bold:true,
    color:'8A5A15', fontFace:F, isTextBox:true, margin:0 });
  s.addText('리프 수조는 탄산칼슘이 잘 석출됩니다. 월 1회 묽은 구연산 순환 → RO-DI 헹굼 루틴을 넣으십시오.',
    { x:7.28, y:5.9, w:5.2, h:0.42, fontSize:11, color:P.ink, fontFace:F,
      lineSpacing:16, isTextBox:true, margin:0 });
}

// ============================================================ 11 배선도
{
  const s = pres.addSlide();
  head(s, '아두이노 배선도', 'Arduino Nano 기준. 핀 여유가 충분하며, 12 V 펌프 전원은 로직과 분리합니다.');
  s.addImage({ path:'fig_wiring.png', x:1.59, y:1.42, w:10.12, h:5.40 });
}

// ============================================================ 12 HC-06 상세
{
  const s = pres.addSlide();
  head(s, 'HC-06 연결 —  분압기를 빠뜨리지 마십시오', 'ZS-040 계열 보드는 통신 핀이 3.3 V 소자입니다. 나노는 5 V 로직이므로 한쪽 방향만 보호가 필요합니다.');

  card(s, 0.62, 1.6, 5.9, 1.5, '#EAF4EC');
  s.addText('HC-06  TXD  →  Nano  D7      직결 가능', { x:0.9, y:1.82, w:5.4, h:0.34,
    fontSize:14, bold:true, color:'2E7D4F', fontFace:F, isTextBox:true, margin:0 });
  s.addText('HC-06 이 내보내는 3.3 V 를 ATmega328P 가 HIGH 로 충분히 인식합니다.\n(대략 3 V 이상이면 HIGH)',
    { x:0.9, y:2.2, w:5.4, h:0.78, fontSize:11.5, color:P.ink, fontFace:F,
      lineSpacing:17, isTextBox:true, margin:0 });

  card(s, 6.78, 1.6, 5.9, 1.5, '#FBEDEC');
  s.addText('Nano  D8  →  HC-06  RXD      분압기 필수', { x:7.06, y:1.82, w:5.4, h:0.34,
    fontSize:14, bold:true, color:P.red, fontFace:F, isTextBox:true, margin:0 });
  s.addText('5 V 를 그대로 넣으면 내부 UART 나 레귤레이터가 손상되거나 수명이 줄어듭니다.\n1 kΩ / 2 kΩ 로 약 3.3 V 로 낮추십시오.',
    { x:7.06, y:2.2, w:5.4, h:0.78, fontSize:11.5, color:P.ink, fontFace:F,
      lineSpacing:17, isTextBox:true, margin:0 });

  card(s, 0.62, 3.3, 12.06, 1.34, P.mid);
  s.addText('D8  ──[ 1 kΩ ]──┬──  HC-06  RXD\n                              └──[ 2 kΩ ]── GND',
    { x:0.95, y:3.5, w:7.0, h:0.94, fontSize:14, color:'CFE7F2',
      fontFace:'Courier New', lineSpacing:24, isTextBox:true, margin:0 });
  s.addText('5 V × 2 kΩ / (1 kΩ + 2 kΩ)  =  3.33 V', { x:8.1, y:3.82, w:4.3, h:0.4,
    fontSize:14, bold:true, color:P.amb, fontFace:F, isTextBox:true, margin:0 });

  const rows = [
    [th('항목'), th('내용')],
    ['전원 VCC', 'ZS-040 보드에는 3.3 V 레귤레이터가 있어 3.6~6 V 입력이 필요합니다. 5 V 를 쓰십시오. 3.3 V 직결은 드롭아웃 부족으로 동작이 불안정해집니다.'],
    ['판매 문구 주의', '"5 V MCU 직결 가능"은 방향을 구분하지 않은 뭉뚱그린 표현입니다. RXD 는 5 V 내성이 없습니다.'],
    ['SoftwareSerial', '송신 중 인터럽트를 막으므로 TSL1401 프레임 캡처와 겹치지 않게 순차 처리하십시오.'],
    ['ESP32 대안', 'ESP32 를 쓰면 블루투스가 내장이라 HC-06 과 분압기가 모두 불필요합니다. 다만 ADC 선형성 보정이 필요합니다.'],
  ];
  tbl(s, 0.62, 4.84, 12.06, rows, [2.3, 9.76], { rowH:0.42, fs:11.5 });
}

// ============================================================ 13 BT 명령어
{
  const s = pres.addSlide();
  head(s, '블루투스 명령어 세트', '스마트폰 BT 시리얼 터미널에서 한 줄씩 입력합니다. 대소문자는 구분하지 않습니다.');

  s.addText('절차 명령  (순차 실행)', { x:0.62, y:1.48, w:6.0, h:0.32, fontSize:14,
    bold:true, color:P.deep, fontFace:F, isTextBox:true, margin:0 });
  tbl(s, 0.62, 1.86, 6.06, [
    [th('명령'), th('동작')],
    [mono('MEAS STD'), '표준용액 측정 → 보정점 A'],
    [mono('DRAIN'), '셀 비우기'],
    [mono('FILL RODI'), 'RO-DI 주입'],
    [mono('MEAS RODI'), 'RO-DI 측정 → 보정점 B'],
    [mono('FILL TANK'), '수조물 주입 (값이 평평해질 때까지)'],
    [mono('MEAS TANK'), '수조물 측정 → 시료'],
    [mono('FILL STD'), '표준용액 주입 · 보관 모드'],
    [mono('END'), '검량선 계산 · 결과 출력 · 종료'],
  ], [2.1, 3.96], { rowH:0.355 });

  s.addText('운용 명령', { x:6.9, y:1.48, w:5.8, h:0.32, fontSize:14, bold:true,
    color:P.amb, fontFace:F, isTextBox:true, margin:0 });
  tbl(s, 6.9, 1.86, 5.78, [
    [th('명령'), th('동작')],
    [mono('RUN'), '전체 시퀀스 1회 자동 실행'],
    [mono('AUTO ON / OFF'), '1일 2회 자동 측정 (09:00 / 21:00)'],
    [mono('STAT'), '현재 상태 · 온도 · 최근 측정값'],
    [mono('LOG'), '최근 측정 이력'],
    [mono('UVC ON / OFF'), 'UVC LED 수동 제어'],
    [mono('DUMP'), '128 px 원시 프레임 덤프 (디버그)'],
    [mono('STOP'), '비상 정지 — 모든 펌프 즉시 off'],
    [mono('HELP'), '명령 목록'],
  ], [2.1, 3.68], { rowH:0.355 });

  card(s, 0.62, 5.42, 12.06, 1.12, P.mid);
  s.addText('응답 예시', { x:0.88, y:5.56, w:2, h:0.28, fontSize:11.5, bold:true,
    color:P.amb, fontFace:F, isTextBox:true, margin:0 });
  s.addText('> MEAS TANK\nOK  edge=63.58px  T=26.12C  ->  34.12 PSU     cal: RODI 0.00@29.98px | STD 35.00@64.88px | slope 0.997 px/PSU',
    { x:0.88, y:5.84, w:11.5, h:0.6, fontSize:11, color:'CFE7F2',
      fontFace:'Courier New', lineSpacing:17, isTextBox:true, margin:0 });
}

// ============================================================ 14 자동 시퀀스
{
  const s = pres.addSlide();
  head(s, '자동 측정 시퀀스', '하루 2회. 각 단계는 블루투스로 하나씩 보낼 수도 있고, RUN 한 번으로 전부 돌릴 수도 있습니다.');

  const steps = [
    ['1','표준용액 측정','보정점 A 획득'],
    ['2','표준용액 비우기','DRAIN'],
    ['3','RO-DI 주입','헹굼 겸용'],
    ['4','RO-DI 측정','보정점 B 획득'],
    ['5','RO-DI 비우기','DRAIN'],
    ['6','수조물 주입','값이 평평해질 때까지'],
    ['7','수조물 측정','시료 · 온도 동시 기록'],
    ['8','수조물 비우기','DRAIN'],
    ['9','표준용액 주입','보관 모드 복귀'],
    ['10','표준액 재확인 · 종료','A ≈ A′ 이면 사이클 유효'],
  ];
  let x = 0.62, y = 1.52;
  steps.forEach((st, i) => {
    const col = (i === 9) ? P.teal : (i === 6 ? P.amb : P.deep);
    const cx = x + (i % 5) * 2.44;
    const cy = y + Math.floor(i / 5) * 1.62;
    card(s, cx, cy, 2.24, 1.4);
    s.addShape(pres.ShapeType.ellipse, { x:cx+0.16, y:cy+0.16, w:0.36, h:0.36,
      fill:{ color:col }, line:{ width:0 } });
    s.addText(st[0], { x:cx+0.16, y:cy+0.16, w:0.36, h:0.36, fontSize:12, bold:true,
      color:P.white, align:'center', valign:'middle', fontFace:F, isTextBox:true, margin:0 });
    s.addText(st[1], { x:cx+0.16, y:cy+0.6, w:1.94, h:0.44, fontSize:12, bold:true,
      color:P.ink, fontFace:F, lineSpacing:15, isTextBox:true, margin:0 });
    s.addText(st[2], { x:cx+0.16, y:cy+1.02, w:1.94, h:0.3, fontSize:10, color:P.grey,
      fontFace:F, isTextBox:true, margin:0 });
  });

  card(s, 0.62, 4.9, 5.9, 1.5, '#EAF2F7');
  s.addText('10번 단계가 특히 중요합니다', { x:0.88, y:5.08, w:5.4, h:0.3, fontSize:13,
    bold:true, color:P.deep, fontFace:F, isTextBox:true, margin:0 });
  s.addText('처음과 끝의 표준액 값이 일치하면 그 사이클은 신뢰할 수 있고, 어긋나면 측정 중 무언가 변했다는 뜻입니다. 장치가 스스로 진단합니다.',
    { x:0.88, y:5.42, w:5.4, h:0.86, fontSize:11.5, color:P.ink, fontFace:F,
      lineSpacing:17, isTextBox:true, margin:0 });

  tbl(s, 6.78, 4.9, 5.9, [
    [th('단계'), th('시간'), th('근거')],
    ['주입 (FILL)', '≈ 30 초', '셀 2 mL × 10배 = 20 mL @ 40 mL/min'],
    ['안정화 (SETTLE)', '≈ 45 초', '기포 배출 + 열평형'],
    ['측정 (MEAS)', '≈ 15 초', '프레임 100회 평균'],
    ['배수 (DRAIN)', '≈ 25 초', ''],
    [{ text:'1 사이클 합계', options:{ bold:true } },
     { text:'≈ 8 분', options:{ bold:true, color:P.deep } },
     { text:'4 단계 + 검증', options:{ bold:true } }],
  ], [1.75, 1.15, 3.0], { rowH:0.34, fs:11 });
}

// ============================================================ 15 부품 목록
{
  const s = pres.addSlide();
  head(s, '재료와 부품', '광학 · 유체 · 전자 · 소모품 네 갈래로 나눈 전체 부품 목록입니다.');
  const rows = [
    [th('구분'), th('부품'), th('사양 · 비고'), th('수량')],
    ['광학', 'BK7 반원통 렌즈', '반경 10~25 mm, 길이 25 mm 내외', '1'],
    ['광학', '단색 LED 590 nm', '스펙트럼 폭 20 nm 이하, 정전류 구동', '1'],
    ['광학', 'TSL1401CL 리니어 어레이', '128 px × 63.5 µm, 아두이노용 모듈 유통', '1'],
    ['광학', '슬릿 · 차광 하우징', '흑색 알루미늄 또는 3D 프린트, 검출팔 250 mm', '1식'],
    ['유체', '페리스탈틱 도징 펌프', '12 V, 40~60 mL/min', '4'],
    ['유체', '플로우셀 본체', 'PTFE 또는 PVDF (UVC 근처는 PMMA 금지)', '1'],
    ['유체', 'O-링 · 튜브', 'Viton O-링, 펌프부만 실리콘 · 나머지 PTFE', '1식'],
    ['전자', 'Arduino Nano', 'ATmega328P 5 V (ESP32 로 대체 가능)', '1'],
    ['전자', 'HC-06 (ZS-040)', '1 kΩ / 2 kΩ 분압기 동반', '1'],
    ['전자', 'DS18B20 · DS3231', '온도(셀 유로 내부) · RTC', '각 1'],
    ['전자', 'MOSFET · 플라이백 다이오드', 'IRLZ44N 등 로직레벨 ×6, 1N4007 ×4', '1식'],
    ['소모품', '35.0 PSU 표준 해수', '보관액 겸 보정액. 월 250 mL 내외 소모', '상시'],
    ['소모품', 'RO-DI · 구연산', '헹굼 · 월 1회 스케일 제거', '상시'],
    ['광학', 'UVC LED 265 nm', '수 mW, 유휴 시 간헐 살균', '1'],
  ];
  s.addTable(rows, { x:0.62, y:1.5, w:12.06, colW:[1.15, 3.5, 5.71, 1.7], fontFace:F,
    fontSize:11, color:P.ink, border:{ type:'solid', color:P.line, pt:0.75 },
    fill:{ color:P.white }, valign:'middle', rowH:0.325, margin:0.06 });
}

// ============================================================ 16 제작 순서
{
  const s = pres.addSlide();
  head(s, '제작 순서와 검증', '광학계를 먼저 세우고, 유체는 나중에 붙이는 편이 디버깅이 쉽습니다.');
  const phases = [
    ['1단계', '광학 벤치 가조립', '렌즈·LED·어레이를 임시 고정하고 공기 중에서 어레이 전체가 밝아지는지 확인합니다. 이것이 풀스케일 기준점입니다.'],
    ['2단계', '정적 시료 시험', '측정면에 RO-DI 한 방울, 표준액 한 방울을 번갈아 올려 경계 픽셀이 약 34 px 이동하는지 확인합니다. 여기서 감도가 맞으면 광학계는 완성입니다.'],
    ['3단계', '플로우셀 결합', '셀을 조립하고 누수·기포를 확인합니다. 주입 중 측정값이 평평해지는 곡선이 보이면 정상입니다.'],
    ['4단계', '펌프 · 제어 결합', '펌프를 MOSFET 으로 하나씩 검증한 뒤 시퀀스를 붙입니다. 플라이백 다이오드를 반드시 먼저 다십시오.'],
    ['5단계', '블루투스 · 자동화', '수동 명령으로 전 단계를 확인한 후 RUN, 그다음 AUTO 를 켭니다.'],
  ];
  let yy = 1.55;
  phases.forEach(([p, t, b], i) => {
    card(s, 0.62, yy, 7.5, 0.92);
    s.addText(p, { x:0.86, y:yy+0.2, w:0.95, h:0.3, fontSize:11.5, bold:true,
      color:P.amb, fontFace:F, isTextBox:true, margin:0 });
    s.addText(t, { x:1.85, y:yy+0.2, w:2.2, h:0.3, fontSize:12.5, bold:true,
      color:P.ink, fontFace:F, isTextBox:true, margin:0 });
    s.addText(b, { x:1.85, y:yy+0.5, w:6.05, h:0.36, fontSize:10.5, color:P.grey,
      fontFace:F, lineSpacing:14, isTextBox:true, margin:0 });
    yy += 1.0;
  });

  card(s, 8.38, 1.55, 4.3, 2.4, '#EAF2F7');
  s.addText('검증 방법', { x:8.62, y:1.75, w:3.9, h:0.3, fontSize:13.5, bold:true,
    color:P.deep, fontFace:F, isTextBox:true, margin:0 });
  s.addText('· 표준액을 두 번 재서 재현성 확인\n· 알려진 다른 농도의 용액으로 교차 확인\n· 상용 굴절계 값과 비교\n· A 와 A′ 의 차이를 매 사이클 기록\n· 플러시 곡선이 평평해지는지 확인',
    { x:8.62, y:2.12, w:3.9, h:1.7, fontSize:11.5, color:P.ink, fontFace:F,
      lineSpacing:19, isTextBox:true, margin:0 });

  card(s, 8.38, 4.1, 4.3, 2.4, '#FDF4E8');
  s.addText('먼저 확인할 것', { x:8.62, y:4.3, w:3.9, h:0.3, fontSize:13.5, bold:true,
    color:'8A5A15', fontFace:F, isTextBox:true, margin:0 });
  s.addText('기포가 최대 적입니다. 측정면에 미세 기포 하나가 붙으면 그 자리가 n=1.0 이 되어 경계선을 망가뜨립니다.\n\n여러 번 읽어 이상치를 버리는 로직을 처음부터 넣으십시오.',
    { x:8.62, y:4.68, w:3.9, h:1.7, fontSize:11.5, color:P.ink, fontFace:F,
      lineSpacing:18, isTextBox:true, margin:0 });
}

// ============================================================ 17 안전
{
  const s = pres.addSlide();
  head(s, '안전 주의사항', '살아 있는 생물이 있는 수조에 연결되는 장치입니다. 배관 실수 한 번이 사고가 됩니다.');
  const items = [
    ['사이펀 · 침수', '수조에 연결된 펌프 루프는 배관을 잘못하면 정지 중 사이펀이 걸려 바닥에 물난리가 납니다. 페리스탈틱 펌프는 정지 시 튜브가 눌려 있어 사이펀이 원천 차단되므로 반드시 이 방식을 쓰십시오.', P.red],
    ['세정액 유입', '표백제는 미량이라도 수조에 들어가면 생물이 죽습니다. 자동 루프 안에 두지 말고, 월 1회 셀을 분리해 수동으로 하며 폐수는 반드시 배수로 보내십시오.', P.red],
    ['UVC 노출', '265 nm 는 눈과 피부에 유해합니다. 셀은 완전 차광 하우징 안에 두고, 하우징이 열리면 UVC 가 꺼지도록 인터록을 넣는 것이 좋습니다.', P.violet],
    ['전원 분리', '12 V 펌프 전원과 5 V 로직 전원을 분리하고 접지를 한 점에서 모으십시오. 모터마다 플라이백 다이오드를 달지 않으면 역기전력이 MCU 를 리셋시킵니다.', P.deep],
    ['펌프 동작 시간 제한', '펌프마다 최대 동작 시간을 코드에 넣고, 초과하면 STOP 으로 빠지게 하십시오. 튜브가 빠졌을 때 무한정 도는 것을 막습니다.', P.deep],
  ];
  let yy = 1.55;
  items.forEach(([t, b, c]) => {
    card(s, 0.62, yy, 12.06, 0.94);
    s.addShape(pres.ShapeType.ellipse, { x:0.86, y:yy+0.29, w:0.36, h:0.36,
      fill:{ color:c }, line:{ width:0 } });
    s.addText('!', { x:0.86, y:yy+0.29, w:0.36, h:0.36, fontSize:14, bold:true,
      color:P.white, align:'center', valign:'middle', fontFace:F, isTextBox:true, margin:0 });
    s.addText(t, { x:1.42, y:yy+0.14, w:2.7, h:0.32, fontSize:13, bold:true, color:P.ink,
      fontFace:F, isTextBox:true, margin:0 });
    s.addText(b, { x:1.42, y:yy+0.46, w:11.0, h:0.42, fontSize:11, color:P.grey,
      fontFace:F, lineSpacing:15, isTextBox:true, margin:0 });
    yy += 1.02;
  });
}

// ============================================================ 18 마무리
{
  const s = pres.addSlide();
  s.background = { color: P.mid };
  s.addText('정리', { x:0.9, y:0.72, w:5, h:0.32, fontSize:13, color:P.amb, bold:true,
    charSpacing:2, fontFace:F, isTextBox:true, margin:0 });
  s.addText('취미용 부품으로 만드는 실험실급 구조', { x:0.9, y:1.1, w:11.5, h:0.62,
    fontSize:30, bold:true, color:P.white, fontFace:F, isTextBox:true, margin:0 });
  s.addText('이 설계의 강점은 부품이 좋아서가 아니라, 매 측정마다 알려진 표준을 스스로 재기 때문입니다.\n전도도 프로브로는 할 수 없는 일입니다.',
    { x:0.9, y:1.86, w:11.5, h:0.7, fontSize:14, color:'B9D3E2', fontFace:F,
      lineSpacing:22, isTextBox:true, margin:0 });

  const k = [['1 px ≈ 1 PSU','250 mm 검출팔 기준'],
             ['± 0.12 PSU','종합 정밀도 (RSS)'],
             ['450 배','온도 오차 개선'],
             ['≈ 8 분','1 사이클 소요'],
             ['1일 2회','무인 자동 측정']];
  let x = 0.9;
  k.forEach(([v, l]) => {
    s.addShape(pres.ShapeType.roundRect, { x, y:2.78, w:2.28, h:1.24,
      fill:{ color:'2A3560' }, line:{ color:'46528C', width:1 }, rectRadius:0.06 });
    s.addText(v, { x:x+0.18, y:2.96, w:1.92, h:0.44, fontSize:17, bold:true, color:P.amb,
      fontFace:F, isTextBox:true, margin:0 });
    s.addText(l, { x:x+0.18, y:3.44, w:1.92, h:0.42, fontSize:10.5, color:'A9C4D6',
      fontFace:F, lineSpacing:14, isTextBox:true, margin:0 });
    x += 2.42;
  });

  s.addText('근거 및 참고자료', { x:0.9, y:4.34, w:11.5, h:0.32, fontSize:13, bold:true,
    color:P.amb, fontFace:F, isTextBox:true, margin:0 });
  const refs = [
    '굴절률 경험식 계수 (본문의 모든 수치는 이 식으로 직접 계산) — Index of Refraction of Seawater and Freshwater as a Function of Wavelength and Temperature, Oregon State University, Parrish Research Group',
    'TSL1401CL 128×1 Linear Sensor Array 데이터시트 — ams-osram (Mouser)',
    '임계각 · 그림자 경계 측정 원리 — Digital handheld refractometer, Wikipedia',
    'TCD1304 의 MHz 샘플링 한계 사례 (TSL1401 권장 근거) — LED refractometry with Arduino, Arduino Forum',
    '해양 광학 센서의 생물오손과 방오 대책 — Biofouling protection for marine environmental sensors, Ocean Science (Copernicus) / Antifouling Strategies for Sensors Used in Water Monitoring, Sensors (MDPI)',
    'HC-05 · HC-06 ZS-040 보드의 전원 · 로직 레벨 — Martyn Currey, ProtoSupplies',
  ];
  s.addText(refs.map((t, i) => ({ text:t, options:{ bullet:true, breakLine: i !== refs.length-1 } })),
    { x:0.9, y:4.7, w:11.5, h:2.3, fontSize:10, color:'9FBBCE', fontFace:F,
      lineSpacing:15, paraSpaceAfter:5, bullet:true, isTextBox:true, margin:0 });
}

pres.writeFile({ fileName: '해수수조_광학식_염도측정_설계.pptx' })
  .then(f => console.log('WROTE', f));
