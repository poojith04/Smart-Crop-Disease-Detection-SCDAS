from geopy.geocoders import Nominatim

class LocationService:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="scdas_rice_app_v1")
    
    def get_location_info(self, latitude, longitude):
        if not latitude or not longitude:
            return {
                'address': 'Location not available',
                'region': 'Unknown',
                'climate_info': 'Enable location services for region-specific rice cultivation advice',
                'crop_advice': 'General rice cultivation practices apply'
            }
        
        try:
            location = self.geolocator.reverse(f"{latitude}, {longitude}")
            address = location.address if location else 'Address not found'
            
            region_info = self.get_regional_rice_advice(latitude, longitude)
            
            return {
                'address': address,
                'latitude': latitude,
                'longitude': longitude,
                'region': region_info['region'],
                'climate_info': region_info['climate'],
                'crop_advice': region_info['advice']
            }
        except Exception as e:
            return {
                'address': 'Error retrieving location',
                'region': 'Unknown',
                'climate_info': 'Unable to fetch location data',
                'crop_advice': 'Consult local agricultural office'
            }
    
    def get_regional_rice_advice(self, latitude, longitude):
        lat = float(latitude)
        lon = float(longitude)
        
        if 8 <= lat <= 13 and 76 <= lon <= 80:
            return {
                'region': 'South India (Tamil Nadu/Kerala)',
                'climate': 'Tropical climate with high rainfall. Suitable for year-round rice cultivation.',
                'advice': 'Grow Samba Mahsuri, ADT-43, CR-1009 varieties. Watch for blast and bacterial blight. Practice SRI (System of Rice Intensification) for water conservation. Two to three crops per year possible.'
            }
        
        elif 15 <= lat <= 19 and 77 <= lon <= 84:
            return {
                'region': 'Andhra Pradesh/Telangana',
                'climate': 'Semi-arid to tropical. Kharif and Rabi seasons suitable for rice.',
                'advice': 'Recommended varieties: MTU-1010, BPT-5204, RNR-15048. Focus on tungro and brown spot management. Use Alternate Wetting Drying (AWD) irrigation method.'
            }
        
        elif 18 <= lat <= 27 and 82 <= lon <= 92:
            return {
                'region': 'Eastern India (West Bengal/Odisha)',
                'climate': 'High rainfall zone, humid subtropical. Major rice bowl of India.',
                'advice': 'Grow Swarna, Lalat, Naveen, Improved Samba Mahsuri. Blast and bacterial blight are major concerns. Ensure good drainage during monsoon. Practice direct seeded rice (DSR) in suitable areas.'
            }
        
        elif 26 <= lat <= 32 and 74 <= lon <= 84:
            return {
                'region': 'North India (Punjab/Haryana/UP)',
                'climate': 'Subtropical with hot summers. Kharif season (June-Nov) ideal for rice.',
                'advice': 'Popular varieties: Pusa-44, PR-126, Pusa Basmati 1509, 1121. Manage bacterial blight and blast. Transplant in June-July. Practice straw management to reduce stubble burning.'
            }
        
        elif 23 <= lat <= 28 and 88 <= lon <= 97:
            return {
                'region': 'North-Eastern India (Assam/Tripura)',
                'climate': 'High rainfall, hilly terrain. Traditional rice cultivation region.',
                'advice': 'Grow Ranjit, Bahadur, Gitesh varieties for lowland. Blast disease is major problem due to high humidity. Practice terrace cultivation in hilly areas. Use organic farming methods.'
            }
        
        elif 20 <= lat <= 25 and 75 <= lon <= 85:
            return {
                'region': 'Central India (Madhya Pradesh/Chhattisgarh)',
                'climate': 'Semi-arid climate with moderate rainfall.',
                'advice': 'Suitable varieties: MTU-1010, Mahamaya, Rajeshwari. Manage brown spot and sheath blight. Grow rice in Kharif season. Practice integrated nutrient management.'
            }
        
        else:
            return {
                'region': 'General Rice Growing Region',
                'climate': 'Variable climate conditions',
                'advice': 'Use locally adapted rice varieties. Monitor for blast, bacterial blight, and tungro. Practice proper water management (5-7cm during critical stages). Consult nearest Krishi Vigyan Kendra (KVK) for specific recommendations.'
            }