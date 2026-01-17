import openpyxl
import pandas as pd
from statistics import mean, median
from datetime import datetime, timedelta

def process_excel_file(filepath):
    """
    Extract data from Excel file and organize by date for next 7 days
    """
    try:
        # Read Excel file with header in row 0
        df = pd.read_excel(filepath, header=0)
        
        # Skip the first row (which contains the header labels)
        df = df.iloc[1:].reset_index(drop=True)
        
        data = {
            'daily_data': [],
            'competitor_pricing': [],
            'metrics': {}
        }
        
        if len(df) > 0:
            # Process daily data (next 7 days)
            daily_data = extract_daily_data(df)
            data['daily_data'] = daily_data
            
            # Extract competitor pricing
            competitor_data = extract_competitor_pricing(df)
            data['competitor_pricing'] = competitor_data
            
            # Calculate overall metrics
            metrics = calculate_metrics(df)
            data['metrics'] = metrics
        
        return data
    except Exception as e:
        raise Exception(f"Error processing Excel file: {str(e)}")

def extract_daily_data(df):
    """
    Extract daily data for 7 days
    """
    daily_data = []
    
    # Find the columns we need
    date_col = 'Unnamed: 1'  # Date is in column 1
    adr_col = 'ADR'  # Column 43
    revenue_col = None  # Revenue might not be directly present
    pickup_col = 'Transient'  # Pickups could be Transient column at index 23
    
    # Verify columns exist
    if date_col not in df.columns:
        date_col = None
    if adr_col not in df.columns:
        adr_col = None
    if pickup_col not in df.columns:
        pickup_col = None
    
    # Extract up to 7 rows (7 days of data)
    for i in range(min(7, len(df))):
        row = df.iloc[i]
        
        # Get date
        date_str = 'Day ' + str(i+1)
        if date_col and pd.notna(row[date_col]):
            try:
                date_val = row[date_col]
                date_str = str(date_val).strip()
            except:
                pass
        
        row_data = {
            'date': date_str,
            'pickups': 0,
            'adr': 0,
            'revenue': 0
        }
        
        # Extract pickups from "Transient" column
        if pickup_col and pd.notna(row[pickup_col]):
            try:
                val = row[pickup_col]
                if isinstance(val, str):
                    val = float(val.replace(',', '').replace('-', '0'))
                row_data['pickups'] = int(float(val))
            except:
                pass
        
        # Extract ADR
        if adr_col and pd.notna(row[adr_col]):
            try:
                val = row[adr_col]
                if isinstance(val, str):
                    val = float(val.replace(',', '').replace('-', '0'))
                row_data['adr'] = float(val)
            except:
                pass
        
        # For revenue, we'll try to calculate from ADR and occupancy
        # or use "Revenue (1000s)" if available
        try:
            # Try Occupancy * ADR approach - look for occupancy in "On the Books"
            if 'On the Books' in df.columns:
                occ_val = row['On the Books']
                if pd.notna(occ_val):
                    try:
                        if isinstance(occ_val, str):
                            occ = float(occ_val.replace(',', '').replace('-', '0')) / 100
                        else:
                            occ = float(occ_val) / 100
                        # Assume ~100 rooms
                        row_data['revenue'] = row_data['adr'] * occ * 100
                    except:
                        pass
        except:
            pass
        
        daily_data.append(row_data)
    
    return daily_data

def extract_competitor_pricing(df):
    """
    Extract competitor hotel pricing for NEXT 7 DAYS
    Returns a list of dicts with daily competitor data
    """
    competitor_data = []
    
    # Competitor rates are in columns 68-75 (Unnamed: 68 through Unnamed: 75)
    competitor_columns = [f'Unnamed: {i}' for i in range(68, 76)]
    
    hotel_names = [
        'Candlewood Suites',
        'Comfort Suites',
        'Fairfield Inn',
        'Hampton Int',
        'Hilton Garden',
        'Holiday Inn',
        'Hyatt Place',
        'Residence Inn'
    ]
    
    # Get competitor rates for all 7 days
    for day_idx in range(min(7, len(df))):
        row = df.iloc[day_idx]
        
        # Get date for this day
        date_col = 'Unnamed: 1'
        date_str = f'Day {day_idx + 1}'
        if date_col in df.columns and pd.notna(row[date_col]):
            try:
                date_str = str(row[date_col]).strip()
            except:
                pass
        
        day_competitors = []
        
        for idx, col in enumerate(competitor_columns):
            if col in df.columns:
                try:
                    rate_val = row[col]
                    if pd.notna(rate_val):
                        try:
                            if isinstance(rate_val, str):
                                rate = float(rate_val.replace(',', '').replace('-', '0'))
                            else:
                                rate = float(rate_val)
                            hotel_name = hotel_names[idx] if idx < len(hotel_names) else f'Hotel {idx+1}'
                            day_competitors.append({
                                'hotel': hotel_name,
                                'rate': round(rate, 2)
                            })
                        except:
                            pass
                except:
                    pass
        
        if day_competitors:
            competitor_data.append({
                'date': date_str,
                'competitors': day_competitors
            })
    
    # Return default if no data found
    if not competitor_data:
        return [
            {
                'date': f'Day {i+1}',
                'competitors': [
                    {'hotel': 'Competitor A', 'rate': 120 + i*2},
                    {'hotel': 'Competitor B', 'rate': 135 + i*2},
                    {'hotel': 'Competitor C', 'rate': 110 + i*2},
                ]
            } for i in range(7)
        ]
    
    return competitor_data

def calculate_metrics(df):
    """
    Calculate average ADR, revenue, occupancy, and pickups from the first 7 days only
    """
    metrics = {
        'average_adr': 0,
        'average_revenue': 0,
        'average_pickups': 0,
        'average_occupancy': 0
    }
    
    # Use only first 7 rows (7-day forecast)
    df_7days = df.iloc[:7]
    
    # Calculate average ADR
    if 'ADR' in df.columns:
        try:
            numeric_vals = pd.to_numeric(df_7days['ADR'], errors='coerce').dropna()
            if len(numeric_vals) > 0:
                metrics['average_adr'] = round(numeric_vals.mean(), 2)
        except:
            pass
    
    # Calculate average occupancy
    if 'On the Books' in df.columns:
        try:
            occ_vals = pd.to_numeric(df_7days['On the Books'], errors='coerce').dropna()
            if len(occ_vals) > 0:
                metrics['average_occupancy'] = round(occ_vals.mean(), 2)
        except:
            pass
    
    # Calculate average revenue from occupancy and ADR
    # Revenue = Occupancy% * ADR * Rooms (assuming 100 rooms)
    if 'On the Books' in df.columns and 'ADR' in df.columns:
        try:
            occ_vals = pd.to_numeric(df_7days['On the Books'], errors='coerce').dropna()
            adr_vals = pd.to_numeric(df_7days['ADR'], errors='coerce').dropna()
            if len(occ_vals) > 0 and len(adr_vals) > 0:
                avg_occ = occ_vals.mean() / 100  # Convert percentage to decimal
                avg_adr = adr_vals.mean()
                rooms = 100  # Assumed room count
                metrics['average_revenue'] = round(avg_occ * avg_adr * rooms, 2)
        except:
            pass
    
    # Calculate average pickups from Transient column
    if 'Transient' in df.columns:
        try:
            numeric_vals = pd.to_numeric(df_7days['Transient'], errors='coerce').dropna()
            if len(numeric_vals) > 0:
                metrics['average_pickups'] = round(numeric_vals.mean(), 2)
        except:
            pass
    
    return metrics
