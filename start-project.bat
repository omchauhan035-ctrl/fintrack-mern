@echo off
title Start Finance Tracker Project (MERN Stack)
echo =======================================================
echo Starting Finance Tracker (Node.js/Express + React 19)
echo =======================================================

echo 1. Launching Node.js Express Backend on http://localhost:5000...
start "Finance Tracker - Node Server" cmd /k "cd /d "%~dp0server" && npm run dev"

echo 2. Launching React Vite Frontend on http://localhost:5173...
start "Finance Tracker - React Frontend" cmd /k "cd /d "%~dp0client" && npm run dev"

echo =======================================================
echo Both servers have been launched in separate windows!
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:5173
echo =======================================================
timeout /t 5 >nul
start http://localhost:5173

