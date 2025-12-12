# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# from fastapi.responses import HTMLResponse
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import httpx
# import json
# import asyncio

# app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Translation API URL
# TRANSLATION_API_URL = "http://[::]:5000/translate"

# class TranslationRequest(BaseModel):
#     text: str
#     target: str = "ur"
#     is_interim: bool = False

# async def send_to_translation_api(text: str, target_lang: str):
#     """Ultra-fast translation with minimal timeout"""
#     try:
#         async with httpx.AsyncClient(timeout=1.5) as http_client:
#             response = await http_client.post(
#                 TRANSLATION_API_URL,
#                 json={
#                     "q": text,
#                     "source": "auto",
#                     "target": target_lang,
#                     "format": "text",
#                     "alternatives": 1,
#                     "api_key": ""
#                 },
#                 headers={"Content-Type": "application/json"}
#             )
#             if response.status_code == 200:
#                 return response.json()
#             else:
#                 return {"error": f"API status {response.status_code}"}
#     except Exception as e:
#         return {"error": f"API error: {str(e)}"}

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     """WebSocket for continuous audio stream processing"""
#     await websocket.accept()
#     try:
#         while True:
#             data = await websocket.receive_text()
#             try:
#                 req = TranslationRequest(**json.loads(data))
#                 translation_response = await send_to_translation_api(req.text, req.target)
#                 await websocket.send_text(json.dumps({
#                     'type': 'translation_chunk',
#                     'original': req.text,
#                     'translation': translation_response,
#                     'is_interim': req.is_interim
#                 }))
#             except Exception as e:
#                 await websocket.send_text(json.dumps({
#                     'type': 'error',
#                     'message': str(e)
#                 }))
#     except WebSocketDisconnect:
#         print("WebSocket disconnected")

