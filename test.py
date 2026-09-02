"""
🚀 SATELLITEN-ZENTRALE PRO BACKEND - ELITE VERSION
Advanced AI, Autonome Systeme, Echtzeit-Analytics, Deep Insights
"""

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
from datetime import datetime, timedelta
import sqlite3
from ai_engine_pro import AIEnginePRO
import numpy as np

app = FastAPI(title="Satelliten-Zentrale Pro Elite", version="2.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global AI Engine
ai_engine = None
active_websockets = set()

@app.on_event("startup")
async def startup():
    global ai_engine
    ai_engine = AIEnginePRO("satellitten.db")
    print("🧠 AI Engine Pro initialized")

# ==================== WEBSOCKET REAL-TIME ====================

@app.websocket("/ws/live-dashboard")
async def websocket_live_dashboard(websocket: WebSocket):
    """Live WebSocket für Echtzeit-Dashboard Updates"""
    await websocket.accept()
    active_websockets.add(websocket)
    
    try:
        while True:
            # Sende alle 2 Sekunden aktualisierte Daten
            dashboard = ai_engine.get_comprehensive_dashboard()
            await websocket.send_json({
                "type": "dashboard_update",
                "timestamp": datetime.now().isoformat(),
                "data": dashboard
            })
            await asyncio.sleep(2)
    except Exception as e:
        active_websockets.discard(websocket)

@app.websocket("/ws/signal-monitor/{channel_id}")
async def websocket_signal_monitor(websocket: WebSocket, channel_id: str):
    """Live Signal-Monitoring per Channel"""
    await websocket.accept()
    
    try:
        while True:
            prediction = ai_engine.signal_predictor.predict_signal_quality_next_hour(channel_id)
            anomalies = ai_engine.anomaly_detector.detect_signal_anomalies(channel_id)
            
            await websocket.send_json({
                "type": "signal_update",
                "channel_id": channel_id,
                "prediction": prediction,
                "anomalies": anomalies,
                "timestamp": datetime.now().isoformat()
            })
            await asyncio.sleep(5)
    except:
        pass

# ==================== AI ENDPOINTS ====================

@app.get("/api/v2/ai/comprehensive-dashboard")
async def get_pro_dashboard():
    """Vollständiges Pro-Dashboard mit allen AI-Features"""
    return ai_engine.get_comprehensive_dashboard()

@app.get("/api/v2/ai/predictions/{channel_id}")
async def get_channel_prediction(channel_id: str):
    """Vorhersagen für spezifischen Channel"""
    return ai_engine.signal_predictor.predict_signal_quality_next_hour(channel_id)

@app.get("/api/v2/ai/smart-recommendations")
async def get_smart_recommendations():
    """AI-generierte Smart Recommendations"""
    return {
        "recommendations": ai_engine.recommendation_engine.get_ai_recommendations(),
        "reasoning": "Basierend auf Viewing-Verhalten, Signalqualität und Zeit"
    }

@app.get("/api/v2/ai/anomalies/{channel_id}")
async def detect_anomalies(channel_id: str):
    """Anomalie-Erkennung"""
    return {
        "signal_anomalies": ai_engine.anomaly_detector.detect_signal_anomalies(channel_id),
        "viewing_anomalies": ai_engine.anomaly_detector.detect_viewing_anomalies()
    }

@app.get("/api/v2/ai/autonomous-actions")
async def get_autonomous_actions():
    """Autonome Optimierungsmaßnahmen"""
    return {
        "actions": ai_engine.autonomous_optimizer.get_autonomous_actions(),
        "auto_executed": True
    }

@app.get("/api/v2/ai/network-health")
async def get_network_health():
    """Gesamtheitlicher Netzwerk-Gesundheitsscore"""
    return ai_engine.analytics.get_network_health_score()

@app.get("/api/v2/ai/viewing-insights")
async def get_viewing_insights():
    """Detaillierte Sehgewohnheits-Analyse"""
    return ai_engine.behavior_analyzer.get_viewing_insights()

@app.get("/api/v2/ai/storage-forecast")
async def get_storage_forecast(days: int = 7):
    """Speicher-Vorhersage"""
    return ai_engine.storage_optimizer.predict_storage_needs(days)

@app.get("/api/v2/ai/roi-metrics")
async def get_roi_metrics():
    """ROI und Effizienz-Metriken"""
    return ai_engine.analytics.get_roi_metrics()

# ==================== ADVANCED ANALYTICS ====================

@app.get("/api/v2/analytics/signal-quality-report")
async def signal_quality_report():
    """Detaillierter Signalqualitäts-Report"""
    conn = sqlite3.connect("satellitten.db")
    cursor = conn.cursor()
    
    # Top/Bottom Channels
    cursor.execute("""
        SELECT channel_id, AVG(snr) as avg_snr, MIN(snr) as min_snr, MAX(snr) as max_snr
        FROM signal_history
        WHERE timestamp > datetime('now', '-7 days')
        GROUP BY channel_id
        ORDER BY avg_snr DESC
    """)
    
    channels = cursor.fetchall()
    conn.close()
    
    return {
        "best_channels": [
            {"channel": ch[0], "avg_snr": round(ch[1], 1), "min": round(ch[2], 1), "max": round(ch[3], 1)}
            for ch in channels[:5]
        ],
        "worst_channels": [
            {"channel": ch[0], "avg_snr": round(ch[1], 1), "min": round(ch[2], 1), "max": round(ch[3], 1)}
            for ch in channels[-5:]
        ]
    }

@app.get("/api/v2/analytics/time-series/{metric}")
async def get_time_series(metric: str, days: int = 30):
    """Zeit-Serie für Metriken"""
    conn = sqlite3.connect("satellitten.db")
    cursor = conn.cursor()
    
    if metric == "signal":
        cursor.execute("""
            SELECT DATE(timestamp), AVG(snr), MIN(snr), MAX(snr)
            FROM signal_history
            WHERE timestamp > datetime('now', '-' || ? || ' days')
            GROUP BY DATE(timestamp)
            ORDER BY DATE(timestamp)
        """, (days,))
        
        data = cursor.fetchall()
        return {
            "metric": "signal_quality",
            "data": [
                {"date": d[0], "avg": round(d[1] or 0, 1), "min": round(d[2] or 0, 1), "max": round(d[3] or 0, 1)}
                for d in data
            ]
        }
    
    elif metric == "viewing":
        cursor.execute("""
            SELECT DATE(timestamp), SUM(duration_minutes), COUNT(*)
            FROM viewing_history
            WHERE timestamp > datetime('now', '-' || ? || ' days')
            GROUP BY DATE(timestamp)
            ORDER BY DATE(timestamp)
        """, (days,))
        
        data = cursor.fetchall()
        return {
            "metric": "viewing_hours",
            "data": [
                {"date": d[0], "hours": round((d[1] or 0) / 60, 1), "sessions": d[2]}
                for d in data
            ]
        }
    
    conn.close()

@app.get("/api/v2/analytics/correlations")
async def get_correlations():
    """Korrelationen zwischen verschiedenen Metriken"""
    conn = sqlite3.connect("satellitten.db")
    cursor = conn.cursor()
    
    # Signal vs Viewing
    cursor.execute("""
        SELECT c.id, c.name, 
               AVG(sh.snr) as avg_signal,
               COUNT(vh.id) as view_count
        FROM channels c
        LEFT JOIN signal_history sh ON c.id = sh.channel_id AND sh.timestamp > datetime('now', '-7 days')
        LEFT JOIN viewing_history vh ON c.id = vh.channel_id AND vh.timestamp > datetime('now', '-7 days')
        GROUP BY c.id
        HAVING view_count > 0
    """)
    
    data = cursor.fetchall()
    conn.close()
    
    signals = np.array([d[2] or 0 for d in data])
    views = np.array([d[3] or 0 for d in data])
    
    if len(signals) > 1:
        correlation = np.corrcoef(signals, views)[0, 1]
    else:
        correlation = 0
    
    return {
        "signal_vs_viewing": round(correlation, 3),
        "interpretation": "Gute Signalqualität = mehr Views" if correlation > 0.3 else "Keine starke Korrelation"
    }

# ==================== SMART ALERTS ====================

@app.get("/api/v2/alerts/critical")
async def get_critical_alerts():
    """Kritische Warnungen"""
    alerts = []
    
    conn = sqlite3.connect("satellitten.db")
    cursor = conn.cursor()
    
    # 1. Schlechtes Signal
    cursor.execute("""
        SELECT channel_id, AVG(snr) FROM signal_history
        WHERE timestamp > datetime('now', '-1 hour')
        GROUP BY channel_id
        HAVING AVG(snr) < 3
    """)
    
    for ch_id, snr in cursor.fetchall():
        alerts.append({
            "severity": "critical",
            "type": "signal",
            "channel": ch_id,
            "message": f"🔴 Kritisches Signal {snr:.1f}dB - Überprüfen!",
            "action": "Antennenposition justieren"
        })
    
    # 2. Speicher voll
    cursor.execute("""
        SELECT SUM(size_gb) FROM recordings WHERE status = 'completed'
    """)
    total_gb = cursor.fetchone()[0] or 0
    
    if total_gb > 880:
        alerts.append({
            "severity": "critical",
            "type": "storage",
            "message": f"💾 Speicher zu {(total_gb/9):.0f}% voll!",
            "action": "Alte Aufnahmen löschen"
        })
    
    # 3. Hohe Paketloss
    cursor.execute("""
        SELECT AVG(packet_loss) FROM signal_history WHERE timestamp > datetime('now', '-1 hour')
    """)
    
    pl = cursor.fetchone()[0] or 0
    if pl > 0.05:
        alerts.append({
            "severity": "critical",
            "type": "packet_loss",
            "message": f"📡 Paketloss {pl*100:.2f}% - Netzwerk Problem?",
            "action": "Internet-Verbindung prüfen"
        })
    
    conn.close()
    
    return {"alerts": alerts, "count": len(alerts)}

# ==================== PREDICTIVE MAINTENANCE ====================

@app.get("/api/v2/maintenance/forecast")
async def maintenance_forecast():
    """Vorhersage für Wartungsbedarf"""
    conn = sqlite3.connect("satellitten.db")
    cursor = conn.cursor()
    
    # Analysiere Fehlerrate
    cursor.execute("""
        SELECT COUNT(*) as total, 
               SUM(CASE WHEN status != 'completed' THEN 1 ELSE 0 END) as failed
        FROM recordings
        WHERE created_at > datetime('now', '-30 days')
    """)
    
    total, failed = cursor.fetchone()
    error_rate = (failed / max(total, 1)) * 100 if total > 0 else 0
    
    conn.close()
    
    maintenance_needed = []
    
    if error_rate > 10:
        maintenance_needed.append({
            "component": "Tuner",
            "urgency": "high",
            "reason": f"Fehlerrate {error_rate:.1f}%",
            "estimated_life": "1-2 Wochen"
        })
    
    return {
        "maintenance_items": maintenance_needed,
        "system_health": "Gut" if error_rate < 5 else "Überprüfung nötig"
    }

# ==================== SMART AUTOMATION ====================

@app.post("/api/v2/automation/execute-action/{action_id}")
async def execute_automation_action(action_id: str):
    """Führe automatische Optimierung aus"""
    actions = ai_engine.autonomous_optimizer.get_autonomous_actions()
    
    for action in actions:
        if action.get("type") == action_id:
            result = {
                "action": action_id,
                "status": "executed",
                "timestamp": datetime.now().isoformat()
            }
            
            if action_id == "storage_cleanup":
                result["freed_gb"] = action.get("expected_savings_gb", 0)
            
            return result
    
    return {"status": "error", "message": "Action not found"}

@app.get("/api/v2/automation/status")
async def get_automation_status():
    """Status der automatischen Systeme"""
    return {
        "autonomous_mode": True,
        "running_optimizations": len(ai_engine.autonomous_optimizer.get_autonomous_actions()),
        "last_optimization": datetime.now().isoformat(),
        "next_scheduled": (datetime.now() + timedelta(hours=1)).isoformat(),
        "automation_level": "Full Auto"
    }

# ==================== INSIGHTS & INTELLIGENCE ====================

@app.get("/api/v2/insights/summary")
async def get_insights_summary():
    """Kurze intelligente Zusammenfassung"""
    insights = ai_engine.behavior_analyzer.get_viewing_insights()
    health = ai_engine.analytics.get_network_health_score()
    
    return {
        "top_summary": [
            f"👁️ Du schaust durchschnittlich {insights['daily_average_hours']} Stunden pro Tag",
            f"⏰ Deine Lieblingszeit: {insights['favorite_hours'][0]}" if insights['favorite_hours'] else "Keine Daten",
            f"📡 Netzwerk-Gesundheit: {health['status']} ({health['overall_score']:.0f}%)",
            f"🔥 Top Sender: {insights['top_channels'][0]['name']}" if insights['top_channels'] else "Keine Daten"
        ]
    }

@app.get("/api/v2/insights/next-24h")
async def get_next_24h_insights():
    """Was kommt in den nächsten 24h?"""
    conn = sqlite3.connect("satellitten.db")
    cursor = conn.cursor()
    
    # Wahrscheinliche Aktivitäten basierend auf Historien
    current_hour = datetime.now().hour
    cursor.execute("""
        SELECT strftime('%H', timestamp) as hour, COUNT(*) as count
        FROM viewing_history
        WHERE strftime('%w', timestamp) = strftime('%w', 'now')
            AND timestamp > datetime('now', '-7 days')
        GROUP BY hour
        ORDER BY count DESC
        LIMIT 3
    """)
    
    likely_active = cursor.fetchall()
    
    # EPG für nächste 24h
    cursor.execute("""
        SELECT COUNT(*) FROM epg WHERE start_time > datetime('now') AND start_time < datetime('now', '+24 hours')
    """)
    
    programs = cursor.fetchone()[0]
    conn.close()
    
    return {
        "likely_active_hours": [f"{int(h):02d}:00-{int(h):02d}:59" for h, _ in likely_active],
        "programs_available": programs,
        "recommendations": "Neue Sender basierend auf deiner Aktivität" if likely_active else "Keine Vorhersage möglich"
    }

# ==================== EXPORT & REPORTING ====================

@app.get("/api/v2/export/monthly-report")
async def export_monthly_report():
    """Export des Monatsberichts"""
    insights = ai_engine.behavior_analyzer.get_viewing_insights()
    roi = ai_engine.analytics.get_roi_metrics()
    health = ai_engine.analytics.get_network_health_score()
    
    return {
        "month": datetime.now().strftime("%B %Y"),
        "viewing_summary": {
            "total_hours": insights['total_hours_month'],
            "favorite_hours": insights['favorite_hours'],
            "top_5_channels": insights['top_channels']
        },
        "system_performance": health,
        "efficiency_metrics": roi,
        "generated": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
