import streamlit as st


def _panda_landing_html() -> str:
    """Full KFP Po face — SVG with 5 cycling expressions + per-emotion orbital dots."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  html,body{
    background:transparent;width:100%;height:100%;
    display:flex;flex-direction:column;align-items:center;
    justify-content:center;overflow:hidden;
    font-family:'Segoe UI',system-ui,sans-serif;
  }
  /* ── Entrance bounce ── */
  @keyframes entrance{
    0%  {opacity:0;transform:scale(.25)translateY(-80px)rotate(-18deg)}
    60% {transform:scale(1.06)translateY(8px)rotate(2deg);opacity:1}
    78% {transform:scale(.97)translateY(-4px)rotate(-.4deg)}
    100%{transform:scale(1)translateY(0)rotate(0);opacity:1}
  }
  /* ── Gentle float ── */
  @keyframes float{
    0%,100%{transform:translateY(0)}
    50%    {transform:translateY(-10px)}
  }
  /* ── Pupils wander ── */
  @keyframes pupilL{
    0%,12%{transform:translate(0,0)}20%,35%{transform:translate(4px,3px)}
    45%,60%{transform:translate(-4px,-3px)}70%,84%{transform:translate(3px,-4px)}
    92%,100%{transform:translate(0,0)}
  }
  @keyframes pupilR{
    0%,12%{transform:translate(0,0)}20%,35%{transform:translate(-4px,3px)}
    45%,60%{transform:translate(4px,-3px)}70%,84%{transform:translate(-2px,-4px)}
    92%,100%{transform:translate(0,0)}
  }
  /* ── Blink ── */
  @keyframes blink{
    0%,84%,100%{transform:scaleY(1)}
    88%        {transform:scaleY(.06)}
  }
  /* ── 50s expression loop: 8s on, 2s crossfade ── */
  @keyframes eHappy  {0%,2%{opacity:1}16%{opacity:1}20%{opacity:0}99%{opacity:0}100%{opacity:1}}
  @keyframes eExcited{0%,18%{opacity:0}22%{opacity:1}36%{opacity:1}40%{opacity:0}100%{opacity:0}}
  @keyframes eThink  {0%,38%{opacity:0}42%{opacity:1}56%{opacity:1}60%{opacity:0}100%{opacity:0}}
  @keyframes eWink   {0%,58%{opacity:0}62%{opacity:1}76%{opacity:1}80%{opacity:0}100%{opacity:0}}
  @keyframes eDeter  {0%,78%{opacity:0}82%{opacity:1}95%{opacity:1}99%{opacity:0}100%{opacity:0}}
  /* same keyframes reused for labels / quotes */
  @keyframes lblHappy  {0%,2%{opacity:.9}16%{opacity:.9}20%{opacity:0}99%{opacity:0}100%{opacity:.9}}
  @keyframes lblExcited{0%,18%{opacity:0}22%{opacity:.9}36%{opacity:.9}40%{opacity:0}100%{opacity:0}}
  @keyframes lblThink  {0%,38%{opacity:0}42%{opacity:.9}56%{opacity:.9}60%{opacity:0}100%{opacity:0}}
  @keyframes lblWink   {0%,58%{opacity:0}62%{opacity:.9}76%{opacity:.9}80%{opacity:0}100%{opacity:0}}
  @keyframes lblDeter  {0%,78%{opacity:0}82%{opacity:.9}95%{opacity:.9}99%{opacity:0}100%{opacity:0}}
  /* ── Dot orbit spin ── */
  @keyframes spin{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}
  @keyframes spinRev{from{transform:rotate(0deg)}to{transform:rotate(-360deg)}}
  /* ── Dot pulse ── */
  @keyframes dotPulse{0%,100%{r:4;opacity:.7}50%{r:6;opacity:1}}
  /* ── Thought bubble pop ── */
  @keyframes bubblePop{0%,100%{transform:scale(1)}50%{transform:scale(1.18)}}
  /* ── Speed-line flicker ── */
  @keyframes speedFlicker{0%,100%{opacity:.5}50%{opacity:1}}

  .wrap{animation:entrance 1s cubic-bezier(.34,1.56,.64,1) .2s both;
        display:flex;flex-direction:column;align-items:center;gap:8px}
  .floater{animation:float 4s ease-in-out 1.4s infinite}
  .pupil-l{transform-box:fill-box;transform-origin:center;animation:pupilL 11s ease-in-out 2s infinite}
  .pupil-r{transform-box:fill-box;transform-origin:center;animation:pupilR 11s ease-in-out 2.6s infinite}
  .lid-l{transform-box:fill-box;transform-origin:50% 40%;animation:blink 6.5s ease-in-out 3s infinite}
  .lid-r{transform-box:fill-box;transform-origin:50% 40%;animation:blink 6.5s ease-in-out 3.3s infinite}

  .e-happy  {animation:eHappy   50s ease-in-out 2.2s infinite}
  .e-excited{animation:eExcited 50s ease-in-out 2.2s infinite;opacity:0}
  .e-think  {animation:eThink   50s ease-in-out 2.2s infinite;opacity:0}
  .e-wink   {animation:eWink    50s ease-in-out 2.2s infinite;opacity:0}
  .e-deter  {animation:eDeter   50s ease-in-out 2.2s infinite;opacity:0}

  /* orbital container must be centred on the face */
  .orbit-happy  {animation:eHappy   50s ease-in-out 2.2s infinite}
  .orbit-excited{animation:eExcited 50s ease-in-out 2.2s infinite;opacity:0}
  .orbit-think  {animation:eThink   50s ease-in-out 2.2s infinite;opacity:0}
  .orbit-wink   {animation:eWink    50s ease-in-out 2.2s infinite;opacity:0}
  .orbit-deter  {animation:eDeter   50s ease-in-out 2.2s infinite;opacity:0}

  .spin    {transform-box:fill-box;transform-origin:center;animation:spin 4s linear infinite}
  .spin-rev{transform-box:fill-box;transform-origin:center;animation:spinRev 6s linear infinite}
  .dp{animation:dotPulse 1.6s ease-in-out infinite}
  .bp{animation:bubblePop 1.2s ease-in-out infinite}
  .sf{animation:speedFlicker .8s ease-in-out infinite}
  /* right base arm hides whilst thinking arm is shown */
  @keyframes hideForThink{0%,38%{opacity:1}42%{opacity:0}56%{opacity:0}60%{opacity:1}100%{opacity:1}}
  .base-arm-right{animation:hideForThink 50s ease-in-out 2.2s infinite}

  /* label pill */
  .lbl{
    font-size:12px;font-weight:800;letter-spacing:.9px;text-transform:uppercase;
    color:#2D6A4F;background:#fff;border:2px solid #2D6A4F;
    border-radius:20px;padding:4px 16px;position:absolute;
    box-shadow:0 2px 8px rgba(45,106,79,.15);
  }
  .lbl-happy  {animation:lblHappy   50s ease-in-out 2.2s infinite}
  .lbl-excited{animation:lblExcited 50s ease-in-out 2.2s infinite;opacity:0}
  .lbl-think  {animation:lblThink   50s ease-in-out 2.2s infinite;opacity:0}
  .lbl-wink   {animation:lblWink    50s ease-in-out 2.2s infinite;opacity:0}
  .lbl-deter  {animation:lblDeter   50s ease-in-out 2.2s infinite;opacity:0}
  .labels{position:relative;height:28px;width:160px;display:flex;align-items:center;justify-content:center}

  /* quote */
  .quotebox{position:relative;height:100px;width:275px;display:flex;align-items:flex-start;justify-content:center;margin-top:4px}
  .q{position:absolute;top:0;text-align:center;padding:0 6px;width:100%}
  .qtext{display:block;font-size:13px;color:#444;line-height:1.6;font-style:italic}
  .qattr{display:block;font-size:11.5px;color:#2D6A4F;margin-top:5px;font-weight:800;letter-spacing:.3px}
  .q-happy  {animation:lblHappy   50s ease-in-out 2.2s infinite}
  .q-excited{animation:lblExcited 50s ease-in-out 2.2s infinite;opacity:0}
  .q-think  {animation:lblThink   50s ease-in-out 2.2s infinite;opacity:0}
  .q-wink   {animation:lblWink    50s ease-in-out 2.2s infinite;opacity:0}
  .q-deter  {animation:lblDeter   50s ease-in-out 2.2s infinite;opacity:0}

  @media(prefers-reduced-motion:reduce){
    .wrap,.floater,.spin,.spin-rev{animation:none!important;opacity:1!important;transform:none!important}
    .e-happy,.orbit-happy,.lbl-happy,.q-happy{animation:none;opacity:1}
    .e-excited,.e-think,.e-wink,.e-deter{display:none}
    .orbit-excited,.orbit-think,.orbit-wink,.orbit-deter{display:none}
    .pupil-l,.pupil-r,.lid-l,.lid-r,.dp,.bp,.sf{animation:none}
    .base-arm-right{animation:none;opacity:1}
    .lbl-excited,.lbl-think,.lbl-wink,.lbl-deter{display:none}
    .q-excited,.q-think,.q-wink,.q-deter{display:none}
  }
</style>
</head>
<body>
<div class="wrap">

  <!-- ── SVG: panda + arms + per-emotion orbital decorations ── -->
  <div class="floater">
  <svg viewBox="-90 0 460 310" width="330" height="292" xmlns="http://www.w3.org/2000/svg">

    <!-- ═══ ORBITAL DECORATIONS (rendered behind the face) ═══ -->

    <!-- 1. HAPPY orbit — soft pink hearts / sparkle ring -->
    <g class="orbit-happy" opacity="1">
      <g class="spin" style="transform-origin:140px 170px">
        <circle cx="140" cy="170" r="155" fill="none" stroke="#FFB3BA" stroke-width="1.5"
                stroke-dasharray="8 10" opacity=".55"/>
        <circle cx="295" cy="170" r="5" fill="#FFB3BA" opacity=".8" class="dp"/>
        <circle cx="140" cy="15"  r="4" fill="#FFB3BA" opacity=".7" class="dp" style="animation-delay:.4s"/>
        <circle cx="-15" cy="170" r="5" fill="#FFB3BA" opacity=".8" class="dp" style="animation-delay:.8s"/>
        <circle cx="140" cy="325" r="4" fill="#FFB3BA" opacity=".7" class="dp" style="animation-delay:1.2s"/>
        <!-- sparkle stars -->
        <text x="33"  y="55"  font-size="16" opacity=".7">✨</text>
        <text x="232" y="55"  font-size="16" opacity=".7">✨</text>
        <text x="33"  y="305" font-size="16" opacity=".6">✨</text>
        <text x="232" y="305" font-size="16" opacity=".6">✨</text>
      </g>
    </g>

    <!-- 2. EXCITED orbit — fast dual rings + energy circles -->
    <g class="orbit-excited" opacity="0">
      <g class="spin" style="transform-origin:140px 170px">
        <circle cx="140" cy="170" r="148" fill="none" stroke="#FFB3BA" stroke-width="2"
                stroke-dasharray="12 8" opacity=".6"/>
        <circle cx="288" cy="170" r="6" fill="#FFB3BA" opacity=".9" class="dp"/>
        <circle cx="140" cy="22"  r="6" fill="#FFB3BA" opacity=".9" class="dp" style="animation-delay:.3s"/>
      </g>
      <g class="spin-rev" style="transform-origin:140px 170px">
        <circle cx="140" cy="170" r="162" fill="none" stroke="#FFD6A5" stroke-width="1.5"
                stroke-dasharray="6 14" opacity=".5"/>
        <circle cx="302" cy="170" r="5" fill="#FFD6A5" opacity=".8" class="dp" style="animation-delay:.5s"/>
        <circle cx="140" cy="8"   r="5" fill="#FFD6A5" opacity=".7" class="dp" style="animation-delay:.9s"/>
      </g>
      <!-- energy burst lines -->
      <line x1="-55" y1="80"  x2="-30" y2="95"  stroke="#FFB3BA" stroke-width="2.5" stroke-linecap="round" class="sf"/>
      <line x1="-65" y1="110" x2="-38" y2="112" stroke="#FFD6A5" stroke-width="2"   stroke-linecap="round" class="sf" style="animation-delay:.2s"/>
      <line x1="-55" y1="140" x2="-30" y2="128" stroke="#FFB3BA" stroke-width="2"   stroke-linecap="round" class="sf" style="animation-delay:.4s"/>
      <line x1="335" y1="80"  x2="310" y2="95"  stroke="#FFB3BA" stroke-width="2.5" stroke-linecap="round" class="sf"/>
      <line x1="345" y1="110" x2="318" y2="112" stroke="#FFD6A5" stroke-width="2"   stroke-linecap="round" class="sf" style="animation-delay:.3s"/>
      <line x1="335" y1="140" x2="310" y2="128" stroke="#FFB3BA" stroke-width="2"   stroke-linecap="round" class="sf" style="animation-delay:.6s"/>
    </g>

    <!-- 3. THINK orbit — slow dashed ring + floating thought bubbles -->
    <g class="orbit-think" opacity="0">
      <g class="spin-rev" style="transform-origin:140px 170px;animation-duration:10s">
        <circle cx="140" cy="170" r="152" fill="none" stroke="#A8DADC" stroke-width="1.5"
                stroke-dasharray="4 12" opacity=".55"/>
        <circle cx="292" cy="170" r="5" fill="#A8DADC" opacity=".8" class="dp"/>
        <circle cx="140" cy="18"  r="4" fill="#A8DADC" opacity=".7" class="dp" style="animation-delay:.6s"/>
        <circle cx="-12" cy="170" r="5" fill="#A8DADC" opacity=".8" class="dp" style="animation-delay:1.1s"/>
        <circle cx="140" cy="322" r="4" fill="#A8DADC" opacity=".6" class="dp" style="animation-delay:1.6s"/>
      </g>
      <!-- rising thought bubbles left side -->
      <circle cx="-42" cy="200" r="4.5" fill="#CCCCCC" opacity=".6" class="bp"/>
      <circle cx="-55" cy="175" r="6.5" fill="#BBBBBB" opacity=".6" class="bp" style="animation-delay:.4s"/>
      <circle cx="-45" cy="148" r="9"   fill="#AAAAAA" opacity=".6" class="bp" style="animation-delay:.8s"/>
      <text x="-52" y="152" font-size="11" text-anchor="middle" fill="#555">💡</text>
    </g>

    <!-- 4. WINK orbit — cheeky arc + sparkles one side -->
    <g class="orbit-wink" opacity="0">
      <g class="spin" style="transform-origin:140px 170px;animation-duration:7s">
        <circle cx="140" cy="170" r="150" fill="none" stroke="#B7E4C7" stroke-width="1.5"
                stroke-dasharray="10 7" opacity=".55"/>
        <circle cx="290" cy="170" r="5"  fill="#B7E4C7" opacity=".8" class="dp"/>
        <circle cx="140" cy="20"  r="4"  fill="#B7E4C7" opacity=".7" class="dp" style="animation-delay:.5s"/>
      </g>
      <!-- cheeky wink stars right side -->
      <text x="305" y="120" font-size="18" opacity=".75" class="bp">★</text>
      <text x="320" y="155" font-size="13" opacity=".6"  class="bp" style="animation-delay:.3s">✦</text>
      <text x="308" y="195" font-size="15" opacity=".65" class="bp" style="animation-delay:.6s">✨</text>
    </g>

    <!-- 5. DETERMINED orbit — heavy dashes + speed lines -->
    <g class="orbit-deter" opacity="0">
      <g class="spin" style="transform-origin:140px 170px;animation-duration:3s">
        <circle cx="140" cy="170" r="150" fill="none" stroke="#1A1A1A" stroke-width="2"
                stroke-dasharray="16 6" opacity=".2"/>
        <circle cx="290" cy="170" r="6" fill="#1A1A1A" opacity=".35" class="dp"/>
        <circle cx="140" cy="20"  r="6" fill="#1A1A1A" opacity=".3"  class="dp" style="animation-delay:.4s"/>
        <circle cx="-10" cy="170" r="6" fill="#1A1A1A" opacity=".3"  class="dp" style="animation-delay:.8s"/>
        <circle cx="140" cy="320" r="6" fill="#1A1A1A" opacity=".3"  class="dp" style="animation-delay:1.2s"/>
      </g>
      <!-- speed lines left -->
      <line x1="-68" y1="140" x2="-30" y2="140" stroke="#1A1A1A" stroke-width="3" stroke-linecap="round" opacity=".35" class="sf"/>
      <line x1="-72" y1="160" x2="-34" y2="157" stroke="#1A1A1A" stroke-width="2" stroke-linecap="round" opacity=".25" class="sf" style="animation-delay:.15s"/>
      <line x1="-70" y1="178" x2="-32" y2="172" stroke="#1A1A1A" stroke-width="2" stroke-linecap="round" opacity=".2"  class="sf" style="animation-delay:.3s"/>
      <!-- speed lines right -->
      <line x1="348" y1="140" x2="310" y2="140" stroke="#1A1A1A" stroke-width="3" stroke-linecap="round" opacity=".35" class="sf"/>
      <line x1="352" y1="160" x2="314" y2="157" stroke="#1A1A1A" stroke-width="2" stroke-linecap="round" opacity=".25" class="sf" style="animation-delay:.2s"/>
      <line x1="350" y1="178" x2="312" y2="172" stroke="#1A1A1A" stroke-width="2" stroke-linecap="round" opacity=".2"  class="sf" style="animation-delay:.4s"/>
    </g>

    <!-- ═══ PANDA ARMS (inside SVG, arching out left & right) ═══ -->
    <!-- Left arm — rounded rect rotated to arch left-down -->
    <rect x="14" y="188" width="24" height="72" rx="12"
          fill="#1A1A1A" transform="rotate(-28 26 188)"/>
    <!-- Left paw -->
    <ellipse cx="5" cy="246" rx="14" ry="10" fill="#1A1A1A" transform="rotate(-28 5 246)"/>
    <g class="base-arm-right">
    <!-- Right arm -->
    <rect x="242" y="188" width="24" height="72" rx="12"
          fill="#1A1A1A" transform="rotate(28 254 188)"/>
    <!-- Right paw -->
    <ellipse cx="275" cy="246" rx="14" ry="10" fill="#1A1A1A" transform="rotate(28 275 246)"/>
    </g>

    <!-- ═══ DROP SHADOW ═══ -->
    <ellipse cx="140" cy="292" rx="56" ry="6" fill="#1A1A1A" opacity=".06">
      <animate attributeName="rx" values="56;44;56" dur="4s" begin="1.4s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values=".06;.03;.06" dur="4s" begin="1.4s" repeatCount="indefinite"/>
    </ellipse>

    <!-- ═══ PANDA HEAD ═══ -->
    <!-- Ears -->
    <circle cx="52"  cy="64" r="46" fill="#1A1A1A"/>
    <circle cx="228" cy="64" r="46" fill="#1A1A1A"/>
    <circle cx="52"  cy="64" r="28" fill="#2D2D2D" opacity=".45"/>
    <circle cx="228" cy="64" r="28" fill="#2D2D2D" opacity=".45"/>
    <!-- Face -->
    <ellipse cx="140" cy="172" rx="118" ry="116" fill="#EFEFED"/>
    <ellipse cx="140" cy="170" rx="114" ry="112" fill="#FFFFFF"/>
    <!-- cheek shading -->
    <ellipse cx="30"  cy="188" rx="22" ry="16" fill="#E8E8E6" opacity=".8"/>
    <ellipse cx="250" cy="188" rx="22" ry="16" fill="#E8E8E6" opacity=".8"/>
    <!-- Eye patches -->
    <ellipse cx="88"  cy="138" rx="46" ry="42" fill="#1A1A1A" transform="rotate(-10 88 138)"/>
    <ellipse cx="192" cy="138" rx="46" ry="42" fill="#1A1A1A" transform="rotate(10 192 138)"/>
    <!-- Sclera + blink -->
    <g class="lid-l"><ellipse cx="90"  cy="133" rx="27" ry="26" fill="#FFFFFF"/></g>
    <g class="lid-r"><ellipse cx="190" cy="133" rx="27" ry="26" fill="#FFFFFF"/></g>
    <!-- Pupils -->
    <g class="pupil-l">
      <circle cx="92"  cy="133" r="14" fill="#1A1A1A"/>
      <circle cx="98"  cy="126" r="6"  fill="#FFFFFF"/>
      <circle cx="87"  cy="138" r="3"  fill="#FFFFFF" opacity=".5"/>
    </g>
    <g class="pupil-r">
      <circle cx="188" cy="133" r="14" fill="#1A1A1A"/>
      <circle cx="194" cy="126" r="6"  fill="#FFFFFF"/>
      <circle cx="183" cy="138" r="3"  fill="#FFFFFF" opacity=".5"/>
    </g>
    <!-- Nose -->
    <ellipse cx="140" cy="164" rx="6" ry="8" fill="#E8E8E8"/>
    <ellipse cx="140" cy="178" rx="17" ry="13" fill="#1A1A1A"/>
    <ellipse cx="133" cy="174" rx="6"  ry="4"  fill="#3A3A3A" opacity=".4"/>
    <line x1="128" y1="186" x2="140" y2="193" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="round"/>
    <line x1="152" y1="186" x2="140" y2="193" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="round"/>

    <!-- ═══ EXPRESSIONS ═══ -->
    <!-- 1. HAPPY -->
    <g class="e-happy">
      <path d="M 96 210 Q 140 248 184 210" stroke="#1A1A1A" stroke-width="5.5" fill="none" stroke-linecap="round"/>
      <ellipse cx="54"  cy="204" rx="18" ry="11" fill="#FFB3BA" opacity=".45"/>
      <ellipse cx="226" cy="204" rx="18" ry="11" fill="#FFB3BA" opacity=".45"/>
    </g>
    <!-- 2. EXCITED -->
    <g class="e-excited">
      <path d="M 88 208 Q 140 256 192 208" stroke="#1A1A1A" stroke-width="6" fill="none" stroke-linecap="round"/>
      <path d="M 89 209 Q 140 252 191 209 L 188 224 Q 140 252 92 224 Z" fill="#FFFFFF" stroke="#D4D4D4" stroke-width="1.2"/>
      <line x1="115" y1="210" x2="115" y2="223" stroke="#D4D4D4" stroke-width="1.5"/>
      <line x1="140" y1="210" x2="140" y2="224" stroke="#D4D4D4" stroke-width="1.5"/>
      <line x1="165" y1="210" x2="165" y2="223" stroke="#D4D4D4" stroke-width="1.5"/>
      <path d="M 54  108 Q 76  94  100 100" stroke="#1A1A1A" stroke-width="5.5" fill="none" stroke-linecap="round"/>
      <path d="M 180 100 Q 204 94  226 108" stroke="#1A1A1A" stroke-width="5.5" fill="none" stroke-linecap="round"/>
      <ellipse cx="42"  cy="196" rx="24" ry="15" fill="#FFB3BA" opacity=".55"/>
      <ellipse cx="238" cy="196" rx="24" ry="15" fill="#FFB3BA" opacity=".55"/>
    </g>
    <!-- 3. THINKING — matches 🤔: RIGHT brow raised, right paw touching chin -->
    <g class="e-think">
      <!-- smirk mouth -->
      <path d="M 100 214 Q 128 230 158 212" stroke="#1A1A1A" stroke-width="5" fill="none" stroke-linecap="round"/>
      <!-- LEFT brow: flat / slightly lowered -->
      <path d="M 52  112 Q 72  106 96 110"  stroke="#1A1A1A" stroke-width="5.5" fill="none" stroke-linecap="round"/>
      <!-- RIGHT brow: raised HIGH — key 🤔 feature -->
      <path d="M 184  96 Q 206  84 228  96" stroke="#1A1A1A" stroke-width="5.5" fill="none" stroke-linecap="round"/>
      <!-- Right arm curving from shoulder (lower-right) up to chin -->
      <path d="M 238 292 Q 232 268 215 256 Q 200 254 178 268"
            stroke="#1A1A1A" stroke-width="24" fill="none"
            stroke-linecap="round" stroke-linejoin="round"/>
      <!-- Paw / fist resting at chin -->
      <ellipse cx="168" cy="270" rx="22" ry="17" fill="#1A1A1A"/>
      <!-- Knuckle highlights -->
      <circle cx="160" cy="265" r="5" fill="#2D2D2D" opacity=".4"/>
      <circle cx="171" cy="261" r="5" fill="#2D2D2D" opacity=".4"/>
    </g>
    <!-- 4. WINK -->
    <g class="e-wink">
      <ellipse cx="190" cy="133" rx="27" ry="26" fill="#1A1A1A"/>
      <path d="M 165 133 Q 190 120 215 133" stroke="#FFFFFF" stroke-width="5.5" fill="none" stroke-linecap="round"/>
      <path d="M 165 128 Q 190 117 215 128" stroke="#1A1A1A" stroke-width="2" fill="none" stroke-linecap="round"/>
      <path d="M 100 212 Q 140 242 174 218" stroke="#1A1A1A" stroke-width="5" fill="none" stroke-linecap="round"/>
      <ellipse cx="230" cy="196" rx="21" ry="13" fill="#FFB3BA" opacity=".62"/>
    </g>
    <!-- 5. DETERMINED -->
    <g class="e-deter">
      <line x1="102" y1="218" x2="178" y2="218" stroke="#1A1A1A" stroke-width="5.5" stroke-linecap="round"/>
      <path d="M 52  102 Q 72  95  96 104"  stroke="#1A1A1A" stroke-width="6" fill="none" stroke-linecap="round"/>
      <path d="M 184 104 Q 208 95 228 102"  stroke="#1A1A1A" stroke-width="6" fill="none" stroke-linecap="round"/>
      <line x1="96"  y1="104" x2="104" y2="112" stroke="#1A1A1A" stroke-width="3" stroke-linecap="round"/>
      <line x1="184" y1="104" x2="176" y2="112" stroke="#1A1A1A" stroke-width="3" stroke-linecap="round"/>
    </g>

  </svg>
  </div>

  <!-- Label pill -->
  <div class="labels">
    <span class="lbl lbl-happy"  >😊 Happy</span>
    <span class="lbl lbl-excited">🎉 Excited!</span>
    <span class="lbl lbl-think"  >🤔 Thinking…</span>
    <span class="lbl lbl-wink"   >😉 Wink</span>
    <span class="lbl lbl-deter"  >💪 Determined</span>
  </div>

  <!-- Quote -->
  <div class="quotebox">
    <div class="q q-happy">
      <span class="qtext">"Happiness is not something ready-made.<br>It comes from your own actions."</span>
      <span class="qattr">— Dalai Lama XIV</span>
    </div>
    <div class="q q-excited">
      <span class="qtext">"Nothing great in the world was accomplished without passion."</span>
      <span class="qattr">— G. W. F. Hegel</span>
    </div>
    <div class="q q-think">
      <span class="qtext">"The measure of intelligence is the ability to change."</span>
      <span class="qattr">— Albert Einstein</span>
    </div>
    <div class="q q-wink">
      <span class="qtext">"Life is too important to be taken seriously."</span>
      <span class="qattr">— Oscar Wilde</span>
    </div>
    <div class="q q-deter">
      <span class="qtext">"It does not matter how slowly you go as long as you do not stop."</span>
      <span class="qattr">— Confucius</span>
    </div>
  </div>

</div>
</body>
</html>"""


