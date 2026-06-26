from flask import Flask, request
import os

app = Flask(__name__)

# =========================================================
#  STYLE — design tokens: deep-space console palette
#  Display: Space Grotesk / Body: Inter / Mono: JetBrains Mono
# =========================================================
STYLE = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  :root{
    --bg:#0a0e1a;
    --panel:#11162a;
    --panel-2:#161c35;
    --line:#232b48;
    --text:#e8ecf4;
    --muted:#6b7691;
    --cyan:#00d9ff;
    --amber:#ffb020;
    --green:#33e08f;
    --radius:10px;
    --display: 'Space Grotesk', sans-serif;
    --body: 'Inter', sans-serif;
    --mono: 'JetBrains Mono', monospace;
  }
  *{box-sizing:border-box; margin:0; padding:0;}
  html{scroll-behavior:smooth;}
  body{
    background:var(--bg);
    color:var(--text);
    font-family:var(--body);
    line-height:1.6;
    overflow-x:hidden;
    background-image:
      radial-gradient(circle at 15% 10%, rgba(0,217,255,0.07), transparent 40%),
      radial-gradient(circle at 85% 30%, rgba(255,176,32,0.05), transparent 45%);
  }
  a{color:inherit; text-decoration:none;}
  .container{max-width:1140px; margin:0 auto; padding:0 24px;}

  /* ---------- NAVBAR ---------- */
  .navbar{
    position:fixed; top:0; left:0; right:0; z-index:100;
    display:flex; align-items:center; justify-content:space-between;
    padding:16px 32px;
    background:rgba(10,14,26,0.85);
    backdrop-filter:blur(10px);
    border-bottom:1px solid var(--line);
  }
  .nav-logo{
    font-family:var(--mono); font-weight:600; font-size:15px;
    letter-spacing:0.5px; display:flex; align-items:center; gap:8px;
  }
  .nav-logo .dot{width:8px; height:8px; border-radius:50%; background:var(--green); box-shadow:0 0 8px var(--green); animation:blink 2s infinite;}
  .nav-logo span.tag{color:var(--cyan);}
  .nav-links{display:flex; align-items:center; gap:28px;}
  .nav-links a{
    font-family:var(--mono); font-size:13px; color:var(--muted);
    padding:6px 2px; border-bottom:2px solid transparent; transition:.2s;
  }
  .nav-links a:hover, .nav-links a.active{color:var(--text); border-bottom-color:var(--cyan);}
  .nav-cta{
    font-family:var(--mono); font-size:12px; padding:8px 14px;
    border:1px solid var(--cyan); border-radius:6px; color:var(--cyan);
    transition:.2s;
  }
  .nav-cta:hover{background:var(--cyan); color:#06121a;}
  @keyframes blink{0%,100%{opacity:1;} 50%{opacity:.25;}}

  /* ---------- TERMINAL WINDOW (shared component) ---------- */
  .term{
    background:var(--panel); border:1px solid var(--line); border-radius:var(--radius);
    overflow:hidden; box-shadow:0 20px 60px -20px rgba(0,0,0,0.6);
  }
  .term-bar{
    display:flex; align-items:center; gap:8px;
    padding:10px 14px; background:var(--panel-2); border-bottom:1px solid var(--line);
  }
  .term-bar .tdot{width:10px; height:10px; border-radius:50%;}
  .term-bar .tdot:nth-child(1){background:#ff5f56;}
  .term-bar .tdot:nth-child(2){background:#ffbd2e;}
  .term-bar .tdot:nth-child(3){background:#27c93f;}
  .term-bar .term-title{margin-left:10px; font-family:var(--mono); font-size:11px; color:var(--muted);}
  .term-body{padding:18px 20px; font-family:var(--mono); font-size:13px; color:#b9c2da;}

  /* ---------- HERO ---------- */
  .hero{
    padding:160px 0 90px; position:relative;
  }
  .hero-grid{
    display:grid; grid-template-columns:1.1fr 0.9fr; gap:48px; align-items:center;
  }
  .eyebrow{
    font-family:var(--mono); font-size:12px; color:var(--cyan); letter-spacing:1.5px;
    text-transform:uppercase; display:flex; align-items:center; gap:8px; margin-bottom:18px;
  }
  .eyebrow::before{content:''; width:18px; height:1px; background:var(--cyan);}
  h1.headline{
    font-family:var(--display); font-weight:700; font-size:50px; line-height:1.08;
    letter-spacing:-0.5px; margin-bottom:20px;
  }
  h1.headline .accent{color:var(--cyan);}
  .lede{font-size:16px; color:var(--muted); max-width:480px; margin-bottom:32px;}
  .cta-row{display:flex; gap:14px; flex-wrap:wrap;}
  .btn{
    font-family:var(--mono); font-size:13px; padding:13px 22px; border-radius:7px;
    display:inline-flex; align-items:center; gap:8px; transition:.2s; border:1px solid transparent;
  }
  .btn-primary{background:var(--cyan); color:#06121a; font-weight:600;}
  .btn-primary:hover{transform:translateY(-2px); box-shadow:0 10px 30px -8px rgba(0,217,255,0.5);}
  .btn-ghost{border:1px solid var(--line); color:var(--text);}
  .btn-ghost:hover{border-color:var(--amber); color:var(--amber);}
  .term-line{display:flex; gap:8px;}
  .term-line .prompt{color:var(--green);}
  .typed::after{content:'▌'; animation:blink 1s infinite; color:var(--cyan);}
  .term-out{color:var(--muted); padding-top:6px; font-size:12px;}

  /* ---------- NODE GRAPH (signature element) ---------- */
  .graph-wrap{position:relative; aspect-ratio:1/1; max-width:420px; margin:0 auto;}
  .graph-wrap svg{width:100%; height:100%;}
  .node-label{font-family:var(--mono); font-size:11px; fill:var(--text); font-weight:600;}
  .node-sub{font-family:var(--mono); font-size:8.5px; fill:var(--muted);}
  .edge{stroke:var(--cyan); stroke-width:1.4; opacity:0.55; stroke-dasharray:5 5; animation:dash 6s linear infinite;}
  .edge.alt{stroke:var(--amber);}
  @keyframes dash{to{stroke-dashoffset:-200;}}
  .pulse-ring{fill:none; stroke:var(--cyan); stroke-width:1.5; opacity:0; transform-origin:center;}
  .pulse-ring.amber{stroke:var(--amber);}
  .pulse-ring.green{stroke:var(--green);}
  .pulse-ring{animation:pulse 3s ease-out infinite;}
  .pulse-ring.d2{animation-delay:1s;}
  .pulse-ring.d3{animation-delay:2s;}
  @keyframes pulse{0%{opacity:.7; transform:scale(0.7);} 100%{opacity:0; transform:scale(1.6);}}
  .core-node circle{fill:var(--panel-2); stroke:var(--cyan); stroke-width:1.5;}
  .leaf-node circle{fill:var(--panel); stroke:var(--line); stroke-width:1.5;}

  @media(prefers-reduced-motion: reduce){
    .nav-logo .dot, .typed::after, .edge, .pulse-ring{animation:none !important;}
  }

  /* ---------- SECTIONS ---------- */
  section{padding:90px 0;}
  .section-head{max-width:560px; margin:0 auto 50px; text-align:center;}
  .section-head .eyebrow{justify-content:center;}
  .section-head .eyebrow::before{display:none;}
  h2.section-title{font-family:var(--display); font-weight:700; font-size:32px; letter-spacing:-0.3px;}
  .section-sub{color:var(--muted); margin-top:10px; font-size:15px;}

  .reveal{opacity:0; transform:translateY(24px); transition:opacity .6s ease, transform .6s ease;}
  .reveal.in{opacity:1; transform:translateY(0);}

  /* stack cards */
  .stack-grid{display:grid; grid-template-columns:repeat(3, 1fr); gap:20px;}
  .stack-card{cursor:default;}
  .stack-card:hover{border-color:var(--cyan); box-shadow:0 14px 40px -18px rgba(0,217,255,0.35);}
  .stack-card .term-body ul{list-style:none; display:flex; flex-direction:column; gap:6px;}
  .stack-card .term-body li::before{content:'›'; color:var(--cyan); margin-right:8px;}
  .stack-card .term-body{transition:.2s;}

  /* about / stats */
  .about-grid{display:grid; grid-template-columns:1fr 1fr; gap:48px; align-items:center;}
  .about-copy p{color:var(--muted); margin-bottom:16px; font-size:15px;}
  .stat-row{display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin-top:28px;}
  .stat{border:1px solid var(--line); border-radius:var(--radius); padding:16px; background:var(--panel);}
  .stat .v{font-family:var(--mono); color:var(--cyan); font-size:13px; font-weight:600;}
  .stat .l{font-size:11px; color:var(--muted); margin-top:4px; text-transform:uppercase; letter-spacing:.5px;}

  .badge-row{display:flex; gap:10px; flex-wrap:wrap; margin-top:10px;}
  .badge{font-family:var(--mono); font-size:11px; padding:6px 10px; border:1px solid var(--line); border-radius:5px; color:var(--muted);}

  /* footer cta */
  .footer-cta{
    border-radius:16px; padding:60px 40px; text-align:center;
    background:linear-gradient(160deg, var(--panel), var(--panel-2));
    border:1px solid var(--line); position:relative; overflow:hidden;
  }
  .footer-cta::before{
    content:''; position:absolute; inset:0;
    background:radial-gradient(circle at 50% 0%, rgba(0,217,255,0.12), transparent 60%);
  }
  .footer-cta h2{font-family:var(--display); font-size:28px; margin-bottom:12px; position:relative;}
  .footer-cta p{color:var(--muted); margin-bottom:26px; position:relative;}
  .footer-cta .cta-row{justify-content:center; position:relative;}

  footer.site-footer{padding:30px 0 50px; text-align:center; color:var(--muted); font-family:var(--mono); font-size:12px;}
  footer.site-footer a{color:var(--cyan);}

  /* ---------- SYLLABUS PAGE ---------- */
  .syl-hero{padding:150px 0 50px; text-align:center;}
  .module{margin-bottom:14px;}
  .module-head{
    display:flex; align-items:center; justify-content:space-between;
    padding:18px 22px; cursor:pointer; user-select:none;
  }
  .module-head .m-left{display:flex; align-items:center; gap:14px;}
  .m-id{font-family:var(--mono); color:var(--cyan); font-size:13px; min-width:30px;}
  .m-title{font-family:var(--display); font-weight:700; font-size:16px;}
  .m-chevron{transition:transform .25s; color:var(--muted);}
  .module.open .m-chevron{transform:rotate(180deg); color:var(--cyan);}
  .module-body{
    max-height:0; overflow:hidden; transition:max-height .35s ease;
    border-top:1px solid var(--line);
  }
  .module.open .module-body{border-top:1px solid var(--line);}
  .module-body-inner{padding:18px 22px; display:flex; flex-wrap:wrap; gap:18px;}
  .module-col{flex:1; min-width:200px;}
  .module-col h4{font-family:var(--mono); font-size:11px; color:var(--amber); text-transform:uppercase; letter-spacing:.5px; margin-bottom:10px;}
  .module-col ul{list-style:none; color:var(--muted); font-size:13.5px; display:flex; flex-direction:column; gap:6px;}
  .module-col ul li::before{content:'—'; color:var(--cyan); margin-right:8px;}
  .tag-row{display:flex; gap:8px; flex-wrap:wrap;}

  /* ---------- responsive ---------- */
  @media(max-width:860px){
    .hero-grid, .about-grid{grid-template-columns:1fr;}
    .stack-grid{grid-template-columns:1fr 1fr;}
    h1.headline{font-size:36px;}
    .nav-links{display:none;}
  }
  @media(max-width:560px){
    .stack-grid{grid-template-columns:1fr;}
    .stat-row{grid-template-columns:1fr;}
  }

  /* focus visibility */
  a:focus-visible, .module-head:focus-visible, button:focus-visible{
    outline:2px solid var(--cyan); outline-offset:2px;
  }
</style>
"""

# =========================================================
#  Shared layout
# =========================================================
def get_layout(title, content, active_page="home"):
    home_active = "active" if active_page == "home" else ""
    syllabus_active = "active" if active_page == "syllabus" else ""
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} · Veera Sir — MultiCloud DevOps</title>
  {STYLE}
</head>
<body>

  <nav class="navbar">
    <a href="/?page=home" class="nav-logo">
      <span class="dot"></span> veera<span class="tag">::</span>ops
    </a>
    <div class="nav-links">
      <a href="/?page=home" class="{home_active}">~/home</a>
      <a href="/?page=syllabus" class="{syllabus_active}">~/syllabus</a>
    </div>
    <a href="https://instagram.com/cloud_tech_devops" target="_blank" rel="noopener" class="nav-cta">@cloud_tech_devops ↗</a>
  </nav>

  {content}

  <footer class="site-footer">
    <div class="container">
      $ echo "Veera Sir — MultiCloud DevOps" &nbsp;·&nbsp;
      <a href="https://instagram.com/cloud_tech_devops" target="_blank" rel="noopener">Instagram</a>
      &nbsp;·&nbsp; built &amp; deployed with care
    </div>
  </footer>

  <script>
    // ---- scroll reveal ----
    const reveals = document.querySelectorAll('.reveal');
    const io = new IntersectionObserver((entries) => {{
      entries.forEach(e => {{ if (e.isIntersecting) e.target.classList.add('in'); }});
    }}, {{ threshold: 0.15 }});
    reveals.forEach(el => io.observe(el));

    // ---- hero terminal typing ----
    const typedEl = document.getElementById('typed-line');
    if (typedEl) {{
      const lines = [
        'kubectl get nodes --all-namespaces',
        'terraform apply -auto-approve',
        'aws eks update-kubeconfig --name prod-cluster',
        'az aks scale --resource-group ops --node-count 5'
      ];
      let li = 0, ci = 0, deleting = false;
      function tick() {{
        const full = lines[li];
        if (!deleting) {{
          ci++;
          typedEl.textContent = full.slice(0, ci);
          if (ci === full.length) {{ deleting = true; setTimeout(tick, 1600); return; }}
        }} else {{
          ci--;
          typedEl.textContent = full.slice(0, ci);
          if (ci === 0) {{ deleting = false; li = (li + 1) % lines.length; }}
        }}
        setTimeout(tick, deleting ? 28 : 45);
      }}
      tick();
    }}

    // ---- syllabus accordion ----
    document.querySelectorAll('.module-head').forEach(head => {{
      head.addEventListener('click', () => {{
        const mod = head.closest('.module');
        const body = mod.querySelector('.module-body');
        const wasOpen = mod.classList.contains('open');
        document.querySelectorAll('.module.open').forEach(m => {{
          m.classList.remove('open');
          m.querySelector('.module-body').style.maxHeight = null;
        }});
        if (!wasOpen) {{
          mod.classList.add('open');
          body.style.maxHeight = body.scrollHeight + 'px';
        }}
      }});
    }});
  </script>
</body>
</html>
"""

# =========================================================
#  Signature visual — animated multi-cloud node graph (inline SVG)
# =========================================================
def get_node_graph():
    return """
    <div class="graph-wrap reveal">
      <svg viewBox="0 0 400 400" aria-hidden="true">
        <line class="edge"      x1="200" y1="200" x2="90"  y2="110" />
        <line class="edge alt"  x1="200" y1="200" x2="310" y2="110" />
        <line class="edge"      x1="200" y1="200" x2="200" y2="330" />

        <circle class="pulse-ring"        cx="200" cy="200" r="34" />
        <circle class="pulse-ring d2"     cx="200" cy="200" r="34" />
        <circle class="pulse-ring d3"     cx="200" cy="200" r="34" />

        <g class="core-node">
          <circle cx="200" cy="200" r="34" />
          <text x="200" y="197" text-anchor="middle" class="node-label">OPS</text>
          <text x="200" y="210" text-anchor="middle" class="node-sub">hub</text>
        </g>

        <g class="leaf-node">
          <circle cx="90" cy="110" r="26" />
          <text x="90" y="106" text-anchor="middle" class="node-label">AWS</text>
          <text x="90" y="119" text-anchor="middle" class="node-sub">EC2 · EKS</text>
        </g>
        <g class="leaf-node">
          <circle cx="310" cy="110" r="26" />
          <text x="310" y="106" text-anchor="middle" class="node-label">Azure</text>
          <text x="310" y="119" text-anchor="middle" class="node-sub">AKS · VMs</text>
        </g>
        <g class="leaf-node">
          <circle cx="200" cy="330" r="26" />
          <text x="200" y="326" text-anchor="middle" class="node-label">GCP</text>
          <text x="200" y="339" text-anchor="middle" class="node-sub">GKE · Run</text>
        </g>
      </svg>
    </div>
    """

# =========================================================
#  HOME PAGE CONTENT
# =========================================================
def get_home_content():
    node_graph = get_node_graph()
    return f"""
  <header class="hero">
    <div class="container hero-grid">
      <div>
        <div class="eyebrow">Multi-Cloud · DevOps · Naresh IT</div>
        <h1 class="headline">Ship infrastructure<br>like an <span class="accent">SRE</span>,<br>not a tutorial.</h1>
        <p class="lede">Veera Sir teaches MultiCloud DevOps end-to-end — AWS, Azure and GCP, wired together with Terraform, Kubernetes and a real CI/CD pipeline. Daily drops on Instagram, deep dives in class.</p>
        <div class="cta-row">
          <a href="/?page=syllabus" class="btn btn-primary">View Syllabus →</a>
          <a href="https://instagram.com/cloud_tech_devops" target="_blank" rel="noopener" class="btn btn-ghost">Follow @cloud_tech_devops</a>
        </div>
      </div>

      <div class="term">
        <div class="term-bar">
          <span class="tdot"></span><span class="tdot"></span><span class="tdot"></span>
          <span class="term-title">veera@multicloud:~</span>
        </div>
        <div class="term-body">
          <div class="term-line"><span class="prompt">$</span> <span id="typed-line" class="typed"></span></div>
          <div class="term-out">// three clouds. one workflow. zero excuses.</div>
        </div>
      </div>
    </div>
  </header>

  <section>
    <div class="container">
      <div class="section-head reveal">
        <div class="eyebrow">Live architecture</div>
        <h2 class="section-title">One hub, three clouds</h2>
        <p class="section-sub">The same DevOps muscle, applied wherever the workload lives.</p>
      </div>
      {node_graph}
    </div>
  </section>

  <section>
    <div class="container">
      <div class="section-head reveal">
        <div class="eyebrow">The stack</div>
        <h2 class="section-title">What you'll actually run</h2>
        <p class="section-sub">No slideware — every module ends with hands-on labs on real cloud accounts.</p>
      </div>
      <div class="stack-grid">

        <div class="term stack-card reveal">
          <div class="term-bar"><span class="tdot"></span><span class="tdot"></span><span class="tdot"></span><span class="term-title">aws.sh</span></div>
          <div class="term-body">
            <ul>
              <li>EC2, VPC, IAM, S3</li>
              <li>EKS &amp; ECS</li>
              <li>Lambda &amp; CloudFront</li>
              <li>RDS &amp; DynamoDB</li>
            </ul>
          </div>
        </div>

        <div class="term stack-card reveal">
          <div class="term-bar"><span class="tdot"></span><span class="tdot"></span><span class="tdot"></span><span class="term-title">azure.sh</span></div>
          <div class="term-body">
            <ul>
              <li>Virtual Machines &amp; VNet</li>
              <li>AKS</li>
              <li>Azure Functions</li>
              <li>Azure DevOps Pipelines</li>
            </ul>
          </div>
        </div>

        <div class="term stack-card reveal">
          <div class="term-bar"><span class="tdot"></span><span class="tdot"></span><span class="tdot"></span><span class="term-title">gcp.sh</span></div>
          <div class="term-body">
            <ul>
              <li>Compute Engine &amp; VPC</li>
              <li>GKE &amp; Cloud Run</li>
              <li>Cloud Functions</li>
              <li>BigQuery basics</li>
            </ul>
          </div>
        </div>

        <div class="term stack-card reveal">
          <div class="term-bar"><span class="tdot"></span><span class="tdot"></span><span class="tdot"></span><span class="term-title">iac.tf</span></div>
          <div class="term-body">
            <ul>
              <li>Terraform modules</li>
              <li>State &amp; remote backends</li>
              <li>Ansible basics</li>
              <li>GitOps workflows</li>
            </ul>
          </div>
        </div>

        <div class="term stack-card reveal">
          <div class="term-bar"><span class="tdot"></span><span class="tdot"></span><span class="tdot"></span><span class="term-title">pipeline.yml</span></div>
          <div class="term-body">
            <ul>
              <li>Jenkins &amp; GitHub Actions</li>
              <li>Docker &amp; image registries</li>
              <li>Helm charts</li>
              <li>Blue-green / canary releases</li>
            </ul>
          </div>
        </div>

        <div class="term stack-card reveal">
          <div class="term-bar"><span class="tdot"></span><span class="tdot"></span><span class="tdot"></span><span class="term-title">observability.yml</span></div>
          <div class="term-body">
            <ul>
              <li>Prometheus &amp; Grafana</li>
              <li>Alertmanager</li>
              <li>Centralized logging</li>
              <li>SLOs &amp; on-call basics</li>
            </ul>
          </div>
        </div>

      </div>
    </div>
  </section>

  <section>
    <div class="container about-grid">
      <div class="reveal">
        <div class="eyebrow">Instructor</div>
        <h2 class="section-title">Veera Sir</h2>
        <div class="about-copy" style="margin-top:16px;">
          <p>Veera Sir teaches the MultiCloud DevOps course at Naresh IT, taking students from first principles to production-grade pipelines across AWS, Azure and GCP.</p>
          <p>Outside the classroom, the work continues on Instagram — a running series breaking down cloud and DevOps concepts one carousel at a time.</p>
        </div>
        <div class="stat-row">
          <div class="stat"><div class="v">AWS · Azure · GCP</div><div class="l">Cloud coverage</div></div>
          <div class="stat"><div class="v">Daily</div><div class="l">Instagram drops</div></div>
          <div class="stat"><div class="v">Hands-on</div><div class="l">Lab-first teaching</div></div>
        </div>
        <div class="badge-row">
          <span class="badge">#Terraform</span><span class="badge">#Kubernetes</span>
          <span class="badge">#CI/CD</span><span class="badge">#Prometheus</span><span class="badge">#GitOps</span>
        </div>
      </div>

      <div class="term reveal">
        <div class="term-bar"><span class="tdot"></span><span class="tdot"></span><span class="tdot"></span><span class="term-title">whoami.sh</span></div>
        <div class="term-body">
          <div class="term-line"><span class="prompt">$</span> whoami</div>
          <div class="term-out" style="margin-bottom:14px;">veera_sir — multicloud devops instructor, naresh it</div>
          <div class="term-line"><span class="prompt">$</span> cat focus.txt</div>
          <div class="term-out">teaching real pipelines, not just theory.<br>aws + azure + gcp, one mental model.</div>
        </div>
      </div>
    </div>
  </section>

  <section>
    <div class="container">
      <div class="footer-cta reveal">
        <h2>Ready to go multi-cloud?</h2>
        <p>Get the full syllabus, or follow along daily on Instagram for bite-sized DevOps breakdowns.</p>
        <div class="cta-row">
          <a href="/?page=syllabus" class="btn btn-primary">Explore the Syllabus →</a>
          <a href="https://instagram.com/cloud_tech_devops" target="_blank" rel="noopener" class="btn btn-ghost">@cloud_tech_devops</a>
        </div>
      </div>
    </div>
  </section>
    """

# =========================================================
#  SYLLABUS PAGE CONTENT
# =========================================================
def module(idx, title, topics, tools):
    topics_html = "".join(f"<li>{t}</li>" for t in topics)
    tags_html = "".join(f"<span class='badge'>{t}</span>" for t in tools)
    return f"""
      <div class="module term reveal">
        <div class="module-head" tabindex="0">
          <div class="m-left">
            <span class="m-id">{idx:02d}</span>
            <span class="m-title">{title}</span>
          </div>
          <span class="m-chevron">▾</span>
        </div>
        <div class="module-body">
          <div class="module-body-inner">
            <div class="module-col">
              <h4>Topics</h4>
              <ul>{topics_html}</ul>
            </div>
            <div class="module-col">
              <h4>Tools</h4>
              <div class="tag-row">{tags_html}</div>
            </div>
          </div>
        </div>
      </div>
    """

def get_syllabus_content():
    modules = [
        module(1, "AWS Fundamentals", ["IAM, EC2 &amp; VPC networking", "S3 &amp; storage classes", "Elastic IP vs Public/Private IP", "Auto Scaling &amp; Load Balancers"], ["EC2", "IAM", "VPC", "S3"]),
        module(2, "Microsoft Azure", ["Resource Groups &amp; VNets", "Virtual Machines &amp; Scale Sets", "Azure AD basics", "Azure DevOps Pipelines"], ["VMs", "VNet", "Azure DevOps"]),
        module(3, "Google Cloud Platform", ["Compute Engine &amp; VPC", "IAM &amp; service accounts", "Cloud Storage &amp; BigQuery basics", "GKE fundamentals"], ["GCE", "GKE", "BigQuery"]),
        module(4, "Terraform &amp; IaC", ["Providers, state &amp; backends", "Modules &amp; reusable infra", "Workspaces &amp; environments", "Ansible for configuration"], ["Terraform", "Ansible"]),
        module(5, "Containers &amp; Kubernetes", ["Docker images &amp; registries", "Pods, Deployments &amp; Services", "Helm charts", "Multi-cloud cluster patterns (EKS/AKS/GKE)"], ["Docker", "Kubernetes", "Helm"]),
        module(6, "CI/CD Pipelines", ["Jenkins pipelines", "GitHub Actions workflows", "Build → test → deploy gates", "Blue-green &amp; canary releases"], ["Jenkins", "GitHub Actions"]),
        module(7, "Monitoring &amp; Observability", ["Prometheus metrics &amp; exporters", "Grafana dashboards", "Alertmanager routing", "Centralized logging basics"], ["Prometheus", "Grafana", "Alertmanager"]),
        module(8, "Capstone: Multi-Cloud Project", ["Design a workload spanning AWS + Azure or GCP", "Provision with Terraform end-to-end", "Wire up a CI/CD pipeline", "Add monitoring &amp; alerting"], ["Terraform", "CI/CD", "Grafana"]),
    ]
    modules_html = "".join(modules)
    return f"""
  <header class="syl-hero">
    <div class="container">
      <div class="eyebrow" style="justify-content:center;">Curriculum</div>
      <h1 class="headline" style="font-size:38px;">The MultiCloud<br><span class="accent">DevOps</span> Syllabus</h1>
      <p class="lede" style="margin:18px auto 0;">Eight modules, three clouds, one continuous pipeline. Click a module to expand it.</p>
    </div>
  </header>

  <section style="padding-top:30px;">
    <div class="container" style="max-width:780px;">
      {modules_html}
    </div>
  </section>

  <section style="padding-top:0;">
    <div class="container">
      <div class="footer-cta reveal">
        <h2>Questions about the course?</h2>
        <p>Reach out through Instagram — new breakdowns drop daily on @cloud_tech_devops.</p>
        <div class="cta-row">
          <a href="https://instagram.com/cloud_tech_devops" target="_blank" rel="noopener" class="btn btn-primary">Message on Instagram →</a>
          <a href="/?page=home" class="btn btn-ghost">← Back to Home</a>
        </div>
      </div>
    </div>
  </section>
    """

# =========================================================
#  ROUTES
# =========================================================
@app.route("/")
def home():
    page = request.args.get("page", "home")
    if page == "syllabus":
        return get_layout("Syllabus", get_syllabus_content(), active_page="syllabus")
    return get_layout("Home", get_home_content(), active_page="home")

@app.route("/health")
def health():
    return {"status": "Healthy"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
