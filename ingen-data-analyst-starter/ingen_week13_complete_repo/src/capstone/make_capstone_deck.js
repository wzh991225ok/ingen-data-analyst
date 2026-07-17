const pptxgen = require("pptxgenjs");
const p = new pptxgen();
p.layout = "LAYOUT_WIDE";
p.author = "Ziheng Wang";
p.title = "Public-Data Analytics on the InGen Robotics Portfolio — Executive Deck";
const A = "/home/claude/cap_fig/";

const NAVY="1E2761", MID="3A5BA0", ICE="CADCFC", WHITE="FFFFFF", INK="222A4A",
      GREY="5A6175", BG="F4F6FB", CARD="FFFFFF", GREEN="2E7D5B", AMBER="B8860B", ORANGE="C77400";
const HEAD="Cambria", BODY="Calibri";

function card(s,x,y,w,h,fill){ s.addShape(p.shapes.ROUNDED_RECTANGLE,{x,y,w,h,fill:{color:fill||CARD},rectRadius:0.07,
  line:{color:"E2E7F2",width:1},shadow:{type:"outer",color:"9AA6C0",blur:6,offset:3,angle:90,opacity:0.22}}); }
function circ(s,x,y,d,fill,g,fs){ s.addShape(p.shapes.OVAL,{x,y,w:d,h:d,fill:{color:fill}});
  if(g) s.addText(g,{x,y,w:d,h:d,align:"center",valign:"middle",fontFace:HEAD,fontSize:fs||14,bold:true,color:WHITE,margin:0}); }
function header(s,t,sub){ s.background={color:BG};
  s.addText(t,{x:0.7,y:0.4,w:12.2,h:0.65,fontFace:HEAD,fontSize:26,bold:true,color:NAVY,margin:0});
  if(sub) s.addText(sub,{x:0.72,y:1.03,w:12.2,h:0.4,fontFace:BODY,fontSize:13,italic:true,color:GREY,margin:0}); }
function tag(s,t,c){ s.addShape(p.shapes.ROUNDED_RECTANGLE,{x:10.95,y:0.45,w:1.85,h:0.5,fill:{color:c},rectRadius:0.25});
  s.addText(t,{x:10.95,y:0.45,w:1.85,h:0.5,align:"center",valign:"middle",fontFace:BODY,fontSize:10.5,bold:true,color:WHITE,margin:0}); }
function foot(s,t){ s.addText(t,{x:0.7,y:6.72,w:12,h:0.35,fontFace:BODY,fontSize:10,italic:true,color:GREY,margin:0}); }

/* 1 — Title */
let s=p.addSlide(); s.background={color:NAVY};
s.addText("CAPSTONE — EXECUTIVE SUMMARY",{x:0.9,y:1.45,w:11.5,h:0.5,fontFace:BODY,fontSize:14,bold:true,color:ICE,charSpacing:3,margin:0});
s.addText("Public-Data Analytics on the\nInGen Robotics Portfolio",{x:0.9,y:2.0,w:11.6,h:1.9,fontFace:HEAD,fontSize:38,bold:true,color:WHITE,lineSpacingMultiple:1.05,margin:0});
s.addText("Market · Competition · BI · Forecasting · Operations",{x:0.9,y:4.0,w:11.5,h:0.5,fontFace:BODY,fontSize:17,color:ICE,margin:0});
s.addText([{text:"Thirteen weeks, five verticals, "},{text:"public data only",options:{bold:true,color:ICE}},{text:" — no internal access required."}],
  {x:0.9,y:4.75,w:11.2,h:0.5,fontFace:BODY,fontSize:14,color:"C9D2EC",margin:0});
s.addText("Ziheng Wang  ·  Data Analyst Intern  ·  inGen Dynamics (Futurenauts)",{x:0.9,y:6.5,w:11.5,h:0.4,fontFace:BODY,fontSize:12,color:"8E9AC2",margin:0});

