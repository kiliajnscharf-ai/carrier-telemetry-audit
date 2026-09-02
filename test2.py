"""
🧠 ADVANCED AI ENGINE PRO - Maximum Intelligence
Deep Learning, Predictive Analytics, Autonomous Optimization
Multi-dimensional Analysis, Real-time Decision Making
"""

import numpy as np
from datetime import datetime, timedelta
import sqlite3
import json
from typing import Dict, List, Tuple, Optional
import math
from enum import Enum

# ==================== AI ALGORITHMS ====================

class SignalQualityPredictor:
    """Machine Learning für Signalqualität-Vorhersage"""
    
    def __init__(self, db_path):
        self.db_path = db_path
        self.model_data = {}
    
    def get_signal_features(self, channel_id: str, hours_back: int = 168) -> np.ndarray:
        """Extrahiert Features aus Signalverlauf"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT snr, ber, signal_strength, packet_loss, timestamp
            FROM signal_history
            WHERE channel_id = ? AND timestamp > datetime('now', '-' || ? || ' hours')
            ORDER BY timestamp
        """, (channel_id, hours_back))
        
        data = cursor.fetchall()
        conn.close()
        
        if len(data) < 5:
            return None
        
        signals = np.array([[d[0] or 0, d[1] or 0, d[2] or 0, d[3] or 0] for d in data])
        
        # Features engineering
        features = {
            'mean_snr': np.mean(signals[:, 0]),
            'std_snr': np.std(signals[:, 0]),
            'trend_snr': np.polyfit(range(len(signals)), signals[:, 0], 1)[0],
            'max_snr': np.max(signals[:, 0]),
            'min_snr': np.min(signals[:, 0]),
            'mean_ber': np.mean(signals[:, 1]),
            'signal_variance': np.var(signals[:, 0]),
            'packet_loss_ratio': np.mean(signals[:, 3]),
            'last_snr': signals[-1, 0],
            'snr_momentum': signals[-1, 0] - signals[max(0, len(signals)-10), 0]
        }
        
        return features
    
    def predict_signal_quality_next_hour(self, channel_id: str) -> Dict:
        """Vorhersage der Signalqualität für nächste Stunde"""
        features = self.get_signal_features(channel_id, hours_back=168)
        
        if features is None:
            return {"confidence": 0, "prediction": "unknown"}
        
        # Weighted prediction based on multiple factors
        trend_weight = 0.3
        variance_weight = 0.2
        momentum_weight = 0.5
        
        trend_score = 1.0 if features['trend_snr'] > 0 else 0.0
        stability_score = 1.0 - min(features['signal_variance'] / 100, 1.0)
        momentum_score = 1.0 if features['snr_momentum'] > 0 else 0.0
        
        overall_score = (
            trend_weight * trend_score +
            variance_weight * stability_score +
            momentum_weight * momentum_score
        )
        
        prediction_quality = {
            "1h_prediction": "improving" if overall_score > 0.6 else "stable" if overall_score > 0.4 else "degrading",
            "confidence": round(min(abs(features['std_snr']) / 10, 1.0), 2),
            "recommended_action": self._recommend_action(features),
            "optimal_modulation": self._predict_modulation(features['mean_snr']),
            "expected_ber": round(features['mean_ber'], 6),
            "stability_index": round(stability_score, 2)
        }
        
        return prediction_quality
    
    def _predict_modulation(self, snr: float) -> str:
        """Wählt beste Modulation basierend auf SNR"""
        if snr < 3:
            return "BPSK"
        elif snr < 6:
            return "QPSK"
        elif snr < 9:
            return "8PSK"
        elif snr < 12:
            return "16APSK"
        else:
            return "32APSK"
    
    def _recommend_action(self, features: Dict) -> str:
        """Empfiehlt Aktionen zur Optimierung"""
        if features['std_snr'] > 2:
            return "Antennenposition prüfen - zu viel Variabilität"
        elif features['mean_ber'] > 0.001:
            return "LNB-Verstärker überprüfen - BER zu hoch"
        elif features['trend_snr'] < -0.1:
            return "Signaldämpfung erkannt - Kabel prüfen"
        else:
            return "Alles optimal - keine Aktion nötig"

