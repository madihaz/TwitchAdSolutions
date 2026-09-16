from pathlib import Path

path = Path('vaft/vaft-ublock-origin.js')
s = path.read_text()

old = """        inAdBreak: false,\n        vaftEverUnmuted: false\n    };"""
new = """        inAdBreak: false,\n        vaftEverUnmuted: false,\n        pausedAt: 0,\n        resumedAt: 0\n    };\n\n    // Do not compare the first post-resume sample with pre-pause state.\n    function resetBufferMonitorState() {\n        playerBufferState.position = 0;\n        playerBufferState.videoCurrentTime = undefined;\n        playerBufferState.bufferedPosition = 0;\n        playerBufferState.bufferDuration = 0;\n        playerBufferState.numSame = 0;\n        playerBufferState.fixAttempts = 0;\n        playerBufferState.recoveryReloadUsed = false;\n    }"""
if s.count(old) != 1:
    raise SystemExit(f'buffer state anchor count: {s.count(old)}')
s = s.replace(old, new)

old = """                            playerBufferState.userPauseIntent = true;\n                        }\n                    });\n                    video.addEventListener('play', () => {\n                        playerBufferState.userPauseIntent = false;\n                        playerBufferState.loggedPauseIntent = false;\n                    });"""
new = """                            playerBufferState.userPauseIntent = true;\n                            playerBufferState.pausedAt = Date.now();\n                            resetBufferMonitorState();\n                        }\n                    });\n                    video.addEventListener('play', () => {\n                        playerBufferState.userPauseIntent = false;\n                        playerBufferState.loggedPauseIntent = false;\n                        playerBufferState.resumedAt = Date.now();\n                        resetBufferMonitorState();\n                    });"""
if s.count(old) != 1:
    raise SystemExit(f'pause/play anchor count: {s.count(old)}')
s = s.replace(old, new)

old = """                        const playerNotActivelyPlaying = videoEl && (videoEl.readyState < 2 || videoEl.paused);"""
new = """                        const playerNotActivelyPlaying = videoEl && (videoEl.readyState < 2 || videoEl.paused);\n                        if (videoEl?.paused || player.isPaused()) {\n                            resetBufferMonitorState();\n                        }"""
if s.count(old) != 1:
    raise SystemExit(f'active-playback anchor count: {s.count(old)}')
s = s.replace(old, new)

path.write_text(s)
print(f'Updated {path}')