# ── Panda Helper — Requirements Form (welcome / thinking / bye states) ────────


def _robot_html(state: str) -> str:
    """Animated panda face helper for the requirements form page — matches landing panda style."""
    _messages = {
        "welcome": (
            "Hey! 🐼 Let's capture your<br>project requirements.<br>Fill in the form!"
        ),
        "thinking": (
            "Hmm, thinking along<br>with you… 🤔"
            "<br><span class='dots'><span>.</span><span>.</span><span>.</span></span>"
        ),
        "bye": (
            "Awesome! 🎉<br>Requirements saved!<br>"
            "Download your PDF below!<br>Time to learn! 🐼"
        ),
    }
    msg = _messages.get(state, _messages["welcome"])
    # Expression visibility per state
    s_happy   = "1" if state == "welcome"  else "0"
    s_think   = "1" if state == "thinking" else "0"
    s_excited = "1" if state == "bye"      else "0"

    wave_l     = "waveL .7s ease-in-out infinite" if state in ("welcome", "bye") else "none"
    wave_r     = "waveR .7s ease-in-out infinite" if state in ("welcome", "bye") else "none"
    body_anim  = "thinkBob 2s ease-in-out infinite" if state == "thinking" else "float 4s ease-in-out 1.2s infinite"

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  html,body{{
    background:transparent;width:100%;height:100%;
    display:flex;flex-direction:column;align-items:center;
    justify-content:flex-start;padding-top:18px;overflow:hidden;
    font-family:'Segoe UI',system-ui,sans-serif;
  }}
  @keyframes fadeUp{{from{{opacity:0;transform:translateY(-10px)}}to{{opacity:1;transform:translateY(0)}}}}
  @keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-10px)}}}}
  @keyframes thinkBob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-8px)}}}}
  @keyframes waveR{{0%,100%{{transform:rotate(-15deg)}}50%{{transform:rotate(45deg)}}}}
  @keyframes waveL{{0%,100%{{transform:rotate(15deg)}}50%{{transform:rotate(-45deg)}}}}
  @keyframes blink{{0%,85%,100%{{transform:scaleY(1)}}89%{{transform:scaleY(.06)}}}}
  @keyframes pupilW{{0%,100%{{transform:translate(0,0)}}40%{{transform:translate(3px,2px)}}80%{{transform:translate(-3px,-2px)}}}}
  .dots span{{display:inline-block;animation:dotBounce 1.2s infinite;font-size:15px;font-weight:700;color:#2D6A4F}}
  .dots span:nth-child(2){{animation-delay:.2s}}
  .dots span:nth-child(3){{animation-delay:.4s}}
  @keyframes dotBounce{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-5px)}}}}
  @media(prefers-reduced-motion:reduce){{*{{animation:none!important;opacity:1!important;transform:none!important}}}}
