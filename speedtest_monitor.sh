!/usr/bin/env python3
"""
Speedtest Monitor für Bad Pyrmont Netzwerkstörungen
Misst kontinuierlich Download, Upload, Latenz und Jitter
"""

import subprocess
import json
import csv
import sys
from datetime import datetime
import time
import os

class SpeedtestMonitor:
    def __init__(self, log_file="speedtest_results.csv", interval=300, max_retries=3):
        self.log_file = log_file
        self.interval = interval  # Sekunden
        self.max_retries = max_retries
        self.fieldnames = ['timestamp', 'download_mbps', 'upload_mbps', 'latency_ms', 'jitter_ms', 'server', 'location']
        
        # Header schreiben, falls Datei neu
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()
    
    def run_speedtest(self):
        """Führt Speedtest durch und gibt Ergebnisse als Dict zurück"""
        try:
            # Speedtest mit JSON-Output
            result = subprocess.run(
                ['speedtest-cli', '--json'],
                capture_output=True,
                text=True,
                timeout=600  # 10 Minuten Timeout
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                
                return {
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'download_mbps': round(data['download'] / 1_000_000, 2),
                    'upload_mbps': round(data['upload'] / 1_000_000, 2),
                    'latency_ms': round(data['ping'], 2),
                    'jitter_ms': round(data.get('jitter', 0), 2),
                    'server': data.get('server', {}).get('name', 'Unknown'),
                    'location': data.get('server', {}).get('sponsor', 'Unknown'),
                }
            else:
                return None
                
        except subprocess.TimeoutExpired:
            print("⏱️  Timeout - Test hat zu lange gedauert")
            return None
        except json.JSONDecodeError:
            print("❌ JSON Parse Fehler")
            return None
        except FileNotFoundError:
            print("❌ speedtest-cli nicht installiert. Führe aus: pip3 install speedtest-cli")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Fehler: {e}")
            return None
    
    def save_result(self, result):
        """Speichert Ergebnis in CSV"""
        if result is None:
            result = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'download_mbps': 'ERROR',
                'upload_mbps': 'ERROR',
                'latency_ms': 'ERROR',
                'jitter_ms': 'ERROR',
                'server': 'ERROR',
                'location': 'ERROR',
            }
        
        with open(self.log_file, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writerow(result)
    
    def print_result(self, result):
        """Formatierte Ausgabe der Ergebnisse"""
        if result is None:
            print(f"❌ Messung fehlgeschlagen")
            return
        
        print(f"\n✅ [{result['timestamp']}]")
        print(f"   ⬇️  Download:    {result['download_mbps']:>8} Mbps")
        print(f"   ⬆️  Upload:      {result['upload_mbps']:>8} Mbps")
        print(f"   📡 Latenz:      {result['latency_ms']:>8} ms")
        print(f"   📊 Jitter:      {result['jitter_ms']:>8} ms")
        print(f"   🖥️  Server:      {result['server']}")
        print(f"   📍 Ort:         {result['location']}")
        print("-" * 50)
    
    def start_monitoring(self):
        """Startet kontinuierliches Monitoring"""
        print("\n" + "="*50)
        print("🚀 SPEEDTEST MONITOR - BAD PYRMONT")
        print("="*50)
        print(f"📊 Ergebnisse: {self.log_file}")
        print(f"⏱️  Intervall: {self.interval} Sekunden ({self.interval/60:.1f} min)")
        print(f"🔄 Max. Versuche: {self.max_retries}")
        print("="*50)
        
        test_count = 0
        error_count = 0
        
        try:
            while True:
                test_count += 1
                print(f"\n🔄 Test {test_count} - {datetime.now().strftime('%H:%M:%S')}")
                
                retry = 0
                result = None
                
                while retry < self.max_retries and result is None:
                    result = self.run_speedtest()
                    
                    if result is None:
                        retry += 1
                        if retry < self.max_retries:
                            wait = 30
                            print(f"⚠️  Versuch {retry}/{self.max_retries} fehlgeschlagen - Wiederhole in {wait}s...")
                            time.sleep(wait)
                    else:
                        self.print_result(result)
                        self.save_result(result)
                
                if result is None:
                    error_count += 1
                    print(f"❌ Test {test_count} fehlgeschlagen nach {self.max_retries} Versuchen")
                    self.save_result(None)
                    
                    # Statistik
                    error_rate = (error_count / test_count) * 100
                    print(f"📈 Fehlerrate: {error_rate:.1f}% ({error_count}/{test_count})")
                
                # Warten bis zur nächsten Messung
                print(f"⏳ Nächste Messung in {self.interval} Sekunden...")
                time.sleep(self.interval)
                
        except KeyboardInterrupt:
            print(f"\n\n🛑 Monitor beendet")
            print(f"📊 Statistik:")
            print(f"   ✅ Erfolgreich: {test_count - error_count}/{test_count}")
            print(f"   ❌ Fehler: {error_count}/{test_count}")
            print(f"   📁 Datei: {self.log_file}")
            sys.exit(0)

if __name__ == "__main__":
    # Konfiguration
    INTERVAL = 300  # 5 Minuten
    LOG_FILE = "speedtest_results.csv"
    MAX_RETRIES = 3
    
    monitor = SpeedtestMonitor(log_file=LOG_FILE, interval=INTERVAL, max_retries=MAX_RETRIES)
    monitor.start_monitoring()
