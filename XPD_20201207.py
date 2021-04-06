"""
File: Autonomous experiments of the dealloyed Ti-Cu metal
Name: Cheng-Chu Chung
----------------------------------------
TODO: plot Ti vs. run(first, second scan...)
"""
import matplotlib.pyplot as plt
import numpy as np
from databroker._drivers.msgpack import BlueskyMsgpackCatalog
import time


def main():
    # xca_db = BlueskyMsgpackCatalog(['/mnt/data/bnl/2020-12_ae/adaptive_reduced/xca/*msgpack'])
    gpcam_db = BlueskyMsgpackCatalog(
        ['D:/Software/Python/SSID/XPD_20201207_TiCuMg_alloy_auto_1/adaptive_reduced/gpcam/*msgpack'])
    # grid_db = BlueskyMsgpackCatalog(['/mnt/data/bnl/2020-12_ae/adaptive_reduced/grid/*msgpack'])
    # print('Scanning numbers:', len(gpcam_db))
    thick_measurements = list(gpcam_db.search({'adaptive_step.snapped.ctrl_thickness': 1}))
    thin_measurements = list(gpcam_db.search({'adaptive_step.snapped.ctrl_thickness': 0}))
    # print('Thick samples:', len(thick_measurements))
    # print('Thin samples:', len(thin_measurements))
    # check_scan_id_and_CPU_time(gpcam_db)

    the_last_scan = -1    # Scan from the last scan
    result = gpcam_db[the_last_scan]     # Extract data from a scan_id
    print(result.metadata['start'])

    # print(result.primary.read())    # Information for each scan, a xarray dataset
    # # Compute the roi
    # peak_location = (2.925, 2.974)  # region of interest (roi) (351) CuMg2
    # q, I, snapped, requested = extract_data(result)
    # roi = compute_peak_area(q, I, *peak_location)
    # print('Region of interest', roi)
    # # Check CPU time
    # otime = result.metadata['start']['original_start_time']
    # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(otime)))

    # # Make a plot of a single measurement
    # fig, ax = plt.subplots()
    # ax.plot(q, I, label=str(snapped.values()))
    # # Label shows: 'ctrl_Ti', 'ctrl_annealing_time', 'ctrl_temp', 'ctrl_thickness'
    # ax.legend()
    # ax.set_xlabel('q')
    # ax.set_ylabel('I')
    # plt.show()


def check_scan_id_and_CPU_time(gpcam_db):
    print('Show Original time and Scan ID')
    time_list = []
    for i in range(1, len(gpcam_db) + 1):   # Extract all information from metadata['start']
        result = gpcam_db[-i]
        otime = result.metadata['start']['original_start_time']     # Assign original_start_time as otime
        time_list.append((time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(otime)),
                                          result.metadata['start']['scan_id']))     # Append (time, scan id)
    time_list.sort()
    for j in range(len(time_list)):
        if time_list[j][0] > '2020-12-11 13:15:00':
            print(time_list[j])


def compute_peak_area(Q, I, q_start, q_stop):
    """
    Integrated area under a peak with estimated background removed.
    Estimates the background by averaging the 3 values on either side
    of the peak and subtracting that as a constant from I before
    integrating.
    Parameters
    ----------
    Q, I : array
        The q-values and binned intensity.  Assumed to be same length.
    q_start, q_stop : float
        The region of q to integrate.  Must be in same units as the Q.
    Returns
    -------
    peak_area : float
    """

    # figure out the index of the start and stop of the q
    # region of interest
    start, stop = np.searchsorted(Q, (q_start, q_stop))
    # add one to stop because we want the index after the end
    # value not the one before
    stop += 1
    # pull out the region of interest from I.
    data_section = I[start:stop]
    # pull out one more q value than I because we want the bin widths.
    q_section = Q[start : stop + 1]
    # compute width of each of the Q bins.
    dQ = np.diff(q_section)
    # estimate the background level by averaging the 3 and and 3 I(q) outside of
    # our ROI in either direction.
    background = (np.mean(I[start - 3 : start]) + np.mean(I[stop : stop + 3])) / 2
    # do the integration!
    return np.sum((data_section - background) * dQ)


def extract_data(h):
    d = h.primary.read()  # this is an xarray
    step = h.metadata['start']['adaptive_step']
    # Average the Q, I(Q) in time (we have 3 measurements at different ys), the snapped ctrl and requested ctrl
    return d['q'].mean('time'), d['mean'].mean('time'), step['snapped'], step['requested']
    # requested: the last one predicted


if __name__ == '__main__':
    main()