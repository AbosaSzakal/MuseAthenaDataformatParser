"""
Graph Helper Module for Real-Time IMU Data Visualization

This module provides self-contained plotting functionality for real-time
accelerometer and gyroscope data visualization using matplotlib.
"""

import threading
import time
from collections import deque
from typing import Optional


# Configuration constants
MAX_PLOT_POINTS = 2000  # Buffer size to capture more samples
IMU_FS = 52.0  # Hz for ACC/GYRO in preset p1045


class GraphHelper:
    """
    Manages real-time plotting of accelerometer and gyroscope data.
    """

    def __init__(self, max_points: int = MAX_PLOT_POINTS, sample_rate: float = IMU_FS):
        """
        Initialize the graph helper with data buffers and configuration.

        Args:
            max_points: Maximum number of data points to display
            sample_rate: IMU sample rate in Hz
        """
        self.max_points = max_points
        self.sample_rate = sample_rate

        # Real-time plotting data buffers
        self.acc_data = {
            'x': deque(maxlen=max_points),
            'y': deque(maxlen=max_points),
            'z': deque(maxlen=max_points)
        }
        self.gyro_data = {
            'x': deque(maxlen=max_points),
            'y': deque(maxlen=max_points),
            'z': deque(maxlen=max_points)
        }

        # Separate timestamp tracking for each sensor type
        self.acc_timestamps = deque(maxlen=max_points)
        self.gyro_timestamps = deque(maxlen=max_points)

        # IMU timing based on device sample rate to preserve true resolution
        self.imu_sample_index = 0  # monotonically increasing sample counter for IMU
        self._pending_gyro_time: Optional[float] = None  # align GYRO time with corresponding ACC sample

        # Plotting control
        self.plot_start_time: Optional[float] = None
        self.stop_plot_event = threading.Event()
        self.plot_thread: Optional[threading.Thread] = None

    def reset(self):
        """Reset all data buffers and timing information."""
        self.acc_data = {
            'x': deque(maxlen=self.max_points),
            'y': deque(maxlen=self.max_points),
            'z': deque(maxlen=self.max_points)
        }
        self.gyro_data = {
            'x': deque(maxlen=self.max_points),
            'y': deque(maxlen=self.max_points),
            'z': deque(maxlen=self.max_points)
        }
        self.acc_timestamps.clear()
        self.gyro_timestamps.clear()
        self.imu_sample_index = 0
        self._pending_gyro_time = None
        self.plot_start_time = None

    def add_acc_sample(self, x: float, y: float, z: float):
        """
        Add an accelerometer sample to the buffer.

        Args:
            x, y, z: Accelerometer data in g
        """
        # Initialize timebase on first sample
        if self.plot_start_time is None:
            self.plot_start_time = time.time()

        # Compute the time for this specific sample from the sample index
        t = self.imu_sample_index / self.sample_rate
        self.imu_sample_index += 1

        self.acc_data['x'].append(x)
        self.acc_data['y'].append(y)
        self.acc_data['z'].append(z)
        self.acc_timestamps.append(t)

        # Remember this time for the subsequent paired GYRO sample (same sample instant)
        self._pending_gyro_time = t

    def add_gyro_sample(self, x: float, y: float, z: float):
        """
        Add a gyroscope sample to the buffer.

        Args:
            x, y, z: Gyroscope data in deg/s
        """
        # Use the most recent ACC sample time if available; otherwise derive from index
        if self._pending_gyro_time is not None:
            t = self._pending_gyro_time
            self._pending_gyro_time = None
        else:
            # Fallback: ensure gyro stays aligned to IMU timebase even if ACC missing
            t = (self.imu_sample_index - 1) / self.sample_rate if self.imu_sample_index > 0 else 0.0

        self.gyro_data['x'].append(x)
        self.gyro_data['y'].append(y)
        self.gyro_data['z'].append(z)
        self.gyro_timestamps.append(t)

    def start_plotting(self):
        """Start the plotting thread."""
        self.stop_plot_event.clear()
        self.plot_thread = threading.Thread(
            target=self._plotter_main,
            name="PlotterThread",
            daemon=True
        )
        self.plot_thread.start()

    def stop_plotting(self, timeout: float = 1.0):
        """
        Stop the plotting thread.

        Args:
            timeout: Maximum time to wait for thread to stop
        """
        self.stop_plot_event.set()
        if self.plot_thread is not None:
            try:
                self.plot_thread.join(timeout=timeout)
            except Exception:
                pass

    def _plotter_main(self):
        """Run matplotlib plotting in a dedicated thread to avoid GUI init on the BLE/asyncio thread."""
        try:
            import matplotlib
            backend_set = False
            for backend in ('TkAgg', 'Qt5Agg', 'QtAgg'):
                try:
                    matplotlib.use(backend)
                    backend_set = True
                    break
                except Exception:
                    continue
            if not backend_set:
                # fallback to non-interactive backend to avoid crashing
                matplotlib.use('Agg')
                print("Warning: No interactive GUI backend available (Tk/Qt missing). Running headless.")
            import matplotlib.pyplot as plt
        except Exception as e:
            print(f"Plotter init failed: {e}")
            return

        plt.ion()
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        fig.suptitle('Real-Time Accelerometer & Gyroscope Data', fontsize=14)

        # Accelerometer subplot
        ax1.set_title('Accelerometer (g)')
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Acceleration')
        ax1.grid(True, alpha=0.3)
        line_acc_x, = ax1.plot([], [], 'r-', label='X', linewidth=0.8, antialiased=True)
        line_acc_y, = ax1.plot([], [], 'g-', label='Y', linewidth=0.8, antialiased=True)
        line_acc_z, = ax1.plot([], [], 'b-', label='Z', linewidth=0.8, antialiased=True)
        ax1.legend(loc='upper right')

        # Gyroscope subplot
        ax2.set_title('Gyroscope (deg/s)')
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Angular Velocity')
        ax2.grid(True, alpha=0.3)
        line_gyro_x, = ax2.plot([], [], 'r-', label='X', linewidth=0.8, antialiased=True)
        line_gyro_y, = ax2.plot([], [], 'g-', label='Y', linewidth=0.8, antialiased=True)
        line_gyro_z, = ax2.plot([], [], 'b-', label='Z', linewidth=0.8, antialiased=True)
        ax2.legend(loc='upper right')

        plt.tight_layout()

        def do_update():
            # Accelerometer - use its own timestamps
            if len(self.acc_data['x']) > 0 and len(self.acc_timestamps) > 0:
                acc_times = list(self.acc_timestamps)
                line_acc_x.set_data(acc_times, list(self.acc_data['x']))
                line_acc_y.set_data(acc_times, list(self.acc_data['y']))
                line_acc_z.set_data(acc_times, list(self.acc_data['z']))
                if len(acc_times) > 1:
                    ax1.set_xlim(acc_times[0], acc_times[-1])
                ax1.relim()
                ax1.autoscale_view(scalex=False, scaley=True)

            # Gyroscope - use its own timestamps
            if len(self.gyro_data['x']) > 0 and len(self.gyro_timestamps) > 0:
                gyro_times = list(self.gyro_timestamps)
                line_gyro_x.set_data(gyro_times, list(self.gyro_data['x']))
                line_gyro_y.set_data(gyro_times, list(self.gyro_data['y']))
                line_gyro_z.set_data(gyro_times, list(self.gyro_data['z']))
                if len(gyro_times) > 1:
                    ax2.set_xlim(gyro_times[0], gyro_times[-1])
                ax2.relim()
                ax2.autoscale_view(scalex=False, scaley=True)

        try:
            while not self.stop_plot_event.is_set():
                do_update()
                # Slightly faster refresh to reduce perceived blockiness without overloading CPU
                plt.pause(0.03)  # ~33 Hz UI update
        finally:
            try:
                plt.ioff()
                # Keep the final plot on screen briefly
                plt.pause(0.1)
            except Exception:
                pass
