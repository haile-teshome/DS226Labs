import streamlit as st
import streamlit.components.v1 as components

def show_lab02():
    st.markdown("## Stage 1: Screening")
    
    html_code = """
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body { font-family: 'Inter', sans-serif; background: transparent; margin: 0; color: #374151; padding: 10px; }
        
        .bubbly-card {
            background: #ffffff; border-radius: 32px; padding: 35px;
            border: 2px solid #f3f4f6; box-shadow: 0 10px 30px rgba(0,0,0,0.02);
            margin-bottom: 30px;
        }

        .grid { display: grid; grid-template-columns: 440px 1fr; gap: 40px; }

        .formula-card {
            background: #f8fafc; border-radius: 20px; padding: 22px; border: 1px solid #e2e8f0;
            margin-top: 15px; font-size: 13px;
        }
        .math-header { color: #64748b; font-size: 11px; font-weight: 800; margin-bottom: 8px; letter-spacing: 0.5px; text-transform: uppercase; }
        
        .math-fraction-container { display: flex; align-items: center; margin-bottom: 20px; }
        .math-fraction { display: inline-flex; flex-direction: column; align-items: center; vertical-align: middle; }
        .math-numerator { border-bottom: 1.5px solid #334155; padding: 0 10px; font-weight: 700; }
        .math-denominator { padding: 0 10px; font-weight: 700; }
        .math-res { font-size: 38px; font-weight: 800; color: #1e3a8a; margin-top: 10px; border-top: 1px solid #e2e8f0; padding-top: 10px; }

        .hl-p { color: #3b82f6; } .hl-se { color: #16a34a; } .hl-fp { color: #dc2626; }

        .axis-text { font-size: 11px; font-weight: 700; fill: #94a3b8; text-transform: uppercase; }
        .chart-title { font-size: 15px; font-weight: 800; fill: #1e293b; text-anchor: middle; }
        
        .box-label { font-size: 13px; font-weight: 800; pointer-events: none; }
        .box-math { font-size: 9px; font-family: monospace; font-weight: 600; pointer-events: none; opacity: 0.8; }

        .label-row { display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 11px; font-weight: 700; color: #64748b; }
        input[type=range] { width: 100%; accent-color: #3b82f6; cursor: pointer; margin-bottom: 20px;}

        .interp-box { 
            margin-top: 25px; padding: 25px; border-radius: 24px; font-size: 14px; line-height: 1.6;
            background: #f1f5f9; border-left: 8px solid #3b82f6;
        }
        .interp-title { font-weight: 800; color: #1e3a8a; display: block; margin-bottom: 5px; text-transform: uppercase; font-size: 12px; }
    </style>

    <div class="bubbly-card">
        <div style="margin-bottom:25px;">
            <span style="background:#3b82f6; color:white; padding:5px 15px; border-radius:20px; font-size:11px; font-weight:800;">PART B2: SCREENING</span>
            <h2 style="margin:10px 0;">Sepsis Alert Probability</h2>
        </div>
        
        <div class="grid">
            <div class="controls">
                <div class="label-row"><span>PREVALENCE P(D)</span><span id="v_p1">0.020</span></div>
                <input type="range" id="p1" min="0.005" max="0.250" step="0.005" value="0.020">

                <div class="label-row"><span>SENSITIVITY P(S+|D)</span><span id="v_se1">0.92</span></div>
                <input type="range" id="se1" min="0.5" max="1.0" step="0.01" value="0.92">

                <div class="label-row"><span>SPECIFICITY P(S-|Dc)</span><span id="v_sp1">0.90</span></div>
                <input type="range" id="sp1" min="0.5" max="1.0" step="0.01" value="0.90">

                <div class="formula-card">
                    <div class="math-header">Probabilistic Formula</div>
                    <div class="math-fraction-container">
                        <span style="font-weight:700; margin-right:8px; font-style:italic;">P(D|S+) =</span>
                        <div class="math-fraction" style="font-style:italic; font-size:14px;">
                            <div class="math-numerator">P(S+|D)P(D)</div>
                            <div class="math-denominator">P(S+|D)P(D) + P(S+|Dc)P(Dc)</div>
                        </div>
                    </div>
                    
                    <div class="math-header">Calculation Plug-in</div>
                    <div class="math-fraction-container">
                        <span style="font-weight:700; margin-right:8px;">PPV =</span>
                        <div class="math-fraction">
                            <div class="math-numerator">
                                <span class="hl-se" id="f_se1">0.92</span> × <span class="hl-p" id="f_p1">0.02</span>
                            </div>
                            <div class="math-denominator">
                                (<span class="hl-se" id="f_se1_d">0.92</span> × <span class="hl-p" id="f_p1_d">0.02</span>) + 
                                (<span class="hl-fp" id="f_fpr1">0.10</span> × <span id="f_hc1">0.98</span>)
                            </div>
                        </div>
                    </div>
                    <div class="math-res" id="res1">15.8%</div>
                </div>
            </div>
            
            <div style="display:flex; flex-direction:column; align-items:center;">
                <svg id="viz1" width="400" height="420"></svg>
                <p style="font-size: 11px; color: #94a3b8; font-weight: 600; text-align: center; max-width: 320px; margin-top: 10px;">
                    FIGURE 1: Outcome Mosaic. The areas represent the relative probabilities of clinical outcomes based on current parameters.
                </p>
            </div>
        </div>

        <div class="interp-box" id="interp1">
            <span class="interp-title">Clinical Interpretation</span>
            <div id="interp_text"></div>
        </div>
    </div>

    <script>
        const W = 320, H = 240, M = 60;

        function updateViz(svgId, prior, sens, spec) {
            const svg = d3.select(svgId);
            svg.selectAll("*").remove();
            const g = svg.append("g").attr("transform", `translate(${M}, 50)`);

            const wS = prior * W;
            const wH = (1 - prior) * W;
            const hTP = sens * H;
            const hFP = (1 - spec) * H;

            g.append("text").attr("x", W/2).attr("y", -25).attr("class", "chart-title").text("Outcome Probability Areas");
            g.append("rect").attr("width", W).attr("height", H).attr("fill", "#f8fafc").attr("rx", 10);
            
            g.append("rect").attr("x", 0).attr("y", H-hTP).attr("width", wS).attr("height", hTP).attr("fill", "#22c55e").attr("fill-opacity", 0.85).attr("rx", 5);
            g.append("rect").attr("x", wS).attr("y", H-hFP).attr("width", wH).attr("height", hFP).attr("fill", "#ef4444").attr("fill-opacity", 0.85).attr("rx", 5);

            const drawArea = (x, y, label, term, color) => {
                const group = g.append("g").attr("transform", `translate(${x},${y})`);
                group.append("text").attr("class", "box-label").attr("text-anchor", "middle").attr("fill", color).text(label);
                group.append("text").attr("class", "box-math").attr("text-anchor", "middle").attr("y", 14).attr("fill", color).text(term);
            };

            drawArea(wS/2, H-hTP/2, "TP", "P(S+|D)P(D)", "#14532d");
            drawArea(wS + wH/2, H-hFP/2, "FP", "P(S+|Dc)P(Dc)", "#7f1d1d");
            drawArea(wS/2, (H-hTP)/2, "FN", "P(S-|D)P(D)", "#64748b");
            drawArea(wS + wH/2, (H-hFP)/2, "TN", "P(S-|Dc)P(Dc)", "#64748b");
            
            g.append("text").attr("x", W/2).attr("y", H+45).attr("class", "axis-text").attr("text-anchor", "middle").style("fill", "#475569").text("Clinical Truth");
            g.append("text").attr("x", wS/2).attr("y", H+25).attr("class", "axis-text").attr("text-anchor", "middle").text("Sick (D)");
            g.append("text").attr("x", wS + wH/2).attr("y", H+25).attr("class", "axis-text").attr("text-anchor", "middle").text("Healthy (Dc)");
            
            const yAx = g.append("g").attr("transform", "rotate(-90)");
            yAx.append("text").attr("x", -H/2).attr("y", -35).attr("class", "axis-text").attr("text-anchor", "middle").style("fill", "#475569").text("Test Result");

            g.append("line").attr("x1", wS).attr("y1", 0).attr("x2", wS).attr("y2", H+10).attr("stroke", "#cbd5e1").attr("stroke-dasharray", "4,4");
        }

        function run() {
            const p = +document.getElementById('p1').value;
            const se = +document.getElementById('se1').value;
            const sp = +document.getElementById('sp1').value;
            const fpr = 1 - sp;
            const hc = 1 - p;
            const tp = p * se;
            const fp = hc * fpr;
            const ppv = tp / (tp + fp);

            document.getElementById('v_p1').innerText = p.toFixed(3);
            document.getElementById('v_se1').innerText = se.toFixed(2);
            document.getElementById('v_sp1').innerText = sp.toFixed(2);
            document.getElementById('f_se1').innerText = document.getElementById('f_se1_d').innerText = se.toFixed(2);
            document.getElementById('f_p1').innerText = document.getElementById('f_p1_d').innerText = p.toFixed(3);
            document.getElementById('f_fpr1').innerText = fpr.toFixed(2);
            document.getElementById('f_hc1').innerText = hc.toFixed(3);
            
            const resVal = (ppv*100).toFixed(1);
            document.getElementById('res1').innerText = resVal + "%";
            
            // --- DYNAMIC COLOR LOGIC ---
            const interpBox = document.getElementById('interp1');
            if (ppv > 0.5) {
                interpBox.style.background = "#fef2f2"; // Light Red
                interpBox.style.borderLeftColor = "#dc2626"; // Bold Red
            } else {
                interpBox.style.background = "#f1f5f9"; // Original Blue-Grey
                interpBox.style.borderLeftColor = "#3b82f6"; // Original Blue
            }

            // DYNAMIC INTERPRETATION
            let extraInsight = "";
            if (fp > tp) {
                extraInsight = `Because the prevalence is low (${(p*100).toFixed(1)}%), the <b>False Positive (Red)</b> area is currently <b>${(fp/tp).toFixed(1)}x larger</b> than the Green area.`;
            } else {
                extraInsight = `With higher prevalence or specificity, the <b>True Positive (Green)</b> area now outweighs the Red area.`;
            }

            document.getElementById('interp_text').innerHTML = `
                Out of all the people the test flags as positive (the combined <b>Green</b> and <b>Red</b> areas), 
                only <b>${resVal}%</b> actually have the condition. ${extraInsight} 
                Clinical action should likely wait for a confirmatory test.
            `;

            updateViz("#viz1", p, se, sp);
        }

        d3.selectAll("input").on("input", run);
        run();
    </script>
    """
    components.html(html_code, height=850)

