try {
  var secret = window.AriaNgServerConfig ? window.AriaNgServerConfig.rpcSecret : '';
  
  // Update AriaNg.Options key in localStorage
  var optionsKey = 'AriaNg.Options';
  var optionsStr = localStorage.getItem(optionsKey);
  var options = optionsStr ? JSON.parse(optionsStr) : {};
  
  options.rpcHost = location.hostname;
  options.rpcPort = location.port ? location.port : (location.protocol === 'https:' ? '443' : '80');
  options.protocol = location.protocol === 'https:' ? 'wss' : 'ws';
  options.rpcInterface = 'jsonrpc';
  options.secret = secret ? btoa(secret) : ''; // Base64 encoding required by AriaNg
  
  localStorage.setItem(optionsKey, JSON.stringify(options));

  // Fallback for ariaNg.settings key
  var legacyKey = 'ariaNg.settings';
  var legacyStr = localStorage.getItem(legacyKey);
  var legacy = legacyStr ? JSON.parse(legacyStr) : {};
  
  legacy.rpcHost = location.hostname;
  legacy.rpcPort = location.port ? location.port : (location.protocol === 'https:' ? '443' : '80');
  legacy.protocol = location.protocol === 'https:' ? 'wss' : 'ws';
  legacy.rpcInterface = 'jsonrpc';
  legacy.secret = secret ? btoa(secret) : '';
  
  localStorage.setItem(legacyKey, JSON.stringify(legacy));
} catch (e) {
  console.error("Failed to apply dynamic server-side settings:", e);
}
