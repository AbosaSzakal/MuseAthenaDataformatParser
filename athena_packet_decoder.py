#for testing pasted packet from Wireshark
C_ARRAY = r"""
unsigned char bytes[] = {0x2, 0x2, 0x20, 0xf2, 0x0, 0xee, 0x0, 0x4, 0x0, 0x1b, 0x18, 0x0, 0xeb, 0x41, 0x0, 0x95, 0x61, 0xd1, 0x89, 0x93, 0x1, 0x12, 0x3f, 0x65, 0x0, 0x0, 0xff, 0xff, 0xff, 0x6f, 0x91, 0x0, 0x0, 0xb7, 0xa1, 0xa5, 0x38, 0x2e, 0x2a, 0xd5, 0xff, 0xbf, 0x2a, 0xd, 0x0, 0x68, 0x24, 0x7c, 0x1e, 0xe1, 0xa7, 0xf, 0xea, 0xea, 0x47, 0x2a, 0x18, 0x3d, 0xff, 0xd5, 0xfd, 0xfb, 0xfe, 0x5e, 0x41, 0x4e, 0x0, 0x2e, 0x0, 0xd8, 0xff, 0x93, 0xfd, 0x19, 0xff, 0x3a, 0x41, 0x4a, 0x0, 0x26, 0x0, 0xdf, 0xff, 0x67, 0xfd, 0xd7, 0xfe, 0x34, 0x41, 0x3c, 0x0, 0x39, 0x0, 0xe7, 0xff, 0x47, 0x2b, 0x6e, 0x1, 0x0, 0xdc, 0xfd, 0xdd, 0xfe, 0x77, 0x41, 0x47, 0x0, 0x3e, 0x0, 0xe1, 0xff, 0xb3, 0xfd, 0xc, 0xff, 0x65, 0x41, 0x38, 0x0, 0x3b, 0x0, 0xea, 0xff, 0xa5, 0xfd, 0xde, 0xfe, 0x40, 0x41, 0x40, 0x0, 0x33, 0x0, 0xd9, 0xff, 0x34, 0x34, 0x28, 0xb2, 0xff, 0xc3, 0x71, 0x80, 0x91, 0x6, 0x55, 0x9f, 0x90, 0x19, 0x9, 0xed, 0x71, 0x20, 0x93, 0x6, 0x6b, 0x9f, 0x0, 0x19, 0x9, 0x26, 0x72, 0xe0, 0x96, 0x6, 0x62, 0x9f, 0x90, 0x18, 0x9, 0x34, 0x35, 0xd3, 0x74, 0x0, 0x5d, 0x72, 0xa0, 0x99, 0x6, 0x76, 0x9f, 0x30, 0x18, 0x9, 0x4a, 0x72, 0x10, 0x9a, 0x6, 0x93, 0x9f, 0x40, 0x19, 0x9, 0x4f, 0x72, 0x90, 0x9a, 0x6, 0xa7, 0x9f, 0xd0, 0x1b, 0x9, 0x47, 0x2c, 0xa6, 0xe9, 0x0, 0xbb, 0xfd, 0xd1, 0xfe, 0x96, 0x41, 0x3d, 0x0, 0x25, 0x0, 0xda, 0xff, 0xc0, 0xfd, 0xe3, 0xfe, 0x50, 0x41, 0x4e, 0x0, 0x29, 0x0, 0xe8, 0xff, 0xa7, 0xfd, 0xf1, 0xfe, 0x51, 0x41, 0x49, 0x0, 0x32, 0x0, 0xe4, 0xff};
"""


