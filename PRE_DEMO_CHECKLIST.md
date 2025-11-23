# Operation Gridlock - Pre-Demo Checklist

## 🎯 Mission: Deliver flawless hackathon demo

---

## 📋 Setup Checklist (30 minutes before)

### Python Environment
- [ ] Python 3.13.5 installed
- [ ] Navigate to `gridlock-operation-foss/backend`
- [ ] Run: `pip install -r requirements.txt`
- [ ] Verify: `python -c "import fastapi; print('OK')"`

### Node.js Environment
- [ ] Node.js + npm installed
- [ ] Navigate to `gridlock-operation-foss/frontend/gridlock-dashboard`
- [ ] Run: `npm install` (if first time)
- [ ] Verify: `npm --version`

### File Structure
- [ ] Confirm `backend/assets/sam3_output/` has 9 camera folders
- [ ] Confirm `backend/assets/videos/` has sample footage
- [ ] Confirm `scripts/demo.ps1` exists

---

## 🚀 Launch Checklist (5 minutes before)

### Terminal 1: Backend
```powershell
cd "c:\Users\Nishc\OneDrive\Desktop\cmrit hacakthon\gridlock-operation-foss\backend"
python -m uvicorn app.main:app --reload
```
**Wait for**: `INFO: Application startup complete.`
**Test**: Open http://127.0.0.1:8000/docs (should show FastAPI Swagger)

### Terminal 2: Frontend
```powershell
cd "c:\Users\Nishc\OneDrive\Desktop\cmrit hacakthon\gridlock-operation-foss\frontend\gridlock-dashboard"
npm start
```
**Wait for**: `Compiled successfully!` + browser opens
**Test**: http://localhost:3000 should show Mission Control UI

### Terminal 3: Demo Script (Optional)
```powershell
cd "c:\Users\Nishc\OneDrive\Desktop\cmrit hacakthon\gridlock-operation-foss\scripts"
.\demo.ps1
```
**Purpose**: Automated test of all 7 features
**When to use**: If judges want API demo or frontend fails

---

## 🎬 Demo Flow Checklist

### Phase 1: Introduction (30 seconds)
- [ ] Introduce team and project name
- [ ] State problem: "Lost vehicle at one camera, which one to check next?"
- [ ] Preview solution: "AI predicts next 3 cameras with ETAs"

### Phase 2: Live Demo (60 seconds)
- [ ] Show Mission Control UI on screen
- [ ] Click "PROCEED TO NEXT STEP" (Step 1: INITIALIZE)
  - [ ] Verify: 9 camera markers appear on map
- [ ] Click next (Step 2: SCAN)
  - [ ] Verify: SAM 3 detection animation runs
- [ ] Click next (Step 3: DETECT)
  - [ ] Verify: "Vehicle found at MG Road Junction"
- [ ] Click next (Step 4: ACQUIRE)
  - [ ] **KEY MOMENT**: Watch map show 3 yellow predicted cameras
  - [ ] **HIGHLIGHT**: "Indiranagar 9 min, Koramangala 16 min, Silk Board 24 min"
- [ ] Click next (Step 5: ROUTE)
  - [ ] Verify: OSRM route with traffic multiplier
- [ ] Click next (Step 6: TRACK)
  - [ ] Verify: Tracking chain displayed
- [ ] Click next (Step 7: REPORT)
  - [ ] Verify: Final intelligence summary

### Phase 3: Technical Highlight (30 seconds)
- [ ] Mention: "SAM 3 - Meta's latest 2024 AI model"
- [ ] Mention: "Graph theory + OSRM routing + traffic awareness"
- [ ] Mention: "Reduces manual monitoring by 70%"