class SmartRecommendationEngine:
    """Advanced Recommendation Engine mit Collaborative Filtering"""
    
    def __init__(self, db_path):
        self.db_path = db_path
        self.similarity_matrix = {}
    
    def calculate_channel_similarity(self) -> Dict:
        """Berechnet Ähnlichkeit zwischen Kanälen"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Hole all Channels mit Viewing-Data
        cursor.execute("""
            SELECT DISTINCT channel_id FROM viewing_history
            WHERE timestamp > datetime('now', '-30 days')
        """)
        
        channels = [row[0] for row in cursor.fetchall()]
        
        # Erstelle Viewing-Vektor pro Channel
        channel_vectors = {}
        for ch in channels:
            cursor.execute("""
                SELECT duration_minutes FROM viewing_history
                WHERE channel_id = ? AND timestamp > datetime('now', '-30 days')
                ORDER BY timestamp
            """, (ch,))
            
            durations = [row[0] for row in cursor.fetchall()]
            channel_vectors[ch] = {
                'total_time': sum(durations),
                'avg_session': np.mean(durations) if durations else 0,
                'frequency': len(durations),
                'consistency': np.std(durations) if len(durations) > 1 else 0
            }
        
        conn.close()
        
        # Berechne Ähnlichkeit (Cosine Similarity)
        similarity = {}
        for ch1 in channels:
            for ch2 in channels:
                if ch1 != ch2:
                    v1 = np.array([channel_vectors[ch1]['total_time'], 
                                 channel_vectors[ch1]['frequency']])
                    v2 = np.array([channel_vectors[ch2]['total_time'], 
                                 channel_vectors[ch2]['frequency']])
                    
                    similarity_score = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-10)
                    key = f"{ch1}:{ch2}"
                    similarity[key] = similarity_score
        
        return similarity
    
    def get_ai_recommendations(self, user_preferences: Dict = None) -> List[Dict]:
        """AI-generierte Empfehlungen mit mehreren Dimensionen"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 1. Content-Based Filtering
        cursor.execute("""
            SELECT c.id, c.name, COUNT(v.id) as views, AVG(c.signal_quality) as quality
            FROM viewing_history v
            JOIN channels c ON v.channel_id = c.id
            WHERE v.timestamp > datetime('now', '-7 days')
            GROUP BY c.id
            ORDER BY views DESC
            LIMIT 5
        """)
        
        top_watched = cursor.fetchall()
        
        # 2. Collaborative Filtering
        similarity = self.calculate_channel_similarity()
        
        # 3. Time-based Recommendations
        current_hour = datetime.now().hour
        cursor.execute("""
            SELECT c.id, c.name, COUNT(v.id) as count
            FROM viewing_history v
            JOIN channels c ON v.channel_id = c.id
            WHERE strftime('%H', v.timestamp) = ?
                AND v.timestamp > datetime('now', '-30 days')
            GROUP BY c.id
            ORDER BY count DESC
            LIMIT 3
        """, (f"{current_hour:02d}",))
        
        time_based = cursor.fetchall()
        
        conn.close()
        
        recommendations = []
        
        # Kombiniere alle Signale
        for i, (ch_id, name, views, quality) in enumerate(top_watched):
            base_score = 0.7
            time_bonus = 0.15 if any(t[0] == ch_id for t in time_based) else 0
            quality_bonus = (quality or 50) / 100 * 0.15
            
            final_score = base_score + time_bonus + quality_bonus
            
            recommendations.append({
                "channel_id": ch_id,
                "channel_name": name,
                "score": round(final_score, 2),
                "reason": self._get_reason(i, bool(time_bonus)),
                "views_7d": views,
                "quality": round(quality or 0, 1)
            })
        
        return sorted(recommendations, key=lambda x: x['score'], reverse=True)
    
    def _get_reason(self, position: int, is_time_based: bool) -> str:
        reasons = [
            "🔥 Am meisten angeschaut",
            "❤️ Beliebt in deiner Region",
            "⭐ Top-Qualität",
            "🎯 Perfekt für diese Uhrzeit",
            "🚀 Trending jetzt"
        ]
        if is_time_based:
            return "🕐 Populär um diese Zeit"
        return reasons[min(position, len(reasons)-1)]