C_ARRAY = r"""
unsigned char bytes[] = {0x2, 0x2, 0x20, 0xf3, 0x0, 0xef, 0x0, 0x4, 0x0, 0x1b, 0x18, 0x0, 0xec, 0x4a, 0x0, 0x6, 0x63, 0xd1, 0x89, 0x93, 0x1, 0x12, 0x69, 0xd3, 0x0, 0x0, 0x8a, 0xa1, 0x3c, 0x0, 0x75, 0x31, 0x9d, 0xd0, 0x97, 0xe9, 0xb5, 0x5f, 0x1, 0xc0, 0x0, 0x0, 0x0, 0x60, 0xff, 0xff, 0xff, 0x84, 0x21, 0xe9, 0xd7, 0xf6, 0xfd, 0xff, 0x12, 0x6a, 0x7a, 0x0, 0x0, 0xc5, 0xc2, 0x96, 0x61, 0xde, 0x1b, 0xbd, 0x8e, 0x61, 0xed, 0x47, 0x2, 0x2e, 0xda, 0xe7, 0x6d, 0x35, 0xcb, 0x7f, 0xfd, 0x38, 0x2e, 0xa4, 0x10, 0x69, 0x3d, 0x72, 0xc8, 0x53, 0xd, 0x7a, 0x0, 0x0, 0xe2, 0x1f, 0x5e, 0x20, 0xe0, 0x1f, 0x8c, 0x20, 0xe4, 0x1f, 0x60, 0x20, 0xe3, 0x1f, 0x5c, 0x20, 0xe2, 0x1f, 0x46, 0x20, 0xe4, 0x1f, 0x51, 0x20, 0x12, 0x6b, 0xd6, 0x0, 0x0, 0xff, 0x3f, 0x5d, 0xd, 0x0, 0x0, 0x0, 0xb4, 0x9f, 0x3b, 0x38, 0x13, 0xf6, 0xe6, 0x12, 0x68, 0x36, 0x14, 0x5, 0xd, 0x80, 0xe6, 0x5d, 0x89, 0x47, 0xf0, 0x11, 0xf2, 0x12, 0x6c, 0x13, 0x1, 0x0, 0x57, 0x40, 0x1e, 0x91, 0xa9, 0xff, 0xff, 0xf3, 0xa0, 0xed, 0x57, 0xfe, 0x3d, 0xcf, 0x0, 0x40, 0xcd, 0xf7, 0xff, 0xe3, 0x9e, 0x39, 0x24, 0xe9, 0xa8, 0x2d, 0x46, 0xb5, 0x12, 0x6d, 0x31, 0x1, 0x0, 0xe8, 0xa5, 0xbf, 0x9a, 0xe9, 0xe9, 0xf, 0xf2, 0xe0, 0x47, 0x28, 0x5, 0x16, 0xc6, 0xff, 0x3f, 0xd, 0xb, 0x0, 0x0, 0x0, 0x72, 0x5e, 0xcf, 0x47, 0xfb, 0x79, 0xee, 0x12, 0x6e, 0x6e, 0x1, 0x0, 0x3f, 0xf0, 0x5a, 0x27, 0x61, 0x34, 0x52, 0x57, 0x1e, 0xb3, 0x27, 0xf9, 0xcd, 0xb0, 0xcc, 0x48, 0x7b, 0xa3, 0xe9, 0xae, 0xd0, 0xb9, 0xd6, 0x91, 0x55, 0x5b, 0xed, 0x41};
"""

import re
import struct
from typing import List, Dict, Optional, Tuple




