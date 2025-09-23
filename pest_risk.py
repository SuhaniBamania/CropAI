import requests
import random
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

@dataclass
class WeatherData:
    """Weather data structure"""
    temperature: float  # Celsius
    humidity: float     # Percentage
    rainfall: float     # mm
    timestamp: datetime

@dataclass
class PestRiskAssessment:
    """Pest risk assessment result"""
    risk_level: str          # 'Low', 'Medium', 'High'
    risk_color: str          # 'green', 'yellow', 'red'
    risk_emoji: str          # Visual indicator
    confidence: float        # 0-1
    primary_threats: List[str]
    recommendations: List[str]
    weather_summary: str
    detailed_analysis: Dict[str, str]

class PestRiskEngine:
    """
    Advanced pest risk assessment engine based on weather conditions
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        
        # Pest-specific thresholds based on agricultural research
        self.risk_thresholds = {
            'aphids': {
                'temp_optimal': (15, 25),
                'humidity_min': 50,
                'rainfall_max': 10
            },
            'fungal_diseases': {
                'temp_optimal': (20, 30),
                'humidity_min': 70,
                'rainfall_min': 5
            },
            'spider_mites': {
                'temp_optimal': (27, 35),
                'humidity_max': 40,
                'rainfall_max': 2
            },
            'thrips': {
                'temp_optimal': (20, 30),
                'humidity_optimal': (40, 70),
                'rainfall_max': 8
            },
            'whiteflies': {
                'temp_optimal': (25, 32),
                'humidity_min': 60,
                'rainfall_max': 12
            }
        }
    
    def get_weather_data(self, location: str = "Delhi") -> WeatherData:
        """
        Fetch real weather data or return mock data for demo
        """
        if self.api_key:
            try:
                params = {
                    'q': location,
                    'appid': self.api_key,
                    'units': 'metric'
                }
                response = requests.get(self.base_url, params=params, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    return WeatherData(
                        temperature=data['main']['temp'],
                        humidity=data['main']['humidity'],
                        rainfall=data.get('rain', {}).get('1h', 0),
                        timestamp=datetime.now()
                    )
            except Exception as e:
                print(f"Weather API error: {e}")
        
        # Return mock data for demo/testing
        return self._generate_mock_weather()
    
    def _generate_mock_weather(self) -> WeatherData:
        """Generate realistic mock weather data"""
        # Create different scenarios for demo
        scenarios = [
            # Low risk scenario
            WeatherData(22.0, 55.0, 2.0, datetime.now()),
            # Medium risk scenario  
            WeatherData(28.0, 68.0, 8.0, datetime.now()),
            # High risk scenario
            WeatherData(34.0, 82.0, 18.0, datetime.now()),
            # Variable scenarios
            WeatherData(26.0, 45.0, 0.0, datetime.now()),  # Hot & dry
            WeatherData(18.0, 85.0, 15.0, datetime.now()),  # Cool & wet
        ]
        
        # Rotate through scenarios or pick random
        return random.choice(scenarios)
    
    def assess_pest_risk(self, weather_data: WeatherData) -> PestRiskAssessment:
        """
        Main assessment function - analyzes weather data and returns risk assessment
        """
        temp = weather_data.temperature
        humidity = weather_data.humidity
        rainfall = weather_data.rainfall
        
        # Calculate individual pest risks
        pest_risks = self._calculate_individual_pest_risks(weather_data)
        
        # Determine overall risk level
        overall_risk = self._determine_overall_risk(pest_risks, weather_data)
        
        # Generate specific recommendations
        recommendations = self._generate_recommendations(pest_risks, weather_data)
        
        # Identify primary threats
        primary_threats = self._identify_primary_threats(pest_risks)
        
        return PestRiskAssessment(
            risk_level=overall_risk['level'],
            risk_color=overall_risk['color'],
            risk_emoji=overall_risk['emoji'],
            confidence=overall_risk['confidence'],
            primary_threats=primary_threats,
            recommendations=recommendations,
            weather_summary=self._generate_weather_summary(weather_data),
            detailed_analysis=self._generate_detailed_analysis(pest_risks, weather_data)
        )
    
    def _calculate_individual_pest_risks(self, weather_data: WeatherData) -> Dict[str, float]:
        """Calculate risk score for each pest type (0-1 scale)"""
        risks = {}
        temp = weather_data.temperature
        humidity = weather_data.humidity
        rainfall = weather_data.rainfall
        
        # Aphids - thrive in moderate temps, high humidity, low rainfall
        aphid_risk = 0
        if 15 <= temp <= 25:
            aphid_risk += 0.4
        if humidity > 50:
            aphid_risk += 0.3
        if rainfall < 10:
            aphid_risk += 0.3
        risks['aphids'] = min(aphid_risk, 1.0)
        
        # Fungal diseases - love warmth, high humidity, moisture
        fungal_risk = 0
        if 20 <= temp <= 30:
            fungal_risk += 0.3
        if humidity > 70:
            fungal_risk += 0.4
        if rainfall > 5:
            fungal_risk += 0.3
        risks['fungal_diseases'] = min(fungal_risk, 1.0)
        
        # Spider mites - hot, dry conditions
        mite_risk = 0
        if temp > 27:
            mite_risk += 0.4
        if humidity < 40:
            mite_risk += 0.3
        if rainfall < 2:
            mite_risk += 0.3
        risks['spider_mites'] = min(mite_risk, 1.0)
        
        # Thrips - moderate conditions
        thrip_risk = 0
        if 20 <= temp <= 30:
            thrip_risk += 0.3
        if 40 <= humidity <= 70:
            thrip_risk += 0.3
        if rainfall < 8:
            thrip_risk += 0.4
        risks['thrips'] = min(thrip_risk, 1.0)
        
        # Whiteflies - warm, humid conditions
        whitefly_risk = 0
        if 25 <= temp <= 32:
            whitefly_risk += 0.4
        if humidity > 60:
            whitefly_risk += 0.3
        if rainfall < 12:
            whitefly_risk += 0.3
        risks['whiteflies'] = min(whitefly_risk, 1.0)
        
        return risks
    
    def _determine_overall_risk(self, pest_risks: Dict[str, float], weather_data: WeatherData) -> Dict[str, any]:
        """Determine overall risk level based on individual pest risks"""
        max_risk = max(pest_risks.values())
        avg_risk = sum(pest_risks.values()) / len(pest_risks)
        
        # Consider extreme weather conditions
        temp_extreme = weather_data.temperature > 35 or weather_data.temperature < 5
        humidity_extreme = weather_data.humidity > 90 or weather_data.humidity < 20
        rainfall_extreme = weather_data.rainfall > 25
        
        if temp_extreme or humidity_extreme or rainfall_extreme:
            max_risk = min(max_risk + 0.2, 1.0)
        
        # Determine risk level
        if max_risk >= 0.7:
            return {
                'level': 'High',
                'color': 'red',
                'emoji': '🔴',
                'confidence': min(max_risk, 0.95)
            }
        elif max_risk >= 0.4:
            return {
                'level': 'Medium', 
                'color': 'yellow',
                'emoji': '🟡',
                'confidence': max_risk * 0.8
            }
        else:
            return {
                'level': 'Low',
                'color': 'green', 
                'emoji': '🟢',
                'confidence': 1 - max_risk
            }
    
    def _identify_primary_threats(self, pest_risks: Dict[str, float]) -> List[str]:
        """Identify the most significant pest threats"""
        # Sort pests by risk level
        sorted_pests = sorted(pest_risks.items(), key=lambda x: x[1], reverse=True)
        
        # Get pests with significant risk (>0.3)
        significant_threats = [pest for pest, risk in sorted_pests if risk > 0.3]
        
        # Map to user-friendly names
        threat_names = {
            'aphids': 'Aphid Infestation',
            'fungal_diseases': 'Fungal Diseases',
            'spider_mites': 'Spider Mite Damage',
            'thrips': 'Thrips Damage',
            'whiteflies': 'Whitefly Infestation'
        }
        
        return [threat_names.get(threat, threat.title()) for threat in significant_threats[:3]]
    
    def _generate_recommendations(self, pest_risks: Dict[str, float], weather_data: WeatherData) -> List[str]:
        """Generate specific recommendations based on risks and weather"""
        recommendations = []
        
        # High-risk pest specific recommendations
        for pest, risk in pest_risks.items():
            if risk > 0.6:
                if pest == 'aphids':
                    recommendations.extend([
                        "🐛 Scout for aphid colonies on new growth",
                        "🌿 Apply insecticidal soap or neem oil spray",
                        "🐞 Release beneficial insects like ladybugs"
                    ])
                elif pest == 'fungal_diseases':
                    recommendations.extend([
                        "💨 Improve air circulation between plants",
                        "🌿 Apply preventive fungicide spray",
                        "💧 Avoid overhead watering - use drip irrigation"
                    ])
                elif pest == 'spider_mites':
                    recommendations.extend([
                        "💦 Increase humidity around plants with misting",
                        "🔍 Check undersides of leaves for fine webbing",
                        "🌿 Apply miticide or predatory mite release"
                    ])
                elif pest == 'thrips':
                    recommendations.extend([
                        "💙 Use blue sticky traps to monitor populations",
                        "🌿 Apply beneficial nematodes to soil",
                        "💨 Remove weeds that harbor thrips"
                    ])
                elif pest == 'whiteflies':
                    recommendations.extend([
                        "💛 Install yellow sticky traps",
                        "🌿 Apply horticultural oil spray",
                        "🧹 Remove lower leaves touching soil"
                    ])
        
        # Weather-specific recommendations
        if weather_data.humidity > 80:
            recommendations.append("💨 Critical: Increase ventilation to reduce humidity")
        if weather_data.temperature > 32:
            recommendations.append("☀️ Provide shade cloth during peak heat hours")
        if weather_data.rainfall > 15:
            recommendations.append("🌧️ Improve drainage and avoid additional watering")
        
        # Remove duplicates and limit to top 6
        return list(dict.fromkeys(recommendations))[:6]
    
    def _generate_weather_summary(self, weather_data: WeatherData) -> str:
        """Generate human-readable weather summary"""
        temp_desc = "hot" if weather_data.temperature > 30 else "warm" if weather_data.temperature > 20 else "cool"
        humidity_desc = "very humid" if weather_data.humidity > 80 else "humid" if weather_data.humidity > 60 else "dry"
        
        if weather_data.rainfall > 10:
            rain_desc = "with significant rainfall"
        elif weather_data.rainfall > 2:
            rain_desc = "with light rainfall"
        else:
            rain_desc = "with no rainfall"
        
        return f"Current conditions: {temp_desc} ({weather_data.temperature:.1f}°C), {humidity_desc} ({weather_data.humidity:.0f}%), {rain_desc} ({weather_data.rainfall:.1f}mm)"
    
    def _generate_detailed_analysis(self, pest_risks: Dict[str, float], weather_data: WeatherData) -> Dict[str, str]:
        """Generate detailed analysis for each factor"""
        analysis = {}
        
        # Temperature analysis
        temp = weather_data.temperature
        if temp > 32:
            analysis['temperature'] = f"High temperature ({temp:.1f}°C) favors spider mites and heat stress"
        elif temp < 15:
            analysis['temperature'] = f"Cool temperature ({temp:.1f}°C) slows pest development but may stress plants"
        else:
            analysis['temperature'] = f"Moderate temperature ({temp:.1f}°C) suitable for most pest activity"
        
        # Humidity analysis
        humidity = weather_data.humidity
        if humidity > 75:
            analysis['humidity'] = f"High humidity ({humidity:.0f}%) creates ideal conditions for fungal diseases"
        elif humidity < 40:
            analysis['humidity'] = f"Low humidity ({humidity:.0f}%) favors spider mites and thrips"
        else:
            analysis['humidity'] = f"Moderate humidity ({humidity:.0f}%) - balanced conditions"
        
        # Rainfall analysis
        rainfall = weather_data.rainfall
        if rainfall > 15:
            analysis['rainfall'] = f"Heavy rainfall ({rainfall:.1f}mm) increases fungal disease pressure"
        elif rainfall < 2:
            analysis['rainfall'] = f"Dry conditions ({rainfall:.1f}mm) favor drought-stress pests"
        else:
            analysis['rainfall'] = f"Moderate moisture ({rainfall:.1f}mm) - good for plant health"
        
        return analysis

def get_pest_risk_assessment(location: str = "Delhi", api_key: str = None, disease: str = None) -> PestRiskAssessment:
    engine = PestRiskEngine(api_key=api_key)
    weather_data = engine.get_weather_data(location)
    assessment = engine.assess_pest_risk(weather_data)

    # Unknown case: different color, emoji, and message
    if disease and disease.lower() == "unknown":
        assessment.risk_level = "Unknown"
        assessment.risk_color = "black"
        assessment.risk_emoji = "⚫"
        assessment.confidence = 0.0
        assessment.primary_threats = ["Not detected (image unknown)"]
        assessment.recommendations = [
            "❓ Unable to provide pest risk due to unclear image.",
            "📸 Retake a clearer photo under good lighting.",
            "🌱 Monitor your plant and try again.",
            "🔎 If symptoms persist, consult a plant expert."
        ]
        assessment.weather_summary = "No valid assessment (image unrecognized)"
        assessment.detailed_analysis = {}

    return assessment