/* 2 — Six findings */
s=p.addSlide(); header(s,"Six findings that matter","If you read one slide, read this one.");
const F=[["1","Funding is not a moat","Capital raised and defensible IP diverge. Margin structure predicts durability — not headline raises."],
["2","The biggest market isn't the loudest","Sentinel (indoor security) has the clearest near-term economics. Humanoid gets the capital and the headlines."],
["3","Attention ≠ opportunity","Demand ranking is the near-inverse of market attractiveness. Sentinel: strong asset, weak share of voice."],
["4","Momentum is up; models beat naive","MASE < 1.0 in 4 of 5 verticals. No single model wins everywhere — keep a portfolio."],
["5","Sentinel's alerts: persistence, not threshold","120-min persistence cuts alert load 33× (16.35 → 0.50/day) while recall rises to 88%."],
["6","Support is a parts problem","Parts = 53% of cycle time, 100% waiting. Parts buffer −23% vs +1 engineer −8%."]];
const fx=[0.7,6.75], fy=[1.6,3.35,5.1], fw=5.9, fh=1.62;
F.forEach((f,i)=>{const x=fx[i%2],y=fy[Math.floor(i/2)];card(s,x,y,fw,fh);
  circ(s,x+0.28,y+0.28,0.5,MID,f[0],14);
  s.addText(f[1],{x:x+0.92,y:y+0.24,w:fw-1.15,h:0.42,fontFace:HEAD,fontSize:13.5,bold:true,color:NAVY,margin:0,valign:"middle"});
  s.addText(f[2],{x:x+0.3,y:y+0.76,w:fw-0.6,h:0.72,fontFace:BODY,fontSize:11,color:INK,margin:0,lineSpacingMultiple:1.05});});

/* 3 — Method */
s=p.addSlide(); header(s,"How this was built","Four phases, thirteen self-contained modules, everything reproducible.");
const PH=[["Phase 1","Wks 1–3","Foundation","Products, 40+ competitors, 12-dataset pipeline, DuckDB warehouse"],
["Phase 2","Wks 4–6","Market analytics","TAM/SAM/SOM, demand-signal index, peer financials"],
["Phase 3","Wks 7–9","BI platform","Star schema, 3 dashboards, exec scorecard"],
["Phase 4","Wks 10–12","Advanced analytics","Forecasting, anomaly detection, process optimisation"]];
const pw=2.92,gp=0.18;
PH.forEach((c,i)=>{const x=0.7+i*(pw+gp);card(s,x,1.75,pw,3.5);
  s.addText(c[0],{x:x+0.25,y:2.0,w:pw-0.5,h:0.35,fontFace:HEAD,fontSize:16,bold:true,color:NAVY,margin:0});
  s.addText(c[1],{x:x+0.25,y:2.38,w:pw-0.5,h:0.3,fontFace:BODY,fontSize:11,bold:true,color:MID,margin:0});
  s.addText(c[2],{x:x+0.25,y:2.75,w:pw-0.5,h:0.45,fontFace:HEAD,fontSize:14,bold:true,color:INK,margin:0});
  s.addText(c[3],{x:x+0.25,y:3.3,w:pw-0.5,h:1.5,fontFace:BODY,fontSize:11,color:GREY,margin:0,lineSpacingMultiple:1.1});
  if(i<3) s.addText("›",{x:x+pw-0.02,y:3.2,w:gp+0.04,h:0.6,align:"center",valign:"middle",fontFace:HEAD,fontSize:20,bold:true,color:MID,margin:0});});
card(s,0.7,5.45,11.95,1.05,"EEF3FB");
s.addText([{text:"Principles:  ",options:{bold:true,color:NAVY}},
 {text:"sourced or not stated  ·  ranges over false precision  ·  synthetic data always labelled  ·  fixed seeds + test suites  ·  methods validated against ground truth where it exists",options:{color:INK}}],
 {x:1.0,y:5.62,w:11.4,h:0.7,fontFace:BODY,fontSize:12,margin:0,lineSpacingMultiple:1.1});

