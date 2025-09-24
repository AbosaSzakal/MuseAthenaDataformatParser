# Muse S Athena Bluetooth protocol

This repo describes my current understanding of the Bluetooth packet format the Muse S Athena (MS-03) uses. The project this was originally for has taken a new direction, so I'm open sourcing this in hopes that someone else might find this useful for further work.

## Basic Format

```
<length in bytes><packet counter><unknown 7 bytes> <packet id byte - detailed later> <unknown 4 bytes, first one likely a counter><samples tightly packed> <other subpackets in the same format>
```

## Packet ID Byte

### First 4 bits (Frequency):
- `0` = frequency not valid
- `1` = 256 Hz
- `2` = 128 Hz
- `3` = 64 Hz
- `4` = 52 Hz
- `5` = 32 Hz
- `6` = 16 Hz
- `7` = 10 Hz
- `8` = 1 Hz
- `9` = 0.1 Hz

### Second 4 bits (Data Type):
- `0` = not valid
- `1` = EEG, 4 channels
- `2` = EEG, 8 channels
- `3` = DRL/REF 
- `4` = Optics, 4 channels
- `5` = Optics, 8 channels
- `6` = Optics, 16 channels
- `7` = Accelerometer + Gyroscope
- `8` = Battery 

**Note**: This leaves quite a few types of data unaccounted for.
In practice, with preset 1045, I was only able to identify EEG, Optics, IMU and battery packets.

## Identified Packets

Packets I was able to identify and how to decode them (all of them use msb and little-endian):

- **EEG**: 2 samples, 8x14 bit integers, `eeg_int* (1450 / 16383)` 
- **IMU**: 3 samples, 6x12bit integers, `gyro_int*-0.0074768`, `acc_int*0.0000610352`
- **OPTICAL**: 3 samples, 4x20bit integers, `optical_int/32768`

### 

**Note**: The conversions are to the values the SDK gives, they might not be the final conversion.

## Presets

Presets for different optics setups (more might exist, not sure what else they contain):

### Optics presets
- **4ch high** - 1046 
- **4ch low** - 1045 - default in MindMonitor
- **8ch high** - 1044
- **8ch low** - 1043
- **16ch high** - 1042
- **16ch low** - 1041

## Reference

I included a quick parser script as reference as well.

Others in the community might fill in the missing pieces, I would look at these repos to check if they support the Athena:
- https://github.com/alexandrebarachant/muse-lsl
- https://github.com/Amused-EEG/amused-py
- https://github.com/kowalej/BlueMuse

## Acknowledgments

I would also like to thank Alexandre Barachant, Adrian Belmans and others in the OpenBrainTalk and NeuroTechX Slacks for their earlier explorations into the device which served as an important jumping off point in my research.
