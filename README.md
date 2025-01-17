# network_watchdog

This is repository for Network watchdog

## How to use

At first, you have to make sure that Target PC accepts ICMP(Ping).

### Check ICMP Rules (Windows)

1. Open Windows Settings
2. Open Windows Security
3. Open Firewall Settings
4. Check the rule of `File and Printer Sharing - ICMP Echo Request (ICMPv4-In)`
5. Activate the rule if it's invalid

And only to run this code:

```bash
python main.py 192.168.0.0
```