/* 4 — Market sizing */
s=p.addSlide(); header(s,"Market sizing — ranges, not points","Published estimates disagree by an order of magnitude. That's the finding.");
tag(s,"Week 4",MID);
const MS=[["Sentinel Prime AI","indoor security","Highest","Guard-replacement economics vs a costed alternative",GREEN],
["Fari","eldercare","Medium-high","Large population; adoption-rate constrained",GREEN],
["Senpai","education","Medium","Steady; tied to budget cycles",MID],
["Aido Rover","outdoor patrol","Scenario range","High potential, high uncertainty",AMBER],
["Aido Humanoid","humanoid","Scenario range","A bet on future deployment, not a current pool",AMBER]];
let my=1.75;
MS.forEach(m=>{card(s,0.7,my,7.6,0.88);
  s.addText(m[0],{x:0.95,y:my+0.14,w:2.0,h:0.3,fontFace:HEAD,fontSize:13,bold:true,color:NAVY,margin:0});
  s.addText(m[1],{x:0.95,y:my+0.46,w:2.0,h:0.28,fontFace:BODY,fontSize:10,color:GREY,margin:0});
  s.addShape(p.shapes.ROUNDED_RECTANGLE,{x:3.05,y:my+0.24,w:1.35,h:0.4,fill:{color:m[4]},rectRadius:0.2});
  s.addText(m[2],{x:3.05,y:my+0.24,w:1.35,h:0.4,align:"center",valign:"middle",fontFace:BODY,fontSize:9.5,bold:true,color:WHITE,margin:0});
  s.addText(m[3],{x:4.55,y:my+0.24,w:3.6,h:0.42,fontFace:BODY,fontSize:10.5,color:INK,margin:0,valign:"middle"});
  my+=0.98;});
s.addImage({path:A+"tornado_sentinel.png",x:8.5,y:1.9,w:4.15,h:2.25});
card(s,8.5,4.4,4.15,2.05,"EEF3FB");
s.addText("Penetration rate dominates",{x:8.75,y:4.6,w:3.7,h:0.35,fontFace:HEAD,fontSize:13.5,bold:true,color:NAVY,margin:0});
s.addText("In every vertical: penetration first, ASP second, unit count a distant third. Market size is mostly a go-to-market variable InGen partly controls — not a fixed external quantity.",
 {x:8.75,y:5.0,w:3.7,h:1.3,fontFace:BODY,fontSize:10.5,color:INK,margin:0,lineSpacingMultiple:1.08});
foot(s,"Humanoid quoted ~$290M–$4.89bn; security robotics ~$4.7bn–$19bn. Every figure is a sourced range.");

/* 5 — Competition */
s=p.addSlide(); header(s,"Competition — funding is not a moat","15 priority peers, real patents and headcounts, dated sources.");
tag(s,"Weeks 1–2",MID);
card(s,0.7,1.75,11.95,1.65,"27306B");
s.addText("Capital raised and defensible IP diverge sharply.",{x:1.1,y:1.98,w:11.1,h:0.4,fontFace:HEAD,fontSize:19,bold:true,color:ICE,margin:0});
s.addText("The most heavily funded humanoid companies are not the most patent-dense. Several quieter competitors hold stronger, earlier, more specific grants. Funding is the metric the trade press reports and the one that shapes internal anxiety — and it is the wrong one.",
 {x:1.1,y:2.44,w:11.1,h:0.8,fontFace:BODY,fontSize:12.5,color:"D5DCF0",margin:0,lineSpacingMultiple:1.1});
const CC=[["$1bn + thin patents","Buying time","A war chest funds runway, not defensibility.",AMBER],
["$100M + dense position","Buying ground","Specific grants around a mechanism are durable.",GREEN],
["Confirmed in Week 6","From the other side","Durable peers have defensible margin structures — not the biggest raises.",MID]];
const cx=[0.7,4.85,9.0];
CC.forEach((c,i)=>{card(s,cx[i],3.6,3.75,2.85);
  s.addText(c[0],{x:cx[i]+0.3,y:3.85,w:3.15,h:0.4,fontFace:HEAD,fontSize:14,bold:true,color:c[3],margin:0});
  s.addText(c[1],{x:cx[i]+0.3,y:4.3,w:3.15,h:0.35,fontFace:BODY,fontSize:12,bold:true,color:NAVY,margin:0});
  s.addText(c[2],{x:cx[i]+0.3,y:4.75,w:3.15,h:1.4,fontFace:BODY,fontSize:11,color:INK,margin:0,lineSpacingMultiple:1.1});});
foot(s,"Excluded on purpose: real-time hiring counts (no dated snapshot) and vendor deployment claims sourced only to marketing.");