class StorageOptimizer:
    """Intelligente Speicherverwaltung mit Machine Learning"""
    
    def __init__(self, db_path, storage_path: str, max_gb: float = 900):
        self.db_path = db_path
        self.storage_path = storage_path
        self.max_gb = max_gb
    
    def predict_storage_needs(self, days_ahead: int = 7) -> Dict:
        """Vorhersage des Speicherbedarfs für nächste Tage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Analysiere Aufnahmemuster der letzten 30 Tage
        cursor.execute("""
            SELECT DATE(created_at) as day, SUM(size_gb) as daily_size
            FROM recordings
            WHERE status = 'completed' AND created_at > datetime('now', '-30 days')
            GROUP BY DATE(created_at)
            ORDER BY day
        """)
        
        daily_data = cursor.fetchall()
        conn.close()
        
        if len(daily_data) < 5:
            return {"prediction": "insufficient_data"}
        
        sizes = np.array([row[1] or 0 for row in daily_data])
        
        # Linear regression für Trend
        trend = np.polyfit(range(len(sizes)), sizes, 1)[0]
        avg_daily = np.mean(sizes)
        
        # Vorhersage
        predicted_usage = [avg_daily + trend * i for i in range(1, days_ahead + 1)]
        total_predicted = sum(predicted_usage)
        
        return {
            "daily_average_gb": round(avg_daily, 2),
            "trend_gb_per_day": round(trend, 2),
            "7day_forecast_gb": round(total_predicted, 2),
            "recommendation": self._get_storage_recommendation(total_predicted)
        }
    
    def _get_storage_recommendation(self, predicted_gb: float) -> str:
        if predicted_gb > 100:
            return "⚠️ Speicher in 7 Tagen voll - jetzt optimieren!"
        elif predicted_gb > 50:
            return "💾 Speicher wird knapp - alte Aufnahmen löschen empfohlen"
        else:
            return "✅ Speicher ok für nächste Woche"

class AnomalyDetector:
    """Erkennt abnormale Muster und Probleme"""
    
    def __init__(self, db_path):
        self.db_path = db_path
        self.anomaly_threshold = 2.0  # Z-Score
    
    def detect_signal_anomalies(self, channel_id: str) -> List[Dict]:
        """Findet abnormale Signalverhalten"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT snr, timestamp FROM signal_history
            WHERE channel_id = ? AND timestamp > datetime('now', '-7 days')
            ORDER BY timestamp
        """, (channel_id,))
        
        data = cursor.fetchall()
        conn.close()
        
        if len(data) < 10:
            return []
        
        snr_values = np.array([d[0] for d in data if d[0]])
        
        # Z-Score Normalisierung
        mean = np.mean(snr_values)
        std = np.std(snr_values)
        
        anomalies = []
        for i, (snr, timestamp) in enumerate(data):
            if snr:
                z_score = abs((snr - mean) / (std + 1e-10))
                if z_score > self.anomaly_threshold:
                    anomalies.append({
                        "timestamp": timestamp,
                        "snr": snr,
                        "z_score": round(z_score, 2),
                        "severity": "high" if z_score > 3 else "medium",
                        "interpretation": self._interpret_anomaly(snr, mean)
                    })
        
        return anomalies[-5:]  # Letzte 5
    
    def _interpret_anomaly(self, snr: float, mean: float) -> str:
        if snr < mean * 0.5:
            return "Kritischer Signalabfall - Blockiertes Signal?"
        elif snr > mean * 1.5:
            return "Unerwarteter Signalsprung - Reflektionen?"
        else:
            return "Abnormale Signalvariation"
    
    def detect_viewing_anomalies(self) -> List[Dict]:
        """Findet abnormale Sehgewohnheiten"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Durchschnittliche Sehdauer pro Tag
        cursor.execute("""
            SELECT DATE(timestamp) as day, SUM(duration_minutes) as total_minutes
            FROM viewing_history
            WHERE timestamp > datetime('now', '-30 days')
            GROUP BY day
        """)
        
        daily_data = cursor.fetchall()
        conn.close()
        
        if len(daily_data) < 7:
            return []
        
        minutes = np.array([d[1] or 0 for d in daily_data])
        mean = np.mean(minutes)
        std = np.std(minutes)
        
        anomalies = []
        for day, minutes_watched in daily_data[-7:]:
            z_score = abs((minutes_watched - mean) / (std + 1e-10))
            if z_score > 1.5:
                anomalies.append({
                    "day": day,
                    "watched_minutes": minutes_watched,
                    "typical_minutes": round(mean, 0),
                    "deviation": "higher" if minutes_watched > mean else "lower"
                })
        
        return anomalies