# @app.get("/", response_class=HTMLResponse)
# async def home():
#     """NEVER-STOP listening with triple-redundant restart mechanisms"""
#     return """
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>⚡ NEVER-STOP Translation - Always Active</title>
#     <style>
#         * {
#             margin: 0;
#             padding: 0;
#             box-sizing: border-box;
#         }
#         body {
#             font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#             background: #0a0e27;
#             color: #e2e8f0;
#             padding: 20px;
#             line-height: 1.6;
#         }
#         .container {
#             max-width: 1400px;
#             margin: 0 auto;
#         }
#         h1 {
#             text-align: center;
#             margin-bottom: 30px;
#             font-size: 2.5em;
#             background: linear-gradient(135deg, #00ff87 0%, #60efff 100%);
#             -webkit-background-clip: text;
#             -webkit-text-fill-color: transparent;
#             background-clip: text;
#             text-shadow: 0 0 30px rgba(0, 255, 135, 0.3);
#         }
#         .input-section {
#             background: linear-gradient(135deg, #1a1f3a 0%, #0f1423 100%);
#             border-radius: 16px;
#             padding: 30px;
#             margin-bottom: 20px;
#             border: 2px solid #00ff8750;
#             box-shadow: 0 8px 32px rgba(0, 255, 135, 0.1);
#         }
#         .controls {
#             display: flex;
#             gap: 15px;
#             margin-top: 15px;
#             align-items: center;
#             flex-wrap: wrap;
#         }
#         select {
#             padding: 14px 24px;
#             background: #0a0e27;
#             border: 2px solid #00ff8750;
#             border-radius: 10px;
#             color: #00ff87;
#             font-size: 16px;
#             cursor: pointer;
#             font-weight: 600;
#             transition: all 0.3s;
#         }
#         select:hover {
#             border-color: #00ff87;
#             box-shadow: 0 0 20px rgba(0, 255, 135, 0.3);
#         }
#         button {
#             padding: 14px 32px;
#             background: linear-gradient(135deg, #00ff87 0%, #60efff 100%);
#             color: #0a0e27;
#             border: none;
#             border-radius: 10px;
#             font-size: 16px;
#             font-weight: 700;
#             cursor: pointer;
#             transition: all 0.3s;
#             box-shadow: 0 4px 15px rgba(0, 255, 135, 0.4);
#         }
#         button:hover:not(:disabled) {
#             transform: translateY(-2px);
#             box-shadow: 0 6px 25px rgba(0, 255, 135, 0.6);
#         }
#         button:disabled {
#             opacity: 0.3;
#             cursor: not-allowed;
#         }
#         button:active:not(:disabled) {
#             transform: translateY(0);
#         }
#         .status {
#             padding: 10px 20px;
#             border-radius: 25px;
#             font-size: 14px;
#             font-weight: 700;
#             text-transform: uppercase;
#             letter-spacing: 1px;
#         }
#         .status.listening {
#             background: linear-gradient(135deg, #00ff87 0%, #00cc6a 100%);
#             color: #0a0e27;
#             animation: pulse 2s ease-in-out infinite;
#         }
#         .status.stopped {
#             background: #ff4444;
#             color: white;
#         }
#         .status.connected {
#             background: #60efff;
#             color: #0a0e27;
#         }
#         .status.restarting {
#             background: #ffa500;
#             color: white;
#             animation: blink 0.5s infinite;
#         }
#         @keyframes pulse {
#             0%, 100% { box-shadow: 0 0 0 0 rgba(0, 255, 135, 0.7); }
#             50% { box-shadow: 0 0 0 15px rgba(0, 255, 135, 0); }
#         }
#         @keyframes blink {
#             0%, 100% { opacity: 1; }
#             50% { opacity: 0.5; }
#         }
#         .section {
#             background: linear-gradient(135deg, #1a1f3a 0%, #0f1423 100%);
#             border-radius: 16px;
#             padding: 25px;
#             margin-bottom: 20px;
#             border: 2px solid #00ff8730;
#             box-shadow: 0 8px 32px rgba(0, 255, 135, 0.05);
#         }
#         .section h2 {
#             color: #00ff87;
#             margin-bottom: 15px;
#             font-size: 1.5em;
#             display: flex;
#             align-items: center;
#             gap: 10px;
#             text-shadow: 0 0 10px rgba(0, 255, 135, 0.5);
#         }
#         .content {
#             background: #0a0e27;
#             padding: 20px;
#             border-radius: 12px;
#             min-height: 150px;
#             font-size: 16px;
#             white-space: pre-wrap;
#             word-wrap: break-word;
#             border: 1px solid #00ff8730;
#             overflow-y: auto;
#             max-height: 400px;
#         }
#         .live-transcript {
#             background: #0a0e27;
#             padding: 20px;
#             border-radius: 12px;
#             min-height: 100px;
#             font-size: 22px;
#             white-space: pre-wrap;
#             word-wrap: break-word;
#             border: 2px solid #00ff8750;
#             margin-bottom: 10px;
#             color: #60efff;
#             font-weight: 500;
#             box-shadow: inset 0 0 20px rgba(96, 239, 255, 0.1);
#         }
#         .live-transcript.interim {
#             color: #00ff87;
#             font-style: italic;
#             animation: glow 1.5s ease-in-out infinite;
#         }
#         @keyframes glow {
#             0%, 100% { text-shadow: 0 0 5px rgba(0, 255, 135, 0.5); }
#             50% { text-shadow: 0 0 20px rgba(0, 255, 135, 0.8); }
#         }
#         .chunk-box {
#             background: rgba(26, 31, 58, 0.6);
#             padding: 18px;
#             margin-bottom: 15px;
#             border-radius: 12px;
#             border-left: 4px solid #00ff87;
#             display: grid;
#             grid-template-columns: 1fr 1fr;
#             gap: 20px;
#             opacity: 0;
#             animation: slideIn 0.3s ease-out forwards;
#             backdrop-filter: blur(10px);
#         }
#         @keyframes slideIn {
#             from {
#                 opacity: 0;
#                 transform: translateX(-20px);
#             }
#             to {
#                 opacity: 1;
#                 transform: translateX(0);
#             }
#         }
#         .chunk-box .label {
#             color: #60efff;
#             font-weight: 700;
#             font-size: 11px;
#             text-transform: uppercase;
#             margin-bottom: 8px;
#             letter-spacing: 1px;
#         }
#         .chunk-box .text {
#             color: #e2e8f0;
#             line-height: 1.6;
#         }
#         .chunk-box.interim {
#             border-left-color: #60efff;
#             background: rgba(96, 239, 255, 0.05);
#         }
#         .chunk-box.final {
#             border-left-color: #00ff87;
#             background: rgba(0, 255, 135, 0.05);
#         }
#         .info {
#             color: #60efff;
#             font-style: italic;
#             padding: 15px;
#             background: rgba(96, 239, 255, 0.1);
#             border-radius: 10px;
#             margin: 15px 0;
#             border-left: 4px solid #60efff;
#             font-weight: 500;
#         }
#         #micIcon {
#             font-size: 32px;
#             animation: float 3s ease-in-out infinite;
#         }
#         @keyframes float {
#             0%, 100% { transform: translateY(0px); }
#             50% { transform: translateY(-10px); }
#         }
#         .stats {
#             display: grid;
#             grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
#             gap: 15px;
#             margin-top: 15px;
#             font-size: 13px;
#         }
#         .stat {
#             background: rgba(0, 255, 135, 0.1);
#             padding: 12px 16px;
#             border-radius: 8px;
#             border: 1px solid #00ff8730;
#             text-align: center;
#         }
#         .stat-label {
#             font-size: 11px;
#             color: #60efff;
#             margin-bottom: 5px;
#             text-transform: uppercase;
#             letter-spacing: 0.5px;
#         }
#         .stat-value {
#             color: #00ff87;
#             font-weight: 700;
#             font-size: 20px;
#         }
#     </style>
# </head>
# <body>
#     <div class="container">
#         <h1>⚡ NEVER-STOP TRANSLATION - ALWAYS LISTENING</h1>
#         <div class="input-section">
#             <div class="controls">
#                 <span id="micIcon">🎙️</span>
#                 <button id="startBtn">START FOREVER LISTENING</button>
#                 <button id="stopBtn" disabled>STOP</button>
#                 <select id="targetLang">
#                     <option value="hi">Hindi (हिन्दी)</option>
#                     <option value="en">English</option>
#                     <option value="ur">Urdu (اردو)</option>
#                     <option value="ar">Arabic (العربية)</option>
#                     <option value="es">Spanish (Español)</option>
#                     <option value="fr">French (Français)</option>
#                     <option value="de">German (Deutsch)</option>
#                     <option value="ja">Japanese (日本語)</option>
#                     <option value="zh">Chinese (中文)</option>
#                 </select>
#                 <span id="status" class="status stopped">READY</span>
#                 <span id="wsStatus"></span>
#             </div>
#             <div class="stats">
#                 <div class="stat">
#                     <div class="stat-label">Translations</div>
#                     <div class="stat-value" id="transCount">0</div>
#                 </div>
#                 <div class="stat">
#                     <div class="stat-label">Avg Speed</div>
#                     <div class="stat-value" id="avgSpeed">0ms</div>
#                 </div>
#                 <div class="stat">
#                     <div class="stat-label">Restarts</div>
#                     <div class="stat-value" id="restartCount">0</div>
#                 </div>
#                 <div class="stat">
#                     <div class="stat-label">Uptime</div>
#                     <div class="stat-value" id="uptime">0s</div>
#                 </div>
#             </div>
#             <div class="info">🔥 NEVER-STOP MODE: Multiple watchdogs ensure mic NEVER closes. Pause 10 seconds? Still listening. Network error? Auto-restart. Browser limit? We handle it. SPEAK ANYTIME!</div>
#         </div>
#         <div class="section">
#             <h2>🔴 LIVE TRANSCRIPT (Always Active)</h2>
#             <div id="liveTranscript" class="live-transcript">Ready to listen forever...</div>
#         </div>
#         <div class="section">
#             <h2>🌐 INSTANT TRANSLATIONS</h2>
#             <div id="liveContent" class="content"></div>
#         </div>
#     </div>
#     <script>
#         let recognition;
#         let websocket;
#         let translationCount = 0;
#         let currentTranscript = '';
#         let isListening = false;
#         let restartAttempts = 0;
#         let totalLatency = 0;
#         let startTime = 0;
#         let lastActivityTime = 0;
        
#         const startBtn = document.getElementById('startBtn');
#         const stopBtn = document.getElementById('stopBtn');
#         const status = document.getElementById('status');
#         const wsStatus = document.getElementById('wsStatus');
#         const liveTranscript = document.getElementById('liveTranscript');
#         const liveContent = document.getElementById('liveContent');
#         const targetLang = document.getElementById('targetLang');
#         const transCount = document.getElementById('transCount');
#         const avgSpeed = document.getElementById('avgSpeed');
#         const restartCountEl = document.getElementById('restartCount');
#         const uptimeEl = document.getElementById('uptime');

#         // TRIPLE WATCHDOG SYSTEM for bulletproof operation
#         let primaryWatchdog = null;
#         let secondaryWatchdog = null;
#         let emergencyWatchdog = null;

#         function debounce(func, delay) {
#             let timeoutId;
#             return function(...args) {
#                 clearTimeout(timeoutId);
#                 timeoutId = setTimeout(() => func.apply(this, args), delay);
#             };
#         }