/* 6 — Demand inversion */
s=p.addSlide(); header(s,"Attention ≠ opportunity","The demand ranking is the near-inverse of market attractiveness.");
tag(s,"Week 5",MID);
s.addImage({path:A+"demand_index.png",x:0.7,y:1.7,w:6.6,h:3.4});
card(s,7.6,1.7,5.05,3.4);
s.addText("The inversion",{x:7.9,y:1.95,w:4.5,h:0.4,fontFace:HEAD,fontSize:17,bold:true,color:NAVY,margin:0});
s.addText([{text:"Aido Rover leads on attention (64). Sentinel Prime AI — the clearest near-term economics — comes ",options:{}},
{text:"last (41).",options:{bold:true,color:NAVY}}],{x:7.9,y:2.42,w:4.5,h:0.7,fontFace:BODY,fontSize:12,color:INK,margin:0,lineSpacingMultiple:1.1});
s.addText("These aren't contradictory. Search and news measure attention. Sizing measures money. The gap is where the commercial opportunity hides.",
 {x:7.9,y:3.2,w:4.5,h:0.9,fontFace:BODY,fontSize:12,color:INK,margin:0,lineSpacingMultiple:1.1});
card(s,7.9,4.15,4.45,0.75,"EEF3FB");
s.addText("Sentinel = strong asset, weak share of voice. A marketing problem — solvable.",
 {x:8.1,y:4.25,w:4.05,h:0.6,fontFace:BODY,fontSize:11.5,bold:true,color:NAVY,margin:0,valign:"middle",lineSpacingMultiple:1.05});
card(s,0.7,5.35,11.95,1.1,"FFFFFF");
s.addText([{text:"Two pain-points recur in every vertical:  ",options:{bold:true,color:NAVY}},
{text:"navigation reliability in cluttered real spaces, and the gap between demo behaviour and sustained field behaviour. Both are credibility problems — both answered by published field-reliability data.",options:{color:INK}}],
 {x:1.0,y:5.55,w:11.4,h:0.75,fontFace:BODY,fontSize:12,margin:0,lineSpacingMultiple:1.1});

/* 7 — Financials */
s=p.addSlide(); header(s,"Financial benchmarks — margin structure is the moat","Real FY2024 filings. The profitable peers aren't 'robotics companies' as the press means it.");
tag(s,"Week 6",MID);
const rows=[[{text:"Company",options:{bold:true,color:WHITE,fill:{color:MID}}},{text:"FY24 revenue",options:{bold:true,color:WHITE,fill:{color:MID}}},
{text:"Gross margin",options:{bold:true,color:WHITE,fill:{color:MID}}},{text:"Op margin",options:{bold:true,color:WHITE,fill:{color:MID}}},
{text:"What it tells us",options:{bold:true,color:WHITE,fill:{color:MID}}}]];
[["Teradyne","$2,820M","58.5%","+20.5%","Test & measurement — the profile robotics aspires to"],
["Cognex","$915M","68.0%","+7.0%","Machine vision — highest margin; a components business"],
["Symbotic","$1,790M","18.0%","−5.0%","Warehouse automation — scale, thin margin, integration economics"],
["iRobot","$681.8M","20.9%","−15.1%","Consumer robotics pure-play — losing money at scale"]].forEach((r,i)=>{
  const bg=i%2?"EEF2FA":"FFFFFF";
  rows.push(r.map((c,j)=>({text:c,options:{fill:{color:bg},color:j===0?NAVY:INK,bold:j===0,fontSize:11}})));});
s.addTable(rows,{x:0.7,y:1.75,w:11.95,colW:[1.5,1.5,1.35,1.3,6.3],rowH:0.5,border:{type:"solid",color:"D9E1F2",pt:0.5},margin:[3,6,3,6],fontFace:BODY});
card(s,0.7,4.6,11.95,1.85,"27306B");
s.addText("Figure AI's ~$1.68bn raise is ~2.5× iRobot's entire FY2024 revenue.",{x:1.1,y:4.82,w:11.1,h:0.4,fontFace:HEAD,fontSize:17,bold:true,color:ICE,margin:0});
s.addText("Capital is not the constraint in this industry — and it is not the moat either. What separates durable from fragile is whether you own something specific enough to charge for. For InGen: Sentinel-style deployments sold against a costed guard alternative have a defensible price story. Volume consumer hardware, on this evidence, does not.",
 {x:1.1,y:5.3,w:11.1,h:1.0,fontFace:BODY,fontSize:12.5,color:"D5DCF0",margin:0,lineSpacingMultiple:1.12});