class AutonomousOptimizer:
    """Autonome Optimierung ohne Nutzer-Eingabe"""
    
    def __init__(self, db_path):
        self.db_path = db_path
    
    def get_autonomous_actions(self) -> List[Dict]:
        """Generiert automatische Optimierungsmaßnahmen"""
        actions = []
        
        # 1. Speicheroptimierung
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT SUM(size_gb) as total FROM recordings WHERE status = 'completed'
        """)
        total_storage = cursor.fetchone()[0] or 0
        
        if total_storage > 850:  # >850GB von 900GB
            actions.append({
                "type": "storage_cleanup",
                "priority": "critical",
                "action": "Lösche Aufnahmen älter als 60 Tage",
                "expected_savings_gb": round((total_storage - 800) * 1.2, 1)
            })
        
        # 2. Signal-Optimierung
        cursor.execute("""
            SELECT channel_id, AVG(snr) as avg_snr FROM signal_history
            WHERE timestamp > datetime('now', '-7 days')
            GROUP BY channel_id
            HAVING avg_snr < 6
        """)
        
        poor_channels = cursor.fetchall()
        for ch_id, snr in poor_channels:
            actions.append({
                "type": "signal_optimization",
                "priority": "high",
                "channel_id": ch_id,
                "action": "Wechsle zu besserer Satelliten-Position",
                "current_snr": round(snr, 1),
                "target_snr": 10
            })
        
        # 3. Aufnahmeplanung
        cursor.execute("""
            SELECT COUNT(*) FROM viewing_history
            WHERE timestamp > datetime('now', '-7 days')
                AND STRFTIME('%w', timestamp) = STRFTIME('%w', 'now')
                AND STRFTIME('%H', timestamp) BETWEEN '20' AND '22'
        """)
        evening_count = cursor.fetchone()[0]
        
        if evening_count > 0:
            actions.append({
                "type": "recording_suggestion",
                "priority": "medium",
                "action": "Plan neue Aufnahmen um 20-22 Uhr (deine Lieblingszeit)",
                "confidence": round(min(evening_count / 10, 1.0), 2)
            })
        
        conn.close()
        
        return sorted(actions, key=lambda x: {"critical": 0, "high": 1, "medium": 2}.get(x["priority"], 3))

class UserBehaviorAnalyzer:
    """Analysiert Nutzerverhalten für bessere Vorhersagen"""
    
    def __init__(self, db_path):
        self.db_path = db_path
    
    def get_viewing_insights(self) -> Dict:
        """Detaillierte Sehgewohnheiten-Analyse"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Favorite times
        cursor.execute("""
            SELECT STRFTIME('%H', timestamp) as hour, COUNT(*) as count
            FROM viewing_history
            WHERE timestamp > datetime('now', '-30 days')
            GROUP BY hour
            ORDER BY count DESC
            LIMIT 3
        """)
        
        favorite_hours = cursor.fetchall()
        
        # Top channels
        cursor.execute("""
            SELECT c.name, SUM(v.duration_minutes) as total_minutes
            FROM viewing_history v
            JOIN channels c ON v.channel_id = c.id
            WHERE v.timestamp > datetime('now', '-30 days')
            GROUP BY v.channel_id
            ORDER BY total_minutes DESC
            LIMIT 5
        """)
        
        top_channels = cursor.fetchall()
        
        # Trends
        cursor.execute("""
            SELECT DATE(timestamp), SUM(duration_minutes) as daily_total
            FROM viewing_history
            WHERE timestamp > datetime('now', '-30 days')
            GROUP BY DATE(timestamp)
            ORDER BY DATE(timestamp)
        """)
        
        daily_totals = [row[1] for row in cursor.fetchall()]
        
        trend = np.polyfit(range(len(daily_totals)), daily_totals, 1)[0] if len(daily_totals) > 1 else 0
        
        conn.close()
        
        return {
            "favorite_hours": [f"{h:02d}:00-{h:02d}:59" for h, _ in favorite_hours[:3]],
            "top_channels": [{"name": name, "hours": round(minutes/60, 1)} for name, minutes in top_channels],
            "daily_average_hours": round(np.mean(daily_totals) / 60, 1) if daily_totals else 0,
            "trend": "increasing" if trend > 0 else "decreasing",
            "total_hours_month": round(sum(daily_totals) / 60, 1)
        }

# ==================== PRO ANALYTICS ====================

class AdvancedAnalytics:
    """Erweiterte Analytik und Insights"""
    
    def __init__(self, db_path):
        self.db_path = db_path
    
    def get_network_health_score(self) -> Dict:
        """Gesamtheitlicher Netzwerk-Gesundheitsscore"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Signal quality
        cursor.execute("""
            SELECT AVG(snr) FROM signal_history WHERE timestamp > datetime('now', '-7 days')
        """)
        avg_snr = cursor.fetchone()[0] or 0
        signal_score = min(avg_snr / 12 * 100, 100)
        
        # Packet loss
        cursor.execute("""
            SELECT AVG(packet_loss) FROM signal_history WHERE timestamp > datetime('now', '-7 days')
        """)
        avg_pl = cursor.fetchone()[0] or 0
        packet_score = max(100 - (avg_pl * 1000), 0)
        
        # Recording success rate
        cursor.execute("""
            SELECT COUNT(*) as total, SUM(CASE WHEN status='completed' THEN 1 ELSE 0 END) as completed
            FROM recordings
            WHERE created_at > datetime('now', '-7 days')
        """)
        result = cursor.fetchone()
        total, completed = result if result[0] > 0 else (1, 1)
        recording_score = (completed / total) * 100 if total > 0 else 100
        
        conn.close()
        
        # Weighted score
        overa
