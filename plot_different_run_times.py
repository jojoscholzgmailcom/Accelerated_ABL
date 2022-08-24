import numpy as np
import matplotlib.pyplot as plt

our_run_times = [0, 0.30, 0.36, 0.37, 0.40, 0.42, 0.45, 0.50, 0.55, 0.57, 0.62]
our_run_times_second = [0, 0,  0.48, 0.51, 0.72, 0.74, 1.13, 1.60, 2.65, 3.89, 5.90]
our_run_times_third = [0, 0,  0, 0.63, 0.71, 1.18, 2.90, 6.83, 13.61, 28.17, 43.70]
ABL_original_run_times = [0, 0.20, 0.26, 0.47, 3.61, 14.89, 92.53, 672.37, 2390.68, 4488.23, 10831.01]

#todo: first scenario: our method vs original

# fig = plt.figure()
# ax = fig.add_subplot(1,1,1)
# ax.plot(range(11), our_run_times, "b", label="Our Method")
# ax.plot(range(11), ABL_original_run_times, "r", label="Original ABL")
# ax.set_xlabel("Number of Locations in the Scenario")
# ax.set_ylabel("Logarithmic run-time in seconds ($Log_{10} x$)")
# plt.yscale('log',basey=10)
# plt.legend()
# plt.show()

#todo: comparison of the proposed approach with different relevant states
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(range(11), our_run_times, label="1 relevant location")
ax.plot(range(11), our_run_times_second,'*-', label="2 relevant locations")
ax.plot(range(11), our_run_times_third,'.-', label="3 relevant locations")
ax.set_xlabel("Number of Locations in the Scenario")
ax.set_ylabel("run-time in seconds")
# plt.yscale('log',basey=10)
plt.legend()
plt.show()