/* 8 — BI platform */
s=p.addSlide(); header(s,"The BI platform","A warehouse an analytics team could actually query, and dashboards on top.");
tag(s,"Weeks 7–9",MID);
s.addImage({path:A+"er_diagram.png",x:0.7,y:1.7,w:4.2,h:4.9});
const BI=[["Star schema","3 facts (telemetry, tickets, pipeline) + 4 dimensions. Surrogate keys, documented grain, zero orphan FKs on every load."],
["100k rows, fixed seed","Synthetic — no internal data was available. It fixes the shape, not the facts."],
["Portable by design","The schema mirrors what an InGen team would hold, so the 15-query library and every dashboard move to real data unchanged."],
["3 tools, 3 jobs","Tableau (external market view) · Looker (operations) · Power BI (exec scorecard, 10 DAX measures)."]];
let by=1.85;
BI.forEach(b=>{s.addText(b[0],{x:5.15,y:by,w:7.4,h:0.35,fontFace:HEAD,fontSize:14,bold:true,color:NAVY,margin:0});
  s.addText(b[1],{x:5.15,y:by+0.38,w:7.45,h:0.85,fontFace:BODY,fontSize:11.5,color:INK,margin:0,lineSpacingMultiple:1.08});
  by+=1.25;});
foot(s,"Dashboards are built and specified; publishing to the live services runs through personal accounts and was not completed. No live URLs are claimed.");

/* 9 — Forecasts */
s=p.addSlide(); header(s,"Forecasts — models beat naive in 4 of 5","5 models per vertical, backtested on a held-out year. MASE < 1.0 beats seasonal-naive.");
tag(s,"Week 10",ORANGE);
const FR=[[{text:"Vertical",options:{bold:true,color:WHITE,fill:{color:MID}}},{text:"Best model",options:{bold:true,color:WHITE,fill:{color:MID}}},
{text:"MAPE",options:{bold:true,color:WHITE,fill:{color:MID}}},{text:"MASE",options:{bold:true,color:WHITE,fill:{color:MID}}}]];
[["Senpai — education","Prophet","3.1%","0.54"],["Aido Humanoid","ETS","2.6%","0.59"],
["Aido Rover — patrol","Prophet","2.5%","0.69"],["Sentinel — security","XGBoost","5.7%","0.96"],
["Fari — eldercare","ETS","4.1%","1.00"]].forEach((r,i)=>{const bg=i%2?"EEF2FA":"FFFFFF";
  FR.push(r.map((c,j)=>({text:c,options:{fill:{color:bg},color:j===0?NAVY:INK,bold:j===0,fontSize:11}})));});
s.addTable(FR,{x:0.7,y:1.75,w:6.1,colW:[2.5,1.4,1.1,1.1],rowH:0.46,border:{type:"solid",color:"D9E1F2",pt:0.5},margin:[3,6,3,6],fontFace:BODY});
card(s,0.7,4.6,6.1,1.9);
s.addText("No single model wins",{x:0.95,y:4.8,w:5.6,h:0.35,fontFace:HEAD,fontSize:14,bold:true,color:NAVY,margin:0});
s.addText("ETS twice, Prophet twice, XGBoost once. Keep a small portfolio and re-select per series rather than standardising on one algorithm. Fari sits at MASE 1.00 — no better than naive, and reported as such.",
 {x:0.95,y:5.2,w:5.65,h:1.15,fontFace:BODY,fontSize:11.5,color:INK,margin:0,lineSpacingMultiple:1.08});
s.addImage({path:A+"bass_humanoid.png",x:7.1,y:1.8,w:5.55,h:2.4});
card(s,7.1,4.4,5.55,2.1);
s.addText("Humanoid: shape, not level",{x:7.35,y:4.6,w:5.05,h:0.35,fontFace:HEAD,fontSize:14,bold:true,color:NAVY,margin:0});
s.addText("Bass curve fits Goldman's anchors exactly (20k/2025 → 250k/2030 → 1.4M/2035). But Morgan Stanley projects ~13M in service by 2035 — ~3× apart. That spread is why humanoid is a scenario, not a forecast.",
 {x:7.35,y:5.0,w:5.1,h:1.3,fontFace:BODY,fontSize:11.5,color:INK,margin:0,lineSpacingMultiple:1.08});
foot(s,"Target is search-interest momentum (0–100) — a relative demand read, not a unit forecast.");