</style></head>
<body>
  <!-- Speech bubble — bamboo green to match panda theme -->
  <div style="
    background:#fff;border:2.5px solid #2D6A4F;border-radius:20px;
    padding:13px 20px;font-size:13.5px;color:#2D6A4F;
    max-width:230px;text-align:center;line-height:1.6;
    box-shadow:0 4px 18px rgba(45,106,79,.18);
    position:relative;margin-bottom:16px;font-weight:600;
    animation:fadeUp .45s ease forwards;
  ">{msg}
    <span style="position:absolute;bottom:-13px;left:50%;transform:translateX(-50%);
      border:10px solid transparent;border-top-color:#2D6A4F;"></span>
  </div>
  <!-- Panda face + arms -->
  <div style="animation:{body_anim};display:flex;align-items:flex-end;">
    <!-- Left arm -->
    <div style="
      width:22px;height:62px;background:#1A1A1A;border-radius:11px;
      transform-origin:top center;animation:{wave_l};
      align-self:flex-end;margin-bottom:14px;margin-right:-5px;
    "></div>
    <!-- Panda SVG (same palette as landing page) -->
    <svg viewBox="0 0 280 290" width="195" height="203" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="140" cy="285" rx="58" ry="6.5" fill="#1A1A1A" opacity=".06"/>
      <!-- Ears -->
      <circle cx="52"  cy="64" r="46" fill="#1A1A1A"/>
      <circle cx="228" cy="64" r="46" fill="#1A1A1A"/>
      <circle cx="52"  cy="64" r="28" fill="#2D2D2D" opacity=".45"/>
      <circle cx="228" cy="64" r="28" fill="#2D2D2D" opacity=".45"/>
      <!-- Head -->
      <ellipse cx="140" cy="172" rx="118" ry="116" fill="#EFEFED"/>
      <ellipse cx="140" cy="170" rx="114" ry="112" fill="#FFFFFF"/>
      <ellipse cx="30"  cy="188" rx="22" ry="16" fill="#E8E8E6" opacity=".8"/>
      <ellipse cx="250" cy="188" rx="22" ry="16" fill="#E8E8E6" opacity=".8"/>
      <!-- Eye patches -->
      <ellipse cx="88"  cy="138" rx="46" ry="42" fill="#1A1A1A" transform="rotate(-10 88 138)"/>
      <ellipse cx="192" cy="138" rx="46" ry="42" fill="#1A1A1A" transform="rotate(10 192 138)"/>
      <!-- Sclera (blink) -->
      <ellipse cx="90"  cy="133" rx="27" ry="26" fill="#FFFFFF"
        style="transform-box:fill-box;transform-origin:50% 40%;animation:blink 5.5s ease-in-out 2s infinite"/>
      <ellipse cx="190" cy="133" rx="27" ry="26" fill="#FFFFFF"
        style="transform-box:fill-box;transform-origin:50% 40%;animation:blink 5.5s ease-in-out 2.5s infinite"/>
      <!-- Pupils (wander) -->
      <g style="transform-box:fill-box;transform-origin:center;animation:pupilW 8s ease-in-out 1s infinite">
        <circle cx="92"  cy="133" r="14" fill="#1A1A1A"/>
        <circle cx="98"  cy="126" r="6"  fill="#FFFFFF"/>
        <circle cx="87"  cy="138" r="3"  fill="#FFFFFF" opacity=".5"/>
      </g>
      <g style="transform-box:fill-box;transform-origin:center;animation:pupilW 8s ease-in-out 2s infinite">
        <circle cx="188" cy="133" r="14" fill="#1A1A1A"/>
        <circle cx="194" cy="126" r="6"  fill="#FFFFFF"/>
        <circle cx="183" cy="138" r="3"  fill="#FFFFFF" opacity=".5"/>
      </g>
      <!-- Nose bridge + nose -->
      <ellipse cx="140" cy="164" rx="6" ry="8" fill="#E8E8E8"/>
      <ellipse cx="140" cy="178" rx="17" ry="13" fill="#1A1A1A"/>
      <ellipse cx="133" cy="174" rx="6"  ry="4"  fill="#3A3A3A" opacity=".4"/>
      <line x1="128" y1="186" x2="140" y2="193" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="round"/>
      <line x1="152" y1="186" x2="140" y2="193" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="round"/>
      <!-- WELCOME: happy smile + blush -->
      <g opacity="{s_happy}">
        <path d="M 96 210 Q 140 248 184 210" stroke="#1A1A1A" stroke-width="5.5" fill="none" stroke-linecap="round"/>
        <ellipse cx="54"  cy="204" rx="18" ry="11" fill="#FFB3BA" opacity=".45"/>
        <ellipse cx="226" cy="204" rx="18" ry="11" fill="#FFB3BA" opacity=".45"/>
      </g>
      <!-- THINKING: smirk + raised brow + thought bubbles -->
      <g opacity="{s_think}">
        <path d="M 100 214 Q 128 228 158 212" stroke="#1A1A1A" stroke-width="5" fill="none" stroke-linecap="round"/>
        <path d="M 52  110 Q 72  94  96 102"  stroke="#1A1A1A" stroke-width="5.5" fill="none" stroke-linecap="round"/>
        <path d="M 184 104 Q 206 100 228 112" stroke="#1A1A1A" stroke-width="5.5" fill="none" stroke-linecap="round"/>
        <circle cx="218" cy="92"  r="5.5" fill="#CCCCCC" opacity=".75"/>
        <circle cx="232" cy="74"  r="8"   fill="#CCCCCC" opacity=".75"/>
        <circle cx="250" cy="52"  r="12"  fill="#CCCCCC" opacity=".75"/>
        <text x="250" y="57" font-size="13" text-anchor="middle" font-family="'Segoe UI',sans-serif" fill="#555">💡</text>
      </g>
      <!-- BYE: excited grin + raised brows + big blush -->
      <g opacity="{s_excited}">
        <path d="M 88 208 Q 140 256 192 208" stroke="#1A1A1A" stroke-width="6" fill="none" stroke-linecap="round"/>
        <path d="M 89 209 Q 140 252 191 209 L 188 224 Q 140 252 92 224 Z" fill="#FFFFFF" stroke="#D4D4D4" stroke-width="1.2"/>
        <line x1="115" y1="210" x2="115" y2="223" stroke="#D4D4D4" stroke-width="1.5"/>
        <line x1="140" y1="210" x2="140" y2="224" stroke="#D4D4D4" stroke-width="1.5"/>
        <line x1="165" y1="210" x2="165" y2="223" stroke="#D4D4D4" stroke-width="1.5"/>
        <path d="M 54  108 Q 76  94  100 100" stroke="#1A1A1A" stroke-width="5.5" fill="none" stroke-linecap="round"/>
        <path d="M 180 100 Q 204 94  226 108" stroke="#1A1A1A" stroke-width="5.5" fill="none" stroke-linecap="round"/>
        <ellipse cx="42"  cy="196" rx="24" ry="15" fill="#FFB3BA" opacity=".55"/>
        <ellipse cx="238" cy="196" rx="24" ry="15" fill="#FFB3BA" opacity=".55"/>
      </g>
    </svg>
    <!-- Right arm -->
    <div style="
      width:22px;height:62px;background:#1A1A1A;border-radius:11px;
      transform-origin:top center;animation:{wave_r};
      align-self:flex-end;margin-bottom:14px;margin-left:-5px;
    "></div>
  </div>