def show_lab02_part2():
    st.markdown("## Stage 2: Confirmatory Clinical Analysis")
    
    html_code = """
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body { font-family: 'Inter', sans-serif; background: transparent; margin: 0; color: #374151; padding: 10px; }
        
        .bubbly-card {
            background: #ffffff; border-radius: 32px; padding: 35px;
            border: 2px solid #1e3a8a; box-shadow: 0 10px 30px rgba(0,0,0,0.05);
            margin-bottom: 30px;
        }

        .grid { display: grid; grid-template-columns: 440px 1fr; gap: 40px; }

        .formula-card {
            background: #f0f4ff; border-radius: 20px; padding: 22px; border: 1px solid #dbeafe;
            margin-top: 15px; font-size: 13px;
        }
        .math-header { color: #1e40af; font-size: 11px; font-weight: 800; margin-bottom: 8px; letter-spacing: 0.5px; text-transform: uppercase; }
        
        .math-fraction-container { display: flex; align-items: center; margin-bottom: 20px; }
        .math-fraction { display: inline-flex; flex-direction: column; align-items: center; vertical-align: middle; }
        .math-numerator { border-bottom: 1.5px solid #1e3a8a; padding: 0 10px; font-weight: 700; }
        .math-denominator { padding: 0 10px; font-weight: 700; }
        .math-res { font-size: 38px; font-weight: 800; color: #1e3a8a; margin-top: 10px; border-top: 2px solid #dbeafe; padding-top: 10px; }

        .hl-p { color: #3b82f6; } .hl-se { color: #16a34a; } .hl-fp { color: #dc2626; }

        .axis-text { font-size: 11px; font-weight: 700; fill: #94a3b8; text-transform: uppercase; }
        .chart-title { font-size: 15px; font-weight: 800; fill: #1e293b; text-anchor: middle; }
        
        .box-label { font-size: 13px; font-weight: 800; pointer-events: none; }
        .box-math { font-size: 9px; font-family: monospace; font-weight: 600; pointer-events: none; opacity: 0.8; }

        .label-row { display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 11px; font-weight: 700; color: #1e40af; }
        input[type=range] { width: 100%; accent-color: #1e3a8a; cursor: pointer; margin-bottom: 20px;}

        .interp-box { 
            margin-top: 25px; padding: 25px; border-radius: 24px; font-size: 14px; line-height: 1.6;
            background: #eff6ff; border-left: 8px solid #1e3a8a;
        }
        .interp-title { font-weight: 800; color: #1e3a8a; display: block; margin-bottom: 5px; text-transform: uppercase; font-size: 12px; }
    </style>

    <div class="bubbly-card">
        <div style="margin-bottom:25px;">
            <span style="background:#1e3a8a; color:white; padding:5px 15px; border-radius:20px; font-size:11px; font-weight:800;">STAGE 2: CONFIRMATION</span>
            <h2 style="margin:10px 0;">Post-Test Diagnostic Probability</h2>
        </div>
        
        <div class="grid">
            <div class="controls">
                <div class="label-row"><span>PRIOR (FROM STAGE 1)</span><span id="v_p2">0.158</span></div>
                <input type="range" id="p2" min="0.01" max="0.99" step="0.01" value="0.158">

                <div class="label-row"><span>CONFIRMATORY SENSITIVITY</span><span id="v_se2">0.95</span></div>
                <input type="range" id="se2" min="0.5" max="1.0" step="0.01" value="0.95">

                <div class="label-row"><span>CONFIRMATORY SPECIFICITY</span><span id="v_sp2">0.98</span></div>
                <input type="range" id="sp2" min="0.5" max="1.0" step="0.01" value="0.98">

                <div class="formula-card">
                    <div class="math-header">Probabilistic Formula</div>
                    <div class="math-fraction-container">
                        <span style="font-weight:700; margin-right:8px; font-style:italic;">P(D|C+) =</span>
                        <div class="math-fraction" style="font-style:italic; font-size:14px;">
                            <div class="math-numerator">P(C+|D)P(D|S+)</div>
                            <div class="math-denominator">P(C+|D)P(D|S+) + P(C+|Dc)P(Dc|S+)</div>
                        </div>
                    </div>
                    
                    <div class="math-header">Calculation Plug-in</div>
                    <div class="math-fraction-container">
                        <span style="font-weight:700; margin-right:8px;">POSTERIOR =</span>
                        <div class="math-fraction">
                            <div class="math-numerator">
                                <span class="hl-se" id="f_se2">0.95</span> × <span class="hl-p" id="f_p2">0.16</span>
                            </div>
                            <div class="math-denominator">
                                (<span class="hl-se" id="f_se2_d">0.95</span> × <span class="hl-p" id="f_p2_d">0.16</span>) + 
                                (<span class="hl-fp" id="f_fpr2">0.02</span> × <span id="f_hc2">0.84</span>)
                            </div>
                        </div>
                    </div>
                    <div class="math-res" id="res2">89.4%</div>
                </div>
            </div>
            
            <div style="display:flex; flex-direction:column; align-items:center;">
                <svg id="viz2" width="400" height="420"></svg>
                <p style="font-size: 11px; color: #94a3b8; font-weight: 600; text-align: center; max-width: 320px; margin-top: 10px;">
                    FIGURE 2: Confirmatory Mosaic. Note how the "Sick (D)" column width reflects the enriched population from Stage 1.
                </p>
            </div>
        </div>

        <div class="interp-box" id="interp2">
            <span class="interp-title">Diagnostic Interpretation</span>
            <div id="interp_text2"></div>
        </div>
    </div>

    <script>
        const W = 320, H = 240, M = 60;

        function updateViz(svgId, prior, sens, spec) {
            const svg = d3.select(svgId);
            svg.selectAll("*").remove();
            const g = svg.append("g").attr("transform", `translate(${M}, 50)`);

            const wS = prior * W;
            const wH = (1 - prior) * W;
            const hTP = sens * H;
            const hFP = (1 - spec) * H;

            g.append("text").attr("x", W/2).attr("y", -25).attr("class", "chart-title").text("Confirmatory Outcome Probabilities");
            g.append("rect").attr("width", W).attr("height", H).attr("fill", "#f8fafc").attr("rx", 10);
            
            g.append("rect").attr("x", 0).attr("y", H-hTP).attr("width", wS).attr("height", hTP).attr("fill", "#16a34a").attr("fill-opacity", 0.85).attr("rx", 5);
            g.append("rect").attr("x", wS).attr("y", H-hFP).attr("width", wH).attr("height", hFP).attr("fill", "#dc2626").attr("fill-opacity", 0.85).attr("rx", 5);

            const drawArea = (x, y, label, term, color) => {
                const group = g.append("g").attr("transform", `translate(${x},${y})`);
                group.append("text").attr("class", "box-label").attr("text-anchor", "middle").attr("fill", color).text(label);
                group.append("text").attr("class", "box-math").attr("text-anchor", "middle").attr("y", 14).attr("fill", color).text(term);
            };

            drawArea(wS/2, H-hTP/2, "TP", "P(C+|D)P(D|S+)", "#064e3b");
            drawArea(wS + wH/2, H-hFP/2, "FP", "P(C+|Dc)P(Dc|S+)", "#7f1d1d");
            drawArea(wS/2, (H-hTP)/2, "FN", "P(C-|D)P(D|S+)", "#64748b");
            drawArea(wS + wH/2, (H-hFP)/2, "TN", "P(C-|Dc)P(Dc|S+)", "#64748b");
            
            g.append("text").attr("x", W/2).attr("y", H+45).attr("class", "axis-text").attr("text-anchor", "middle").style("fill", "#475569").text("Clinical Truth");
            g.append("text").attr("x", wS/2).attr("y", H+25).attr("class", "axis-text").attr("text-anchor", "middle").text("Sick (D)");
            g.append("text").attr("x", wS + wH/2).attr("y", H+25).attr("class", "axis-text").attr("text-anchor", "middle").text("Healthy (Dc)");
            
            const yAx = g.append("g").attr("transform", "rotate(-90)");
            yAx.append("text").attr("x", -H/2).attr("y", -35).attr("class", "axis-text").attr("text-anchor", "middle").style("fill", "#475569").text("Confirm Result");

            g.append("line").attr("x1", wS).attr("y1", 0).attr("x2", wS).attr("y2", H+10).attr("stroke", "#cbd5e1").attr("stroke-dasharray", "4,4");
        }

        function run() {
            const p = +document.getElementById('p2').value;
            const se = +document.getElementById('se2').value;
            const sp = +document.getElementById('sp2').value;
            const fpr = 1 - sp;
            const hc = 1 - p;
            const tp = p * se;
            const fp = hc * fpr;
            const ppv = tp / (tp + fp);

            document.getElementById('v_p2').innerText = p.toFixed(3);
            document.getElementById('v_se2').innerText = se.toFixed(2);
            document.getElementById('v_sp2').innerText = sp.toFixed(2);
            document.getElementById('f_se2').innerText = document.getElementById('f_se2_d').innerText = se.toFixed(2);
            document.getElementById('f_p2').innerText = document.getElementById('f_p2_d').innerText = p.toFixed(3);
            document.getElementById('f_fpr2').innerText = fpr.toFixed(2);
            document.getElementById('f_hc2').innerText = hc.toFixed(3);
            
            const resVal = (ppv*100).toFixed(1);
            document.getElementById('res2').innerText = resVal + "%";
            
            // --- DYNAMIC COLOR LOGIC ---
            const interpBox = document.getElementById('interp2');
            if (ppv >= 0.85) {
                interpBox.style.background = "#f0fdf4"; // Light Green (Confirmed)
                interpBox.style.borderLeftColor = "#16a34a"; // Bold Green
            } else if (ppv >= 0.5) {
                interpBox.style.background = "#fffbeb"; // Yellow (Uncertain)
                interpBox.style.borderLeftColor = "#d97706"; // Bold Amber
            } else {
                interpBox.style.background = "#eff6ff"; // Blue
                interpBox.style.borderLeftColor = "#1e3a8a"; 
            }

            let extraInsight = "";
            if (tp > fp) {
                extraInsight = `Because the starting prior is higher (<b>${(p*100).toFixed(1)}%</b>), the <b>True Positive (Green)</b> area now easily outweighs the Red area.`;
            } else {
                extraInsight = `Even with confirmation, the low prior means the <b>Red (False Positive)</b> area remains significant.`;
            }

            document.getElementById('interp_text2').innerHTML = `
                In Stage 2, we only test those who flagged positive in Stage 1. This "enriches" our population. 
                ${extraInsight} A positive confirmation result provides <b>${resVal}% certainty</b>, 
                making it a strong basis for clinical intervention.
            `;

            updateViz("#viz2", p, se, sp);
        }

        d3.selectAll("input").on("input", run);
        run();
    </script>
    """
    components.html(html_code, height=850)