/* 10 — Anomaly: the ceiling */
s=p.addSlide(); header(s,"Sentinel: you can't threshold your way out of model quality","Real public benchmarks (NAB — MIT; SKAB — GPL-3.0). No InGen data.");
tag(s,"Week 11",ORANGE);
card(s,0.7,1.7,11.95,1.5,"27306B");
s.addText("At 80% recall, the false-alarm rate bottoms out near 13% — whatever threshold we pick.",{x:1.1,y:1.9,w:11.1,h:0.4,fontFace:HEAD,fontSize:18,bold:true,color:ICE,margin:0});
s.addText("That ceiling is set by the model's discriminative power (AP ≈ 0.51), not by threshold policy. The stated 5% budget is unreachable at that recall — and we say so rather than quietly relaxing the bar.",
 {x:1.1,y:2.35,w:11.1,h:0.7,fontFace:BODY,fontSize:12.5,color:"D5DCF0",margin:0,lineSpacingMultiple:1.1});
s.addImage({path:A+"pr_curves.png",x:0.7,y:3.4,w:6.4,h:2.4});
card(s,7.35,3.4,5.3,2.4);
s.addText("5 detectors, identical splits",{x:7.6,y:3.6,w:4.8,h:0.35,fontFace:HEAD,fontSize:14,bold:true,color:NAVY,margin:0});
s.addText("Isolation Forest · One-Class SVM · LOF · AutoEncoder (PyOD) — against an EWMA control chart, the thing a plant engineer would already do.\n\nAutoEncoder leads NAB (F1 0.555), LOF leads SKAB (F1 0.545). Both clear the baseline — the bar that justifies the complexity.",
 {x:7.6,y:4.0,w:4.85,h:1.65,fontFace:BODY,fontSize:11,color:INK,margin:0,lineSpacingMultiple:1.06});
foot(s,"Fitted unsupervised on a clean warm-up window — how a Sentinel unit would be baselined at commissioning.");

/* 11 — Anomaly: the win */
s=p.addSlide(); header(s,"...but persistence cuts alert load 33×","The point-level rate is the wrong metric. Operators experience alerts, not readings.");
tag(s,"Week 11",ORANGE);
s.addImage({path:A+"operational_frontier.png",x:0.7,y:1.7,w:7.3,h:2.4});
const AL=[["16.35","false alerts / day","no persistence filter",AMBER],["0.50","false alerts / day","120-min persistence",GREEN]];
let ay=1.75;
AL.forEach(a=>{card(s,8.3,ay,4.35,1.15);
  s.addText(a[0],{x:8.55,y:ay+0.12,w:1.5,h:0.6,fontFace:HEAD,fontSize:26,bold:true,color:a[3],margin:0,valign:"middle"});
  s.addText(a[1],{x:10.1,y:ay+0.18,w:2.4,h:0.3,fontFace:BODY,fontSize:11.5,bold:true,color:INK,margin:0});
  s.addText(a[2],{x:10.1,y:ay+0.5,w:2.4,h:0.3,fontFace:BODY,fontSize:10.5,color:GREY,margin:0});
  ay+=1.25;});
card(s,8.3,4.25,4.35,1.4,"EEF3FB");
s.addText("Recall RISES to 88%",{x:8.55,y:4.45,w:3.85,h:0.35,fontFace:HEAD,fontSize:14,bold:true,color:GREEN,margin:0});
s.addText("All 4/4 real failures still caught. Real failures are sustained; false positives are isolated spikes.",
 {x:8.55,y:4.82,w:3.9,h:0.7,fontFace:BODY,fontSize:11,color:INK,margin:0,lineSpacingMultiple:1.05});
card(s,0.7,4.35,7.3,2.1);
s.addText("Adaptive thresholds lost — and the reason is the lesson",{x:0.95,y:4.55,w:6.8,h:0.35,fontFace:HEAD,fontSize:13.5,bold:true,color:NAVY,margin:0});
s.addText("Rolling quantile cut false alarms (13.4% → 3.3%) but collapsed recall (80% → 33%). NAB's failures run ~2 days, so a rolling baseline absorbs the anomaly and lifts the threshold exactly when it should hold. Survived a full parameter sweep; a baseline-freeze test confirmed the diagnosis. Verdict: fixed + persistence, re-baselined on a schedule.",
 {x:0.95,y:4.95,w:6.85,h:1.4,fontFace:BODY,fontSize:11,color:INK,margin:0,lineSpacingMultiple:1.06});
