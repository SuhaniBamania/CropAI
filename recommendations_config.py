import random
from datetime import datetime, date

class RecommendationEngine:
    """
    Advanced recommendation engine that provides contextual advice based on:
    - Disease type and severity
    - Environmental conditions
    - Seasonal factors
    - Regional considerations
    """
    
    def __init__(self):
        self.base_recommendations = self._load_base_recommendations()
        self.environmental_factors = self._load_environmental_factors()
        self.seasonal_advice = self._load_seasonal_advice()
        self.regional_adjustments = self._load_regional_adjustments()
    
    def _load_base_recommendations(self):
        """Base disease-specific recommendations"""
        return {
            'Blight': {
                'disease': 'Leaf Blight',
                'severity': 'High',
                'urgency_level': 'Critical',
                'treatment_duration': '2-3 weeks',
                'success_rate': '85%',
                'immediate_actions': [
                    '🚨 Remove and destroy affected leaves immediately',
                    '💧 Reduce watering frequency - avoid overhead watering',
                    '🌿 Apply copper-based fungicide spray every 7-10 days',
                    '🍃 Improve air circulation around plants',
                    '🧤 Wear gloves and disinfect tools between plants'
                ],
                'preventive_measures': [
                    '🌱 Plant resistant varieties in future seasons',
                    '💨 Ensure proper plant spacing (3-4 feet apart)',
                    '🚰 Install drip irrigation system',
                    '🧹 Clean garden tools with 70% alcohol',
                    '🍂 Apply organic mulch to prevent soil splash'
                ],
                'monitoring': [
                    '👁️ Check plants daily for new brown/black spots',
                    '📊 Monitor humidity levels (keep below 85%)',
                    '🌡️ Optimal temperature range: 20-25°C',
                    '🌧️ Watch weather forecasts for rain periods',
                    '📱 Take photos to track progression'
                ],
                'fertilizer_advice': 'Temporarily reduce nitrogen (promotes soft growth). Apply balanced NPK (10-10-10) after disease control. Add calcium to strengthen cell walls.',
                'organic_solutions': [
                    '🥛 Spray diluted milk solution (1:10 ratio) weekly',
                    '🧄 Neem oil application every 5-7 days at sunset',
                    '🍃 Baking soda spray (1 tsp per liter water)',
                    '☕ Compost tea foliar spray twice weekly',
                    '🌿 Plant marigolds nearby as companion plants'
                ],
                'chemical_alternatives': [
                    'Copper sulfate solution (1%)',
                    'Chlorothalonil fungicide',
                    'Mancozeb spray (follow label rates)'
                ],
                'cost_estimate': '$15-25 for organic treatment, $30-50 for chemical'
            },
            
            'Healthy': {
                'disease': 'No Disease Detected',
                'severity': 'None',
                'urgency_level': 'Routine',
                'treatment_duration': 'Ongoing maintenance',
                'success_rate': '95%',
                'immediate_actions': [
                    '✅ Continue current excellent care routine',
                    '💧 Maintain consistent watering schedule',
                    '🌿 Monitor for any changes in leaf appearance',
                    '🌱 Consider light pruning for better air circulation'
                ],
                'preventive_measures': [
                    '🔄 Plan crop rotation for next season',
                    '🌱 Apply organic compost monthly (2-3 inches)',
                    '🛡️ Maintain preventive neem oil spray schedule',
                    '🌾 Ensure proper plant nutrition with soil testing',
                    '🐛 Encourage beneficial insects with diverse plantings'
                ],
                'monitoring': [
                    '📅 Weekly comprehensive plant health inspections',
                    '🌧️ Monitor weather for stress conditions',
                    '🐛 Check for early signs of pest activity',
                    '🌡️ Track soil and air temperature variations',
                    '💧 Monitor soil moisture levels'
                ],
                'fertilizer_advice': 'Continue balanced fertilization (NPK 20-20-20) bi-weekly during growing season. Add organic matter monthly.',
                'organic_solutions': [
                    '🍂 Maintain 2-3 inch organic mulch layer',
                    '🦋 Plant pollinator-friendly flowers nearby',
                    '☀️ Ensure 6-8 hours direct sunlight daily',
                    '💧 Deep water 2-3 times weekly rather than daily light watering',
                    '🌿 Apply liquid kelp fertilizer monthly'
                ],
                'enhancement_tips': [
                    'Install drip irrigation for efficiency',
                    'Add beneficial mycorrhizal fungi to soil',
                    'Create windbreaks for protection'
                ]
            },
            
            'Mosaic': {
                'disease': 'Mosaic Virus',
                'severity': 'High',
                'urgency_level': 'Critical',
                'treatment_duration': 'No cure - prevention focused',
                'success_rate': '20% (management only)',
                'immediate_actions': [
                    '🚨 Isolate affected plants immediately',
                    '🔥 Remove and burn infected plants (NEVER compost)',
                    '🧤 Disinfect all tools with 10% bleach solution',
                    '🚫 Avoid touching healthy plants after infected ones',
                    '🏃‍♂️ Act quickly - virus spreads rapidly'
                ],
                'preventive_measures': [
                    '🐛 Aggressive aphid and thrips control program',
                    '🌱 Use only certified virus-free seeds/transplants',
                    '🧹 Maintain strict garden sanitation',
                    '🚰 Avoid overhead watering completely',
                    '🥽 Wear disposable gloves when handling plants'
                ],
                'monitoring': [
                    '🔍 Daily inspection for mosaic leaf patterns',
                    '🐜 Monitor aphid populations with yellow sticky traps',
                    '📈 Track spread to neighboring plants',
                    '🌡️ Monitor temperature (viruses spread faster in heat)',
                    '📊 Keep detailed records of affected areas'
                ],
                'fertilizer_advice': 'Boost remaining plant immunity with phosphorus-rich fertilizer (0-20-20). Avoid high nitrogen which attracts aphids.',
                'organic_solutions': [
                    '🌿 Spray insecticidal soap weekly for vector control',
                    '🧄 Apply neem oil to deter virus-carrying insects',
                    '🍃 Use reflective aluminum mulch to confuse aphids',
                    '🌸 Plant trap crops like nasturtiums to lure aphids away',
                    '💨 Install fans to disrupt insect flight patterns'
                ],
                'vector_control': [
                    'Release ladybugs for aphid control',
                    'Use beneficial nematodes for soil pests',
                    'Install fine mesh barriers'
                ],
                'replacement_strategy': 'Plant resistant varieties immediately after removal'
            },
            
            'Rust': {
                'disease': 'Leaf Rust',
                'severity': 'Medium',
                'urgency_level': 'Moderate',
                'treatment_duration': '3-4 weeks',
                'success_rate': '90%',
                'immediate_actions': [
                    '🍃 Remove rust-infected leaves and bag for trash',
                    '💨 Improve air circulation with pruning/spacing',
                    '🌿 Apply sulfur-based fungicide immediately',
                    '💧 Switch to drip irrigation or soaker hoses',
                    '🧹 Clean up all fallen leaves weekly'
                ],
                'preventive_measures': [
                    '🌱 Research and plant rust-resistant varieties',
                    '📏 Maintain 4-6 feet between plants for airflow',
                    '🌤️ Water early morning, never in evening',
                    '🧹 Weekly garden cleanup of debris',
                    '🌿 Apply preventive sulfur dust monthly'
                ],
                'monitoring': [
                    '👀 Check leaf undersides for orange/brown pustules',
                    '🌡️ Monitor temperature (rust thrives 20-25°C)',
                    '💧 Track humidity levels with hygrometer',
                    '🌪️ Watch for poor air circulation areas',
                    '📸 Photo document progression weekly'
                ],
                'fertilizer_advice': 'Apply potassium-rich fertilizer (0-0-50) to strengthen plant cell walls. Reduce nitrogen temporarily to slow soft growth.',
                'organic_solutions': [
                    '🧄 Bi-weekly neem oil applications at sunset',
                    '☕ Weekly compost tea spray to boost immunity',
                    '🌿 Plant garlic and chives nearby as natural fungicides',
                    '🥛 Milk spray (1:9 ratio) twice weekly',
                    '🌸 Chamomile tea spray for mild antifungal effect'
                ],
                'environmental_management': [
                    'Increase garden ventilation with fans',
                    'Reduce overhead watering to zero',
                    'Prune lower branches for air flow'
                ]
            },
            
            'Unknown': {
                'disease': 'Unidentified Condition',
                'severity': 'Unknown',
                'urgency_level': 'Precautionary',
                'treatment_duration': 'Pending diagnosis',
                'success_rate': 'Depends on actual condition',
                'immediate_actions': [
                    '📸 Take detailed photos from multiple angles',
                    '🔍 Contact local agricultural extension office',
                    '🌿 Isolate plant until proper identification',
                    '📝 Document all symptoms and environmental conditions',
                    '🌡️ Record temperature and humidity data'
                ],
                'preventive_measures': [
                    '🌱 Continue general plant health best practices',
                    '💧 Maintain proper watering schedule',
                    '🌿 Apply gentle organic treatments as precaution',
                    '🧹 Increase sanitation measures',
                    '👥 Consult with experienced local gardeners'
                ],
                'monitoring': [
                    '📊 Track symptom progression daily with photos',
                    '🌡️ Monitor environmental conditions closely',
                    '📞 Stay in contact with agricultural experts',
                    '📚 Research similar symptoms online',
                    '🕐 Set reminders for regular check-ups'
                ],
                'fertilizer_advice': 'Continue balanced nutrition (10-10-10) until diagnosis. Avoid experimental treatments.',
                'organic_solutions': [
                    '🧄 Very mild neem oil application as precaution',
                    '🍃 Light compost tea spray for general plant health',
                    '🌱 Ensure optimal growing conditions',
                    '💧 Maintain consistent moisture levels',
                    '🌿 Provide adequate but not excessive nutrients'
                ],
                'diagnostic_resources': [
                    'Local university extension services',
                    'Master gardener programs',
                    'Online plant diagnostic tools',
                    'Professional plant pathologists'
                ]
            }
        }
    
    def _load_environmental_factors(self):
        """Environmental condition adjustments"""
        return {
            'high_humidity': {
                'warning': '⚠️ High humidity (>85%) detected - Increased fungal disease risk',
                'risk_level': 'High',
                'actions': [
                    '💨 Increase air circulation with fans or pruning',
                    '🌿 Apply preventive fungicide spray immediately',
                    '💧 Reduce watering frequency by 25%',
                    '🍃 Remove lower leaves touching soil',
                    '🌡️ Monitor temperature to prevent condensation'
                ]
            },
            'low_humidity': {
                'warning': '🌵 Low humidity (<40%) - Plants may experience stress',
                'risk_level': 'Medium',
                'actions': [
                    '💧 Increase watering frequency slightly',
                    '🌊 Apply 3-4 inch mulch layer for moisture retention',
                    '💦 Group plants together for microclimate',
                    '🌿 Consider morning misting (avoid leaves)',
                    '🏠 Create windbreaks to reduce moisture loss'
                ]
            },
            'temperature_stress': {
                'hot': '🌡️ High temperatures (>30°C) can stress plants',
                'cold': '❄️ Low temperatures (<10°C) slow growth and healing',
                'actions': [
                    '☀️ Provide afternoon shade during heat waves',
                    '💧 Increase watering during hot periods',
                    '🛡️ Use row covers for cold protection',
                    '🌿 Avoid fertilizing during temperature extremes'
                ]
            }
        }
    
    def _load_seasonal_advice(self):
        """Season-specific recommendations"""
        return {
            'spring': {
                'focus': 'Prevention and establishment',
                'key_activities': [
                    'Start regular fertilization program',
                    'Begin weekly pest monitoring',
                    'Plant resistant varieties',
                    'Prepare irrigation systems',
                    'Apply pre-emergent treatments'
                ]
            },
            'summer': {
                'focus': 'Disease management and plant support',
                'key_activities': [
                    'Increase watering frequency',
                    'Provide shade during extreme heat',
                    'Monitor for heat stress signs',
                    'Maintain consistent fungicide schedule',
                    'Harvest regularly to reduce plant stress'
                ]
            },
            'autumn': {
                'focus': 'Harvest and preparation',
                'key_activities': [
                    'Reduce fertilization gradually',
                    'Harvest mature crops promptly',
                    'Clean up garden debris',
                    'Plan crop rotation for next year',
                    'Apply dormant season treatments'
                ]
            },
            'winter': {
                'focus': 'Planning and preparation',
                'key_activities': [
                    'Plan next season variety selection',
                    'Order resistant seeds early',
                    'Study disease patterns from past season',
                    'Prepare soil amendments',
                    'Research new treatment methods'
                ]
            }
        }
    
    def _load_regional_adjustments(self):
        """Regional climate and pest adjustments"""
        return {
            'tropical': {
                'climate_challenges': ['High humidity', 'Rapid disease spread', 'Year-round pests'],
                'adaptations': [
                    'Increase fungicide frequency',
                    'Focus on drainage improvement',
                    'Select heat-resistant varieties'
                ]
            },
            'temperate': {
                'climate_challenges': ['Seasonal variations', 'Spring/fall disease pressure'],
                'adaptations': [
                    'Time treatments with weather patterns',
                    'Prepare for season transitions',
                    'Focus on soil health'
                ]
            },
            'arid': {
                'climate_challenges': ['Water stress', 'Extreme temperatures', 'Wind damage'],
                'adaptations': [
                    'Emphasize water conservation',
                    'Provide wind protection',
                    'Select drought-resistant varieties'
                ]
            }
        }
    
    def get_current_season(self):
        """Determine current season based on date"""
        month = datetime.now().month
        if month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        elif month in [9, 10, 11]:
            return 'autumn'
        else:
            return 'winter'
    
    def generate_comprehensive_recommendation(self, disease, confidence_score=None, 
                                           environmental_conditions=None, region='temperate'):
        """
        Generate comprehensive, contextual recommendations
        """
        base_rec = self.base_recommendations.get(disease, self.base_recommendations['Unknown']).copy()
        
        # Add seasonal context
        current_season = self.get_current_season()
        seasonal_info = self.seasonal_advice[current_season]
        base_rec['seasonal_focus'] = seasonal_info['focus']
        base_rec['seasonal_activities'] = seasonal_info['key_activities']
        
        # Add confidence adjustments
        if confidence_score and confidence_score < 0.6:
            base_rec['confidence_warning'] = f'⚠️ Detection confidence: {confidence_score:.1%}. Consider multiple opinions.'
            base_rec['recommended_action'] = 'Take additional photos and consult local experts for confirmation.'
        
        # Add environmental adjustments
        if environmental_conditions:
            for condition, value in environmental_conditions.items():
                if condition in self.environmental_factors:
                    env_advice = self.environmental_factors[condition]
                    base_rec[f'{condition}_advice'] = env_advice
        
        # Add regional adjustments
        if region in self.regional_adjustments:
            regional_info = self.regional_adjustments[region]
            base_rec['regional_considerations'] = regional_info
        
        # Add cost-effectiveness tips
        base_rec['budget_tips'] = self._generate_budget_tips(disease)
        
        # Add follow-up schedule
        base_rec['follow_up_schedule'] = self._generate_follow_up_schedule(disease)
        
        return base_rec
    
    def _generate_budget_tips(self, disease):
        """Generate cost-effective treatment suggestions"""
        budget_tips = {
            'Blight': [
                'Make your own copper fungicide with copper sulfate',
                'Use milk spray before expensive fungicides',
                'Focus on prevention to avoid repeated treatments'
            ],
            'Healthy': [
                'Compost kitchen scraps for free fertilizer',
                'Collect rainwater for irrigation',
                'Save seeds from healthy plants'
            ],
            'Mosaic': [
                'Remove infected plants early to prevent spread costs',
                'Use companion planting instead of expensive treatments',
                'Invest in quality seeds to prevent reinfection'
            ],
            'Rust': [
                'Sulfur powder is more economical than liquid sprays',
                'Improve airflow with pruning rather than fans',
                'Use baking soda spray as budget fungicide'
            ],
            'Unknown': [
                'Consult free extension services before paid consultants',
                'Use general organic treatments while diagnosing',
                'Document with photos to avoid repeat consultations'
            ]
        }
        return budget_tips.get(disease, budget_tips['Unknown'])
    
    def _generate_follow_up_schedule(self, disease):
        """Generate follow-up monitoring schedule"""
        schedules = {
            'Blight': {
                'daily': 'Check for new spots',
                'weekly': 'Apply treatments, photograph progress',
                'bi_weekly': 'Evaluate treatment effectiveness',
                'monthly': 'Review and adjust strategy'
            },
            'Healthy': {
                'weekly': 'General health inspection',
                'monthly': 'Apply preventive treatments',
                'seasonally': 'Soil testing and crop planning'
            },
            'Mosaic': {
                'daily': 'Monitor for spread',
                'weekly': 'Vector control measures',
                'monthly': 'Evaluate garden-wide prevention'
            },
            'Rust': {
                'daily': 'Check weather conditions',
                'weekly': 'Apply treatments, remove affected leaves',
                'bi_weekly': 'Assess treatment progress'
            },
            'Unknown': {
                'daily': 'Photo documentation',
                'weekly': 'Symptom assessment',
                'as_needed': 'Expert consultation'
            }
        }
        return schedules.get(disease, schedules['Unknown'])

# Utility functions for easy integration
def get_recommendation(disease, confidence=None, environmental_data=None, region='temperate'):
    """Simple function to get recommendations - use this in your Flask app"""
    engine = RecommendationEngine()
    return engine.generate_comprehensive_recommendation(disease, confidence, environmental_data, region)

def get_quick_tip(disease):
    """Get a quick, one-line tip for the disease"""
    quick_tips = {
        'Blight': 'Act fast! Remove infected leaves and spray copper fungicide immediately.',
        'Healthy': 'Great job! Continue your current care routine and stay vigilant.',
        'Mosaic': 'Critical: Isolate and remove infected plants to prevent spread.',
        'Rust': 'Improve airflow and apply sulfur spray - treatable with quick action.',
        'Unknown': 'Take detailed photos and consult your local extension office.'
    }
    return quick_tips.get(disease, quick_tips['Unknown'])