#         function connectWebSocket() {
#             if (websocket && websocket.readyState === WebSocket.OPEN) return;
#             websocket = new WebSocket('ws://' + window.location.host + '/ws');
            
#             websocket.onopen = function() {
#                 wsStatus.textContent = '⚡ WS CONNECTED';
#                 wsStatus.className = 'status connected';
#             };
            
#             websocket.onclose = function() {
#                 wsStatus.textContent = '🔄 WS RECONNECTING...';
#                 wsStatus.className = 'status stopped';
#                 setTimeout(connectWebSocket, 300);
#             };
            
#             websocket.onerror = function(error) {
#                 console.error('WS error:', error);
#             };
            
#             websocket.onmessage = function(event) {
#                 const startTime = performance.now();
#                 try {
#                     const data = JSON.parse(event.data);
#                     if (data.type === 'translation_chunk') {
#                         translationCount++;
#                         transCount.textContent = translationCount;
                        
#                         const latency = performance.now() - startTime;
#                         totalLatency += latency;
#                         avgSpeed.textContent = Math.round(totalLatency / translationCount) + 'ms';
                        
#                         let translatedText = '';
#                         if (data.translation) {
#                             if (typeof data.translation === 'string') {
#                                 translatedText = data.translation;
#                             } else if (data.translation.translatedText) {
#                                 translatedText = data.translation.translatedText;
#                             } else if (Array.isArray(data.translation) && data.translation[0]) {
#                                 translatedText = data.translation[0].text || data.translation[0];
#                             } else if (data.translation.text) {
#                                 translatedText = data.translation.text;
#                             } else if (data.translation.error) {
#                                 translatedText = `⚠️ ${data.translation.error}`;
#                             }
#                         }
                        
#                         if (!translatedText || translatedText.trim() === '') {
#                             translatedText = `⚠️ Translating... (${data.original.substring(0, 30)}...)`;
#                             console.warn('Translation format:', data.translation);
#                         }
                        
#                         let chunkDiv = Array.from(liveContent.children).find(el => {
#                             const originalEl = el.querySelector('.text.original');
#                             return originalEl && 
#                                    originalEl.textContent.trim() === data.original.trim() &&
#                                    el.classList.contains('interim');
#                         });
                        
#                         if (data.is_interim) {
#                             if (!chunkDiv) {
#                                 chunkDiv = document.createElement('div');
#                                 chunkDiv.className = 'chunk-box interim';
#                                 chunkDiv.innerHTML = `
#                                     <div>
#                                         <div class="label">🎤 Original</div>
#                                         <div class="text original"></div>
#                                     </div>
#                                     <div>
#                                         <div class="label">⚡ Translating...</div>
#                                         <div class="text translated"></div>
#                                     </div>
#                                 `;
#                                 const origEl = chunkDiv.querySelector('.text.original');
#                                 const transEl = chunkDiv.querySelector('.text.translated');
#                                 if (origEl) origEl.textContent = data.original || '';
#                                 if (transEl) transEl.textContent = translatedText || '';
#                                 liveContent.insertBefore(chunkDiv, liveContent.firstChild);
#                             } else {
#                                 const transEl = chunkDiv.querySelector('.text.translated');
#                                 if (transEl) transEl.textContent = translatedText || '';
#                             }
#                         } else {
#                             if (chunkDiv) {
#                                 chunkDiv.classList.remove('interim');
#                                 chunkDiv.classList.add('final');
#                                 const labelEl = chunkDiv.querySelector('.label:last-of-type');
#                                 const transEl = chunkDiv.querySelector('.text.translated');
#                                 if (labelEl) labelEl.textContent = '✓ Translated';
#                                 if (transEl) transEl.textContent = translatedText || '';
#                             } else {
#                                 chunkDiv = document.createElement('div');
#                                 chunkDiv.className = 'chunk-box final';
#                                 chunkDiv.innerHTML = `
#                                     <div>
#                                         <div class="label">🎤 Original</div>
#                                         <div class="text original"></div>
#                                     </div>
#                                     <div>
#                                         <div class="label">✓ Translated</div>
#                                         <div class="text translated"></div>
#                                     </div>
#                                 `;
#                                 const origEl = chunkDiv.querySelector('.text.original');
#                                 const transEl = chunkDiv.querySelector('.text.translated');
#                                 if (origEl) origEl.textContent = data.original || '';
#                                 if (transEl) transEl.textContent = translatedText || '';
#                                 liveContent.insertBefore(chunkDiv, liveContent.firstChild);
#                             }
#                         }
#                     }
#                 } catch (e) {
#                     console.error('Parse error:', e, 'Event data:', event.data);
#                 }
#             };
#         }

#         // FORCE START recognition with retry logic
#         function forceStartRecognition() {
#             if (!isListening) return;
            
#             try {
#                 recognition.start();
#                 console.log('✅ Recognition started successfully');
#                 status.textContent = '⚡ ALWAYS LISTENING';
#                 status.className = 'status listening';
#                 lastActivityTime = Date.now();
#             } catch (e) {
#                 if (e.name === 'InvalidStateError') {
#                     console.log('⚠️ Already running, ignoring...');
#                 } else {
#                     console.error('❌ Start error:', e);
#                     // Try to stop and restart
#                     try {
#                         recognition.stop();
#                     } catch(stopErr) {}
                    
#                     setTimeout(() => {
#                         if (isListening) {
#                             console.log('🔄 Retrying start...');
#                             forceStartRecognition();
#                         }
#                     }, 200);
#                 }
#             }
#         }

#         if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
#             recognition = new (window.webkitSpeechRecognition || window.SpeechRecognition)();
#             recognition.continuous = true;
#             recognition.interimResults = true;
#             recognition.lang = 'en-US';
#             recognition.maxAlternatives = 1;
#         } else {
#             alert('Speech API not supported. Use Chrome/Edge!');
#         }

#         recognition.onresult = function(event) {
#             lastActivityTime = Date.now();
#             let interimTranscript = '';
#             let finalTranscript = '';
            
#             for (let i = event.resultIndex; i < event.results.length; i++) {
#                 const transcript = event.results[i][0].transcript;
#                 if (event.results[i].isFinal) {
#                     finalTranscript += transcript + ' ';
#                     sendForTranslation(transcript, false);
#                 } else {
#                     interimTranscript += transcript;
#                 }
#             }
            
#             currentTranscript = finalTranscript + interimTranscript;
#             liveTranscript.textContent = currentTranscript || 'Speak anytime...';
            
#             if (interimTranscript) {
#                 liveTranscript.className = 'live-transcript interim';
#                 debouncedSendInterim(interimTranscript);
#             } else if (finalTranscript) {
#                 liveTranscript.className = 'live-transcript';
#             }
#         };

