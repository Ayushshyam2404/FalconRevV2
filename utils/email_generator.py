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
    competitor_section = create_competitor_section(competitor_pricing, our_adr)
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

def create_competitor_section(competitor_pricing, our_adr=0):
    """Create competitor pricing display with rate comparison to our rate"""
    if not competitor_pricing:
        return ""
    
    cards = ""
    for competitor in competitor_pricing:
        comp_rate = competitor.get('rate', 0)
        # Calculate difference: positive if competitor is more expensive than us, negative if cheaper
        rate_diff = comp_rate - our_adr
        
        # Format the difference with +/- sign
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

def get_timestamp():
    """Get current timestamp"""
    from datetime import datetime
    return datetime.now().strftime("Generated on %B %d, %Y at %I:%M %p")
