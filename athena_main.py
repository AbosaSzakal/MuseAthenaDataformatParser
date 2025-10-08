import asyncio
import time
from collections import defaultdict

from athena_packet_decoder import packetParser as athena_parse_packet
from graph_helper import GraphHelper
from athena_connection import AthenaConnection, connect_and_stream
from muse_discovery import find_muse_devices

# Console formatting helpers
LINE = "=" * 64

# Athena parser central stats (per-second aggregator)
# We aggregate SAMPLES per packet type so Hz reflects sample rate.
athena_central_stats = defaultdict(int)
athena_last_print = 0.0

# Initialize graph helper for real-time plotting
graph_helper = GraphHelper()


def _maybe_print_athena_stats(now: float):
    """Print aggregated Athena stats once per ~1s with Hz estimates, then reset."""
    global athena_last_print, athena_central_stats
    if athena_last_print == 0.0:
        athena_last_print = now
        return

    dt = now - athena_last_print
    if dt < 1.0:
        return

    if athena_central_stats:
        # Build a compact line: key=count (hz)
        parts = []
        for k in sorted(athena_central_stats.keys()):
            count = athena_central_stats[k]
            hz = (count / dt) if dt > 0 else 0.0
            parts.append(f"{k}:{count} ({hz:.1f} Hz)")
        print(f"[Athena stats {dt:.2f}s] " + ", ".join(parts))

    # Reset for next window
    athena_central_stats = defaultdict(int)
    athena_last_print = now


def packet_callback(raw: bytes):
    """Per-packet callback; parse and fold Athena stats into a central per-second dict.

    The Athena packet parser now returns a dict mapping type -> { packets: int, samples: int }.
    We sum SAMPLES per type to estimate sample-rate Hz in the periodic printout.
    """
    # Parse this BLE notification with the Athena parser and aggregate counts
    stats, parsed_packets = athena_parse_packet(raw, verbose=False, collect=True)

    # Other data types that were decoded are also in parsed_packets, I just did not graph them

    # Use per-sample time derived from fixed IMU sample rate to avoid packet-timestamp aliasing
    # Each ACC and GYRO entry represents one sample at 1/IMU_FS seconds spacing.
    for packet in parsed_packets:
        for entry in packet.get('entries', []):
            entry_type = entry.get('type')
            data = entry.get('data', [])

            if entry_type == 'ACC' and len(data) == 3:
                graph_helper.add_acc_sample(data[0], data[1], data[2])

            elif entry_type == 'GYRO' and len(data) == 3:
                graph_helper.add_gyro_sample(data[0], data[1], data[2])
    
    for k, rec in stats.items():
        # Support both old (int count) and new ({packets, samples}) formats
        if isinstance(rec, dict):
            samples = int(rec.get('samples', 0))
        else:
            samples = int(rec)
        athena_central_stats[k] += samples

    # Print once per second with Hz estimates, then clear
    _maybe_print_athena_stats(time.time())
    
    
async def stream_athena():
    devices = await find_muse_devices(timeout=5.0)
    if not devices:
        print("No Muse device found. Ensure headset is on and Bluetooth is enabled.")
        return

    device = devices[0]
    print(f"Found device: {device.name} ({device.address})")

    client = AthenaConnection(verbose=False)

    client.on_packet(packet_callback)

    # Start plotting in a separate thread to avoid GUI init on the asyncio/BLE thread
    graph_helper.start_plotting()

    # Use two-phase preset sequence - this is what MindMonitor does, though it might not be needed
    # Mindmonitor might be doing this because it has a default, likely p21, and then after identifying the device, it might swithch to a better preset
    preset = 'p1045'
    initial_preset = 'p21'

    # Start streaming in background using athena_connection
    stream_task = asyncio.create_task(
        connect_and_stream(
            client,
            device.address,
            duration_seconds=0,  # 0 = stream until interrupted
            preset=preset,
            initial_preset=initial_preset
        )
    )

    # Wait for streaming to finish
    try:
        success = await stream_task
    except Exception as e:
        print(f"Error during streaming: {e}")
        success = False
    finally:
        # Signal plot thread to stop and join it
        graph_helper.stop_plotting()


if __name__ == "__main__":
    try:
        asyncio.run(stream_athena())
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting...")
