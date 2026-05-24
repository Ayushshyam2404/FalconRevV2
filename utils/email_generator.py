# ── Theme Palettes ────────────────────────────────────────────────────────────
DARK = {
    'bg_page':       '#080808',
    'bg_wrap':       '#141414',
    'bg_card':       '#1c1c1c',
    'bg_th':         '#0d0d0d',
    'bg_alt':        '#161616',
    'bg_footer':     '#0d0d0d',
    'bg_occ':        '#1e1e1e',
    'bg_key':        '#111111',
    'bg_our':        '#110900',
    'border_main':   '#222222',
    'border_card':   '#242424',
    'border_sect':   '#1e1e1e',
    'border_our':    '#2a1a00',
    'border_th':     '#1e1e1e',
    'border_td':     '#1a1a1a',
    'shadow':        'rgba(0,0,0,0.6)',
    'txt_pri':       '#e8e8e8',
    'txt_sec':       '#cccccc',
    'txt_muted':     '#555555',
    'txt_faint':     '#333333',
    'txt_th':        '#555555',
    'txt_date':      '#ffffff',
    'txt_comp_date': '#666666',
    'txt_footer':    '#333333',
    'txt_our':       '#ff9500',
    'st_color':      '#ff9500',
    'tu_bg':  '#0d2e1a', 'tu_txt':  '#4ade80',
    'tdw_bg': '#2e0d0d', 'tdw_txt': '#f87171',
    'tf_bg':  '#1e1e1e', 'tf_txt':  '#555555',
    'bu_bg':  '#0d2e1a', 'bu_txt':  '#4ade80',
    'bdw_bg': '#2e0d0d', 'bdw_txt': '#f87171',
    'bf_bg':  '#1e1e1e', 'bf_txt':  '#555555',
    'rp':  '#4ade80',
    'rc':  '#f87171',
    'rs':  '#666666',
    'rna': '#333333',
    'mv':  '#ffffff',
    'ml':  '#555555',
    'fb':  '#ff9500',
    'sub': 'rgba(255,255,255,0.85)',
    'chart_avg_top': '#4a9eff', 'chart_avg_bot': '#2563eb',
    'leg_txt': '#888888',
    'pos_pricier': '#4ade80', 'pos_cheaper': '#f87171',
}

LIGHT = {
    'bg_page':       '#f0f2f5',
    'bg_wrap':       '#ffffff',
    'bg_card':       '#ffffff',
    'bg_th':         '#f5f5f5',
    'bg_alt':        '#fafafa',
    'bg_footer':     '#f8f8f8',
    'bg_occ':        '#e0e0e0',
    'bg_key':        '#f5f5f5',
    'bg_our':        '#fff7ed',
    'border_main':   '#e0e0e0',
    'border_card':   '#e8e8e8',
    'border_sect':   '#e8e8e8',
    'border_our':    '#fbbf24',
    'border_th':     '#e8e8e8',
    'border_td':     '#eeeeee',
    'shadow':        'rgba(0,0,0,0.1)',
    'txt_pri':       '#111111',
    'txt_sec':       '#444444',
    'txt_muted':     '#777777',
    'txt_faint':     '#aaaaaa',
    'txt_th':        '#777777',
    'txt_date':      '#111111',
    'txt_comp_date': '#888888',
    'txt_footer':    '#aaaaaa',
    'txt_our':       '#ea580c',
    'st_color':      '#ea580c',
    'tu_bg':  '#dcfce7', 'tu_txt':  '#15803d',
    'tdw_bg': '#fee2e2', 'tdw_txt': '#b91c1c',
    'tf_bg':  '#f3f4f6', 'tf_txt':  '#6b7280',
    'bu_bg':  '#dcfce7', 'bu_txt':  '#15803d',
    'bdw_bg': '#fee2e2', 'bdw_txt': '#b91c1c',
    'bf_bg':  '#f3f4f6', 'bf_txt':  '#6b7280',
    'rp':  '#15803d',
    'rc':  '#b91c1c',
    'rs':  '#777777',
    'rna': '#cccccc',
    'mv':  '#111111',
    'ml':  '#777777',
    'fb':  '#ea580c',
    'sub': 'rgba(0,0,0,0.7)',
    'chart_avg_top': '#3b82f6', 'chart_avg_bot': '#1d4ed8',
    'leg_txt': '#555555',
    'pos_pricier': '#15803d', 'pos_cheaper': '#b91c1c',
}