</body></html>"""


# ── Sitting Panda — Waiting State (Requirements Page Right Side) ──────────────


def _sitting_panda_html() -> str:
    """Static sitting panda — same face style as landing, no animations."""
    return """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  html,body{
    background:transparent;width:100%;height:100%;
    display:flex;flex-direction:column;align-items:center;
    justify-content:center;overflow:hidden;
    font-family:'Segoe UI',system-ui,sans-serif;
  }
</style></head>
<body>
  <div style="display:flex;flex-direction:column;align-items:center;gap:10px;">
    <!-- Speech bubble -->
    <div style="
      background:#fff;border:2.5px solid #2D6A4F;border-radius:18px;
      padding:11px 18px;font-size:13px;color:#2D6A4F;
      max-width:210px;text-align:center;line-height:1.55;
      box-shadow:0 4px 16px rgba(45,106,79,.15);
      position:relative;font-weight:600;
    ">Fill in your project<br>requirements 🐼
      <span style="position:absolute;bottom:-11px;left:50%;transform:translateX(-50%);
        border:9px solid transparent;border-top-color:#2D6A4F;"></span>
    </div>
    <!-- Sitting panda body (static) -->
    <div>
      <svg viewBox="0 0 320 420" width="220" height="300" xmlns="http://www.w3.org/2000/svg">
        <!-- Shadow -->
        <ellipse cx="160" cy="405" rx="70" ry="10" fill="#1A1A1A" opacity=".06"/>
        <!-- Body (sitting torso) -->
        <ellipse cx="160" cy="320" rx="82" ry="90" fill="#FFFFFF" stroke="#E0E0E0" stroke-width="1"/>
        <!-- Belly patch -->
        <ellipse cx="160" cy="320" rx="52" ry="60" fill="#F5F5F5"/>
        <!-- Legs (sitting, spread forward) -->
        <ellipse cx="105" cy="380" rx="38" ry="22" fill="#1A1A1A"/>
        <ellipse cx="215" cy="380" rx="38" ry="22" fill="#1A1A1A"/>
        <!-- Feet pads -->
        <ellipse cx="80"  cy="385" rx="16" ry="12" fill="#2D2D2D"/>
        <ellipse cx="240" cy="385" rx="16" ry="12" fill="#2D2D2D"/>
        <circle cx="73" cy="382" r="4" fill="#3A3A3A" opacity=".4"/>
        <circle cx="87" cy="382" r="4" fill="#3A3A3A" opacity=".4"/>
        <circle cx="233" cy="382" r="4" fill="#3A3A3A" opacity=".4"/>
        <circle cx="247" cy="382" r="4" fill="#3A3A3A" opacity=".4"/>
        <!-- Arms (resting on lap) -->
        <ellipse cx="90"  cy="305" rx="22" ry="48" fill="#1A1A1A" transform="rotate(25 90 305)"/>
        <ellipse cx="230" cy="305" rx="22" ry="48" fill="#1A1A1A" transform="rotate(-25 230 305)"/>
        <!-- Hand/paw circles on lap -->
        <circle cx="118" cy="340" r="15" fill="#1A1A1A"/>
        <circle cx="202" cy="340" r="15" fill="#1A1A1A"/>
        <!-- Paw pads -->
        <circle cx="118" cy="340" r="8" fill="#2D2D2D"/>
        <circle cx="202" cy="340" r="8" fill="#2D2D2D"/>
        <!-- Tail (static) -->
        <circle cx="248" cy="360" r="16" fill="#1A1A1A"/>

        <!-- === HEAD (same panda face as landing) === -->
        <!-- Ears -->
        <circle cx="82"  cy="84" r="42" fill="#1A1A1A"/>
        <circle cx="238" cy="84" r="42" fill="#1A1A1A"/>
        <circle cx="82"  cy="84" r="25" fill="#2D2D2D" opacity=".45"/>
        <circle cx="238" cy="84" r="25" fill="#2D2D2D" opacity=".45"/>
        <!-- Head shape -->
        <ellipse cx="160" cy="170" rx="108" ry="106" fill="#EFEFED"/>
        <ellipse cx="160" cy="168" rx="104" ry="102" fill="#FFFFFF"/>
        <!-- Cheek shading -->
        <ellipse cx="58"  cy="186" rx="18" ry="13" fill="#E8E8E6" opacity=".7"/>
        <ellipse cx="262" cy="186" rx="18" ry="13" fill="#E8E8E6" opacity=".7"/>
        <!-- Eye patches -->
        <ellipse cx="110" cy="140" rx="42" ry="38" fill="#1A1A1A" transform="rotate(-10 110 140)"/>
        <ellipse cx="210" cy="140" rx="42" ry="38" fill="#1A1A1A" transform="rotate(10 210 140)"/>
        <!-- Sclera -->
        <ellipse cx="112" cy="136" rx="24" ry="23" fill="#FFFFFF"/>
        <ellipse cx="208" cy="136" rx="24" ry="23" fill="#FFFFFF"/>
        <!-- Pupils -->
        <g>
          <circle cx="114" cy="136" r="12" fill="#1A1A1A"/>
          <circle cx="119" cy="130" r="5" fill="#FFFFFF"/>
          <circle cx="109" cy="140" r="2.5" fill="#FFFFFF" opacity=".5"/>
        </g>
        <g>
          <circle cx="206" cy="136" r="12" fill="#1A1A1A"/>
          <circle cx="211" cy="130" r="5" fill="#FFFFFF"/>
          <circle cx="201" cy="140" r="2.5" fill="#FFFFFF" opacity=".5"/>
        </g>
        <!-- Nose bridge + nose -->
        <ellipse cx="160" cy="162" rx="5.5" ry="7" fill="#E8E8E8"/>
        <ellipse cx="160" cy="175" rx="15" ry="11" fill="#1A1A1A"/>
        <ellipse cx="154" cy="172" rx="5" ry="3.5" fill="#3A3A3A" opacity=".4"/>
        <line x1="150" y1="183" x2="160" y2="189" stroke="#1A1A1A" stroke-width="2.2" stroke-linecap="round"/>
        <line x1="170" y1="183" x2="160" y2="189" stroke="#1A1A1A" stroke-width="2.2" stroke-linecap="round"/>
        <!-- Gentle smile -->
        <path d="M 118 204 Q 160 236 202 204" stroke="#1A1A1A" stroke-width="4.5" fill="none" stroke-linecap="round"/>
        <!-- Blush -->
        <ellipse cx="76"  cy="198" rx="16" ry="10" fill="#FFB3BA" opacity=".4"/>
        <ellipse cx="244" cy="198" rx="16" ry="10" fill="#FFB3BA" opacity=".4"/>
      </svg>
    </div>
  </div>
</body></html>"""


# ── KFP Footer ────────────────────────────────────────────────────────────────

