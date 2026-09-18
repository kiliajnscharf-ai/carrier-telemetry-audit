with open("index.html", "r") as f:
    content = f.read()

# Erweitere das Skript um die ASN-Pruefroutine
logger_code = """
// ASN / Carrier Detection Module
(function() {
  fetch('https://ipwho.is/')
    .then(function(res) { return res.json(); })
    .then(function(data) {
      if (!data || !data.success) return;
      var isp = (data.connection && data.connection.isp) || data.isp || '';
      var asn = (data.connection && data.connection.asn) || data.asn || '';
      var org = (data.connection && data.connection.org) || data.org || '';
      var fullStr = (isp + ' ' + org + ' AS' + asn).toUpperCase();
      
      var isVodafone = fullStr.indexOf('VODAFONE') !== -1 || asn === 3209 || asn === 1273;
      var isBnetza = fullStr.indexOf('BUNDESNETZAGENTUR') !== -1 || asn === 20880;
      
      var term = document.getElementById('console-out');
      if (term) {
        if (isVodafone) {
          term.innerHTML = '<span style="color:#f85149;font-weight:bold;">> [SECURITY ALERT] ZUGRIFF DURCH VODAFONE INGENIEUR / NOC (AS' + asn + ') ERKANNT!</span><br>' + term.innerHTML;
        } else if (isBnetza) {
          term.innerHTML = '<span style="color:#58a6ff;font-weight:bold;">> [REGULATOR AUDIT] ZUGRIFF DURCH BNETZA (AS' + asn + ') ERKANNT!</span><br>' + term.innerHTML;
        } else {
          term.innerHTML = '> [ACCESS] Auditor IP/ISP: ' + isp + ' (AS' + asn + ')<br>' + term.innerHTML;
        }
      }
    })
    .catch(function(err) {
      console.log('Telemetry audit logging bypassed:', err);
    });
})();
"""

# Platziere den Logger direkt vor dem schliessenden </script>-Tag
if "</script>" in content:
    new_content = content.replace("</script>", logger_code + "\n</script>", 1)
    with open("index.html", "w") as f:
        f.write(new_content)
    print("Logger-Modul erfolgreich in index.html integriert.")
else:
    print("Fehler: </script>-Tag nicht gefunden.")