def generate_email_html(data, logo_base64="", subject_line="", theme="dark"):
    """
    Generate rich card-based HTML email.
    theme: 'dark' (default) or 'light'
    Logo should be a base64 data URI (data:image/png;base64,...)
    """
    t = LIGHT if theme == "light" else DARK

    daily_data         = data.get('daily_data', [])
    competitor_pricing = data.get('competitor_pricing', [])
    metrics            = data.get('metrics', {})

    metrics_html      = create_metrics_cards(metrics, daily_data, theme=theme)
    daily_section     = create_daily_section(daily_data, theme=theme)
    competitor_section = create_competitor_section(competitor_pricing, daily_data, theme=theme)
    rate_comparison   = create_rate_comparison_chart(daily_data, competitor_pricing, theme=theme)

    logo_html = (
        f'<img src="{logo_base64}" alt="Logo" style="max-width:80px;height:auto;margin-bottom:16px;">'
        if logo_base64 else ""
    )
    timestamp = get_timestamp()

    date_range = ""
    if daily_data:
        first = daily_data[0].get('date', '')
        last  = daily_data[-1].get('date', '') if len(daily_data) > 1 else first
        if first and last and first != last:
            date_range = f" &nbsp;&middot;&nbsp; {first} &ndash; {last}"

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
  background: {t['bg_page']};
  color: {t['txt_pri']};
  font-size: 18px;
  line-height: 1.6;
}}
.wrapper {{ max-width:1350px; margin:0 auto; padding:32px; }}
.container {{
  background: {t['bg_wrap']};
  border-radius: 20px;
  overflow: hidden;
  border: 1px solid {t['border_main']};
  box-shadow: 0 6px 36px {t['shadow']};
}}
.header {{
  background: linear-gradient(135deg, #ff9500 0%, #e8600a 100%);
  padding: 64px 56px 56px;
  text-align: center;
}}
.header h1 {{
  font-size: 62px;
  font-weight: 700;
  color: #fff;
  letter-spacing: -1.5px;
  margin-bottom: 12px;
  text-shadow: 0 2px 10px rgba(0,0,0,0.18);
}}
.subtitle {{
  font-size: 18px;
  color: {t['sub']};
  font-weight: 400;
}}
.content {{ padding: 50px 56px; }}
.section {{ margin-bottom: 52px; }}
.section-title {{
  font-size: 13px;
  font-weight: 700;
  color: {t['st_color']};
  letter-spacing: 2.5px;
  text-transform: uppercase;
  margin-bottom: 24px;
  padding-bottom: 14px;
  border-bottom: 1px solid {t['border_sect']};
}}
/* ── Metrics ── */
.metrics-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
}}
.metric-card {{
  background: {t['bg_card']};
  border: 1px solid {t['border_card']};
  border-radius: 16px;
  padding: 32px 24px 28px;
  text-align: center;
  position: relative;
  overflow: hidden;
}}
.metric-card::before {{
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 4px;
  background: linear-gradient(90deg, #ff9500, #ff6b35);
}}
.metric-value {{
  font-size: 48px;
  font-weight: 700;
  color: {t['mv']};
  letter-spacing: -0.5px;
  line-height: 1;
  margin-bottom: 12px;
}}
.metric-label {{
  font-size: 13px;
  color: {t['ml']};
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  margin-bottom: 14px;
}}
.metric-trend {{
  font-size: 14px;
  font-weight: 700;
  padding: 5px 14px;
  border-radius: 20px;
  display: inline-block;
}}
.trend-up   {{ background: {t['tu_bg']};  color: {t['tu_txt']};  }}
.trend-down {{ background: {t['tdw_bg']}; color: {t['tdw_txt']}; }}
.trend-flat {{ background: {t['tf_bg']};  color: {t['tf_txt']};  }}
/* ── Forecast table ── */
.daily-table {{ width:100%; border-collapse:collapse; }}
.daily-table thead tr {{ background: {t['bg_th']}; }}
.daily-table th {{
  padding: 18px 22px;
  font-size: 13px;
  font-weight: 700;
  color: {t['txt_th']};
  letter-spacing: 1.5px;
  text-transform: uppercase;
  text-align: right;
  border-bottom: 1px solid {t['border_th']};
}}
.daily-table th:first-child {{ text-align:left; padding-left:28px; }}
.daily-table td {{
  padding: 20px 22px;
  text-align: right;
  border-bottom: 1px solid {t['border_td']};
  color: {t['txt_sec']};
  font-size: 17px;
  vertical-align: middle;
}}
.daily-table td:first-child {{
  text-align: left;
  font-weight: 600;
  color: {t['txt_date']};
  padding-left: 28px;
  font-size: 16px;
}}
.daily-table tbody tr:last-child td {{ border-bottom: none; }}
.daily-table tbody tr:nth-child(even) {{ background: {t['bg_alt']}; }}
.pickup-row   {{ display:flex; align-items:center; justify-content:flex-end; gap:9px; }}
.pickup-count {{ font-size:18px; font-weight:700; color:{t['txt_date']}; }}
.pickup-badge {{ font-size:13px; font-weight:700; padding:4px 10px; border-radius:6px; }}
.badge-up   {{ background:{t['bu_bg']};  color:{t['bu_txt']};  }}
.badge-down {{ background:{t['bdw_bg']}; color:{t['bdw_txt']}; }}
.badge-flat {{ background:{t['bf_bg']};  color:{t['bf_txt']};  }}
.occ-cell {{ display:flex; align-items:center; justify-content:flex-end; gap:10px; }}
.occ-bar  {{ width:72px; height:6px; background:{t['bg_occ']}; border-radius:3px; overflow:hidden; flex-shrink:0; }}
.occ-fill {{ height:100%; border-radius:3px; background:linear-gradient(90deg,#ff9500,#ff6b35); }}
/* ── Competitor table ── */
.comp-table {{ width:100%; border-collapse:collapse; font-size:16px; }}
.comp-table th {{
  padding: 16px 16px;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  background: {t['bg_th']};
  color: {t['txt_th']};
  text-align: center;
  border-bottom: 1px solid {t['border_th']};
  white-space: nowrap;
}}
.comp-table th:first-child {{ text-align:left; padding-left:22px; }}
.comp-table th.our-col {{ color:#ff9500; border-bottom:2px solid #ff9500; }}
.comp-table td {{
  padding: 16px 16px;
  text-align: center;
  border-bottom: 1px solid {t['border_td']};
  font-weight: 600;
  font-size: 16px;
  vertical-align: middle;
}}
.comp-table td:first-child {{ text-align:left; padding-left:22px; font-weight:500; font-size:15px; color:{t['txt_comp_date']}; }}
.comp-table tbody tr:last-child td {{ border-bottom:none; }}
.comp-table tbody tr:nth-child(even) {{ background: {t['bg_alt']}; }}
.our-cell {{
  color: #ff9500 !important;
  font-weight: 800;
  font-size: 17px;
  border-left: 1px solid {t['border_our']};
  border-right: 1px solid {t['border_our']};
  background: {t['bg_our']};
}}
.rate-pricier {{ color: {t['rp']}; }}
.rate-cheaper {{ color: {t['rc']}; }}
.rate-similar {{ color: {t['rs']}; }}
.rate-na      {{ color: {t['rna']}; }}
.diff-tag {{ font-size:12px; font-weight:600; opacity:0.75; display:block; margin-top:2px; }}
/* ── Footer ── */
.footer {{
  background: {t['bg_footer']};
  padding: 32px 48px;
  text-align: center;
  border-top: 1px solid {t['border_sect']};
}}
.footer-text  {{ font-size:15px; color:{t['txt_footer']}; line-height:2; }}
.footer-brand {{ color:{t['fb']}; font-weight:600; }}
/* ── Responsive table scroll ── */
.table-scroll {{ overflow-x: auto; -webkit-overflow-scrolling: touch; }}
.daily-table  {{ min-width: 560px; }}
.comp-table   {{ min-width: 600px; }}
/* ── Breakpoints ── */
@media (max-width: 960px) {{
  .wrapper  {{ padding: 20px; }}
  .header   {{ padding: 48px 36px 40px; }}
  .header h1 {{ font-size: 50px; }}
  .content  {{ padding: 36px 28px; }}
}}
@media (max-width: 640px) {{
  .wrapper  {{ padding: 10px; }}
  .header   {{ padding: 36px 18px 30px; }}
  .header h1 {{ font-size: 34px; letter-spacing: -0.5px; }}
  .subtitle  {{ font-size: 15px; }}
  .content   {{ padding: 20px 14px; }}
  .section   {{ margin-bottom: 36px; }}
  .section-title {{ font-size: 11px; letter-spacing: 2px; }}
  .metric-card   {{ padding: 22px 16px 18px; }}
  .metric-value  {{ font-size: 34px; }}
  .metric-label  {{ font-size: 11px; }}
  .metric-trend  {{ font-size: 12px; padding: 4px 10px; }}
  .daily-table th {{ padding: 13px 14px; font-size: 11px; }}
  .daily-table td {{ padding: 13px 14px; font-size: 14px; }}
  .daily-table td:first-child {{ font-size: 13px; padding-left: 16px; }}
  .daily-table th:first-child {{ padding-left: 16px; }}
  .comp-table th {{ padding: 11px 10px; font-size: 11px; }}
  .comp-table td {{ padding: 11px 10px; font-size: 13px; }}
  .comp-table td:first-child {{ padding-left: 14px; font-size: 12px; }}
  .pickup-count  {{ font-size: 15px; }}
  .footer {{ padding: 24px 16px; }}
  .footer-text {{ font-size: 13px; }}
}}
</style>
</head>
<body>
<div class="wrapper"><div class="container">

  <div class="header">
    <div class="logo">{logo_html}</div>
    <h1>Falcon Rev</h1>
    <div class="subtitle">7-Day Revenue Forecast{date_range}</div>
  </div>

  <div class="content">
    {metrics_html}
    {daily_section}
    {competitor_section}
    {rate_comparison}
  </div>

  <div class="footer">
    <div class="footer-text">
      <p>Generated by <span class="footer-brand">Falcon Rev</span> &nbsp;&middot;&nbsp; Powered by <span class="footer-brand">Orange Falcon</span></p>
      <p style="margin-top:5px;color:{t['txt_faint']};">{timestamp}</p>
    </div>
  </div>

</div></div>
</body>
</html>"""
    return html


def _calc_trend(daily_data, field, threshold=0.015):
    """Compare first-half average vs second-half average to detect rising/falling trend."""
    vals = [d.get(field, 0) for d in daily_data if d.get(field, 0) > 0]
    if len(vals) < 4:
        return 'flat'
    mid       = max(2, len(vals) // 2)
    avg_first = sum(vals[:mid]) / mid
    avg_last  = sum(vals[-mid:]) / mid
    if avg_first == 0:
        return 'flat'
    change = (avg_last - avg_first) / avg_first
    if change > threshold:
        return 'up'
    if change < -threshold:
        return 'down'
    return 'flat'


def create_metrics_cards(metrics, daily_data=None, theme="dark"):
    """Four KPI cards: ADR, Revenue, Occupancy, Pickups — with trend arrows."""
    adr       = metrics.get('average_adr', 0)
    revenue   = metrics.get('average_revenue', 0)
    occupancy = metrics.get('average_occupancy', 0)
    pickups   = metrics.get('average_pickups', 0)
    daily_data = daily_data or []

    labels  = {'up': '&#8593; Rising', 'down': '&#8595; Falling', 'flat': '&#8594; Stable'}
    classes = {'up': 'trend-up',       'down': 'trend-down',      'flat': 'trend-flat'}

    adr_t = _calc_trend(daily_data, 'adr')
    rev_t = _calc_trend(daily_data, 'revenue')

    def trend(key):
        return f'<span class="metric-trend {classes[key]}">{labels[key]}</span>'

    return f"""
    <div class="section">
      <div class="section-title">Key Metrics &mdash; 7-Day Average</div>
      <div class="metrics-grid">
        <div class="metric-card">
          <div class="metric-value">${adr:.0f}</div>
          <div class="metric-label">Avg ADR</div>
          {trend(adr_t)}
        </div>
        <div class="metric-card">
          <div class="metric-value">${revenue:,.0f}</div>
          <div class="metric-label">Avg Daily Revenue</div>
          {trend(rev_t)}
        </div>
        <div class="metric-card">
          <div class="metric-value">{occupancy:.1f}%</div>
          <div class="metric-label">Avg Occupancy</div>
          <span class="metric-trend trend-flat">On the Books</span>
        </div>
        <div class="metric-card">
          <div class="metric-value">{pickups:.0f}</div>
          <div class="metric-label">Avg Pickups</div>
          <span class="metric-trend trend-flat">Per Day</span>
        </div>
      </div>
    </div>
    """


def create_daily_section(daily_data, theme="dark"):
    """7-day forecast table with occupancy mini-bar and pickup change badges."""
    if not daily_data:
        return ""

    rows = ""
    prev_pickups = None

    for day in daily_data:
        date    = day.get('date', '&mdash;')
        pickups = day.get('pickups', 0)
        adr     = day.get('adr', 0)
        revenue = day.get('revenue', 0)

        # Back-calculate occupancy: revenue = (occ/100) * adr * 100_rooms
        occ = 0.0
        if adr > 0 and revenue > 0:
            occ = (revenue / (adr * 100)) * 100

        if prev_pickups is not None:
            change = pickups - prev_pickups
            if change > 0:
                badge = f'<span class="pickup-badge badge-up">&#8593;&nbsp;+{change:.0f}</span>'
            elif change < 0:
                badge = f'<span class="pickup-badge badge-down">&#8595;&nbsp;{change:.0f}</span>'
            else:
                badge = '<span class="pickup-badge badge-flat">&#8594;&nbsp;0</span>'
        else:
            badge = ''

        pickup_cell = f'<div class="pickup-row"><span class="pickup-count">{pickups}</span>{badge}</div>'
        adr_str = f'${adr:,.0f}' if adr > 0 else '&mdash;'
        rev_str = f'${revenue:,.0f}' if revenue > 0 else '&mdash;'

        if occ > 0:
            bar_w   = min(100.0, occ)
            occ_str = (
                f'<div class="occ-cell"><span>{occ:.1f}%</span>'
                f'<div class="occ-bar"><div class="occ-fill" style="width:{bar_w:.1f}%"></div></div>'
                f'</div>'
            )
        else:
            occ_str = '&mdash;'

        rows += f"""
        <tr>
          <td>{date}</td>
          <td>{pickup_cell}</td>
          <td>{adr_str}</td>
          <td>{occ_str}</td>
          <td>{rev_str}</td>
        </tr>"""
        prev_pickups = pickups

    return f"""
    <div class="section">
      <div class="section-title">7-Day Forecast</div>
      <div class="table-scroll">
        <table class="daily-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Pickups</th>
              <th>ADR</th>
              <th>Occupancy</th>
              <th>Revenue</th>
            </tr>
          </thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
    </div>
    """


def create_competitor_section(competitor_pricing, daily_data=None, theme="dark"):
    """Competitor pricing table: green = they are pricier (opportunity), red = they are cheaper (threat).
    Hotels that have no rate data on ANY day are excluded from the table."""
    if not competitor_pricing:
        return ""

    t         = LIGHT if theme == "light" else DARK
    daily_data = daily_data or []
    THRESHOLD  = 10.0

    is_new_format = (
        isinstance(competitor_pricing, list)
        and len(competitor_pricing) > 0
        and isinstance(competitor_pricing[0], dict)
        and 'competitors' in competitor_pricing[0]
    )

    if not is_new_format:
        # Legacy single-day card grid
        our_adr = daily_data[0].get('adr', 0) if daily_data else 0
        cards   = ""
        for comp in competitor_pricing:
            rate = comp.get('rate', 0)
            diff = rate - our_adr if our_adr > 0 else 0
            if diff > THRESHOLD:
                diff_style = f"color:{t['rp']};font-size:12px;"
                diff_str   = f'+${diff:.0f}'
            elif diff < -THRESHOLD:
                diff_style = f"color:{t['rc']};font-size:12px;"
                diff_str   = f'-${abs(diff):.0f}'
            else:
                diff_style = f"color:{t['rs']};font-size:12px;"
                diff_str   = '~ same'
            cards += (
                f'<div style="background:{t["bg_card"]};border:1px solid {t["border_card"]};'
                f'border-radius:12px;padding:18px;text-align:center;">'
                f'<div style="font-size:12px;color:{t["txt_muted"]};margin-bottom:8px;font-weight:600;">{comp.get("hotel","Hotel")}</div>'
                f'<div style="font-size:24px;font-weight:700;color:#ff9500;">${rate:.0f}</div>'
                f'<div style="margin-top:5px;{diff_style}">{diff_str}</div>'
                f'</div>'
            )
        return f"""
    <div class="section">
      <div class="section-title">Competitor Pricing</div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;">{cards}</div>
    </div>
        """

    # ── 7-day wide table ──────────────────────────────────────────────────────
    # Only include hotels that have at least one day with rate > 0
    hotels_with_data = set()
    for day_data in competitor_pricing:
        for comp in day_data.get('competitors', []):
            if comp.get('hotel', '') and comp.get('rate', 0) > 0:
                hotels_with_data.add(comp['hotel'])

    # Preserve insertion order
    all_hotels = []
    for day_data in competitor_pricing:
        for comp in day_data.get('competitors', []):
            name = comp.get('hotel', '')
            if name and name not in all_hotels and name in hotels_with_data:
                all_hotels.append(name)

    if not all_hotels:
        return ""

    def abbrev(name):
        words = name.split()
        return ' '.join(w[:4] for w in words[:2]) if len(words) > 1 else name[:8]

    header_cells = "<th>Date</th><th class='our-col'>Our Rate</th>"
    for hotel in all_hotels:
        header_cells += f"<th title='{hotel}'>{abbrev(hotel)}</th>"

    legend_pairs = " &nbsp;|&nbsp; ".join(
        f'<span style="color:{t["txt_muted"]};font-size:12px;">{abbrev(h)}&nbsp;=&nbsp;{h}</span>'
        for h in all_hotels
    )
    legend_html = f'<div style="margin-bottom:16px;line-height:2.2;">{legend_pairs}</div>'

    table_rows = ""
    for idx, day_data in enumerate(competitor_pricing):
        date_str = day_data.get('date', f'Day {idx+1}')
        our_adr  = daily_data[idx].get('adr', 0) if idx < len(daily_data) else 0
        comp_map = {c.get('hotel', ''): c.get('rate', 0) for c in day_data.get('competitors', [])}

        our_cell   = f"<td class='our-cell'>${our_adr:.0f}</td>" if our_adr > 0 else "<td class='our-cell'>&mdash;</td>"
        comp_cells = ""
        for hotel in all_hotels:
            rate = comp_map.get(hotel, 0)
            if rate <= 0:
                comp_cells += "<td class='rate-na'>&mdash;</td>"
                continue
            diff = rate - our_adr if our_adr > 0 else 0
            if our_adr > 0:
                if diff > THRESHOLD:
                    cls      = "rate-pricier"
                    diff_tag = f'<span class="diff-tag">+${diff:.0f}</span>'
                elif diff < -THRESHOLD:
                    cls      = "rate-cheaper"
                    diff_tag = f'<span class="diff-tag">-${abs(diff):.0f}</span>'
                else:
                    cls      = "rate-similar"
                    diff_tag = f'<span class="diff-tag">{diff:+.0f}</span>'
            else:
                cls      = "rate-similar"
                diff_tag = ""
            comp_cells += f"<td class='{cls}'>${rate:.0f}{diff_tag}</td>"

        table_rows += f"<tr><td>{date_str}</td>{our_cell}{comp_cells}</tr>"

    key_html = (
        f'<div style="display:flex;gap:22px;margin-top:16px;font-size:12px;'
        f'padding:14px 18px;background:{t["bg_key"]};border-radius:10px;flex-wrap:wrap;align-items:center;">'
        f'<span style="color:{t["rp"]};font-weight:700;">&#9632; Green</span>'
        f'<span style="color:{t["txt_muted"]};">Competitor more expensive &mdash; pricing opportunity</span>'
        f'<span style="color:{t["rc"]};font-weight:700;margin-left:18px;">&#9632; Red</span>'
        f'<span style="color:{t["txt_muted"]};">Competitor cheaper &mdash; competitive threat</span>'
        f'<span style="color:{t["rs"]};font-weight:700;margin-left:18px;">&#9632; Gray</span>'
        f'<span style="color:{t["txt_muted"]};">Within &plusmn;$10</span>'
        f'</div>'
    )

    return f"""
    <div class="section">
      <div class="section-title">Competitor Pricing &mdash; 7-Day Forecast</div>
      {legend_html}
      <div style="overflow-x:auto;">
        <table class="comp-table">
          <thead><tr>{header_cells}</tr></thead>
          <tbody>{table_rows}</tbody>
        </table>
      </div>
      {key_html}
    </div>
    """


def create_rate_comparison_chart(daily_data, competitor_pricing, theme="dark"):
    """Our rate vs average competitor rate — clean 2-bar chart per day."""
    if not daily_data or not competitor_pricing:
        return ""

    t = LIGHT if theme == "light" else DARK

    BAR_MAX_H = 200
    BAR_W     = 44

    all_rates = []
    for idx, day_data in enumerate(competitor_pricing):
        if idx < len(daily_data):
            r = daily_data[idx].get('adr', 0)
            if r > 0:
                all_rates.append(r)
        all_rates += [c.get('rate', 0) for c in day_data.get('competitors', []) if c.get('rate', 0) > 0]

    if not all_rates:
        return ""

    max_rate = max(all_rates)
    cols     = ""

    for idx, day_data in enumerate(competitor_pricing):
        date_str   = day_data.get('date', f'Day {idx+1}')
        our_rate   = daily_data[idx].get('adr', 0) if idx < len(daily_data) else 0
        comp_rates = [c.get('rate', 0) for c in day_data.get('competitors', []) if c.get('rate', 0) > 0]

        if not comp_rates:
            continue

        avg_comp  = sum(comp_rates) / len(comp_rates)
        cheaper_n = sum(1 for r in comp_rates if r < our_rate - 5)
        pricier_n = sum(1 for r in comp_rates if r > our_rate + 5)

        our_h = int((our_rate / max_rate) * BAR_MAX_H) if max_rate > 0 else 0
        avg_h = int((avg_comp / max_rate) * BAR_MAX_H) if max_rate > 0 else 0

        if cheaper_n == 0 and pricier_n > 0:
            pos_txt   = f'{pricier_n} pricier'
            pos_color = t['pos_pricier']
        elif pricier_n == 0 and cheaper_n > 0:
            pos_txt   = f'{cheaper_n} cheaper'
            pos_color = t['pos_cheaper']
        elif cheaper_n > 0:
            pos_txt   = f'{cheaper_n} cheaper'
            pos_color = t['pos_cheaper']
        else:
            pos_txt   = 'At market'
            pos_color = t['rs']

        cols += (
            f'<div style="display:flex;flex-direction:column;align-items:center;min-width:110px;">'
            f'<div style="display:flex;align-items:flex-end;gap:8px;height:{BAR_MAX_H}px;margin-bottom:12px;">'
            f'<div style="display:flex;flex-direction:column;align-items:center;gap:5px;">'
            f'<span style="font-size:13px;font-weight:700;color:#ff9500;">${our_rate:.0f}</span>'
            f'<div style="width:{BAR_W}px;height:{our_h}px;'
            f'background:linear-gradient(180deg,#ff9500,#ff6b35);'
            f'border-radius:5px 5px 0 0;min-height:5px;"></div>'
            f'</div>'
            f'<div style="display:flex;flex-direction:column;align-items:center;gap:5px;">'
            f'<span style="font-size:13px;font-weight:700;color:{t["chart_avg_top"]};">${avg_comp:.0f}</span>'
            f'<div style="width:{BAR_W}px;height:{avg_h}px;'
            f'background:linear-gradient(180deg,{t["chart_avg_top"]},{t["chart_avg_bot"]});'
            f'border-radius:5px 5px 0 0;min-height:5px;"></div>'
            f'</div>'
            f'</div>'
            f'<div style="font-size:13px;color:{t["leg_txt"]};text-align:center;margin-bottom:6px;">{date_str}</div>'
            f'<div style="font-size:12px;font-weight:700;color:{pos_color};">{pos_txt}</div>'
            f'</div>'
        )

    if not cols:
        return ""

    legend = (
        f'<div style="display:flex;align-items:center;gap:22px;margin-bottom:22px;font-size:13px;color:{t["leg_txt"]};">'
        f'<span><span style="display:inline-block;width:13px;height:13px;background:#ff9500;'
        f'border-radius:3px;vertical-align:middle;margin-right:7px;"></span>Our Rate</span>'
        f'<span><span style="display:inline-block;width:13px;height:13px;background:{t["chart_avg_top"]};'
        f'border-radius:3px;vertical-align:middle;margin-right:7px;"></span>Avg Competitor</span>'
        f'</div>'
    )

    return f"""
    <div class="section">
      <div class="section-title">Rate Comparison &mdash; Our Rate vs Market Average</div>
      {legend}
      <div style="display:flex;gap:14px;align-items:flex-end;overflow-x:auto;padding-bottom:10px;border-bottom:1px solid {t['border_sect']};">
        {cols}
      </div>
    </div>
    """


def get_timestamp():
    """Get current timestamp"""
    from datetime import datetime
    return datetime.now().strftime("Generated on %B %d, %Y at %I:%M %p")


def convert_html_to_image(html_content):
    """
    Convert HTML email to PNG image using Selenium and Chrome
    Returns the image as bytes
    """
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        import tempfile
        import os
        import time

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1280,2600')

        with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w') as tmp_html:
            tmp_html.write(html_content)
            tmp_html_path = tmp_html.name

        file_url = f"file://{tmp_html_path}"
        driver   = webdriver.Chrome(options=chrome_options)

        try:
            driver.get(file_url)
            time.sleep(1)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'wrapper'))
            )
            total_height = driver.execute_script("return document.body.scrollHeight")
            total_width  = driver.execute_script("return document.body.scrollWidth")
            driver.set_window_size(max(900, total_width + 60), total_height + 100)
            time.sleep(0.5)
            screenshot = driver.get_screenshot_as_png()
        finally:
            driver.quit()

        os.unlink(tmp_html_path)
        return screenshot

    except Exception as e:
        print(f"Error converting HTML to image: {str(e)}")
        raise Exception(f"Failed to convert email to image: {str(e)}")
