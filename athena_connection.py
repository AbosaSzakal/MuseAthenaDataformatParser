"""
Athena BLE connection utilities 

Provides:
- CONTROL_CHAR_UUID, SENSOR_CHAR_UUIDS, COMMANDS
- AthenaConnection: minimal state + callbacks
- connect_and_stream: connect, configure, start stream, stop
"""

# Heavy based on amused-py by Adrian Belmans
# https://github.com/Amused-EEG/amused-py


from __future__ import annotations

import asyncio
import datetime
from typing import Optional, Callable, Dict, Any

from bleak import BleakClient

# BLE UUIDs and command bytes (copied to avoid MuseStreamClient dependency)
CONTROL_CHAR_UUID = "273e0001-4c4d-454d-96be-f03bac821358"
# Preferred order: UNIVERSAL first as per known-good logs, then other data chars
SENSOR_CHAR_UUIDS = [
    "273e0013-4c4d-454d-96be-f03bac821358",  # UNIVERSAL / combined sensors
    "273e0003-4c4d-454d-96be-f03bac821358",  # EEG TP9 (fallback)
]

COMMANDS = {
    # Version / status / control
    'v4': bytes.fromhex('0376340a'),           # Version (protocol v4)
    'v6': bytes.fromhex('0376360a'),           # Version (protocol v6) - fallback
    's': bytes.fromhex('02730a'),              # Status
    'h': bytes.fromhex('02680a'),              # Halt
    # Presets
    'p21': bytes.fromhex('047032310a'),        # Basic preset
    'p1034': bytes.fromhex('0670313033340a'),  # Sleep preset
    'p1035': bytes.fromhex('0670313033350a'),  # Sleep preset 2
    'p1045': bytes.fromhex('0670313034350a'),  # Alternate preset seen in logs
    # Streaming
    'd': bytes.fromhex('02640a'),              # Start streaming (short command)
    'dc001': bytes.fromhex('0664633030310a'),  # Start streaming (extended) - fallback
    # Misc / legacy
    'L1': bytes.fromhex('034c310a'),           # L1 command (legacy/no-op on some fw)
}


class AthenaConnection:
    """
    Minimal connection state holder with basic callbacks.

    Callbacks:
    - on_packet: Callable[[bytes], None] for raw packet notifications
    """

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.client: Optional[BleakClient] = None
        self.is_streaming: bool = False
        self.packet_count: int = 0
        self.device_info: Dict[str, Any] = {}
        self._on_packet: Optional[Callable[[bytes], None]] = None

    def on_packet(self, callback: Callable[[bytes], None]):
        self._on_packet = callback

    def log(self, message: str):
        if self.verbose:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print(f"[{timestamp}] {message}")

    # Notification handlers (compatible signature with Bleak)
    def handle_control_notification(self, _sender: int, data: bytearray):
        """Parse control responses for basic info (best-effort)."""
        try:
            text = data.decode('utf-8', errors='ignore')
            if '{' in text and '}' in text:
                start = text.index('{')
                end = text.rindex('}') + 1
                json_str = text[start:end]
                import json
                info = json.loads(json_str)
                self.device_info.update(info)
                if 'fw' in info:
                    self.log(f"Firmware: {info['fw']}")
                if 'bp' in info:
                    self.log(f"Battery: {info['bp']}%")
        except Exception:
            # Ignore parse errors; control packets vary by firmware
            pass

    def handle_sensor_notification(self, _sender: int, data: bytearray):
        """Mark streaming active, count packets, and forward raw if requested."""
        self.packet_count += 1
        if not self.is_streaming:
            self.is_streaming = True
            self.log("Streaming started!")
        if self._on_packet:
            try:
                self._on_packet(bytes(data))
            except Exception as e:
                self.log(f"Packet callback error: {e}")

    def get_summary(self) -> Dict[str, Any]:
        return {
            'packets_received': self.packet_count,
            'device_info': self.device_info,
        }