foot(s,"Recommendation: two tiers — fast (intrusion) + sustained (degradation). Thresholds transfer as a method, not as constants.");

/* 12 — Process: diagnosis */
s=p.addSlide(); header(s,"Support is a parts problem, not a people problem","Where the fleet-support cycle time actually goes.");
tag(s,"Week 12",ORANGE);
s.addImage({path:A+"wait_vs_service.png",x:0.7,y:1.7,w:7.1,h:2.8});
card(s,8.1,1.7,4.55,2.8);
s.addText("53%",{x:8.35,y:1.9,w:4.05,h:0.65,fontFace:HEAD,fontSize:34,bold:true,color:AMBER,margin:0});
s.addText("of all process time is Parts & dispatch — and 100% of it is unstaffed waiting.",
 {x:8.35,y:2.6,w:4.05,h:0.7,fontFace:BODY,fontSize:12.5,bold:true,color:INK,margin:0,lineSpacingMultiple:1.08});
s.addText("Nobody is working during it, so no amount of headcount shortens it. On-site repair, by contrast, is 48% queueing — which headcount can shorten. That distinction drives the whole recommendation.",
 {x:8.35,y:3.4,w:4.05,h:1.0,fontFace:BODY,fontSize:11,color:GREY,margin:0,lineSpacingMultiple:1.06});
card(s,0.7,4.75,11.95,1.75,"27306B");
s.addText("The drivers you'd reach for explain 4% of the variance. One structural fact explains 72%.",{x:1.1,y:4.95,w:11.1,h:0.4,fontFace:HEAD,fontSize:17,bold:true,color:ICE,margin:0});
s.addText("Product, severity, geography, weekday, team workload → R² = 0.04. Add \"did this ticket need a physical part?\" → R² = 0.72, and a dispatched ticket takes +578% longer [+555%, +601%]. Severity and queue length are real but second-order.",
 {x:1.1,y:5.4,w:11.1,h:0.9,fontFace:BODY,fontSize:12.5,color:"D5DCF0",margin:0,lineSpacingMultiple:1.12});

/* 13 — Process: the fix */
s=p.addSlide(); header(s,"What each fix would actually buy","8 replications per scenario, paired to identical seeds, 95% CIs.");
tag(s,"Week 12",ORANGE);
s.addImage({path:A+"scenario_comparison.png",x:0.7,y:1.7,w:11.95,h:2.3});
const SC=[["Regional parts buffer","−23%","P90 falls 64h → 47h. The tail is what customers complain about.",GREEN],
["+1 Field Ops FTE","−8%","Nearly zeroes field-queue wait (4.9h → 0.4h) — but that stage is only ~15% of the process.",MID],
["Reroute Tier-1 triage","−1.9%","Not significant. Triage is 4% of process time. The obvious lever does nothing.",AMBER]];
const sx=[0.7,4.85,9.0];
SC.forEach((c,i)=>{card(s,sx[i],4.25,3.75,2.2);
  s.addText(c[1],{x:sx[i]+0.3,y:4.42,w:3.15,h:0.5,fontFace:HEAD,fontSize:24,bold:true,color:c[3],margin:0});
  s.addText(c[0],{x:sx[i]+0.3,y:4.95,w:3.15,h:0.32,fontFace:HEAD,fontSize:13,bold:true,color:NAVY,margin:0});
  s.addText(c[2],{x:sx[i]+0.3,y:5.32,w:3.2,h:1.0,fontFace:BODY,fontSize:10.5,color:INK,margin:0,lineSpacingMultiple:1.06});});
foot(s,"Amdahl's law in practice: perfect staffing of a 15% stage cannot buy more than 15%. Both changes together: −29%.");

