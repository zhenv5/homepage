import os
import subprocess
from datetime import datetime, timedelta, date
from collections import Counter
import json
import re
import html

# Load parsed papers
with open("/Users/jiankai/Library/CloudStorage/Dropbox/Codes/homepage/.oil-ui/papers.json", "r", encoding="utf-8") as f:
    papers = json.load(f)

# Generate Overall Activity Heatmap SVG (including private & public repos)
def generate_overall_heatmap(svg_path="/Users/jiankai/Library/CloudStorage/Dropbox/Codes/homepage/assets/github-heatmap.svg"):
    base = '/Users/jiankai/Library/CloudStorage/Dropbox/Codes'
    today = date.today()
    start_date = today - timedelta(days=364)
    while start_date.weekday() != 6:
        start_date -= timedelta(days=1)

    commit_counts = Counter()
    for d in os.listdir(base):
        full = os.path.join(base, d)
        if os.path.isdir(os.path.join(full, '.git')):
            try:
                cmd = ['git', '-C', full, 'log', f'--since={start_date.strftime("%Y-%m-%d")}', '--format=%ad', '--date=short']
                out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode('utf-8')
                for dt in out.splitlines():
                    dt = dt.strip()
                    if dt:
                        commit_counts[dt] += 1
            except Exception:
                pass

    total_commits = sum(commit_counts.values())

    cell_size = 10
    cell_gap = 3
    left_margin = 28
    top_margin = 20
    width = left_margin + 53 * (cell_size + cell_gap) + 10
    height = top_margin + 7 * (cell_size + cell_gap) + 10

    def get_color(count):
        if count == 0:
            return '#ebedf0'
        elif count <= 4:
            return '#9be9a8'
        elif count <= 12:
            return '#40c463'
        elif count <= 25:
            return '#30a14e'
        else:
            return '#216e39'

    rects = []
    month_labels = []
    last_month = None

    curr = start_date
    week_idx = 0

    while curr <= today:
        day_of_week = (curr.weekday() + 1) % 7 # 0 is Sunday, 1 is Monday ... 6 is Saturday
        x = left_margin + week_idx * (cell_size + cell_gap)
        y = top_margin + day_of_week * (cell_size + cell_gap)
        dt_str = curr.strftime('%Y-%m-%d')
        count = commit_counts[dt_str]
        color = get_color(count)
        
        rects.append(f'<rect class="day" width="{cell_size}" height="{cell_size}" x="{x}" y="{y}" fill="{color}" rx="2" ry="2" data-date="{dt_str}" data-count="{count}"><title>{count} contributions on {dt_str}</title></rect>')
        
        if curr.day <= 7 and day_of_week == 0:
            month_name = curr.strftime('%b')
            if month_name != last_month:
                month_labels.append(f'<text x="{x}" y="12" font-size="10" fill="#767676" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif">{month_name}</text>')
                last_month = month_name
                
        if day_of_week == 6:
            week_idx += 1
        curr += timedelta(days=1)

    day_labels = [
        f'<text x="0" y="{top_margin + 1 * (cell_size + cell_gap) + 8}" font-size="9" fill="#767676" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif">Mon</text>',
        f'<text x="0" y="{top_margin + 3 * (cell_size + cell_gap) + 8}" font-size="9" fill="#767676" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif">Wed</text>',
        f'<text x="0" y="{top_margin + 5 * (cell_size + cell_gap) + 8}" font-size="9" fill="#767676" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif">Fri</text>'
    ]

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto">
  <style>
    .day {{ shape-rendering: geometricPrecision; outline: none; }}
    .day:hover {{ stroke: #0369a1; stroke-width: 1.5; }}
  </style>
  <g>
    {''.join(month_labels)}
    {''.join(day_labels)}
    {''.join(rects)}
  </g>
</svg>'''

    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg)

    return total_commits

overall_commit_count = generate_overall_heatmap()
print(f"Generated overall activity heatmap with {overall_commit_count} commits (including private repos).")

def categorize(p):
    title = p["title"].lower()
    venue = p["venue"].lower()
    
    if "patent" in venue or "patent" in title:
        return "patent"
    if any(k in title for k in ["split learning", "federated", "differential privacy", "private", "privacy", "protection", "leakage", "clean room", "unlearning"]):
        return "privacy"
    if any(k in title for k in ["code generation", "language model", "llm", "print debugging", "fairness"]):
        return "llm"
    if any(k in title for k in ["graph", "embedding", "hierarchy", "routing", "atp", "transitivity"]):
        return "graph"
    if any(k in title for k in ["recommend", "retrieval", "ranking", "subsampling", "collaborative filtering", "ads ranking"]):
        return "recsys"
    return "other"

links_map = {
    "label leakage and protection in two-party split learning": {
        "arxiv": "https://arxiv.org/abs/2102.08504",
        "code": "https://github.com/OscarcarLi/label-protection",
        "venue_badge": "ICLR 2022",
        "keywords": ["Split Learning", "Label Leakage", "Gradient Defense"],
        "tldr": "Demonstrates gradient inversion label leakage in vertical split learning and designs the Marvell noise defense mechanism to preserve privacy without degrading utility.",
        "highlight": True
    },
    "dpauc: differentially private auc computation in federated learning": {
        "arxiv": "https://arxiv.org/abs/2211.10486",
        "code": "https://github.com/bytedance/fedlearner/tree/master/example/privacy/DPAUC",
        "venue_badge": "AAAI 2023",
        "keywords": ["Federated Learning", "Differential Privacy", "AUC Optimization"],
        "tldr": "Formulates differentially private pairwise ranking loss optimization with DP-SGD for cross-silo advertising conversion.",
        "highlight": True
    },
    "privacy preserving conversion modeling in data clean room": {
        "venue_badge": "RecSys 2024",
        "keywords": ["Data Clean Room", "Privacy-Preserving ML", "Conversion Modeling"],
        "tldr": "Architects an end-to-end framework enabling multi-party ad attribution and CTR modeling within secure clean rooms.",
        "highlight": True
    },
    "decoupled entity representation learning for pinterest ads ranking": {
        "venue_badge": "RecSys 2025",
        "keywords": ["Ads Ranking", "Decoupled Representation", "Large-Scale RecSys"],
        "tldr": "Decouples query and pin entity embeddings to scale real-time retrieval across billions of candidates in Pinterest Ads.",
        "highlight": True
    },
    "leveraging print debugging to improve code generation in large language models": {
        "arxiv": "https://arxiv.org/abs/2401.05319",
        "venue_badge": "arXiv 2024",
        "keywords": ["LLM Code Generation", "Print Debugging", "Self-Refinement"],
        "tldr": "Proposes LDB (Large Language Model Debugger), enabling LLMs to segment, trace, and verify variable execution states like human developers.",
        "highlight": True
    },
    "weak proxies are sufficient and preferable for fairness with missing sensitive attributes": {
        "arxiv": "https://arxiv.org/abs/2306.03859",
        "venue_badge": "ICML 2023",
        "keywords": ["AI Fairness", "Weak Proxies", "Sensitive Attributes"],
        "tldr": "Proves that weak proxy representations achieve Pareto-optimal algorithmic fairness when sensitive attributes are unobserved.",
        "highlight": True
    },
    "pslf: defending against label leakage in split learning": {
        "venue_badge": "CIKM 2023",
        "keywords": ["Split Learning", "Adversarial Defense", "Feature Obfuscation"],
        "tldr": "Proposes perturbation mechanisms for intermediate representations to neutralize gradient inversion attacks in split networks.",
        "highlight": True
    },
    "dgrec: graph neural network for recommendation with diversified embedding generation": {
        "arxiv": "https://arxiv.org/abs/2211.10486",
        "code": "https://github.com/YangLiangwei/DGRec",
        "venue_badge": "WSDM 2023",
        "keywords": ["Graph Neural Networks", "Embedding Diversification", "RecSys"],
        "tldr": "Diversified graph embedding generation for mitigating filter bubbles in user-item recommendation graphs.",
        "highlight": True
    },
    "graph-based model-agnostic data subsampling for recommendation systems": {
        "venue_badge": "KDD 2023",
        "keywords": ["Graph Subsampling", "Efficiency", "Recommendation Scale"],
        "tldr": "Graph topological subsampling enabling extreme throughput and training speedup on massive recommender datasets.",
        "highlight": True
    },
    "netflix and forget: efficient and exact machine unlearning from bi-linear recommendations": {
        "arxiv": "https://arxiv.org/abs/2302.06676",
        "venue_badge": "NeurIPS W 2022",
        "keywords": ["Machine Unlearning", "Recommendation Privacy", "Bi-linear Models"],
        "tldr": "Provable exact machine unlearning algorithm removing user interaction data from bilinear recommendation models with minimal retraining.",
        "highlight": True
    },
    "defending against reconstruction attack in vertical federated learning": {
        "arxiv": "https://arxiv.org/abs/2107.09898",
        "code": "https://github.com/bytedance/fedlearner/tree/master/example/privacy/embedding_protection",
        "venue_badge": "FL-ICML 2021",
        "keywords": ["Vertical FedLearning", "Reconstruction Attack", "Feature Encryption"],
        "highlight": True
    },
    "learning an end-to-end structure for retrieval in large-scale recommendations": {
        "venue_badge": "CIKM 2021",
        "keywords": ["Retrieval Indexing", "End-to-End Learning", "Recommendation Systems"],
        "highlight": True
    },
    "atp: directed graph embedding with asymmetric transitivity preservation": {
        "arxiv": "https://arxiv.org/abs/1811.00839",
        "code": "https://github.com/zhenv5/atp",
        "pdf": "documents/Paper_ATP_Directed_Graph_Embedding_AAAI_2019.pdf",
        "slides": "documents/Slides_AAAI_2019_ATP.pdf",
        "venue_badge": "AAAI 2019",
        "keywords": ["Directed Graph Embedding", "Asymmetric Transitivity", "Non-linear Mapping"],
        "tldr": "Preserves high-order directed reachability and transitivity via asymmetric non-linear dual-vector projections.",
        "highlight": True
    },
    "breaking cycles in noisy hierarchies": {
        "arxiv": "https://arxiv.org/abs/1703.08100",
        "code": "https://github.com/zhenv5/breaking_cycles_in_noisy_hierarchies",
        "pdf": "documents/Paper_WebSci_17_Breaking_Cycles_in_Noisy_Hierarchies.pdf",
        "slides": "documents/Slides_WebSci_2017_Breaking_Cycles_in_Noisy_Hierarchies.pdf",
        "venue_badge": "WebSci 2017",
        "keywords": ["Noisy Hierarchies", "Cycle Breaking", "Social Graphs"],
        "tldr": "Approximation algorithm resolving minimal feedback arc sets in web and noisy social hierarchies."
    },
    "coldroute: effective routing of cold questions in stack exchange sites: j. sun et al.": {
        "arxiv": "https://arxiv.org/abs/1807.00462",
        "slides": "documents/Slides_ECMLPKDD_2018_ColdRoute.pdf",
        "code": "https://github.com/zhenv5/ColdRoute",
        "venue_badge": "ECML PKDD 2018",
        "keywords": ["Cold-Start Routing", "Factorization Machines", "Stack Exchange"]
    },
    "vsrank: a novel framework for ranking-based collaborative filtering": {
        "pdf": "documents/Paper_TIST2014_VSRank.pdf",
        "venue_badge": "ACM TIST 2014",
        "keywords": ["Collaborative Filtering", "Ranking Optimization", "Vector Space Model"]
    },
    "learning to rank for hybrid recommendation": {
        "pdf": "documents/Paper_CIKM2012_Learning_to_Rank_for_Hybrid_R.pdf",
        "venue_badge": "CIKM 2012",
        "keywords": ["Hybrid Recommendations", "Learning to Rank", "Feature Fusion"]
    },
    "adapting vector space model to ranking-based collaborative filtering": {
        "pdf": "documents/Paper_CIKM2012_Adapting_Vector_Space_Model_to_Ranking_based_CF.pdf",
        "venue_badge": "CIKM 2012",
        "keywords": ["Vector Space Model", "CF Ranking", "Implicit Feedback"]
    }
}

def generate_bibtex(p):
    words = [w for w in re.sub(r'[^a-zA-Z0-9 ]', '', p["title"]).split() if w.lower() not in ["a", "an", "the", "in", "on", "for"]]
    prefix = words[0].lower() if words else "paper"
    key = f"{prefix}{p['year'] or '2024'}"
    authors_clean = p["authors"].replace("…", "and others")
    v_clean = p["venue"].split(',')[0].strip() or "Conference / Journal"
    return f"""@article{{{key},
  title={{{p['title']}}},
  author={{{authors_clean}}},
  journal={{{v_clean}}},
  year={{{p['year'] or '2024'}}}
}}"""

def format_authors(authors_str):
    res = authors_str
    patterns = [r'\bJiankai Sun\b', r'\bJ Sun\b', r'\bJ\. Sun\b']
    for pat in patterns:
        res = re.sub(pat, r'<span class="author-self">\g<0></span>', res)
    return res

# Count category totals for pillars
cat_counts = {"privacy": 0, "recsys": 0, "graph": 0, "llm": 0, "patent": 0, "other": 0}
for p in papers:
    cat = categorize(p)
    cat_counts[cat] = cat_counts.get(cat, 0) + 1

pub_cards_html = []
patent_cards_html = []

for idx, p in enumerate(papers):
    title_lower = p["title"].lower().strip()
    cat = categorize(p)
    meta = links_map.get(title_lower, {})
    
    badge = meta.get("venue_badge")
    if not badge:
        if cat == "patent":
            badge = "Patent"
        elif p["year"]:
            badge = f"{p['year']}"
        else:
            badge = "Research"
            
    # Unified, scholarly badge styles (slate-blue for tier venues, neutral slate for others)
    is_top_venue = any(v in badge for v in ["ICLR", "AAAI", "RecSys", "ICML", "KDD", "WSDM", "CIKM", "ACM", "NeurIPS"])
    badge_class = "badge-tier" if is_top_venue else "badge-neutral"
            
    cites_badge = f'<span class="cite-count mono">{p["cites"]} cites</span>' if p["cites"] > 0 else ''
    is_highlight = meta.get("highlight", False) or p["cites"] >= 40
    
    # Action buttons - Clean typographic links with subtle arrows, NO EMOJIS!
    action_btns = []
    if meta.get("arxiv"):
        action_btns.append(f'<a href="{meta["arxiv"]}" target="_blank" rel="noopener" class="action-btn">arXiv ↗</a>')
    if meta.get("code"):
        action_btns.append(f'<a href="{meta["code"]}" target="_blank" rel="noopener" class="action-btn">Code ↗</a>')
    if meta.get("pdf"):
        action_btns.append(f'<a href="{meta["pdf"]}" target="_blank" rel="noopener" class="action-btn">PDF ↗</a>')
    if meta.get("slides"):
        action_btns.append(f'<a href="{meta["slides"]}" target="_blank" rel="noopener" class="action-btn">Slides ↗</a>')
    if p.get("scholar_link"):
        action_btns.append(f'<a href="{p["scholar_link"]}" target="_blank" rel="noopener" class="action-btn">Scholar ↗</a>')
        
    bib_text = html.escape(generate_bibtex(p))
    action_btns.append(
        f'<button type="button" class="action-btn bib-btn" data-bib="{bib_text}" onclick="copyBibtex(this)" title="Copy BibTeX citation">'
        f'<svg class="bib-icon" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        f'<rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>'
        f'<path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>'
        f'</svg>'
        f'<span>BibTeX</span>'
        f'</button>'
    )

    actions_html = f'<div class="pub-actions mono">{"".join(action_btns)}</div>'
    
    # TL;DR note if present
    tldr_html = f'<div class="pub-tldr"><span class="tldr-badge mono">TL;DR:</span> {html.escape(meta["tldr"])}</div>' if meta.get("tldr") else ''

    # Minimal keyword tags (curated, max 3)
    kw_chips = []
    for kw in meta.get("keywords", [])[:3]:
        kw_chips.append(f'<span class="paper-kw mono">#{kw}</span>')
    kw_html = f'<div class="paper-keywords">{"".join(kw_chips)}</div>' if kw_chips else ''

    # Clean, elegant card layout without excessive inner borders
    card_html = f"""
    <article class="pub-card" data-category="{cat}" data-highlight="{'true' if is_highlight else 'false'}" data-year="{p['year']}">
      <div class="pub-header">
        <span class="venue-badge {badge_class} mono">{badge}</span>
        <h3 class="pub-title">{html.escape(p['title'])}</h3>
        {cites_badge}
      </div>
      <div class="pub-authors">{format_authors(html.escape(p['authors']))}</div>
      <div class="pub-venue">{html.escape(p['venue'])}</div>
      {tldr_html}
      {kw_html}
      {actions_html}
    </article>
    """
    
    if cat == "patent":
        patent_cards_html.append(card_html)
    else:
        pub_cards_html.append(card_html)

print(f"Generated {len(pub_cards_html)} publications and {len(patent_cards_html)} patents.")

full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Jiankai Sun — Machine Learning Engineer & Researcher</title>
  <meta name="description" content="Personal academic and engineering homepage of Jiankai Sun. Machine Learning Engineer at Pinterest, ex-ByteDance AML-US, Ph.D. from The Ohio State University.">
  <meta name="keywords" content="Jiankai Sun, Machine Learning, Pinterest, ByteDance, Federated Learning, Split Learning, Privacy, LLM, Graph Embedding, Recommender Systems">
  <meta property="og:title" content="Jiankai Sun — Machine Learning Engineer & Researcher">
  <meta property="og:description" content="Machine Learning Engineer at Pinterest · Ex-ByteDance AML-US · Ph.D. in CS @ The Ohio State University">
  <meta property="og:type" content="website">
  <link rel="canonical" href="https://jiankaisun.com/">
  <meta property="og:url" content="https://jiankaisun.com/">

  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-Y64RCNPS3S"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());

    gtag('config', 'G-Y64RCNPS3S');
  </script>

  <!-- Cloudflare Web Analytics -->
  <script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "89b3581f8f6643fca01d90ace429ef61"}}'></script>
  <!-- End Cloudflare Web Analytics -->

  <style>
    *, *::before, *::after {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    :root {{
      --bg: #fafaf9;
      --card-bg: #ffffff;
      --text-main: #1c1917;
      --text-muted: #57534e;
      --text-sub: #78716c;
      --border: #e7e5e4;
      --border-focus: #cbd5e1;
      --primary: #0369a1;
      --primary-hover: #075985;
      --primary-light: #f0f9ff;
      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 14px;
    }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      background-color: var(--bg);
      color: var(--text-main);
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }}
    .mono {{
      font-family: ui-monospace, "SF Mono", Menlo, Monaco, Consolas, monospace;
    }}
    .serif {{
      font-family: Charter, "Bitstream Charter", "Sitka Text", Cambria, Georgia, serif;
    }}

    /* Compact Sticky Utility Header */
    .utility-header {{
      background: rgba(250, 250, 249, 0.94);
      backdrop-filter: blur(10px);
      border-bottom: 1px solid var(--border);
      padding: 0 28px;
      height: 52px;
      position: sticky;
      top: 0;
      z-index: 50;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 13.5px;
    }}
    .nav-brand {{
      font-weight: 700;
      color: var(--text-main);
      text-decoration: none;
      display: flex;
      align-items: center;
      gap: 10px;
      flex-shrink: 0;
    }}
    .brand-title {{
      font-size: 15px;
      letter-spacing: -0.01em;
    }}
    .brand-chip {{
      background: #f1f5f9;
      color: #334155;
      border: 1px solid #e2e8f0;
      font-size: 11px;
      font-weight: 600;
      padding: 2px 7px;
      border-radius: var(--radius-sm);
    }}
    .nav-links {{
      display: flex;
      gap: 22px;
      font-weight: 500;
      color: var(--text-muted);
      align-items: center;
    }}
    .nav-links a {{
      color: inherit;
      text-decoration: none;
      transition: color 0.15s;
    }}
    .nav-links a:hover {{
      color: var(--primary);
    }}
    .status-location {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      color: #475569;
      font-weight: 500;
      font-size: 12.5px;
      flex-shrink: 0;
    }}
    .loc-dot {{
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: #0369a1;
    }}

    /* Main Container with Open Canvas Breathing Room */
    .container {{
      max-width: 1200px;
      width: 100%;
      margin: 0 auto;
      padding: 36px 24px 80px 24px;
      display: flex;
      flex-direction: column;
      gap: 48px;
    }}

    /* Hero Section: Editorial Academic Centered Stage */
    .hero-section {{
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      gap: 22px;
      padding-bottom: 34px;
      border-bottom: 1px solid var(--border);
      max-width: 820px;
      margin: 0 auto;
      width: 100%;
    }}
    .hero-header {{
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      gap: 14px;
      width: 100%;
    }}
    .hero-title h1 {{
      font-size: 42px;
      font-weight: 700;
      letter-spacing: -0.025em;
      color: #0c0a09;
      line-height: 1.15;
    }}
    .hero-subtitle {{
      font-size: 16px;
      color: var(--text-muted);
      margin-top: 4px;
      font-weight: 400;
      max-width: 62ch;
      margin-left: auto;
      margin-right: auto;
    }}
    .hero-subtitle strong {{
      color: #0c0a09;
      font-weight: 600;
    }}

    /* Balanced, Scholarly Social Links */
    .social-pills {{
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 8px;
    }}
    .social-pill {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      padding: 6px 12px;
      font-size: 13px;
      font-weight: 500;
      color: #292524;
      text-decoration: none;
      transition: all 0.15s;
    }}
    .social-pill svg {{
      width: 14px;
      height: 14px;
      fill: currentColor;
    }}
    .social-pill:hover {{
      border-color: #cbd5e1;
      background: #f8fafc;
      color: var(--primary);
      transform: translateY(-1px);
    }}

    /* Bio Narrative */
    .bio-prose {{
      font-size: 15.5px;
      line-height: 1.75;
      color: #292524;
      max-width: 66ch;
      margin: 0 auto;
      text-align: center;
    }}
    .bio-prose p {{
      margin-bottom: 12px;
    }}
    .bio-prose p:last-child {{
      margin-bottom: 0;
    }}
    .bio-prose strong {{
      color: #0c0a09;
      font-weight: 600;
    }}

    /* Scholarly Metrics Banner */
    .metrics-row {{
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 28px;
      padding-top: 10px;
      width: 100%;
    }}
    .metric-item {{
      display: flex;
      flex-direction: column;
    }}
    .metric-value {{
      font-size: 24px;
      font-weight: 700;
      color: #0c0a09;
      line-height: 1.1;
    }}
    .metric-label {{
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-sub);
      margin-top: 3px;
    }}
    .metric-divider {{
      width: 1px;
      height: 32px;
      background: var(--border);
    }}

    /* Section Headers */
    .section-header-block {{
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      flex-wrap: wrap;
      gap: 12px;
      margin-bottom: 18px;
    }}
    .section-headline {{
      font-size: 22px;
      font-weight: 700;
      letter-spacing: -0.015em;
      color: #0c0a09;
    }}
    .section-subtext {{
      font-size: 14px;
      color: var(--text-muted);
      margin-top: 2px;
    }}

    /* Open Canvas Research Pillars Section */
    .pillars-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
    }}
    .pillar-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 18px 20px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      cursor: pointer;
      text-decoration: none;
      color: inherit;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      position: relative;
    }}
    .pillar-card:hover {{
      border-color: #0369a1;
      box-shadow: 0 4px 16px rgba(3, 105, 161, 0.08);
      transform: translateY(-2px);
    }}
    .pillar-index {{
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.08em;
      color: #0369a1;
      text-transform: uppercase;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .pillar-count {{
      font-size: 11px;
      color: var(--text-sub);
      font-weight: 600;
    }}
    .pillar-title {{
      font-size: 15.5px;
      font-weight: 700;
      color: #0c0a09;
      line-height: 1.3;
    }}
    .pillar-desc {{
      font-size: 13px;
      color: var(--text-muted);
      line-height: 1.5;
      flex: 1;
    }}
    .pillar-action {{
      font-size: 12px;
      font-weight: 600;
      color: #0369a1;
      display: flex;
      align-items: center;
      gap: 4px;
      margin-top: 4px;
    }}

    /* Vibe Coding & Indie Software Section */
    .vibe-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 18px;
    }}
    .vibe-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .vibe-card:hover {{
      border-color: #cbd5e1;
      box-shadow: 0 6px 18px rgba(0,0,0,0.04);
      transform: translateY(-2px);
    }}
    .vibe-top {{
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      gap: 8px;
    }}
    .vibe-name {{
      font-size: 16px;
      font-weight: 700;
      color: #0c0a09;
    }}
    .vibe-category {{
      font-size: 11px;
      font-weight: 600;
      padding: 2px 7px;
      border-radius: 4px;
      background: #f1f5f9;
      color: #334155;
      border: 1px solid #e2e8f0;
    }}
    .vibe-desc {{
      font-size: 13.5px;
      color: var(--text-muted);
      line-height: 1.5;
      flex: 1;
    }}
    .vibe-tags {{
      display: flex;
      flex-wrap: wrap;
      gap: 5px;
    }}
    .vibe-tag {{
      font-size: 11px;
      font-weight: 500;
      color: var(--text-sub);
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      padding: 2px 6px;
      border-radius: 4px;
    }}
    .vibe-footer {{
      display: flex;
      align-items: center;
      gap: 8px;
      padding-top: 6px;
      border-top: 1px solid #f1f5f9;
    }}
    .vibe-btn {{
      font-size: 12px;
      font-weight: 600;
      color: var(--primary);
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 3px;
      padding: 4px 10px;
      border-radius: var(--radius-sm);
      background: #f0f9ff;
      border: 1px solid #bae6fd;
      transition: all 0.12s;
    }}
    .vibe-btn:hover {{
      background: #e0f2fe;
      color: var(--primary-hover);
    }}
    .vibe-status {{
      font-size: 11.5px;
      color: var(--text-sub);
      margin-left: auto;
    }}

    /* Two Column Layout Grid */
    .layout-grid {{
      display: grid;
      grid-template-columns: 380px 1fr;
      gap: 32px;
      align-items: start;
    }}

    /* Left Sidebar: GitHub & Open Source */
    .sidebar-col {{
      display: flex;
      flex-direction: column;
      gap: 20px;
    }}
    .sidebar-block {{
      display: flex;
      flex-direction: column;
      gap: 12px;
      border: none;
      background: none;
      box-shadow: none;
      border-radius: 0;
    }}
    .sidebar-head {{
      font-size: 12.5px;
      font-weight: 700;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: var(--text-sub);
      margin-bottom: 6px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .sidebar-head a {{
      color: var(--primary);
      text-decoration: none;
      font-size: 12px;
      text-transform: none;
      letter-spacing: normal;
    }}

    /* GitHub Heatmap Container */
    .heatmap-container {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}
    .heatmap-meta {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 12px;
      color: var(--text-sub);
    }}
    .heatmap-img {{
      width: 100%;
      height: auto;
      display: block;
    }}
    .heatmap-legend {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 11.5px;
      color: #78716c;
      border-top: 1px solid #f0f0ee;
      padding-top: 6px;
    }}
    .legend-squares {{
      display: flex;
      align-items: center;
      gap: 3px;
    }}
    .legend-sq {{
      width: 9px;
      height: 9px;
      border-radius: 2px;
    }}

    /* Featured Repos List */
    .repo-items {{
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin-top: 6px;
    }}
    .repo-card {{
      display: flex;
      flex-direction: column;
      gap: 4px;
      padding: 10px 12px;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      text-decoration: none;
      color: var(--text-main);
      transition: all 0.15s;
    }}
    .repo-card:hover {{
      border-color: #cbd5e1;
      transform: translateX(2px);
    }}
    .repo-name {{
      font-size: 13.5px;
      font-weight: 600;
      color: #0369a1;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .repo-desc {{
      font-size: 12.5px;
      color: var(--text-muted);
      line-height: 1.4;
    }}

    /* Right Column: Publications Stream */
    .main-col {{
      display: flex;
      flex-direction: column;
      gap: 18px;
    }}
    .filter-bar {{
      display: flex;
      flex-direction: column;
      gap: 12px;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 16px 20px;
    }}
    .search-wrapper {{
      position: relative;
      width: 100%;
    }}
    .search-input {{
      width: 100%;
      padding: 9px 36px 9px 34px;
      font-size: 13.5px;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      outline: none;
      background: #fafaf9;
      color: var(--text-main);
      transition: all 0.15s;
    }}
    .search-input:focus {{
      border-color: var(--primary);
      background: #ffffff;
      box-shadow: 0 0 0 3px rgba(3, 105, 161, 0.08);
    }}
    .search-icon {{
      position: absolute;
      left: 11px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-sub);
      pointer-events: none;
      display: flex;
      align-items: center;
    }}
    .search-kbd {{
      position: absolute;
      right: 12px;
      top: 50%;
      transform: translateY(-50%);
      font-size: 11px;
      font-weight: 600;
      color: #94a3b8;
      background: #f1f5f9;
      border: 1px solid #e2e8f0;
      padding: 2px 6px;
      border-radius: 4px;
      pointer-events: none;
      transition: opacity 0.15s;
    }}
    .search-clear {{
      position: absolute;
      right: 10px;
      top: 50%;
      transform: translateY(-50%);
      font-size: 14px;
      color: #64748b;
      background: none;
      border: none;
      cursor: pointer;
      display: none;
      padding: 4px 6px;
      border-radius: 4px;
    }}
    .search-clear:hover {{
      color: #0f172a;
      background: #f1f5f9;
    }}

    .filter-tabs {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }}
    .filter-btn {{
      background: #fafaf9;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      padding: 5px 11px;
      font-size: 12px;
      font-weight: 500;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.15s;
    }}
    .filter-btn:hover {{
      background: #f1f5f9;
      color: var(--text-main);
    }}
    .filter-btn.active {{
      background: #0f172a;
      border-color: #0f172a;
      color: #ffffff;
    }}

    /* Publications List & Cards */
    .pub-list {{
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    .pub-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 16px 20px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      transition: opacity 0.16s ease, transform 0.16s ease, border-color 0.15s ease;
    }}
    .pub-card:hover {{
      border-color: var(--border-focus);
      box-shadow: 0 4px 14px rgba(0,0,0,0.03);
      transform: translateY(-1px);
    }}
    .pub-header {{
      display: flex;
      align-items: baseline;
      flex-wrap: wrap;
      gap: 8px;
    }}
    .venue-badge {{
      font-size: 11px;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 4px;
      flex-shrink: 0;
      text-transform: uppercase;
      letter-spacing: 0.02em;
    }}
    /* Unified Scholarly Badge Styles */
    .badge-tier {{
      background: #f0f9ff;
      color: #0369a1;
      border: 1px solid #bae6fd;
    }}
    .badge-neutral {{
      background: #f8fafc;
      color: #475569;
      border: 1px solid #e2e8f0;
    }}

    .cite-count {{
      font-size: 11px;
      font-weight: 600;
      color: #0369a1;
      background: #f0f9ff;
      border: 1px solid #bae6fd;
      padding: 1px 7px;
      border-radius: 10px;
      margin-left: auto;
    }}

    .pub-title {{
      font-size: 15px;
      font-weight: 600;
      color: #0c0a09;
      line-height: 1.4;
      max-width: 78ch;
    }}
    .pub-authors {{
      font-size: 13.5px;
      color: var(--text-muted);
      line-height: 1.4;
    }}
    .author-self {{
      color: #0c0a09;
      font-weight: 700;
      text-decoration: underline;
      text-decoration-color: #cbd5e1;
      text-underline-offset: 2px;
    }}
    /* Natural publication venue font (no forced long mono lines) */
    .pub-venue {{
      font-size: 13px;
      color: var(--text-sub);
      line-height: 1.4;
      max-width: 82ch;
    }}
    /* Clean Editorial TL;DR */
    .pub-tldr {{
      font-size: 13px;
      color: var(--text-muted);
      line-height: 1.5;
      max-width: 72ch;
      margin: 2px 0 3px 0;
    }}
    .tldr-badge {{
      font-size: 11px;
      font-weight: 700;
      color: #0369a1;
      margin-right: 4px;
      letter-spacing: 0.03em;
    }}

    .paper-keywords {{
      display: flex;
      flex-wrap: wrap;
      gap: 5px;
      margin-top: 2px;
    }}
    .paper-kw {{
      font-size: 11px;
      color: #0369a1;
      background: #f0f9ff;
      border: 1px solid #bae6fd;
      padding: 1px 6px;
      border-radius: 3px;
    }}
    .pub-actions {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 6px;
    }}
    .action-btn {{
      display: inline-flex;
      align-items: center;
      gap: 3px;
      font-size: 11.5px;
      font-weight: 600;
      color: #334155;
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      padding: 3px 8px;
      border-radius: var(--radius-sm);
      text-decoration: none;
      cursor: pointer;
      transition: all 0.12s;
    }}
    .action-btn:hover {{
      background: #f1f5f9;
      border-color: #cbd5e1;
      color: var(--primary);
    }}
    .bib-btn {{
      color: #1e293b;
      background: #ffffff;
      border: 1px solid #cbd5e1;
      font-weight: 600;
      gap: 5px;
    }}
    .bib-btn:hover {{
      background: #f0f9ff;
      border-color: #0284c7;
      color: #0284c7;
      box-shadow: 0 1px 3px rgba(2, 132, 199, 0.12);
    }}
    .bib-btn:active {{
      transform: scale(0.97);
    }}
    .bib-btn.copied {{
      color: #15803d !important;
      border-color: #86efac !important;
      background: #f0fdf4 !important;
    }}
    .bib-icon {{
      flex-shrink: 0;
    }}

    /* Toast Notification */
    .toast {{
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: #0f172a;
      color: #ffffff;
      padding: 9px 16px;
      border-radius: var(--radius-sm);
      font-size: 12.5px;
      font-weight: 500;
      box-shadow: 0 4px 16px rgba(0,0,0,0.18);
      opacity: 0;
      pointer-events: none;
      transform: translateY(8px);
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      z-index: 999;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .toast.show {{
      opacity: 1;
      pointer-events: auto;
      transform: translateY(0);
    }}

    /* Responsive Breakpoints */
    @media (max-width: 1080px) {{
      .pillars-grid {{
        grid-template-columns: repeat(2, 1fr);
      }}
      .vibe-grid {{
        grid-template-columns: repeat(2, 1fr);
      }}
    }}
    @media (max-width: 960px) {{
      .layout-grid {{
        grid-template-columns: 1fr;
      }}
      .metrics-row {{
        gap: 16px;
      }}
      .metric-divider {{
        display: none;
      }}
    }}
    @media (max-width: 640px) {{
      /* Compact, non-wrapping mobile header with smooth edge-fade mask */
      .utility-header {{
        padding: 0 16px;
        height: 48px;
        gap: 12px;
      }}
      .brand-chip, .status-location {{
        display: none;
      }}
      .nav-links {{
        gap: 14px;
        font-size: 12.5px;
        overflow-x: auto;
        white-space: nowrap;
        -webkit-overflow-scrolling: touch;
        scrollbar-width: none;
        -webkit-mask-image: linear-gradient(to right, black 82%, transparent 100%);
        mask-image: linear-gradient(to right, black 82%, transparent 100%);
        padding-right: 16px;
      }}
      .nav-links::-webkit-scrollbar {{
        display: none;
      }}
      .container {{
        padding: 20px 14px 48px 14px;
        gap: 36px;
      }}
      .hero-title h1 {{
        font-size: 30px;
      }}
      .metrics-row {{
        flex-wrap: wrap;
        gap: 14px 24px;
      }}
      .metric-value {{
        font-size: 20px;
      }}
      .pillars-grid {{
        grid-template-columns: 1fr;
      }}
      .vibe-grid {{
        grid-template-columns: 1fr;
      }}
      .search-kbd {{
        display: none;
      }}
    }}
  </style>
</head>
<body>

  <!-- Compact Sticky Utility Header -->
  <header class="utility-header">
    <a href="#" class="nav-brand">
      <span class="brand-title">Jiankai Sun</span>
      <span class="brand-chip mono">AI / Systems</span>
    </a>
    <nav class="nav-links mono">
      <a href="#about">About</a>
      <a href="#research">Research</a>
      <a href="#vibe-coding">Vibe Coding</a>
      <a href="#publications">Publications</a>
      <a href="#opensource">Activity</a>
    </nav>
    <div class="status-location mono">
      <span class="loc-dot"></span>
      <span>Seattle, WA · Pinterest MLE</span>
    </div>
  </header>

  <!-- Main Container -->
  <main class="container">

    <!-- Hero Section: Open Canvas Editorial (No Boxy Cage) -->
    <section class="hero-section" id="about">
      <div class="hero-header">
        <div class="hero-title">
          <h1 class="serif">Jiankai Sun</h1>
          <div class="hero-subtitle">
            Machine Learning Engineer at <strong>Pinterest</strong> · Ph.D. in Computer Science (The Ohio State University)
          </div>
        </div>

        <div class="social-pills mono">
          <a href="https://scholar.google.com/citations?user=GQ6xw-oAAAAJ&hl=en" target="_blank" rel="noopener" class="social-pill">
            <svg viewBox="0 0 24 24"><path d="M12 24a7 7 0 1 1 0-14 7 7 0 0 1 0 14zm0-24L0 9.5l4 3.18v6.82h3v-4.5h10v4.5h3V12.68l4-3.18L12 0z"/></svg>
            Scholar (1.6k+ Cites)
          </a>
          <a href="https://github.com/zhenv5" target="_blank" rel="noopener" class="social-pill">
            <svg viewBox="0 0 24 24"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>
            GitHub @zhenv5
          </a>
          <a href="https://www.linkedin.com/in/jiankaisun/" target="_blank" rel="noopener" class="social-pill">
            <svg viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
            LinkedIn
          </a>
          <a href="https://twitter.com/zhenv5" target="_blank" rel="noopener" class="social-pill">
            <svg viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
            Twitter
          </a>
          <a href="mailto:sun.cse.osu@gmail.com" class="social-pill">
            <svg viewBox="0 0 24 24"><path d="M0 3v18h24v-18h-24zm21.518 2l-9.518 7.713-9.518-7.713h19.036zm-19.518 14v-11.817l9.518 7.713 9.518-7.713v11.817h-19.036z"/></svg>
            Email
          </a>
        </div>
      </div>

      <div class="bio-prose">
        <p>
          I am a Machine Learning Engineer at <strong>Pinterest</strong>. Previously, I was a Research Scientist at 
          <strong>ByteDance AML-US</strong> in Seattle. I obtained my Ph.D. in Computer Science from <strong>The Ohio State University</strong>, 
          advised by Prof. Srinivasan Parthasarathy.
        </p>
        <p>
          My research and engineering focus centers on 
          <strong>Privacy-Preserving Machine Learning</strong> (Federated Learning, Split Learning, Data Clean Rooms), 
          <strong>Large-Scale Recommender Systems</strong> (Ads ranking, decoupled representation learning, retrieval), 
          <strong>Graph Representation Learning</strong>, and 
          <strong>Large Language Models & Alignment</strong> (code generation, proxy fairness). 
          Outside of work, I love <strong>vibe coding</strong> indie mobile apps, traditional board games, and local-first utilities.
        </p>
      </div>

      <div class="metrics-row mono">
        <div class="metric-item">
          <div class="metric-value">1,639</div>
          <div class="metric-label">Citations</div>
        </div>
        <div class="metric-divider"></div>
        <div class="metric-item">
          <div class="metric-value">20</div>
          <div class="metric-label">h-index</div>
        </div>
        <div class="metric-divider"></div>
        <div class="metric-item">
          <div class="metric-value">23</div>
          <div class="metric-label">i10-index</div>
        </div>
        <div class="metric-divider"></div>
        <div class="metric-item">
          <div class="metric-value">50+</div>
          <div class="metric-label">Publications & Patents</div>
        </div>
      </div>
    </section>

    <!-- Research Themes Section (Open Canvas, Interactive Filter Linkage) -->
    <section class="section-block" id="research">
      <div class="section-header-block">
        <div>
          <h2 class="section-headline serif">Core Research Themes</h2>
          <p class="section-subtext">Scientific and algorithmic focus areas. Click any theme to explore corresponding publications.</p>
        </div>
      </div>

      <div class="pillars-grid">
        <!-- Pillar 1 -->
        <div class="pillar-card" onclick="filterByPillar('privacy')">
          <div class="pillar-index mono">
            <span>01 / PRIVACY</span>
            <span class="pillar-count">{cat_counts.get('privacy', 0)} papers</span>
          </div>
          <h3 class="pillar-title">Federated & Split Learning</h3>
          <p class="pillar-desc">
            Two-party split learning label protection, cross-silo differential privacy, data clean rooms, and vertical federated learning.
          </p>
          <div class="pillar-action mono">View papers →</div>
        </div>

        <!-- Pillar 2 -->
        <div class="pillar-card" onclick="filterByPillar('recsys')">
          <div class="pillar-index mono">
            <span>02 / RECSYS</span>
            <span class="pillar-count">{cat_counts.get('recsys', 0)} papers</span>
          </div>
          <h3 class="pillar-title">Recommender Systems</h3>
          <p class="pillar-desc">
            Decoupled representation learning for ads ranking, end-to-end retrieval, machine unlearning, and diversified item ranking.
          </p>
          <div class="pillar-action mono">View papers →</div>
        </div>

        <!-- Pillar 3 -->
        <div class="pillar-card" onclick="filterByPillar('graph')">
          <div class="pillar-index mono">
            <span>03 / GRAPHS</span>
            <span class="pillar-count">{cat_counts.get('graph', 0)} papers</span>
          </div>
          <h3 class="pillar-title">Graph Representation</h3>
          <p class="pillar-desc">
            Directed graph embedding with asymmetric transitivity preservation, cycle breaking in noisy hierarchies, and cold-start routing.
          </p>
          <div class="pillar-action mono">View papers →</div>
        </div>

        <!-- Pillar 4 -->
        <div class="pillar-card" onclick="filterByPillar('llm')">
          <div class="pillar-index mono">
            <span>04 / LLMS</span>
            <span class="pillar-count">{cat_counts.get('llm', 0)} papers</span>
          </div>
          <h3 class="pillar-title">LLMs & AI Alignment</h3>
          <p class="pillar-desc">
            Improving LLM code generation through print debugging, proxy fairness with missing sensitive attributes, and self-refinement.
          </p>
          <div class="pillar-action mono">View papers →</div>
        </div>
      </div>
    </section>

    <!-- Vibe Coding & Indie Software Section (Direct Website Links, No GitHub Buttons) -->
    <section class="section-block" id="vibe-coding">
      <div class="section-header-block">
        <div>
          <h2 class="section-headline serif">Vibe Coding & Indie Software</h2>
          <p class="section-subtext">Handcrafted native iOS apps, board game engines, and local-first personal utilities.</p>
        </div>
      </div>

      <div class="vibe-grid">
        <!-- Project 1 -->
        <div class="vibe-card">
          <div class="vibe-top">
            <span class="vibe-name">FolkBoardGames</span>
            <span class="vibe-category mono">Game Suite</span>
          </div>
          <p class="vibe-desc">
            Traditional folk board game suite (Ou-Zi Qi, Mi-Zi Qi, Xia-Shi Qi, Fang Qi). Zero-latency canvas rendering, offline AI engine, and interactive rules.
          </p>
          <div class="vibe-tags mono">
            <span class="vibe-tag">iOS App</span>
            <span class="vibe-tag">WeChat MiniGame</span>
            <span class="vibe-tag">Canvas AI</span>
          </div>
          <div class="vibe-footer">
            <a href="https://folkboardgames.com" target="_blank" rel="noopener" class="vibe-btn mono">folkboardgames.com ↗</a>
            <span class="vibe-status mono">Active Development</span>
          </div>
        </div>

        <!-- Project 2 -->
        <div class="vibe-card">
          <div class="vibe-top">
            <span class="vibe-name">TinyTasteBook</span>
            <span class="vibe-category mono">iOS App</span>
          </div>
          <p class="vibe-desc">
            Baby solids & allergy tracker designed with Swift & SwiftUI. Local-first architecture, zero analytics tracking, clear pediatric timeline, and clean reactions journal.
          </p>
          <div class="vibe-tags mono">
            <span class="vibe-tag">SwiftUI</span>
            <span class="vibe-tag">Local-First</span>
            <span class="vibe-tag">Privacy</span>
          </div>
          <div class="vibe-footer">
            <a href="https://tinytastebook.com" target="_blank" rel="noopener" class="vibe-btn mono">tinytastebook.com ↗</a>
            <span class="vibe-status mono">iOS 17+ Native</span>
          </div>
        </div>

        <!-- Project 3 -->
        <div class="vibe-card">
          <div class="vibe-top">
            <span class="vibe-name">HoiBaby</span>
            <span class="vibe-category mono">iOS Utility</span>
          </div>
          <p class="vibe-desc">
            Infant feeding routine tracker with iOS 17 Interactive Widgets and Live Activities. One-tap nursing timers, formula logs, and daily rhythm insights.
          </p>
          <div class="vibe-tags mono">
            <span class="vibe-tag">WidgetKit</span>
            <span class="vibe-tag">Live Activity</span>
            <span class="vibe-tag">Swift</span>
          </div>
          <div class="vibe-footer">
            <a href="https://hoibaby.com" target="_blank" rel="noopener" class="vibe-btn mono">hoibaby.com ↗</a>
            <span class="vibe-status mono">Interactive Widgets</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Two-Column Grid: Left Sidebar & Right Publications -->
    <div class="layout-grid" id="publications">
      
      <!-- Left Sidebar: Overall Activity & Open Source -->
      <aside class="sidebar-col" id="opensource">
        
        <!-- Live Overall Contribution Heatmap -->
        <div class="sidebar-block">
          <div class="sidebar-head mono">
            <span>Overall Activity</span>
            <a href="https://github.com/zhenv5" target="_blank" rel="noopener">@zhenv5 ↗</a>
          </div>
          
          <div class="heatmap-container">
            <div class="heatmap-meta mono">
              <span>Public & Private Repos</span>
              <span style="color: #0369a1; font-weight: 600;">{overall_commit_count:,} Commits</span>
            </div>
            
            <img src="assets/github-heatmap.svg" alt="Jiankai Sun Overall Activity Heatmap" class="heatmap-img" loading="lazy">
            
            <div class="heatmap-legend mono">
              <span>Less</span>
              <div class="legend-squares">
                <span class="legend-sq" style="background: #ebedf0;"></span>
                <span class="legend-sq" style="background: #9be9a8;"></span>
                <span class="legend-sq" style="background: #40c463;"></span>
                <span class="legend-sq" style="background: #30a14e;"></span>
                <span class="legend-sq" style="background: #216e39;"></span>
              </div>
              <span>More</span>
            </div>
          </div>

          <!-- Featured Open Source Repos -->
          <div class="repo-items">
            <a href="https://github.com/zhenv5/atp" target="_blank" rel="noopener" class="repo-card">
              <div class="repo-name mono">
                <span>zhenv5/atp</span>
                <span>★ 38</span>
              </div>
              <div class="repo-desc">Directed graph embedding preserving asymmetric transitivity (AAAI 2019).</div>
            </a>
            <a href="https://github.com/zhenv5/breaking_cycles_in_noisy_hierarchies" target="_blank" rel="noopener" class="repo-card">
              <div class="repo-name mono">
                <span>breaking_cycles_in_noisy_hierarchies</span>
                <span>★ 26</span>
              </div>
              <div class="repo-desc">Cycle breaking algorithms in noisy social and web hierarchies (WebSci 2017).</div>
            </a>
            <a href="https://github.com/zhenv5/ColdRoute" target="_blank" rel="noopener" class="repo-card">
              <div class="repo-name mono">
                <span>zhenv5/ColdRoute</span>
                <span>★ 19</span>
              </div>
              <div class="repo-desc">Cold-start question routing with factorization machines (ECML-PKDD 2018).</div>
            </a>
          </div>
        </div>

      </aside>

      <!-- Right Column: Searchable, Filterable Publications Stream -->
      <section class="main-col">
        
        <!-- Filter Controls -->
        <div class="filter-bar">
          <div class="search-wrapper">
            <span class="search-icon">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
            </span>
            <input type="text" id="paper-search" class="search-input" placeholder="Search publications by title, author, keyword, or venue..." oninput="handleSearch()">
            <span class="search-kbd mono" title="Press / to search">/</span>
            <button id="search-clear" class="search-clear mono" onclick="clearSearch()" title="Clear search">✕</button>
          </div>

          <div class="filter-tabs mono" id="filter-tabs">
            <button class="filter-btn active" data-filter="all" onclick="setFilter('all', this)">All ({len(papers)})</button>
            <button class="filter-btn" data-filter="highlight" onclick="setFilter('highlight', this)">Selected Highlights</button>
            <button class="filter-btn" data-filter="privacy" onclick="setFilter('privacy', this)">Privacy & Federated ({cat_counts.get('privacy', 0)})</button>
            <button class="filter-btn" data-filter="recsys" onclick="setFilter('recsys', this)">Recommender Systems ({cat_counts.get('recsys', 0)})</button>
            <button class="filter-btn" data-filter="graph" onclick="setFilter('graph', this)">Graph Learning ({cat_counts.get('graph', 0)})</button>
            <button class="filter-btn" data-filter="llm" onclick="setFilter('llm', this)">LLMs & Alignment ({cat_counts.get('llm', 0)})</button>
            <button class="filter-btn" data-filter="patent" onclick="setFilter('patent', this)">Patents ({len(patent_cards_html)})</button>
          </div>
        </div>

        <!-- Publications Stream -->
        <div class="pub-list" id="pub-container">
          {"".join(pub_cards_html)}
          {"".join(patent_cards_html)}
        </div>

        <div id="no-results" class="mono" style="display: none; padding: 40px; text-align: center; color: var(--text-sub); background: #ffffff; border: 1px solid var(--border); border-radius: var(--radius-md);">
          <div>No publications match your search or filter criteria.</div>
          <button type="button" onclick="resetAllFilters()" style="margin-top: 12px; padding: 6px 14px; font-size: 12px; border-radius: var(--radius-sm); border: 1px solid var(--border); background: #f8fafc; cursor: pointer; color: var(--text-main);">Reset all filters</button>
        </div>

      </section>
    </div>

  </main>

  <!-- BibTeX Toast -->
  <div id="toast" class="toast mono">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#22c55e" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
    <span>BibTeX citation copied to clipboard</span>
  </div>

  <script>
    let currentFilter = 'all';
    let currentSearch = '';

    function filterByPillar(cat) {{
      const tab = document.querySelector('.filter-btn[data-filter="' + cat + '"]');
      if (tab) {{
        setFilter(cat, tab);
      }}
      const pubSection = document.getElementById('publications');
      if (pubSection) {{
        pubSection.scrollIntoView({{ behavior: 'smooth' }});
      }}
    }}

    function setFilter(filter, btn) {{
      currentFilter = filter;
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
      applyFilter();
    }}

    function clearSearch() {{
      const input = document.getElementById('paper-search');
      input.value = '';
      document.getElementById('search-clear').style.display = 'none';
      const kbd = document.querySelector('.search-kbd');
      if (kbd) kbd.style.display = 'block';
      handleSearch();
      input.focus();
    }}

    function resetAllFilters() {{
      const input = document.getElementById('paper-search');
      input.value = '';
      document.getElementById('search-clear').style.display = 'none';
      const kbd = document.querySelector('.search-kbd');
      if (kbd) kbd.style.display = 'block';
      currentSearch = '';
      const allBtn = document.querySelector('.filter-btn[data-filter="all"]');
      setFilter('all', allBtn);
    }}

    function handleSearch() {{
      const input = document.getElementById('paper-search');
      currentSearch = input.value.toLowerCase().trim();
      const clearBtn = document.getElementById('search-clear');
      const kbd = document.querySelector('.search-kbd');
      if (input.value.length > 0) {{
        if (clearBtn) clearBtn.style.display = 'block';
        if (kbd) kbd.style.display = 'none';
      }} else {{
        if (clearBtn) clearBtn.style.display = 'none';
        if (kbd) kbd.style.display = 'block';
      }}
      applyFilter();
    }}

    function applyFilter() {{
      const cards = document.querySelectorAll('.pub-card');
      let visibleCount = 0;

      cards.forEach(card => {{
        const category = card.getAttribute('data-category');
        const isHighlight = card.getAttribute('data-highlight') === 'true';
        const cardText = card.textContent.toLowerCase();

        let matchesCat = false;
        if (currentFilter === 'all') {{
          matchesCat = true;
        }} else if (currentFilter === 'highlight') {{
          matchesCat = isHighlight;
        }} else {{
          matchesCat = (category === currentFilter);
        }}

        let matchesSearch = true;
        if (currentSearch.length > 0) {{
          matchesSearch = cardText.includes(currentSearch);
        }}

        if (matchesCat && matchesSearch) {{
          card.style.display = 'flex';
          card.style.opacity = '1';
          visibleCount++;
        }} else {{
          card.style.display = 'none';
          card.style.opacity = '0';
        }}
      }});

      const noRes = document.getElementById('no-results');
      if (visibleCount === 0) {{
        noRes.style.display = 'block';
      }} else {{
        noRes.style.display = 'none';
      }}
    }}

    function copyBibtex(btn) {{
      const bib = btn.getAttribute('data-bib');
      if (!bib) return;

      const originalHtml = btn.innerHTML;
      navigator.clipboard.writeText(bib).then(() => {{
        btn.innerHTML = '<svg class="bib-icon" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg> <span>Copied!</span>';
        btn.classList.add('copied');

        const toast = document.getElementById('toast');
        if (toast) {{
          toast.classList.add('show');
          setTimeout(() => {{
            toast.classList.remove('show');
          }}, 2200);
        }}
        setTimeout(() => {{
          btn.innerHTML = originalHtml;
          btn.classList.remove('copied');
        }}, 1800);
      }}).catch(err => {{
        console.error('Clipboard copy failed:', err);
      }});
    }}

    // Global keyboard shortcut: press / or Cmd+K / Ctrl+K to jump to search
    document.addEventListener('keydown', (e) => {{
      const searchInput = document.getElementById('paper-search');
      if (e.key === '/' && document.activeElement !== searchInput) {{
        e.preventDefault();
        searchInput.focus();
        searchInput.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
      }} else if ((e.metaKey || e.ctrlKey) && e.key === 'k') {{
        e.preventDefault();
        searchInput.focus();
        searchInput.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
      }} else if (e.key === 'Escape' && document.activeElement === searchInput) {{
        clearSearch();
        searchInput.blur();
      }}
    }});
  </script>
</body>
</html>
"""

with open("/Users/jiankai/Library/CloudStorage/Dropbox/Codes/homepage/index.html", "w", encoding="utf-8") as f:
    f.write(full_html)

print("Regenerated index.html with overall activity heatmap & official website links.")