#         const debouncedSendInterim = debounce(function(text) {
#             sendForTranslation(text, true);
#         }, 200);

#         recognition.onerror = function(event) {
#             console.error('❌ Recognition error:', event.error, 'Message:', event.message);
            
#             // Ignore harmless errors
#             if (event.error === 'no-speech' || event.error === 'aborted') {
#                 console.log('ℹ️ Harmless error, continuing...');
#                 lastActivityTime = Date.now();
#                 return;
#             }
            
#             if (event.error === 'network') {
#                 console.warn('⚠️ Network error, will force restart...');
#             }
            
#             if (event.error === 'audio-capture') {
#                 console.error('🎤 Mic access issue!');
#                 status.textContent = '⚠️ MIC ISSUE';
#                 status.className = 'status stopped';
#                 return;
#             }
            
#             // AGGRESSIVE restart for any other error
#             if (isListening) {
#                 restartAttempts++;
#                 restartCountEl.textContent = restartAttempts;
#                 status.textContent = '🔄 AUTO-RESTARTING';
#                 status.className = 'status restarting';
                
#                 setTimeout(() => {
#                     if (isListening) {
#                         console.log('🔄 Restarting after error:', event.error);
#                         forceStartRecognition();
#                     }
#                 }, 50);
#             }
#         };

#         recognition.onend = function() {
#             console.log('⚠️ Recognition ended - RESTARTING IMMEDIATELY');
            
#             if (isListening) {
#                 restartAttempts++;
#                 restartCountEl.textContent = restartAttempts;
#                 status.textContent = '🔄 AUTO-RESTARTING';
#                 status.className = 'status restarting';
                
#                 // INSTANT restart - NO DELAY
#                 setTimeout(() => {
#                     if (isListening) {
#                         forceStartRecognition();
#                     }
#                 }, 10); // 10ms - virtually instant
#             } else {
#                 status.textContent = 'STOPPED';
#                 status.className = 'status stopped';
#                 startBtn.disabled = false;
#                 stopBtn.disabled = true;
#             }
#         };

#         recognition.onstart = function() {
#             console.log('✅ Recognition active');
#             lastActivityTime = Date.now();
#         };

#         function sendForTranslation(text, isInterim = false) {
#             if (!text.trim() || !websocket || websocket.readyState !== WebSocket.OPEN) return;
#             try {
#                 websocket.send(JSON.stringify({
#                     text: text.trim(),
#                     target: targetLang.value,
#                     is_interim: isInterim
#                 }));
#             } catch (error) {
#                 console.error('Send error:', error);
#             }
#         }

#         // PRIMARY WATCHDOG: Check every 1 second
#         function startPrimaryWatchdog() {
#             primaryWatchdog = setInterval(() => {
#                 if (!isListening) return;
                
#                 // Force restart if inactive for 3 seconds
#                 if (Date.now() - lastActivityTime > 3000) {
#                     console.log('🐕 Primary watchdog: No activity, forcing restart...');
#                     try {
#                         recognition.stop();
#                     } catch(e) {}
#                     forceStartRecognition();
#                     lastActivityTime = Date.now();
#                 }
#             }, 1000);
#         }

#         // SECONDARY WATCHDOG: More aggressive, every 2 seconds
#         function startSecondaryWatchdog() {
#             secondaryWatchdog = setInterval(() => {
#                 if (!isListening) return;
                
#                 // Double-check mic is actually running
#                 console.log('🐕 Secondary watchdog: Health check...');
                
#                 // If no activity for 5 seconds, emergency restart
#                 if (Date.now() - lastActivityTime > 5000) {
#                     console.warn('🐕 Secondary watchdog: EMERGENCY RESTART!');
#                     restartAttempts++;
#                     restartCountEl.textContent = restartAttempts;
#                     try {
#                         recognition.abort();
#                     } catch(e) {}
#                     setTimeout(() => {
#                         if (isListening) forceStartRecognition();
#                     }, 100);
#                     lastActivityTime = Date.now();
#                 }
#             }, 2000);
#         }

#         // EMERGENCY WATCHDOG: Nuclear option, every 10 seconds
#         function startEmergencyWatchdog() {
#             emergencyWatchdog = setInterval(() => {
#                 if (!isListening) return;
                
#                 // If system is completely dead (no activity for 10s), nuclear restart
#                 if (Date.now() - lastActivityTime > 10000) {
#                     console.error('🐕 EMERGENCY WATCHDOG: NUCLEAR RESTART!');
#                     restartAttempts++;
#                     restartCountEl.textContent = restartAttempts;
                    
#                     // Full reset
#                     try {
#                         recognition.abort();
#                         recognition.stop();
#                     } catch(e) {}
                    
#                     setTimeout(() => {
#                         if (isListening) {
#                             // Create fresh recognition instance
#                             recognition = new (window.webkitSpeechRecognition || window.SpeechRecognition)();
#                             recognition.continuous = true;
#                             recognition.interimResults = true;
#                             recognition.lang = 'en-US';
#                             recognition.maxAlternatives = 1;
#                             setupRecognitionHandlers();
#                             forceStartRecognition();
#                         }
#                     }, 500);
#                     lastActivityTime = Date.now();
#                 }
#             }, 10000);
#         }

#         function setupRecognitionHandlers() {
#             recognition.onresult = recognition.onresult;
#             recognition.onerror = recognition.onerror;
#             recognition.onend = recognition.onend;
#             recognition.onstart = recognition.onstart;
#         }

#         // Uptime counter
#         function startUptimeCounter() {
#             setInterval(() => {
#                 if (isListening && startTime) {
#                     const seconds = Math.floor((Date.now() - startTime) / 1000);
#                     uptimeEl.textContent = seconds + 's';
#                 }
#             }, 1000);
#         }

#         startBtn.addEventListener('click', function() {
#             isListening = true;
#             restartAttempts = 0;
#             startTime = Date.now();
#             lastActivityTime = Date.now();
            
#             connectWebSocket();
#             forceStartRecognition();
            
#             // Start ALL watchdogs
#             startPrimaryWatchdog();
#             startSecondaryWatchdog();
#             startEmergencyWatchdog();
            
#             startBtn.disabled = true;
#             stopBtn.disabled = false;
#             liveContent.innerHTML = '';
#             liveTranscript.textContent = 'Speak anytime...';
#             translationCount = 0;
#             totalLatency = 0;
#             transCount.textContent = '0';
#             avgSpeed.textContent = '0ms';
#             restartCountEl.textContent = '0';
#         });

#         stopBtn.addEventListener('click', function() {
#             isListening = false;
            
#             // Stop ALL watchdogs
#             clearInterval(primaryWatchdog);
#             clearInterval(secondaryWatchdog);
#             clearInterval(emergencyWatchdog);
            