/* 14 — Limitations */
s=p.addSlide(); header(s,"What public data could not answer","Stated plainly, because the caveats matter as much as the findings.");
const LM=[["No internal InGen data — anywhere","Every figure is public or clearly-labelled synthetic. Market bottom-ups use assumed penetration, not observed conversion. These analyses are directional, not decision-grade."],
["The synthetic warehouse fixes shape, not fact","Weeks 7–9 and 12 rest on generated data. Nothing there measures InGen's actual fleet, support org or pipeline. Scorecard KPI targets are my assumptions."],
["Forecasts are momentum reads","A 0–100 search index answers \"is attention rising?\" — not \"how many units will we sell?\""],
["Week 12's numbers are model properties","The −23% is a simulation result, not a measurement. The method was validated (7/9 generating effects recovered); the number still needs real data."],
["Dashboards built, not published","Specs, extracts, prototypes and design log are complete. No live URLs exist, and none are claimed."],
["Left out on purpose","Competitor hiring counts (no dated snapshot), vendor deployment claims (marketing-sourced), frozen EV/Revenue multiples."]];
const lx=[0.7,6.75], ly=[1.55,3.2,4.85], lw=5.9, lh=1.5;
LM.forEach((l,i)=>{const x=lx[i%2],y=ly[Math.floor(i/2)];card(s,x,y,lw,lh);
  s.addText(l[0],{x:x+0.3,y:y+0.18,w:lw-0.6,h:0.36,fontFace:HEAD,fontSize:12.5,bold:true,color:AMBER,margin:0});
  s.addText(l[1],{x:x+0.3,y:y+0.58,w:lw-0.6,h:0.82,fontFace:BODY,fontSize:10.5,color:INK,margin:0,lineSpacingMultiple:1.04});});
foot(s,"Week 11 is the exception that proves the point: real public benchmarks were reachable, and its results are measurements on real sensor data.");

/* 15 — Recommendations + the ask */
s=p.addSlide(); s.background={color:NAVY};
s.addText("What I'd do next",{x:0.9,y:0.55,w:11.5,h:0.6,fontFace:HEAD,fontSize:27,bold:true,color:WHITE,margin:0});
const RC=[["1","Market Sentinel Prime AI harder","First on market attractiveness, last on demand signal — the widest gap in the portfolio."],
["2","Fund a regional parts buffer before hiring","−23% vs −8%. Parts is 53% of process time and 100% waiting."],
["3","Ship two-tier alerting on Sentinel","Fast tier for intrusion; 120-min sustained tier at ~0.5 false alerts/day."],
["4","Treat humanoid as an option, not a plan","Credible analysts differ ~3× on 2035. Scenario-bound it."]];
let ry=1.35;
RC.forEach(r=>{card(s,0.9,ry,7.1,1.05,"27306B");
  circ(s,1.15,ry+0.25,0.55,MID,r[0],15);
  s.addText(r[1],{x:1.9,y:ry+0.14,w:5.9,h:0.32,fontFace:HEAD,fontSize:14,bold:true,color:ICE,margin:0});
  s.addText(r[2],{x:1.9,y:ry+0.5,w:5.95,h:0.45,fontFace:BODY,fontSize:10.5,color:"C9D2EC",margin:0,lineSpacingMultiple:1.04});
  ry+=1.15;});
card(s,8.3,1.35,4.35,4.45,"27306B");
s.addText("The one ask",{x:8.6,y:1.6,w:3.8,h:0.4,fontFace:HEAD,fontSize:18,bold:true,color:WHITE,margin:0});
s.addText("Read access to one small, anonymized slice of real InGen data.",
 {x:8.6,y:2.1,w:3.85,h:0.7,fontFace:HEAD,fontSize:14,bold:true,color:ICE,margin:0,lineSpacingMultiple:1.1});
s.addText("The synthetic warehouse already matches the intended schema, so real data slots in with minimal rework — and it dissolves most of the limitations at once:\n\n· the warehouse becomes real\n· the dashboards become operational\n· Week 12's diagnostic becomes a measurement\n· the forecasts gain a calibration target",
 {x:8.6,y:2.95,w:3.85,h:2.7,fontFace:BODY,fontSize:11,color:"C9D2EC",margin:0,lineSpacingMultiple:1.15});
s.addText("Weeks 1–13 complete  ·  13 self-contained modules, each with README, plan, status and tests  ·  HANDOFF.md documents how to pick up every workstream  ·  thank you.",
 {x:0.9,y:6.25,w:11.6,h:0.5,fontFace:BODY,fontSize:11.5,italic:true,color:"8E9AC2",margin:0});

p.writeFile({fileName:"Capstone_Executive_Deck.pptx"}).then(()=>console.log("written")).catch(e=>console.log("ERR",e));
