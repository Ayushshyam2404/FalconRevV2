def generate_email_html(data, logo_base64="", subject_line=""):
    """
    Generate clean card-based HTML email with orange/dark theme
    Logo should be base64 encoded data URI (data:image/png;base64,...)
    """
    daily_data = data.get('daily_data', [])
    competitor_pricing = data.get('competitor_pricing', [])
    metrics = data.get('metrics', {})
    our_adr = data.get('our_adr', 0)  # Our hotel's ADR for comparison
    
    metrics_html = create_metrics_cards(metrics)
    daily_section = create_daily_section(daily_data)
    competitor_section = create_competitor_section(competitor_pricing, daily_data)
    rate_comparison = create_rate_comparison_chart(daily_data, competitor_pricing)
    logo_html = f'<img src="{logo_base64}" alt="Logo" style="max-width: 80px; height: auto; margin-bottom: 16px;">' if logo_base64 else ""
    timestamp = get_timestamp()
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif;
                background: #0a0a0a;
                color: #fff;
                line-height: 1.6;
            }}
            
            .wrapper {{
                max-width: 680px;
                margin: 0 auto;
                padding: 20px;
            }}
            
            .container {{
                background: #1a1a1a;
                border-radius: 18px;
                overflow: hidden;
                box-shadow: 0 2px 10px rgba(0,0,0,0.3);
            }}
            
            .header {{
                background: linear-gradient(135deg, #ff9500 0%, #ff6b35 100%);
                padding: 48px 32px;
                text-align: center;
            }}
            
            .logo {{
                margin-bottom: 20px;
            }}
            
            .header h1 {{
                font-size: 32px;
                font-weight: 600;
                color: #fff;
                margin-bottom: 8px;
                letter-spacing: -0.5px;
            }}
            
            .header p {{
                font-size: 15px;
                color: rgba(255,255,255,0.9);
                font-weight: 400;
            }}
            
            .content {{
                padding: 32px;
            }}
            
            .section {{
                margin-bottom: 32px;
            }}
            
            .section-title {{
                font-size: 16px;
                font-weight: 600;
                color: #ff9500;
                margin-bottom: 20px;
                letter-spacing: -0.3px;
                text-transform: uppercase;
            }}
            
            .metrics-grid {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 16px;
                margin-bottom: 0;
            }}
            
            .metric-card {{
                background: #262626;
                padding: 24px;
                border-radius: 12px;
                text-align: center;
                border: 1px solid #333;
            }}
            
            .metric-value {{
                font-size: 28px;
                font-weight: 700;
                color: #ff9500;
                margin-bottom: 8px;
            }}
            
            .metric-label {{
                font-size: 12px;
                color: #a1a1a1;
                font-weight: 500;
                letter-spacing: 0.3px;
                text-transform: uppercase;
            }}
            
            .daily-table {{
                width: 100%;
                border-collapse: collapse;
                font-size: 14px;
            }}
            
            .daily-table thead {{
                border-bottom: 2px solid #333;
            }}
            
            .daily-table th {{
                padding: 14px 12px;
                text-align: right;
                font-size: 13px;
                font-weight: 600;
                color: #a1a1a1;
                letter-spacing: 0.3px;
                background: #0f0f0f;
            }}
            
            .daily-table th:first-child {{
                text-align: left;
            }}
            
            .daily-table td {{
                padding: 14px 12px;
                text-align: right;
                border-bottom: 1px solid #262626;
                color: #e0e0e0;
            }}
            
            .daily-table td:first-child {{
                text-align: left;
                font-weight: 500;
                color: #fff;
            }}
            
            .daily-table tr:last-child td {{
                border-bottom: none;
            }}
            
            .table-scroll {{
                overflow-x: auto;
                margin: 0 -32px;
                padding: 0 32px;
                -webkit-overflow-scrolling: touch;
            }}
            
            .table-scroll table {{
                min-width: 100%;
            }}
            
            .chart-container {{
                margin-top: 24px;
            }}
            
            .chart-row {{
                display: flex;
                align-items: flex-end;
                margin-bottom: 32px;
                gap: 16px;
            }}
            
            .chart-label {{
                font-size: 13px;
                font-weight: 500;
                color: #a1a1a1;
                min-width: 80px;
                text-align: right;
            }}
            
            .chart-bar-wrapper {{
                display: flex;
                gap: 20px;
                align-items: flex-end;
                flex: 1;
                border-bottom: 2px solid #333;
                padding-bottom: 8px;
            }}
            
            .bar-group {{
                display: flex;
                flex-direction: column;
                align-items: center;
            }}
            
            .bar-value {{
                font-size: 13px;
                font-weight: 700;
                color: #fff;
                margin-bottom: 8px;
            }}
            
            .chart-bar {{
                width: 28px;
                border-radius: 3px 3px 0 0;
                display: block;
                min-height: 2px;
            }}
            
            .bar-our {{
                background: #ff9500;
            }}
            
            .bar-avg {{
                background: #4a9eff;
            }}
            
            .chart-legend {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 16px;
                margin-top: 20px;
                font-size: 12px;
            }}
            
            .legend-item {{
                display: flex;
                align-items: center;
                gap: 8px;
            }}
            
            .legend-color {{
                width: 16px;
                height: 16px;
                border-radius: 2px;
            }}
            
            .pickup-change {{
                font-weight: 600;
                padding: 4px 8px;
                border-radius: 6px;
                display: inline-block;
                min-width: 60px;
                text-align: center;
            }}
            
            .pickup-positive {{
                background: #1b7540;
                color: #52dd7a;
            }}
            
            .pickup-negative {{
                background: #7a2a2a;
                color: #ff6b5b;
            }}
            
            .pickup-neutral {{
                background: #333;
                color: #a1a1a1;
            }}
            
            .competitor-grid {{
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 12px;
            }}
            
            .competitor-card {{
                background: #262626;
                padding: 16px;
                border-radius: 12px;
                text-align: center;
                border: 1px solid #333;
            }}
            
            .competitor-name {{
                font-size: 12px;
                color: #a1a1a1;
                margin-bottom: 10px;
                font-weight: 500;
                min-height: 30px;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            
            .competitor-rate {{
                font-size: 24px;
                font-weight: 700;
                color: #ff9500;
            }}
            
            .rate-diff {{
                font-size: 13px;
                font-weight: 600;
                margin-top: 8px;
                padding: 6px 8px;
                border-radius: 6px;
            }}
            
            .rate-diff.positive {{
                background: #1b7540;
                color: #52dd7a;
            }}
            
            .rate-diff.negative {{
                background: #7a2a2a;
                color: #ff6b5b;
            }}
            
            .rate-diff.neutral {{
                background: #333;
                color: #a1a1a1;
            }}
            
            .footer {{
                background: #0f0f0f;
                padding: 24px 32px;
                text-align: center;
                border-top: 1px solid #333;
            }}
            
            .footer-text {{
                font-size: 12px;
                color: #666;
                line-height: 1.6;
            }}
            
            .footer-brand {{
                color: #ff9500;
                font-weight: 600;
            }}
            
            @media (max-width: 600px) {{
                .metrics-grid {{
                    grid-template-columns: 1fr;
                }}
                
                .competitor-grid {{
                    grid-template-columns: repeat(2, 1fr);
                }}
                
                .header h1 {{
                    font-size: 24px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="wrapper">
            <div class="container">
                <div class="header">
                    <div class="logo">
                        {logo_html}
                    </div>
                    <h1>Falcon Rev</h1>
                    <p>7-Day Forecast & Analysis</p>
                </div>
                
                <div class="content">
                    {metrics_html}
                    {daily_section}
                    {competitor_section}
                    {rate_comparison}
                </div>
                
                <div class="footer">
                    <div class="footer-text">
                        <p>Generated automatically by <span class="footer-brand">Falcon Rev</span></p>
                        <p>Powered by <span class="footer-brand">Orange Falcon</span> (formerly Orange Technolab LLC)</p>
                        <p style="margin-top: 12px; color: #555;">{timestamp}</p>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

def create_metrics_cards(metrics):
    """Create simple metric cards with values"""
    adr = metrics.get('average_adr', 0)
    revenue = metrics.get('average_revenue', 0)
    occupancy = metrics.get('average_occupancy', 0)
    
    return f"""
    <div class="section">
        <div class="section-title">Key Metrics</div>
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-value">${adr:.0f}</div>
                <div class="metric-label">Average ADR</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">${revenue:,.0f}</div>
                <div class="metric-label">Avg Revenue</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{occupancy:.1f}%</div>
                <div class="metric-label">Avg Occupancy</div>
            </div>
        </div>
    </div>
    """

def create_daily_section(daily_data):
    """Create 7-day forecast table with pickup changes and color coding"""
    if not daily_data:
        return ""
    
    table_rows = ""
    prev_pickups = None
    
    for day in daily_data:
        pickups = day['pickups']
        
        if prev_pickups is not None:
            change = pickups - prev_pickups
            if change > 0:
                pickup_display = f'<span class="pickup-change pickup-positive">+{change:.0f}</span>'
            elif change < 0:
                pickup_display = f'<span class="pickup-change pickup-negative">{change:.0f}</span>'
            else:
                pickup_display = f'<span class="pickup-change pickup-neutral">→</span>'
        else:
            pickup_display = f'<span class="pickup-change pickup-neutral">Start</span>'
        
        table_rows += f"""
        <tr>
            <td>{day['date']}</td>
            <td>{pickup_display}</td>
            <td>${day['adr']:,.0f}</td>
            <td>${day['revenue']:,.0f}</td>
        </tr>
        """
        
        prev_pickups = pickups
    
    return f"""
    <div class="section">
        <div class="section-title">7-Day Forecast</div>
        <table class="daily-table">
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Pickups</th>
                    <th>ADR</th>
                    <th>Revenue</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
    </div>
    """

def create_competitor_section(competitor_pricing, daily_data=None):
    """Create competitor pricing display for 7 days in table format with hotel names as columns"""
    if not competitor_pricing:
        return ""
    
    if daily_data is None:
        daily_data = []
    
    # Check if this is the new format (list of dicts with date and competitors)
    is_new_format = (
        isinstance(competitor_pricing, list) and 
        len(competitor_pricing) > 0 and 
        isinstance(competitor_pricing[0], dict) and 
        'competitors' in competitor_pricing[0]
    )
    
    if not is_new_format:
        # Handle old format for backward compatibility - single day display
        our_adr = daily_data[0].get('adr', 0) if daily_data else 0
        cards = ""
        for competitor in competitor_pricing:
            comp_rate = competitor.get('rate', 0)
            rate_diff = comp_rate - our_adr
            
            if rate_diff > 0:
                diff_display = f'<div class="rate-diff positive">+${rate_diff:.0f}</div>'
            elif rate_diff < 0:
                diff_display = f'<div class="rate-diff negative">${rate_diff:.0f}</div>'
            else:
                diff_display = f'<div class="rate-diff neutral">Same</div>'
            
            cards += f"""
            <div class="competitor-card">
                <div class="competitor-name">{competitor.get('hotel', 'Hotel')}</div>
                <div class="competitor-rate">${comp_rate:.0f}</div>
                {diff_display}
            </div>
            """
        
        return f"""
        <div class="section">
            <div class="section-title">Competitor Pricing</div>
            <div class="competitor-grid">
                {cards}
            </div>
        </div>
        """
    
    # Handle new format: 7 days of competitor data in wide table format
    # First, collect all unique competitor hotels across all days
    all_hotels = []
    for day_data in competitor_pricing:
        competitors = day_data.get('competitors', [])
        for comp in competitors:
            hotel_name = comp.get('hotel', '')
            if hotel_name and hotel_name not in all_hotels:
                all_hotels.append(hotel_name)
    
    # Build table header with actual hotel names
    header_html = "<tr><th>Date</th><th style='background: #ff9500; color: #fff;'>Our Hotel</th>"
    for hotel in all_hotels:
        # Truncate long hotel names for better display
        display_name = hotel.replace(' ', '<br>')
        header_html += f"<th>{display_name}</th>"
    header_html += "</tr>"
    
    # Build table rows
    table_rows = ""
    
    for idx, day_data in enumerate(competitor_pricing):
        date_str = day_data.get('date', 'Day')
        competitors = day_data.get('competitors', [])
        
        # Get the correct ADR for this day from daily_data
        day_adr = 0
        if daily_data and idx < len(daily_data):
            day_adr = daily_data[idx].get('adr', 0)
        
        # Create a map of hotel name -> rate for this day
        comp_rates = {}
        for comp in competitors:
            hotel_name = comp.get('hotel', '')
            rate = comp.get('rate', 0)
            comp_rates[hotel_name] = rate
        
        # Build row
        row_html = f"<tr><td>{date_str}</td><td style='background: #f5f5f5; font-weight: 600; color: #1a1a1a;'>${day_adr:.0f}</td>"
        
        for hotel in all_hotels:
            rate = comp_rates.get(hotel, 0)
            if rate > 0:
                row_html += f"<td>${rate:.0f}</td>"
            else:
                row_html += f"<td>-</td>"
        
        row_html += "</tr>"
        table_rows += row_html
    
    return f"""
    <div class="section">
        <div class="section-title">Competitor Pricing - 7 Day Forecast</div>
        <div class="table-scroll">
            <table class="daily-table" style="font-size: 13px;">
                <thead>
                    {header_html}
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        </div>
    </div>
    """

def get_timestamp():
    """Get current timestamp"""
    from datetime import datetime
    return datetime.now().strftime("Generated on %B %d, %Y at %I:%M %p")
def create_rate_comparison_chart(daily_data, competitor_pricing):
    """Create a simple bar chart comparing our hotel rates vs all individual competitor rates"""
    if not daily_data or not competitor_pricing:
        return ""
    
    chart_rows = ""
    max_rate = 0
    
    # Calculate max rate for scaling
    for idx, day_data in enumerate(competitor_pricing):
        our_rate = 0
        if daily_data and idx < len(daily_data):
            our_rate = daily_data[idx].get('adr', 0)
        
        competitors = day_data.get('competitors', [])
        if competitors:
            max_rate = max(max_rate, our_rate)
            for comp in competitors:
                max_rate = max(max_rate, comp.get('rate', 0))
    
    if max_rate == 0:
        max_rate = 150  # Default scale
    
    # Color palette for competitors
    competitor_colors = [
        '#4a9eff',  # Blue
        '#52dd7a',  # Green
        '#ff6b5b',  # Red
        '#ffd93d',  # Yellow
        '#a78bfa',  # Purple
        '#06b6d4',  # Cyan
        '#f472b6',  # Pink
        '#ec4899',  # Rose
    ]
    
    # Build chart rows
    for idx, day_data in enumerate(competitor_pricing):
        date_str = day_data.get('date', 'Day')
        our_rate = 0
        if daily_data and idx < len(daily_data):
            our_rate = daily_data[idx].get('adr', 0)
        
        competitors = day_data.get('competitors', [])
        
        bars_html = f"""
                <div class="bar-group">
                    <div class="bar-value">${our_rate:.0f}</div>
                    <div class="chart-bar bar-our" style="height: {(our_rate / max_rate) * 150 if max_rate > 0 else 0}px;"></div>
                </div>
        """
        
        # Add bars for all competitors with different colors
        for comp_idx, comp in enumerate(competitors):
            comp_rate = comp.get('rate', 0)
            color = competitor_colors[comp_idx % len(competitor_colors)]
            bars_html += f"""
                <div class="bar-group">
                    <div class="bar-value">${comp_rate:.0f}</div>
                    <div class="chart-bar" style="background: {color}; height: {(comp_rate / max_rate) * 150 if max_rate > 0 else 0}px;"></div>
                </div>
            """
        
        chart_rows += f"""
        <div class="chart-row">
            <div class="chart-label">{date_str}</div>
            <div class="chart-bar-wrapper">
                {bars_html}
            </div>
        </div>
        """
    
    # Build legend with all competitors
    legend_html = f"""
                <div class="legend-item">
                    <div class="legend-color" style="background: #ff9500;"></div>
                    <span>Our Hotel</span>
                </div>
    """
    
    # Add competitors to legend - collect unique hotel names
    unique_hotels = {}
    if competitor_pricing:
        for day_data in competitor_pricing:
            for comp_idx, comp in enumerate(day_data.get('competitors', [])):
                hotel_name = comp.get('hotel', f'Competitor {comp_idx + 1}')
                if comp_idx not in unique_hotels:
                    unique_hotels[comp_idx] = hotel_name
    
    # Build legend with actual hotel names
    for comp_idx in sorted(unique_hotels.keys()):
        color = competitor_colors[comp_idx % len(competitor_colors)]
        hotel_name = unique_hotels[comp_idx]
        legend_html += f"""
                <div class="legend-item">
                    <div class="legend-color" style="background: {color};"></div>
                    <span>{hotel_name}</span>
                </div>
            """
    
    return f"""
    <div class="section">
        <div class="section-title">Rate Comparison - Our Hotel vs Competitors</div>
        <div class="chart-container">
            {chart_rows}
            <div class="chart-legend">
                {legend_html}
            </div>
        </div>
    </div>
    """