#             try {
#                 recognition.stop();
#             } catch (e) {
#                 console.log('Stop error:', e);
#             }
#             if (websocket) {
#                 websocket.close();
#             }
#             status.textContent = 'STOPPED';
#             status.className = 'status stopped';
#             startBtn.disabled = false;
#             stopBtn.disabled = true;
#         });

#         // Connect on load
#         connectWebSocket();
#         startUptimeCounter();
#     </script>
# </body>
# </html>
#     """

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)



from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import json
import asyncio
import uvicorn


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Global variable for dynamic translation URL
TRANSLATION_API_URL = "http://[::]:5000/translate" # Default
class UrlRequest(BaseModel):
    url: str
class TranslationRequest(BaseModel):
    text: str
    target: str = "ur"
    is_interim: bool = False
@app.post("/set_url")
async def set_translation_url(req: UrlRequest):
    """Set the translation API URL dynamically"""
    global TRANSLATION_API_URL
    TRANSLATION_API_URL = req.url
    return {"status": "URL set successfully", "url": TRANSLATION_API_URL}
@app.post("/test_url")
async def test_translation_url(req: UrlRequest):
    """Test connection to the translation API"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as http_client:
            response = await http_client.post(
                req.url,
                json={
                    "q": "test",
                    "source": "auto",
                    "target": "en",
                    "format": "text",
                    "alternatives": 1,
                    "api_key": ""
                },
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                return {"status": "connected", "response": response.json()}
            else:
                return {"status": "error", "message": f"Status {response.status_code}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
async def send_to_translation_api(text: str, target_lang: str):
    """Ultra-fast translation with minimal timeout"""
    try:
        async with httpx.AsyncClient(timeout=2.0) as http_client:
            response = await http_client.post(
                TRANSLATION_API_URL,
                json={
                    "q": text,
                    "source": "auto",
                    "target": target_lang,
                    "format": "text",
                    "alternatives": 1,
                    "api_key": ""
                },
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"API status {response.status_code}"}
    except Exception as e:
        return {"error": f"API error: {str(e)}"}
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for continuous audio stream processing"""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            try:
                req = TranslationRequest(**json.loads(data))
                translation_response = await send_to_translation_api(req.text, req.target)
                await websocket.send_text(json.dumps({
                    'type': 'translation_chunk',
                    'original': req.text,
                    'translation': translation_response,
                    'is_interim': req.is_interim
                }))
            except Exception as e:
                await websocket.send_text(json.dumps({
                    'type': 'error',
                    'message': str(e)
                }))
    except WebSocketDisconnect:
        print("WebSocket disconnected")