async def connect_and_stream(
    connection: AthenaConnection,
    address: str,
    duration_seconds: int = 30,
    preset: str = 'p1045',
    initial_preset: Optional[str] = None,
) -> bool:
    """Connect to device, configure, and stream using AthenaConnection.

    - Uses v4 + status + halt
    - Applies warm-up preset (optional) then final preset
    - Enables sensor notifications (UNIVERSAL first)
    - Starts stream with 'd', falls back to 'dc001' if needed
    - Stops with 'h' after duration
    """
    try:
        log = connection.log
        log(f"Connecting to {address}...")

        async with BleakClient(address) as ble:
            connection.client = ble
            connection.packet_count = 0
            connection.is_streaming = False
            log("Connected!")

            # Best-effort MTU negotiation
            try:
                if hasattr(ble, 'request_mtu') and callable(getattr(ble, 'request_mtu')):
                    mtu = await ble.request_mtu(512)
                    log(f"MTU negotiated: {mtu}")
                else:
                    mtu = getattr(ble, 'mtu_size', None) or getattr(ble, 'mtu', None)
                    if mtu:
                        log(f"MTU (reported): {mtu}")
            except Exception as e:
                log(f"MTU request not supported or failed: {e}")

            # Enable control notifications and query info
            await ble.start_notify(CONTROL_CHAR_UUID, connection.handle_control_notification)
            await ble.write_gatt_char(CONTROL_CHAR_UUID, COMMANDS['v4'], response=False)
            await asyncio.sleep(0.1)
            await ble.write_gatt_char(CONTROL_CHAR_UUID, COMMANDS['s'], response=False)
            await asyncio.sleep(0.1)
            await ble.write_gatt_char(CONTROL_CHAR_UUID, COMMANDS['h'], response=False)
            await asyncio.sleep(0.1)

            # Determine first preset and apply
            first_preset = initial_preset or preset
            log(f"Setting preset: {first_preset}")
            await ble.write_gatt_char(CONTROL_CHAR_UUID, COMMANDS[first_preset], response=False)
            await asyncio.sleep(0.1)
            await ble.write_gatt_char(CONTROL_CHAR_UUID, COMMANDS['s'], response=False)
            await asyncio.sleep(0.1)

            # Enable sensor notifications (prefer UNIVERSAL UUID first)
            sensor_enabled = False
            for char_uuid in SENSOR_CHAR_UUIDS:
                try:
                    await ble.start_notify(char_uuid, connection.handle_sensor_notification)
                    sensor_enabled = True
                    log(f"Sensor notifications enabled on {char_uuid}")
                    break
                except Exception as e:
                    log(f"Failed enabling notify on {char_uuid}: {e}")
                    continue
            if not sensor_enabled:
                log("Failed to enable sensor notifications")
                return False

            # Start streaming (phase 1)
            log("Starting stream (d)...")
            try:
                await ble.write_gatt_char(CONTROL_CHAR_UUID, COMMANDS['d'], response=False)
            except Exception as e:
                log(f"Failed to start with 'd': {e}")
            await asyncio.sleep(0.15)
            if not connection.is_streaming:
                log("No data yet; trying extended start (dc001) x2...")
                try:
                    await ble.write_gatt_char(CONTROL_CHAR_UUID, COMMANDS['dc001'], response=False)
                    await asyncio.sleep(0.05)
                    await ble.write_gatt_char(CONTROL_CHAR_UUID, COMMANDS['dc001'], response=False)
                except Exception as e:
                    log(f"Failed to start with 'dc001': {e}")
            await asyncio.sleep(1.0)

            # Optional second phase: switch to final preset after warm-up
            if initial_preset and preset != first_preset:
                log("Switching to final preset sequence...")
                try:
                    await ble.write_gatt_char(CONTROL_CHAR_UUID, COMMANDS['h'], response=False)
                    await asyncio.sleep(0.1)
                except Exception as e:
                    log(f"Halt before final preset failed: {e}")
                log(f"Setting preset: {preset}")
                await ble.write_gatt_char(CONTROL_CHAR_UUID, COMMANDS[preset], response=False)
                await asyncio.sleep(0.1)
                await ble.write_gatt_char(CONTROL_CHAR_UUID, COMMANDS['s'], response=False)
                await asyncio.sleep(0.1)
                # Re-enable sensor notifications
                for char_uuid in SENSOR_CHAR_UUIDS:
                    try:
                        await ble.start_notify(char_uuid, connection.handle_sensor_notification)
                        log(f"Sensor notifications re-enabled on {char_uuid}")
                        break
                    except Exception as e:
                        log(f"Failed re-enabling notify on {char_uuid}: {e}")
                        continue
                connection.is_streaming = False
                log("Starting stream (final, d)...")
                try:
                    await ble.write_gatt_char(CONTROL_CHAR_UUID, COMMANDS['d'], response=False)
                except Exception as e:
                    log(f"Final start with 'd' failed: {e}")
                await asyncio.sleep(0.15)
                if not connection.is_streaming:
                    log("No data yet after final 'd'; trying extended start (dc001) x2...")
                    try:
                        await ble.write_gatt_char(CONTROL_CHAR_UUID, COMMANDS['dc001'], response=False)
                        await asyncio.sleep(0.05)
                        await ble.write_gatt_char(CONTROL_CHAR_UUID, COMMANDS['dc001'], response=False)
                    except Exception as e:
                        log(f"Final start with 'dc001' failed: {e}")
                await asyncio.sleep(2)

            # Final check
            if not connection.is_streaming:
                log("Streaming failed to start")
                return False

            # Stream for specified duration
            if duration_seconds > 0:
                log(f"Streaming for {duration_seconds} seconds...")
                await asyncio.sleep(duration_seconds)
            else:
                log("Streaming continuously (Ctrl+C to stop)...")
                while True:
                    await asyncio.sleep(1)

            # Stop streaming
            log("Stopping stream...")
            try:
                await ble.write_gatt_char(CONTROL_CHAR_UUID, COMMANDS['h'], response=False)
            except Exception:
                pass

            return True
    except Exception as e:
        try:
            connection.log(f"Athena connection error: {e}")
        except Exception:
            print(f"Athena connection error: {e}")
        return False
    finally:
        connection.client = None
