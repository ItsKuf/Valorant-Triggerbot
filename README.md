# Valorant Triggerbot
This is a simple Valorant Triggerbot that detects the enemy's color and then automatically shoots for you.

# Setup:
- Change player outline to purple.
- Change secondary shoot button to "K".
- Adjust the config.json to your liking; however, the default settings are good enough.

# How To Use:
Hold down shift key to activate when playing

# Settings To Configure If You Know What You're Doing:
```
{
    "trigger_hotkey": "0xA0",       // Hex code for the trigger hotkey (0xA0 corresponds to the left Shift key)
    "base_delay": 0.01,             // Base delay in seconds before triggering
    "trigger_delay": 40,            // Percentage delay to add to the base delay
    "color_tolerance": 70,          // Tolerance for color matching
    "always_enabled": false         // If true, the triggerbot is always enabled; otherwise, it activates on hotkey press
}
```

# ⚠ USE SAFELY ⚠
## Is very bannable and gets detectd very eaily if you rage use it
