import streamlit as st
import streamlit.components.v1 as components

def show_lab03():
    
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
        
        .math-res-container { display: flex; gap: 20px; margin-top: 15px; border-top: 1px solid #e2e8f0; padding-top: 15px; }
        .math-res-box { flex: 1; }
        .math-res-label { font-size: 10px; font-weight: 800; color: #64748b; margin-bottom: 4px; }
        .math-res-val { font-size: 24px; font-weight: 800; color: #1e3a8a; }

        .axis-text { font-size: 11px; font-weight: 700; fill: #94a3b8; text-transform: uppercase; }
        .chart-title { font-size: 15px; font-weight: 800; fill: #1e293b; text-anchor: middle; }
        
        .label-row { display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 11px; font-weight: 700; color: #64748b; }
        input[type=range] { width: 100%; accent-color: #3b82f6; cursor: pointer; margin-bottom: 20px;}

        .interp-box { 
            margin-top: 25px; padding: 25px; border-radius: 24px; font-size: 14px; line-height: 1.6;
            background: #f1f5f9; border-left: 8px solid #3b82f6;
        }
        .interp-title { font-weight: 800; color: #1e3a8a; display: block; margin-bottom: 5px; text-transform: uppercase; font-size: 12px; }
        
        .legend-item { display: flex; align-items: center; gap: 8px; font-size: 12px; font-weight: 600; margin-bottom: 5px; }
        .legend-line { width: 30px; height: 3px; border-radius: 2px; }
    </style>

    <div class="bubbly-card">
        <div style="margin-bottom:25px;">
            <span style="background:#3b82f6; color:white; padding:5px 15px; border-radius:20px; font-size:11px; font-weight:800;">PART C: CONJUGATE UPDATING</span>
            <h2 style="margin:10px 0;">Beta-Binomial Triplot Viewer</h2>
        </div>
        
        <div class="grid">
            <div class="controls">
                <div class="label-row"><span>PRIOR ALPHA (&alpha;)</span><span id="v_alpha">2.0</span></div>
                <input type="range" id="alpha" min="1" max="50" step="1" value="2">

                <div class="label-row"><span>PRIOR BETA (&beta;)</span><span id="v_beta">2.0</span></div>
                <input type="range" id="beta" min="1" max="50" step="1" value="2">

                <div class="label-row"><span>OBSERVED SUCCESSES (y)</span><span id="v_y">18</span></div>
                <input type="range" id="y" min="0" max="100" step="1" value="18">

                <div class="label-row"><span>TOTAL TRIALS (n)</span><span id="v_n">40</span></div>
                <input type="range" id="n" min="1" max="100" step="1" value="40">

                <div class="formula-card">
                    <div class="math-header">Posterior Parameters</div>
                    <div style="font-family: monospace; font-size: 14px; margin-bottom: 10px;">
                        &theta;|y ~ Beta(&alpha; + y, &beta; + n - y)
                    </div>
                    <div id="post_params" style="font-weight: 700; color: #1e3a8a; font-size: 16px;">
                        Beta(20, 24)
                    </div>
                    
                    <div class="math-res-container">
                        <div class="math-res-box">
                            <div class="math-res-label">POSTERIOR MEAN</div>
                            <div class="math-res-val" id="post_mean">0.455</div>
                        </div>
                        <div class="math-res-box">
                            <div class="math-res-label">POSTERIOR SD</div>
                            <div class="math-res-val" id="post_sd">0.074</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div style="display:flex; flex-direction:column; align-items:center;">
                <div style="display:flex; gap:20px; margin-bottom:15px;">
                    <div class="legend-item"><div class="legend-line" style="background:#94a3b8;"></div> Prior</div>
                    <div class="legend-item"><div class="legend-line" style="background:#3b82f6; border: 1.5px dashed #3b82f6; height:0;"></div> Likelihood</div>
                    <div class="legend-item"><div class="legend-line" style="background:#1e3a8a;"></div> Posterior</div>
                </div>
                <svg id="triplot" width="440" height="380"></svg>
                <p style="font-size: 11px; color: #94a3b8; font-weight: 600; text-align: center; max-width: 320px; margin-top: 10px;">
                    FIGURE 3: Triplot visualization. The posterior acts as a compromise between the prior beliefs and the observed data[cite: 12, 95].
                </p>
            </div>
        </div>

        <div class="interp-box" id="interp3">
            <span class="interp-title">Posterior Interpretation</span>
            <div id="interp_text3"></div>
        </div>
    </div>

    <script>
        const W = 360, H = 280, M = 50;

        function jStatBeta(x, a, b) {
            if (x < 0 || x > 1) return 0;
            const logBeta = (a, b) => {
                const logGamma = (n) => {
                    let res = 0;
                    while (n > 1) { n--; res += Math.log(n); }
                    return res;
                };
                return logGamma(a) + logGamma(b) - logGamma(a + b);
            };
            return Math.exp((a - 1) * Math.log(x) + (b - 1) * Math.log(1 - x) - logBeta(a, b));
        }

        function updateTriplot(alpha, beta, y, n) {
            const svg = d3.select("#triplot");
            svg.selectAll("*").remove();
            const g = svg.append("g").attr("transform", `translate(${M}, 30)`);

            const aPost = alpha + y;
            const bPost = beta + n - y;
            
            const theta_grid = d3.range(0, 1.001, 0.005);
            const prior_vals = theta_grid.map(t => jStatBeta(t, alpha, beta));
            const post_vals = theta_grid.map(t => jStatBeta(t, aPost, bPost));
            
            // Likelihood kernel normalized for plotting
            const raw_like = theta_grid.map(t => Math.pow(t, y) * Math.pow(1 - t, n - y));
            const max_like = Math.max(...raw_like);
            const normalized_like = raw_like.map(v => (v / max_like) * Math.max(...post_vals, ...prior_vals));

            const yMax = Math.max(...prior_vals, ...post_vals, ...normalized_like);
            
            const x = d3.scaleLinear().domain([0, 1]).range([0, W]);
            const y_scale = d3.scaleLinear().domain([0, yMax * 1.1]).range([H, 0]);

            const line = d3.line().x(d => x(d.t)).y(d => y_scale(d.v)).curve(d3.curveBasis);

            // Draw Prior
            g.append("path")
                .datum(theta_grid.map((t, i) => ({t, v: prior_vals[i]})))
                .attr("fill", "none").attr("stroke", "#94a3b8").attr("stroke-width", 2)
                .attr("d", line);

            // Draw Likelihood (Dashed)
            g.append("path")
                .datum(theta_grid.map((t, i) => ({t, v: normalized_like[i]})))
                .attr("fill", "none").attr("stroke", "#3b82f6").attr("stroke-width", 2)
                .attr("stroke-dasharray", "5,5")
                .attr("d", line);

            // Draw Posterior
            g.append("path")
                .datum(theta_grid.map((t, i) => ({t, v: post_vals[i]})))
                .attr("fill", "none").attr("stroke", "#1e3a8a").attr("stroke-width", 3)
                .attr("d", line);

            // Axes
            g.append("g").attr("transform", `translate(0,${H})`).call(d3.axisBottom(x).ticks(5));
            g.append("g").call(d3.axisLeft(y_scale).ticks(5));
            
            g.append("text").attr("x", W/2).attr("y", H + 40).attr("class", "axis-text").attr("text-anchor", "middle").text("Theta (Success Probability)");
            g.append("text").attr("transform", "rotate(-90)").attr("x", -H/2).attr("y", -40).attr("class", "axis-text").attr("text-anchor", "middle").text("Density");
        }

        function run() {
            const alpha = +document.getElementById('alpha').value;
            const beta = +document.getElementById('beta').value;
            let y = +document.getElementById('y').value;
            let n = +document.getElementById('n').value;

            // Ensure y <= n
            if (y > n) { y = n; document.getElementById('y').value = y; }
            
            const aPost = alpha + y;
            const bPost = beta + n - y;
            const mean = aPost / (aPost + bPost);
            const variance = (aPost * bPost) / (Math.pow(aPost + bPost, 2) * (aPost + bPost + 1));
            const sd = Math.sqrt(variance);

            document.getElementById('v_alpha').innerText = alpha.toFixed(1);
            document.getElementById('v_beta').innerText = beta.toFixed(1);
            document.getElementById('v_y').innerText = y;
            document.getElementById('v_n').innerText = n;
            
            document.getElementById('post_params').innerText = `Beta(${aPost}, ${bPost})`;
            document.getElementById('post_mean').innerText = mean.toFixed(3);
            document.getElementById('post_sd').innerText = sd.toFixed(3);

            const interpBox = document.getElementById('interp3');
            if (n > 50) {
                interpBox.style.background = "#f0fdf4"; // Green for high data
                interpBox.style.borderLeftColor = "#16a34a";
            } else {
                interpBox.style.background = "#f1f5f9";
                interpBox.style.borderLeftColor = "#3b82f6";
            }

            document.getElementById('interp_text3').innerHTML = `
                The posterior distribution <b>Beta(${aPost}, ${bPost})</b> reflects our updated knowledge[cite: 65]. 
                With <b>n=${n}</b> trials, the data is ${n > 20 ? 'dominating' : 'balancing'} the prior. 
                The 95% Credible Interval is roughly between <b>${(mean - 1.96*sd).toFixed(2)}</b> and <b>${(mean + 1.96*sd).toFixed(2)}</b>.
            `;

            updateTriplot(alpha, beta, y, n);
        }

        d3.selectAll("input").on("input", run);
        run();
    </script>
    """
    components.html(html_code, height=850)