def parse_packet(
	data: bytes,
	tag: int,
	tag_index: int,
	verbose: bool = False,
) -> Tuple[int, Optional[str], List[Dict[str, List[float]]], int]:
	"""Parse a packet based on the tag byte found at tag_index.

	Contract:
	- Inputs: data (full bytes buffer), tag (value of data[tag_index]), tag_index (0-based index of tag in data)
	- Output: tuple (next_index, packet_type_name, entries, samples)
		- next_index: index (0-based) immediately AFTER the data this function consumed
		- packet_type_name: one of {"EEG", "ACC_GYRO", "OPTICAL", "BATTERY"} or "UNKNOWN_0xNN" for unknown tags
		- entries: list of {"type": <str>, "data": <list[float]>} extracted from the packet
		  For example: EEG -> one entry {type: "EEG", data: [..16 floats..]}
					   ACC_GYRO -> 6 entries (3x ACC, 3x GYRO), each data has 3 floats
					   OPTICAL -> 3 entries (one per sample), each data has 4 floats
				   BATTERY -> 1 entry with 10 values
		- samples: number of time samples represented in this packet for that modality
	- On insufficient data, raises ValueError.
	- Printing is controlled by the `verbose` flag (disabled by default).
	"""
	# After the tag byte, skip 4 bytes for both known tag types (per spec)
	# Start of payload after skip:
	payload_start = tag_index + 1 + 4

	match tag:
		case 0x12: # 8 channel EEG data x 2 samples (14bit precision) at 256 Hz
			# Parse next 28 bytes as UNSIGNED 14-bit little-endian values, print two EEG lines
			payload_len = 28
			end_index = payload_start + payload_len
			if end_index > len(data):
				raise ValueError(
					f"Not enough data for tag 0x12: need up to index {end_index}, have {len(data)}"
				)
			block28 = data[payload_start:end_index]
			values = parse_uint14_le_values(block28)
			scaled = [v * (1450 / 16383) for v in values]
			mid = len(scaled) // 2
			if verbose:
				print("EEG:", scaled[:mid])
				print("EEG:", scaled[mid:])
			entries = [{"type": "EEG", "data": list(map(float, scaled))}]
			# 2 time samples (across 8 channels)
			return end_index, "EEG", entries, 2
 
		case 0x47: # 3 samples of ACC + GYRO (12bit precision) at 52 Hz
			# Skip 4 bytes, then parse 18 int16_le numbers (3 samples x [ACCx,ACCy,ACCz, GYROx,GYROy,GYROz])
			ints_needed = 18
			bytes_needed = ints_needed * 2
			end_index = payload_start + bytes_needed
			if end_index > len(data):
				raise ValueError(
					f"Not enough data for tag 0x47: need up to index {end_index}, have {len(data)}"
				)
			block = data[payload_start:end_index]
			vals = list(struct.unpack('<18h', block))
			# Print three samples, ACC then GYRO, in the order they appear with scaling corrections
			entries: List[Dict[str, List[float]]] = []
			for i in range(3):
				base = i * 6
				acc_raw = vals[base: base + 3]
				gyro_raw = vals[base + 3: base + 6]
				# Convert to double (float) and apply scaling corrections
				acc_scaled = [float(x) * float(0.0000610352) for x in acc_raw]
				gyro_scaled = [float(x) * float(-0.0074768) for x in gyro_raw]
				if verbose:
					print(f"ACC: {acc_scaled}")
					print(f"GYRO: {gyro_scaled}")
				entries.append({"type": "ACC", "data": acc_scaled})
				entries.append({"type": "GYRO", "data": gyro_scaled})
			# 3 time samples (shared across ACC and GYRO modalities)
			return end_index, "ACC_GYRO", entries, 3

		case 0x34: # 3 samples of 20bit OPTICAL data at 64hz
			bytes_needed = 30
			end_index = payload_start + bytes_needed
			if end_index > len(data):
				raise ValueError(
					f"Not enough data for tag 0x34: need up to index {end_index}, have {len(data)}"
				)
			block = data[payload_start:end_index]
			
			# Convert to bit array for 20-bit parsing
			bits = bytes_to_bitarray_lsb_first(block)
			
			# Parse 3 samples, each with 4x20bit values
			entries: List[Dict[str, List[float]]] = []
			for sample in range(3):
				sample_values = []
				for value in range(4):
					bit_start = (sample * 4 + value) * 20
					bit_end = bit_start + 20
					if bit_end > len(bits):
						raise ValueError(f"Not enough bits for sample {sample}, value {value}")
					
					# Extract 20 bits and convert to integer (little-endian)
					value_bits = bits[bit_start:bit_end]
					int_value = 0
					for bit_index, bit in enumerate(value_bits):
						if bit:
							int_value |= (1 << bit_index)
					sample_values.append(int_value)
				sample_values_scaled = [float(x) / float(32768) for x in sample_values]
				if verbose:
					print(f"Sample {sample + 1}: {sample_values_scaled}")
				entries.append({"type": "OPTICAL", "data": sample_values_scaled})

			# 3 time samples
			return end_index, "OPTICAL", entries, 3

		case 0x98: # BATTERY data - 10 x 16-bit unsigned integers, 0.1hz
			# Skip 4 bytes, then parse 10 16-bit unsigned integers
			# 10 * 16 bits = 160 bits = 20 bytes
			bytes_needed = 20
			end_index = payload_start + bytes_needed
			if end_index > len(data):
				raise ValueError(
					f"Not enough data for tag 0x98: need up to index {end_index}, have {len(data)}"
				)
			block = data[payload_start:end_index]
			
			# Convert to bit array for 16-bit parsing
			bits = bytes_to_bitarray_lsb_first(block)

			# Parse 10 16-bit unsigned integers
			values = []
			for i in range(10):
				bit_start = i * 16
				bit_end = bit_start + 16
				if bit_end > len(bits):
					raise ValueError(f"Not enough bits for 16-bit value {i}")

				# Extract 16 bits and convert to integer (little-endian)
				value_bits = bits[bit_start:bit_end]
				int_value = 0
				for bit_index, bit in enumerate(value_bits):
					if bit:
						int_value |= (1 << bit_index)
				values.append(int_value)
			
			if verbose:
				print(f"BATTERY: {values}")
			entries = [{"type": "BATTERY", "data": [float(v) for v in values]}]
			# Treat battery as 1 sample snapshot
			return end_index, "BATTERY", entries, 1

		case _:
			# Unknown tag: consume nothing beyond the tag itself but return the tag as a type name
			# so the caller can register that an unknown was encountered.
			unknown_name = f"UNKNOWN_0x{tag:02X}"
			if verbose:
				print(f"Unhandled tag 0x{tag:02x} at {tag_index}; returning {unknown_name}.")
			return tag_index + 1, unknown_name, [], 1