@app.get("/", response_class=HTMLResponse)
async def home():
    """Config page + NEVER-STOP listening with triple-redundant restart mechanisms"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚡ NEVER-STOP Translation - Always Active</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0a0e27;
            color: #e2e8f0;
            padding: 20px;
            line-height: 1.6;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        h1 {
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            background: linear-gradient(135deg, #00ff87 0%, #60efff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 0 30px rgba(0, 255, 135, 0.3);
        }
        .config-section {
            background: linear-gradient(135deg, #1a1f3a 0%, #0f1423 100%);
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 20px;
            border: 2px solid #00ff8750;
            box-shadow: 0 8px 32px rgba(0, 255, 135, 0.1);
        }
        .config-section.hidden {
            display: none;
        }
        .running-section {
            display: none;
        }
        .running-section.active {
            display: block;
        }
        .controls {
            display: flex;
            gap: 15px;
            margin-top: 15px;
            align-items: center;
            flex-wrap: wrap;
        }
        input[type="url"] {
            padding: 14px 24px;
            background: #0a0e27;
            border: 2px solid #00ff8750;
            border-radius: 10px;
            color: #00ff87;
            font-size: 16px;
            flex: 1;
            min-width: 300px;
        }
        input[type="url"]:focus {
            border-color: #00ff87;
            outline: none;
            box-shadow: 0 0 20px rgba(0, 255, 135, 0.3);
        }
        select {
            padding: 14px 24px;
            background: #0a0e27;
            border: 2px solid #00ff8750;
            border-radius: 10px;
            color: #00ff87;
            font-size: 16px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s;
        }
        select:hover {
            border-color: #00ff87;
            box-shadow: 0 0 20px rgba(0, 255, 135, 0.3);
        }
        button {
            padding: 14px 32px;
            background: linear-gradient(135deg, #00ff87 0%, #60efff 100%);
            color: #0a0e27;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(0, 255, 135, 0.4);
        }
        button:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 6px 25px rgba(0, 255, 135, 0.6);
        }
        button:disabled {
            opacity: 0.3;
            cursor: not-allowed;
        }
        button:active:not(:disabled) {
            transform: translateY(0);
        }
        .status {
            padding: 10px 20px;
            border-radius: 25px;
            font-size: 14px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .status.listening {
            background: linear-gradient(135deg, #00ff87 0%, #00cc6a 100%);
            color: #0a0e27;
            animation: pulse 2s ease-in-out infinite;
        }
        .status.stopped {
            background: #ff4444;
            color: white;
        }
        .status.connected {
            background: #60efff;
            color: #0a0e27;
        }
        .status.restarting {
            background: #ffa500;
            color: white;
            animation: blink 0.5s infinite;
        }
        .status.testing {
            background: #60efff;
            color: #0a0e27;
        }
        .status.error {
            background: #ff4444;
            color: white;
        }
        @keyframes pulse {
            0%, 100% { box-shadow: 0 0 0 0 rgba(0, 255, 135, 0.7); }
            50% { box-shadow: 0 0 0 15px rgba(0, 255, 135, 0); }
        }
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .section {
            background: linear-gradient(135deg, #1a1f3a 0%, #0f1423 100%);
            border-radius: 16px;
            padding: 25px;
            margin-bottom: 20px;
            border: 2px solid #00ff8730;
            box-shadow: 0 8px 32px rgba(0, 255, 135, 0.05);
        }
        .section h2 {
            color: #00ff87;
            margin-bottom: 15px;
            font-size: 1.5em;
            display: flex;
            align-items: center;
            gap: 10px;
            text-shadow: 0 0 10px rgba(0, 255, 135, 0.5);
        }
        .content {
            background: #0a0e27;
            padding: 20px;
            border-radius: 12px;
            min-height: 150px;
            font-size: 16px;
            white-space: pre-wrap;
            word-wrap: break-word;
            border: 1px solid #00ff8730;
            overflow-y: auto;
            max-height: 400px;
        }
        .live-transcript {
            background: #0a0e27;
            padding: 20px;
            border-radius: 12px;
            min-height: 100px;
            font-size: 22px;
            white-space: pre-wrap;
            word-wrap: break-word;
            border: 2px solid #00ff8750;
            margin-bottom: 10px;
            color: #60efff;
            font-weight: 500;
            box-shadow: inset 0 0 20px rgba(96, 239, 255, 0.1);
        }
        .live-transcript.interim {
            color: #00ff87;
            font-style: italic;
            animation: glow 1.5s ease-in-out infinite;
        }
        @keyframes glow {
            0%, 100% { text-shadow: 0 0 5px rgba(0, 255, 135, 0.5); }
            50% { text-shadow: 0 0 20px rgba(0, 255, 135, 0.8); }
        }
        .translated-stream {
            background: #0a0e27;
            padding: 20px;
            border-radius: 12px;
            min-height: 100px;
            font-size: 22px;
            white-space: pre-wrap;
            word-wrap: break-word;
            border: 2px solid #00ff8750;
            color: #00ff87;
            font-weight: 500;
            box-shadow: inset 0 0 20px rgba(0, 255, 135, 0.1);
            line-height: 1.6;
        }
        .info {
            color: #60efff;
            font-style: italic;
            padding: 15px;
            background: rgba(96, 239, 255, 0.1);
            border-radius: 10px;
            margin: 15px 0;
            border-left: 4px solid #60efff;
            font-weight: 500;
        }
        #micIcon {
            font-size: 32px;
            animation: float 3s ease-in-out infinite;
        }
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 15px;
            margin-top: 15px;
            font-size: 13px;
        }
        .stat {
            background: rgba(0, 255, 135, 0.1);
            padding: 12px 16px;
            border-radius: 8px;
            border: 1px solid #00ff8730;
            text-align: center;
        }
        .stat-label {
            font-size: 11px;
            color: #60efff;
            margin-bottom: 5px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .stat-value {
            color: #00ff87;
            font-weight: 700;
            font-size: 20px;
        }
        .error-message {
            color: #ff4444;
            background: rgba(255, 68, 68, 0.1);
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #ff4444;
            margin: 10px 0;
        }
        .checkbox-container {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-top: 10px;
        }
        input[type="checkbox"] {
            width: 18px;
            height: 18px;
            accent-color: #00ff87;
        }
        label {
            color: #00ff87;
            font-weight: 500;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ NEVER-STOP TRANSLATION - ALWAYS LISTENING</h1>
       
        <!-- Config Section -->
        <div id="configSection" class="config-section">
            <h2>🔧 Configuration</h2>
            <div class="controls">
                <input type="url" id="translationUrl" placeholder="Enter Translation API URL (e.g., http://localhost:5000/translate)" value="http://[::]:5000/translate">
                <select id="targetLang">
                    <option value="hi">Hindi (हिन्दी)</option>
                    <option value="en">English</option>
                    <option value="ur">Urdu (اردو)</option>
                    <option value="ar">Arabic (العربية)</option>
                    <option value="es">Spanish (Español)</option>
                    <option value="fr">French (Français)</option>
                    <option value="de">German (Deutsch)</option>
                    <option value="ja">Japanese (日本語)</option>
                    <option value="zh">Chinese (中文)</option>
                </select>
                <div class="checkbox-container">
                    <input type="checkbox" id="enableInterimTranslation" checked>
                    <label for="enableInterimTranslation">Enable Live Interim Translations (slower but more responsive)</label>
                </div>
                <button id="submitBtn">SUBMIT & START</button>
            </div>
            <div id="errorMessage" class="error-message" style="display: none;"></div>
            <div class="info">Enter your translation API URL, select target language, and submit to test connection & start forever listening! Translations optimized for speed: only finals by default.</div>
        </div>
        <!-- Running Section -->
        <div id="runningSection" class="running-section">
            <div class="input-section">
                <div class="controls">
                    <span id="micIcon">🎙️</span>
                    <button id="startBtn">START FOREVER LISTENING</button>
                    <button id="stopBtn" disabled>STOP</button>
                    <span id="status" class="status stopped">READY</span>
                    <span id="wsStatus"></span>
                </div>
                <div class="stats">
                    <div class="stat">
                        <div class="stat-label">Translations</div>
                        <div class="stat-value" id="transCount">0</div>
                    </div>
                    <div class="stat">
                        <div class="stat-label">Avg Speed</div>
                        <div class="stat-value" id="avgSpeed">0ms</div>
                    </div>
                    <div class="stat">
                        <div class="stat-label">Restarts</div>
                        <div class="stat-value" id="restartCount">0</div>
                    </div>
                    <div class="stat">
                        <div class="stat-label">Uptime</div>
                        <div class="stat-value" id="uptime">0s</div>
                    </div>
                </div>
                <div class="info">🔥 NEVER-STOP MODE: Multiple watchdogs ensure mic NEVER closes. Pause 10 seconds? Still listening. Network error? Auto-restart. Browser limit? We handle it. SPEAK ANYTIME!</div>
            </div>
            <div class="section">
                <h2>🔴 LIVE TRANSCRIPT (Always Active)</h2>
                <div id="liveTranscript" class="live-transcript">Ready to listen forever...</div>
            </div>
            <div class="section">
                <h2>🌐 INSTANT TRANSLATIONS (Streaming)</h2>
                <div id="translatedStream" class="translated-stream">Translation stream will appear here...</div>
            </div>
        </div>
    </div>
    <script>
        let recognition;
        let websocket;
        let translationCount = 0;
        let finalTranscript = '';
        let interimTranscript = '';
        let finalTranslated = '';
        let interimTranslated = '';
        let isListening = false;
        let restartAttempts = 0;
        let totalLatency = 0;
        let startTime = 0;
        let lastActivityTime = 0;
        let translationUrl = '';
        let targetLanguage = '';
        let enableInterimTranslation = true;
      
        const configSection = document.getElementById('configSection');
        const runningSection = document.getElementById('runningSection');
        const submitBtn = document.getElementById('submitBtn');
        const translationUrlInput = document.getElementById('translationUrl');
        const targetLang = document.getElementById('targetLang');
        const enableInterimCheckbox = document.getElementById('enableInterimTranslation');
        const errorMessage = document.getElementById('errorMessage');
        const startBtn = document.getElementById('startBtn');
        const stopBtn = document.getElementById('stopBtn');
        const status = document.getElementById('status');
        const wsStatus = document.getElementById('wsStatus');
        const liveTranscript = document.getElementById('liveTranscript');
        const translatedStream = document.getElementById('translatedStream');
        const transCount = document.getElementById('transCount');
        const avgSpeed = document.getElementById('avgSpeed');
        const restartCountEl = document.getElementById('restartCount');
        const uptimeEl = document.getElementById('uptime');
      
        // Submit config
        submitBtn.addEventListener('click', async function() {
            translationUrl = translationUrlInput.value.trim();
            targetLanguage = targetLang.value;
            enableInterimTranslation = enableInterimCheckbox.checked;
          
            if (!translationUrl) {
                showError('Please enter a valid Translation API URL');
                return;
            }
          
            status.textContent = 'Testing connection...';
            status.className = 'status testing';
          
            try {
                const response = await fetch('/test_url', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: translationUrl })
                });
                const result = await response.json();
              
                if (result.status === 'connected') {
                    // Set URL on backend
                    await fetch('/set_url', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ url: translationUrl })
                    });
                  
                    // Hide config, show running
                    configSection.classList.add('hidden');
                    runningSection.classList.add('active');
                    status.textContent = 'Connected & Ready!';
                    status.className = 'status connected';
                } else {
                    showError(result.message || 'Connection failed');
                }
            } catch (e) {
                showError('Failed to test connection: ' + e.message);
            }
        });
      
        function showError(msg) {
            errorMessage.textContent = msg;
            errorMessage.style.display = 'block';
            status.textContent = 'Error';
            status.className = 'status error';
        }
      
        // TRIPLE WATCHDOG SYSTEM for bulletproof operation (less aggressive for speed)
        let primaryWatchdog = null;
        let secondaryWatchdog = null;
        let emergencyWatchdog = null;
      
        function debounce(func, delay) {
            let timeoutId;
            return function(...args) {
                clearTimeout(timeoutId);
                timeoutId = setTimeout(() => func.apply(this, args), delay);
            };
        }
      
        function connectWebSocket() {
            if (websocket && websocket.readyState === WebSocket.OPEN) return;
            websocket = new WebSocket('ws://' + window.location.host + '/ws');
          
            websocket.onopen = function() {
                wsStatus.textContent = '⚡ WS CONNECTED';
                wsStatus.className = 'status connected';
            };
          
            websocket.onclose = function() {
                wsStatus.textContent = '🔄 WS RECONNECTING...';
                wsStatus.className = 'status stopped';
                setTimeout(connectWebSocket, 300);
            };
          
            websocket.onerror = function(error) {
                console.error('WS error:', error);
            };
          
            websocket.onmessage = function(event) {
                const msgStartTime = performance.now();
                try {
                    const data = JSON.parse(event.data);
                    if (data.type === 'translation_chunk') {
                        translationCount++;
                        transCount.textContent = translationCount;
                      
                        const latency = performance.now() - msgStartTime;
                        totalLatency += latency;
                        avgSpeed.textContent = Math.round(totalLatency / translationCount) + 'ms';
                      
                        let translatedChunk = '';
                        if (data.translation) {
                            if (typeof data.translation === 'string') {
                                translatedChunk = data.translation;
                            } else if (data.translation.translatedText) {
                                translatedChunk = data.translation.translatedText;
                            } else if (Array.isArray(data.translation) && data.translation[0]) {
                                translatedChunk = data.translation[0].text || data.translation[0];
                            } else if (data.translation.text) {
                                translatedChunk = data.translation.text;
                            } else if (data.translation.error) {
                                translatedChunk = `⚠️ ${data.translation.error}`;
                            }
                        }
                      
                        if (!translatedChunk || translatedChunk.trim() === '') {
                            translatedChunk = `⚠️ Translating... (${data.original.substring(0, 30)}...)`;
                            console.warn('Translation format:', data.translation);
                        }
                      
                        if (data.is_interim && enableInterimTranslation) {
                            // Replace (don't append) interim translation
                            interimTranslated = translatedChunk + ' ';
                        } else {
                            // Append to permanent (for both final and non-interim)
                            finalTranslated += translatedChunk + ' ';
                            // Clear interim when final arrives
                            interimTranslated = '';
                        }
                      
                        // Display: finals + current interim
                        const displayTranslated = finalTranslated + interimTranslated;
                        translatedStream.textContent = displayTranslated.trim();
                        translatedStream.scrollTop = translatedStream.scrollHeight;
                    }
                } catch (e) {
                    console.error('Parse error:', e, 'Event data:', event.data);
                }
            };
        }
      
        // FORCE START recognition with retry logic
        function forceStartRecognition() {
            if (!isListening) return;
          
            try {
                recognition.start();
                console.log('✅ Recognition started successfully');
                status.textContent = '⚡ ALWAYS LISTENING';
                status.className = 'status listening';
                lastActivityTime = Date.now();
            } catch (e) {
                if (e.name === 'InvalidStateError') {
                    console.log('⚠️ Already running, ignoring...');
                } else {
                    console.error('❌ Start error:', e);
                    // Try to stop and restart
                    try {
                        recognition.stop();
                    } catch(stopErr) {}
                  
                    setTimeout(() => {
                        if (isListening) {
                            console.log('🔄 Retrying start...');
                            forceStartRecognition();
                        }
                    }, 200);
                }
            }
        }
      
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            recognition = new (window.webkitSpeechRecognition || window.SpeechRecognition)();
            recognition.continuous = true;
            recognition.interimResults = true;
            recognition.lang = 'en-US';
            recognition.maxAlternatives = 1;
        } else {
            alert('Speech API not supported. Use Chrome/Edge!');
        }
      
        recognition.onresult = function(event) {
            lastActivityTime = Date.now();
          
            // Process only NEW results (from resultIndex)
            for (let i = event.resultIndex; i < event.results.length; i++) {
                if (event.results[i].isFinal) {
                    // Append to permanent final transcript
                    finalTranscript += event.results[i][0].transcript + ' ';
                    // Send this final chunk for translation
                    sendForTranslation(event.results[i][0].transcript, false);
                    // Clear any pending interim (it's now final)
                    interimTranscript = '';
                }
            }
          
            // Handle current interim (last result, if not final)
            if (event.results.length > 0 && !event.results[event.results.length - 1].isFinal) {
                interimTranscript = event.results[event.results.length - 1][0].transcript;
                // Debounce-send the current interim for live translation preview ONLY if enabled
                if (enableInterimTranslation) {
                    debouncedSendInterim(interimTranscript);
                }
            }
          
            // Display: finals + current interim (overwrites previous interim)
            const displayText = finalTranscript + interimTranscript;
            liveTranscript.textContent = displayText || 'Speak anytime...';
            liveTranscript.scrollTop = liveTranscript.scrollHeight;
          
            // Style interim glow
            if (interimTranscript) {
                liveTranscript.className = 'live-transcript interim';
            } else {
                liveTranscript.className = 'live-transcript';
            }
        };
      
        const debouncedSendInterim = debounce(function(text) {
            sendForTranslation(text, true);
        }, 100);  // Reduced to 100ms for snappier response
      
        recognition.onerror = function(event) {
            console.error('❌ Recognition error:', event.error, 'Message:', event.message);
          
            // Ignore harmless errors
            if (event.error === 'no-speech' || event.error === 'aborted') {
                console.log('ℹ️ Harmless error, continuing...');
                lastActivityTime = Date.now();
                return;
            }
          
            if (event.error === 'network') {
                console.warn('⚠️ Network error, will force restart...');
            }
          
            if (event.error === 'audio-capture') {
                console.error('🎤 Mic access issue!');
                status.textContent = '⚠️ MIC ISSUE';
                status.className = 'status stopped';
                return;
            }
          
            // AGGRESSIVE restart for any other error
            if (isListening) {
                restartAttempts++;
                restartCountEl.textContent = restartAttempts;
                status.textContent = '🔄 AUTO-RESTARTING';
                status.className = 'status restarting';
              
                setTimeout(() => {
                    if (isListening) {
                        console.log('🔄 Restarting after error:', event.error);
                        forceStartRecognition();
                    }
                }, 50);
            }
        };
      
        recognition.onend = function() {
            console.log('⚠️ Recognition ended - RESTARTING IMMEDIATELY');
          
            if (isListening) {
                restartAttempts++;
                restartCountEl.textContent = restartAttempts;
                status.textContent = '🔄 AUTO-RESTARTING';
                status.className = 'status restarting';
              
                // INSTANT restart - NO DELAY
                setTimeout(() => {
                    if (isListening) {
                        forceStartRecognition();
                    }
                }, 10); // 10ms - virtually instant
            } else {
                status.textContent = 'STOPPED';
                status.className = 'status stopped';
                startBtn.disabled = false;
                stopBtn.disabled = true;
            }
        };
      
        recognition.onstart = function() {
            console.log('✅ Recognition active');
            lastActivityTime = Date.now();
        };
      
        function sendForTranslation(text, isInterim = false) {
            if (!text.trim() || !websocket || websocket.readyState !== WebSocket.OPEN) return;
            try {
                websocket.send(JSON.stringify({
                    text: text.trim(),
                    target: targetLanguage,
                    is_interim: isInterim
                }));
            } catch (error) {
                console.error('Send error:', error);
            }
        }
      
        // PRIMARY WATCHDOG: Check every 2 seconds (less aggressive)
        function startPrimaryWatchdog() {
            primaryWatchdog = setInterval(() => {
                if (!isListening) return;
              
                // Force restart if inactive for 5 seconds
                if (Date.now() - lastActivityTime > 5000) {
                    console.log('🐕 Primary watchdog: No activity, forcing restart...');
                    try {
                        recognition.stop();
                    } catch(e) {}
                    forceStartRecognition();
                    lastActivityTime = Date.now();
                }
            }, 2000);
        }
      
        // SECONDARY WATCHDOG: Every 5 seconds
        function startSecondaryWatchdog() {
            secondaryWatchdog = setInterval(() => {
                if (!isListening) return;
              
                // If no activity for 10 seconds, emergency restart
                if (Date.now() - lastActivityTime > 10000) {
                    console.warn('🐕 Secondary watchdog: EMERGENCY RESTART!');
                    restartAttempts++;
                    restartCountEl.textContent = restartAttempts;
                    try {
                        recognition.abort();
                    } catch(e) {}
                    setTimeout(() => {
                        if (isListening) forceStartRecognition();
                    }, 100);
                    lastActivityTime = Date.now();
                }
            }, 5000);
        }
      
        // EMERGENCY WATCHDOG: Every 15 seconds
        function startEmergencyWatchdog() {
            emergencyWatchdog = setInterval(() => {
                if (!isListening) return;
              
                // If system is completely dead (no activity for 20s), nuclear restart
                if (Date.now() - lastActivityTime > 20000) {
                    console.error('🐕 EMERGENCY WATCHDOG: NUCLEAR RESTART!');
                    restartAttempts++;
                    restartCountEl.textContent = restartAttempts;
                  
                    // Full reset
                    try {
                        recognition.abort();
                        recognition.stop();
                    } catch(e) {}
                  
                    setTimeout(() => {
                        if (isListening) {
                            // Create fresh recognition instance
                            recognition = new (window.webkitSpeechRecognition || window.SpeechRecognition)();
                            recognition.continuous = true;
                            recognition.interimResults = true;
                            recognition.lang = 'en-US';
                            recognition.maxAlternatives = 1;
                            setupRecognitionHandlers();
                            forceStartRecognition();
                        }
                    }, 500);
                    lastActivityTime = Date.now();
                }
            }, 15000);
        }
      
        function setupRecognitionHandlers() {
            // Re-attach handlers
            recognition.onresult = recognition.onresult;
            recognition.onerror = recognition.onerror;
            recognition.onend = recognition.onend;
            recognition.onstart = recognition.onstart;
        }
      
        // Uptime counter
        function startUptimeCounter() {
            setInterval(() => {
                if (isListening && startTime) {
                    const seconds = Math.floor((Date.now() - startTime) / 1000);
                    uptimeEl.textContent = seconds + 's';
                }
            }, 1000);
        }
      
        startBtn.addEventListener('click', function() {
            isListening = true;
            restartAttempts = 0;
            startTime = Date.now();
            lastActivityTime = Date.now();
          
            finalTranscript = '';
            interimTranscript = '';
            finalTranslated = '';
            interimTranslated = '';
            liveTranscript.textContent = 'Speak anytime...';
            translatedStream.textContent = 'Translation stream will appear here...';
          
            connectWebSocket();
            forceStartRecognition();
          
            // Start ALL watchdogs
            startPrimaryWatchdog();
            startSecondaryWatchdog();
            startEmergencyWatchdog();
          
            startUptimeCounter();
          
            startBtn.disabled = true;
            stopBtn.disabled = false;
            translationCount = 0;
            totalLatency = 0;
            transCount.textContent = '0';
            avgSpeed.textContent = '0ms';
            restartCountEl.textContent = '0';
        });
      
        stopBtn.addEventListener('click', function() {
            isListening = false;
          
            // Stop ALL watchdogs
            clearInterval(primaryWatchdog);
            clearInterval(secondaryWatchdog);
            clearInterval(emergencyWatchdog);
          
            try {
                recognition.stop();
            } catch (e) {
                console.log('Stop error:', e);
            }
            if (websocket) {
                websocket.close();
            }
            finalTranscript = '';
            interimTranscript = '';
            finalTranslated = '';
            interimTranslated = '';
            status.textContent = 'STOPPED';
            status.className = 'status stopped';
            startBtn.disabled = false;
            stopBtn.disabled = true;
        });
      
        // Connect on load (for WS readiness)
        connectWebSocket();
    </script>
</body>
</html>
    """
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)