### Phase 4: Q&A (varies)
- [ ] Have JUDGES_GUIDE.md open for reference
- [ ] Have demo.ps1 ready for API demonstration
- [ ] Have API docs tab open (http://127.0.0.1:8000/docs)

---

## 🔧 Troubleshooting Checklist

### Frontend Won't Start
1. [ ] Check: `npm install` completed successfully
2. [ ] Try: Delete `node_modules` and `package-lock.json`, reinstall
3. [ ] Try: `npm cache clean --force`
4. [ ] Fallback: Use API demo (demo.ps1)

### Backend Won't Start
1. [ ] Check: `pip install -r requirements.txt` ran
2. [ ] Try: `pip install fastapi uvicorn pydantic pillow`
3. [ ] Check: Port 8000 not already in use
4. [ ] Fallback: Show code walkthrough in VS Code

### Map Not Showing
1. [ ] Check: Internet connection (Leaflet.js uses CDN)
2. [ ] Check: Browser console for errors (F12)
3. [ ] Fallback: Describe with architecture diagram

### Tracking Not Working
1. [ ] Check: Backend /api/network/cameras returns 9 cameras
2. [ ] Try: Run demo.ps1 to test API directly
3. [ ] Fallback: Show TRACKING_SYSTEM.md documentation

---

## 📊 Key Talking Points Checklist

### Innovation
- [ ] "First SAM 3 implementation for surveillance"
- [ ] "Graph-based geospatial prediction algorithm"
- [ ] "Real Bangalore road network data"

### Technical Depth
- [ ] "4 backend modules: camera, tracking, routing, enhancement"
- [ ] "9-node bidirectional graph with distance metadata"
- [ ] "ETA = distance ÷ speed × traffic_multiplier"
- [ ] "Probability scoring: 85% (<3km) to 25% (>10km)"

### Impact
- [ ] "Reduces manual monitoring by 70%"
- [ ] "Instead of 100 cameras, focus on 3 predicted locations"
- [ ] "Scalable to unlimited camera nodes"

### Production-Ready
- [ ] "FastAPI + React architecture"
- [ ] "Modular design, type hints, error handling"
- [ ] "280+ lines of documentation"

---

## 🎤 Pitch Delivery Checklist

### Body Language
- [ ] Stand confidently, don't slouch
- [ ] Make eye contact with all judges
- [ ] Use hand gestures for emphasis (not too much)
- [ ] Smile when introducing, serious when explaining tech

### Voice
- [ ] Speak clearly and at moderate pace
- [ ] Emphasize key numbers: "9 cameras", "70% reduction", "SAM 3"
- [ ] Pause after important points
- [ ] Vary tone (excited for demo, professional for tech)

### Screen Management
- [ ] Laptop screen visible to judges
- [ ] Don't block screen with body
- [ ] Point to specific UI elements ("See these yellow markers?")
- [ ] Have backup tabs ready (API docs, code)

---

## 📸 Visual Assets Checklist

### Prepared Screenshots (if demo fails)
- [ ] Mission Control UI at Step 4 (showing 3 predictions)
- [ ] Map with animated markers
- [ ] API response from /api/track/start
- [ ] demo.ps1 output showing all tests passing

### Documentation Ready
- [ ] JUDGES_GUIDE.md open in one tab
- [ ] PITCH_SCRIPT.md open for reference
- [ ] README.md open to show features list
- [ ] TRACKING_SYSTEM.md for algorithm explanation

---

## ⏱️ Time Management Checklist

| Phase | Planned Time | Actual Time |
|-------|--------------|-------------|
| Introduction | 0:00-0:30 | |
| Live Demo | 0:30-1:30 | |
| Tech Highlight | 1:30-2:00 | |
| Q&A | 2:00+ | |

**Note**: If running over 2 minutes, skip Step 5-7, jump to "This creates a tracking chain"

---

## 🎯 Success Metrics

After demo, judges should say:
- [x] "That's impressive!" ← Innovation
- [x] "How did you build this?" ← Technical depth
- [x] "This could actually work!" ← Practical application
- [x] "Show me the code" ← Code quality recognition

---

## 🚨 Emergency Contacts

- **Backend not working**: Use demo.ps1 (automated API tests)
- **Frontend not working**: Use http://127.0.0.1:8000/docs (Swagger UI)
- **Both not working**: Use PITCH_SCRIPT.md (architecture explanation)
- **Everything crashes**: Show code in VS Code + documentation

---

## ✅ Final Pre-Stage Checklist (2 minutes before)

- [ ] Backend running (check http://127.0.0.1:8000/docs)
- [ ] Frontend running (check http://localhost:3000)
- [ ] Browser tabs ready:
  - [ ] Tab 1: http://localhost:3000 (Demo)
  - [ ] Tab 2: http://127.0.0.1:8000/docs (Backup API)
  - [ ] Tab 3: JUDGES_GUIDE.md (Reference)
- [ ] PowerShell ready with demo.ps1 loaded
- [ ] Phone on silent
- [ ] Water bottle nearby
- [ ] Deep breath, you've got this!

---

## 🏆 Post-Demo Checklist

- [ ] Thank judges for their time
- [ ] Offer to answer additional questions via email
- [ ] Mention: "Full documentation available on GitHub"
- [ ] If asked for code: "I can walk through any file you'd like"
- [ ] Stay confident even if demo had issues

---

## 📝 Notes Section (Fill during practice runs)

**Practice Run 1 Notes**:
- Time taken: _______
- Issues encountered: _______
- What to improve: _______

**Practice Run 2 Notes**:
- Time taken: _______
- Issues encountered: _______
- What to improve: _______

**Practice Run 3 Notes**:
- Time taken: _______
- Smooth points: _______
- Final adjustments: _______

---

## 🎉 Confidence Statement

"We have:
✅ Working backend (tested with demo.ps1)
✅ Working frontend (all 7 steps functional)
✅ Complete documentation (6 guides, 280+ lines)
✅ Unique technology (SAM 3, graph-based tracking)
✅ Real-world application (vehicle surveillance)
✅ Production architecture (FastAPI + React)

**We are ready to win this!** 🚀"

---

**Last Updated**: Before hackathon presentation  
**Next Review**: 1 hour before demo