def parse_c_array_to_bytes(c_src: str) -> bytes:
	"""Extract integer byte values from a C array initializer string and strip the first 12 bytes.

	Supports hex (0x..), decimal, and ignores any other tokens.
	"""
	# Find the part inside curly braces {...}
	m = re.search(r"\{([^}]*)\}", c_src, flags=re.S)
	if not m:
		raise ValueError("Could not find byte array initializer in C source string.")
	body = m.group(1)
	# Match hex like 0x2a or decimal like 42
	tokens = re.findall(r"0x[0-9a-fA-F]+|\b\d+\b", body)
	values: List[int] = []
	for t in tokens:
		if t.lower().startswith("0x"):
			v = int(t, 16)
		else:
			v = int(t, 10)
		if not (0 <= v <= 0xFF):
			raise ValueError(f"Value out of byte range: {t}")
		values.append(v)
	# Strip the first 12 bytes
	return bytes(values[12:])


def bytes_to_bitarray_lsb_first(data: bytes) -> List[int]:
	"""Convert bytes to a list of bits (0/1), least-significant-bit first per byte."""
	bits: List[int] = []
	for b in data:
		for i in range(8):
			bits.append((b >> i) & 1)
	return bits


def parse_uint14_le_values(buf: bytes) -> List[int]:
	"""Parse a buffer whose bitstream encodes consecutive unsigned 14-bit little-endian values.

	- Little-endian here means the first bit encountered is the least-significant bit of the value
	  (LSB-first bit order across the stream).
	- Unsigned width=14 (no two's complement adjustment).
	Returns a list of 14-bit unsigned integers in range [0, 16383].
	"""
	bits = bytes_to_bitarray_lsb_first(buf)
	width = 14
	n_vals = len(bits) // width
	out: List[int] = []
	for i in range(n_vals):
		chunk = bits[i * width : (i + 1) * width]
		# assemble little-endian from LSB-first bits
		val = 0
		for bit_index, bit in enumerate(chunk):
			if bit:
				val |= (1 << bit_index)
		out.append(val)
	return out


def main():
	data = parse_c_array_to_bytes(C_ARRAY)

	# 1) Convert the C array into a bit array (LSB-first), then print basic info
	bit_array = bytes_to_bitarray_lsb_first(data)
	print(f"Total bytes: {len(data)}; total bits: {len(bit_array)}")

	# 2) Print the 22nd byte in hex (1-based indexing => index 21 in Python)
	if len(data) < 10:
		raise ValueError("Not enough data to access the 10th byte.")
	byte10 = data[9]
	print(f"10th byte: 0x{byte10:02x}")

	# 3) Call the packet parser on the 10th byte/tag and continue parsing in a loop
	next_index = 9  # Start at the 10th byte (0-based index 9)

	while next_index < len(data):
		tag = data[next_index]
		try:
			next_index, _packet_name, _entries, _samples = parse_packet(data, tag, next_index, verbose=False)
		except ValueError as e:
			print(f"Error parsing packet: {e}")
			break

	print(f"Finished parsing. Final index: {next_index}, total data length: {len(data)}")

	# Optional: demonstrate the new packetParser on the same data
	counts = packetParser(data, verbose=True)
	print(f"Packet counts: {counts}")


def packetParser(data: bytes, verbose: bool = False) -> Dict[str, Dict[str, int]]:
	"""Process a raw bytes buffer and count packets and samples per recognized type.

	Returns a dict mapping packet type names to an object:
	  { 'packets': <count of packets>, 'samples': <total samples> }

	Recognized packet type names: "EEG", "ACC_GYRO", "OPTICAL", "BATTERY".
	Unknown tags are returned as type names in the form "UNKNOWN_0xNN". To avoid noise,
	consecutive unknowns are suppressed until a known packet is successfully detected again.
	"""
	counts: Dict[str, Dict[str, int]] = {}
	idx = 0
	n = len(data)
	# When True, we've just seen an unknown; suppress additional unknowns until a known packet is parsed.
	unknown_suppressed = False
	while idx < n:
		tag = data[idx]
		try:
			next_idx, packet_name, _entries, samples = parse_packet(data, tag, idx, verbose=verbose)
		except ValueError as e:
			if verbose:
				print(f"Error parsing at index {idx}: {e}")
			# If we can't parse, advance by 1 to avoid infinite loop
			idx += 1
			continue

		if packet_name:
			# Handle suppression of consecutive unknowns
			if packet_name.startswith("UNKNOWN_0x"):
				if not unknown_suppressed:
					rec = counts.get(packet_name, {"packets": 0, "samples": 0})
					rec["packets"] += 1
					rec["samples"] += int(samples)
					counts[packet_name] = rec
					unknown_suppressed = True
				# else: suppress this unknown occurrence
			else:
				rec = counts.get(packet_name, {"packets": 0, "samples": 0})
				rec["packets"] += 1
				rec["samples"] += int(samples)
				counts[packet_name] = rec
				unknown_suppressed = False
			# Optionally, user can handle `entries` externally if needed

		# Ensure progress
		if next_idx <= idx:
			idx += 1
		else:
			idx = next_idx

	return counts


if __name__ == "__main__":
	main()
